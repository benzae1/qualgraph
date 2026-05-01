"""Git co-change annotator."""

from __future__ import annotations

import collections
import itertools
from pathlib import Path

import networkx as nx
from git import InvalidGitRepositoryError, Repo

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.git_history import _commit_records
from qualgraph.annotators.locations import nodes_for_file
from qualgraph.graph.schema import EdgeAttrs, EdgeType, NodeType, edge_attrs_to_graph


class CoChangeAnnotator(BaseAnnotator):
    name = "co_change"
    version = "1.0"

    def __init__(self, min_count: int = 5, min_rate: float = 0.5, max_commits: int | None = 1000) -> None:
        self.min_count = min_count
        self.min_rate = min_rate
        self.max_commits = max_commits

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        try:
            repo = Repo(repo_path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            return AnnotatorResult(name=self.name, errors=["not a git repository"])

        file_churn: collections.Counter[str] = collections.Counter()
        pair_counts: collections.Counter[tuple[str, str]] = collections.Counter()

        for commit in _commit_records(repo, repo_path, self.max_commits):
            touched = sorted(set(commit.files))
            for file_path in touched:
                file_churn[file_path] += 1
            for left, right in itertools.combinations(touched, 2):
                pair_counts[(left, right)] += 1

        edges_added = 0
        for (left, right), count in pair_counts.items():
            denominator = max(1, min(file_churn[left], file_churn[right]))
            rate = count / denominator
            if count < self.min_count or rate < self.min_rate:
                continue
            left_node = _module_node_for_file(graph, left)
            right_node = _module_node_for_file(graph, right)
            if not left_node or not right_node or left_node == right_node:
                continue
            graph.add_edge(
                left_node,
                right_node,
                **edge_attrs_to_graph(
                    EdgeAttrs(
                        type=EdgeType.CO_CHANGES_WITH,
                        source=left,
                        target=right,
                        weight=float(count),
                    )
                ),
            )
            graph[left_node][right_node]["co_change_count"] = count
            graph[left_node][right_node]["co_change_rate"] = rate
            edges_added += 1

        return AnnotatorResult(name=self.name, edges_added=edges_added)


def _module_node_for_file(graph: nx.DiGraph, file_path: str) -> str | None:
    for node_id in nodes_for_file(graph, file_path):
        if graph.nodes[node_id].get("type") == NodeType.MODULE.value:
            return node_id
    return None
