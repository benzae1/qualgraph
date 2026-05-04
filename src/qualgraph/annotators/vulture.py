"""Vulture dead-code annotator."""

from __future__ import annotations

import re
import importlib.util
import subprocess
import sys
from pathlib import Path

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.locations import find_node_for_location


WHITELIST_LOCATION_RE = re.compile(r"\((?P<path>.+?):(?P<line>\d+)\)")
SCAN_EXCLUDES = ".git,.hg,.mypy_cache,.pytest_cache,.qualgraph,.ruff_cache,.tox,.venv,__pycache__,build,dist,htmlcov,venv"


class VultureAnnotator(BaseAnnotator):
    name = "vulture"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("vulture") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        for _node_id, attrs in graph.nodes(data=True):
            attrs.pop("dead_code", None)

        completed = subprocess.run(
            [sys.executable, "-m", "vulture", ".", "--make-whitelist", "--exclude", SCAN_EXCLUDES],
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode not in (0, 1, 2, 3):
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "vulture failed")

        nodes_touched: set[str] = set()
        for line in completed.stdout.splitlines():
            match = WHITELIST_LOCATION_RE.search(line)
            if match is None:
                continue
            node_id = find_node_for_location(
                graph,
                _relative_to_repo(repo_path, match.group("path")),
                int(match.group("line")),
            )
            if node_id is None:
                continue
            attrs = graph.nodes[node_id]
            attrs["dead_code"] = True
            if add_finding(
                attrs,
                {
                    "source": "vulture",
                    "code": _vulture_code(line),
                    "severity": _vulture_severity(line),
                    "confidence": "EXTRACTED",
                    "message": line.strip(),
                    "line": int(match.group("line")),
                },
            ):
                nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _vulture_code(line: str) -> str:
    text = line.lower()
    if "unused variable" in text:
        return "unused_variable"
    if "unused import" in text:
        return "unused_import"
    if "unused function" in text:
        return "unused_function"
    if "unused method" in text:
        return "unused_method"
    if "unused class" in text:
        return "unused_class"
    if "unused attribute" in text:
        return "unused_attribute"
    return "dead_code"


def _vulture_severity(line: str) -> str:
    code = _vulture_code(line)
    if code in {"unused_function", "unused_method", "unused_class"}:
        return "MEDIUM"
    return "LOW"
