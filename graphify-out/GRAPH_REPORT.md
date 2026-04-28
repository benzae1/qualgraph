# Graph Report - analytify  (2026-04-28)

## Corpus Check
- 46 files · ~6,781 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 144 nodes · 223 edges · 7 communities detected
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `RunLogger` - 18 edges
2. `_extract_classes_and_functions()` - 14 edges
3. `build_graph()` - 9 edges
4. `node_text()` - 9 edges
5. `_extract_intra_file_calls()` - 8 edges
6. `_extract_module()` - 7 edges
7. `EdgeType` - 7 edges
8. `LLMAnalyzer` - 7 edges
9. `LLMClient` - 7 edges
10. `BaseAnnotator` - 6 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `RunLogger` --uses--> `AnnotatorResult`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `RunLogger` --uses--> `BaseAnnotator`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `RunLogger` --uses--> `Mutate ``graph`` with this annotator's signal.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.16
Nodes (13): Mutate ``graph`` with this annotator's signal., _elapsed_ms(), _error_record(), _json_safe(), LLMUsage, Structured run logging for qualgraph.  Every CLI run should create a JSONL event, Write structured JSONL events and aggregate per-run counters., RunLogger (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.19
Nodes (20): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), _extract_imports(), _extract_intra_file_calls() (+12 more)

### Community 2 - "Community 2"
Cohesion: 0.2
Nodes (18): Definition, _docstring(), _extract_classes_and_functions(), _extract_module(), _module_qualified_name(), _node_type(), Build a NetworkX code graph from Python source files.  The builder intentionally, Enum (+10 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (10): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., _elapsed_ms(), LLMClient, LLMProvider, LLMRequest, LLMResponse (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.26
Nodes (9): ABC, annotate(), AnnotatorResult, BaseAnnotator, _count_delta(), _elapsed_ms(), Base interface for graph annotators., _result_counts() (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.31
Nodes (10): _add_edge(), _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), Name-based cross-file graph resolution.  This resolver is deliberately conservat, resolve_calls(), _resolve_name() (+2 more)

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

## Knowledge Gaps
- **9 isolated node(s):** `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.`, `Tree-sitter parsing helpers for Python source files.` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RunLogger` connect `Community 0` to `Community 3`, `Community 4`?**
  _High betweenness centrality (0.225) - this node is a cross-community bridge._
- **Why does `build_graph()` connect `Community 1` to `Community 2`, `Community 5`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `_error_record()` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `RunLogger` (e.g. with `AnnotatorResult` and `BaseAnnotator`) actually correct?**
  _`RunLogger` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `_extract_classes_and_functions()` (e.g. with `make_node_id()` and `NodeAttrs`) actually correct?**
  _`_extract_classes_and_functions()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `build_graph()` (e.g. with `str` and `parse_file()`) actually correct?**
  _`build_graph()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `node_text()` (e.g. with `_extract_classes_and_functions()` and `_class_definition_nodes()`) actually correct?**
  _`node_text()` has 8 INFERRED edges - model-reasoned connections that need verification._