"""Derived cross-signal findings annotator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.annotators.findings import add_finding, clear_findings_by_source
from qualgraph.findings.cross_signal import detect_cross_signal_findings
from qualgraph.findings.model import Finding


class CrossSignalAnnotator(BaseAnnotator):
    name = "cross-signal"
    version = "1.0"

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        clear_findings_by_source(graph, self.name)
        nodes_touched: set[str] = set()
        for finding in detect_cross_signal_findings(graph):
            if finding.node_id not in graph.nodes:
                continue
            if add_finding(graph.nodes[finding.node_id], _finding_payload(finding)):
                nodes_touched.add(finding.node_id)
        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _finding_payload(finding: Finding) -> dict[str, Any]:
    return {
        "source": CrossSignalAnnotator.name,
        "code": finding.kind,
        "severity": finding.severity.upper(),
        "confidence": finding.confidence or "INFERRED",
        "message": finding.message or finding.kind.replace("_", " "),
        "evidence": finding.evidence,
    }
