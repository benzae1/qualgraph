import json

import networkx as nx

from qualgraph.graph.schema import NodeAttrs, NodeType, node_attrs_to_graph
from qualgraph.llm.tasks import export_tasks, import_results
from qualgraph.report.markdown import render_markdown_report


def test_export_and_import_agent_llm_tasks(tmp_path) -> None:
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
                line_end=8,
                source="def work():\n    return risky()\n",
                complexity=8,
                centrality=0.75,
                coverage_line=0.0,
            )
        ),
    )
    task_dir = tmp_path / "run-1" / "llm_tasks"

    manifest = export_tasks(graph, task_dir, limit=1)

    assert len(manifest["tasks"]) == 1
    task_file = task_dir / "0001.sample.work.md"
    assert task_file.exists()
    assert "Write JSON output to:" in task_file.read_text(encoding="utf-8")

    output_path = tmp_path / "run-1" / "llm_results" / "0001.json"
    output_path.write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "kind": "unhandled_error_path",
                        "severity": "HIGH",
                        "confidence": "INFERRED",
                        "message": "The risky call has no visible error handling.",
                        "evidence": {"line": 6},
                        "suggested_action": "Add explicit handling or document why propagation is safe.",
                        "line": 6,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    summary = import_results(graph, tmp_path / "run-1")

    assert summary["findings_added"] == 1
    assert graph.nodes["function"]["llm_severity_max"] == 1.0
    assert graph.nodes["function"]["risk_components"]["llm"] == 1.0
    report = render_markdown_report(graph)
    assert "llm unhandled_error_path" in report
    assert "The risky call has no visible error handling." in report
