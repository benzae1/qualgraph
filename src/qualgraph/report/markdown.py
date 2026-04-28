"""Markdown report rendering."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import networkx as nx


def render_markdown_report(graph: nx.DiGraph) -> str:
    nodes = list(graph.nodes(data=True))
    edges = list(graph.edges(data=True))
    node_types = Counter(attrs.get("type", "unknown") for _node_id, attrs in nodes)
    edge_types = Counter(attrs.get("type", "unknown") for _source, _target, attrs in edges)
    findings_total = sum(len(attrs.get("findings", [])) for _node_id, attrs in nodes)
    covered = [attrs["coverage_line"] for _node_id, attrs in nodes if attrs.get("coverage_line") is not None]
    avg_coverage = sum(covered) / len(covered) if covered else None

    lines = [
        "# Qualgraph Report",
        "",
        "## Summary",
        "",
        f"- Nodes: {graph.number_of_nodes()}",
        f"- Edges: {graph.number_of_edges()}",
        f"- Clusters: {graph.graph.get('cluster_count', 'unknown')}",
        f"- Findings: {findings_total}",
    ]
    if avg_coverage is not None:
        lines.append(f"- Average line coverage: {avg_coverage:.1%}")

    lines.extend(["", "## Node Types", ""])
    lines.extend(f"- {node_type}: {count}" for node_type, count in sorted(node_types.items()))

    lines.extend(["", "## Edge Types", ""])
    lines.extend(f"- {edge_type}: {count}" for edge_type, count in sorted(edge_types.items()))

    lines.extend(["", "## Top Structural Nodes", ""])
    for _node_id, attrs in _top_nodes(nodes):
        lines.append(
            "- "
            f"{attrs.get('qualified_name', attrs.get('name'))} "
            f"({attrs.get('type')}, centrality={float(attrs.get('centrality') or 0):.3f}, "
            f"role={attrs.get('cluster_role') or 'unknown'})"
        )

    lines.extend(["", "## Findings By Tool", ""])
    tool_counts = Counter(
        finding.get("source", "unknown")
        for _node_id, attrs in nodes
        for finding in attrs.get("findings", [])
        if isinstance(finding, dict)
    )
    if tool_counts:
        lines.extend(f"- {tool}: {count}" for tool, count in sorted(tool_counts.items()))
    else:
        lines.append("- none")

    lines.extend(["", "## Coverage Gaps", ""])
    gaps = [
        attrs
        for _node_id, attrs in nodes
        if attrs.get("coverage_line") is not None and attrs.get("coverage_line", 1.0) < 0.8
    ]
    for attrs in sorted(gaps, key=lambda item: item.get("coverage_line") or 0)[:10]:
        lines.append(
            f"- {attrs.get('qualified_name')}: {float(attrs.get('coverage_line') or 0):.1%} "
            f"({attrs.get('file_path')}:{attrs.get('line_start')})"
        )
    if not gaps:
        lines.append("- none")

    return "\n".join(lines) + "\n"


def write_markdown_report(graph: nx.DiGraph, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown_report(graph), encoding="utf-8")
    return output_path


def _top_nodes(nodes: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    return sorted(
        nodes,
        key=lambda item: (
            float(item[1].get("centrality") or 0),
            int(item[1].get("out_degree") or 0),
            int(item[1].get("in_degree") or 0),
        ),
        reverse=True,
    )[:10]
