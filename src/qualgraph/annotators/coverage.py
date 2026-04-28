"""Coverage.py annotator."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import coverage
import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator


class CoverageAnnotator(BaseAnnotator):
    name = "coverage"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("coverage") is not None and importlib.util.find_spec("pytest") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        if not _has_tests(repo_path):
            return AnnotatorResult(name=self.name)

        completed = subprocess.run(
            [sys.executable, "-m", "coverage", "run", "--branch", "-m", "pytest"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "coverage run failed")

        cov = coverage.Coverage(data_file=str(repo_path / ".coverage"))
        cov.load()
        nodes_annotated = 0

        for measured_file in cov.get_data().measured_files():
            try:
                filename, statements, _excluded, missing, _missing_text = cov.analysis2(measured_file)
            except coverage.CoverageException:
                continue
            relative = _relative_to_repo(repo_path, filename)
            executable = set(statements)
            missing_lines = set(missing)
            for _node_id, attrs in graph.nodes(data=True):
                if attrs.get("file_path") != relative:
                    continue
                node_lines = set(range(int(attrs["line_start"]), int(attrs["line_end"]) + 1))
                executable_in_node = executable & node_lines
                if not executable_in_node:
                    continue
                missing_in_node = missing_lines & executable_in_node
                attrs["coverage_line"] = 1 - (len(missing_in_node) / len(executable_in_node))
                nodes_annotated += 1

        return AnnotatorResult(name=self.name, nodes_annotated=nodes_annotated)


def _has_tests(repo_path: Path) -> bool:
    tests_dir = repo_path / "tests"
    return tests_dir.exists() and any(tests_dir.rglob("test*.py"))


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
