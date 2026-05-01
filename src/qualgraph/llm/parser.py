"""Parse and validate LLM analysis responses."""

from __future__ import annotations

import json
from typing import Any


VALID_DIMENSIONS = {"maintainability", "reliability", "security", "performance"}
VALID_SEVERITIES = {"low", "medium", "high", "critical"}
VALID_CONFIDENCE = {"EXTRACTED", "INFERRED", "AMBIGUOUS"}


def parse_analysis_response(response_text: str, evidence_corpus: str) -> dict[str, Any]:
    payload = json.loads(response_text)
    findings = []
    proposed = 0
    rejected = 0
    for finding in payload.get("findings", []) or []:
        if not isinstance(finding, dict):
            continue
        proposed += 1
        normalized = _normalize_finding(finding)
        evidence = normalized.get("evidence") or ""
        if not evidence or evidence not in evidence_corpus:
            rejected += 1
            continue
        findings.append(normalized)
    return {"findings": findings, "proposed_count": proposed, "rejected_count": rejected}


def _normalize_finding(finding: dict[str, Any]) -> dict[str, Any]:
    dimension = str(finding.get("dimension") or "").lower()
    severity = str(finding.get("severity") or "").lower()
    confidence = str(finding.get("confidence") or "")
    return {
        "dimension": dimension if dimension in VALID_DIMENSIONS else "maintainability",
        "severity": severity if severity in VALID_SEVERITIES else "low",
        "confidence": confidence if confidence in VALID_CONFIDENCE else "AMBIGUOUS",
        "title": str(finding.get("title") or "Untitled finding"),
        "description": str(finding.get("description") or ""),
        "evidence": str(finding.get("evidence") or ""),
        "suggested_action": str(finding.get("suggested_action") or ""),
    }
