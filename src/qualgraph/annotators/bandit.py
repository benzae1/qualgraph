"""Bandit security annotator."""

from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.locations import find_node_for_location


class BanditAnnotator(BaseAnnotator):
    name = "bandit"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("bandit") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        completed = subprocess.run(
            [sys.executable, "-m", "bandit", "-r", ".", "-f", "json"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode not in (0, 1):
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "bandit failed")

        payload = json.loads(completed.stdout or "{}")
        nodes_touched: set[str] = set()
        for finding in payload.get("results", []):
            filename = finding.get("filename")
            line_number = finding.get("line_number")
            if not filename or line_number is None:
                continue
            node_id = find_node_for_location(graph, _relative_to_repo(repo_path, filename), int(line_number))
            if node_id is None:
                continue
            graph.nodes[node_id].setdefault("findings", []).append(_finding_payload(finding))
            nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _finding_payload(finding: dict[str, Any]) -> dict[str, Any]:
    issue_cwe = finding.get("issue_cwe") or {}
    return {
        "source": "bandit",
        "severity": finding.get("issue_severity"),
        "confidence": finding.get("issue_confidence"),
        "cwe": issue_cwe.get("id"),
        "message": finding.get("issue_text"),
        "test_id": finding.get("test_id"),
        "line": finding.get("line_number"),
    }


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
