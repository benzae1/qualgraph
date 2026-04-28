"""Docstring coverage annotator."""

from __future__ import annotations

from pathlib import Path

import networkx as nx
from docstring_parser import parse

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.graph.schema import NodeType


class DocstringAnnotator(BaseAnnotator):
    name = "docstring"
    version = "1.0"

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        nodes_annotated = 0
        errors: list[str] = []

        for _node_id, attrs in graph.nodes(data=True):
            if attrs.get("type") not in (
                NodeType.CLASS.value,
                NodeType.FUNCTION.value,
                NodeType.METHOD.value,
                NodeType.TEST_FUNCTION.value,
            ):
                continue

            docstring = attrs.get("docstring")
            attrs["has_docstring"] = bool(docstring)
            attrs["has_params_documented"] = False
            attrs["has_returns_documented"] = False
            attrs["docstring_param_count"] = 0

            if not docstring:
                nodes_annotated += 1
                continue

            try:
                parsed = parse(_strip_docstring_quotes(docstring))
            except Exception as exc:
                errors.append(f"{attrs.get('id', '<unknown>')}: {exc}")
                nodes_annotated += 1
                continue

            attrs["has_params_documented"] = bool(parsed.params)
            attrs["has_returns_documented"] = parsed.returns is not None
            attrs["docstring_param_count"] = len(parsed.params)
            nodes_annotated += 1

        return AnnotatorResult(
            name=self.name,
            nodes_annotated=nodes_annotated,
            errors=errors,
        )


def _strip_docstring_quotes(docstring: str) -> str:
    stripped = docstring.strip()
    for quote in ('"""', "'''", '"', "'"):
        if stripped.startswith(quote) and stripped.endswith(quote):
            return stripped[len(quote) : -len(quote)].strip()
    return stripped
