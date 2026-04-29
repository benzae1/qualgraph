"""Structured run logging for qualgraph.

Every CLI run should create a JSONL event stream plus a compact summary. The
API here is deliberately independent from the CLI so the same logger can later
be used by a service worker or test harness.
"""

from __future__ import annotations

import json
import logging as stdlib_logging
import traceback
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Iterator, Mapping, Optional
from uuid import uuid4


LOGGER_NAME = "qualgraph"
DEFAULT_RUNS_DIR = ".qualgraph/runs"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def configure_console_logging(level: int = stdlib_logging.INFO) -> None:
    stdlib_logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


@dataclass(slots=True)
class LLMUsage:
    calls: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0

    @property
    def prompt_tokens(self) -> int:
        return self.input_tokens

    @property
    def completion_tokens(self) -> int:
        return self.output_tokens


@dataclass(slots=True)
class RunSummary:
    run_id: str
    started_at: str
    finished_at: Optional[str] = None
    duration_ms: Optional[float] = None
    repo_path: Optional[str] = None
    annotators: list[dict[str, Any]] = field(default_factory=list)
    llm: LLMUsage = field(default_factory=LLMUsage)
    errors: list[dict[str, Any]] = field(default_factory=list)


class RunLogger:
    """Write structured JSONL events and aggregate per-run counters."""

    def __init__(
        self,
        repo_path: str | Path | None = None,
        artifacts_dir: str | Path | None = None,
        run_id: str | None = None,
    ) -> None:
        self.repo_path = Path(repo_path).resolve() if repo_path is not None else None
        self.run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
        base_dir = Path(artifacts_dir or DEFAULT_RUNS_DIR)
        self.run_dir = base_dir / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.events_path = self.run_dir / "run.jsonl"
        self.llm_calls_path = self.run_dir / "llm_calls.jsonl"
        self.summary_path = self.run_dir / "run_summary.json"
        self._started = perf_counter()
        self.summary = RunSummary(
            run_id=self.run_id,
            started_at=utc_now_iso(),
            repo_path=str(self.repo_path) if self.repo_path is not None else None,
        )
        self.log_event("run_started", repo_path=self.summary.repo_path)

    def log_event(self, event: str, **fields: Any) -> None:
        record = {
            "ts": utc_now_iso(),
            "run_id": self.run_id,
            "event": event,
            **_json_safe(fields),
        }
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    @contextmanager
    def span(self, event: str, **fields: Any) -> Iterator[dict[str, Any]]:
        started = perf_counter()
        payload: dict[str, Any] = {}
        self.log_event(f"{event}_started", **fields)
        try:
            yield payload
        except Exception as exc:
            duration_ms = _elapsed_ms(started)
            error = _error_record(exc)
            self.summary.errors.append({"event": event, **error})
            self.log_event(f"{event}_failed", duration_ms=duration_ms, **fields, **payload, **error)
            raise
        else:
            self.log_event(
                f"{event}_finished",
                duration_ms=_elapsed_ms(started),
                **fields,
                **payload,
            )

    def log_annotator(
        self,
        name: str,
        version: str,
        duration_ms: float,
        counts: Mapping[str, Any] | None = None,
        status: str = "ok",
        error: BaseException | None = None,
    ) -> None:
        record = {
            "name": name,
            "version": version,
            "duration_ms": duration_ms,
            "status": status,
            "counts": dict(counts or {}),
        }
        if error is not None:
            error_data = _error_record(error)
            record["error"] = error_data
            self.summary.errors.append({"event": "annotator", "annotator": name, **error_data})
        self.summary.annotators.append(record)
        self.log_event("annotator_finished", **record)

    def log_llm_call(
        self,
        model: str,
        duration_ms: float,
        input_tokens: int = 0,
        cached_input_tokens: int = 0,
        output_tokens: int = 0,
        cost_usd: float = 0.0,
        status: str = "ok",
        node_id: str | None = None,
        prompt_template: str | None = None,
        error: BaseException | None = None,
    ) -> None:
        computed_total = input_tokens + output_tokens
        if status == "ok":
            self.summary.llm.calls += 1
            self.summary.llm.input_tokens += input_tokens
            self.summary.llm.cached_input_tokens += cached_input_tokens
            self.summary.llm.output_tokens += output_tokens
            self.summary.llm.total_tokens += computed_total
            self.summary.llm.cost_usd += cost_usd

        record: dict[str, Any] = {
            "node_id": node_id,
            "prompt_template": prompt_template,
            "model": model,
            "input_tokens": input_tokens,
            "cached_tokens": cached_input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost_usd,
            "latency_ms": duration_ms,
            "status": status,
        }
        if error is not None:
            error_data = _error_record(error)
            record["error"] = error_data
            self.summary.errors.append({"event": "llm_call", **error_data})
        with self.llm_calls_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(_json_safe(record), sort_keys=True) + "\n")
        self.log_event("llm_call_finished", **record)

    def finish(self) -> RunSummary:
        self.summary.finished_at = utc_now_iso()
        self.summary.duration_ms = _elapsed_ms(self._started)
        self.log_event(
            "run_finished",
            duration_ms=self.summary.duration_ms,
            annotator_count=len(self.summary.annotators),
            llm_calls=self.summary.llm.calls,
            llm_cost_usd=self.summary.llm.cost_usd,
            error_count=len(self.summary.errors),
        )
        self.summary_path.write_text(
            json.dumps(_json_safe(asdict(self.summary)), indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return self.summary


def graph_counts(graph: Any) -> dict[str, int]:
    nodes = graph.number_of_nodes() if hasattr(graph, "number_of_nodes") else 0
    edges = graph.number_of_edges() if hasattr(graph, "number_of_edges") else 0
    return {"nodes": int(nodes), "edges": int(edges)}


def _elapsed_ms(started: float) -> float:
    return round((perf_counter() - started) * 1000, 3)


def _error_record(error: BaseException) -> dict[str, Any]:
    return {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": "".join(traceback.format_exception(type(error), error, error.__traceback__)),
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    try:
        json.dumps(value)
    except TypeError:
        return str(value)
    return value
