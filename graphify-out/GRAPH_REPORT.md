# Graph Report - analytify  (2026-04-28)

## Corpus Check
- 46 files · ~7,748 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 174 nodes · 282 edges · 10 communities detected
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 79 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 42|Community 42]]

## God Nodes (most connected - your core abstractions)
1. `RunLogger` - 22 edges
2. `_extract_classes_and_functions()` - 15 edges
3. `build()` - 10 edges
4. `build_graph()` - 10 edges
5. `_extract_intra_file_calls()` - 9 edges
6. `node_text()` - 9 edges
7. `_extract_module()` - 8 edges
8. `EdgeType` - 7 edges
9. `LLMAnalyzer` - 7 edges
10. `LLMClient` - 7 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `build()` --calls--> `build_graph()`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\graph\builder.py
- `build()` --calls--> `annotate_clusters()`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\graph\clustering.py
- `build()` --calls--> `annotate_metrics()`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\graph\metrics.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (31): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), Definition, _docstring() (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (17): Mutate ``graph`` with this annotator's signal., build(), main(), Command-line interface for qualgraph., Graph-aware code quality analysis for Python projects., Build a Python code graph and write an annotated graph artifact., _elapsed_ms(), _error_record() (+9 more)

### Community 2 - "Community 2"
Cohesion: 0.17
Nodes (19): _add_edge(), Build a NetworkX code graph from Python source files.  The builder intentionally, Enum, _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), Name-based cross-file graph resolution.  This resolver is deliberately conservat (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (10): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., _elapsed_ms(), LLMClient, LLMProvider, LLMRequest, LLMResponse (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (11): ABC, annotate(), AnnotatorResult, BaseAnnotator, _count_delta(), _elapsed_ms(), Base interface for graph annotators., _result_counts() (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.36
Nodes (7): _graphml_safe_copy(), _graphml_value(), _json_safe(), Graph serialization helpers., to_node_link_data(), write_graphml_graph(), write_json_graph()

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (8): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _is_pipeline_node(), _percentile(), Structural metrics and cluster role heuristics., Write centrality and degree metrics back onto graph nodes., Classify each node's role within its cluster using simple topology.

### Community 7 - "Community 7"
Cohesion: 0.47
Nodes (5): annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs., Return ``node_id -> cluster_id`` using Leiden on an undirected graph., _to_igraph()

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **16 isolated node(s):** `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.`, `Leiden community detection for code graphs.` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 8`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build()` connect `Community 1` to `Community 0`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.305) - this node is a cross-community bridge._
- **Why does `RunLogger` connect `Community 1` to `Community 3`, `Community 4`?**
  _High betweenness centrality (0.275) - this node is a cross-community bridge._
- **Why does `build_graph()` connect `Community 0` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Graph-aware code quality analysis for Python projects.`) actually correct?**
  _`RunLogger` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `_extract_classes_and_functions()` (e.g. with `make_node_id()` and `NodeAttrs`) actually correct?**
  _`_extract_classes_and_functions()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `build()` (e.g. with `RunLogger` and `span()`) actually correct?**
  _`build()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `build_graph()` (e.g. with `build()` and `str`) actually correct?**
  _`build_graph()` has 4 INFERRED edges - model-reasoned connections that need verification._