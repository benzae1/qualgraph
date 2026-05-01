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
    default_select = "E,F,W,B,C90,SIM,RUF"

    def is_available(self) -> bool:
        return importlib.util.find_spec("ruff") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        command = [sys.executable, "-m", "ruff", "check", "--output-format=json"]
        if not _has_ruff_config(repo_path):
            command.extend([f"--select={self.default_select}"])
        command.append(".")
        completed = _run_ruff(command, repo_path)
        if completed.returncode not in (0, 1) and _looks_like_config_error(completed):
            command = [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--output-format=json",
                "--isolated",
                f"--select={self.default_select}",
                ".",
            ]
            completed = _run_ruff(command, repo_path)
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
            if _skip_low_signal_finding(relative, finding):
                continue
            node_id = find_node_for_location(graph, relative, int(row))
            if node_id is None:
                continue
            if add_finding(graph.nodes[node_id], _finding_payload(finding, repo_path, relative)):
                nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _finding_payload(finding: dict[str, Any], repo_path: Path, relative_path: str) -> dict[str, Any]:
    row = (finding.get("location") or {}).get("row")
    severity = _severity_for_rule(str(finding.get("code") or ""))
    return {
        "source": "ruff",
        "code": finding.get("code"),
        "severity": severity,
        "severity_num": _severity_num(severity),
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


def _run_ruff(command: list[str], repo_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False,
    )


def _looks_like_config_error(completed: subprocess.CompletedProcess[str]) -> bool:
    output = f"{completed.stderr}\n{completed.stdout}".lower()
    return "failed to parse" in output or "toml parse error" in output or "unknown rule selector" in output


def _skip_low_signal_finding(relative_path: str, finding: dict[str, Any]) -> bool:
    code = str(finding.get("code") or "")
    if code == "S101":
        return True
    if not _is_test_path(relative_path):
        return False
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


def _severity_for_rule(code: str) -> str:
    if code.startswith("F"):
        return "MEDIUM"
    if code.startswith("B"):
        return "MEDIUM"
    if code.startswith("S"):
        return "MEDIUM"
    if code.startswith("C90"):
        return "MEDIUM"
    if code in {"RUF006", "RUF015", "RUF018", "RUF100"}:
        return "MEDIUM"
    return "LOW"


def _severity_num(severity: str) -> float:
    return {
        "HIGH": 1.0,
        "MEDIUM": 0.66,
        "LOW": 0.33,
    }.get(severity.upper(), 0.0)
