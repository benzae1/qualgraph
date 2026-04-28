"""Canonical graph schema for qualgraph.

This module is intentionally small and boring: the rest of the project should
build graphs to these shapes instead of inventing attributes ad hoc.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class NodeType(str, Enum):
    MODULE = "Module"
    CLASS = "Class"
    FUNCTION = "Function"
    METHOD = "Method"
    TEST_FUNCTION = "TestFunction"


class EdgeType(str, Enum):
    CALLS = "calls"
    IMPORTS = "imports"
    INHERITS = "inherits"
    TESTED_BY = "tested_by"
    CO_CHANGES_WITH = "co_changes_with"
    IMPORTS_VULNERABLE = "imports_vulnerable"


NODE_ID_SEPARATOR = "::"


@dataclass(slots=True)
class NodeAttrs:
    # Identity
    id: str
    type: NodeType
    name: str
    qualified_name: str
    file_path: str
    line_start: int
    line_end: int
    source: Optional[str] = None
    docstring: Optional[str] = None
    # Everything else populated by annotators - keep optional.
    complexity: Optional[float] = None
    maintainability_index: Optional[float] = None
    coverage_line: Optional[float] = None
    coverage_branch: Optional[float] = None
    churn: Optional[int] = None
    author_count: Optional[int] = None
    bug_fix_keywords: Optional[int] = None
    centrality: Optional[float] = None
    betweenness_centrality: Optional[float] = None
    degree_centrality: Optional[float] = None
    pagerank: Optional[float] = None
    structural_score: Optional[float] = None
    in_degree: Optional[int] = None
    out_degree: Optional[int] = None
    cluster_id: Optional[int] = None
    cluster_role: Optional[str] = None
    findings: list[Any] = field(default_factory=list)
    risk_score: Optional[float] = None
    risk_components: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EdgeAttrs:
    type: EdgeType
    source: Optional[str] = None
    target: Optional[str] = None
    confidence: Optional[float] = None
    weight: Optional[float] = None
    findings: list[Any] = field(default_factory=list)


IDENTITY_NODE_ATTRS = (
    "id",
    "type",
    "name",
    "qualified_name",
    "file_path",
    "line_start",
    "line_end",
)

OPTIONAL_NODE_ATTRS = (
    "source",
    "docstring",
    "complexity",
    "maintainability_index",
    "coverage_line",
    "coverage_branch",
    "churn",
    "author_count",
    "bug_fix_keywords",
    "centrality",
    "betweenness_centrality",
    "degree_centrality",
    "pagerank",
    "structural_score",
    "in_degree",
    "out_degree",
    "cluster_id",
    "cluster_role",
    "findings",
    "risk_score",
    "risk_components",
)

NODE_ATTRS = IDENTITY_NODE_ATTRS + OPTIONAL_NODE_ATTRS
EDGE_ATTRS = ("type", "source", "target", "confidence", "weight", "findings")


def make_node_id(file_path: str | Path, qualified_name: str, line_start: int) -> str:
    """Return the stable node id used by graph building and caching.

    Convention: ``file_path::qualified_name::line_start``.
    """

    normalized_path = Path(file_path).as_posix()
    return NODE_ID_SEPARATOR.join((normalized_path, qualified_name, str(line_start)))


def node_attrs_to_graph(attrs: NodeAttrs) -> dict[str, Any]:
    data = asdict(attrs)
    data["type"] = attrs.type.value
    return data


def edge_attrs_to_graph(attrs: EdgeAttrs) -> dict[str, Any]:
    data = asdict(attrs)
    data["type"] = attrs.type.value
    return data


def coerce_node_type(value: str | NodeType) -> NodeType:
    return value if isinstance(value, NodeType) else NodeType(value)


def coerce_edge_type(value: str | EdgeType) -> EdgeType:
    return value if isinstance(value, EdgeType) else EdgeType(value)
