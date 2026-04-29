"""Markdown report rendering."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.findings import finding_key


def render_markdown_report(graph: nx.DiGraph) -> str:
    nodes = list(graph.nodes(data=True))
    edges = list(graph.edges(data=True))
    node_types = Counter(attrs.get("type", "unknown") for _node_id, attrs in nodes)
    edge_types = Counter(attrs.get("type", "unknown") for _source, _target, attrs in edges)
    finding_records = _finding_records(nodes)
    findings_total = len(finding_records)
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
        in_degree = int(attrs.get("in_degree") or 0)
        out_degree = int(attrs.get("out_degree") or 0)
        lines.append(
            "- "
            f"{attrs.get('qualified_name', attrs.get('name'))} "
            f"({attrs.get('type')}, score={_format_score(attrs.get('structural_score', attrs.get('centrality')))}, "
            f"degree={in_degree + out_degree} in/out={in_degree}/{out_degree}, "
            f"betweenness={_format_small(attrs.get('betweenness_centrality', attrs.get('centrality')))}, "
            f"role={attrs.get('cluster_role') or 'unknown'})"
        )

    lines.extend(["", "## Findings By Tool", ""])
    lines.append("_Deduped by node, tool, rule, location, and message._")
    lines.append("")
    tool_counts = Counter(record["finding"].get("source", "unknown") for record in finding_records)
    if tool_counts:
        for tool, count in sorted(tool_counts.items()):
            records = [record for record in finding_records if record["finding"].get("source", "unknown") == tool]
            prod_count = sum(1 for record in records if not _is_test_node(record["node"]))
            test_count = count - prod_count
            top_rules = _top_rule_text(records, limit=3)
            lines.append(f"- {tool}: {count} total ({prod_count} production, {test_count} test); top rules: {top_rules}")
    else:
        lines.append("- none")

    lines.extend(["", "## Top Finding Rules", ""])
    top_rules = _top_rules(finding_records, limit=10)
    if top_rules:
        for (source, code, message), count in top_rules:
            lines.append(f"- {source} {code}: {count} - {_shorten(message)}")
    else:
        lines.append("- none")

    lines.extend(["", "## Priority Findings", ""])
    priority_findings = _priority_findings(finding_records, limit=10)
    if priority_findings:
        for record in priority_findings:
            finding = record["finding"]
            node = record["node"]
            lines.append(
                "- "
                f"{node.get('qualified_name')}: "
                f"{finding.get('source')} {_finding_code(finding)} "
                f"{_severity_text(finding)}- {_shorten(finding.get('message'))} "
                f"({node.get('file_path')}:{_finding_line(finding, node)})"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Risk Hotspots", ""])
    hotspots = _risk_hotspots(nodes, finding_records, limit=10)
    if hotspots:
        for score, attrs, finding_count in hotspots:
            coverage = attrs.get("coverage_line")
            coverage_text = "unknown" if coverage is None else f"{float(coverage):.1%}"
            lines.append(
                "- "
                f"{attrs.get('qualified_name')}: score={score:.1f}, findings={finding_count}, "
                f"coverage={coverage_text}, complexity={attrs.get('complexity') or 'n/a'}, "
                f"churn={attrs.get('churn') or 0} ({attrs.get('file_path')}:{attrs.get('line_start')})"
            )
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

    lines.extend(["", "## Test Linkage", ""])
    lines.extend(_test_linkage_lines(nodes, edges))

    lines.extend(["", "## Git History", ""])
    lines.extend(_git_history_lines(nodes))

    lines.extend(["", "## Co-Change", ""])
    lines.extend(_co_change_lines(edges))

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
            float(item[1].get("structural_score", item[1].get("centrality")) or 0),
            int(item[1].get("out_degree") or 0) + int(item[1].get("in_degree") or 0),
            int(item[1].get("out_degree") or 0),
        ),
        reverse=True,
    )[:10]


def _finding_records(nodes: list[tuple[str, dict]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for node_id, attrs in nodes:
        for finding in attrs.get("findings", []) or []:
            if not isinstance(finding, dict):
                continue
            key = (node_id, *finding_key(finding))
            if key in seen:
                continue
            seen.add(key)
            records.append({"node_id": node_id, "node": attrs, "finding": finding})
    return records


def _top_rules(records: list[dict[str, Any]], limit: int) -> list[tuple[tuple[str, str, str], int]]:
    messages: dict[tuple[str, str], str] = {}
    counts: Counter[tuple[str, str]] = Counter()
    for record in records:
        finding = record["finding"]
        source = finding.get("source", "unknown")
        code = _finding_code(finding)
        counts[(source, code)] += 1
        messages.setdefault((source, code), finding.get("message") or "")
    return [((source, code, messages[(source, code)]), count) for (source, code), count in counts.most_common(limit)]


def _top_rule_text(records: list[dict[str, Any]], limit: int) -> str:
    rules = _top_rules(records, limit)
    if not rules:
        return "none"
    return ", ".join(f"{code} ({count})" for (_source, code, _message), count in rules)


def _priority_findings(records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    filtered = [record for record in records if not _is_low_signal_finding(record)]
    return sorted(filtered, key=_priority_key)[:limit]


def _priority_key(record: dict[str, Any]) -> tuple[int, int, int, str]:
    finding = record["finding"]
    test_rank = 1 if _is_test_node(record["node"]) else 0
    source_rank = {"bandit": 0, "vulture": 1, "ruff": 2}.get(finding.get("source"), 3)
    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(str(finding.get("severity") or "").upper(), 3)
    return (test_rank, source_rank, severity_rank, str(record["node"].get("qualified_name") or ""))


def _is_low_signal_finding(record: dict[str, Any]) -> bool:
    finding = record["finding"]
    code = _finding_code(finding)
    if code.startswith("D"):
        return True
    if _is_test_node(record["node"]) and code in {"S101", "B101"}:
        return True
    return False


def _risk_hotspots(
    nodes: list[tuple[str, dict]],
    finding_records: list[dict[str, Any]],
    limit: int,
) -> list[tuple[float, dict, int]]:
    findings_by_node = Counter(record["node_id"] for record in finding_records if not _is_low_signal_finding(record))
    hotspots: list[tuple[float, dict, int]] = []
    for node_id, attrs in nodes:
        if attrs.get("type") not in {"Function", "Method"}:
            continue
        finding_count = findings_by_node[node_id]
        if attrs.get("risk_score") is not None:
            score = float(attrs.get("risk_score") or 0.0)
        else:
            coverage = attrs.get("coverage_line")
            coverage_penalty = 0.0 if coverage is None else max(0.0, 1.0 - float(coverage)) * 5
            complexity = float(attrs.get("complexity") or 0.0)
            churn = float(attrs.get("churn") or 0.0)
            structural = float(attrs.get("structural_score", attrs.get("centrality")) or 0.0)
            score = finding_count + coverage_penalty + min(complexity / 5, 3.0) + min(churn / 10, 3.0) + structural
        if score > 0:
            hotspots.append((score, attrs, finding_count))
    return sorted(hotspots, key=lambda item: item[0], reverse=True)[:limit]


def _test_linkage_lines(nodes: list[tuple[str, dict]], edges: list[tuple[str, str, dict]]) -> list[str]:
    production = {
        node_id: attrs
        for node_id, attrs in nodes
        if attrs.get("type") in {"Function", "Method"} and not _is_test_node(attrs)
    }
    tested_nodes = {source for source, _target, attrs in edges if attrs.get("type") == "tested_by"}
    tested_count = len(set(production) & tested_nodes)
    lines = [f"- Tested production functions/methods: {tested_count}/{len(production)}"]
    untested = [
        attrs
        for node_id, attrs in production.items()
        if node_id not in tested_nodes and (attrs.get("coverage_line") is None or float(attrs.get("coverage_line") or 0) < 0.8)
    ]
    for attrs in sorted(untested, key=lambda item: float(item.get("coverage_line") or 0))[:10]:
        coverage = attrs.get("coverage_line")
        coverage_text = "unknown" if coverage is None else f"{float(coverage):.1%}"
        lines.append(f"- Untested/weakly tested: {attrs.get('qualified_name')} ({coverage_text}, {attrs.get('file_path')}:{attrs.get('line_start')})")
    if len(lines) == 1:
        lines.append("- No untested production functions with low coverage.")
    return lines


def _git_history_lines(nodes: list[tuple[str, dict]]) -> list[str]:
    files: dict[str, dict[str, Any]] = {}
    for _node_id, attrs in nodes:
        file_path = attrs.get("file_path")
        if not file_path or attrs.get("churn") is None:
            continue
        current = files.setdefault(file_path, {"churn": 0, "author_count": 0, "bug_fix_keywords": 0})
        current["churn"] = max(current["churn"], int(attrs.get("churn") or 0))
        current["author_count"] = max(current["author_count"], int(attrs.get("author_count") or 0))
        current["bug_fix_keywords"] = max(current["bug_fix_keywords"], int(attrs.get("bug_fix_keywords") or 0))
    if not files:
        return ["- No git history annotations available."]
    lines = []
    for file_path, attrs in sorted(files.items(), key=lambda item: item[1]["churn"], reverse=True)[:10]:
        lines.append(
            f"- {file_path}: churn={attrs['churn']}, authors={attrs['author_count']}, "
            f"bugfix commits={attrs['bug_fix_keywords']}"
        )
    return lines


def _co_change_lines(edges: list[tuple[str, str, dict]]) -> list[str]:
    co_changes = [(source, target, attrs) for source, target, attrs in edges if attrs.get("type") == "co_changes_with"]
    if not co_changes:
        return ["- No co-change pairs met the configured threshold."]
    lines = []
    for source, target, attrs in sorted(co_changes, key=lambda item: item[2].get("co_change_count") or 0, reverse=True)[:10]:
        lines.append(
            f"- {source} <-> {target}: count={attrs.get('co_change_count')}, "
            f"rate={float(attrs.get('co_change_rate') or 0):.1%}"
        )
    return lines


def _is_test_node(attrs: dict[str, Any]) -> bool:
    file_path = str(attrs.get("file_path") or "")
    return attrs.get("type") == "TestFunction" or file_path.startswith("tests/")


def _finding_code(finding: dict[str, Any]) -> str:
    return str(finding.get("code") or finding.get("test_id") or "unknown")


def _finding_line(finding: dict[str, Any], attrs: dict[str, Any]) -> Any:
    location = finding.get("location")
    if isinstance(location, dict) and location.get("row") is not None:
        return location["row"]
    return finding.get("line") or attrs.get("line_start")


def _severity_text(finding: dict[str, Any]) -> str:
    severity = finding.get("severity")
    confidence = finding.get("confidence")
    if severity and confidence:
        return f"[{severity}/{confidence}] "
    if severity:
        return f"[{severity}] "
    return ""


def _format_score(value: Any) -> str:
    return f"{float(value or 0.0):.3f}"


def _format_small(value: Any) -> str:
    number = float(value or 0.0)
    if number == 0:
        return "0"
    if abs(number) < 0.0001:
        return f"{number:.2e}"
    return f"{number:.4f}"


def _shorten(value: Any, limit: int = 110) -> str:
    text = str(value or "").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."
