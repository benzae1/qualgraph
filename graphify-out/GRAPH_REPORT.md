# Graph Report - analytify  (2026-04-29)

## Corpus Check
- 61 files · ~16,887 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 504 nodes · 1410 edges · 18 communities detected
- Extraction: 47% EXTRACTED · 53% INFERRED · 0% AMBIGUOUS · INFERRED: 742 edges (avg confidence: 0.63)
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
1. `RunLogger` - 44 edges
2. `AnnotatorResult` - 41 edges
3. `BaseAnnotator` - 30 edges
4. `TestLinkageAnnotator` - 29 edges
5. `CoChangeAnnotator` - 28 edges
6. `DocstringAnnotator` - 27 edges
7. `RadonAnnotator` - 27 edges
8. `BanditAnnotator` - 25 edges
9. `CoverageAnnotator` - 25 edges
10. `PipAuditAnnotator` - 25 edges

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
Nodes (59): build_context(), build_node_analysis_prompt(), evidence_corpus(), _node_summary(), Build graph-aware LLM prompts., render_analysis_prompt(), _template_env(), _truncate() (+51 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (29): ABC, LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., AnthropicProvider, _cost(), _message_text(), Anthropic LLM provider. (+21 more)

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (37): BanditAnnotator, BaseAnnotator, Mutate ``graph`` with this annotator's signal., Check that the underlying tool is installed and runnable., BaseAnnotator, Command-line interface for qualgraph., Render a Markdown report from an annotated graph JSON file., Render a Markdown report from an annotated graph JSON file. (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (29): annotate(), build(), _default_llm_task_dir(), llm_export_tasks(), llm_import_results(), main(), report(), _resolve_annotators() (+21 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (20): AnnotatorResult, Base interface for graph annotators., _has_tests(), Coverage.py annotator., _relative_to_repo(), Docstring coverage annotator., _strip_docstring_quotes(), AnnotatorPipeline (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (29): Definition, Build a NetworkX code graph from Python source files.  The builder intentionally, _module_node_for_file(), Git co-change annotator., Enum, Git history annotator., _relative_to_target(), _target_prefix() (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (31): _add_edge(), _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), _docstring() (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (21): _finding_payload(), Bandit security annotator., _relative_to_repo(), _severity_num(), add_finding(), clear_findings_by_source(), finding_key(), Helpers for attaching tool findings to graph nodes. (+13 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (18): detect_untested_hotspots(), _percentile(), Cross-signal findings derived from the shared graph., Finding, Typed findings produced by derived and LLM analysis., node_attrs_to_graph(), NodeAttrs, _node() (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (10): Cache, cache_key(), normalized_function_body(), SQLite-backed content-addressed cache., Normalize source for cache identity without semantic reformatting., _strip_comments(), test_cache_get_put_round_trips_json_and_replaces_existing_value(), test_cache_key_uses_exact_ordered_fields() (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.26
Nodes (12): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _degree_centrality(), _is_pipeline_node(), _normalize(), _pagerank(), _percentile() (+4 more)

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

- **Why does `RunLogger` connect `Community 3` to `Community 2`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `AnnotatorResult` connect `Community 5` to `Community 8`, `Community 1`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `LLMResponse` connect `Community 2` to `Community 3`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `RunLogger` (e.g. with `Command-line interface for qualgraph.` and `Graph-aware code quality analysis for Python projects.`) actually correct?**
  _`RunLogger` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `AnnotatorResult` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`AnnotatorResult` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `str` (e.g. with `.checkout()` and `.__init__()`) actually correct?**
  _`str` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `BaseAnnotator` (e.g. with `BanditAnnotator` and `Bandit security annotator.`) actually correct?**
  _`BaseAnnotator` has 27 INFERRED edges - model-reasoned connections that need verification._