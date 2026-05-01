"""Base interface for graph annotators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import networkx as nx


@dataclass(slots=True)
class AnnotatorResult:
    name: str
    nodes_annotated: int = 0
    edges_added: int = 0
    duration_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)
    extra_counts: dict[str, Any] = field(default_factory=dict)

    def counts(self) -> dict[str, Any]:
        return {
            "nodes_annotated": self.nodes_annotated,
            "edges_added": self.edges_added,
            "error_count": len(self.errors or []),
            **self.extra_counts,
        }


class BaseAnnotator(ABC):
    name: str = "base"
    version: str = "0.1.0"

    @abstractmethod
    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        """Mutate ``graph`` with this annotator's signal."""

    def is_available(self) -> bool:
        """Check that the underlying tool is installed and runnable."""

        return True
