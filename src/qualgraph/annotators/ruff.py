"""Ruff lint annotator."""

from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.locations import find_node_for_location


class RuffAnnotator(BaseAnnotator):
    name = "ruff"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("ruff") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        completed = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--output-format=json", "--select=ALL", "."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode not in (0, 1):
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "ruff failed")

        findings = json.loads(completed.stdout or "[]")
        nodes_touched: set[str] = set()
        for finding in findings:
            filename = finding.get("filename")
            row = (finding.get("location") or {}).get("row")
            if not filename or row is None:
                continue
            node_id = find_node_for_location(graph, _relative_to_repo(repo_path, filename), int(row))
            if node_id is None:
                continue
            if add_finding(graph.nodes[node_id], _finding_payload(finding)):
                nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _finding_payload(finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "ruff",
        "code": finding.get("code"),
        "message": finding.get("message"),
        "location": finding.get("location"),
        "end_location": finding.get("end_location"),
        "fix": finding.get("fix"),
    }


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
