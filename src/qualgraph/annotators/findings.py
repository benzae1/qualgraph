"""Helpers for attaching tool findings to graph nodes."""

from __future__ import annotations

import json
from typing import Any

import networkx as nx


def clear_findings_by_source(graph: nx.DiGraph, source: str) -> None:
    """Remove stale findings from a previous run of the same annotator."""

    for _node_id, attrs in graph.nodes(data=True):
        findings = attrs.get("findings") or []
        attrs["findings"] = [
            finding
            for finding in findings
            if not isinstance(finding, dict) or finding.get("source") != source
        ]


def add_finding(attrs: dict[str, Any], finding: dict[str, Any]) -> bool:
    """Attach ``finding`` if the same tool/code/location is not already present."""

    findings = attrs.setdefault("findings", [])
    key = finding_key(finding)
    for existing in findings:
        if isinstance(existing, dict) and finding_key(existing) == key:
            return False
    findings.append(finding)
    return True


def finding_key(finding: dict[str, Any]) -> tuple[Any, ...]:
    location = finding.get("location") or {}
    if isinstance(location, dict):
        location_key = (location.get("row"), location.get("column"))
    else:
        location_key = _stable_json(location)
    return (
        finding.get("source"),
        finding.get("code") or finding.get("test_id"),
        finding.get("line"),
        location_key,
        finding.get("message"),
    )


def _stable_json(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True)
    except TypeError:
        return str(value)
