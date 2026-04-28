"""Helpers for mapping file/line findings back to graph nodes."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import networkx as nx


LOCATION_INDEX_KEY = "_location_index"


def find_node_for_location(graph: nx.DiGraph, file_path: str | Path, line: int) -> Optional[str]:
    """Return the smallest graph node containing ``file_path:line``."""

    if line <= 0:
        return None

    index = graph.graph.get(LOCATION_INDEX_KEY)
    if index is None:
        index = _build_location_index(graph)
        graph.graph[LOCATION_INDEX_KEY] = index

    normalized = _normalize_path(file_path)
    candidates = index.get(normalized)
    if candidates is None:
        candidates = _suffix_candidates(index, normalized)
    if not candidates:
        return None

    for line_start, line_end, node_id in candidates:
        if line_start <= line <= line_end:
            return node_id
    return None


def nodes_for_file(graph: nx.DiGraph, file_path: str | Path) -> list[str]:
    index = graph.graph.get(LOCATION_INDEX_KEY)
    if index is None:
        index = _build_location_index(graph)
        graph.graph[LOCATION_INDEX_KEY] = index

    normalized = _normalize_path(file_path)
    candidates = index.get(normalized)
    if candidates is None:
        candidates = _suffix_candidates(index, normalized)
    return [node_id for _line_start, _line_end, node_id in candidates or []]


def _build_location_index(graph: nx.DiGraph) -> dict[str, list[tuple[int, int, str]]]:
    by_file: dict[str, list[tuple[int, int, str]]] = {}
    for node_id, attrs in graph.nodes(data=True):
        file_path = attrs.get("file_path")
        line_start = attrs.get("line_start")
        line_end = attrs.get("line_end")
        if not file_path or line_start is None or line_end is None:
            continue
        key = _normalize_path(file_path)
        by_file.setdefault(key, []).append((int(line_start), int(line_end), node_id))

    for intervals in by_file.values():
        intervals.sort(key=lambda item: (item[1] - item[0], -item[0]))
    return by_file


def _suffix_candidates(
    index: dict[str, list[tuple[int, int, str]]],
    normalized: str,
) -> list[tuple[int, int, str]]:
    matches = [
        intervals
        for indexed_path, intervals in index.items()
        if indexed_path.endswith("/" + normalized) or normalized.endswith("/" + indexed_path)
    ]
    if len(matches) == 1:
        return matches[0]
    return []


def _normalize_path(path: str | Path) -> str:
    return Path(path).as_posix().lstrip("./")
