"""Typed findings produced by derived and LLM analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Finding:
    node_id: str
    kind: str
    severity: str
    evidence: dict[str, Any] = field(default_factory=dict)
    message: str | None = None
    confidence: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}
