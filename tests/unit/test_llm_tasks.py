import json

import networkx as nx

from qualgraph.graph.schema import NodeAttrs, NodeType, node_attrs_to_graph
from qualgraph.llm.context import build_context, render_analysis_prompt
from qualgraph.llm.parser import parse_analysis_response
from qualgraph.llm.tasks import export_tasks, import_results
from qualgraph.report.markdown import render_markdown_report


def test_build_context_sorts_callers_and_limits_callees() -> None:
    graph = nx.DiGraph()
    graph.add_node("target", **_node("target", "sample.target", source="def target():\n    return 1\n"))
    graph.add_node("caller_low", **_node("caller_low", "sample.low", source="def low():\n    target()\n", centrality=0.1))
    graph.add_node("caller_high", **_node("caller_high", "sample.high", source="def high():\n    target()\n", centrality=0.9))
    for index in range(6):
        graph.add_node(f"callee_{index}", **_node(f"callee_{index}", f"sample.callee_{index}"))
        graph.add_edge("target", f"callee_{index}", type="calls")
    graph.add_edge("caller_low", "target", type="calls")
    graph.add_edge("caller_high", "target", type="calls")

    context = build_context(graph, "target", max_callers=2, max_callees=5)

    assert [caller["qualified_name"] for caller in context["callers"]] == ["sample.high", "sample.low"]
    assert len(context["callees"]) == 5
    prompt = render_analysis_prompt(context)
    assert "Function: sample.target" in prompt
    assert "Return ONLY a JSON object" in prompt


def test_parse_analysis_response_discards_findings_without_source_evidence() -> None:
    payload = {
        "findings": [
            {
                "dimension": "reliability",
                "severity": "high",
                "confidence": "INFERRED",
                "title": "Unhandled risky call",
                "description": "The risky call is not guarded.",
                "evidence": "return risky()",
                "suggested_action": "Handle or document the propagation.",
            },
            {
                "dimension": "security",
                "severity": "critical",
                "confidence": "INFERRED",
                "title": "Invented issue",
                "description": "This evidence is not present.",
                "evidence": "eval(user_input)",
                "suggested_action": "Remove it.",
            },
        ]
    }

    parsed = parse_analysis_response(json.dumps(payload), "def work():\n    return risky()\n")

    assert len(parsed["findings"]) == 1
    assert parsed["findings"][0]["title"] == "Unhandled risky call"
    assert parsed["proposed_count"] == 2
    assert parsed["rejected_count"] == 1


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
                        "dimension": "reliability",
                        "severity": "high",
                        "confidence": "INFERRED",
                        "title": "Unhandled risky call",
                        "description": "The risky call has no visible error handling.",
                        "evidence": "return risky()",
                        "suggested_action": "Add explicit handling or document why propagation is safe.",
                    }
                ]
            }
        ),
        encoding="utf-8-sig",
    )

    summary = import_results(graph, tmp_path / "run-1")

    assert summary["findings_added"] == 1
    assert summary["proposed"] == 1
    assert summary["accepted"] == 1
    assert summary["rejected"] == 0
    assert graph.graph["llm_validation"] == {
        "tasks": 1,
        "imported": 1,
        "proposed": 1,
        "accepted": 1,
        "rejected": 0,
    }
    assert graph.nodes["function"]["llm_severity_max"] == 0.85
    assert graph.nodes["function"]["risk_components"]["llm"] == 0.85
    report = render_markdown_report(graph)
    assert "LLM findings proposed/accepted/rejected: 1/1/0" in report
    assert "llm reliability" in report
    assert "The risky call has no visible error handling." in report


def _node(
    node_id: str,
    qualified_name: str,
    source: str = "def f():\n    pass\n",
    centrality: float = 0.0,
) -> dict:
    return node_attrs_to_graph(
        NodeAttrs(
            id=node_id,
            type=NodeType.FUNCTION,
            name=qualified_name.rsplit(".", 1)[-1],
            qualified_name=qualified_name,
            file_path="sample.py",
            line_start=1,
            line_end=3,
            source=source,
            centrality=centrality,
        )
    )
