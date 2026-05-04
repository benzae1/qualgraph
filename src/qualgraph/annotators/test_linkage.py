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
        static_edges = _add_static_test_edges(graph)
        dynamic_edges, note = _add_dynamic_context_edges(graph, repo_path)
        extra_counts = {
            "static_edges": static_edges,
            "coverage_context_edges": dynamic_edges,
        }
        if note:
            extra_counts["note"] = note
        return AnnotatorResult(
            name=self.name,
            edges_added=static_edges + dynamic_edges,
            extra_counts=extra_counts,
        )


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
                **{
                    **edge_attrs_to_graph(EdgeAttrs(type=EdgeType.TESTED_BY)),
                    "linkage_source": "static",
                },
            )
            edges_added += 1
    return edges_added


def _add_dynamic_context_edges(graph: nx.DiGraph, repo_path: Path) -> tuple[int, str | None]:
    coverage_file = repo_path / ".coverage"
    if not coverage_file.exists():
        return 0, "no coverage data available"

    cov = coverage.Coverage(data_file=str(coverage_file))
    try:
        cov.load()
    except coverage.CoverageException:
        return 0, "coverage data unreadable"
    data = cov.get_data()
    if not hasattr(data, "contexts_by_lineno"):
        return 0, "coverage context data unavailable"

    test_nodes = [
        {
            "node_id": node_id,
            "name": attrs.get("name"),
            "qualified_name": attrs.get("qualified_name"),
            "file_path": attrs.get("file_path"),
        }
        for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") == NodeType.TEST_FUNCTION.value
    ]
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
                        **{
                            **edge_attrs_to_graph(EdgeAttrs(type=EdgeType.TESTED_BY)),
                            "linkage_source": "coverage_context",
                        },
                    )
                    edges_added += 1
    return edges_added, None if edges_added else "no coverage-context links found"


def _match_test_context(context: str, test_nodes: list[dict[str, str | None]]) -> str | None:
    normalized_context = context.replace("\\", "/")
    for test_node in test_nodes:
        test_name = test_node.get("name")
        qualified_name = str(test_node.get("qualified_name") or "").replace(".", "::")
        file_path = str(test_node.get("file_path") or "").replace("\\", "/")
        if qualified_name and qualified_name in normalized_context:
            return test_node["node_id"]
        if file_path and file_path in normalized_context and test_name and str(test_name) in normalized_context:
            return test_node["node_id"]
        if test_name and str(test_name) in normalized_context:
            return test_node["node_id"]
    return None


def _relative_to_repo(repo_path: Path, filename: str) -> str:
    path = Path(filename)
    try:
        return path.resolve().relative_to(repo_path.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
