# Architecture

Qualgraph is a local CLI plus an offline viewer. Its source of truth is a
NetworkX directed graph.

## Pipeline

```text
Python repository
  -> graph builder
  -> metrics and clustering
  -> annotator pipeline
  -> risk scoring
  -> optional LLM analysis
  -> Markdown report, JSON export, local viewer
```

## Graph

Primary node types:

- `Module`
- `Class`
- `Function`
- `Method`
- `TestFunction`
- dependency nodes for vulnerable imports

Primary edge types:

- `calls`
- `imports`
- `inherits`
- `tested_by`
- `co_changes_with`
- `imports_vulnerable`

Important attributes include source location, source snippet, docstring,
centrality, cluster id, complexity, coverage, churn, findings, and risk score.

## Annotators

Annotators mutate graph nodes and edges independently. Failures are isolated and
recorded in the run log.

Implemented annotators include Radon, Ruff, Vulture, coverage/test linkage, git
history, co-change, docstring metadata, Bandit, pip-audit, detect-secrets,
profiler ingestion, and cross-signal derived findings.

## Risk Scoring

Risk is attached to function and method nodes. The current model combines
centrality, complexity, churn, coverage gaps, security severity, LLM severity,
and profiler hot-path weight. Components are preserved so reports can explain
why a node ranked highly.

## Reports And Exports

The Markdown report is optimized for human review. The versioned JSON export is
the stable integration surface for future dashboards, IDE integrations, CI
checks, and hosted-product experiments.
