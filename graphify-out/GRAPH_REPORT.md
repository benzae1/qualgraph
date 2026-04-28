# Graph Report - analytify  (2026-04-28)

## Corpus Check
- 56 files · ~10,958 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 308 nodes · 651 edges · 13 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 263 edges (avg confidence: 0.65)
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
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 40|Community 40]]

## God Nodes (most connected - your core abstractions)
1. `AnnotatorResult` - 26 edges
2. `OrderService` - 24 edges
3. `RunLogger` - 24 edges
4. `Order` - 23 edges
5. `Inventory` - 22 edges
6. `PricingEngine` - 20 edges
7. `BaseAnnotator` - 20 edges
8. `run_pipeline()` - 15 edges
9. `_extract_classes_and_functions()` - 15 edges
10. `Customer` - 14 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `test_pricing_combines_coupon_and_category_discount()` --calls--> `PricingEngine`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\pricing.py
- `test_reports_summarize_categories_and_inventory()` --calls--> `popular_categories()`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\reports.py
- `test_reports_summarize_categories_and_inventory()` --calls--> `inventory_health()`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\reports.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (26): Enum, Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, CustomerTier, LineItem (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (33): ABC, BanditAnnotator, _finding_payload(), Bandit security annotator., _relative_to_repo(), AnnotatorResult, BaseAnnotator, Base interface for graph annotators. (+25 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (34): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), Definition, _docstring() (+26 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (24): Mutate ``graph`` with this annotator's signal., build(), main(), Command-line interface for qualgraph., Graph-aware code quality analysis for Python projects., Build a Python code graph and write an annotated graph artifact., _elapsed_ms(), _error_record() (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (6): PricingEngine, customer_summary(), inventory_health(), popular_categories(), render_daily_digest(), revenue_by_country()

### Community 5 - "Community 5"
Cohesion: 0.19
Nodes (10): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., _elapsed_ms(), LLMClient, LLMProvider, LLMRequest, LLMResponse (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (15): _add_edge(), Build a NetworkX code graph from Python source files.  The builder intentionally, _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), Name-based cross-file graph resolution.  This resolver is deliberately conservat, resolve_calls() (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (8): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _is_pipeline_node(), _percentile(), Structural metrics and cluster role heuristics., Write centrality and degree metrics back onto graph nodes., Classify each node's role within its cluster using simple topology.

### Community 8 - "Community 8"
Cohesion: 0.48
Nodes (6): _build_location_index(), find_node_for_location(), _normalize_path(), Helpers for mapping file/line findings back to graph nodes., Return the smallest graph node containing ``file_path:line``., _suffix_candidates()

### Community 9 - "Community 9"
Cohesion: 0.47
Nodes (5): annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs., Return ``node_id -> cluster_id`` using Leiden on an undirected graph., _to_igraph()

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **21 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_graph()` connect `Community 2` to `Community 1`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Why does `RunLogger` connect `Community 3` to `Community 1`, `Community 5`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `build()` connect `Community 3` to `Community 9`, `Community 2`, `Community 7`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `AnnotatorResult` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`AnnotatorResult` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `OrderService` (e.g. with `Inventory` and `Customer`) actually correct?**
  _`OrderService` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Graph-aware code quality analysis for Python projects.`) actually correct?**
  _`RunLogger` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Order` (e.g. with `StockItem` and `Inventory`) actually correct?**
  _`Order` has 14 INFERRED edges - model-reasoned connections that need verification._