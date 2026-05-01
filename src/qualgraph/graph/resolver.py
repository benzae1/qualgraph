"""Name-based cross-file graph resolution.

This resolver is deliberately conservative and imperfect. It uses imports and
qualified-name suffixes to connect calls and inheritance edges, which is enough
for v1 graph context but will miss dynamic dispatch, aliases assigned at
runtime, decorators that replace functions, and type-driven method targets.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping

import networkx as nx

from qualgraph.graph.schema import EdgeAttrs, EdgeType, edge_attrs_to_graph


def resolve_calls(g: nx.DiGraph, symbol_table: Mapping[str, str]) -> None:
    pending_calls = list(g.graph.get("pending_calls", []))
    pending_inherits = list(g.graph.get("pending_inherits", []))
    pending_imports = list(g.graph.get("pending_imports", []))
    import_maps = g.graph.get("import_maps", {})
    suffix_index = _suffix_index(symbol_table)

    for imported in pending_imports:
        target_id = _resolve_name(imported["name"], imported["file_path"], symbol_table, import_maps, suffix_index)
        if target_id and target_id != imported["source"]:
            _add_edge(
                g,
                imported["source"],
                target_id,
                EdgeType.IMPORTS,
                source=imported["alias"],
                target=imported["name"],
            )

    unresolved_calls = []
    for call in pending_calls:
        target_id = _resolve_name(call["name"], call["file_path"], symbol_table, import_maps, suffix_index)
        if target_id and target_id != call["source"]:
            _add_edge(g, call["source"], target_id, EdgeType.CALLS, source=call["name"])
        else:
            unresolved_calls.append(call)

    unresolved_inherits = []
    for inherit in pending_inherits:
        target_id = _resolve_name(inherit["name"], inherit["file_path"], symbol_table, import_maps, suffix_index)
        if target_id and target_id != inherit["source"]:
            _add_edge(g, inherit["source"], target_id, EdgeType.INHERITS, source=inherit["name"])
        else:
            unresolved_inherits.append(inherit)

    g.graph["unresolved_calls"] = unresolved_calls
    g.graph["unresolved_inherits"] = unresolved_inherits


def _resolve_name(
    name: str,
    file_path: str,
    symbol_table: Mapping[str, str],
    import_maps: Mapping[str, Mapping[str, str]],
    suffix_index: Mapping[str, set[str]],
) -> str | None:
    candidates = _candidate_names(name, file_path, import_maps)
    for candidate in candidates:
        if candidate in symbol_table:
            return symbol_table[candidate]

    suffix_matches: set[str] = set()
    for candidate in candidates:
        suffix_matches.update(suffix_index.get(candidate, set()))
    unique_matches = sorted(suffix_matches)
    if len(unique_matches) == 1:
        return unique_matches[0]
    return None


def _suffix_index(symbol_table: Mapping[str, str]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = defaultdict(set)
    for qualified_name, node_id in symbol_table.items():
        parts = qualified_name.split(".")
        for offset in range(len(parts)):
            index[".".join(parts[offset:])].add(node_id)
    return dict(index)


def _candidate_names(
    name: str,
    file_path: str,
    import_maps: Mapping[str, Mapping[str, str]],
) -> list[str]:
    import_map = import_maps.get(file_path, {})
    parts = name.split(".")
    candidates = [name]

    if parts[0] in import_map:
        imported_name = import_map[parts[0]]
        rest = parts[1:]
        candidates.insert(0, ".".join([imported_name, *rest]) if rest else imported_name)

    if name in import_map:
        candidates.insert(0, import_map[name])

    return _dedupe(candidates)


def _dedupe(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _add_edge(g: nx.DiGraph, source_id: str, target_id: str, edge_type: EdgeType, **attrs: Any) -> None:
    edge_attrs = edge_attrs_to_graph(EdgeAttrs(type=edge_type, **attrs))
    g.add_edge(source_id, target_id, **edge_attrs)
