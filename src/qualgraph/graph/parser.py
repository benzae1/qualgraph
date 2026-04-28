"""Tree-sitter parsing helpers for Python source files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import tree_sitter_python
from tree_sitter import Language, Parser, Tree


try:
    PY_LANGUAGE = Language(tree_sitter_python.language(), "python")
except TypeError:
    PY_LANGUAGE = Language(tree_sitter_python.language())

FUNCTION_QUERY = PY_LANGUAGE.query(
    """
    (function_definition
      name: (identifier) @func.name
      parameters: (parameters) @func.params
      body: (block) @func.body) @func.def
    """,
)

CLASS_QUERY = PY_LANGUAGE.query(
    """
    (class_definition
      name: (identifier) @class.name
      body: (block) @class.body) @class.def
    """,
)

IMPORT_QUERY = PY_LANGUAGE.query(
    """
    [
      (import_statement) @import.statement
      (import_from_statement) @import.statement
    ]
    """,
)

CALL_QUERY = PY_LANGUAGE.query(
    """
    (call
      function: (_) @call.func
      arguments: (argument_list) @call.args) @call
    """,
)


def parse_file(path: str | Path) -> tuple[bytes, Tree]:
    with open(path, "rb") as handle:
        source = handle.read()
    parser = _parser()
    return source, parser.parse(source or b"\n")


def query_matches(query: Any, tree: Tree) -> list[tuple[int, dict[str, list[Any]]]]:
    if hasattr(query, "matches"):
        return [
            (pattern_index, _normalize_captures(captures))
            for pattern_index, captures in query.matches(tree.root_node)
        ]

    from tree_sitter import QueryCursor

    return QueryCursor(query).matches(tree.root_node)


def node_text(source: bytes, node: Any) -> str:
    return source[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def _parser() -> Parser:
    parser = Parser()
    if hasattr(parser, "set_language"):
        parser.set_language(PY_LANGUAGE)
        return parser
    try:
        return Parser(PY_LANGUAGE)
    except TypeError:
        parser.language = PY_LANGUAGE
        return parser


def _normalize_captures(captures: dict[str, Any]) -> dict[str, list[Any]]:
    normalized = {}
    for name, value in captures.items():
        normalized[name] = value if isinstance(value, list) else [value]
    return normalized
