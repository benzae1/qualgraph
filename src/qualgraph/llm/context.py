"""Build graph-aware LLM prompts."""

from __future__ import annotations

import json
from typing import Any

import networkx as nx


SYSTEM_PROMPT = (
    "You are a careful code quality analyst. Use only the evidence in the task. "
    "Return concise, actionable findings as valid JSON."
)


def build_node_analysis_prompt(graph: nx.DiGraph, node_id: str) -> tuple[str, str]:
    attrs = graph.nodes[node_id]
    payload = {
        "node": _node_payload(attrs),
        "risk_components": attrs.get("risk_components") or {},
        "existing_findings": attrs.get("findings") or [],
        "neighbors": _neighbor_payload(graph, node_id),
        "source": _truncate(attrs.get("source") or "", 6000),
    }
    user = (
        "Analyze this code graph node for maintainability, reliability, security, "
        "and performance issues.\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "findings": [\n'
        "    {\n"
        '      "kind": "short_snake_case",\n'
        '      "severity": "LOW|MEDIUM|HIGH",\n'
        '      "confidence": "EXTRACTED|INFERRED|AMBIGUOUS",\n'
        '      "message": "one sentence",\n'
        '      "evidence": {"key": "value"},\n'
        '      "suggested_action": "one sentence",\n'
        '      "line": 123\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "If there is no meaningful issue, return {\"findings\": []}.\n\n"
        "Task evidence:\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )
    return SYSTEM_PROMPT, user


def _node_payload(attrs: dict[str, Any]) -> dict[str, Any]:
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
    return {key: attrs.get(key) for key in keys if attrs.get(key) is not None}


def _neighbor_payload(graph: nx.DiGraph, node_id: str) -> list[dict[str, Any]]:
    neighbors: list[dict[str, Any]] = []
    for _source, target, attrs in graph.out_edges(node_id, data=True):
        target_attrs = graph.nodes[target]
        neighbors.append(
            {
                "direction": "out",
                "edge_type": attrs.get("type"),
                "node_id": target,
                "qualified_name": target_attrs.get("qualified_name"),
                "type": target_attrs.get("type"),
            }
        )
    for source, _target, attrs in graph.in_edges(node_id, data=True):
        source_attrs = graph.nodes[source]
        neighbors.append(
            {
                "direction": "in",
                "edge_type": attrs.get("type"),
                "node_id": source,
                "qualified_name": source_attrs.get("qualified_name"),
                "type": source_attrs.get("type"),
            }
        )
    return neighbors[:30]


def _truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "\n... truncated ..."
