# Graph Report - analytify  (2026-04-29)

## Corpus Check
- 62 files · ~20,281 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 601 nodes · 2063 edges · 18 communities detected
- Extraction: 39% EXTRACTED · 61% INFERRED · 0% AMBIGUOUS · INFERRED: 1258 edges (avg confidence: 0.6)
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
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]

## God Nodes (most connected - your core abstractions)
1. `RunLogger` - 73 edges
2. `TestLinkageAnnotator` - 50 edges
3. `CoChangeAnnotator` - 49 edges
4. `AnnotatorResult` - 48 edges
5. `DocstringAnnotator` - 48 edges
6. `RadonAnnotator` - 48 edges
7. `BanditAnnotator` - 46 edges
8. `CoverageAnnotator` - 46 edges
9. `PipAuditAnnotator` - 46 edges
10. `RuffAnnotator` - 46 edges

## Surprising Connections (you probably didn't know these)
- `RunLogger` --uses--> `Provider-agnostic LLM client with built-in cost/timing logging.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\llm\client.py
- `RunLogger` --uses--> `Base interface for graph annotators.`  [INFERRED]
  src\qualgraph\logging.py → src\qualgraph\annotators\base.py
- `parse_analysis_response()` --calls--> `test_parse_analysis_response_discards_findings_without_source_evidence()`  [INFERRED]
  src\qualgraph\llm\parser.py → tests\unit\test_llm_tasks.py
- `build()` --calls--> `RunLogger`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\logging.py
- `build()` --calls--> `build_graph()`  [INFERRED]
  src\qualgraph\cli.py → src\qualgraph\graph\builder.py

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
Cohesion: 0.2
Nodes (66): High-level LLM analysis entry points., Analyze the highest-risk nodes with cache-first, evidence-validated LLM calls., Anthropic LLM provider., BanditAnnotator, Mutate ``graph`` with this annotator's signal., BaseAnnotator, _DryRunProvider, _NoopCache (+58 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (46): ABC, _finding_payload(), Bandit security annotator., _relative_to_repo(), _severity_num(), AnnotatorResult, BaseAnnotator, Base interface for graph annotators. (+38 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (59): AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), parse_response() (+51 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (58): Git co-change annotator., _calls_from_node(), _calls_matching_package(), detect_complex_hotspots(), detect_cross_signal_findings(), detect_cyclic_dependencies(), detect_god_nodes(), detect_hidden_coupling() (+50 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (27): LLMAnalyzer, NodeAnalysisRequest, AnthropicProvider, _cost(), _message_text(), _system_blocks(), TokenPricing, _resolve_provider() (+19 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (32): annotate(), build(), _default_llm_task_dir(), _default_model(), llm_analyze(), llm_export_tasks(), llm_import_results(), main() (+24 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (40): _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), Definition, _docstring() (+32 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (31): _add_edge(), _module_node_for_file(), Git history annotator., _relative_to_target(), _target_prefix(), _add_vulnerable_import_edge(), _clear_imports_vulnerable_edges(), _ensure_dependency_node() (+23 more)

### Community 9 - "Community 9"
Cohesion: 0.26
Nodes (12): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _degree_centrality(), _is_pipeline_node(), _normalize(), _pagerank(), _percentile() (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.27
Nodes (8): cache_key(), normalized_function_body(), SQLite-backed content-addressed cache., Normalize source for cache identity without semantic reformatting., _strip_comments(), test_cache_key_uses_exact_ordered_fields(), test_normalized_function_body_can_strip_comments_without_black_formatting(), test_normalized_function_body_preserves_format_but_normalizes_line_endings_and_trailing_space()

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **34 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 11`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RunLogger` connect `Community 1` to `Community 2`, `Community 3`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `Cache` connect `Community 1` to `Community 10`, `Community 3`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `NodeType` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 5`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 66 inferred relationships involving `RunLogger` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`RunLogger` has 66 INFERRED edges - model-reasoned connections that need verification._
- **Are the 47 inferred relationships involving `TestLinkageAnnotator` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`TestLinkageAnnotator` has 47 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `CoChangeAnnotator` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`CoChangeAnnotator` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 46 inferred relationships involving `AnnotatorResult` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`AnnotatorResult` has 46 INFERRED edges - model-reasoned connections that need verification._