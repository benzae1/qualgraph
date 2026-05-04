import networkx as nx

from qualgraph.viewer.model import ViewerData


def test_viewer_summary_clusters_and_findings_are_derived_from_graph() -> None:
    viewer = ViewerData(_viewer_graph(), top_n=5)

    summary = viewer.summary()
    clusters = viewer.clusters()
    findings = viewer.findings(source="llm")
    payload = viewer.graph_payload()

    assert summary["nodes"] == 3
    assert summary["edges"] == 2
    assert summary["llm_findings"] == 1
    assert summary["warnings"]
    assert [item["source"] for item in findings] == ["llm"]
    assert {cluster["id"] for cluster in clusters} == {"1", "2"}
    assert payload["mode"] == "clusters"
    assert len(payload["nodes"]) == 2
    assert payload["edges"][0]["weight"] == 1


def test_viewer_graph_payload_omits_source_until_node_detail() -> None:
    viewer = ViewerData(_viewer_graph())

    cluster_payload = viewer.graph_payload(cluster_id="1")
    detail = viewer.node_detail("pkg/mod.py::pkg.mod.risky::10")

    assert "source" not in cluster_payload["nodes"][0]
    assert detail is not None
    assert detail["source"] == "def risky():\n    return eval(user_input)\n"
    assert detail["findings"][0]["source"] == "llm"
    assert detail["relationships"]["outgoing"][0]["edge_type"] == "calls"


def test_viewer_returns_none_for_missing_node() -> None:
    assert ViewerData(_viewer_graph()).node_detail("missing") is None


def test_viewer_overview_payload_limits_cluster_hairball() -> None:
    graph = nx.DiGraph()
    for index in range(60):
        graph.add_node(
            f"pkg/mod_{index}.py::pkg.mod_{index}.node::1",
            type="Function",
            name=f"node_{index}",
            qualified_name=f"pkg.mod_{index}.node",
            file_path=f"pkg/mod_{index}.py",
            line_start=1,
            line_end=2,
            cluster_id=index,
            risk_score=float(index),
        )
        if index:
            graph.add_edge(
                f"pkg/mod_{index - 1}.py::pkg.mod_{index - 1}.node::1",
                f"pkg/mod_{index}.py::pkg.mod_{index}.node::1",
                type="calls",
            )

    payload = ViewerData(graph).graph_payload()

    assert payload["mode"] == "clusters"
    assert payload["total_clusters"] == 60
    assert payload["hidden_clusters"] == 18
    assert len(payload["nodes"]) == 42
    assert len(payload["edges"]) < 60


def _viewer_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_node(
        "pkg/mod.py::pkg.mod.risky::10",
        type="Function",
        name="risky",
        qualified_name="pkg.mod.risky",
        file_path="pkg/mod.py",
        line_start=10,
        line_end=12,
        source="def risky():\n    return eval(user_input)\n",
        cluster_id=1,
        risk_score=4.5,
        complexity=5,
        churn=3,
        findings=[
            {
                "source": "llm",
                "code": "security",
                "dimension": "security",
                "severity": "HIGH",
                "confidence": "EXTRACTED",
                "message": "Untrusted input reaches eval.",
                "evidence": "return eval(user_input)",
                "suggested_action": "Avoid eval for untrusted input.",
            }
        ],
    )
    graph.add_node(
        "pkg/helper.py::pkg.helper.clean::1",
        type="Function",
        name="clean",
        qualified_name="pkg.helper.clean",
        file_path="pkg/helper.py",
        line_start=1,
        line_end=2,
        cluster_id=1,
        risk_score=0.5,
    )
    graph.add_node(
        "tests/test_mod.py::tests.test_mod.test_risky::5",
        type="TestFunction",
        name="test_risky",
        qualified_name="tests.test_mod.test_risky",
        file_path="tests/test_mod.py",
        line_start=5,
        line_end=8,
        cluster_id=2,
        risk_score=0.0,
    )
    graph.add_edge("pkg/mod.py::pkg.mod.risky::10", "pkg/helper.py::pkg.helper.clean::1", type="calls")
    graph.add_edge("pkg/mod.py::pkg.mod.risky::10", "tests/test_mod.py::tests.test_mod.test_risky::5", type="tested_by", linkage_source="static")
    return graph
