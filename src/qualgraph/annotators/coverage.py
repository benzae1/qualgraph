"""Coverage.py annotator."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import coverage
import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator


class CoverageAnnotator(BaseAnnotator):
    name = "coverage"
    version = "1.0"

    def __init__(
        self,
        *,
        mode: str = "auto",
        pytest_args: list[str] | None = None,
    ) -> None:
        self.mode = mode
        self.pytest_args = list(pytest_args or [])

    def is_available(self) -> bool:
        return importlib.util.find_spec("coverage") is not None and importlib.util.find_spec("pytest") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        if not _has_tests(repo_path):
            return AnnotatorResult(name=self.name)

        coverage_file = repo_path / ".coverage"
        errors: list[str] = []
        if self.mode == "skip":
            return AnnotatorResult(name=self.name, errors=["coverage run skipped"])
        if self.mode == "reuse" and not coverage_file.exists():
            return AnnotatorResult(name=self.name, errors=[f"coverage data not found: {coverage_file}"])
        if self.mode == "run" or (self.mode == "auto" and not coverage_file.exists()):
            rcfile = _write_context_rcfile(repo_path)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "coverage",
                    "run",
                    "--rcfile",
                    str(rcfile),
                    "-m",
                    "pytest",
                    "--continue-on-collection-errors",
                    *self.pytest_args,
                ],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=False,
            )
            error = _subprocess_error(completed)
            if completed.returncode != 0 and not coverage_file.exists():
                raise RuntimeError(error or "coverage run failed")
            if completed.returncode != 0 and error:
                errors.append(error)

        cov = coverage.Coverage(data_file=str(coverage_file))
        cov.load()
        nodes_annotated = 0
        nodes_by_file = _nodes_by_file(graph)

        for measured_file in cov.get_data().measured_files():
            try:
                filename, statements, _excluded, missing, _missing_text = cov.analysis2(measured_file)
            except coverage.CoverageException:
                continue
            relative = _relative_to_repo(repo_path, filename)
            candidates = nodes_by_file.get(relative)
            if not candidates:
                continue
            executable = set(statements)
            missing_lines = set(missing)
            for attrs, line_start, line_end in candidates:
                node_lines = set(range(line_start, line_end + 1))
                executable_in_node = executable & node_lines
                if not executable_in_node:
                    continue
                missing_in_node = missing_lines & executable_in_node
                attrs["coverage_line"] = 1 - (len(missing_in_node) / len(executable_in_node))
                nodes_annotated += 1

        return AnnotatorResult(name=self.name, nodes_annotated=nodes_annotated, errors=errors)


def _has_tests(repo_path: Path) -> bool:
    tests_dir = repo_path / "tests"
    return tests_dir.exists() and any(tests_dir.rglob("test*.py"))


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _write_context_rcfile(repo_path: Path) -> Path:
    qualgraph_dir = repo_path / ".qualgraph"
    qualgraph_dir.mkdir(parents=True, exist_ok=True)
    rcfile = qualgraph_dir / "coverage-context.ini"
    rcfile.write_text(
        "[run]\n"
        "branch = True\n"
        "relative_files = True\n"
        "dynamic_context = test_function\n",
        encoding="utf-8",
    )
    return rcfile


def _nodes_by_file(graph: nx.DiGraph) -> dict[str, list[tuple[dict, int, int]]]:
    by_file: dict[str, list[tuple[dict, int, int]]] = defaultdict(list)
    for _node_id, attrs in graph.nodes(data=True):
        file_path = attrs.get("file_path")
        line_start = attrs.get("line_start")
        line_end = attrs.get("line_end")
        if not file_path or line_start is None or line_end is None:
            continue
        by_file[str(file_path)].append((attrs, int(line_start), int(line_end)))
    return by_file


def _subprocess_error(completed: subprocess.CompletedProcess[str]) -> str:
    stderr = completed.stderr.strip()
    stdout = completed.stdout.strip()
    if stderr and stdout:
        return f"{stderr}\n{stdout}"
    return stderr or stdout
