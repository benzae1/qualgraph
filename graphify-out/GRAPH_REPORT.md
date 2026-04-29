# Graph Report - analytify  (2026-04-29)

## Corpus Check
- 62 files · ~21,148 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 634 nodes · 2286 edges · 17 communities detected
- Extraction: 37% EXTRACTED · 63% INFERRED · 0% AMBIGUOUS · INFERRED: 1436 edges (avg confidence: 0.59)
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
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]

## God Nodes (most connected - your core abstractions)
1. `RunLogger` - 82 edges
2. `TestLinkageAnnotator` - 59 edges
3. `CoChangeAnnotator` - 58 edges
4. `DocstringAnnotator` - 57 edges
5. `RadonAnnotator` - 57 edges
6. `BanditAnnotator` - 55 edges
7. `CoverageAnnotator` - 55 edges
8. `PipAuditAnnotator` - 55 edges
9. `RuffAnnotator` - 55 edges
10. `VultureAnnotator` - 55 edges

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
Nodes (80): build_context(), build_node_analysis_prompt(), evidence_corpus(), _node_summary(), Build graph-aware LLM prompts., render_analysis_prompt(), _template_env(), _truncate() (+72 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (53): ABC, _finding_payload(), Bandit security annotator., _relative_to_repo(), _severity_num(), AnnotatorResult, BaseAnnotator, Base interface for graph annotators. (+45 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (31): Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, CustomerTier, LineItem, Order (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.21
Nodes (74): High-level LLM analysis entry points., Analyze the highest-risk nodes with cache-first, evidence-validated LLM calls., Anthropic LLM provider., BanditAnnotator, Mutate ``graph`` with this annotator's signal., BaseAnnotator, _DryRunProvider, _NoopCache (+66 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (44): AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), LLMAnalyzer (+36 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (65): Definition, Build a NetworkX code graph from Python source files.  The builder intentionally, Git co-change annotator., _calls_from_node(), _calls_matching_package(), detect_complex_hotspots(), detect_cross_signal_findings(), detect_cyclic_dependencies() (+57 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (41): annotate(), build(), _default_llm_task_dir(), _default_model(), _echo_verbose_run(), export_json(), llm_analyze(), llm_export_tasks() (+33 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (30): _add_edge(), _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), _docstring() (+22 more)

### Community 8 - "Community 8"
Cohesion: 0.24
Nodes (11): _add_edge(), _candidate_names(), _dedupe(), _matches_suffix(), resolve_calls(), _resolve_name(), edge_attrs_to_graph(), _add_dynamic_context_edges() (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.26
Nodes (12): annotate_cluster_roles(), annotate_metrics(), _cluster_role(), _degree_centrality(), _is_pipeline_node(), _normalize(), _pagerank(), _percentile() (+4 more)

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **34 isolated node(s):** `Domain models for the tiny shop benchmark.`, `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RunLogger` connect `Community 3` to `Community 1`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `Cache` connect `Community 3` to `Community 0`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `NodeType` connect `Community 5` to `Community 0`, `Community 1`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 75 inferred relationships involving `RunLogger` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`RunLogger` has 75 INFERRED edges - model-reasoned connections that need verification._
- **Are the 56 inferred relationships involving `TestLinkageAnnotator` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`TestLinkageAnnotator` has 56 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `CoChangeAnnotator` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`CoChangeAnnotator` has 54 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `DocstringAnnotator` (e.g. with `_DryRunProvider` and `_NoopCache`) actually correct?**
  _`DocstringAnnotator` has 54 INFERRED edges - model-reasoned connections that need verification._