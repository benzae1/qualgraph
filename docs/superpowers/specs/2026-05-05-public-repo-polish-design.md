# Qualgraph Public Repo Polish — Design Spec
Date: 2026-05-05

## Overview

Polish Qualgraph for a public-quality open-source release. Four workstreams executed sequentially:

1. **Packaging & CLI** — rename package, add `qualgraph analyze`, clean pyproject.toml
2. **Documentation** — full README rewrite, new `docs/` directory, surface files
3. **Viewer polish** — encoding fix, responsive layout, error states, `/api/health`, unit tests
4. **CI/CD** — `ci.yml`, `release.yml`, Dependabot

## Constraints & Decisions

- Product name: **Qualgraph**; package name: `qualgraph`; GitHub remote stays `benzae1/analytify` until renamed
- Order: Packaging → Docs → Viewer → CI/CD (user-facing first)
- `qualgraph analyze`: full implementation (all flags)
- Playwright: skipped; visual fixes verified manually; API/overflow logic unit-tested
- Release workflow: full with PyPI publish gated behind `vars.PUBLISH_TO_PYPI`
- README: full rewrite; architecture detail moved to `docs/`
- LLM docs: maximally detailed — primary differentiator for potential users

---

## Workstream 1: Packaging & CLI

### pyproject.toml

Replace current `analytify` project metadata with:

```toml
[project]
name = "qualgraph"
version = "0.1.0"
description = "Local, graph-aware code quality analysis for Python repositories"
readme = "README.md"
license = {text = "MIT"}
authors = [{name = "Anton Benz", email = "anton.erdmann.benz@uni-weimar.de"}]
requires-python = ">=3.11"
keywords = ["code-quality", "static-analysis", "graph", "llm", "python"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Quality Assurance",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "https://github.com/benzae1/analytify"
Documentation = "https://github.com/benzae1/analytify/tree/main/docs"
"Bug Tracker" = "https://github.com/benzae1/analytify/issues"

[project.optional-dependencies]
dev = ["pytest", "ruff", "build", "twine"]

[project.scripts]
qualgraph = "qualgraph.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Remove the `analytify` console script entry.

### `src/qualgraph/__main__.py`

```python
from qualgraph.cli import app
app()
```

Enables `python -m qualgraph`.

### `qualgraph analyze <repo>` command

New Typer command in `cli.py`. Orchestrates:
1. `build` — graph construction (tree-sitter parser)
2. `annotate` — annotator pipeline filtered by preset
3. `report` — markdown report
4. `export-json` — JSON artifact

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--preset` | enum | `standard` | `fast`, `standard`, or `full` |
| `--coverage-mode` | bool | False | Pass through to coverage annotator |
| `--top-n` | int | 10 | Top-N nodes for report/LLM |
| `--serve` | bool | False | Start viewer after completion |
| `--open` | bool | False | Open browser automatically |
| `--artifacts-dir` | path | `.qualgraph/` | Override output directory |

`QUALGRAPH_ARTIFACTS_DIR` env var also overrides the artifacts directory. If the directory is unwritable, print a clear error and exit non-zero instead of raising a traceback.

**Preset annotator sets:**

| Preset | Annotators |
|--------|-----------|
| `fast` | radon, ruff, vulture |
| `standard` | fast + git_history, coverage, test_linkage, cross_signal |
| `full` | all annotators: standard + bandit, pip_audit, secrets, profiler |

**Output layout under `--artifacts-dir`:**

```
.qualgraph/
├── graph.json          # exported graph
├── report.md           # markdown report
├── cache.sqlite        # LLM result cache
└── runs/               # per-run logs
```

---

## Workstream 2: Documentation

### README.md — full rewrite

Sections in order:

1. **Hero** — one-line pitch + badges (CI, Python 3.11+, MIT license, GitHub release; PyPI once published)
2. **What Qualgraph does** — 3–4 sentence description + bullet list of all signals (complexity, linting, dead code, coverage, git churn, security, LLM insights)
3. **Quickstart** — `pip install qualgraph` → `qualgraph analyze <repo> --preset fast` → open viewer; runnable in under 60 seconds
4. **Installation** — from PyPI, from source (`pip install -e ".[dev]"`), dev setup steps
5. **CLI reference** — `analyze`, `build`, `annotate`, `report`, `serve`; flags table for each
6. **Viewer** — what it shows, how to launch (`qualgraph serve`), screenshot placeholder
7. **LLM workflows** — agent-file (no key) vs. API-backed; cost gating; cache behaviour; practical examples
8. **Privacy & locality** — all code stays local unless user opts into an API provider; no telemetry
9. **Output artifacts** — `.qualgraph/` directory layout, what each file is for
10. **Troubleshooting** — top 5 failure modes with diagnostic steps and fixes
11. **Development** — clone, `pip install -e ".[dev]"`, `pytest`, `ruff check .`, `graphify update .`
12. **License** — MIT

### `docs/` directory (new)

| File | Content |
|------|---------|
| `docs/architecture.md` | Graph design, annotator pipeline, risk formula, signal list, node/edge schema — moved from current README |
| `docs/installation.md` | Detailed install scenarios: venv, pipx, Windows path setup, tree-sitter native dependency notes |
| `docs/configuration.md` | `qualgraph.yaml` full key reference with types, defaults, and examples |
| `docs/cli.md` | Full CLI reference with runnable examples for every command and flag |
| `docs/viewer.md` | Viewer features, all API endpoints, keyboard navigation, `/api/health` |
| `docs/llm-workflows.md` | See detailed spec below |

### `docs/llm-workflows.md` — detailed spec

This is the most important doc for potential users. Cover:

**Agent-file workflow (no API key required):**
1. Run `qualgraph analyze <repo> --preset standard` to build graph and score nodes
2. Run `qualgraph llm export-tasks` — exports a `tasks.md` file with one task per high-risk node
3. Paste `tasks.md` into any LLM chat (Claude, GPT-4, Gemini, local models via copy-paste)
4. The LLM returns structured findings; save as `tasks.results.md`
5. Run `qualgraph llm import-results tasks.results.md` — findings are merged back into the graph
6. Run `qualgraph report` to regenerate the report with LLM findings included

Include: example `tasks.md` snippet, example LLM response, example import command, example report section showing LLM finding.

**API-backed workflow:**
1. Set provider: `ANTHROPIC_API_KEY=...` or `OPENAI_API_KEY=...`
2. Run `qualgraph llm analyze --provider anthropic --model claude-sonnet-4-6 --top-n 10`
3. Cost is estimated before API calls; user confirms
4. Results cached in `cache.sqlite` — re-running with same graph and prompt costs nothing
5. Use `--dry-run` to see what would be sent without spending tokens

**Ollama (local models):**
- `ollama pull llama3`
- `qualgraph llm analyze --provider ollama --model llama3`
- No API key, no cost, fully local

**What the LLM sees:** show example context block — function signature, docstring, complexity score, callers, test linkage, git churn, security findings. Explain that the graph shapes what context is sent (callers, callees, cluster neighbours).

**How to use the JSON export with LLMs:**
- `qualgraph export-json` → `.qualgraph/graph.json`
- Load the JSON into an LLM context (via file upload or API file param)
- Example prompt: "Here is a code quality graph for my Python repo. Which functions have the highest risk and why? Focus on nodes with high churn and low coverage."
- The JSON schema is documented; each node has `risk_score`, `complexity`, `coverage`, `churn`, `findings` fields

**Cache behaviour:**
- All API results cached by content hash of (prompt, code context, model)
- Identical nodes across multiple runs never re-queried
- Cache location: `.qualgraph/cache.sqlite`
- Clear with `qualgraph cache clear`

### Surface files

| File | Content |
|------|---------|
| `qualgraph.yaml.example` | Every config key filled with realistic example + inline comment |
| `CHANGELOG.md` | Keep a Changelog format; `## [Unreleased]` lists this polish pass |
| `CONTRIBUTING.md` | Setup, branching, commit style, how to add an annotator, PR checklist |
| `SECURITY.md` | Supported versions table, report-a-vulnerability instructions (private email) |
| `LICENSE` | MIT, current year, author name |

---

## Workstream 3: Viewer Polish

### Encoding fix

Root cause: HTTP response `Content-Type` header missing `charset=utf-8`, causing browsers to misinterpret multi-byte characters. Fix: set `Content-Type: text/html; charset=utf-8` on all HTML responses in `server.py`. Audit HTML templates for any literal non-ASCII characters and replace with HTML entities or ensure source files are saved as UTF-8.

### Responsive layout

Add CSS breakpoints:
- **≤768px (tablet):** sidebar stacks below graph panel; font sizes reduce slightly
- **≤480px (mobile):** single-column layout; graph panel height capped

Overflow fixes applied globally:
- `overflow-wrap: break-word` on node names, qualified names, file paths
- `max-width: 100%` on badges and images
- `overflow-x: auto` on code blocks and findings tables

### Empty / loading / error states

- **Loading:** spinner shown while `/api/graph` is in-flight
- **Empty:** "No nodes to display. Run `qualgraph build <repo>` first." if graph returns 0 nodes
- **Error:** friendly heading + raw error in a collapsed `<details>` block if `/api/graph` returns non-200

### Keyboard & accessibility

- Visible focus rings (`outline: 2px solid #4f46e5`) on all buttons, links, and list items
- `aria-label` on icon-only buttons
- Tooltips via `title` attribute on all control buttons

### `/api/health` endpoint

```json
GET /api/health
{"status": "ok", "graph_loaded": true}
```

Returns 200 always; `graph_loaded` reflects whether the graph file parsed successfully.

### Error messages in `qualgraph serve`

- Missing graph file: `"Graph file not found at '{path}'. Run 'qualgraph build <repo>' first."`
- Port occupied: `"Port {port} is already in use. Try '--port <other-port>'."`

### Unit tests added

- `tests/unit/test_viewer_server.py` additions:
  - `/api/health` returns 200 with `{"status": "ok", "graph_loaded": bool}`
  - `/api/health` returns `graph_loaded: false` when no graph file present
  - Long node name (>80 chars) does not cause `overflow-x` scroll (assert rendered HTML has `overflow-wrap: break-word` style)
  - Port conflict raises `SystemExit` with message containing "already in use"
  - Missing graph file raises `SystemExit` with message containing "not found"

---

## Workstream 4: CI/CD

### `.github/workflows/ci.yml`

Triggers: `push` and `pull_request` to `main`.

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
```

Steps:
1. `actions/checkout@v4`
2. `actions/setup-python@v5` with matrix version
3. `pip install -e ".[dev]"`
4. `pip check`
5. `ruff check .`
6. `pytest tests/`
7. `python -m build`
8. Wheel smoke: create fresh venv, install built wheel, run `qualgraph --help`
9. CLI smoke: `qualgraph analyze benchmarks/repos/tiny_repo --preset fast --top-n 3`
10. Assert `.qualgraph/report.md` exists
11. Assert `.qualgraph/graph.json` exists
12. Viewer smoke: start `qualgraph serve &`, `curl /api/health`, assert `"status":"ok"`

### `.github/workflows/release.yml`

Triggers: push of `v*` tags.

Steps:
1. Checkout + Python 3.12 setup
2. `pip install build twine`
3. `python -m build`
4. `twine check dist/*`
5. Upload `dist/` as Actions artifact
6. Create GitHub Release via `softprops/action-gh-release@v2`, attach dist files
7. PyPI publish via `pypa/gh-action-pypi-publish@release/v1` — gated: `if: vars.PUBLISH_TO_PYPI == 'true'`

### `.github/dependabot.yml`

- Weekly updates for GitHub Actions (`/` directory)
- Weekly updates for pip (`/` directory)

### Action version policy

Use current stable versions as of 2026-05-05:
- `actions/checkout@v4`
- `actions/setup-python@v5`
- `softprops/action-gh-release@v2`
- `pypa/gh-action-pypi-publish@release/v1`

Dependabot will keep these current.

---

## Test Plan

### Clean install verification
```bash
python -m venv .venv-test
.venv-test/Scripts/pip install -e ".[dev]"
qualgraph --help
python -m qualgraph --help
qualgraph analyze benchmarks/repos/tiny_repo --preset fast --top-n 5
```

### Package verification
```bash
python -m build
twine check dist/*
# Install wheel in fresh venv
python -m venv .venv-wheel
.venv-wheel/Scripts/pip install dist/qualgraph-0.1.0-py3-none-any.whl
.venv-wheel/Scripts/qualgraph --help
```

### Runtime verification
```bash
pytest
ruff check .
pip check
```

### Viewer API smoke
```bash
qualgraph serve &
curl http://localhost:8080/api/health
# expect: {"status": "ok", "graph_loaded": true}
```

---

## Out of Scope

- Playwright visual tests (deferred)
- HTML report / dashboard (future workstream)
- Type coverage annotator (scaffolded, not implemented)
- Cluster summarization LLM tasks
- Differential analysis between snapshots
- Multi-language support
- GitHub repo rename from `analytify` to `qualgraph`
