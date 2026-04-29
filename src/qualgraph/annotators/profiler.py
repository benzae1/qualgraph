"""cProfile JSON annotator."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator
from qualgraph.graph.schema import NodeType


@dataclass(frozen=True, slots=True)
class ProfileRecord:
    file_path: str
    line: int
    call_count: int
    cum_time: float


class ProfilerAnnotator(BaseAnnotator):
    name = "profiler"
    version = "1.0"

    def __init__(self, profile_path: str | Path | None = None) -> None:
        self.profile_path = Path(profile_path) if profile_path is not None else None

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        if self.profile_path is None:
            return AnnotatorResult(name=self.name, errors=["profile JSON path not provided"])
        path = self.profile_path
        if not path.is_absolute():
            path = Path(repo_path) / path
        if not path.exists():
            return AnnotatorResult(name=self.name, errors=[f"profile JSON not found: {path}"])

        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        records = _profile_records(payload)
        total = _total_time(payload, records)
        index = _node_location_index(graph, repo_path)
        nodes_touched: set[str] = set()

        for record in records:
            node_id = index.get((_normalize_path(record.file_path), record.line))
            if node_id is None:
                continue
            attrs = graph.nodes[node_id]
            attrs["profile_cum_time"] = record.cum_time
            attrs["profile_call_count"] = record.call_count
            attrs["cpu_pct"] = record.cum_time / total if total > 0 else 0.0
            attrs["hotpath_weight"] = attrs["cpu_pct"]
            nodes_touched.add(node_id)

        graph.graph["profile_total_time"] = total
        graph.graph["profile_records"] = len(records)
        return AnnotatorResult(name=self.name, nodes_annotated=len(nodes_touched))


def _profile_records(payload: dict[str, Any]) -> list[ProfileRecord]:
    raw = payload.get("functions") or payload.get("stats") or payload.get("records") or []
    if isinstance(raw, dict):
        return [_record_from_mapping(key, value) for key, value in raw.items() if isinstance(value, dict)]
    if isinstance(raw, list):
        return [_record_from_item(item) for item in raw if isinstance(item, dict)]
    return []


def _record_from_mapping(key: str, value: dict[str, Any]) -> ProfileRecord:
    file_path = value.get("filename") or value.get("file") or value.get("file_path")
    line = value.get("line") or value.get("line_number") or value.get("lineno")
    if file_path is None or line is None:
        parsed = _parse_function_key(key)
        file_path = file_path or parsed.get("file_path")
        line = line or parsed.get("line")
    return ProfileRecord(
        file_path=str(file_path or ""),
        line=int(line or 0),
        call_count=_call_count(value),
        cum_time=_cum_time(value),
    )


def _record_from_item(item: dict[str, Any]) -> ProfileRecord:
    key = str(item.get("key") or item.get("function") or "")
    parsed = _parse_function_key(key)
    return ProfileRecord(
        file_path=str(item.get("filename") or item.get("file") or item.get("file_path") or parsed.get("file_path") or ""),
        line=int(item.get("line") or item.get("line_number") or item.get("lineno") or parsed.get("line") or 0),
        call_count=_call_count(item),
        cum_time=_cum_time(item),
    )


def _parse_function_key(value: str) -> dict[str, Any]:
    # Supports common pstats-ish keys such as "pkg/module.py:42(func)".
    if ":" not in value:
        return {}
    file_path, rest = value.rsplit(":", 1)
    digits = []
    for char in rest:
        if not char.isdigit():
            break
        digits.append(char)
    if not digits:
        return {}
    return {"file_path": file_path, "line": int("".join(digits))}


def _call_count(value: dict[str, Any]) -> int:
    raw = value.get("call_count") or value.get("ncalls") or value.get("calls") or value.get("primitive_calls") or 0
    if isinstance(raw, str) and "/" in raw:
        raw = raw.split("/", 1)[-1]
    return int(float(raw or 0))


def _cum_time(value: dict[str, Any]) -> float:
    return float(value.get("cum_time") or value.get("cumtime") or value.get("cumulative_time") or value.get("cum") or 0.0)


def _total_time(payload: dict[str, Any], records: list[ProfileRecord]) -> float:
    explicit = (
        payload.get("total")
        or payload.get("total_time")
        or payload.get("total_cum_time")
        or payload.get("profile_total_time")
    )
    if explicit is not None:
        return float(explicit)
    return max((record.cum_time for record in records), default=0.0)


def _node_location_index(graph: nx.DiGraph, repo_path: Path) -> dict[tuple[str, int], str]:
    index: dict[tuple[str, int], str] = {}
    repo = Path(repo_path).resolve()
    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") not in {NodeType.FUNCTION.value, NodeType.METHOD.value, NodeType.TEST_FUNCTION.value}:
            continue
        line_start = attrs.get("line_start")
        file_path = attrs.get("file_path")
        if file_path is None or line_start is None:
            continue
        paths = {_normalize_path(str(file_path))}
        try:
            paths.add(_normalize_path(str((repo / str(file_path)).resolve())))
        except OSError:
            pass
        for path in paths:
            index[(path, int(line_start))] = node_id
    return index


def _normalize_path(value: str) -> str:
    return Path(value).as_posix().lower()
