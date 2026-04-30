"""High-level LLM analysis entry points."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Iterable

import networkx as nx

from qualgraph.annotators.findings import add_finding
from qualgraph.cache.sqlite import cache_key, normalized_function_body
from qualgraph.llm.client import LLMClient, LLMProvider, LLMRequest, LLMResponse
from qualgraph.llm.context import PROMPT_TEMPLATE_VERSION, SYSTEM_PROMPT, build_context, evidence_corpus
from qualgraph.llm.context import render_analysis_prompt
from qualgraph.llm.parser import parse_analysis_response
from qualgraph.logging import RunLogger
from qualgraph.scoring.risk import score as score_risk


LANGUAGE_VERSION = "py3.11"
ANNOTATOR_NAME = "llm_analysis"
ANNOTATOR_VERSION = "1.0"


@dataclass(slots=True)
class NodeAnalysisRequest:
    node_id: str
    context: str
    system: str = "You are a careful code quality analyst. Return concise, evidence-backed findings."
    prompt_template: str = "node_analysis"


@dataclass(slots=True)
class AnalysisSummary:
    ranked: int = 0
    analyzed: int = 0
    cache_hits: int = 0
    llm_calls: int = 0
    findings_added: int = 0
    dry_run: bool = False
    dry_run_tasks: list[dict[str, Any]] = field(default_factory=list)


class LLMAnalyzer:
    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def analyze_node(self, request: NodeAnalysisRequest) -> LLMResponse:
        return self.client.complete(
            LLMRequest(
                system=request.system,
                user=request.context,
                node_id=request.node_id,
                prompt_template=request.prompt_template,
            )
        )

    def analyze_nodes(self, requests: Iterable[NodeAnalysisRequest]) -> list[LLMResponse]:
        return [self.analyze_node(request) for request in requests]


def analyze_top_n(
    graph: nx.DiGraph,
    top_n: int,
    provider: LLMProvider,
    cache: Any,
    logger: RunLogger | None = None,
    dry_run: bool = False,
) -> AnalysisSummary:
    """Analyze the highest-risk nodes with cache-first, evidence-validated LLM calls."""

    ranked = sorted(
        [
            (node_id, float(attrs["risk_score"]))
            for node_id, attrs in graph.nodes(data=True)
            if attrs.get("risk_score") is not None
        ],
        key=lambda item: -item[1],
    )[:top_n]
    summary = AnalysisSummary(ranked=len(ranked), dry_run=dry_run)
    client = LLMClient(provider, run_logger=logger)

    for node_id, risk_score in ranked:
        ctx = build_context(graph, node_id)
        key = _cache_key(ctx, provider.model_id)
        request = build_request(ctx, node_id=node_id)
        if dry_run:
            summary.dry_run_tasks.append(
                {
                    "node_id": node_id,
                    "risk_score": risk_score,
                    "cache_key": key,
                    "model": provider.model_id,
                    "system": request.system,
                    "user": request.user,
                }
            )
            if logger is not None:
                logger.log_event(
                    "llm_analysis_dry_run",
                    node_id=node_id,
                    risk_score=risk_score,
                    model=provider.model_id,
                    cache_key=key,
                )
            continue

        cached = cache.get(key)
        if cached is not None:
            findings = cached
            summary.cache_hits += 1
            if logger is not None:
                logger.log_event("llm_analysis_cache_hit", node_id=node_id, cache_key=key)
        else:
            response = client.complete(request)
            findings = parse_response(response.text, ctx)
            cache.put(key, findings)
            summary.llm_calls += 1

        graph.nodes[node_id]["llm_findings"] = findings
        graph.nodes[node_id]["llm_analyzed"] = True
        graph.nodes[node_id]["llm_no_findings"] = not findings
        summary.findings_added += _attach_findings(graph.nodes[node_id], findings)
        summary.analyzed += 1

    if not dry_run:
        score_risk(graph)
    return summary


def build_request(ctx: dict[str, Any], node_id: str | None = None) -> LLMRequest:
    return LLMRequest(
        system=SYSTEM_PROMPT,
        user=render_analysis_prompt(ctx),
        cache_keys=["system"],
        node_id=node_id,
        prompt_template=PROMPT_TEMPLATE_VERSION,
    )


def parse_response(response_text: str, ctx: dict[str, Any]) -> list[dict[str, Any]]:
    parsed = parse_analysis_response(response_text, evidence_corpus(ctx))
    return parsed["findings"]


def _cache_key(ctx: dict[str, Any], model_id: str) -> str:
    return cache_key(
        language_version=LANGUAGE_VERSION,
        grammar_version=_grammar_version(),
        normalized_function_body=normalized_function_body(ctx["target"].get("source") or ""),
        annotator_name=ANNOTATOR_NAME,
        annotator_version=ANNOTATOR_VERSION,
        model_id=model_id,
        prompt_template_version=PROMPT_TEMPLATE_VERSION,
    )


def _grammar_version() -> str:
    try:
        return version("tree-sitter-python")
    except PackageNotFoundError:
        return "unknown"


def _attach_findings(attrs: dict[str, Any], findings: list[dict[str, Any]]) -> int:
    attrs["findings"] = [
        finding
        for finding in attrs.get("findings", []) or []
        if not isinstance(finding, dict) or finding.get("source") != "llm"
    ]
    added = 0
    max_severity = 0.0
    for finding in findings:
        payload = _finding_payload(finding)
        max_severity = max(max_severity, payload["severity_num"])
        if add_finding(attrs, payload):
            added += 1
    attrs["llm_severity_max"] = max_severity
    return added


def _finding_payload(finding: dict[str, Any]) -> dict[str, Any]:
    severity = str(finding.get("severity") or "low").lower()
    dimension = str(finding.get("dimension") or "maintainability")
    title = str(finding.get("title") or dimension)
    description = str(finding.get("description") or title)
    return {
        "source": "llm",
        "code": dimension,
        "severity": severity.upper(),
        "severity_num": _severity_num(severity),
        "confidence": finding.get("confidence") or "AMBIGUOUS",
        "message": description,
        "dimension": dimension,
        "title": title,
        "description": description,
        "evidence": finding.get("evidence") or "",
        "suggested_action": finding.get("suggested_action"),
    }


def _severity_num(severity: str) -> float:
    return {"critical": 1.0, "high": 0.85, "medium": 0.66, "low": 0.33}.get(severity, 0.0)
