"""Read-only view models for the local Qualgraph viewer."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.graph.serialize import read_json_graph


TESTED_BY = "tested_by"


class ViewerData:
    """Precomputed graph summaries used by the local HTTP viewer."""

    def __init__(self, graph: nx.DiGraph, *, graph_path: str | Path | None = None, top_n: int = 50) -> None:
        self.graph = graph
        self.graph_path = str(graph_path) if graph_path is not None else None
        self.top_n = top_n
        self._nodes = dict(graph.nodes(data=True))
        self._findings = self._build_findings()
        self._clusters = self._build_clusters()

    @classmethod
    def from_path(cls, graph_path: str | Path, *, top_n: int = 50) -> "ViewerData":
        return cls(read_json_graph(graph_path), graph_path=graph_path, top_n=top_n)

    def summary(self) -> dict[str, Any]:
        findings_by_source = Counter(item["source"] for item in self._findings)
        findings_by_severity = Counter(item["severity"] for item in self._findings)
        findings_by_dimension = Counter(item["dimension"] for item in self._findings)
        llm_validation = self.graph.graph.get("llm_validation")
        return {
            "graph_path": self.graph_path,
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "clusters": len(self._clusters),
            "node_types": _counter_items(Counter(attrs.get("type", "unknown") for attrs in self._nodes.values())),
            "edge_types": _counter_items(Counter(attrs.get("type", "unknown") for _s, _t, attrs in self.graph.edges(data=True))),
            "findings": len(self._findings),
            "llm_findings": findings_by_source.get("llm", 0),
            "findings_by_source": _counter_items(findings_by_source),
            "findings_by_severity": _counter_items(findings_by_severity),
            "findings_by_dimension": _counter_items(findings_by_dimension),
            "top_risk": self.top_risk_nodes(self.top_n),
            "annotator_status": self.graph.graph.get("annotator_status") or [],
            "warnings": _warnings(self.graph, self._nodes),
            "llm_validation": llm_validation if isinstance(llm_validation, dict) else None,
        }

    def graph_payload(self, *, cluster_id: str | None = None) -> dict[str, Any]:
        if cluster_id is None:
            return {
                "mode": "clusters",
                "nodes": [
                    {
                        "id": cluster["id"],
                        "label": cluster["name"],
                        "size": cluster["size"],
                        "risk_score": cluster["max_risk_score"],
                        "finding_count": cluster["finding_count"],
                        "llm_finding_count": cluster["llm_finding_count"],
                        "kind": cluster["kind"],
                    }
                    for cluster in self.clusters()
                ],
                "edges": self._cluster_edges(),
            }
        cluster_nodes = [
            node_id
            for node_id, attrs in self._nodes.items()
            if _cluster_id(attrs) == cluster_id
        ]
        node_set = set(cluster_nodes)
        return {
            "mode": "cluster",
            "cluster_id": cluster_id,
            "nodes": [self._slim_node(node_id, self._nodes[node_id]) for node_id in cluster_nodes],
            "edges": [
                _slim_edge(source, target, attrs)
                for source, target, attrs in self.graph.edges(data=True)
                if source in node_set and target in node_set
            ],
        }

    def clusters(self) -> list[dict[str, Any]]:
        return sorted(
            self._clusters.values(),
            key=lambda item: (item["max_risk_score"], item["finding_count"], item["size"]),
            reverse=True,
        )

    def findings(self, *, source: str | None = None) -> list[dict[str, Any]]:
        findings = self._findings
        if source:
            findings = [item for item in findings if item["source"] == source]
        return sorted(findings, key=lambda item: (_severity_rank(item["severity"]), item["risk_score"]), reverse=True)

    def node_detail(self, node_id: str) -> dict[str, Any] | None:
        attrs = self._nodes.get(node_id)
        if attrs is None:
            return None
        incoming = [
            self._neighbor(source, edge_attrs, direction="incoming")
            for source, _target, edge_attrs in self.graph.in_edges(node_id, data=True)
        ]
        outgoing = [
            self._neighbor(target, edge_attrs, direction="outgoing")
            for _source, target, edge_attrs in self.graph.out_edges(node_id, data=True)
        ]
        return {
            **self._slim_node(node_id, attrs),
            "source": attrs.get("source") or "",
            "docstring": attrs.get("docstring"),
            "findings": [self._finding_record(node_id, attrs, finding, index) for index, finding in enumerate(attrs.get("findings") or []) if isinstance(finding, dict)],
            "risk_components": attrs.get("risk_components") or {},
            "metrics": {
                "centrality": attrs.get("centrality"),
                "structural_score": attrs.get("structural_score"),
                "betweenness_centrality": attrs.get("betweenness_centrality"),
                "pagerank": attrs.get("pagerank"),
                "in_degree": attrs.get("in_degree"),
                "out_degree": attrs.get("out_degree"),
                "maintainability_index": attrs.get("maintainability_index"),
            },
            "relationships": {
                "incoming": incoming[:100],
                "outgoing": outgoing[:100],
            },
        }

    def top_risk_nodes(self, limit: int) -> list[dict[str, Any]]:
        nodes = [
            self._slim_node(node_id, attrs)
            for node_id, attrs in self._nodes.items()
            if attrs.get("type") in {"Function", "Method"} and not _is_test_node(attrs)
        ]
        return sorted(nodes, key=lambda item: float(item.get("risk_score") or 0.0), reverse=True)[:limit]

    def _build_findings(self) -> list[dict[str, Any]]:
        records = []
        for node_id, attrs in self._nodes.items():
            for index, finding in enumerate(attrs.get("findings") or []):
                if isinstance(finding, dict):
                    records.append(self._finding_record(node_id, attrs, finding, index))
        return records

    def _build_clusters(self) -> dict[str, dict[str, Any]]:
        grouped: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
        for node_id, attrs in self._nodes.items():
            grouped[_cluster_id(attrs)].append((node_id, attrs))

        findings_by_cluster = Counter(record["cluster_id"] for record in self._findings)
        llm_by_cluster = Counter(record["cluster_id"] for record in self._findings if record["source"] == "llm")
        clusters = {}
        for cluster_id, members in grouped.items():
            attrs_list = [attrs for _node_id, attrs in members]
            risks = [float(attrs.get("risk_score") or 0.0) for attrs in attrs_list]
            names = [str(attrs.get("qualified_name") or attrs.get("name") or "") for attrs in attrs_list]
            paths = [str(attrs.get("file_path") or "") for attrs in attrs_list if attrs.get("file_path")]
            clusters[cluster_id] = {
                "id": cluster_id,
                "name": _cluster_name(cluster_id, attrs_list, names, paths),
                "size": len(members),
                "kind": "test" if sum(1 for attrs in attrs_list if _is_test_node(attrs)) >= len(attrs_list) / 2 else "production",
                "max_risk_score": max(risks, default=0.0),
                "avg_risk_score": sum(risks) / len(risks) if risks else 0.0,
                "finding_count": findings_by_cluster[cluster_id],
                "llm_finding_count": llm_by_cluster[cluster_id],
                "node_types": _counter_items(Counter(attrs.get("type", "unknown") for attrs in attrs_list)),
                "top_files": _counter_items(Counter(paths), limit=5),
                "top_risk_nodes": sorted(
                    [self._slim_node(node_id, attrs) for node_id, attrs in members],
                    key=lambda item: float(item.get("risk_score") or 0.0),
                    reverse=True,
                )[:5],
            }
        return clusters

    def _cluster_edges(self) -> list[dict[str, Any]]:
        edges: Counter[tuple[str, str, str]] = Counter()
        for source, target, attrs in self.graph.edges(data=True):
            source_cluster = _cluster_id(self._nodes.get(source, {}))
            target_cluster = _cluster_id(self._nodes.get(target, {}))
            if source_cluster == target_cluster:
                continue
            edge_type = str(attrs.get("type") or "unknown")
            ordered = tuple(sorted((source_cluster, target_cluster)))
            edges[(ordered[0], ordered[1], edge_type)] += 1
        return [
            {"source": source, "target": target, "type": edge_type, "weight": weight}
            for (source, target, edge_type), weight in edges.most_common(500)
        ]

    def _slim_node(self, node_id: str, attrs: dict[str, Any]) -> dict[str, Any]:
        cluster_id = _cluster_id(attrs)
        return {
            "id": node_id,
            "name": attrs.get("name") or node_id,
            "qualified_name": attrs.get("qualified_name") or attrs.get("name") or node_id,
            "type": attrs.get("type") or "unknown",
            "file_path": attrs.get("file_path"),
            "line_start": attrs.get("line_start"),
            "line_end": attrs.get("line_end"),
            "cluster_id": cluster_id,
            "cluster_name": getattr(self, "_clusters", {}).get(cluster_id, {}).get("name"),
            "cluster_role": attrs.get("cluster_role"),
            "risk_score": float(attrs.get("risk_score") or 0.0),
            "coverage_line": attrs.get("coverage_line"),
            "complexity": attrs.get("complexity"),
            "churn": attrs.get("churn"),
            "finding_count": len([item for item in attrs.get("findings") or [] if isinstance(item, dict)]),
            "llm_finding_count": len([item for item in attrs.get("findings") or [] if isinstance(item, dict) and item.get("source") == "llm"]),
            "is_test": _is_test_node(attrs),
        }

    def _finding_record(self, node_id: str, attrs: dict[str, Any], finding: dict[str, Any], index: int) -> dict[str, Any]:
        code = str(finding.get("code") or finding.get("test_id") or "unknown")
        source = str(finding.get("source") or "unknown")
        severity = str(finding.get("severity") or "UNKNOWN").upper()
        return {
            "id": f"{node_id}::finding::{index}",
            "node_id": node_id,
            "node_name": attrs.get("qualified_name") or attrs.get("name") or node_id,
            "file_path": attrs.get("file_path"),
            "line": _finding_line(finding, attrs),
            "cluster_id": _cluster_id(attrs),
            "source": source,
            "code": code,
            "severity": severity,
            "confidence": finding.get("confidence"),
            "dimension": _dimension(finding),
            "message": finding.get("message") or finding.get("description") or code,
            "evidence": finding.get("evidence"),
            "suggested_action": finding.get("suggested_action"),
            "risk_score": float(attrs.get("risk_score") or 0.0),
        }

    def _neighbor(self, node_id: str, edge_attrs: dict[str, Any], *, direction: str) -> dict[str, Any]:
        attrs = self._nodes.get(node_id, {})
        return {
            **self._slim_node(node_id, attrs),
            "edge_type": edge_attrs.get("type") or "unknown",
            "direction": direction,
            "edge": {key: value for key, value in edge_attrs.items() if key in {"type", "co_change_count", "co_change_rate", "linkage_source"}},
        }


def _slim_edge(source: str, target: str, attrs: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": source,
        "target": target,
        "type": attrs.get("type") or "unknown",
        "weight": attrs.get("co_change_count") or 1,
        **({"linkage_source": attrs.get("linkage_source")} if attrs.get("type") == TESTED_BY else {}),
    }


def _cluster_id(attrs: dict[str, Any]) -> str:
    cluster_id = attrs.get("cluster_id")
    return "unclustered" if cluster_id is None else str(cluster_id)


def _cluster_name(cluster_id: str, attrs_list: list[dict[str, Any]], names: list[str], paths: list[str]) -> str:
    explicit = next((attrs.get("cluster_name") or attrs.get("llm_cluster_name") for attrs in attrs_list if attrs.get("cluster_name") or attrs.get("llm_cluster_name")), None)
    if explicit:
        return str(explicit)
    path_label = _path_label(paths)
    if path_label:
        return path_label
    symbol = next((name.rsplit(".", 1)[-1] for name in names if name), None)
    return _humanize(symbol or f"Cluster {cluster_id}")


def _path_label(paths: list[str]) -> str | None:
    candidates = Counter()
    ignored = {"", ".", "src", "tests", "test", "benchmarks", "repos", "__pycache__"}
    for path in paths:
        parts = Path(path).with_suffix("").parts
        for part in reversed(parts):
            lowered = part.lower()
            if lowered in ignored or lowered.startswith("."):
                continue
            candidates[part] += 1
            break
    if not candidates:
        return None
    return _humanize(candidates.most_common(1)[0][0])


def _humanize(value: str) -> str:
    return str(value).strip("_").replace("_", " ").replace("-", " ").title().strip() or "Cluster"


def _is_test_node(attrs: dict[str, Any]) -> bool:
    file_path = str(attrs.get("file_path") or "").replace("\\", "/")
    return (
        attrs.get("type") == "TestFunction"
        or file_path.startswith("tests/")
        or "/tests/" in file_path
        or file_path.rsplit("/", 1)[-1].startswith("test_")
    )


def _finding_line(finding: dict[str, Any], attrs: dict[str, Any]) -> Any:
    location = finding.get("location")
    if isinstance(location, dict) and location.get("row") is not None:
        return location["row"]
    return finding.get("line") or attrs.get("line_start")


def _dimension(finding: dict[str, Any]) -> str:
    explicit = finding.get("dimension")
    if explicit:
        return str(explicit).lower()
    source = str(finding.get("source") or "").lower()
    code = str(finding.get("code") or finding.get("test_id") or "").lower()
    if source in {"bandit", "pip-audit", "detect-secrets"} or "secret" in code:
        return "security"
    if "coverage" in code or "test" in code or "cycle" in code:
        return "reliability"
    if "profile" in code or "hotpath" in code or "performance" in code:
        return "performance"
    if "docstring" in code:
        return "documentation"
    return "maintainability"


def _severity_rank(severity: str) -> int:
    return {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(str(severity).upper(), 0)


def _counter_items(counter: Counter, *, limit: int | None = None) -> list[dict[str, Any]]:
    items = counter.most_common(limit)
    return [{"name": str(name), "count": count} for name, count in items]


def _warnings(graph: nx.DiGraph, nodes: dict[str, dict[str, Any]]) -> list[str]:
    warnings = []
    production_funcs = [
        attrs
        for attrs in nodes.values()
        if attrs.get("type") in {"Function", "Method"} and not _is_test_node(attrs)
    ]
    if production_funcs and not any(attrs.get("coverage_line") is not None for attrs in production_funcs):
        warnings.append("Coverage data is unavailable; coverage gaps and coverage-context linkage are disabled.")
    annotators = graph.graph.get("annotator_status") or []
    failed = [item for item in annotators if isinstance(item, dict) and str(item.get("status", "")).startswith("failed")]
    for item in failed:
        warnings.append(f"Annotator failed: {item.get('name')}")
    return warnings
