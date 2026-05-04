"""Composite risk scoring for LLM candidate selection."""

from __future__ import annotations

from typing import Any, Mapping

import networkx as nx

from qualgraph.graph.schema import NodeType


DEFAULT_WEIGHTS: dict[str, float] = {
    "w1": 1.0,
    "w2": 1.0,
    "w3": 1.0,
    "w4": 1.0,
    "w5": 1.0,
    "w6": 1.0,
    "w7": 1.0,
}


def score(graph: nx.DiGraph, weights: Mapping[str, float] | None = None) -> None:
    """Write composite risk scores onto function and method nodes."""

    active_weights = {**DEFAULT_WEIGHTS, **dict(weights or {})}
    funcs = [
        (node_id, attrs)
        for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") in {NodeType.FUNCTION, NodeType.FUNCTION.value, NodeType.METHOD, NodeType.METHOD.value}
    ]
    if not funcs:
        return

    coverage_available = any(attrs.get("coverage_line") is not None for _node_id, attrs in funcs)
    graph.graph["coverage_available"] = coverage_available

    percentile_ranks: dict[str, list[float]] = {}
    for component in ("centrality", "complexity", "churn", "hotpath"):
        values = [float(attrs.get(component) or 0.0) for _node_id, attrs in funcs]
        if component == "hotpath":
            values = [float(attrs.get("cpu_pct") or attrs.get("hotpath_weight") or 0.0) for _node_id, attrs in funcs]
        percentile_ranks[component] = _rankdata(values)

    for index, (_node_id, attrs) in enumerate(funcs):
        security_max = max(
            (
                _severity_num(finding)
                for finding in attrs.get("findings", []) or []
                if isinstance(finding, dict) and finding.get("source") == "bandit"
            ),
            default=0.0,
        )
        coverage = attrs.get("coverage_line")
        coverage_gap = 0.0 if coverage is None else 1.0 - float(coverage or 0.0)
        hotpath_raw = float(attrs.get("cpu_pct") or attrs.get("hotpath_weight") or 0.0)
        components = {
            "centrality": active_weights["w1"] * percentile_ranks["centrality"][index],
            "complexity": active_weights["w2"] * percentile_ranks["complexity"][index],
            "churn": active_weights["w3"] * percentile_ranks["churn"][index],
            "security": active_weights["w5"] * security_max,
            "llm": active_weights["w6"] * float(attrs.get("llm_severity_max") or 0.0),
            "hotpath": active_weights["w7"] * (percentile_ranks["hotpath"][index] if hotpath_raw > 0 else 0.0),
        }
        if coverage_available:
            components["coverage_gap"] = active_weights["w4"] * coverage_gap
        attrs["risk_score"] = float(sum(components.values()))
        attrs["risk_components"] = components


def top_risk_nodes(graph: nx.DiGraph, limit: int = 50) -> list[tuple[str, dict[str, Any]]]:
    """Return the highest-risk function/method nodes after scoring."""

    funcs = [
        (node_id, attrs)
        for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") in {NodeType.FUNCTION, NodeType.FUNCTION.value, NodeType.METHOD, NodeType.METHOD.value}
        and not _is_test_attrs(attrs)
    ]
    return sorted(funcs, key=lambda item: float(item[1].get("risk_score") or 0.0), reverse=True)[:limit]


def _is_test_attrs(attrs: dict[str, Any]) -> bool:
    file_path = str(attrs.get("file_path") or "").replace("\\", "/")
    return (
        attrs.get("type") == NodeType.TEST_FUNCTION.value
        or file_path.startswith("tests/")
        or "/tests/" in file_path
        or file_path.rsplit("/", 1)[-1].startswith("test_")
    )


def _rankdata(values: list[float]) -> list[float]:
    if not values:
        return []
    ordered = sorted((value, index) for index, value in enumerate(values))
    ranks = [0.0] * len(values)
    position = 0
    while position < len(ordered):
        end = position + 1
        while end < len(ordered) and ordered[end][0] == ordered[position][0]:
            end += 1
        average_rank = ((position + 1) + end) / 2
        for _value, original_index in ordered[position:end]:
            ranks[original_index] = average_rank / len(values)
        position = end
    return ranks


def _severity_num(finding: dict[str, Any]) -> float:
    explicit = finding.get("severity_num")
    if explicit is not None:
        return float(explicit)
    return {
        "HIGH": 1.0,
        "MEDIUM": 0.66,
        "LOW": 0.33,
    }.get(str(finding.get("severity") or "").upper(), 0.0)
