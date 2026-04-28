"""Graph serialization helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import networkx as nx
from networkx.readwrite import json_graph


SCHEMA_VERSION = "0.1.0"


def to_node_link_data(g: nx.DiGraph) -> dict[str, Any]:
    try:
        data = json_graph.node_link_data(g, edges="links")
    except TypeError:
        data = json_graph.node_link_data(g, link="links")
    data["schema_version"] = SCHEMA_VERSION
    data.setdefault("graph", {})
    data["graph"]["schema_version"] = SCHEMA_VERSION
    return _json_safe(data)


def write_json_graph(g: nx.DiGraph, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(to_node_link_data(g), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return output_path


def read_json_graph(path: str | Path) -> nx.DiGraph:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    try:
        return json_graph.node_link_graph(data, directed=True, edges="links")
    except TypeError:
        return json_graph.node_link_graph(data, directed=True, link="links")


def write_graphml_graph(g: nx.DiGraph, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(_graphml_safe_copy(g), output_path)
    return output_path


def _graphml_safe_copy(g: nx.DiGraph) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.graph.update({key: _graphml_value(value) for key, value in g.graph.items()})
    graph.graph["schema_version"] = SCHEMA_VERSION
    for node_id, attrs in g.nodes(data=True):
        graph.add_node(node_id, **{key: _graphml_value(value) for key, value in attrs.items()})
    for source, target, attrs in g.edges(data=True):
        graph.add_edge(source, target, **{key: _graphml_value(value) for key, value in attrs.items()})
    return graph


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    try:
        json.dumps(value)
    except TypeError:
        return str(value)
    return value


def _graphml_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(_json_safe(value), sort_keys=True)
