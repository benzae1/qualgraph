# Graph Report - analytify  (2026-04-28)

## Corpus Check
- 54 files · ~9,860 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 275 nodes · 565 edges · 11 communities detected
- Extraction: 61% EXTRACTED · 39% INFERRED · 0% AMBIGUOUS · INFERRED: 223 edges (avg confidence: 0.65)
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
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 43|Community 43]]

## God Nodes (most connected - your core abstractions)
1. `OrderService` - 24 edges
2. `RunLogger` - 24 edges
3. `Order` - 23 edges
4. `Inventory` - 22 edges
5. `PricingEngine` - 20 edges
6. `run_pipeline()` - 15 edges
7. `_extract_classes_and_functions()` - 15 edges
8. `Customer` - 14 edges
9. `LineItem` - 13 edges
10. `Mailer` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Command-line interface for qualgraph.` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\logging.py
- `Graph-aware code quality analysis for Python projects.` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\logging.py
- `Build a Python code graph and write an annotated graph artifact.` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\logging.py
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `test_pricing_combines_coupon_and_category_discount()` --calls--> `PricingEngine`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\pricing.py

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
Nodes (23): Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, LineItem, Product, Mailer (+15 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (29): ABC, AnnotatorResult, BaseAnnotator, Base interface for graph annotators., Mutate ``graph`` with this annotator's signal., Check that the underlying tool is installed and runnable., BaseAnnotator, LLMProvider (+21 more)

### Community 2 - "Community 2"
Cohesion: 0.16
Nodes (29): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), _docstring(), _extract_classes_and_functions() (+21 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (25): _add_edge(), Definition, Build a NetworkX code graph from Python source files.  The builder intentionally, Enum, CustomerTier, OrderStatus, Domain models for the tiny shop benchmark., _add_edge() (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (5): Order, PriceBreakdown, PricingEngine, Pricing rules for orders., customer_summary()

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (17): build(), main(), Command-line interface for qualgraph., Graph-aware code quality analysis for Python projects., Build a Python code graph and write an annotated graph artifact., annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs. (+9 more)

### Community 6 - "Community 6"
Cohesion: 0.23
Nodes (8): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., _elapsed_ms(), LLMClient, LLMRequest, LLMResponse, Provider-agnostic LLM client with built-in cost/timing logging.

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (8): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _is_pipeline_node(), _percentile(), Structural metrics and cluster role heuristics., Write centrality and degree metrics back onto graph nodes., Classify each node's role within its cluster using simple topology.

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **19 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 8`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_graph()` connect `Community 2` to `Community 3`, `Community 5`?**
  _High betweenness centrality (0.222) - this node is a cross-community bridge._
- **Why does `RunLogger` connect `Community 1` to `Community 5`, `Community 6`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `build()` connect `Community 5` to `Community 1`, `Community 2`, `Community 7`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `OrderService` (e.g. with `Inventory` and `Customer`) actually correct?**
  _`OrderService` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Graph-aware code quality analysis for Python projects.`) actually correct?**
  _`RunLogger` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Order` (e.g. with `StockItem` and `Inventory`) actually correct?**
  _`Order` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Inventory` (e.g. with `LineItem` and `Order`) actually correct?**
  _`Inventory` has 11 INFERRED edges - model-reasoned connections that need verification._