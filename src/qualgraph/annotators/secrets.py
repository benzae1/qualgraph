"""Detect-secrets annotator."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import networkx as nx
from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.locations import find_node_for_location


EXCLUDED_PARTS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".qualgraph",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "venv",
}


class SecretsAnnotator(BaseAnnotator):
    name = "detect-secrets"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("detect_secrets") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        payload = _scan_secrets(repo_path, _python_files_from_graph(graph))
        nodes_touched: set[str] = set()
        for filename, findings in (payload.get("results") or {}).items():
            for finding in findings or []:
                line_number = finding.get("line_number")
                if line_number is None:
                    continue
                node_id = find_node_for_location(graph, _relative_to_repo(repo_path, filename), int(line_number))
                if node_id is None:
                    continue
                if add_finding(graph.nodes[node_id], _finding_payload(filename, finding)):
                    nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _scan_secrets(repo_path: Path, filenames: list[str]) -> dict[str, Any]:
    collection = SecretsCollection(root=str(repo_path))
    with default_settings():
        for filename in filenames:
            collection.scan_file(filename)
    return {"results": collection.json()}


def _python_files_from_graph(graph: nx.DiGraph) -> list[str]:
    files = {
        str(attrs.get("file_path"))
        for _node_id, attrs in graph.nodes(data=True)
        if attrs.get("file_path") and not _excluded(str(attrs.get("file_path")))
    }
    return sorted(files)


def _excluded(filename: str) -> bool:
    normalized = Path(filename).as_posix()
    return any(part in EXCLUDED_PARTS for part in normalized.split("/"))


def _finding_payload(filename: str, finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "detect-secrets",
        "code": finding.get("type") or "secret",
        "severity": "LOW",
        "confidence": "AMBIGUOUS",
        "message": f"Potential secret detected: {finding.get('type') or 'unknown'}",
        "file": filename,
        "line": finding.get("line_number"),
        "is_verified": bool(finding.get("is_verified")),
        "hashed_secret": finding.get("hashed_secret"),
    }


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
