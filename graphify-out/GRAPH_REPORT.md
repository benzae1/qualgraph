# Graph Report - analytify  (2026-04-29)

## Corpus Check
- 62 files · ~19,378 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 573 nodes · 1868 edges · 18 communities detected
- Extraction: 41% EXTRACTED · 59% INFERRED · 0% AMBIGUOUS · INFERRED: 1102 edges (avg confidence: 0.61)
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
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]

## God Nodes (most connected - your core abstractions)
1. `RunLogger` - 66 edges
2. `AnnotatorResult` - 44 edges
3. `TestLinkageAnnotator` - 43 edges
4. `CoChangeAnnotator` - 42 edges
5. `DocstringAnnotator` - 41 edges
6. `RadonAnnotator` - 41 edges
7. `BanditAnnotator` - 39 edges
8. `CoverageAnnotator` - 39 edges
9. `PipAuditAnnotator` - 39 edges
10. `RuffAnnotator` - 39 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `detect_untested_hotspots()` --calls--> `test_detect_untested_hotspots_combines_complexity_centrality_and_coverage()`  [INFERRED]
  src\qualgraph\findings\cross_signal.py → tests\unit\test_static_annotators.py
- `test_detect_hidden_coupling_requires_no_static_dependency_path()` --calls--> `detect_hidden_coupling()`  [INFERRED]
  tests\unit\test_static_annotators.py → src\qualgraph\findings\cross_signal.py
- `test_detect_vulnerable_usage_requires_vulnerable_import_and_matching_call()` --calls--> `detect_vulnerable_usage()`  [INFERRED]
  tests\unit\test_static_annotators.py → src\qualgraph\findings\cross_signal.py
- `test_detect_outdated_documentation_combines_docstring_llm_finding_and_churn()` --calls--> `detect_outdated_documentation()`  [INFERRED]
  tests\unit\test_static_annotators.py → src\qualgraph\findings\cross_signal.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (78): AnalysisSummary, LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., Analyze the highest-risk nodes with cache-first, evidence-validated LLM calls., AnthropicProvider, Anthropic LLM provider., TokenPricing (+70 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (81): analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), parse_response(), _severity_num() (+73 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (66): ABC, Bandit security annotator., AnnotatorResult, BaseAnnotator, Base interface for graph annotators., Check that the underlying tool is installed and runnable., Definition, Build a NetworkX code graph from Python source files.  The builder intentionally (+58 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (32): Enum, Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, CustomerTier, LineItem (+24 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (33): annotate(), build(), _default_llm_task_dir(), _default_model(), llm_analyze(), llm_export_tasks(), llm_import_results(), main() (+25 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (31): _rankdata(), Composite risk scoring for LLM candidate selection., Write composite risk scores onto function and method nodes., Return the highest-risk function/method nodes after scoring., score(), _severity_num(), top_risk_nodes(), node_attrs_to_graph() (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.16
Nodes (29): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), _docstring(), _extract_classes_and_functions() (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (12): _add_edge(), _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), resolve_calls(), _resolve_name(), edge_attrs_to_graph() (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.26
Nodes (12): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _degree_centrality(), _is_pipeline_node(), _normalize(), _pagerank(), _percentile() (+4 more)

### Community 9 - "Community 9"
Cohesion: 0.24
Nodes (7): normalized_function_body(), SQLite-backed content-addressed cache., Normalize source for cache identity without semantic reformatting., _strip_comments(), test_cache_get_put_round_trips_json_and_replaces_existing_value(), test_normalized_function_body_can_strip_comments_without_black_formatting(), test_normalized_function_body_preserves_format_but_normalizes_line_endings_and_trailing_space()

### Community 10 - "Community 10"
Cohesion: 0.47
Nodes (3): _cost(), _message_text(), _system_blocks()

### Community 11 - "Community 11"
Cohesion: 0.5
Nodes (2): _cached_input_tokens(), _cost()

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **33 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 11`** (5 nodes): `_cached_input_tokens()`, `_cost()`, `model_id()`, `.complete()`, `openai.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RunLogger` connect `Community 0` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `Cache` connect `Community 0` to `Community 9`, `Community 4`, `Community 1`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `AnnotatorResult` connect `Community 2` to `Community 0`, `Community 1`, `Community 7`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 59 inferred relationships involving `RunLogger` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`RunLogger` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `AnnotatorResult` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`AnnotatorResult` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 40 inferred relationships involving `TestLinkageAnnotator` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`TestLinkageAnnotator` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `CoChangeAnnotator` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`CoChangeAnnotator` has 38 INFERRED edges - model-reasoned connections that need verification._