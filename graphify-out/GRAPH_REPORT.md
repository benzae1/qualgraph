# Graph Report - analytify  (2026-04-28)

## Corpus Check
- 56 files · ~12,525 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 344 nodes · 813 edges · 16 communities detected
- Extraction: 54% EXTRACTED · 46% INFERRED · 0% AMBIGUOUS · INFERRED: 371 edges (avg confidence: 0.63)
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
- [[_COMMUNITY_Community 38|Community 38]]

## God Nodes (most connected - your core abstractions)
1. `AnnotatorResult` - 38 edges
2. `RunLogger` - 28 edges
3. `BaseAnnotator` - 28 edges
4. `OrderService` - 24 edges
5. `Order` - 23 edges
6. `Inventory` - 22 edges
7. `PricingEngine` - 20 edges
8. `run_pipeline()` - 16 edges
9. `_extract_classes_and_functions()` - 15 edges
10. `Customer` - 14 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `make_inventory()` --calls--> `Inventory`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\inventory.py
- `make_inventory()` --calls--> `Product`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\models.py
- `test_checkout_reserves_stock_and_sends_mail()` --calls--> `Mailer`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\orders.py
- `test_payment_decline_releases_stock()` --calls--> `PaymentGateway`  [INFERRED]
  benchmarks\repos\tiny_repo\tests\test_orders.py → benchmarks\repos\tiny_repo\tiny_shop\orders.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (42): ABC, BanditAnnotator, _finding_payload(), Bandit security annotator., _relative_to_repo(), AnnotatorResult, BaseAnnotator, Base interface for graph annotators. (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.1
Nodes (23): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., Mutate ``graph`` with this annotator's signal., Graph-aware code quality analysis for Python projects., _elapsed_ms(), LLMClient, LLMProvider (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (35): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), Definition, _docstring() (+27 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (30): annotate(), build(), main(), report(), _resolve_annotators(), annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs. (+22 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (19): _add_edge(), _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), Name-based cross-file graph resolution.  This resolver is deliberately conservat, resolve_calls(), _resolve_name() (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (3): Order, PricingEngine, customer_summary()

### Community 6 - "Community 6"
Cohesion: 0.16
Nodes (10): PipelineLogger, Sequential annotator pipeline., run_pipeline(), _stdlib_logger(), FailingAnnotator, GoodAnnotator, test_run_pipeline_times_successes_and_isolates_failures(), UnavailableAnnotator (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (5): Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Product

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (10): Enum, CustomerTier, LineItem, OrderStatus, Domain models for the tiny shop benchmark., Mailer, PaymentGateway, Order orchestration services. (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.47
Nodes (8): Customer, OrderService, make_inventory(), test_checkout_reports_missing_stock(), test_checkout_reserves_stock_and_sends_mail(), test_payment_decline_releases_stock(), test_pricing_combines_coupon_and_category_discount(), test_reports_summarize_categories_and_inventory()

### Community 10 - "Community 10"
Cohesion: 0.46
Nodes (1): Receipt

### Community 11 - "Community 11"
Cohesion: 0.5
Nodes (7): _build_location_index(), find_node_for_location(), nodes_for_file(), _normalize_path(), Helpers for mapping file/line findings back to graph nodes., Return the smallest graph node containing ``file_path:line``., _suffix_candidates()

### Community 12 - "Community 12"
Cohesion: 0.53
Nodes (5): inventory_health(), popular_categories(), Reporting helpers for the tiny shop benchmark., render_daily_digest(), revenue_by_country()

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **23 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (8 nodes): `.release_order()`, `.can_receive_promos()`, `.send()`, `.cancel()`, `.checkout()`, `.quote()`, `.ship()`, `Receipt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_graph()` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `RunLogger` connect `Community 1` to `Community 0`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `AnnotatorResult` connect `Community 0` to `Community 1`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `AnnotatorResult` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`AnnotatorResult` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Build a Python code graph and write an annotated graph artifact.`) actually correct?**
  _`RunLogger` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `BaseAnnotator` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`BaseAnnotator` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `OrderService` (e.g. with `Inventory` and `Customer`) actually correct?**
  _`OrderService` has 14 INFERRED edges - model-reasoned connections that need verification._