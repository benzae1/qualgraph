"""Ruff lint annotator."""

from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.locations import find_node_for_location


class RuffAnnotator(BaseAnnotator):
    name = "ruff"
    version = "1.0"
    default_select = "E,F,W,B,C90,S,SIM,RUF"

    def is_available(self) -> bool:
        return importlib.util.find_spec("ruff") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        command = [sys.executable, "-m", "ruff", "check", "--output-format=json"]
        if not _has_ruff_config(repo_path):
            command.extend([f"--select={self.default_select}"])
        command.append(".")
        completed = subprocess.run(
            command,
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
            relative = _relative_to_repo(repo_path, filename)
            if _skip_low_signal_test_finding(relative, finding):
                continue
            node_id = find_node_for_location(graph, relative, int(row))
            if node_id is None:
                continue
            if add_finding(graph.nodes[node_id], _finding_payload(finding, repo_path, relative)):
                nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _finding_payload(finding: dict[str, Any], repo_path: Path, relative_path: str) -> dict[str, Any]:
    row = (finding.get("location") or {}).get("row")
    return {
        "source": "ruff",
        "code": finding.get("code"),
        "message": finding.get("message"),
        "location": finding.get("location"),
        "end_location": finding.get("end_location"),
        "fix": finding.get("fix"),
        "line": row,
        "evidence": _source_line(repo_path, relative_path, row),
    }


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _has_ruff_config(repo_path: Path) -> bool:
    if (repo_path / "ruff.toml").exists() or (repo_path / ".ruff.toml").exists():
        return True
    pyproject = repo_path / "pyproject.toml"
    if not pyproject.exists():
        return False
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return False
    return "ruff" in (data.get("tool") or {})


def _skip_low_signal_test_finding(relative_path: str, finding: dict[str, Any]) -> bool:
    if not _is_test_path(relative_path):
        return False
    code = str(finding.get("code") or "")
    return code == "S101" or code.startswith("D")


def _is_test_path(relative_path: str) -> bool:
    normalized = relative_path.replace("\\", "/")
    return normalized.startswith("tests/") or "/tests/" in normalized or Path(normalized).name.startswith("test_")


def _source_line(repo_path: Path, relative_path: str, row: Any) -> str:
    if row is None:
        return ""
    try:
        line_number = int(row)
    except (TypeError, ValueError):
        return ""
    try:
        lines = (repo_path / relative_path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1].strip()
    return ""
