"""Cross-signal findings derived from the shared graph."""

from __future__ import annotations

import networkx as nx

from qualgraph.findings.model import Finding
from qualgraph.graph.schema import NodeType


def detect_untested_hotspots(
    graph: nx.DiGraph,
    complexity_pct: float = 0.8,
    centrality_pct: float = 0.7,
) -> list[Finding]:
    funcs = [
        (node_id, attrs)
        for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") in {NodeType.FUNCTION, NodeType.FUNCTION.value, NodeType.METHOD, NodeType.METHOD.value}
        and attrs.get("complexity") is not None
    ]
    if not funcs:
        return []

    cx_threshold = _percentile([float(attrs["complexity"]) for _node_id, attrs in funcs], complexity_pct)
    cn_threshold = _percentile([float(attrs.get("centrality") or 0.0) for _node_id, attrs in funcs], centrality_pct)
    findings: list[Finding] = []
    for node_id, attrs in funcs:
        complexity = float(attrs["complexity"])
        centrality = float(attrs.get("centrality") or 0.0)
        if (
            complexity >= cx_threshold
            and centrality >= cn_threshold
            and float(attrs.get("coverage_line") or 0.0) == 0.0
        ):
            findings.append(
                Finding(
                    node_id=node_id,
                    kind="untested_hotspot",
                    severity="high",
                    evidence={
                        "complexity": complexity,
                        "centrality": centrality,
                        "coverage": 0.0,
                    },
                )
            )
    return findings


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    bounded = min(max(percentile, 0.0), 1.0)
    ordered = sorted(values)
    index = round((len(ordered) - 1) * bounded)
    return ordered[index]
