"""Cross-signal findings derived from the shared graph."""

from __future__ import annotations

from typing import Any

import networkx as nx

from qualgraph.findings.model import Finding
from qualgraph.graph.schema import EdgeType, NodeType


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
        and attrs.get("coverage_line") is not None
        and not _is_test_attrs(attrs)
    ]
    if not funcs:
        return []

    cx_threshold = _percentile([float(attrs["complexity"]) for _node_id, attrs in funcs], complexity_pct)
    cn_threshold = _percentile([float(attrs.get("centrality") or 0.0) for _node_id, attrs in funcs], centrality_pct)
    findings: list[Finding] = []
    for node_id, attrs in funcs:
        complexity = float(attrs["complexity"])
        centrality = float(attrs.get("centrality") or 0.0)
        coverage = float(attrs["coverage_line"])
        if (
            complexity >= cx_threshold
            and centrality >= cn_threshold
            and coverage == 0.0
        ):
            findings.append(
                Finding(
                    node_id=node_id,
                    kind="untested_hotspot",
                    severity="high",
                    evidence={
                        "complexity": complexity,
                        "centrality": centrality,
                        "coverage": coverage,
                    },
                )
            )
    return findings


def detect_hidden_coupling(graph: nx.DiGraph) -> list[Finding]:
    """Find co-change edges that lack a static calls/imports path in either direction."""

    dependency_graph = _edge_type_subgraph(graph, {EdgeType.CALLS.value, EdgeType.IMPORTS.value})
    findings: list[Finding] = []
    for source, target, attrs in graph.edges(data=True):
        if attrs.get("type") != EdgeType.CO_CHANGES_WITH.value:
            continue
        left_file, right_file = _edge_file_pair(graph, source, target, attrs)
        if _is_test_path(str(left_file or "")) or _is_test_path(str(right_file or "")):
            continue
        if _is_type_only_path(left_file) or _is_type_only_path(right_file):
            continue
        if _is_obvious_test_pair(left_file, right_file):
            continue
        if nx.has_path(dependency_graph, source, target) or nx.has_path(dependency_graph, target, source):
            continue
        findings.append(
            Finding(
                node_id=source,
                kind="hidden_coupling",
                severity="medium",
                confidence="INFERRED",
                message="Files or modules change together without an observed static calls/imports path.",
                evidence={
                    "target": target,
                    "co_change_count": attrs.get("co_change_count") or attrs.get("weight"),
                    "co_change_rate": attrs.get("co_change_rate"),
                    "edge_type": attrs.get("type"),
                },
            )
        )
    return findings


def detect_vulnerable_usage(graph: nx.DiGraph) -> list[Finding]:
    """Find vulnerable imports that are also used by calls from the same node."""

    findings: list[Finding] = []
    for node_id in graph.nodes:
        vulnerable_edges = [
            (target, attrs)
            for _source, target, attrs in graph.out_edges(node_id, data=True)
            if attrs.get("type") == EdgeType.IMPORTS_VULNERABLE.value
        ]
        if not vulnerable_edges:
            continue

        calls = _calls_from_node(graph, node_id)
        for dependency_node, vuln_attrs in vulnerable_edges:
            package = str(vuln_attrs.get("package") or graph.nodes[dependency_node].get("name") or "").strip()
            matched_calls = _calls_matching_package(graph, calls, package)
            if not package or not matched_calls:
                continue
            findings.append(
                Finding(
                    node_id=node_id,
                    kind="vulnerable_usage",
                    severity="high",
                    confidence="INFERRED",
                    message="A node imports a vulnerable package and appears to call symbols from that package.",
                    evidence={
                        "package": package,
                        "dependency_node": dependency_node,
                        "vulnerability_ids": vuln_attrs.get("vulnerability_ids", []),
                        "matched_calls": matched_calls,
                    },
                )
            )
    return findings


def detect_outdated_documentation(graph: nx.DiGraph, churn_pct: float = 0.8) -> list[Finding]:
    """Promote docstring consistency LLM findings on high-churn nodes."""

    nodes = [(node_id, attrs) for node_id, attrs in graph.nodes(data=True) if attrs.get("churn") is not None]
    if not nodes:
        return []
    churn_threshold = _percentile([float(attrs.get("churn") or 0.0) for _node_id, attrs in nodes], churn_pct)
    findings: list[Finding] = []
    for node_id, attrs in nodes:
        churn = float(attrs.get("churn") or 0.0)
        if churn < churn_threshold:
            continue
        doc_findings = [
            finding
            for finding in attrs.get("findings", []) or []
            if isinstance(finding, dict) and _is_docstring_consistency_finding(finding)
        ]
        for finding in doc_findings:
            findings.append(
                Finding(
                    node_id=node_id,
                    kind="outdated_documentation",
                    severity=str(finding.get("severity") or "medium").lower(),
                    confidence=finding.get("confidence") or "INFERRED",
                    message="High-churn code also has an LLM docstring consistency finding.",
                    evidence={
                        "churn": churn,
                        "churn_threshold": churn_threshold,
                        "llm_finding": {
                            "code": finding.get("code") or finding.get("kind"),
                            "message": finding.get("message") or finding.get("description"),
                            "evidence": finding.get("evidence"),
                        },
                    },
                )
            )
    return findings


def detect_god_nodes(
    graph: nx.DiGraph,
    centrality_pct: float = 0.95,
    complexity_pct: float = 0.95,
    degree_pct: float = 0.95,
) -> list[Finding]:
    """Find nodes that are simultaneously central, complex, and highly connected."""

    candidates = [
        (node_id, attrs)
        for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") in {NodeType.FUNCTION, NodeType.FUNCTION.value, NodeType.METHOD, NodeType.METHOD.value}
        and not _is_test_attrs(attrs)
    ]
    if not candidates:
        return []
    centrality_threshold = _percentile([float(attrs.get("centrality") or 0.0) for _node_id, attrs in candidates], centrality_pct)
    complexity_threshold = _percentile([float(attrs.get("complexity") or 0.0) for _node_id, attrs in candidates], complexity_pct)
    degree_threshold = _percentile([float(_total_degree(graph, node_id, attrs)) for node_id, attrs in candidates], degree_pct)

    findings: list[Finding] = []
    for node_id, attrs in candidates:
        centrality = float(attrs.get("centrality") or 0.0)
        complexity = float(attrs.get("complexity") or 0.0)
        in_degree = int(attrs.get("in_degree") if attrs.get("in_degree") is not None else graph.in_degree(node_id))
        out_degree = int(attrs.get("out_degree") if attrs.get("out_degree") is not None else graph.out_degree(node_id))
        degree = in_degree + out_degree
        if centrality >= centrality_threshold and complexity >= complexity_threshold and degree >= degree_threshold:
            findings.append(
                Finding(
                    node_id=node_id,
                    kind="god_node",
                    severity="high",
                    confidence="INFERRED",
                    message="Node is in the top band for centrality, complexity, and connectivity.",
                    evidence={
                        "centrality": centrality,
                        "centrality_threshold": centrality_threshold,
                        "complexity": complexity,
                        "complexity_threshold": complexity_threshold,
                        "in_degree": in_degree,
                        "out_degree": out_degree,
                        "degree_threshold": degree_threshold,
                    },
                )
            )
    return findings


def detect_cyclic_dependencies(graph: nx.DiGraph, max_cycles: int = 50) -> list[Finding]:
    """Find cycles in the calls subgraph."""

    calls_graph = _edge_type_subgraph(graph, {EdgeType.CALLS.value})
    findings: list[Finding] = []
    for cycle in nx.simple_cycles(calls_graph):
        if len(cycle) < 2:
            continue
        for node_id in cycle:
            findings.append(
                Finding(
                    node_id=node_id,
                    kind="cyclic_dependency",
                    severity="medium",
                    confidence="EXTRACTED",
                    message="Node participates in a cycle in the calls graph.",
                    evidence={"cycle": cycle, "cycle_size": len(cycle)},
                )
            )
        if len({tuple(finding.evidence["cycle"]) for finding in findings if finding.kind == "cyclic_dependency"}) >= max_cycles:
            break
    return findings


def detect_complex_hotspots(
    graph: nx.DiGraph,
    cpu_pct_threshold: float = 0.05,
    complexity_threshold: float | None = None,
    complexity_pct: float = 0.8,
    coverage_threshold: float = 0.5,
) -> list[Finding]:
    """Find CPU-heavy, complex, weakly covered functions."""

    candidates = [
        (node_id, attrs)
        for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") in {NodeType.FUNCTION, NodeType.FUNCTION.value, NodeType.METHOD, NodeType.METHOD.value}
        and attrs.get("complexity") is not None
        and attrs.get("cpu_pct") is not None
        and attrs.get("coverage_line") is not None
        and not _is_test_attrs(attrs)
    ]
    if not candidates:
        return []
    threshold = (
        float(complexity_threshold)
        if complexity_threshold is not None
        else _percentile([float(attrs.get("complexity") or 0.0) for _node_id, attrs in candidates], complexity_pct)
    )
    findings: list[Finding] = []
    for node_id, attrs in candidates:
        cpu_pct = float(attrs.get("cpu_pct") or 0.0)
        complexity = float(attrs.get("complexity") or 0.0)
        coverage = float(attrs.get("coverage_line") or 0.0)
        if cpu_pct > cpu_pct_threshold and complexity > threshold and coverage < coverage_threshold:
            findings.append(
                Finding(
                    node_id=node_id,
                    kind="complex_hotspot",
                    severity="high",
                    confidence="INFERRED",
                    message="CPU-heavy code is also complex and weakly covered.",
                    evidence={
                        "cpu_pct": cpu_pct,
                        "cpu_pct_threshold": cpu_pct_threshold,
                        "complexity": complexity,
                        "complexity_threshold": threshold,
                        "coverage": coverage,
                        "coverage_threshold": coverage_threshold,
                        "profile_cum_time": attrs.get("profile_cum_time"),
                        "profile_call_count": attrs.get("profile_call_count"),
                    },
                )
            )
    return findings


def detect_cross_signal_findings(graph: nx.DiGraph) -> list[Finding]:
    """Run all deterministic cross-signal detectors."""

    findings: list[Finding] = []
    findings.extend(detect_untested_hotspots(graph))
    findings.extend(detect_hidden_coupling(graph))
    findings.extend(detect_vulnerable_usage(graph))
    findings.extend(detect_outdated_documentation(graph))
    findings.extend(detect_god_nodes(graph))
    findings.extend(detect_cyclic_dependencies(graph))
    findings.extend(detect_complex_hotspots(graph))
    return findings


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    bounded = min(max(percentile, 0.0), 1.0)
    ordered = sorted(values)
    index = round((len(ordered) - 1) * bounded)
    return ordered[index]


def _edge_type_subgraph(graph: nx.DiGraph, edge_types: set[str]) -> nx.DiGraph:
    subgraph = nx.DiGraph()
    subgraph.add_nodes_from(graph.nodes)
    subgraph.add_edges_from(
        (source, target)
        for source, target, attrs in graph.edges(data=True)
        if attrs.get("type") in edge_types
    )
    return subgraph


def _calls_matching_package(
    graph: nx.DiGraph,
    calls: list[dict[str, Any]],
    package: str,
) -> list[dict[str, Any]]:
    matched = []
    for call in calls:
        target = call.get("target")
        call_name = str(call.get("call") or "")
        target_attrs = graph.nodes[target] if target in graph.nodes else {}
        target_name = str(target_attrs.get("qualified_name") or target_attrs.get("name") or "")
        if _matches_package(call_name, package) or _matches_package(target_name, package):
            payload = {"call": call_name or target_name}
            if target is not None:
                payload["target"] = target
            matched.append(payload)
    return matched


def _calls_from_node(graph: nx.DiGraph, node_id: str) -> list[dict[str, Any]]:
    calls = [
        {"target": target, "call": attrs.get("source")}
        for _source, target, attrs in graph.out_edges(node_id, data=True)
        if attrs.get("type") == EdgeType.CALLS.value
    ]
    calls.extend(
        {"call": call.get("name"), "line": call.get("line_start")}
        for call in graph.graph.get("unresolved_calls", []) or []
        if call.get("source") == node_id
    )
    return calls


def _matches_package(value: str, package: str) -> bool:
    normalized_value = _normalize_package(value.split(".", 1)[0])
    normalized_package = _normalize_package(package.split(".", 1)[0])
    return bool(normalized_value and normalized_value == normalized_package)


def _normalize_package(value: str) -> str:
    return value.replace("_", "-").lower()


def _is_docstring_consistency_finding(finding: dict[str, Any]) -> bool:
    code = str(finding.get("code") or finding.get("kind") or "").lower()
    title = str(finding.get("title") or "").lower()
    message = str(finding.get("message") or finding.get("description") or "").lower()
    return (
        finding.get("source") == "llm"
        and (
            code in {"docstring_consistency", "outdated_documentation"}
            or "docstring" in title
            or ("docstring" in message and "consistent" in message)
        )
    )


def _total_degree(graph: nx.DiGraph, node_id: str, attrs: dict[str, Any]) -> int:
    in_degree = attrs.get("in_degree") if attrs.get("in_degree") is not None else graph.in_degree(node_id)
    out_degree = attrs.get("out_degree") if attrs.get("out_degree") is not None else graph.out_degree(node_id)
    return int(in_degree) + int(out_degree)


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


def _is_type_only_path(path: Any) -> bool:
    normalized = str(path or "").replace("\\", "/").lower()
    filename = normalized.rsplit("/", 1)[-1]
    return filename in {"types.py", "_types.py", "typing.py"} or normalized.endswith("/types/__init__.py")


def _is_test_attrs(attrs: dict[str, Any]) -> bool:
    return attrs.get("type") == NodeType.TEST_FUNCTION.value or _is_test_path(str(attrs.get("file_path") or ""))


def _edge_file_pair(graph: nx.DiGraph, source: str, target: str, attrs: dict[str, Any]) -> tuple[Any, Any]:
    left = attrs.get("source") or (graph.nodes[source].get("file_path") if source in graph.nodes else None)
    right = attrs.get("target") or (graph.nodes[target].get("file_path") if target in graph.nodes else None)
    return left, right
