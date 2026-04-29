"""Detect-secrets annotator."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.locations import find_node_for_location


class SecretsAnnotator(BaseAnnotator):
    name = "detect-secrets"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("detect_secrets") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        completed = subprocess.run(
            [sys.executable, "-m", "detect_secrets", "scan", "--all-files"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "detect-secrets failed")

        payload = json.loads(completed.stdout or "{}")
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
