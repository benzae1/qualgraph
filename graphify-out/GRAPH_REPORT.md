# Graph Report - analytify  (2026-04-28)

## Corpus Check
- 46 files · ~5,106 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 109 nodes · 122 edges · 7 communities detected
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `RunLogger` - 18 edges
2. `LLMAnalyzer` - 7 edges
3. `LLMClient` - 7 edges
4. `BaseAnnotator` - 6 edges
5. `LLMRequest` - 6 edges
6. `_error_record()` - 5 edges
7. `AnnotatorPipeline` - 5 edges
8. `LLMResponse` - 5 edges
9. `utc_now_iso()` - 4 edges
10. `span()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Base interface for graph annotators.` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\annotators\base.py → src\qualgraph\logging.py
- `Provider-agnostic LLM client with built-in cost/timing logging.` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\llm\client.py → src\qualgraph\logging.py
- `AnnotatorResult` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\annotators\base.py → src\qualgraph\logging.py
- `BaseAnnotator` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\annotators\base.py → src\qualgraph\logging.py
- `Mutate ``graph`` with this annotator's signal.` --uses--> `RunLogger`  [INFERRED]
  src\qualgraph\annotators\base.py → src\qualgraph\logging.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.25
Nodes (8): LLMAnalyzer, NodeAnalysisRequest, High-level LLM analysis entry points., _elapsed_ms(), LLMClient, LLMRequest, LLMResponse, Provider-agnostic LLM client with built-in cost/timing logging.

### Community 1 - "Community 1"
Cohesion: 0.26
Nodes (9): _elapsed_ms(), _error_record(), _json_safe(), LLMUsage, Structured run logging for qualgraph.  Every CLI run should create a JSONL event, RunSummary, span(), utc_now_iso() (+1 more)

### Community 2 - "Community 2"
Cohesion: 0.23
Nodes (9): ABC, annotate(), AnnotatorResult, BaseAnnotator, _count_delta(), _elapsed_ms(), Base interface for graph annotators., _result_counts() (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.21
Nodes (10): Enum, coerce_edge_type(), coerce_node_type(), EdgeAttrs, EdgeType, make_node_id(), NodeAttrs, NodeType (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (5): Mutate ``graph`` with this annotator's signal., Write structured JSONL events and aggregate per-run counters., RunLogger, AnnotatorPipeline, Sequential annotator pipeline.

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (2): LLMProvider, Protocol

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

## Knowledge Gaps
- **10 isolated node(s):** `LLMUsage`, `Structured run logging for qualgraph.  Every CLI run should create a JSONL event`, `Write structured JSONL events and aggregate per-run counters.`, `Mutate ``graph`` with this annotator's signal.`, `NodeAttrs` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 5`** (3 nodes): `LLMProvider`, `.complete()`, `Protocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 6`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RunLogger` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 5`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Why does `LLMClient` connect `Community 0` to `Community 4`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `_error_record()` connect `Community 1` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `RunLogger` (e.g. with `AnnotatorResult` and `BaseAnnotator`) actually correct?**
  _`RunLogger` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LLMAnalyzer` (e.g. with `LLMClient` and `LLMRequest`) actually correct?**
  _`LLMAnalyzer` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `LLMClient` (e.g. with `NodeAnalysisRequest` and `LLMAnalyzer`) actually correct?**
  _`LLMClient` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `BaseAnnotator` (e.g. with `RunLogger` and `AnnotatorPipeline`) actually correct?**
  _`BaseAnnotator` has 3 INFERRED edges - model-reasoned connections that need verification._