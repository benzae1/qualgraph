"""Markdown report rendering."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import networkx as nx
from jinja2 import Environment, FileSystemLoader, select_autoescape

from qualgraph.annotators.findings import finding_key
from qualgraph.findings.cross_signal import detect_cross_signal_findings
from qualgraph.findings.model import Finding


CROSS_SIGNAL_SOURCE = "cross-signal"


def render_markdown_report(graph: nx.DiGraph, top_n: int = 10) -> str:
    return _template_env().get_template("report.md.j2").render(**build_report_context(graph, top_n=top_n))


def build_report_context(graph: nx.DiGraph, top_n: int = 10) -> dict[str, Any]:
    nodes = list(graph.nodes(data=True))
    edges = list(graph.edges(data=True))
    run_summary = _latest_run_summary(graph)
    finding_records = _finding_records(graph, nodes)
    actionable_records = [record for record in finding_records if _is_actionable_record(record)]
    covered = [float(attrs["coverage_line"]) for _node_id, attrs in nodes if attrs.get("coverage_line") is not None]
    avg_coverage = sum(covered) / len(covered) if covered else None
    top_findings = _priority_findings(actionable_records, limit=3)
    risk_nodes = _risk_nodes(nodes, finding_records, limit=top_n)
    clusters = _clusters(nodes, finding_records, risk_nodes)
    cluster_stats = _cluster_stats(nodes, clusters)
    non_actionable = max(0, len(finding_records) - len(actionable_records))
    return {
        "summary": {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "clusters": cluster_stats["label"],
            "findings": len(actionable_records),
            "total_findings": len(finding_records),
            "non_actionable_findings": non_actionable,
            "avg_coverage": avg_coverage,
            "llm_cost_usd": _llm_cost(graph, run_summary),
            "llm_cost_label": _llm_cost_label(graph, run_summary),
            "llm_model": _llm_model(graph, run_summary),
            "duration_ms": _duration_ms(graph, run_summary),
            "top_findings": top_findings,
            "llm_validation": _llm_validation(graph),
        },
        "node_types": sorted(Counter(attrs.get("type", "unknown") for _node_id, attrs in nodes).items()),
        "edge_types": sorted(Counter(attrs.get("type", "unknown") for _source, _target, attrs in edges).items()),
        "top_structural_nodes": _top_nodes(nodes),
        "findings_by_tool": _findings_by_tool(finding_records),
        "top_rules": _top_rules(actionable_records, limit=10),
        "priority_findings": _priority_findings(actionable_records, limit=10),
        "risk_nodes": risk_nodes,
        "coverage_gaps": _coverage_gaps(nodes, limit=10),
        "test_linkage": _test_linkage(nodes, edges),
        "git_history": _git_history(nodes),
        "co_changes": _co_changes(graph),
        "clusters": clusters,
        "cross_signal_findings": _cross_signal_findings(finding_records),
        "dimension_scorecards": _dimension_scorecards(actionable_records, risk_nodes),
        "annotator_status": _annotator_status(graph, run_summary),
        "format_score": _format_score,
        "format_small": _format_small,
        "format_percent": _format_percent,
        "shorten": _shorten,
        "finding_message": _finding_message,
        "suggested_action": _suggested_action,
        "finding_code": _finding_code,
        "finding_line": _finding_line,
        "severity_text": _severity_text,
        "format_evidence": _format_evidence,
    }


def write_markdown_report(graph: nx.DiGraph, path: str | Path, top_n: int = 10) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown_report(graph, top_n=top_n), encoding="utf-8")
    return output_path


def _template_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        autoescape=select_autoescape(default=False),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _finding_records(graph: nx.DiGraph, nodes: list[tuple[str, dict]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    seen_cross_tool: set[tuple[Any, ...]] = set()
    for node_id, attrs in nodes:
        for finding in attrs.get("findings", []) or []:
            if not isinstance(finding, dict):
                continue
            key = (node_id, *finding_key(finding))
            if key in seen:
                continue
            cross_tool_key = _cross_tool_finding_key(node_id, attrs, finding)
            if cross_tool_key in seen_cross_tool:
                continue
            seen.add(key)
            seen_cross_tool.add(cross_tool_key)
            records.append(_record(node_id, attrs, finding, graph))
    for finding in detect_cross_signal_findings(graph):
        if finding.node_id not in graph.nodes:
            continue
        attrs = graph.nodes[finding.node_id]
        payload = _cross_signal_payload(finding)
        key = (finding.node_id, *finding_key(payload))
        if key in seen:
            continue
        seen.add(key)
        records.append(_record(finding.node_id, attrs, payload, graph))
    return records


def _record(node_id: str, attrs: dict[str, Any], finding: dict[str, Any], graph: nx.DiGraph) -> dict[str, Any]:
    normalized = dict(finding)
    if not normalized.get("evidence"):
        normalized["evidence"] = _source_evidence(graph, attrs, _finding_line(normalized, attrs))
    return {
        "node_id": node_id,
        "node": attrs,
        "finding": normalized,
        "dimension": _dimension(normalized),
        "code": _finding_code(normalized),
        "line": _finding_line(normalized, attrs),
    }


def _cross_signal_payload(finding: Finding) -> dict[str, Any]:
    return {
        "source": CROSS_SIGNAL_SOURCE,
        "code": finding.kind,
        "severity": finding.severity.upper(),
        "confidence": finding.confidence or "INFERRED",
        "message": finding.message or finding.kind.replace("_", " "),
        "evidence": finding.evidence,
    }


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


def _findings_by_tool(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: list[dict[str, Any]] = []
    counts = Counter(record["finding"].get("source", "unknown") for record in records)
    for tool, count in sorted(counts.items()):
        tool_records = [record for record in records if record["finding"].get("source", "unknown") == tool]
        prod_count = sum(1 for record in tool_records if not _is_test_node(record["node"]))
        grouped.append(
            {
                "tool": tool,
                "count": count,
                "production": prod_count,
                "test": count - prod_count,
                "top_rules": _top_rule_text(tool_records, limit=3),
            }
        )
    return grouped


def _top_rules(records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    messages: dict[tuple[str, str], str] = {}
    counts: Counter[tuple[str, str]] = Counter()
    for record in records:
        finding = record["finding"]
        source = finding.get("source", "unknown")
        code = _finding_code(finding)
        counts[(source, code)] += 1
        messages.setdefault((source, code), finding.get("message") or "")
    return [
        {"source": source, "code": code, "message": messages[(source, code)], "count": count}
        for (source, code), count in counts.most_common(limit)
    ]


def _top_rule_text(records: list[dict[str, Any]], limit: int) -> str:
    rules = _top_rules(records, limit)
    if not rules:
        return "none"
    return ", ".join(f"{rule['code']} ({rule['count']})" for rule in rules)


def _priority_findings(records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    return sorted(records, key=_priority_key)[:limit]


def _priority_key(record: dict[str, Any]) -> tuple[int, float, str]:
    finding = record["finding"]
    test_rank = 1 if _is_test_node(record["node"]) else 0
    source_bonus = {"llm": 0.25, "cross-signal": 0.15, "bandit": 0.2, "pip-audit": 0.2, "vulture": 0.0, "ruff": 0.0}.get(
        finding.get("source"),
        0.0,
    )
    severity = {"CRITICAL": 1.0, "HIGH": 0.85, "MEDIUM": 0.66, "LOW": 0.33}.get(
        str(finding.get("severity") or "").upper(),
        0.0,
    )
    risk = min(float(record["node"].get("risk_score") or 0.0) / 5.0, 1.0)
    impact = severity + risk + source_bonus
    return (test_rank, -impact, str(record["node"].get("qualified_name") or ""))


def _is_low_signal_finding(record: dict[str, Any]) -> bool:
    finding = record["finding"]
    code = _finding_code(finding)
    if code.startswith("D"):
        return True
    if code in {"S101", "B101"}:
        return True
    return False


def _is_actionable_record(record: dict[str, Any]) -> bool:
    return not _is_test_node(record["node"]) and not _is_low_signal_finding(record)


def _risk_nodes(
    nodes: list[tuple[str, dict]],
    finding_records: list[dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    findings_by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    visible_findings_by_node = Counter()
    for record in finding_records:
        findings_by_node[record["node_id"]].append(record)
        if _is_actionable_record(record):
            visible_findings_by_node[record["node_id"]] += 1

    risk_nodes = []
    for node_id, attrs in nodes:
        if attrs.get("type") not in {"Function", "Method"}:
            continue
        if _is_test_node(attrs):
            continue
        score = _risk_score(node_id, attrs, visible_findings_by_node[node_id])
        if score <= 0:
            continue
        risk_nodes.append(
            {
                "node_id": node_id,
                "node": attrs,
                "score": score,
                "findings": [record for record in findings_by_node.get(node_id, []) if _is_actionable_record(record)],
                "finding_count": visible_findings_by_node[node_id],
                "risk_components": attrs.get("risk_components") or {},
            }
        )
    return sorted(risk_nodes, key=lambda item: item["score"], reverse=True)[:limit]


def _risk_score(node_id: str, attrs: dict[str, Any], finding_count: int) -> float:
    if attrs.get("risk_score") is not None:
        return float(attrs.get("risk_score") or 0.0)
    coverage = attrs.get("coverage_line")
    coverage_penalty = 0.0 if coverage is None else max(0.0, 1.0 - float(coverage)) * 5
    complexity = float(attrs.get("complexity") or 0.0)
    churn = float(attrs.get("churn") or 0.0)
    structural = float(attrs.get("structural_score", attrs.get("centrality")) or 0.0)
    hotpath = float(attrs.get("hotpath_weight") or 0.0)
    return finding_count + coverage_penalty + min(complexity / 5, 3.0) + min(churn / 10, 3.0) + structural + hotpath


def _coverage_gaps(nodes: list[tuple[str, dict]], limit: int) -> list[dict[str, Any]]:
    gaps = [
        attrs
        for _node_id, attrs in nodes
        if attrs.get("coverage_line") is not None and attrs.get("coverage_line", 1.0) < 0.8
    ]
    return sorted(gaps, key=lambda item: item.get("coverage_line") or 0)[:limit]


def _test_linkage(nodes: list[tuple[str, dict]], edges: list[tuple[str, str, dict]]) -> dict[str, Any]:
    production = {
        node_id: attrs
        for node_id, attrs in nodes
        if attrs.get("type") in {"Function", "Method"} and not _is_test_node(attrs)
    }
    static_nodes = {
        source
        for source, _target, attrs in edges
        if attrs.get("type") == "tested_by" and _linkage_source(attrs) == "static"
    }
    dynamic_nodes = {
        source
        for source, _target, attrs in edges
        if attrs.get("type") == "tested_by" and _linkage_source(attrs) == "coverage_context"
    }
    tested_nodes = static_nodes | dynamic_nodes
    covered_nodes = {
        node_id
        for node_id, attrs in production.items()
        if attrs.get("coverage_line") is not None and float(attrs.get("coverage_line") or 0.0) > 0.0
    }
    untested = [
        attrs
        for node_id, attrs in production.items()
        if node_id not in tested_nodes and attrs.get("coverage_line") is not None and float(attrs.get("coverage_line") or 0) < 0.8
    ]
    return {
        "tested": len(set(production) & tested_nodes),
        "static_tested": len(set(production) & static_nodes),
        "context_tested": len(set(production) & dynamic_nodes),
        "covered": len(covered_nodes),
        "production": len(production),
        "coverage_known": sum(1 for attrs in production.values() if attrs.get("coverage_line") is not None),
        "untested": sorted(untested, key=lambda item: float(item.get("coverage_line") or 0))[:10],
    }


def _git_history(nodes: list[tuple[str, dict]]) -> list[dict[str, Any]]:
    files: dict[str, dict[str, Any]] = {}
    for _node_id, attrs in nodes:
        file_path = attrs.get("file_path")
        if not file_path or attrs.get("churn") is None:
            continue
        current = files.setdefault(file_path, {"file_path": file_path, "churn": 0, "author_count": 0, "bug_fix_keywords": 0})
        current["churn"] = max(current["churn"], int(attrs.get("churn") or 0))
        current["author_count"] = max(current["author_count"], int(attrs.get("author_count") or 0))
        current["bug_fix_keywords"] = max(current["bug_fix_keywords"], int(attrs.get("bug_fix_keywords") or 0))
    return sorted(files.values(), key=lambda item: item["churn"], reverse=True)[:10]


def _co_changes(graph: nx.DiGraph) -> list[dict[str, Any]]:
    dependency_graph = nx.DiGraph()
    dependency_graph.add_nodes_from(graph.nodes)
    dependency_graph.add_edges_from(
        (source, target)
        for source, target, attrs in graph.edges(data=True)
        if attrs.get("type") in {"calls", "imports"}
    )
    co_changes = []
    for source, target, attrs in graph.edges(data=True):
        if attrs.get("type") != "co_changes_with":
            continue
        left_file, right_file = _edge_file_pair(graph, source, target, attrs)
        if not _is_production_pair(left_file, right_file):
            continue
        if _is_type_only_path(left_file) or _is_type_only_path(right_file):
            continue
        if _is_obvious_test_pair(left_file, right_file):
            continue
        if nx.has_path(dependency_graph, source, target) or nx.has_path(dependency_graph, target, source):
            continue
        co_changes.append({"source": source, "target": target, **attrs})
    return sorted(co_changes, key=lambda item: item.get("co_change_count") or 0, reverse=True)[:10]


def _linkage_source(attrs: dict[str, Any]) -> str | None:
    return attrs.get("linkage_source") or attrs.get("source")


def _clusters(
    nodes: list[tuple[str, dict]],
    finding_records: list[dict[str, Any]],
    risk_nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    names = _cluster_names(nodes)
    findings_by_cluster: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    risk_by_cluster: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for record in finding_records:
        findings_by_cluster[record["node"].get("cluster_id")].append(record)
    for risk_node in risk_nodes:
        risk_by_cluster[risk_node["node"].get("cluster_id")].append(risk_node)

    cluster_ids = sorted({attrs.get("cluster_id") for _node_id, attrs in nodes if attrs.get("cluster_id") is not None})
    clusters = []
    for cluster_id in cluster_ids:
        cluster_nodes = [attrs for _node_id, attrs in nodes if attrs.get("cluster_id") == cluster_id]
        cluster_records = [record for record in findings_by_cluster.get(cluster_id, []) if _is_actionable_record(record)]
        issues = _top_rules(cluster_records, limit=3)
        inferred = _infer_cluster_summary(cluster_nodes)
        clusters.append(
            {
                "id": cluster_id,
                "name": names.get(cluster_id) or inferred["name"],
                "description": inferred["description"],
                "size": len(cluster_nodes),
                "role_counts": Counter(attrs.get("cluster_role") or "unknown" for attrs in cluster_nodes).most_common(3),
                "issues": issues,
                "top_risk": risk_by_cluster.get(cluster_id, [])[:3],
            }
        )
    clusters = sorted(clusters, key=lambda item: (item["size"], len(item["top_risk"]), len(item["issues"])), reverse=True)
    return _dedupe_cluster_names(clusters)[:20]


def _cluster_names(nodes: list[tuple[str, dict]]) -> dict[Any, str]:
    names = {}
    for _node_id, attrs in nodes:
        cluster_id = attrs.get("cluster_id")
        name = attrs.get("cluster_name") or attrs.get("llm_cluster_name")
        if cluster_id is not None and name:
            names.setdefault(cluster_id, str(name))
    return names


def _cross_signal_findings(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in records if record["finding"].get("source") == CROSS_SIGNAL_SOURCE]


def _dimension_scorecards(
    records: list[dict[str, Any]],
    risk_nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_dimension: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_dimension[record["dimension"]].append(record)
    for dimension in ("maintainability", "reliability", "security", "performance", "documentation"):
        by_dimension.setdefault(dimension, [])
    scorecards = []
    for dimension, dimension_records in sorted(by_dimension.items()):
        severity_counts = Counter(str(record["finding"].get("severity") or "UNKNOWN").upper() for record in dimension_records)
        offenders = [
            risk_node
            for risk_node in risk_nodes
            if any(record["dimension"] == dimension for record in risk_node["findings"])
        ][:5]
        scorecards.append(
            {
                "dimension": dimension,
                "count": len(dimension_records),
                "severity_counts": sorted(severity_counts.items()),
                "worst_offenders": offenders,
            }
        )
    return scorecards


def _cluster_count(nodes: list[tuple[str, dict]]) -> int:
    return len({attrs.get("cluster_id") for _node_id, attrs in nodes if attrs.get("cluster_id") is not None})


def _cluster_stats(nodes: list[tuple[str, dict]], displayed: list[dict[str, Any]]) -> dict[str, Any]:
    sizes = Counter(attrs.get("cluster_id") for _node_id, attrs in nodes if attrs.get("cluster_id") is not None)
    total = len(sizes)
    trivial = sum(1 for size in sizes.values() if size <= 1)
    label = f"{total} total, {len(displayed)} shown"
    if trivial:
        label += f", {trivial} trivial"
    return {"total": total, "shown": len(displayed), "trivial": trivial, "label": label}


def _llm_cost(graph: nx.DiGraph, run_summary: dict[str, Any] | None = None) -> float:
    llm = graph.graph.get("llm") or {}
    if isinstance(llm, dict) and llm:
        return float(llm.get("cost_usd") or llm.get("total_cost_usd") or 0.0)
    if run_summary:
        summary_llm = run_summary.get("llm") or {}
        if isinstance(summary_llm, dict):
            return float(summary_llm.get("cost_usd") or 0.0)
    return float(graph.graph.get("llm_cost_usd") or 0.0)


def _llm_cost_label(graph: nx.DiGraph, run_summary: dict[str, Any] | None = None) -> str:
    model = _llm_model(graph, run_summary)
    calls = _llm_calls(graph, run_summary)
    cost = _llm_cost(graph, run_summary)
    if calls == 0 and not model:
        return "N/A (agent-completed local task files)"
    if model and (model.startswith("ollama/") or model.startswith("ollama:") or model == "ollama"):
        return "N/A (local Ollama)"
    return f"${cost:.4f}"


def _llm_model(graph: nx.DiGraph, run_summary: dict[str, Any] | None = None) -> str | None:
    llm = graph.graph.get("llm") or {}
    if isinstance(llm, dict) and llm.get("model"):
        return str(llm["model"])
    if run_summary:
        calls_path = _llm_calls_path(run_summary)
        if calls_path and calls_path.exists():
            for line in calls_path.read_text(encoding="utf-8").splitlines():
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("model"):
                    return str(record["model"])
    return None


def _llm_validation(graph: nx.DiGraph) -> dict[str, int] | None:
    raw = graph.graph.get("llm_validation")
    if not isinstance(raw, dict):
        return None
    proposed = int(raw.get("proposed") or 0)
    accepted = int(raw.get("accepted") or 0)
    rejected = int(raw.get("rejected") or 0)
    if proposed == 0 and accepted == 0 and rejected == 0:
        return None
    return {"proposed": proposed, "accepted": accepted, "rejected": rejected}


def _llm_calls(graph: nx.DiGraph, run_summary: dict[str, Any] | None = None) -> int:
    llm = graph.graph.get("llm") or {}
    if isinstance(llm, dict) and llm.get("calls") is not None:
        return int(llm.get("calls") or 0)
    if run_summary:
        summary_llm = run_summary.get("llm") or {}
        if isinstance(summary_llm, dict):
            return int(summary_llm.get("calls") or 0)
    return 0


def _llm_calls_path(run_summary: dict[str, Any]) -> Path | None:
    repo_path = run_summary.get("repo_path")
    run_id = run_summary.get("run_id")
    if not repo_path or not run_id:
        return None
    return Path(repo_path) / ".qualgraph" / "runs" / str(run_id) / "llm_calls.jsonl"


def _duration_ms(graph: nx.DiGraph, run_summary: dict[str, Any] | None = None) -> float | None:
    for key in ("duration_ms", "run_duration_ms", "analysis_duration_ms"):
        if graph.graph.get(key) is not None:
            return float(graph.graph[key])
    if run_summary and run_summary.get("duration_ms") is not None:
        return float(run_summary["duration_ms"])
    return None


def _dimension(finding: dict[str, Any]) -> str:
    explicit = finding.get("dimension")
    if explicit:
        return str(explicit).lower()
    source = str(finding.get("source") or "").lower()
    code = _finding_code(finding).lower()
    if source in {"bandit", "pip-audit", "detect-secrets"} or "vulnerable" in code or "secret" in code:
        return "security"
    if "coverage" in code or "test" in code or "cycle" in code:
        return "reliability"
    if "profile" in code or "hotspot" in code or "hotpath" in code or "performance" in code:
        return "performance"
    if "docstring" in code or "documentation" in code:
        return "documentation"
    return "maintainability"


def _annotator_status(graph: nx.DiGraph, run_summary: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    raw_statuses = graph.graph.get("annotator_status")
    if not raw_statuses and run_summary:
        raw_statuses = run_summary.get("annotators")
    statuses = []
    for item in raw_statuses or []:
        if not isinstance(item, dict):
            continue
        statuses.append(
            {
                "name": item.get("name") or "unknown",
                "status": item.get("status") or "unknown",
                "duration_ms": item.get("duration_ms"),
                "counts": _format_counts(item.get("counts")),
            }
        )
    return statuses


def _format_counts(counts: Any) -> str:
    if not isinstance(counts, dict) or not counts:
        return ""
    parts = []
    for key, value in counts.items():
        if value is None:
            continue
        if value in (0, 0.0) and key != "error_count":
            continue
        parts.append(f"{key}={value}")
    return ", ".join(parts)


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


def _cross_tool_finding_key(node_id: str, attrs: dict[str, Any], finding: dict[str, Any]) -> tuple[Any, ...]:
    code = _finding_code(finding)
    canonical_code = {"B101": "assert-used", "S101": "assert-used"}.get(code, code)
    return (
        node_id,
        attrs.get("file_path"),
        _finding_line(finding, attrs),
        canonical_code,
        _canonical_message(finding),
    )


def _canonical_message(finding: dict[str, Any]) -> str:
    message = str(finding.get("message") or "").lower()
    if "assert" in message:
        return "assert-used"
    return re.sub(r"\s+", " ", message).strip()


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


def _format_percent(value: Any) -> str:
    if value is None:
        return "unknown"
    try:
        return f"{float(value):.1%}"
    except Exception:
        return "unknown"


def _format_evidence(value: Any) -> str:
    if isinstance(value, dict):
        preferred = [
            "target",
            "partners",
            "partner_count",
            "co_change_count",
            "co_change_rate",
            "max_co_change_rate",
            "centrality",
            "complexity",
            "coverage",
            "in_degree",
            "out_degree",
            "degree_threshold",
        ]
        parts = []
        for key in preferred:
            if key not in value:
                continue
            item = value[key]
            if isinstance(item, float):
                item = round(item, 4)
            parts.append(f"{key}={item}")
        if parts:
            return ", ".join(parts)
    return str(value or "")


def _shorten(value: Any, limit: int = 110) -> str:
    text = str(value or "").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _finding_message(finding: dict[str, Any], limit: int = 110) -> str:
    message = str(finding.get("message") or "").replace("\n", " ").strip()
    if finding.get("source") == "llm":
        return message
    return _shorten(message, limit)


def _suggested_action(finding: dict[str, Any], limit: int = 180) -> str:
    action = str(finding.get("suggested_action") or "").replace("\n", " ").strip()
    if finding.get("source") == "llm":
        return action
    return _shorten(action, limit)


def _is_obvious_test_pair(left: Any, right: Any) -> bool:
    left_path = str(left or "").replace("\\", "/")
    right_path = str(right or "").replace("\\", "/")
    if not left_path or not right_path:
        return False
    left_is_test = _is_test_path(left_path)
    right_is_test = _is_test_path(right_path)
    if left_is_test == right_is_test:
        return False
    prod = right_path if left_is_test else left_path
    test = left_path if left_is_test else right_path
    prod_stem = prod.rsplit("/", 1)[-1].removesuffix(".py")
    test_stem = test.rsplit("/", 1)[-1].removesuffix(".py")
    return test_stem in {f"test_{prod_stem}", f"{prod_stem}_test"} or prod_stem in test_stem


def _is_test_path(path: str) -> bool:
    return path.startswith("tests/") or "/tests/" in path or path.rsplit("/", 1)[-1].startswith("test_")


def _is_production_pair(left: Any, right: Any) -> bool:
    return bool(left and right and not _is_test_path(str(left)) and not _is_test_path(str(right)))


def _is_type_only_path(path: Any) -> bool:
    normalized = str(path or "").replace("\\", "/").lower()
    filename = normalized.rsplit("/", 1)[-1]
    return filename in {"types.py", "_types.py", "typing.py"} or normalized.endswith("/types/__init__.py")


def _edge_file_pair(graph: nx.DiGraph, source: str, target: str, attrs: dict[str, Any]) -> tuple[Any, Any]:
    left = attrs.get("source") or (graph.nodes[source].get("file_path") if source in graph.nodes else None)
    right = attrs.get("target") or (graph.nodes[target].get("file_path") if target in graph.nodes else None)
    return left, right


def _source_evidence(graph: nx.DiGraph, attrs: dict[str, Any], line: Any) -> str:
    try:
        line_number = int(line)
    except (TypeError, ValueError):
        return ""
    line_start = int(attrs.get("line_start") or line_number)
    source = str(attrs.get("source") or "")
    if source:
        lines = source.splitlines()
        index = line_number - line_start
        if 0 <= index < len(lines):
            return lines[index].strip()
    repo_path = graph.graph.get("repo_path")
    file_path = attrs.get("file_path")
    if not repo_path or not file_path:
        return ""
    try:
        lines = (Path(repo_path) / str(file_path)).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1].strip()
    return ""


def _infer_cluster_summary(cluster_nodes: list[dict[str, Any]]) -> dict[str, str]:
    names = [str(attrs.get("qualified_name") or attrs.get("name") or "") for attrs in cluster_nodes]
    paths = [str(attrs.get("file_path") or "") for attrs in cluster_nodes if attrs.get("file_path")]
    label = _dominant_label(names, paths)
    top_symbols = [
        name.rsplit(".", 1)[-1]
        for name in names
        if name and not name.startswith("test_")
    ][:3]
    readable = label if label in _domain_labels().values() else label.replace("_", " ").replace("-", " ").title().strip()
    description = "Includes " + ", ".join(top_symbols) if top_symbols else "No dominant production symbols."
    return {"name": readable, "description": description}


def _dedupe_cluster_names(clusters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    name_counts = Counter(str(cluster["name"]) for cluster in clusters)
    used: set[str] = set()
    for cluster in clusters:
        base_name = str(cluster["name"])
        if name_counts[base_name] <= 1:
            used.add(base_name)
            continue
        discriminator = _cluster_discriminator(cluster)
        candidate = f"{base_name} ({discriminator})" if discriminator else base_name
        if candidate in used:
            candidate = f"{candidate} #{cluster['id']}"
        cluster["name"] = candidate
        used.add(candidate)
    return clusters


def _cluster_discriminator(cluster: dict[str, Any]) -> str:
    description = str(cluster.get("description") or "")
    if description.startswith("Includes "):
        first = description.removeprefix("Includes ").split(",", 1)[0].strip()
        if first:
            return _humanize_symbol(first)
    return f"Cluster {cluster.get('id')}"


def _humanize_symbol(value: str) -> str:
    text = value.strip("_").replace("_", " ").strip()
    if not text:
        return "Cluster"
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    return " ".join(part.capitalize() for part in text.split())


def _dominant_label(names: list[str], paths: list[str]) -> str:
    test_label = _test_infrastructure_label(names, paths)
    if test_label:
        return test_label
    path_label = _path_segment_label(paths)
    if path_label:
        return path_label
    scores: Counter[str] = Counter()
    for token, label in _domain_labels().items():
        scores[label] = sum(1 for item in [*names, *paths] if token in item.lower())
    label, count = scores.most_common(1)[0]
    if count:
        return label
    candidates: Counter[str] = Counter()
    for path in paths:
        parts = Path(path).with_suffix("").parts
        for part in reversed(parts):
            if part not in {"src", "tests", "test"} and not part.startswith("test_"):
                candidates[part] += 1
                break
    if candidates:
        return candidates.most_common(1)[0][0]
    return "Cluster"


def _test_infrastructure_label(names: list[str], paths: list[str]) -> str | None:
    items = [*names, *paths]
    if not items:
        return None
    testish = sum(
        1
        for item in items
        if "conftest" in item.lower()
        or "mockserver" in item.lower()
        or "/tests/" in item.replace("\\", "/").lower()
        or item.replace("\\", "/").lower().startswith("tests/")
    )
    return "Test Infrastructure" if testish / len(items) >= 0.35 else None


def _path_segment_label(paths: list[str]) -> str | None:
    ignored = {
        "",
        ".",
        "src",
        "tests",
        "test",
        "benchmarks",
        "repos",
        "scrapy",
        "starlette",
        "qualgraph",
        "__pycache__",
    }
    candidates: Counter[str] = Counter()
    for path in paths:
        normalized = Path(path).with_suffix("").parts
        for part in reversed(normalized[:-1]):
            lowered = part.lower()
            if lowered in ignored or lowered.startswith("test_") or lowered.startswith("."):
                continue
            candidates[part] += 1
            break
    if not candidates:
        return None
    label, count = candidates.most_common(1)[0]
    if count < max(2, len(paths) * 0.2):
        return None
    return label


def _domain_labels() -> dict[str, str]:
    return {
        "routing": "Routing & URL matching",
        "responses": "Responses & streaming",
        "requests": "Requests & body parsing",
        "middleware": "Middleware",
        "testclient": "Test client",
        "websockets": "WebSockets",
        "datastructures": "Data structures",
        "config": "Configuration",
        "templating": "Templating",
        "authentication": "Authentication",
    }


def _latest_run_summary(graph: nx.DiGraph) -> dict[str, Any] | None:
    repo_path = graph.graph.get("repo_path")
    if not repo_path:
        return None
    runs_dir = Path(repo_path) / ".qualgraph" / "runs"
    if not runs_dir.exists():
        return None
    summaries = sorted(runs_dir.glob("*/run_summary.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    for summary_path in summaries:
        try:
            return json.loads(summary_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
    return None
