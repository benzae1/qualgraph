"""Vulture dead-code annotator."""

from __future__ import annotations

import re
import importlib.util
import subprocess
import sys
from pathlib import Path

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.locations import find_node_for_location


WHITELIST_LOCATION_RE = re.compile(r"\((?P<path>.+?):(?P<line>\d+)\)")


class VultureAnnotator(BaseAnnotator):
    name = "vulture"
    version = "1.0"

    def is_available(self) -> bool:
        return importlib.util.find_spec("vulture") is not None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        completed = subprocess.run(
            [sys.executable, "-m", "vulture", ".", "--make-whitelist"],
            cwd=repo_path,
            capture_output=True,
            text=True,
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
            attrs.setdefault("findings", []).append(
                {
                    "source": "vulture",
                    "message": line.strip(),
                    "line": int(match.group("line")),
                }
            )
            nodes_touched.add(node_id)

        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
