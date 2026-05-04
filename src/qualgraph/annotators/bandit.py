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
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.locations import find_node_for_location


SCAN_EXCLUDES = ".git,.hg,.mypy_cache,.pytest_cache,.qualgraph,.ruff_cache,.tox,.venv,__pycache__,build,dist,htmlcov,venv"


class BanditAnnotator(BaseAnnotator):
    name = "bandit"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("bandit") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        completed = subprocess.run(
            [sys.executable, "-m", "bandit", "-r", ".", "-f", "json", "-x", SCAN_EXCLUDES, "-s", "B101"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode not in (0, 1):
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "bandit failed")

        raw_output = completed.stdout.strip()
        if not raw_output:
            return AnnotatorResult(name=self.name)
        json_start = raw_output.find("{")
        if json_start < 0:
            message = completed.stderr.strip() or raw_output
            return AnnotatorResult(name=self.name, errors=[f"bandit did not emit JSON: {message}"])

        try:
            payload = json.loads(raw_output[json_start:] or "{}")
        except json.JSONDecodeError as exc:
            message = completed.stderr.strip() or completed.stdout.strip() or str(exc)
            return AnnotatorResult(name=self.name, errors=[f"bandit did not emit JSON: {message}"])
        nodes_touched: set[str] = set()
        located_nodes: set[str] = set()
        suppressed_low_signal = 0
        for finding in payload.get("results", []):
            filename = finding.get("filename")
            line_number = finding.get("line_number")
            if not filename or line_number is None:
                continue
            node_id = find_node_for_location(graph, _relative_to_repo(repo_path, filename), int(line_number))
            if node_id is None:
                continue
            located_nodes.add(node_id)
            if _is_low_signal_finding(finding):
                suppressed_low_signal += 1
                continue
            if add_finding(graph.nodes[node_id], _finding_payload(finding)):
                nodes_touched.add(node_id)

        return AnnotatorResult(
            name=self.name,
            nodes_annotated=len(nodes_touched),
            extra_counts={
                "results_scanned": len(payload.get("results", []) or []),
                "nodes_matched": len(located_nodes),
                "suppressed_low_signal": suppressed_low_signal,
            },
        )


def _finding_payload(finding: dict[str, Any]) -> dict[str, Any]:
    issue_cwe = finding.get("issue_cwe") or {}
    return {
        "source": "bandit",
        "severity": finding.get("issue_severity"),
        "severity_num": _severity_num(finding.get("issue_severity")),
        "confidence": finding.get("issue_confidence"),
        "cwe": issue_cwe.get("id"),
        "message": finding.get("issue_text"),
        "test_id": finding.get("test_id"),
        "line": finding.get("line_number"),
    }


def _is_low_signal_finding(finding: dict[str, Any]) -> bool:
    return str(finding.get("test_id") or "").upper() == "B101"


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _severity_num(severity: Any) -> float:
    return {
        "HIGH": 1.0,
        "MEDIUM": 0.66,
        "LOW": 0.33,
    }.get(str(severity or "").upper(), 0.0)
