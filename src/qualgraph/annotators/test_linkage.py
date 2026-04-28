"""Test-to-code linkage annotator."""

from __future__ import annotations

from pathlib import Path

import coverage
import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.locations import find_node_for_location
from qualgraph.graph.schema import EdgeAttrs, EdgeType, NodeType, edge_attrs_to_graph


class TestLinkageAnnotator(BaseAnnotator):
    name = "test_linkage"
    version = "1.0"

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        edges_added = _add_static_test_edges(graph)
        edges_added += _add_dynamic_context_edges(graph, repo_path)
        return AnnotatorResult(name=self.name, edges_added=edges_added)


def _add_static_test_edges(graph: nx.DiGraph) -> int:
    edges_added = 0
    for source, target, attrs in list(graph.edges(data=True)):
        if attrs.get("type") != EdgeType.CALLS.value:
            continue
        source_type = graph.nodes[source].get("type")
        target_type = graph.nodes[target].get("type")
        if source_type != NodeType.TEST_FUNCTION.value or target_type == NodeType.TEST_FUNCTION.value:
            continue
        if not graph.has_edge(target, source):
            graph.add_edge(
                target,
                source,
                **edge_attrs_to_graph(EdgeAttrs(type=EdgeType.TESTED_BY, source="static")),
            )
            edges_added += 1
    return edges_added


def _add_dynamic_context_edges(graph: nx.DiGraph, repo_path: Path) -> int:
    coverage_file = repo_path / ".coverage"
    if not coverage_file.exists():
        return 0

    cov = coverage.Coverage(data_file=str(coverage_file))
    try:
        cov.load()
    except coverage.CoverageException:
        return 0
    data = cov.get_data()
    if not hasattr(data, "contexts_by_lineno"):
        return 0

    test_nodes = {
        attrs.get("name"): node_id
        for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") == NodeType.TEST_FUNCTION.value
    }
    edges_added = 0
    for measured_file in data.measured_files():
        try:
            contexts_by_line = data.contexts_by_lineno(measured_file)
        except coverage.CoverageException:
            continue
        relative = _relative_to_repo(repo_path, measured_file)
        for line, contexts in contexts_by_line.items():
            code_node = find_node_for_location(graph, relative, int(line))
            if code_node is None or graph.nodes[code_node].get("type") == NodeType.TEST_FUNCTION.value:
                continue
            for context in contexts:
                test_node = _match_test_context(context, test_nodes)
                if test_node and not graph.has_edge(code_node, test_node):
                    graph.add_edge(
                        code_node,
                        test_node,
                        **edge_attrs_to_graph(EdgeAttrs(type=EdgeType.TESTED_BY, source="coverage_context")),
                    )
                    edges_added += 1
    return edges_added


def _match_test_context(context: str, test_nodes: dict[str | None, str]) -> str | None:
    for test_name, node_id in test_nodes.items():
        if test_name and test_name in context:
            return node_id
    return None


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
