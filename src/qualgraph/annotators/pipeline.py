"""Sequential annotator pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from qualgraph.annotators.base import BaseAnnotator
from qualgraph.logging import RunLogger


@dataclass(slots=True)
class AnnotatorPipeline:
    annotators: list[BaseAnnotator] = field(default_factory=list)
    continue_on_error: bool = True

    def __init__(
        self,
        annotators: Iterable[BaseAnnotator] = (),
        continue_on_error: bool = True,
    ) -> None:
        self.annotators = list(annotators)
        self.continue_on_error = continue_on_error

    def run(
        self,
        graph: Any,
        repo_path: str | Path,
        run_logger: RunLogger | None = None,
    ) -> Any:
        if run_logger is not None:
            run_logger.log_event(
                "annotator_pipeline_started",
                annotator_count=len(self.annotators),
                annotators=[annotator.name for annotator in self.annotators],
            )

        for annotator in self.annotators:
            try:
                annotator.run(graph, repo_path, run_logger=run_logger)
            except Exception:
                if not self.continue_on_error:
                    raise

        if run_logger is not None:
            run_logger.log_event("annotator_pipeline_finished", annotator_count=len(self.annotators))
        return graph
