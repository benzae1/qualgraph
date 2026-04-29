"""Build graph-aware LLM prompts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
import networkx as nx


SYSTEM_PROMPT = (
    "You are a careful code quality analyst. Use only the evidence in the task. "
    "Return concise, actionable findings as valid JSON."
)
PROMPT_TEMPLATE_VERSION = "analysis-v1"


def build_node_analysis_prompt(graph: nx.DiGraph, node_id: str) -> tuple[str, str]:
    return SYSTEM_PROMPT, render_analysis_prompt(build_context(graph, node_id))


def build_context(
    graph: nx.DiGraph,
    node_id: str,
    max_callers: int = 3,
    max_callees: int = 5,
) -> dict[str, Any]:
    node_attrs = graph.nodes[node_id]
    callers = sorted(
        graph.predecessors(node_id),
        key=lambda item: graph.nodes[item].get("centrality", 0) or 0,
        reverse=True,
    )[:max_callers]
    callees = list(graph.successors(node_id))[:max_callees]
    cluster_nodes = [
        candidate
        for candidate, attrs in graph.nodes(data=True)
        if attrs.get("cluster_id") == node_attrs.get("cluster_id")
    ]
    return {
        "target": _node_summary(graph, node_id, include_source=True),
        "callers": [_node_summary(graph, caller, include_source=True) for caller in callers],
        "callees": [_node_summary(graph, callee, include_source=True) for callee in callees],
        "cluster": {
            "id": node_attrs.get("cluster_id"),
            "size": len(cluster_nodes),
            "role": node_attrs.get("cluster_role"),
        },
        "static_findings": node_attrs.get("findings", []),
        "test_status": {
            "coverage_line": node_attrs.get("coverage_line"),
            "test_count": node_attrs.get("test_count", 0),
        },
        "git_summary": {
            "churn": node_attrs.get("churn"),
            "bug_fixes": node_attrs.get("bug_fix_keywords"),
        },
    }


def render_analysis_prompt(context: dict[str, Any]) -> str:
    return _template_env().get_template("analysis.j2").render(**context)


def evidence_corpus(context: dict[str, Any]) -> str:
    nodes = [context.get("target") or {}, *context.get("callers", []), *context.get("callees", [])]
    return "\n".join(str(node.get("source") or "") for node in nodes)


def _node_summary(graph: nx.DiGraph, node_id: str, include_source: bool = False) -> dict[str, Any]:
    attrs = graph.nodes[node_id]
    keys = [
        "id",
        "type",
        "name",
        "qualified_name",
        "file_path",
        "line_start",
        "line_end",
        "complexity",
        "coverage_line",
        "churn",
        "centrality",
        "risk_score",
    ]
    summary = {key: attrs.get(key) for key in keys if attrs.get(key) is not None}
    if include_source:
        summary["source"] = _truncate(attrs.get("source") or "", 6000)
    return summary


def _template_env() -> Environment:
    template_dir = Path(__file__).parent / "prompts"
    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(default=False),
    )


def _truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "\n... truncated ..."
