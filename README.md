Got it — that's a much cleaner framing. You want a serious personal project that you genuinely own (no academic constraints, no open-source obligations, no immediate monetization pressure), built in a way that *doesn't foreclose* the option of turning it into a paid tool down the road.

That's actually the freest position to be in. You're not optimizing for a writeup, not optimizing for community contributions, not optimizing for paying customers — just optimizing for "build the thing well, keep options open." Below is the spec rewritten for that framing.

A few things change versus the previous versions:

- **No academic framing or evaluation methodology** — you don't need RQs, baselines, or threats-to-validity sections.
- **No open-source attribution constraints driving design** — you're building from scratch (which we'd already settled on), not forking, so no MIT cleanup needed.
- **No commercial positioning yet** — no pricing tiers, no competitive battle cards, no SaaS infrastructure.
- **But: keep architectural decisions that don't burn future bridges** — clean separation of concerns, configurable everything, no licensing landmines, deployable as a CLI today and as a service tomorrow without a rewrite.

---

# qualgraph: project specification

*A graph-aware code quality analysis tool. Personal project, built from scratch, designed to remain extensible toward a paid product if the project warrants it.*

---

## 1. What this is

A command-line tool that analyzes a Python codebase and produces a ranked, multi-dimensional quality report. It builds a graph of the code, annotates the graph with signals from multiple sources (static analyzers, test coverage, git history, security scanners, optional runtime profilers), uses an LLM to reason about high-risk parts of the codebase with graph-aware context, and outputs findings — particularly cross-signal findings that single-tool analyzers can't produce.

The defining technical choice is that **everything sits on a shared graph**. Static metrics, lint findings, coverage data, git churn, security findings, and LLM analyses all annotate nodes and edges in the same NetworkX graph. This makes cross-signal reasoning natural and lets the LLM operate on focused subgraphs instead of dumping the whole codebase into context.

## 2. Why build it

Three observations motivate the work:

**LLMs can't actually analyze large codebases**, even with million-token windows. The "Lost in the Middle" effect degrades recall well before the limit, and most real codebases dwarf any context window anyway. Bigger windows aren't the answer; better context selection is.

**Existing static analyzers operate file-by-file.** They miss issues that depend on architectural relationships across files, and they produce noisy decontextualized findings. SonarQube, Pylint, Ruff, and Bandit all live in this regime.

**Modern AI code review tools have started building graph context layers** (Greptile, CodeRabbit, Bito), but they target PR-comment workflows, don't integrate runtime data, don't expose the graph to users, and don't combine signals across categories.

The interesting space is the integration: graph + static + tests + history + security + (optional) profiler + LLM, all on one shared structure. Building this well is non-trivial but not research-level hard, and the result is a tool that produces findings nothing else can.

## 3. Personal goals for the project

Worth being explicit about, since these shape priorities:

- **Build something real**. End-to-end working tool, used on actual codebases, producing findings that are actually useful. Not a prototype that demos well and falls apart on the second repo.
- **Own every line**. Built from scratch, no fork. You should be able to explain any architectural decision or any function in the codebase.
- **Keep optionality**. The choices you make now shouldn't preclude a future where this becomes a SaaS, or a paid CLI, or a hosted analysis service, or a GitHub App.
- **Quality over feature count**. A tool that does six things well beats a tool that does sixteen things badly. Cut features, don't cut polish.
- **Sustainable pace**. This is a personal project. You should still be enjoying it in month five, not slogging.

## 4. What the tool does, concretely

A user runs `qualgraph analyze ./my-repo` and gets back, after a few minutes:

- A Markdown report ranking the top 50 highest-risk parts of their codebase with specific findings and evidence
- A JSON dump of the annotated graph for programmatic use
- A `qualgraph.db` cache so subsequent runs are fast (only changed code re-analyzed)

The findings span four quality dimensions: **Maintainability** (complexity, smells, dead code, docs), **Reliability** (test coverage, untested hotspots, LLM-identified bugs), **Security** (SAST findings, vulnerable dependencies, secrets, vulnerable-import attribution), and **Performance** (optional, requires opt-in profiler run).

The headline features — the things that make the tool worth using over running Pylint + Ruff + Bandit separately — are the **cross-signal findings**:

- Untested hotspots: high complexity + high centrality + zero coverage = critical refactor priority
- Hidden coupling: files that change together on every commit but have no static dependency
- Vulnerable usage: pip-audit CVE attributed to the specific code locations that import the vulnerable package
- Outdated documentation: LLM detects docstring describing behavior the code no longer implements
- Architectural smells: god nodes, cyclic dependencies, layering violations detected via graph topology
- Performance gaps (if profiler enabled): hot path that is also complex and untested

These findings are surfaced because all the data lives on one graph. None of them can be produced by tools running independently.

## 5. Technical architecture

### 5.1 The pipeline

```
repo path
    │
    ▼
[Graph Builder]      ← Tree-sitter Python + NetworkX + Leiden clustering
    │
    ▼
graph (in memory + serializable to JSON)
    │
    ▼
[Annotator Pipeline] ← runs sequentially, each annotator mutates graph nodes/edges
    │
    ▼
annotated graph
    │
    ▼
[Risk Scorer]        ← weighted composite score per node, deterministic
    │
    ▼
top-N high-risk nodes
    │
    ▼
[LLM Analyzer]       ← per-node graph-aware context → structured findings
    │
    ▼
[Cross-Signal Detector] ← derived findings requiring multiple signals
    │
    ▼
[Report Generator]   ← Markdown + JSON
```

### 5.2 Graph schema

`NetworkX DiGraph`. Node types: `Module`, `Class`, `Function`, `Method`, `TestFunction`. Edge types: `calls`, `imports`, `inherits`, `tested_by`, `co_changes_with`, `imports_vulnerable`.

Each node carries attributes from each signal source (all optional, populated incrementally):

- Identity and source: id, type, name, qualified_name, file_path, line range, source code, docstring
- Structural: in/out-degree, betweenness, cluster_id, cluster_role
- Maintainability: complexity, MI, lint findings, dead-code flag, type coverage, doc coverage
- History: churn, author count, bug-fix-keyword count, last modified
- Reliability: line/branch coverage, test_count
- Security: SAST findings, vulnerable-import flags, secret findings
- Performance: cpu_pct, call_count, peak allocation (only if profiler ran)
- Semantic: LLM findings with severity, confidence, evidence
- Derived: composite risk score and component breakdown

### 5.3 Risk scoring

For each function node:

```
risk = w₁·centrality_norm
     + w₂·complexity_norm
     + w₃·churn_norm
     + w₄·(1 − coverage)
     + w₅·security_severity_max
     + w₆·llm_severity_max
     + w₇·hotpath_weight
```

All components normalized to [0, 1] by percentile rank within the repo. Weights configurable. The top-N (default 50) by composite risk go to the LLM. This is the cost-control lever — full-graph LLM analysis would cost too much and most nodes don't need it.

### 5.4 The annotators

Independent, each one a class implementing `BaseAnnotator.annotate(graph, repo_path)`. Listed in priority order — if you fall behind, drop the bottom ones first.

| Tier | Annotator | Source |
|---|---|---|
| Core | Radon | complexity, MI |
| Core | Ruff | lint findings |
| Core | Vulture | dead code |
| Core | Coverage | line/branch coverage from `coverage.py` |
| Core | TestLinkage | static + dynamic test-to-code edges |
| Core | GitHistory | churn, authors, bug-fix-keyword density |
| Core | Docstring | doc coverage, has_params, has_returns |
| Core | Bandit | Python SAST |
| Core | PipAudit | dependency CVEs |
| Important | CoChange | hidden coupling edges |
| Important | Secrets | detect-secrets |
| Important | TypeCoverage | mypy strict |
| Optional | Profiler | cProfile JSON ingestion |

### 5.5 The LLM layer

Provider-agnostic client wrapping Anthropic and OpenAI (and ideally a local Ollama option from day one, since you want optionality for a future "self-hosted, no data leaves your machine" pitch).

For each top-N node, build a structured context:

- Source code of the node
- All static metrics already on the node
- Source + metrics of immediate callers (up to 3) and callees (up to 5)
- Cluster description (size, role, dominant issues)
- Test status summary
- Git history summary (recently changed? bug-heavy?)
- Existing static findings on this node

The prompt asks for findings across four dimensions, each with severity, confidence (`EXTRACTED` / `INFERRED` / `AMBIGUOUS`), evidence citation, and a suggested action. The evidence-citation requirement is the primary anti-hallucination mechanism.

A separate, cheaper LLM use case: docstring consistency check — does this docstring still describe what this code does? Costs a fraction of the main analysis and produces a high-value finding category.

A third LLM use: cluster summarization — give each Leiden cluster a name and short description for the report. Cheap, runs once per cluster.

### 5.6 Caching

SQLite-backed, content-addressed, keyed by:

```
sha256(language_version + grammar_version + normalized_function_body +
       annotator_name + annotator_version + model_id + prompt_template_version)
```

Cache hit on a function unchanged across runs = zero cost. Anthropic's prompt caching (10% rate on cached reads) used for the system prompt and any repo-level context blocks.

### 5.7 Configuration

YAML config (`qualgraph.yaml`) covers: language list, exclude paths, enabled annotators, risk score weights, top-N selection, LLM provider/model/max-calls, output formats. Sensible defaults so that `qualgraph analyze ./my-repo` works without a config.

### 5.8 Output

Primary: a single Markdown report — executive summary, per-cluster sections, top-N risk nodes with full evidence trails, cross-signal findings section, per-dimension scorecards.

Secondary: a JSON graph dump for programmatic use, optional GraphML export.

### 5.9 CLI surface

```
qualgraph build <repo>      # build graph only, no analysis
qualgraph annotate <repo>   # run all annotators on existing graph
qualgraph llm <repo>        # run LLM analysis on top-N
qualgraph analyze <repo>    # full pipeline
qualgraph report <graph>    # regenerate report from saved graph
qualgraph diff <a> <b>      # compare quality between two graphs (placeholder for v2)
```

## 6. Design principles that protect future optionality

These are the decisions that matter for keeping the door open to a paid product later, without forcing commercial decisions now.

**Provider abstraction for LLMs.** The LLM client should be one interface with three implementations (Anthropic, OpenAI, Ollama). This costs little upfront and means a future "bring your own key" or "self-hosted, no data leaves your network" offering is a feature flag, not a rewrite.

**Stateless core, optional persistence.** The core analyzer takes a repo path and returns findings. Persistence (the cache, future "team dashboards", future "compare runs over time") is layered on top. This means today's CLI is also tomorrow's analysis worker behind a SaaS API, with no surgery.

**No telemetry by default, and clear license on what code goes where.** A future commercial deployment will want telemetry; a personal project should not collect it. Keep the boundary clean — telemetry is one optional module that can be flipped on later. Do not send any user code or analysis results anywhere except the LLM provider the user has explicitly configured.

**Don't pick a license yet.** As a personal project that's not open source, you don't need to. The repo is private. If and when you publish anything (a marketing site, a teaser, a first paid release), that's when the license decision happens. Keep the option open. The two natural paths later: fully closed-source SaaS, or "source available" with a non-commercial license (BSL, PolyForm) — both fine, both deferrable.

**Pin everything aggressively.** Version-pin every dependency in `pyproject.toml`. Version-pin tree-sitter grammars. Version-pin LLM model IDs in the cache key. Future-you debugging an analysis from six months ago will thank present-you.

**Build the test repos as fixtures.** Three repos at sizes 500 LOC, 5K LOC, 20K LOC. Use the small one as a regression-test fixture committed to the repo. Use the medium ones as your iteration targets. This is the difference between "tool that worked once on my laptop" and "tool that I trust to ship features on."

**Logs and artifacts on every run.** Every analysis run writes a structured log: which annotators ran, how long they took, how many LLM calls, total cost, errors and stack traces. This is invaluable for debugging and trivially graduates into product analytics later.

**Clean separation between graph, annotators, scorer, LLM, and report.** Each of these is its own module with a defined interface. You should be able to swap the report renderer (Markdown today, HTML tomorrow, dashboard the day after) without touching anything else. Same for the LLM module, the annotator pipeline, and the storage backend.

## 7. Scope

### 7.1 In scope (build now)

- Python codebases only
- CLI tool, runs locally on the user's machine
- All thirteen annotators listed in §5.4 except optionally the profiler
- Composite risk scorer with configurable weights
- LLM analysis on top-N nodes with three-provider support (Anthropic, OpenAI, Ollama)
- Cross-signal derived findings
- Markdown + JSON output
- SQLite cache
- Three test repos, with the smallest one used as a regression fixture
- Real use on at least three real codebases (yours or OSS) to validate findings

### 7.2 Out of scope for now (not forever)

- Other languages (architecture allows it; implementation is Python-only)
- Web dashboard or UI
- GitHub/GitLab App or PR commenting
- IDE plugin
- Multi-repo / monorepo aware analysis
- Real-time / continuous analysis
- Authentication, multi-user features, SSO
- Differential analysis between two graph snapshots (the `diff` CLI is a stub)
- Custom rule engine
- Telemetry, usage analytics, A/B testing
- Hosted SaaS infrastructure
- Pricing, billing, payment integration

### 7.3 Future-optionality items (don't build, but don't preclude)

These should be explicitly noted in the architecture so future-you knows they're considered:

- Multi-language: graph schema is language-agnostic; each language is a parser plugin + per-language annotator set
- Hosted version: the analyzer is already stateless and library-callable
- Privacy-preserving deployment: Ollama provider is in from day one, so a "self-hosted, no data leaves your network" pitch needs no new code
- Team features: team-level config, multi-repo views, dashboards — all layer on top of the existing JSON graph dump
- Differential analysis: the cache makes this almost free once the comparison logic is written
- IDE / CI integration: the CLI's exit codes and JSON output are the integration surface

## 8. Build phases

Twelve weeks at roughly 8-10 hours per week. Hard checkpoint at week 6 — if the pipeline isn't end-to-end on the small repo by then, cut scope.

**Weeks 1-2 — Core graph builder.** Project scaffolding, Tree-sitter Python parsing, function/class/call/import extraction, NetworkX graph, Leiden clustering, docstring and rationale-comment extraction, graph metrics, JSON serialization, `qualgraph build` CLI. Tested on tiny and small repos.

**Weeks 3-4 — Static annotators.** Annotator framework, Radon, Ruff, Vulture, mypy, Docstring. `qualgraph annotate` CLI.

**Weeks 5-6 — Test and history annotators.** Coverage, TestLinkage (with `tested_by` edges), GitHistory, CoChange. First derived finding: untested hotspot. **Hard checkpoint here**: end-to-end pipeline must produce a recognizable Markdown report for the small repo by end of week 6.

**Week 7 — Security annotators.** Bandit, PipAudit, Secrets. Vulnerable-import attribution as a derived finding.

**Weeks 8-9 — LLM layer.** Provider abstraction (Anthropic, OpenAI, Ollama), SQLite cache, prompt-caching support, cost telemetry, composite scorer, top-N selection, context builder, multi-dimension prompt template, response parsing into structured findings, docstring consistency check, cluster summarization. `qualgraph llm` CLI with `--max-llm-calls` and `--dry-run`.

**Week 10 — Optional profiler tier.** cProfile JSON ingestion, hot-path attribution, complex-hotspot derived finding. Cuttable if behind.

**Week 11 — Report generation and polish.** Jinja2 Markdown templates, executive summary, cluster sections, top-N risk-node sections with evidence trails, cross-signal findings section, per-dimension scorecards, JSON export, optional GraphML, progress bars, useful error messages.

**Week 12 — Validation, cleanup, and decision point.** Run end-to-end on three real codebases. Manually inspect 10-20 findings per repo, fix obvious issues, tune defaults. Decide whether the project is worth continuing — if yes, what direction. Possible directions documented in §10 below.

## 9. Risks and how to handle them

**LLM cost during development.** Use Haiku 4.5 (\$1/M input) for all dev work, switch to Sonnet 4.6 only for final validation runs. Aggressive caching means most iterations are free. Budget: $10/month is enough for active development.

**LLM hallucination in findings.** Confidence labels and evidence-citation requirement. Cross-signal corroboration before surfacing findings (don't let the LLM be the sole source of any finding flagged "high severity" — require a static signal to back it up).

**Tree-sitter call-graph accuracy.** Cross-file calls resolved by name matching are imperfect. Accept this in v1; flag in the README; Pyright-via-LSP enrichment is a future optionality item.

**Annotator integration breakage.** Each external tool's output format can change. Pin tool versions. Each annotator catches its own exceptions and logs but doesn't crash the pipeline.

**Scope creep into multi-language.** Strict Python-only for v1. Multi-language is a feature you sell later, not a feature you debug now.

**Burnout / loss of motivation.** This is the real risk on a personal project. Mitigations: ship something usable by week 6 even if it's narrow; use the tool on your own code so the dogfood loop motivates you; keep a CHANGELOG so you can see your own progress; don't compare yourself to teams of ten engineers.

**Falling behind schedule.** Cuttable scope, in order: profiler, GraphML export, mypy/type coverage, secrets, co-change, docstring consistency LLM call, cluster summarization. Cut from the bottom of this list as needed — the tool is still defensible without any of these.

## 10. Decision points after week 12

At the end of the 12 weeks, you have a working tool. The question becomes: what next? Three honest paths:

**Path A — Ship it as a small free tool.** Polish, write a README, make the repo public (with an appropriate license), put it on PyPI. Use it yourself, share it on Hacker News and r/Python, see what the response is. Low effort, high signal about whether anyone cares.

**Path B — Expand the tool.** Add TypeScript support. Add a web dashboard. Add GitHub App integration. Add differential analysis. Each of these is a multi-week project. Pick one based on what you actually wanted from the tool while using it.

**Path C — Pivot toward commercial.** Set up a landing page, take the existing tool and put it behind a CLI license check or a hosted analysis API, charge for it. This is real product-building work — pricing, packaging, payments, support, marketing, legal. Don't do this casually; do it because you talked to ten potential customers and they said they'd pay.

You don't need to decide now. The architectural choices in §6 protect all three paths. The decision happens after you've used the tool yourself for a month and have actual data on whether it's worth continuing in any direction.

## 11. What's not in this document

Deliberately deferred until they actually matter:

- Marketing copy, taglines, positioning statements
- Pricing model details
- Legal entity structure
- Trademark search for the name
- Domain registration
- Hosting / infrastructure design
- Customer development conversations
- Competitive analysis with depth
- Roadmap beyond v1

If and when path C becomes the active direction, all of these become urgent. Until then, they're distractions. Build the tool first.

---

This is the spec. It's intended to be feedable to an LLM with prompts like:

> "Generate the project structure and `pyproject.toml` for the qualgraph project specified above."

> "Generate the BaseAnnotator abstract class and the RadonAnnotator implementation specified in §5.4."

> "Generate the LLM prompt template for per-node quality analysis as specified in §5.5, using the structured context fields listed."

> "Generate a Jinja2 template for the Markdown report following the structure in §5.8."

The spec is detailed enough to constrain architectural decisions and leave only implementation specifics for the LLM to fill in.