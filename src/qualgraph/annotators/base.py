"""Base interface for graph annotators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any, Mapping

from qualgraph.logging import RunLogger, graph_counts


@dataclass(slots=True)
class AnnotatorResult:
    nodes_touched: int = 0
    edges_touched: int = 0
    findings_added: int = 0
    extra: dict[str, Any] = field(default_factory=dict)

    def counts(self) -> dict[str, Any]:
        return {
            "nodes_touched": self.nodes_touched,
            "edges_touched": self.edges_touched,
            "findings_added": self.findings_added,
            **self.extra,
        }


class BaseAnnotator(ABC):
    name = "base"
    version = "0.1.0"

    @abstractmethod
    def annotate(self, graph: Any, repo_path: Path) -> AnnotatorResult | Mapping[str, Any] | None:
        """Mutate ``graph`` with this annotator's signal."""

    def run(
        self,
        graph: Any,
        repo_path: str | Path,
        run_logger: RunLogger | None = None,
    ) -> AnnotatorResult | Mapping[str, Any] | None:
        started = perf_counter()
        before = graph_counts(graph)
        try:
            result = self.annotate(graph, Path(repo_path))
        except Exception as exc:
            if run_logger is not None:
                run_logger.log_annotator(
                    name=self.name,
                    version=self.version,
                    duration_ms=_elapsed_ms(started),
                    counts={**_count_delta(before, graph_counts(graph)), "before": before, "after": graph_counts(graph)},
                    status="failed",
                    error=exc,
                )
            raise

        after = graph_counts(graph)
        result_counts = _result_counts(result)
        counts = {**_count_delta(before, after), **result_counts, "before": before, "after": after}
        if run_logger is not None:
            run_logger.log_annotator(
                name=self.name,
                version=self.version,
                duration_ms=_elapsed_ms(started),
                counts=counts,
            )
        return result


def _result_counts(result: AnnotatorResult | Mapping[str, Any] | None) -> dict[str, Any]:
    if isinstance(result, AnnotatorResult):
        return result.counts()
    if isinstance(result, Mapping):
        return dict(result)
    return {}


def _count_delta(before: Mapping[str, int], after: Mapping[str, int]) -> dict[str, int]:
    return {
        "nodes_added": after.get("nodes", 0) - before.get("nodes", 0),
        "edges_added": after.get("edges", 0) - before.get("edges", 0),
    }


def _elapsed_ms(started: float) -> float:
    return round((perf_counter() - started) * 1000, 3)
