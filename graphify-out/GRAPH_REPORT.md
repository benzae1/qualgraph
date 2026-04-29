# Graph Report - analytify  (2026-04-29)

## Corpus Check
- 57 files · ~15,146 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 407 nodes · 1016 edges · 18 communities detected
- Extraction: 54% EXTRACTED · 46% INFERRED · 0% AMBIGUOUS · INFERRED: 468 edges (avg confidence: 0.63)
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
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]

## God Nodes (most connected - your core abstractions)
1. `AnnotatorResult` - 41 edges
2. `RunLogger` - 32 edges
3. `BaseAnnotator` - 30 edges
4. `OrderService` - 24 edges
5. `Order` - 23 edges
6. `Inventory` - 22 edges
7. `PricingEngine` - 20 edges
8. `TestLinkageAnnotator` - 19 edges
9. `render_markdown_report()` - 19 edges
10. `CoChangeAnnotator` - 18 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
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
Cohesion: 0.06
Nodes (32): Enum, Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, CustomerTier, LineItem (+24 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (38): BanditAnnotator, Mutate ``graph`` with this annotator's signal., BaseAnnotator, annotate(), build(), main(), Command-line interface for qualgraph., Render a Markdown report from an annotated graph JSON file. (+30 more)

### Community 2 - "Community 2"
Cohesion: 0.1
Nodes (42): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), Definition, _docstring() (+34 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (27): ABC, Bandit security annotator., AnnotatorResult, BaseAnnotator, Base interface for graph annotators., Check that the underlying tool is installed and runnable., _module_node_for_file(), Git co-change annotator. (+19 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (21): _finding_payload(), _relative_to_repo(), add_finding(), clear_findings_by_source(), finding_key(), Helpers for attaching tool findings to graph nodes., Remove stale findings from a previous run of the same annotator., Attach ``finding`` if the same tool/code/location is not already present. (+13 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (20): _add_edge(), _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), Name-based cross-file graph resolution.  This resolver is deliberately conservat, resolve_calls(), _resolve_name() (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (21): _co_change_lines(), _finding_code(), _finding_line(), _finding_records(), _format_score(), _format_small(), _git_history_lines(), _is_low_signal_finding() (+13 more)

### Community 7 - "Community 7"
Cohesion: 0.18
Nodes (10): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., _elapsed_ms(), LLMClient, LLMProvider, LLMRequest, LLMResponse (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.25
Nodes (13): _has_tests(), _relative_to_repo(), _add_vulnerable_import_edge(), _clear_imports_vulnerable_edges(), _ensure_dependency_node(), _finding_payload(), _import_package_candidates(), _import_records() (+5 more)

### Community 9 - "Community 9"
Cohesion: 0.26
Nodes (12): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _degree_centrality(), _is_pipeline_node(), _normalize(), _pagerank(), _percentile() (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.28
Nodes (6): detect_untested_hotspots(), _percentile(), Cross-signal findings derived from the shared graph., Finding, Typed findings produced by derived and LLM analysis., test_detect_untested_hotspots_combines_complexity_centrality_and_coverage()

### Community 11 - "Community 11"
Cohesion: 0.43
Nodes (7): _graphml_safe_copy(), _graphml_value(), _json_safe(), Graph serialization helpers., to_node_link_data(), write_graphml_graph(), write_json_graph()

### Community 12 - "Community 12"
Cohesion: 0.47
Nodes (5): annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs., Return ``node_id -> cluster_id`` using Leiden on an undirected graph., _to_igraph()

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **29 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+24 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 13`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_graph()` connect `Community 2` to `Community 8`, `Community 1`, `Community 5`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `RunLogger` connect `Community 1` to `Community 3`, `Community 4`, `Community 7`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `AnnotatorResult` connect `Community 3` to `Community 8`, `Community 1`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `AnnotatorResult` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`AnnotatorResult` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Graph-aware code quality analysis for Python projects.`) actually correct?**
  _`RunLogger` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `BaseAnnotator` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`BaseAnnotator` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `OrderService` (e.g. with `Inventory` and `Customer`) actually correct?**
  _`OrderService` has 14 INFERRED edges - model-reasoned connections that need verification._