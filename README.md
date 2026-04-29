# Qualgraph

Qualgraph is a local, graph-aware code quality analysis tool for Python repositories. It builds a code graph, annotates that graph with static analysis, tests, git history, security, and LLM-derived findings, then renders a risk-ranked report.

The central design choice is simple: **all signals live on the same graph**. Functions, methods, classes, modules, calls, imports, test links, vulnerable imports, coverage, churn, complexity, security findings, and LLM findings are all represented as node or edge attributes on one NetworkX graph. This makes cross-signal findings natural and gives LLMs focused graph context instead of a raw code dump.

This repository is a personal project built from scratch. The goal is a real local CLI that works on real codebases while preserving future optionality: paid CLI, hosted service, GitHub app, source-available product, or simply a useful private tool.

## Intended Outcome

A user should eventually be able to run a single workflow such as:

```powershell
qualgraph analyze .
```

or, through an agent skill:

```text
/qualgraph .
```

and receive:

- an annotated JSON graph
- a Markdown report
- risk-ranked code hotspots
- static analyzer findings
- coverage and test-linkage gaps
- git-history signals
- security findings
- cross-signal derived findings
- optional LLM findings, completed either through API providers or through an agent-file workflow that works with subscription LLM tools

## Why It Exists

LLMs are useful code reviewers, but they are poor at whole-repository analysis when handed too much unstructured context. Static analyzers are useful, but mostly file-local and noisy. Qualgraph sits between them:

1. Build a structural graph of the code.
2. Attach deterministic signals from local tools.
3. Score the graph to choose a small top-N set.
4. Ask an LLM only about focused, high-risk nodes.
5. Import structured LLM findings back into the graph.
6. Render one evidence-backed report.

The tool should produce findings that are hard to get from independent tools, for example:

- high-complexity, high-centrality functions with no tests
- vulnerable package imports attributed to the exact importing node
- hidden coupling from git co-change edges
- LLM findings grounded in code, metrics, neighbors, and existing findings
- risk scores that combine structure, complexity, churn, coverage, security, LLM, and hot-path signals

## Current Architecture

```text
repository
  |
  v
Graph Builder
  - Tree-sitter Python parser
  - NetworkX DiGraph
  - modules/classes/functions/methods/test functions
  - calls/imports/inherits edges
  |
  v
Graph Metrics and Clustering
  - centrality
  - in/out degree
  - Leiden clusters
  - cluster roles
  |
  v
Annotator Pipeline
  - each annotator mutates graph nodes or edges
  - failures are isolated
  |
  v
Risk Scorer
  - percentile-ranked components
  - top-risk function/method selection
  |
  v
LLM Task Layer
  - API providers: Anthropic, OpenAI, Ollama
  - agent-file workflow for subscription LLM users
  |
  v
Result Import and Report
  - findings attached to graph nodes
  - risk recomputed
  - Markdown report rendered
```

## Graph Schema

Qualgraph uses a `networkx.DiGraph`.

Node types:

- `Module`
- `Class`
- `Function`
- `Method`
- `TestFunction`
- dependency nodes added by security attribution

Edge types:

- `calls`
- `imports`
- `inherits`
- `tested_by`
- `co_changes_with`
- `imports_vulnerable`

Important node attributes:

- identity: `id`, `type`, `name`, `qualified_name`, `file_path`, `line_start`, `line_end`
- source: `source`, `docstring`
- structure: `centrality`, `betweenness_centrality`, `degree_centrality`, `pagerank`, `in_degree`, `out_degree`, `cluster_id`, `cluster_role`
- maintainability: `complexity`, `maintainability_index`
- reliability: `coverage_line`, `coverage_branch`
- history: `churn`, `author_count`, `bug_fix_keywords`
- findings: `findings`
- risk: `risk_score`, `risk_components`
- LLM: `llm_severity_max`
- future performance: `hotpath_weight`

## Implemented CLI Surface

```powershell
qualgraph build <repo> --output .qualgraph/graph.json
qualgraph annotate <repo> --graph .qualgraph/graph.json --output .qualgraph/annotated.graph.json --annotators radon,ruff,coverage,git,security
qualgraph report .qualgraph/annotated.graph.json --output .qualgraph/report.md
```

LLM agent-file workflow:

```powershell
qualgraph llm export-tasks .qualgraph/annotated.graph.json --limit 20
qualgraph llm import-results .qualgraph/runs/<run_id> --graph .qualgraph/annotated.graph.json --output .qualgraph/final.graph.json
qualgraph report .qualgraph/final.graph.json --output .qualgraph/report.md
```

API-backed LLM workflow:

```powershell
qualgraph llm analyze .qualgraph/annotated.graph.json --max-llm-calls 20 --provider ollama --dry-run
qualgraph llm analyze .qualgraph/annotated.graph.json --max-llm-calls 20 --provider openai --model gpt-4o-mini --output .qualgraph/final.graph.json
```

The intended future command is:

```powershell
qualgraph analyze <repo>
```

which should run the full build, annotate, score, LLM, import, and report pipeline.

## Annotators

Implemented or scaffolded annotators:

- `RadonAnnotator`: complexity and maintainability index
- `RuffAnnotator`: lint findings
- `VultureAnnotator`: dead-code findings
- `CoverageAnnotator`: line coverage from coverage.py
- `TestLinkageAnnotator`: `tested_by` edges from static calls and coverage contexts
- `GitHistoryAnnotator`: churn, author count, bug-fix keyword count
- `CoChangeAnnotator`: hidden-coupling edges from git co-change
- `DocstringAnnotator`: docstring presence metadata
- `BanditAnnotator`: Python security findings
- `PipAuditAnnotator`: vulnerable dependency findings and `imports_vulnerable` attribution
- `SecretsAnnotator`: conservative detect-secrets findings
- `CrossSignalAnnotator`: derived findings that combine graph structure, metrics, history, security, and LLM signals

Grouped annotator aliases:

- `coverage` runs coverage plus test linkage
- `git` runs git history plus co-change
- `security` runs Bandit, PipAudit, and Secrets
- `cross_signal` or `derived` runs cross-signal derived findings

## Cross-Signal Findings

Cross-signal findings exist because all inputs share graph nodes and edges.

Implemented:

- `detect_untested_hotspots(graph)`: high complexity + high centrality + zero line coverage
- `detect_hidden_coupling(graph)`: co-change edge with no calls/imports path
- `detect_vulnerable_usage(graph)`: vulnerable import plus a call to symbols from that package
- `detect_outdated_documentation(graph)`: docstring-consistency LLM finding on high-churn code
- `detect_god_nodes(graph)`: top-band centrality, complexity, and in/out degree
- `detect_cyclic_dependencies(graph)`: cycles in the calls subgraph

Planned:

- complex hot path: profiler hot path + complexity + weak tests

## Risk Scoring

Risk is written to function and method nodes:

```text
risk =
  w1 * centrality_percentile
  + w2 * complexity_percentile
  + w3 * churn_percentile
  + w4 * coverage_gap
  + w5 * security_severity_max
  + w6 * llm_severity_max
  + w7 * hotpath_weight
```

The scorer stores both:

- `risk_score`
- `risk_components`

The LLM layer should analyze only the top-N risk nodes. This gates API cost and keeps subscription-agent workflows manageable.

## LLM Provider Abstraction

The API-facing LLM layer uses:

- `LLMRequest`
- `LLMResponse`
- `LLMProvider`
- `LLMClient`

Providers:

- `AnthropicProvider`
- `OpenAIProvider`
- `OllamaProvider`

Telemetry:

- every LLM call writes to `.qualgraph/runs/<run_id>/llm_calls.jsonl`
- fields include node id, prompt template, model id, token counts, cached tokens, cost, and latency

Pricing is configurable in provider constructors. Ollama cost is always zero.

## Subscription LLM and Skill Workflow

Not every user has API access. Many users have subscription access through tools such as Codex, Claude Code, Cursor, or other agentic IDE tools. Qualgraph supports this through a **filesystem task protocol** rather than browser automation or copy-paste.

The workflow:

1. Qualgraph exports top-risk node tasks:

   ```text
   .qualgraph/runs/<run_id>/llm_tasks/
     manifest.json
     0001.some.node.md
     0002.other.node.md
   ```

2. An agent reads `manifest.json` and each task Markdown file.

3. The agent writes valid JSON results to:

   ```text
   .qualgraph/runs/<run_id>/llm_results/
     0001.json
     0002.json
   ```

4. Qualgraph imports those results, attaches them as `llm` findings, recomputes risk, and renders the final report.

This lets a subscription LLM session do the semantic analysis without requiring API keys and without asking the user to manually paste prompts into a web UI.

## Qualgraph Skill

The repository includes a repo-local skill scaffold:

```text
.agents/skills/qualgraph/SKILL.md
```

The intended skill behavior is:

1. Create or reuse `.venv`.
2. Build the graph.
3. Run annotators.
4. Export LLM task files.
5. Complete those task files using the current agent session.
6. Import LLM results.
7. Render `.qualgraph/report.md`.
8. Return the final report path and a concise summary.

This is the preferred user experience for subscription-LLM users:

```text
/qualgraph .
```

The user should not need to know the internal command sequence.

## SQLite Cache

The LLM cache is content-addressed and stored in SQLite.

Key fields, in exact order:

```text
language_version
grammar_version
normalized_function_body
annotator_name
annotator_version
model_id
prompt_template_version
```

`normalized_function_body`:

- normalizes line endings
- strips trailing whitespace
- strips trailing blank lines
- can optionally strip comments
- does not run Black or otherwise reformat code

The cache table:

```sql
CREATE TABLE IF NOT EXISTS llm_cache(
  key TEXT PRIMARY KEY,
  response_json TEXT NOT NULL,
  created_at TEXT NOT NULL
)
```

## Reports

The Markdown report currently includes:

- summary counts
- node type counts
- edge type counts
- top structural nodes
- findings by tool
- top finding rules
- priority findings
- risk hotspots
- coverage gaps
- test linkage summary
- git history summary
- co-change summary

Important note for agents: `qualgraph build` alone creates a sparse structural report. Findings, coverage, git, and security sections populate only after `qualgraph annotate` has run. LLM findings appear only after `llm export-tasks`, agent result completion, and `llm import-results`.

## Development Workflow

Use the local venv:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e . pytest
```

Run tests:

```powershell
$env:PYTHONPATH='src;benchmarks/repos/tiny_repo'
.venv\Scripts\python -m pytest
```

Check report generation:

```powershell
.venv\Scripts\qualgraph build benchmarks\repos\tiny_repo --output .qualgraph\dev.graph.json
.venv\Scripts\qualgraph report .qualgraph\dev.graph.json --output .qualgraph\dev.report.md
```

For full local analysis:

```powershell
.venv\Scripts\qualgraph build benchmarks\repos\tiny_repo --output .qualgraph\graph.json
.venv\Scripts\qualgraph annotate benchmarks\repos\tiny_repo --graph .qualgraph\graph.json --output .qualgraph\annotated.graph.json --annotators radon,ruff,coverage,git,security
.venv\Scripts\qualgraph llm export-tasks .qualgraph\annotated.graph.json --limit 20
```

Then complete task JSON files, import results, and render:

```powershell
.venv\Scripts\qualgraph llm import-results .qualgraph\runs\<run_id> --graph .qualgraph\annotated.graph.json --output .qualgraph\final.graph.json
.venv\Scripts\qualgraph report .qualgraph\final.graph.json --output .qualgraph\report.md
```

## Current Status

Implemented:

- graph builder
- parser and resolver
- metrics and clustering
- graph serialization
- annotator pipeline
- static annotators
- security annotators
- cross-signal untested hotspot detector
- risk scorer
- LLM provider abstraction
- LLM telemetry
- agent-file LLM workflow
- SQLite LLM cache
- API-backed LLM analyzer with `--max-llm-calls` and `--dry-run`
- Markdown report generation
- repo-local Qualgraph skill scaffold
- tiny benchmark repo and unit tests

Still planned or incomplete:

- single `qualgraph analyze` command
- richer final report sections and executive summary
- HTML report or dashboard
- profiler/hot-path annotator
- type coverage annotator
- cluster summarization
- docstring consistency LLM tasks
- differential analysis between graph snapshots
- multi-language support

## Design Principles

- Keep the graph as the source of truth.
- Keep annotators independent and failure-isolated.
- Keep LLM analysis top-N and evidence-based.
- Keep API providers optional.
- Keep subscription-LLM usage first-class through the agent-file workflow.
- Do not automate ChatGPT or Claude web UIs.
- Keep all user code local unless the user explicitly chooses an API provider.
- Make all run artifacts inspectable under `.qualgraph/`.
- Commit small vertical slices with tests.

## Instructions For Future Agents

When continuing this project:

1. Read this README first.
2. Read `AGENTS.md`.
3. Read `graphify-out/GRAPH_REPORT.md` before architecture or codebase questions.
4. Prefer `.qualgraph/` for generated analysis artifacts.
5. Use `.venv` for tests and CLI checks.
6. After code changes, run tests and verify report generation.
7. After code changes, run `graphify update .`.
8. Keep the subscription-friendly agent-file LLM workflow in mind for all LLM-related work.
9. Commit each completed change slice.

The intended product shape is not just a library. It is a local CLI plus an agent skill that can orchestrate the entire analysis and LLM-finding loop for users with or without API keys.
