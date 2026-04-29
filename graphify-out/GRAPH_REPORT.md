# Graph Report - analytify  (2026-04-29)

## Corpus Check
- 58 files · ~16,569 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 455 nodes · 1184 edges · 17 communities detected
- Extraction: 52% EXTRACTED · 48% INFERRED · 0% AMBIGUOUS · INFERRED: 573 edges (avg confidence: 0.62)
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
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]

## God Nodes (most connected - your core abstractions)
1. `AnnotatorResult` - 41 edges
2. `RunLogger` - 38 edges
3. `BaseAnnotator` - 30 edges
4. `OrderService` - 24 edges
5. `Order` - 23 edges
6. `TestLinkageAnnotator` - 23 edges
7. `Inventory` - 22 edges
8. `CoChangeAnnotator` - 22 edges
9. `DocstringAnnotator` - 21 edges
10. `RadonAnnotator` - 21 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `NodeType` --uses--> `Composite risk scoring for LLM candidate selection.`  [INFERRED]
  src\qualgraph\graph\schema.py → src\qualgraph\scoring\risk.py
- `NodeType` --uses--> `Write composite risk scores onto function and method nodes.`  [INFERRED]
  src\qualgraph\graph\schema.py → src\qualgraph\scoring\risk.py
- `NodeType` --uses--> `Return the highest-risk function/method nodes after scoring.`  [INFERRED]
  src\qualgraph\graph\schema.py → src\qualgraph\scoring\risk.py

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
Nodes (31): Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, CustomerTier, LineItem, Order (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (60): _add_edge(), _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), Definition (+52 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (29): ABC, LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., AnthropicProvider, _cost(), _message_text(), Anthropic LLM provider. (+21 more)

### Community 3 - "Community 3"
Cohesion: 0.2
Nodes (31): BanditAnnotator, BaseAnnotator, Check that the underlying tool is installed and runnable., BaseAnnotator, main(), Command-line interface for qualgraph., Render a Markdown report from an annotated graph JSON file., Render a Markdown report from an annotated graph JSON file. (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (28): Mutate ``graph`` with this annotator's signal., annotate(), build(), Graph-aware code quality analysis for Python projects., _resolve_annotators(), annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs. (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (32): _co_change_lines(), _finding_code(), _finding_line(), _finding_records(), _format_score(), _format_small(), _git_history_lines(), _is_low_signal_finding() (+24 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (18): AnnotatorResult, Base interface for graph annotators., _has_tests(), Coverage.py annotator., _relative_to_repo(), AnnotatorPipeline, PipelineLogger, Sequential annotator pipeline. (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (21): _finding_payload(), Bandit security annotator., _relative_to_repo(), _severity_num(), add_finding(), clear_findings_by_source(), finding_key(), Helpers for attaching tool findings to graph nodes. (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (16): detect_untested_hotspots(), _percentile(), Cross-signal findings derived from the shared graph., Git history annotator., _relative_to_target(), _target_prefix(), Finding, Typed findings produced by derived and LLM analysis. (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.26
Nodes (12): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _degree_centrality(), _is_pipeline_node(), _normalize(), _pagerank(), _percentile() (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.31
Nodes (8): _rankdata(), Composite risk scoring for LLM candidate selection., Write composite risk scores onto function and method nodes., Return the highest-risk function/method nodes after scoring., score(), _severity_num(), top_risk_nodes(), test_risk_score_writes_weighted_components_for_llm_selection()

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **30 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 11`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RunLogger` connect `Community 4` to `Community 2`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `build_graph()` connect `Community 1` to `Community 8`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `AnnotatorResult` connect `Community 6` to `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `AnnotatorResult` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`AnnotatorResult` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Graph-aware code quality analysis for Python projects.`) actually correct?**
  _`RunLogger` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `BaseAnnotator` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`BaseAnnotator` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `str` (e.g. with `.checkout()` and `.__init__()`) actually correct?**
  _`str` has 22 INFERRED edges - model-reasoned connections that need verification._