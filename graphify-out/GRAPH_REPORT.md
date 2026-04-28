# Graph Report - .  (2026-04-28)

## Corpus Check
- Corpus is ~0 words - fits in a single context window. You may not need a graph.

## Summary
- 92 nodes · 56 edges · 9 communities detected
- Extraction: 0% EXTRACTED · 100% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Annotator Plugins|Annotator Plugins]]
- [[_COMMUNITY_CLI & Pipeline Core|CLI & Pipeline Core]]
- [[_COMMUNITY_Graph Construction|Graph Construction]]
- [[_COMMUNITY_LLM Integration|LLM Integration]]
- [[_COMMUNITY_Reporting & Scoring|Reporting & Scoring]]
- [[_COMMUNITY_Project Documentation|Project Documentation]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]

## God Nodes (most connected - your core abstractions)
1. `Annotator Base Class` - 13 edges
2. `graph package` - 7 edges
3. `llm.client` - 5 edges
4. `Annotator Pipeline` - 4 edges
5. `graph.builder` - 4 edges
6. `graph.schema` - 4 edges
7. `llm.analyser` - 4 edges
8. `qualgraph CLI` - 3 edges
9. `Vulture Dead-Code Annotator` - 3 edges
10. `graph.metrics` - 3 edges

## Surprising Connections (you probably didn't know these)
- `README` --references--> `CHANGELOG`  [INFERRED]
  README.md → CHANGELOG.md
- `Bandit Security Annotator` --implements--> `Annotator Base Class`  [INFERRED]
  src/qualgraph/annotators/bandit.py → src/qualgraph/annotators/base.py
- `Bandit Security Annotator` --semantically_similar_to--> `pip-audit Annotator`  [INFERRED] [semantically similar]
  src/qualgraph/annotators/bandit.py → src/qualgraph/annotators/pip_audit.py
- `Coverage Annotator` --implements--> `Annotator Base Class`  [INFERRED]
  src/qualgraph/annotators/coverage.py → src/qualgraph/annotators/base.py
- `Co-Change Annotator` --implements--> `Annotator Base Class`  [INFERRED]
  src/qualgraph/annotators/co_change.py → src/qualgraph/annotators/base.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Annotator Plugins"
Cohesion: 0.22
Nodes (13): Bandit Security Annotator, Annotator Base Class, Co-Change Annotator, Coverage Annotator, Docstring Annotator, Git History Annotator, pip-audit Annotator, Profiler Annotator (+5 more)

### Community 1 - "CLI & Pipeline Core"
Cohesion: 0.25
Nodes (8): Annotator Pipeline, Cache Package Init, SQLite Cache Backend, qualgraph CLI, qualgraph Config, Cross-Signal Findings, Findings Data Model, qualgraph Logging

### Community 2 - "Graph Construction"
Cohesion: 0.43
Nodes (8): graph.builder, graph.clustering, graph package, graph.metrics, graph.parser, graph.resolver, graph.schema, graph.serialise

### Community 3 - "LLM Integration"
Cohesion: 0.39
Nodes (8): llm.analyser, llm.providers.anthropic, llm.client, llm.context, llm package, llm.providers.ollama, llm.providers.openai, llm.parser

### Community 4 - "Reporting & Scoring"
Cohesion: 0.5
Nodes (5): report.json_export, report.markdown, report package, scoring.risk, scoring package

### Community 5 - "Project Documentation"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): qualgraph Package Init

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (1): Annotators Package Init

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (1): Findings Package Init

## Knowledge Gaps
- **15 isolated node(s):** `qualgraph Config`, `qualgraph Logging`, `qualgraph Package Init`, `Docstring Annotator`, `Profiler Annotator` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Project Documentation`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `qualgraph Package Init`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `Annotators Package Init`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `Findings Package Init`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Annotator Base Class` connect `Annotator Plugins` to `CLI & Pipeline Core`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Annotator Pipeline` connect `CLI & Pipeline Core` to `Annotator Plugins`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `Annotator Base Class` (e.g. with `Bandit Security Annotator` and `Coverage Annotator`) actually correct?**
  _`Annotator Base Class` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `graph package` (e.g. with `graph.builder` and `graph.clustering`) actually correct?**
  _`graph package` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `llm.client` (e.g. with `llm package` and `llm.analyser`) actually correct?**
  _`llm.client` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Annotator Pipeline` (e.g. with `Annotator Base Class` and `SQLite Cache Backend`) actually correct?**
  _`Annotator Pipeline` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `graph.builder` (e.g. with `graph package` and `graph.parser`) actually correct?**
  _`graph.builder` has 4 INFERRED edges - model-reasoned connections that need verification._