"""Sequential annotator pipeline."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Protocol

import networkx as nx
from rich.progress import Progress

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.logging import RunLogger


class PipelineLogger(Protocol):
    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...


@dataclass(slots=True)
class AnnotatorPipeline:
    annotators: list[BaseAnnotator] = field(default_factory=list)

    def __init__(
        self,
        annotators: Iterable[BaseAnnotator] = (),
    ) -> None:
        self.annotators = list(annotators)

    def run(
        self,
        graph: nx.DiGraph,
        repo_path: str | Path,
        logger: PipelineLogger | RunLogger | None = None,
    ) -> list[AnnotatorResult]:
        return run_pipeline(graph, Path(repo_path), self.annotators, logger)


def run_pipeline(
    graph: nx.DiGraph,
    repo_path: str | Path,
    annotators: Iterable[BaseAnnotator],
    logger: PipelineLogger | RunLogger | None = None,
    show_progress: bool = False,
) -> list[AnnotatorResult]:
    """Run annotators sequentially without letting one failure stop the rest."""

    annotator_list = list(annotators)
    stdlib_logger = _stdlib_logger(logger)
    run_logger = logger if isinstance(logger, RunLogger) else None
    repo = Path(repo_path)
    results: list[AnnotatorResult] = []

    if run_logger is not None:
        run_logger.log_event(
            "annotator_pipeline_started",
            annotator_count=len(annotator_list),
            annotators=[annotator.name for annotator in annotator_list],
        )

    progress = Progress(transient=True) if show_progress and annotator_list else None
    if progress is None:
        for annotator in annotator_list:
            results.extend(_run_one_annotator(graph, repo, annotator, stdlib_logger, run_logger))
    else:
        with progress:
            task = progress.add_task("annotators", total=len(annotator_list))
            for annotator in annotator_list:
                progress.update(task, description=f"annotator: {annotator.name}")
                results.extend(_run_one_annotator(graph, repo, annotator, stdlib_logger, run_logger))
                progress.advance(task)

    if run_logger is not None:
        run_logger.log_event(
            "annotator_pipeline_finished",
            annotator_count=len(annotator_list),
            result_count=len(results),
        )
    return results


def _run_one_annotator(
    graph: nx.DiGraph,
    repo: Path,
    annotator: BaseAnnotator,
    stdlib_logger: PipelineLogger,
    run_logger: RunLogger | None,
) -> list[AnnotatorResult]:
    if not annotator.is_available():
        stdlib_logger.warning("%s unavailable, skipping", annotator.name)
        if run_logger is not None:
            run_logger.log_annotator(
                name=annotator.name,
                version=annotator.version,
                duration_ms=0.0,
                counts={},
                status="skipped",
            )
        return []

    started = time.perf_counter()
    try:
        result = annotator.annotate(graph, repo)
        if not isinstance(result, AnnotatorResult):
            raise TypeError(f"{annotator.name}.annotate returned {type(result).__name__}")
        result.duration_seconds = time.perf_counter() - started
        stdlib_logger.info(
            "%s annotated %s nodes in %.1fs",
            annotator.name,
            result.nodes_annotated,
            result.duration_seconds,
        )
        if run_logger is not None:
            run_logger.log_annotator(
                name=annotator.name,
                version=annotator.version,
                duration_ms=result.duration_seconds * 1000,
                counts=result.counts(),
                status="ok" if not result.errors else "ok_with_errors",
            )
        return [result]
    except Exception as exc:
        duration_seconds = time.perf_counter() - started
        stdlib_logger.exception("%s failed: %s", annotator.name, exc)
        result = AnnotatorResult(
            name=annotator.name,
            duration_seconds=duration_seconds,
            errors=[str(exc)],
        )
        if run_logger is not None:
            run_logger.log_annotator(
                name=annotator.name,
                version=annotator.version,
                duration_ms=result.duration_seconds * 1000,
                counts=result.counts(),
                status="failed",
                error=exc,
            )
        return [result]


def _stdlib_logger(logger: PipelineLogger | RunLogger | None) -> PipelineLogger:
    if logger is not None and all(hasattr(logger, name) for name in ("info", "warning", "exception")):
        return logger
    return logging.getLogger("qualgraph.annotators")
