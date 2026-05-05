# Qualgraph

[![CI](https://github.com/benzae1/analytify/actions/workflows/ci.yml/badge.svg)](https://github.com/benzae1/analytify/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Release](https://img.shields.io/github/v/release/benzae1/analytify?include_prereleases)

Qualgraph is a local, graph-aware code quality analyzer for Python repositories.
It builds a code graph, annotates it with quality signals, ranks risky code, and
renders a Markdown report plus an offline web viewer.

The core idea is that structure, static analysis, coverage, git history,
security findings, profiler data, and optional LLM findings all live on the same
NetworkX graph. That makes cross-signal findings possible, such as complex code
with weak tests, hidden git co-change coupling, and risky vulnerable imports.

## Quickstart

Until the package is published to PyPI, install from the repository:

```bash
python -m pip install "git+https://github.com/benzae1/analytify.git"
```

For local development:

```bash
git clone https://github.com/benzae1/analytify.git
cd analytify
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
git clone https://github.com/benzae1/analytify.git
cd analytify
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
```

Run the full local workflow on the bundled tiny benchmark repository:

```bash
qualgraph analyze benchmarks/repos/tiny_repo --preset fast --coverage-mode skip --top-n 5
```

This writes:

- `.qualgraph/graph.json`
- `.qualgraph/annotated.graph.json`
- `.qualgraph/report.md`
- `.qualgraph/export.json`
- `.qualgraph/runs/<run_id>/run_summary.json`

Open the local viewer:

```bash
qualgraph serve .qualgraph/annotated.graph.json --open
```

`python -m qualgraph --help` works too.

## CLI

The one-command path is:

```bash
qualgraph analyze <repo> --preset standard
```

Useful focused commands:

```bash
qualgraph build <repo> --output .qualgraph/graph.json
qualgraph annotate <repo> --graph .qualgraph/graph.json --output .qualgraph/annotated.graph.json --annotators full
qualgraph report .qualgraph/annotated.graph.json --output .qualgraph/report.md
qualgraph export-json .qualgraph/annotated.graph.json --output .qualgraph/export.json
qualgraph serve .qualgraph/annotated.graph.json --open
```

Presets:

- `fast`: radon, ruff, docstring, and cross-signal findings.
- `standard`: fast plus git history and co-change.
- `full`: standard plus vulture, coverage/test linkage, and security tools.

If `.qualgraph/runs` is not writable, pass a run-log directory:

```bash
qualgraph analyze . --artifacts-dir /tmp/qualgraph-runs
```

or set `QUALGRAPH_ARTIFACTS_DIR`.

## LLM Workflows

Qualgraph does not require API keys. The subscription-friendly workflow exports
focused task files for an agent to complete:

```bash
qualgraph llm export-tasks .qualgraph/annotated.graph.json --limit 20
qualgraph llm import-results .qualgraph/runs/<run_id> --graph .qualgraph/annotated.graph.json --output .qualgraph/final.graph.json
qualgraph report .qualgraph/final.graph.json --output .qualgraph/report.md
```

API-backed analysis is available for OpenAI, Anthropic, and local Ollama:

```bash
qualgraph llm analyze .qualgraph/annotated.graph.json --provider ollama --dry-run
qualgraph llm analyze .qualgraph/annotated.graph.json --provider openai --model gpt-4o-mini
```

User code stays local unless you explicitly choose an API provider.

## Documentation

- [Installation](docs/installation.md)
- [CLI Reference](docs/cli.md)
- [Configuration](docs/configuration.md)
- [Viewer](docs/viewer.md)
- [LLM Workflows](docs/llm-workflows.md)
- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## Development

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
python -m build
python -m twine check dist/*
```

Viewer browser checks require Chromium:

```bash
python -m playwright install chromium
python -m pytest tests/e2e -q
```

After code changes in this repository, run:

```bash
graphify update .
```

## Status

Qualgraph is alpha software. The public interface is useful, but the graph
schema and scoring model may still evolve before a stable 1.0 release.
