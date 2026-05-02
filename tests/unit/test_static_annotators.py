from pathlib import Path
from unittest.mock import patch

import networkx as nx

from qualgraph.annotators.cross_signal import CrossSignalAnnotator
from qualgraph.annotators.bandit import BanditAnnotator
from qualgraph.annotators.coverage import _write_context_rcfile
from qualgraph.annotators.docstring import DocstringAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.annotators.git_history import _relative_to_target
from qualgraph.annotators.locations import find_node_for_location
from qualgraph.annotators.pip_audit import PipAuditAnnotator
from qualgraph.annotators.profiler import ProfilerAnnotator
from qualgraph.annotators.radon import RadonAnnotator
from qualgraph.annotators.ruff import RuffAnnotator
from qualgraph.annotators.secrets import SecretsAnnotator
from qualgraph.annotators.test_linkage import TestLinkageAnnotator
from qualgraph.findings.cross_signal import (
    detect_cross_signal_findings,
    detect_complex_hotspots,
    detect_cyclic_dependencies,
    detect_god_nodes,
    detect_hidden_coupling,
    detect_outdated_documentation,
    detect_untested_hotspots,
    detect_vulnerable_usage,
)
from qualgraph.graph.builder import build_graph
from qualgraph.graph.clustering import cluster_leiden
from qualgraph.graph.metrics import annotate_metrics
from qualgraph.graph.schema import NodeAttrs, NodeType, node_attrs_to_graph
from qualgraph.report.json_export import EXPORT_SCHEMA_VERSION, export_json_data
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


def test_cluster_leiden_coarsens_large_tiny_cluster_sets() -> None:
    graph = nx.DiGraph()
    for index in range(250):
        graph.add_node(f"node-{index}", type=NodeType.FUNCTION.value, file_path=f"pkg/mod_{index}.py")

    clusters = cluster_leiden(graph)

    assert len(set(clusters.values())) <= 25


def test_cluster_leiden_splits_oversized_clusters() -> None:
    graph = nx.DiGraph()
    for index in range(1000):
        graph.add_node(f"node-{index}", type=NodeType.FUNCTION.value, file_path=f"pkg/area/mod_{index}.py")
        if index:
            graph.add_edge(f"node-{index - 1}", f"node-{index}", type="calls")
            graph.add_edge(f"node-{index}", "node-0", type="calls")

    clusters = cluster_leiden(graph)
    sizes = {}
    for cluster_id in clusters.values():
        sizes[cluster_id] = sizes.get(cluster_id, 0) + 1

    assert max(sizes.values()) <= 500


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
    assert any(attrs.get("linkage_source") == "static" for _source, _target, attrs in graph.edges(data=True))


def test_coverage_context_rcfile_enables_test_function_contexts(tmp_path: Path) -> None:
    rcfile = _write_context_rcfile(tmp_path)

    text = rcfile.read_text(encoding="utf-8")
    assert "branch = True" in text
    assert "dynamic_context = test_function" in text
    assert rcfile.parent.name == ".qualgraph"


def test_profiler_annotator_attributes_cprofile_json_by_file_and_line(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    profile_path = repo / "profile.json"
    profile_path.write_text(
        _json(
            {
                "total_time": 2.0,
                "functions": [
                    {
                        "filename": "sample.py",
                        "line": 5,
                        "call_count": 4,
                        "cum_time": 0.5,
                    },
                    {
                        "filename": "missing.py",
                        "line": 1,
                        "call_count": 1,
                        "cum_time": 0.25,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    graph = _sample_graph_with_function()

    result = ProfilerAnnotator(profile_path).annotate(graph, repo)

    assert result.nodes_annotated == 1
    attrs = graph.nodes["function"]
    assert attrs["profile_cum_time"] == 0.5
    assert attrs["profile_call_count"] == 4
    assert attrs["cpu_pct"] == 0.25
    assert attrs["hotpath_weight"] == 0.25
    assert graph.graph["profile_total_time"] == 2.0
    assert result.counts()["profile_records"] == 2
    assert result.counts()["max_cpu_pct"] == 0.25
    assert result.counts()["top_hotpath"] == "sample.work"


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


def test_ruff_uses_project_config_and_attaches_source_line_evidence(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[tool.ruff]\nline-length = 120\n", encoding="utf-8")
    (repo / "sample.py").write_text("\n\n\n\ndef work():\n    return 1\n", encoding="utf-8")
    graph = _sample_graph_with_function()
    payload = [
        {
            "filename": str(repo / "sample.py"),
            "code": "SIM101",
            "message": "example",
            "location": {"row": 6, "column": 5},
            "end_location": {"row": 6, "column": 13},
        }
    ]

    with patch("qualgraph.annotators.ruff.subprocess.run", return_value=_completed(payload)) as run:
        result = RuffAnnotator().annotate(graph, repo)

    command = run.call_args.args[0]
    assert "--select=E,F,W,B,C90,S,SIM,RUF" not in command
    assert result.nodes_annotated == 1
    finding = graph.nodes["function"]["findings"][0]
    assert finding["line"] == 6
    assert finding["evidence"] == "return 1"


def test_ruff_defaults_to_curated_rules_without_project_config(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "sample.py").write_text("\n\n\n\ndef work():\n    return 1\n", encoding="utf-8")
    graph = _sample_graph_with_function()

    with patch("qualgraph.annotators.ruff.subprocess.run", return_value=_completed([])) as run:
        RuffAnnotator().annotate(graph, repo)

    assert "--select=E,F,W,B,C90,SIM,RUF" in run.call_args.args[0]


def test_ruff_retries_with_isolated_defaults_when_project_config_is_incompatible(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[tool.ruff.lint]\nselect = ['TC']\n", encoding="utf-8")
    (repo / "sample.py").write_text("\n\n\n\ndef work():\n    return 1\n", encoding="utf-8")
    graph = _sample_graph_with_function()

    failed = _completed([], returncode=2, stderr="Failed to parse pyproject.toml\nUnknown rule selector: `TC`")
    with patch("qualgraph.annotators.ruff.subprocess.run", side_effect=[failed, _completed([])]) as run:
        result = RuffAnnotator().annotate(graph, repo)

    assert result.nodes_annotated == 0
    assert run.call_count == 2
    assert "--isolated" in run.call_args.args[0]
    assert "--select=E,F,W,B,C90,SIM,RUF" in run.call_args.args[0]


def test_ruff_drops_assert_rule_and_maps_severity(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "sample.py").write_text("\n\n\n\ndef work():\n    return missing_name\n", encoding="utf-8")
    graph = _sample_graph_with_function()
    payload = [
        {
            "filename": str(repo / "sample.py"),
            "code": "S101",
            "message": "Use of assert detected",
            "location": {"row": 6, "column": 5},
        },
        {
            "filename": str(repo / "sample.py"),
            "code": "F821",
            "message": "Undefined name `missing_name`",
            "location": {"row": 6, "column": 12},
        },
    ]

    with patch("qualgraph.annotators.ruff.subprocess.run", return_value=_completed(payload)):
        result = RuffAnnotator().annotate(graph, repo)

    assert result.nodes_annotated == 1
    finding = graph.nodes["function"]["findings"][0]
    assert finding["code"] == "F821"
    assert finding["severity"] == "MEDIUM"
    assert finding["severity_num"] == 0.66


def test_bandit_reports_suppressed_low_signal_findings(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "sample.py").write_text("\n\n\n\ndef work():\n    subprocess.Popen(cmd, shell=True)\n", encoding="utf-8")
    graph = _sample_graph_with_function()
    payload = {
        "results": [
            {
                "filename": str(repo / "sample.py"),
                "line_number": 6,
                "test_id": "B101",
                "issue_text": "Use of assert detected",
            },
            {
                "filename": str(repo / "sample.py"),
                "line_number": 6,
                "test_id": "B602",
                "issue_text": "subprocess call with shell=True identified",
                "issue_severity": "HIGH",
                "issue_confidence": "HIGH",
            },
        ]
    }

    with patch("qualgraph.annotators.bandit.subprocess.run", return_value=_completed(payload)):
        result = BanditAnnotator().annotate(graph, repo)

    assert result.nodes_annotated == 1
    assert result.counts()["results_scanned"] == 2
    assert result.counts()["nodes_matched"] == 1
    assert result.counts()["suppressed_low_signal"] == 1
    assert graph.nodes["function"]["findings"][0]["test_id"] == "B602"


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


def test_detect_hidden_coupling_requires_no_static_dependency_path() -> None:
    graph = nx.DiGraph()
    graph.add_nodes_from(["coupled_left", "coupled_right", "static_left", "middle", "static_right"])
    graph.add_edge("coupled_left", "coupled_right", type="co_changes_with", co_change_count=8, co_change_rate=0.75)
    graph.add_edge("static_left", "static_right", type="co_changes_with", co_change_count=9, co_change_rate=0.9)
    graph.add_edge("static_left", "middle", type="calls")
    graph.add_edge("middle", "static_right", type="imports")

    findings = detect_hidden_coupling(graph)

    assert [finding.node_id for finding in findings] == ["coupled_left"]
    assert findings[0].kind == "hidden_coupling"
    assert findings[0].evidence["target"] == "coupled_right"


def test_detect_hidden_coupling_skips_obvious_code_to_test_pairs() -> None:
    graph = nx.DiGraph()
    graph.add_node("prod", file_path="starlette/routing.py")
    graph.add_node("test", file_path="tests/test_routing.py")
    graph.add_edge(
        "prod",
        "test",
        type="co_changes_with",
        co_change_count=10,
        co_change_rate=0.8,
    )

    assert detect_hidden_coupling(graph) == []


def test_detect_hidden_coupling_skips_type_only_modules() -> None:
    graph = nx.DiGraph()
    graph.add_node("runtime", file_path="starlette/routing.py")
    graph.add_node("types", file_path="starlette/types.py")
    graph.add_edge(
        "runtime",
        "types",
        type="co_changes_with",
        co_change_count=10,
        co_change_rate=0.8,
    )

    assert detect_hidden_coupling(graph) == []


def test_detect_hidden_coupling_aggregates_repeated_hubs() -> None:
    graph = nx.DiGraph()
    graph.add_nodes_from(["hub", "a", "b", "c"])
    graph.add_edge("hub", "a", type="co_changes_with", co_change_count=2, co_change_rate=0.4)
    graph.add_edge("hub", "b", type="co_changes_with", co_change_count=3, co_change_rate=0.6)
    graph.add_edge("c", "hub", type="co_changes_with", co_change_count=4, co_change_rate=0.8)

    findings = detect_hidden_coupling(graph)

    assert [finding.kind for finding in findings] == ["hidden_coupling_hub"]
    assert findings[0].node_id == "hub"
    assert findings[0].evidence["partner_count"] == 3
    assert findings[0].evidence["co_change_count"] == 9


def test_detect_vulnerable_usage_requires_vulnerable_import_and_matching_call() -> None:
    graph = nx.DiGraph()
    graph.add_node("uses_vuln", type=NodeType.FUNCTION.value)
    graph.add_node("imports_only", type=NodeType.FUNCTION.value)
    graph.add_node("dependency::requests", type="Dependency", name="requests")
    graph.add_node("requests_get", type=NodeType.FUNCTION.value, qualified_name="requests.api.get")
    graph.add_node("safe_call", type=NodeType.FUNCTION.value, qualified_name="json.loads")
    graph.add_node("uses_unresolved_vuln", type=NodeType.FUNCTION.value)
    graph.add_edge(
        "uses_vuln",
        "dependency::requests",
        type="imports_vulnerable",
        package="requests",
        vulnerability_ids=["CVE-2024-0001"],
    )
    graph.add_edge(
        "imports_only",
        "dependency::requests",
        type="imports_vulnerable",
        package="requests",
        vulnerability_ids=["CVE-2024-0001"],
    )
    graph.add_edge(
        "uses_unresolved_vuln",
        "dependency::requests",
        type="imports_vulnerable",
        package="requests",
        vulnerability_ids=["CVE-2024-0001"],
    )
    graph.add_edge("uses_vuln", "requests_get", type="calls", source="requests.get")
    graph.add_edge("imports_only", "safe_call", type="calls", source="json.loads")
    graph.graph["unresolved_calls"] = [{"source": "uses_unresolved_vuln", "name": "requests.post", "line_start": 12}]

    findings = detect_vulnerable_usage(graph)

    assert [finding.node_id for finding in findings] == ["uses_vuln", "uses_unresolved_vuln"]
    assert {finding.kind for finding in findings} == {"vulnerable_usage"}
    assert findings[0].evidence["package"] == "requests"
    assert findings[0].evidence["matched_calls"] == [{"call": "requests.get", "target": "requests_get"}]
    assert findings[1].evidence["matched_calls"] == [{"call": "requests.post"}]


def test_detect_outdated_documentation_combines_docstring_llm_finding_and_churn() -> None:
    graph = nx.DiGraph()
    graph.add_node(
        "stale_docs",
        type=NodeType.FUNCTION.value,
        churn=20,
        findings=[
            {
                "source": "llm",
                "code": "docstring_consistency",
                "severity": "MEDIUM",
                "confidence": "INFERRED",
                "message": "Docstring no longer matches return behavior.",
                "evidence": "return value",
            }
        ],
    )
    graph.add_node(
        "low_churn_docs",
        type=NodeType.FUNCTION.value,
        churn=1,
        findings=[{"source": "llm", "code": "docstring_consistency", "message": "Docstring mismatch."}],
    )

    findings = detect_outdated_documentation(graph, churn_pct=0.99)

    assert [finding.node_id for finding in findings] == ["stale_docs"]
    assert findings[0].kind == "outdated_documentation"
    assert findings[0].evidence["churn"] == 20.0


def test_detect_god_nodes_combines_top_centrality_complexity_and_degree() -> None:
    graph = nx.DiGraph()
    graph.add_node("god", type=NodeType.FUNCTION.value, centrality=1.0, complexity=30)
    graph.add_node("complex_only", type=NodeType.FUNCTION.value, centrality=0.1, complexity=29)
    graph.add_node("caller_1")
    graph.add_node("caller_2")
    graph.add_node("callee_1")
    graph.add_node("callee_2")
    graph.add_edge("caller_1", "god", type="calls")
    graph.add_edge("caller_2", "god", type="calls")
    graph.add_edge("god", "callee_1", type="calls")
    graph.add_edge("god", "callee_2", type="calls")
    graph.add_edge("complex_only", "callee_1", type="calls")

    findings = detect_god_nodes(graph, centrality_pct=0.99, complexity_pct=0.99, degree_pct=0.99)

    assert [finding.node_id for finding in findings] == ["god"]
    assert findings[0].kind == "god_node"
    assert findings[0].evidence["in_degree"] == 2
    assert findings[0].evidence["out_degree"] == 2


def test_detect_cyclic_dependencies_uses_calls_subgraph_only() -> None:
    graph = nx.DiGraph()
    graph.add_edge("a", "b", type="calls")
    graph.add_edge("b", "a", type="calls")
    graph.add_edge("x", "y", type="calls")
    graph.add_edge("y", "z", type="calls")
    graph.add_edge("z", "x", type="calls")
    graph.add_edge("c", "d", type="imports")
    graph.add_edge("d", "c", type="imports")

    findings = detect_cyclic_dependencies(graph)

    assert len(findings) == 1
    assert findings[0].kind == "cyclic_dependency"
    assert findings[0].evidence["cycle_size"] == 3
    assert findings[0].evidence["members"] == ["x", "y", "z"]


def test_detect_complex_hotspots_combines_cpu_complexity_and_coverage() -> None:
    graph = nx.DiGraph()
    graph.add_node("hot", type=NodeType.FUNCTION.value, cpu_pct=0.2, complexity=12, coverage_line=0.25)
    graph.add_node("covered", type=NodeType.FUNCTION.value, cpu_pct=0.2, complexity=12, coverage_line=0.9)
    graph.add_node("simple", type=NodeType.FUNCTION.value, cpu_pct=0.2, complexity=2, coverage_line=0.25)
    graph.add_node("cold", type=NodeType.FUNCTION.value, cpu_pct=0.01, complexity=12, coverage_line=0.25)

    findings = detect_complex_hotspots(graph, cpu_pct_threshold=0.05, complexity_threshold=10, coverage_threshold=0.5)

    assert [finding.node_id for finding in findings] == ["hot"]
    assert findings[0].kind == "complex_hotspot"
    assert findings[0].evidence["cpu_pct"] == 0.2
    assert findings[0].evidence["complexity"] == 12.0
    assert findings[0].evidence["coverage"] == 0.25


def test_detect_cross_signal_findings_runs_all_detectors() -> None:
    graph = nx.DiGraph()
    graph.add_node("hotspot", type=NodeType.FUNCTION.value, complexity=12, centrality=0.9, coverage_line=0.0)
    graph.add_node("other", type=NodeType.FUNCTION.value, complexity=1, centrality=0.1, coverage_line=1.0)

    findings = detect_cross_signal_findings(graph)

    assert any(finding.kind == "untested_hotspot" for finding in findings)


def test_cross_signal_annotator_attaches_reportable_findings() -> None:
    graph = nx.DiGraph()
    graph.add_node("hotspot", type=NodeType.FUNCTION.value, complexity=12, centrality=0.9, coverage_line=0.0)
    graph.add_node("other", type=NodeType.FUNCTION.value, complexity=1, centrality=0.1, coverage_line=1.0)

    result = CrossSignalAnnotator().annotate(graph, Path("."))

    assert result.nodes_annotated == 1
    finding = graph.nodes["hotspot"]["findings"][0]
    assert finding["source"] == "cross-signal"
    assert finding["code"] == "untested_hotspot"
    assert finding["severity"] == "HIGH"


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

    with patch("qualgraph.annotators.secrets._scan_secrets", return_value=payload):
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


def test_risk_score_uses_percentile_hotpath_weight() -> None:
    graph = nx.DiGraph()
    graph.add_node("cold", type=NodeType.FUNCTION.value, cpu_pct=0.0)
    graph.add_node("warm", type=NodeType.FUNCTION.value, cpu_pct=0.1)
    graph.add_node("hot", type=NodeType.FUNCTION.value, cpu_pct=0.5)

    score(graph, {"w1": 0, "w2": 0, "w3": 0, "w4": 0, "w5": 0, "w6": 0, "w7": 1})

    assert graph.nodes["cold"]["risk_components"]["hotpath"] == 0.0
    assert graph.nodes["warm"]["risk_components"]["hotpath"] > 0.0
    assert graph.nodes["hot"]["risk_components"]["hotpath"] == 1.0


def test_top_risk_nodes_excludes_test_files_by_default() -> None:
    graph = nx.DiGraph()
    graph.add_node("prod", type=NodeType.FUNCTION.value, file_path="pkg/runtime.py", risk_score=1.0)
    graph.add_node("test", type=NodeType.FUNCTION.value, file_path="tests/test_runtime.py", risk_score=99.0)

    assert [node_id for node_id, _attrs in top_risk_nodes(graph, limit=10)] == ["prod"]


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
                risk_score=2.0,
                risk_components={"coverage_gap": 0.75, "complexity": 0.5, "hotpath": 0.0},
            )
        ),
    )
    finding = {"source": "ruff", "code": "E501", "message": "line too long", "location": {"row": 6, "column": 1}}
    graph.nodes["function"]["findings"] = [finding, dict(finding)]
    graph.add_edge("module", "function", type="calls")
    annotate_metrics(graph)

    report = render_markdown_report(graph)

    assert "- Findings: 2 actionable production (2 total" in report
    assert "## Executive Summary" in report
    assert "## Per-Cluster Overview" in report
    assert "## Top-N Risk Nodes" in report
    assert "## Cross-Signal Findings" in report
    assert "## Per-Dimension Scorecards" in report
    assert "## Annotator Status" in report
    assert "## Top Finding Rules" in report
    assert "ruff E501: 1" in report
    assert "## Risk Hotspots" in report
    assert "score=" in report
    assert "why=finding-backed score + coverage gap + high complexity" in report
    assert "hotpath=0.00" not in report
    assert "betweenness=" in report


def test_report_backfills_missing_evidence_from_node_source() -> None:
    graph = nx.DiGraph()
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
                line_end=6,
                source="def work():\n    return risky()\n",
                complexity=1,
            )
        ),
    )
    graph.nodes["function"]["findings"] = [
        {"source": "ruff", "code": "B001", "message": "example", "location": {"row": 6, "column": 5}}
    ]

    report = render_markdown_report(graph)

    assert "Evidence: return risky()" in report


def test_report_does_not_truncate_llm_messages_or_suggested_actions() -> None:
    graph = nx.DiGraph()
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
                line_end=6,
                source="def work():\n    return risky()\n",
                complexity=1,
            )
        ),
    )
    message = (
        "This LLM finding is deliberately longer than the normal report shortening limit so the "
        "renderer must keep the final clause that explains the concrete failure mode."
    )
    action = (
        "This suggested action is also longer than the normal evidence limit and should retain the "
        "specific remediation steps at the end."
    )
    graph.nodes["function"]["findings"] = [
        {
            "source": "llm",
            "code": "reliability",
            "severity": "MEDIUM",
            "confidence": "INFERRED",
            "message": message,
            "evidence": "return risky()",
            "suggested_action": action,
        }
    ]

    report = render_markdown_report(graph)

    assert message in report
    assert action in report
    assert "concrete failure mode..." not in report


def test_report_top_rules_always_surfaces_llm_rules() -> None:
    graph = nx.DiGraph()
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
                line_end=6,
                source="def work():\n    return risky()\n",
                complexity=1,
            )
        ),
    )
    graph.nodes["function"]["findings"] = [
        {"source": "ruff", "code": f"RUF{index:03d}", "message": f"ruff issue {index}", "line": 6}
        for index in range(12)
    ]
    graph.nodes["function"]["findings"].append(
        {
            "source": "llm",
            "code": "security",
            "severity": "HIGH",
            "confidence": "INFERRED",
            "message": "The risky call can execute untrusted input.",
            "evidence": "return risky()",
        }
    )

    report = render_markdown_report(graph)

    assert "llm security: 1" in report


def test_report_derives_cross_signal_findings_when_not_attached() -> None:
    graph = nx.DiGraph()
    graph.add_node(
        "hotspot",
        type=NodeType.FUNCTION.value,
        qualified_name="sample.hotspot",
        file_path="sample.py",
        line_start=1,
        line_end=4,
        complexity=12,
        centrality=0.9,
        coverage_line=0.0,
    )
    graph.add_node(
        "other",
        type=NodeType.FUNCTION.value,
        qualified_name="sample.other",
        file_path="sample.py",
        line_start=6,
        line_end=7,
        complexity=1,
        centrality=0.1,
        coverage_line=1.0,
    )

    report = render_markdown_report(graph)

    assert "## Cross-Signal Findings" in report
    assert "sample.hotspot: untested_hotspot" in report


def test_report_dedupes_cluster_names_and_excludes_tests_from_risk_nodes() -> None:
    graph = nx.DiGraph()
    graph.graph["cluster_count"] = 2
    graph.add_node(
        "prod",
        type=NodeType.FUNCTION.value,
        qualified_name="sample.prod",
        file_path="sample.py",
        line_start=1,
        line_end=4,
        risk_score=1.0,
        cluster_id=1,
        cluster_name="Middleware",
    )
    graph.add_node(
        "test",
        type=NodeType.FUNCTION.value,
        qualified_name="tests.test_sample.helper",
        file_path="tests/test_sample.py",
        line_start=1,
        line_end=4,
        risk_score=99.0,
        cluster_id=2,
        cluster_name="Middleware",
    )

    report = render_markdown_report(graph, top_n=10)

    assert "Middleware (Prod)" in report
    assert "Middleware (Helper)" in report
    assert "### 1. sample.prod" in report
    assert "### 1. tests.test_sample.helper" not in report


def test_report_status_and_linkage_distinguish_static_edges_from_coverage() -> None:
    graph = nx.DiGraph()
    graph.graph["annotator_status"] = [
        {"name": "coverage", "status": "ok", "duration_ms": 12.5, "counts": {"nodes_annotated": 1, "error_count": 0}},
        {"name": "bandit", "status": "failed", "duration_ms": 1.0, "counts": {}},
    ]
    graph.add_node(
        "prod",
        type=NodeType.FUNCTION.value,
        qualified_name="sample.prod",
        file_path="sample.py",
        line_start=1,
        line_end=4,
        coverage_line=0.75,
    )
    graph.add_node(
        "test",
        type=NodeType.TEST_FUNCTION.value,
        qualified_name="tests.test_sample.test_prod",
        file_path="tests/test_sample.py",
        line_start=1,
        line_end=4,
    )
    graph.add_edge("prod", "test", type="tested_by", source="coverage_context")

    report = render_markdown_report(graph)

    assert "coverage: ok (12.5 ms); nodes_annotated=1, error_count=0" in report
    assert "bandit: failed (1.0 ms)" in report
    assert "Statically linked production functions/methods: 0/1" in report
    assert "Coverage-context linked production functions/methods: 1/1" in report
    assert "Covered production functions/methods: 1/1" in report


def test_report_explains_missing_coverage_contexts() -> None:
    graph = nx.DiGraph()
    graph.add_node(
        "prod",
        type=NodeType.FUNCTION.value,
        qualified_name="sample.prod",
        file_path="sample.py",
        line_start=1,
        line_end=4,
        coverage_line=0.75,
    )

    report = render_markdown_report(graph)

    assert "Coverage-context linked production functions/methods: 0/1" in report
    assert "No coverage contexts found; run coverage with dynamic_context=test_function" in report


def test_json_export_wraps_node_link_data_with_versioned_metadata() -> None:
    graph = nx.DiGraph()
    graph.graph["config"] = {"annotators": ["radon"]}
    graph.add_node("node", type=NodeType.FUNCTION.value)

    payload = export_json_data(graph, run_timestamp="2026-04-29T00:00:00+00:00")

    assert payload["schema_version"] == EXPORT_SCHEMA_VERSION
    assert payload["metadata"]["run_timestamp"] == "2026-04-29T00:00:00+00:00"
    assert payload["metadata"]["config_hash"]
    assert payload["metadata"]["annotator_versions"]["radon"] == "1.0"
    assert payload["graph"]["schema_version"]
    assert payload["graph"]["nodes"][0]["id"] == "node"


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


def _json(payload: dict) -> str:
    import json

    return json.dumps(payload)


class _completed:
    def __init__(self, payload: dict, returncode: int = 0, stderr: str = "") -> None:
        import json

        self.returncode = returncode
        self.stdout = json.dumps(payload)
        self.stderr = stderr
