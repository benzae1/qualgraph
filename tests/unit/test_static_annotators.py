from pathlib import Path

import networkx as nx

from qualgraph.annotators.docstring import DocstringAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.git_history import _relative_to_target
from qualgraph.annotators.locations import find_node_for_location
from qualgraph.annotators.radon import RadonAnnotator
from qualgraph.annotators.test_linkage import TestLinkageAnnotator
from qualgraph.graph.builder import build_graph
from qualgraph.graph.metrics import annotate_metrics
from qualgraph.graph.schema import NodeAttrs, NodeType, node_attrs_to_graph
from qualgraph.report.markdown import render_markdown_report


def test_find_node_for_location_prefers_smallest_containing_node() -> None:
    graph = nx.DiGraph()
    graph.add_node(
        "module",
        **node_attrs_to_graph(
            NodeAttrs(
                id="module",
                type=NodeType.MODULE,
                name="sample",
                qualified_name="sample",
                file_path="sample.py",
                line_start=1,
                line_end=20,
            )
        ),
    )
    graph.add_node(
        "function",
        **node_attrs_to_graph(
            NodeAttrs(
                id="function",
                type=NodeType.FUNCTION,
                name="work",
                qualified_name="sample.work",
                file_path="sample.py",
                line_start=5,
                line_end=8,
            )
        ),
    )

    assert find_node_for_location(graph, "sample.py", 6) == "function"
    assert find_node_for_location(graph, "sample.py", 2) == "module"
    assert find_node_for_location(graph, "missing.py", 6) is None


def test_radon_and_docstring_annotate_tiny_repo_nodes() -> None:
    repo = Path("benchmarks/repos/tiny_repo")
    graph = build_graph(repo, [])

    radon_result = RadonAnnotator().annotate(graph, repo)
    docstring_result = DocstringAnnotator().annotate(graph, repo)

    assert radon_result.nodes_annotated > 0
    assert docstring_result.nodes_annotated > 0
    assert any(attrs.get("complexity") for _node_id, attrs in graph.nodes(data=True))
    assert any(attrs.get("has_docstring") is not None for _node_id, attrs in graph.nodes(data=True))


def test_test_linkage_adds_static_tested_by_edges() -> None:
    repo = Path("benchmarks/repos/tiny_repo")
    graph = build_graph(repo, [])

    result = TestLinkageAnnotator().annotate(graph, repo)

    assert result.edges_added > 0
    assert any(attrs.get("type") == "tested_by" for _source, _target, attrs in graph.edges(data=True))


def test_git_history_path_mapping_for_nested_repo_targets() -> None:
    assert _relative_to_target("benchmarks/repos/tiny_repo/tiny_shop/orders.py", "benchmarks/repos/tiny_repo") == (
        "tiny_shop/orders.py"
    )
    assert _relative_to_target("src/qualgraph/cli.py", "benchmarks/repos/tiny_repo") is None


def test_findings_helpers_dedupe_and_clear_by_source() -> None:
    attrs = {"findings": []}
    finding = {"source": "ruff", "code": "E501", "message": "line too long", "location": {"row": 4, "column": 1}}

    assert add_finding(attrs, finding) is True
    assert add_finding(attrs, dict(finding)) is False
    assert len(attrs["findings"]) == 1

    graph = nx.DiGraph()
    graph.add_node("node", findings=[finding, {"source": "bandit", "test_id": "B101"}])
    clear_findings_by_source(graph, "ruff")

    assert graph.nodes["node"]["findings"] == [{"source": "bandit", "test_id": "B101"}]


def test_report_surfaces_deduped_rules_hotspots_and_readable_centrality() -> None:
    graph = nx.DiGraph()
    graph.add_node(
        "module",
        **node_attrs_to_graph(
            NodeAttrs(
                id="module",
                type=NodeType.MODULE,
                name="sample",
                qualified_name="sample",
                file_path="sample.py",
                line_start=1,
                line_end=20,
            )
        ),
    )
    graph.add_node(
        "function",
        **node_attrs_to_graph(
            NodeAttrs(
                id="function",
                type=NodeType.FUNCTION,
                name="work",
                qualified_name="sample.work",
                file_path="sample.py",
                line_start=5,
                line_end=8,
                coverage_line=0.25,
                complexity=6,
                churn=4,
            )
        ),
    )
    finding = {"source": "ruff", "code": "E501", "message": "line too long", "location": {"row": 6, "column": 1}}
    graph.nodes["function"]["findings"] = [finding, dict(finding)]
    graph.add_edge("module", "function", type="calls")
    annotate_metrics(graph)

    report = render_markdown_report(graph)

    assert "- Findings: 1" in report
    assert "## Top Finding Rules" in report
    assert "ruff E501: 1" in report
    assert "## Risk Hotspots" in report
    assert "score=" in report
    assert "betweenness=" in report
