"""Tree-sitter parsing helpers for Python source files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import tree_sitter_python
from tree_sitter import Language, Parser, Query, QueryCursor, Tree


PY_LANGUAGE = Language(tree_sitter_python.language())

FUNCTION_QUERY = Query(
    PY_LANGUAGE,
    """
    (function_definition
      name: (identifier) @func.name
      parameters: (parameters) @func.params
      body: (block) @func.body) @func.def
    """,
)

CLASS_QUERY = Query(
    PY_LANGUAGE,
    """
    (class_definition
      name: (identifier) @class.name
      body: (block) @class.body) @class.def
    """,
)

IMPORT_QUERY = Query(
    PY_LANGUAGE,
    """
    [
      (import_statement) @import.statement
      (import_from_statement) @import.statement
    ]
    """,
)

CALL_QUERY = Query(
    PY_LANGUAGE,
    """
    (call
      function: (_) @call.func
      arguments: (argument_list) @call.args) @call
    """,
)


def parse_file(path: str | Path) -> tuple[bytes, Tree]:
    with open(path, "rb") as handle:
        source = handle.read()
    parser = Parser(PY_LANGUAGE)
    return source, parser.parse(source)


def query_matches(query: Query, tree: Tree) -> list[tuple[int, dict[str, list[Any]]]]:
    return QueryCursor(query).matches(tree.root_node)


def node_text(source: bytes, node: Any) -> str:
    return source[node.start_byte : node.end_byte].decode("utf-8", errors="replace")
