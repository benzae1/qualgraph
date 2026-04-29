from pathlib import Path
from unittest.mock import patch

import networkx as nx

from qualgraph.annotators.docstring import DocstringAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.git_history import _relative_to_target
from qualgraph.annotators.locations import find_node_for_location
from qualgraph.annotators.pip_audit import PipAuditAnnotator
from qualgraph.annotators.radon import RadonAnnotator
from qualgraph.annotators.secrets import SecretsAnnotator
from qualgraph.annotators.test_linkage import TestLinkageAnnotator
from qualgraph.findings.cross_signal import detect_untested_hotspots
from qualgraph.graph.builder import build_graph
from qualgraph.graph.metrics import annotate_metrics
from qualgraph.graph.schema import NodeAttrs, NodeType, node_attrs_to_graph
from qualgraph.report.markdown import render_markdown_report
from qualgraph.scoring.risk import score, top_risk_nodes


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


def test_detect_untested_hotspots_combines_complexity_centrality_and_coverage() -> None:
    graph = nx.DiGraph()
    graph.add_node(
        "hotspot",
        type=NodeType.FUNCTION.value,
        complexity=12,
        centrality=0.9,
        coverage_line=0.0,
    )
    graph.add_node(
        "covered_hotspot",
        type=NodeType.METHOD.value,
        complexity=11,
        centrality=0.8,
        coverage_line=0.75,
    )
    graph.add_node(
        "simple_center",
        type=NodeType.FUNCTION.value,
        complexity=2,
        centrality=0.95,
        coverage_line=0.0,
    )
    graph.add_node(
        "module",
        type=NodeType.MODULE.value,
        complexity=99,
        centrality=1.0,
        coverage_line=0.0,
    )

    findings = detect_untested_hotspots(graph, complexity_pct=0.5, centrality_pct=0.5)

    assert [finding.node_id for finding in findings] == ["hotspot"]
    assert findings[0].kind == "untested_hotspot"
    assert findings[0].severity == "high"
    assert findings[0].evidence == {"complexity": 12.0, "centrality": 0.9, "coverage": 0.0}


def test_pip_audit_adds_vulnerable_import_edges_to_importing_node() -> None:
    graph = _sample_graph_with_function()
    graph.graph["pending_imports"] = [
        {
            "source": "module",
            "name": "requests",
            "alias": "requests",
            "file_path": "sample.py",
            "line_start": 6,
        }
    ]
    payload = {
        "dependencies": [
            {
                "name": "requests",
                "version": "2.19.0",
                "vulns": [{"id": "PYSEC-1", "aliases": ["CVE-2024-0001"]}],
            }
        ]
    }

    with patch("qualgraph.annotators.pip_audit.subprocess.run", return_value=_completed(payload)):
        result = PipAuditAnnotator().annotate(graph, Path("."))

    assert result.edges_added == 1
    assert result.nodes_annotated == 1
    assert graph.has_edge("function", "dependency::requests")
    edge = graph.edges["function", "dependency::requests"]
    assert edge["type"] == "imports_vulnerable"
    assert edge["package"] == "requests"
    assert edge["vulnerability_ids"] == ["CVE-2024-0001", "PYSEC-1"]
    assert graph.nodes["function"]["findings"][0]["source"] == "pip-audit"


def test_detect_secrets_attaches_conservative_low_severity_findings() -> None:
    graph = _sample_graph_with_function()
    payload = {
        "results": {
            "sample.py": [
                {
                    "type": "Secret Keyword",
                    "line_number": 6,
                    "hashed_secret": "abc123",
                    "is_verified": False,
                }
            ]
        }
    }

    with patch("qualgraph.annotators.secrets.subprocess.run", return_value=_completed(payload)):
        result = SecretsAnnotator().annotate(graph, Path("."))

    assert result.nodes_annotated == 1
    finding = graph.nodes["function"]["findings"][0]
    assert finding["source"] == "detect-secrets"
    assert finding["severity"] == "LOW"
    assert finding["confidence"] == "AMBIGUOUS"


def test_risk_score_writes_weighted_components_for_llm_selection() -> None:
    graph = nx.DiGraph()
    graph.add_node(
        "low",
        type=NodeType.FUNCTION.value,
        centrality=0.1,
        complexity=1,
        churn=0,
        coverage_line=1.0,
    )
    graph.add_node(
        "high",
        type=NodeType.METHOD.value,
        centrality=0.9,
        complexity=12,
        churn=8,
        coverage_line=0.25,
        findings=[{"source": "bandit", "severity_num": 1.0}],
    )

    score(graph, {"w1": 1, "w2": 2, "w3": 3, "w4": 4, "w5": 5, "w6": 6, "w7": 7})

    components = graph.nodes["high"]["risk_components"]
    assert components == {
        "centrality": 1.0,
        "complexity": 2.0,
        "churn": 3.0,
        "coverage_gap": 3.0,
        "security": 5.0,
        "llm": 0.0,
        "hotpath": 0.0,
    }
    assert graph.nodes["high"]["risk_score"] == 14.0
    assert [node_id for node_id, _attrs in top_risk_nodes(graph, limit=1)] == ["high"]


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


def _sample_graph_with_function() -> nx.DiGraph:
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
    return graph


class _completed:
    def __init__(self, payload: dict) -> None:
        import json

        self.returncode = 0
        self.stdout = json.dumps(payload)
        self.stderr = ""
