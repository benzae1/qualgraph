"""Pip-audit vulnerability annotator."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.locations import find_node_for_location
from qualgraph.graph.schema import EdgeAttrs, EdgeType, edge_attrs_to_graph


class PipAuditAnnotator(BaseAnnotator):
    name = "pip-audit"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("pip_audit") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        _clear_imports_vulnerable_edges(graph)

        completed = subprocess.run(
            [sys.executable, "-m", "pip_audit", "-f", "json"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode not in (0, 1):
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "pip-audit failed")

        payload = json.loads(completed.stdout or "{}")
        vulnerable = _vulnerable_dependencies(payload)
        if not vulnerable:
            return AnnotatorResult(name=self.name)

        nodes_touched: set[str] = set()
        edges_added = 0
        for imported in _import_records(graph):
            matched = _match_vulnerable_dependency(imported["name"], vulnerable)
            if matched is None:
                continue
            node_id = find_node_for_location(graph, imported["file_path"], int(imported["line_start"]))
            if node_id is None:
                node_id = imported["source"]
            package_node = _ensure_dependency_node(graph, matched)
            if _add_vulnerable_import_edge(graph, node_id, package_node, matched, imported):
                edges_added += 1
            if add_finding(graph.nodes[node_id], _finding_payload(matched, imported)):
                nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched), edges_added=edges_added)


def _vulnerable_dependencies(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    vulnerable: dict[str, dict[str, Any]] = {}
    for dependency in payload.get("dependencies", []) or []:
        vulns = dependency.get("vulns") or dependency.get("vulnerabilities") or []
        if not vulns:
            continue
        name = str(dependency.get("name") or "").strip()
        if not name:
            continue
        normalized = _normalize_package(name)
        vulnerable[normalized] = {
            "name": name,
            "version": dependency.get("version"),
            "vulnerabilities": vulns,
        }
    return vulnerable


def _import_records(graph: nx.DiGraph) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for imported in graph.graph.get("pending_imports", []) or []:
        if imported.get("name") and imported.get("source") and imported.get("file_path"):
            records.append(dict(imported))

    for source, _target, attrs in graph.edges(data=True):
        if attrs.get("type") != EdgeType.IMPORTS.value:
            continue
        import_name = attrs.get("target") or attrs.get("source")
        source_attrs = graph.nodes[source]
        if import_name and source_attrs.get("file_path"):
            records.append(
                {
                    "source": source,
                    "name": import_name,
                    "alias": attrs.get("source"),
                    "file_path": source_attrs["file_path"],
                    "line_start": source_attrs.get("line_start", 1),
                }
            )

    return records


def _match_vulnerable_dependency(
    import_name: str,
    vulnerable: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    candidates = _import_package_candidates(import_name)
    for candidate in candidates:
        match = vulnerable.get(candidate)
        if match is not None:
            return match
    return None


def _import_package_candidates(import_name: str) -> list[str]:
    parts = [part for part in str(import_name).split(".") if part]
    candidates = []
    for index in range(1, len(parts) + 1):
        candidates.append(_normalize_package(".".join(parts[:index])))
    return candidates


def _ensure_dependency_node(graph: nx.DiGraph, dependency: dict[str, Any]) -> str:
    node_id = f"dependency::{_normalize_package(dependency['name'])}"
    vulnerability_ids = _vulnerability_ids(dependency["vulnerabilities"])
    if graph.has_node(node_id):
        graph.nodes[node_id].update(
            version=dependency.get("version"),
            vulnerability_ids=vulnerability_ids,
            vulnerability_count=len(vulnerability_ids),
        )
    else:
        graph.add_node(
            node_id,
            id=node_id,
            type="Dependency",
            name=dependency["name"],
            qualified_name=dependency["name"],
            file_path="",
            line_start=0,
            line_end=0,
            version=dependency.get("version"),
            vulnerability_ids=vulnerability_ids,
            vulnerability_count=len(vulnerability_ids),
            findings=[],
        )
    return node_id


def _add_vulnerable_import_edge(
    graph: nx.DiGraph,
    source_node: str,
    package_node: str,
    dependency: dict[str, Any],
    imported: dict[str, Any],
) -> bool:
    if graph.has_edge(source_node, package_node):
        existing = graph.edges[source_node, package_node]
        if existing.get("type") == EdgeType.IMPORTS_VULNERABLE.value:
            return False
    edge_attrs = edge_attrs_to_graph(
        EdgeAttrs(
            type=EdgeType.IMPORTS_VULNERABLE,
            source="pip-audit",
            target=dependency["name"],
            confidence=1.0,
        )
    )
    edge_attrs.update(
        {
            "package": dependency["name"],
            "version": dependency.get("version"),
            "import_name": imported.get("name"),
            "line": imported.get("line_start"),
            "vulnerability_ids": _vulnerability_ids(dependency["vulnerabilities"]),
            "findings": [_finding_payload(dependency, imported)],
        }
    )
    graph.add_edge(source_node, package_node, **edge_attrs)
    return True


def _finding_payload(dependency: dict[str, Any], imported: dict[str, Any]) -> dict[str, Any]:
    vulnerability_ids = _vulnerability_ids(dependency["vulnerabilities"])
    return {
        "source": "pip-audit",
        "code": ",".join(vulnerability_ids) or "vulnerable_dependency",
        "severity": "HIGH",
        "confidence": "EXTRACTED",
        "message": f"{dependency['name']} {dependency.get('version') or ''} has known vulnerabilities",
        "package": dependency["name"],
        "version": dependency.get("version"),
        "import_name": imported.get("name"),
        "line": imported.get("line_start"),
        "vulnerability_ids": vulnerability_ids,
    }


def _vulnerability_ids(vulnerabilities: list[dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for vulnerability in vulnerabilities:
        vuln_id = vulnerability.get("id") or vulnerability.get("vulnerability_id")
        if vuln_id:
            ids.append(str(vuln_id))
        for alias in vulnerability.get("aliases") or []:
            if str(alias).startswith("CVE-"):
                ids.append(str(alias))
    return sorted(set(ids))


def _clear_imports_vulnerable_edges(graph: nx.DiGraph) -> None:
    edges_to_remove = [
        (source, target)
        for source, target, attrs in graph.edges(data=True)
        if attrs.get("type") == EdgeType.IMPORTS_VULNERABLE.value and attrs.get("source") == "pip-audit"
    ]
    graph.remove_edges_from(edges_to_remove)
    dependency_nodes = [
        node_id
        for node_id, attrs in graph.nodes(data=True)
        if str(node_id).startswith("dependency::")
        and attrs.get("type") == "Dependency"
        and graph.degree(node_id) == 0
    ]
    graph.remove_nodes_from(dependency_nodes)


def _normalize_package(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()
