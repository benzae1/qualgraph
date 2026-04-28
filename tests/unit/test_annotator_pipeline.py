from pathlib import Path

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.pipeline import run_pipeline


class GoodAnnotator(BaseAnnotator):
    name = "good"
    version = "1.0"

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        graph.nodes["node"]["annotated"] = True
        return AnnotatorResult(name=self.name, nodes_annotated=1)


class UnavailableAnnotator(GoodAnnotator):
    name = "unavailable"

    def is_available(self) -> bool:
        return False


class FailingAnnotator(GoodAnnotator):
    name = "failing"

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        raise RuntimeError("boom")


def test_run_pipeline_times_successes_and_isolates_failures() -> None:
    graph = nx.DiGraph()
    graph.add_node("node")

    results = run_pipeline(
        graph,
        Path("."),
        [GoodAnnotator(), UnavailableAnnotator(), FailingAnnotator()],
    )

    assert graph.nodes["node"]["annotated"] is True
    assert [(result.name, result.nodes_annotated, bool(result.errors)) for result in results] == [
        ("good", 1, False),
        ("failing", 0, True),
    ]
    assert results[0].duration_seconds >= 0
    assert results[1].duration_seconds >= 0
