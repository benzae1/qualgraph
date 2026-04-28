# Graph Report - analytify  (2026-04-28)

## Corpus Check
- 53 files · ~9,664 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 260 nodes · 525 edges · 11 communities detected
- Extraction: 62% EXTRACTED · 38% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.66)
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
- [[_COMMUNITY_Community 43|Community 43]]

## God Nodes (most connected - your core abstractions)
1. `OrderService` - 24 edges
2. `Order` - 23 edges
3. `Inventory` - 22 edges
4. `RunLogger` - 22 edges
5. `PricingEngine` - 20 edges
6. `_extract_classes_and_functions()` - 15 edges
7. `Customer` - 14 edges
8. `LineItem` - 13 edges
9. `Mailer` - 12 edges
10. `Receipt` - 11 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `test_checkout_reserves_stock_and_sends_mail()` --calls--> `Mailer`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\orders.py
- `test_payment_decline_releases_stock()` --calls--> `PaymentGateway`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\orders.py
- `test_pricing_combines_coupon_and_category_discount()` --calls--> `PricingEngine`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\pricing.py
- `StockItem` --uses--> `LineItem`  [INFERRED]
  benchmarks\repos\tiny_repo\tiny_shop\inventory.py → benchmarks\repos\tiny_repo\tiny_shop\models.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (19): Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, Product, OrderService, Receipt (+11 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (28): ABC, annotate(), AnnotatorResult, BaseAnnotator, _count_delta(), _elapsed_ms(), Base interface for graph annotators., Mutate ``graph`` with this annotator's signal. (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.1
Nodes (13): Enum, CustomerTier, LineItem, Order, OrderStatus, Domain models for the tiny shop benchmark., Mailer, PaymentGateway (+5 more)

### Community 3 - "Community 3"
Cohesion: 0.15
Nodes (31): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), _docstring(), _extract_classes_and_functions() (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (18): _add_edge(), Definition, Build a NetworkX code graph from Python source files.  The builder intentionally, _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), Name-based cross-file graph resolution.  This resolver is deliberately conservat (+10 more)

### Community 5 - "Community 5"
Cohesion: 0.19
Nodes (10): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., _elapsed_ms(), LLMClient, LLMProvider, LLMRequest, LLMResponse (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (8): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _is_pipeline_node(), _percentile(), Structural metrics and cluster role heuristics., Write centrality and degree metrics back onto graph nodes., Classify each node's role within its cluster using simple topology.

### Community 7 - "Community 7"
Cohesion: 0.36
Nodes (7): _graphml_safe_copy(), _graphml_value(), _json_safe(), Graph serialization helpers., to_node_link_data(), write_graphml_graph(), write_json_graph()

### Community 8 - "Community 8"
Cohesion: 0.47
Nodes (5): annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs., Return ``node_id -> cluster_id`` using Leiden on an undirected graph., _to_igraph()

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **17 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_graph()` connect `Community 3` to `Community 1`, `Community 4`?**
  _High betweenness centrality (0.235) - this node is a cross-community bridge._
- **Why does `RunLogger` connect `Community 1` to `Community 5`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Why does `build()` connect `Community 1` to `Community 8`, `Community 3`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `OrderService` (e.g. with `Inventory` and `Customer`) actually correct?**
  _`OrderService` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Order` (e.g. with `StockItem` and `Inventory`) actually correct?**
  _`Order` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Inventory` (e.g. with `LineItem` and `Order`) actually correct?**
  _`Inventory` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Graph-aware code quality analysis for Python projects.`) actually correct?**
  _`RunLogger` has 15 INFERRED edges - model-reasoned connections that need verification._