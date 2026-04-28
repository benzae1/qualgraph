"""Radon maintainability annotator."""

from __future__ import annotations

from pathlib import Path

import networkx as nx
from radon.complexity import cc_visit
from radon.metrics import mi_visit

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.graph.schema import NodeType


class RadonAnnotator(BaseAnnotator):
    name = "radon"
    version = "1.0"

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        nodes_annotated = 0
        errors: list[str] = []

        for _node_id, attrs in graph.nodes(data=True):
            if attrs.get("type") not in (NodeType.FUNCTION.value, NodeType.METHOD.value):
                continue
            source = attrs.get("source")
            if not source:
                continue
            try:
                cc_results = cc_visit(source)
                if cc_results:
                    attrs["complexity"] = cc_results[0].complexity
                attrs["maintainability_index"] = mi_visit(source, multi=False)
                nodes_annotated += 1
            except SyntaxError as exc:
                errors.append(f"{attrs.get('id', '<unknown>')}: {exc}")

        return AnnotatorResult(
            name=self.name,
            nodes_annotated=nodes_annotated,
            errors=errors,
        )
