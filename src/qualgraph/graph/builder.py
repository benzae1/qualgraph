"""Build a NetworkX code graph from Python source files.

The builder intentionally separates extraction from resolution. Pass 1 records
what is concrete in each file and resolves obvious local calls. Pass 2 performs
name-based cross-file resolution; that is useful for v1 but necessarily
imperfect for dynamic Python.
"""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.graph.parser import (
    CALL_QUERY,
    CLASS_QUERY,
    FUNCTION_QUERY,
    IMPORT_QUERY,
    node_text,
    parse_file,
    query_matches,
)
from qualgraph.graph.resolver import resolve_calls
from qualgraph.graph.schema import (
    EdgeAttrs,
    EdgeType,
    NodeAttrs,
    NodeType,
    edge_attrs_to_graph,
    make_node_id,
    node_attrs_to_graph,
)


DEFAULT_EXCLUDE_GLOBS = [
    ".git/**",
    ".venv/**",
    "venv/**",
    "__pycache__/**",
    "graphify-out/**",
    "src/qualgraph/graphify-out/**",
]


@dataclass(slots=True)
class Definition:
    node: Any
    node_id: str
    name: str
    qualified_name: str
    type: NodeType
    file_path: str


def build_graph(repo_path: Path, exclude_globs: list[str] | None = None) -> nx.DiGraph:
    repo_path = Path(repo_path).resolve()
    g = nx.DiGraph()
    g.graph["repo_path"] = str(repo_path)
    g.graph["symbol_table"] = {}
    g.graph["import_maps"] = {}
    g.graph["pending_calls"] = []
    g.graph["pending_inherits"] = []

    files = _collect_python_files(repo_path, exclude_globs or [])
    symbol_table: dict[str, str] = {}

    # Pass 1: nodes + intra-file edges.
    for file_path in files:
        source, tree = parse_file(file_path)
        relative_file = file_path.relative_to(repo_path).as_posix()
        module_id = _extract_module(g, source, tree, relative_file, symbol_table)
        definitions = _extract_classes_and_functions(g, source, tree, relative_file, symbol_table)
        import_map = _extract_imports(g, source, tree, relative_file, module_id)
        _extract_intra_file_calls(g, source, tree, relative_file, module_id, definitions)
        g.graph["import_maps"][relative_file] = import_map

    # Pass 2: cross-file calls (name-based; imperfect for dynamic Python).
    resolve_calls(g, symbol_table)
    g.graph["symbol_table"] = dict(symbol_table)

    return g


def _collect_python_files(repo_path: Path, exclude_globs: list[str]) -> list[Path]:
    patterns = [*DEFAULT_EXCLUDE_GLOBS, *exclude_globs]
    files: list[Path] = []
    for path in repo_path.rglob("*.py"):
        relative = path.relative_to(repo_path).as_posix()
        if any(_matches_glob(relative, pattern) for pattern in patterns):
            continue
        files.append(path)
    return sorted(files)


def _extract_module(
    g: nx.DiGraph,
    source: bytes,
    tree: Any,
    file_path: str,
    symbol_table: dict[str, str],
) -> str:
    qualified_name = _module_qualified_name(file_path)
    line_end = max(tree.root_node.end_point.row + 1, 1)
    node_id = make_node_id(file_path, qualified_name, 1)
    attrs = NodeAttrs(
        id=node_id,
        type=NodeType.MODULE,
        name=Path(file_path).stem,
        qualified_name=qualified_name,
        file_path=file_path,
        line_start=1,
        line_end=line_end,
        source=source.decode("utf-8", errors="replace"),
        docstring=_docstring(source, tree.root_node),
    )
    g.add_node(node_id, **node_attrs_to_graph(attrs))
    symbol_table[qualified_name] = node_id
    return node_id


def _extract_classes_and_functions(
    g: nx.DiGraph,
    source: bytes,
    tree: Any,
    file_path: str,
    symbol_table: dict[str, str],
) -> list[Definition]:
    module_name = _module_qualified_name(file_path)
    raw_defs = _class_definition_nodes(source, tree) + _function_definition_nodes(source, tree)
    raw_defs.sort(key=lambda item: item["node"].start_byte)
    definitions: list[Definition] = []

    for item in raw_defs:
        node = item["node"]
        name = item["name"]
        parent = _nearest_parent_definition(node, definitions)
        qualified_name = f"{parent.qualified_name}.{name}" if parent else f"{module_name}.{name}"
        node_type = _node_type(name, node, parent)
        line_start = node.start_point.row + 1
        node_id = make_node_id(file_path, qualified_name, line_start)
        attrs = NodeAttrs(
            id=node_id,
            type=node_type,
            name=name,
            qualified_name=qualified_name,
            file_path=file_path,
            line_start=line_start,
            line_end=node.end_point.row + 1,
            source=node_text(source, node),
            docstring=_docstring(source, item.get("body")),
        )
        g.add_node(node_id, **node_attrs_to_graph(attrs))
        symbol_table[qualified_name] = node_id
        definition = Definition(
            node=node,
            node_id=node_id,
            name=name,
            qualified_name=qualified_name,
            type=node_type,
            file_path=file_path,
        )
        definitions.append(definition)

        if node_type is NodeType.CLASS:
            for base_name in _class_base_names(source, node):
                g.graph["pending_inherits"].append(
                    {
                        "source": node_id,
                        "name": base_name,
                        "file_path": file_path,
                        "line_start": line_start,
                    }
                )

    return definitions


def _extract_imports(
    g: nx.DiGraph,
    source: bytes,
    tree: Any,
    file_path: str,
    module_id: str,
) -> dict[str, str]:
    import_map: dict[str, str] = {}
    imports: list[dict[str, Any]] = []
    for _, captures in query_matches(IMPORT_QUERY, tree):
        for statement in captures.get("import.statement", []):
            imports.extend(_parse_import_statement(source, statement))

    for imported in imports:
        alias = imported["alias"]
        import_map[alias] = imported["qualified_name"]
        g.graph.setdefault("pending_imports", []).append(
            {
                "source": module_id,
                "name": imported["qualified_name"],
                "alias": alias,
                "file_path": file_path,
                "line_start": imported["line_start"],
            }
        )

    return import_map


def _extract_intra_file_calls(
    g: nx.DiGraph,
    source: bytes,
    tree: Any,
    file_path: str,
    module_id: str,
    definitions: list[Definition],
) -> None:
    local_symbols = _local_symbol_index(definitions)
    for _, captures in query_matches(CALL_QUERY, tree):
        call_nodes = captures.get("call", [])
        func_nodes = captures.get("call.func", [])
        if not call_nodes or not func_nodes:
            continue
        call_node = call_nodes[0]
        func_node = func_nodes[0]
        call_name = _call_name(source, func_node)
        if not call_name:
            continue

        source_definition = _nearest_parent_definition(call_node, definitions)
        source_id = source_definition.node_id if source_definition else module_id
        target_id = _resolve_local_call(call_name, source_definition, local_symbols)

        if target_id and target_id != source_id:
            _add_edge(g, source_id, target_id, EdgeType.CALLS, source=call_name)
        else:
            g.graph["pending_calls"].append(
                {
                    "source": source_id,
                    "name": call_name,
                    "file_path": file_path,
                    "line_start": call_node.start_point.row + 1,
                }
            )


def _class_definition_nodes(source: bytes, tree: Any) -> list[dict[str, Any]]:
    result = []
    for _, captures in query_matches(CLASS_QUERY, tree):
        defs = captures.get("class.def", [])
        names = captures.get("class.name", [])
        bodies = captures.get("class.body", [])
        if defs and names:
            result.append({"node": defs[0], "name": node_text(source, names[0]), "body": bodies[0] if bodies else None})
    return result


def _function_definition_nodes(source: bytes, tree: Any) -> list[dict[str, Any]]:
    result = []
    for _, captures in query_matches(FUNCTION_QUERY, tree):
        defs = captures.get("func.def", [])
        names = captures.get("func.name", [])
        bodies = captures.get("func.body", [])
        if defs and names:
            result.append({"node": defs[0], "name": node_text(source, names[0]), "body": bodies[0] if bodies else None})
    return result


def _nearest_parent_definition(node: Any, definitions: list[Definition]) -> Definition | None:
    parents = [
        definition
        for definition in definitions
        if definition.node.start_byte < node.start_byte and node.end_byte <= definition.node.end_byte
    ]
    if not parents:
        return None
    return max(parents, key=lambda definition: definition.node.start_byte)


def _node_type(name: str, node: Any, parent: Definition | None) -> NodeType:
    if node.type == "class_definition":
        return NodeType.CLASS
    if parent and parent.type is NodeType.CLASS:
        return NodeType.METHOD
    if name.startswith("test_"):
        return NodeType.TEST_FUNCTION
    return NodeType.FUNCTION


def _class_base_names(source: bytes, node: Any) -> list[str]:
    bases: list[str] = []
    for child in node.children:
        if child.type != "argument_list":
            continue
        for grandchild in child.named_children:
            if grandchild.type in {"identifier", "attribute", "dotted_name"}:
                bases.append(node_text(source, grandchild))
    return bases


def _parse_import_statement(source: bytes, statement: Any) -> list[dict[str, Any]]:
    if statement.type == "import_statement":
        return _parse_plain_import(source, statement)
    if statement.type == "import_from_statement":
        return _parse_from_import(source, statement)
    return []


def _parse_plain_import(source: bytes, statement: Any) -> list[dict[str, Any]]:
    imports = []
    for child in statement.named_children:
        if child.type == "aliased_import":
            name_node, alias_node = _aliased_import_parts(child)
            qualified_name = node_text(source, name_node)
            alias = node_text(source, alias_node)
        elif child.type == "dotted_name":
            qualified_name = node_text(source, child)
            alias = qualified_name.split(".", 1)[0]
        else:
            continue
        imports.append(
            {
                "qualified_name": qualified_name,
                "alias": alias,
                "line_start": statement.start_point.row + 1,
            }
        )
    return imports


def _parse_from_import(source: bytes, statement: Any) -> list[dict[str, Any]]:
    named_children = list(statement.named_children)
    if not named_children:
        return []
    module_node = named_children[0]
    module_name = node_text(source, module_node)
    imports = []
    for child in named_children[1:]:
        if child.type == "aliased_import":
            name_node, alias_node = _aliased_import_parts(child)
            imported_name = node_text(source, name_node)
            alias = node_text(source, alias_node)
        elif child.type in {"dotted_name", "identifier"}:
            imported_name = node_text(source, child)
            alias = imported_name.split(".")[-1]
        else:
            continue
        imports.append(
            {
                "qualified_name": f"{module_name}.{imported_name}",
                "alias": alias,
                "line_start": statement.start_point.row + 1,
            }
        )
    return imports


def _aliased_import_parts(node: Any) -> tuple[Any, Any]:
    named = list(node.named_children)
    if len(named) < 2:
        return named[0], named[0]
    return named[0], named[1]


def _local_symbol_index(definitions: list[Definition]) -> dict[str, list[Definition]]:
    by_name: dict[str, list[Definition]] = {}
    for definition in definitions:
        by_name.setdefault(definition.name, []).append(definition)
        by_name.setdefault(definition.qualified_name, []).append(definition)
    return by_name


def _resolve_local_call(
    call_name: str,
    source_definition: Definition | None,
    local_symbols: dict[str, list[Definition]],
) -> str | None:
    if source_definition and call_name.startswith("self."):
        method_name = call_name.split(".", 1)[1]
        class_name = source_definition.qualified_name.rsplit(".", 1)[0]
        candidates = local_symbols.get(f"{class_name}.{method_name}", [])
        if candidates:
            return candidates[0].node_id

    candidates = local_symbols.get(call_name, [])
    if len(candidates) == 1:
        return candidates[0].node_id

    simple_name = call_name.rsplit(".", 1)[-1]
    candidates = local_symbols.get(simple_name, [])
    if len(candidates) == 1:
        return candidates[0].node_id
    return None


def _call_name(source: bytes, node: Any) -> str | None:
    if node.type in {"identifier", "attribute", "dotted_name"}:
        return node_text(source, node)
    return None


def _docstring(source: bytes, block_node: Any | None) -> str | None:
    if block_node is None:
        return None
    for child in block_node.named_children:
        if child.type != "expression_statement":
            continue
        named_children = list(child.named_children)
        if not named_children:
            continue
        first = named_children[0]
        if first.type in {"string", "concatenated_string"}:
            return node_text(source, first)
        break
    return None


def _module_qualified_name(file_path: str) -> str:
    path = Path(file_path)
    without_suffix = path.with_suffix("")
    parts = list(without_suffix.parts)
    if parts and parts[0] == "src":
        parts = parts[1:]
    if parts[-1] == "__init__":
        parts = parts[:-1] or ["__init__"]
    return ".".join(parts)


def _matches_glob(path: str, pattern: str) -> bool:
    normalized = pattern.replace("\\", "/")
    return fnmatch(path, normalized) or fnmatch(path, normalized.rstrip("/") + "/**")


def _add_edge(g: nx.DiGraph, source_id: str, target_id: str, edge_type: EdgeType, **attrs: Any) -> None:
    edge_attrs = edge_attrs_to_graph(EdgeAttrs(type=edge_type, **attrs))
    g.add_edge(source_id, target_id, **edge_attrs)
