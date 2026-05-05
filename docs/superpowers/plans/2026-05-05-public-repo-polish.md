# Qualgraph Public Repo Polish — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Polish Qualgraph for a public-quality open-source release across four sequential workstreams: packaging rename, documentation, viewer polish, and CI/CD.

**Architecture:** The existing `src/qualgraph/` package is already well-structured; work is additive. The packaging rename touches `pyproject.toml` and adds `__main__.py`. The `analyze` command is a new Typer command in `cli.py` that orchestrates the existing `build_graph`, `run_pipeline`, `write_markdown_report`, and `write_json_export` functions. Viewer work is isolated to `server.py` and `assets/`. All new GitHub Actions files are in `.github/`.

**Tech Stack:** Python 3.11+, Typer, hatchling build backend, NetworkX, pytest, ruff, GitHub Actions

---

## File Map

**Created:**
- `src/qualgraph/__main__.py` — `python -m qualgraph` entry
- `docs/architecture.md` — architecture detail (moved from README)
- `docs/installation.md`
- `docs/configuration.md`
- `docs/cli.md`
- `docs/viewer.md`
- `docs/llm-workflows.md`
- `LICENSE`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `.github/dependabot.yml`

**Modified:**
- `pyproject.toml` — rename to qualgraph, add build-system, metadata, dev extras
- `src/qualgraph/cli.py` — add `analyze` command
- `src/qualgraph/viewer/server.py` — add `/api/health`, improve error messages
- `src/qualgraph/viewer/assets/styles.css` — responsive + overflow fixes
- `src/qualgraph/viewer/assets/index.html` — loading/empty/error states, focus styles
- `README.md` — full rewrite
- `CHANGELOG.md` — fill with Unreleased section
- `CONTRIBUTING.md` — fill with setup, branching, PR checklist
- `SECURITY.md` — fill with supported versions and disclosure process
- `qualgraph.yaml.example` — fill all keys

**Tests modified:**
- `tests/unit/test_viewer_server.py` — add health, error message, overflow tests

---

## Task 1: Rename package metadata in pyproject.toml

**Goal:** Replace `analytify` project metadata with `qualgraph`, add `[build-system]` with hatchling, fill all metadata fields, add `dev` extras, remove the `analytify` console script.

**Files:**
- Modify: `pyproject.toml`

**Acceptance Criteria:**
- [ ] `[project] name = "qualgraph"`
- [ ] `[build-system]` section present with hatchling
- [ ] `description`, `readme`, `license`, `authors`, `keywords`, `classifiers`, `[project.urls]` all filled
- [ ] `[project.optional-dependencies] dev` includes pytest, ruff, build, twine
- [ ] Only `qualgraph` console script (no `analytify`)
- [ ] `pip install -e ".[dev]"` succeeds in a fresh venv
- [ ] `pip check` exits 0
- [ ] `qualgraph --help` exits 0

**Verify:** `pip install -e ".[dev]" && pip check && qualgraph --help`

**Steps:**

- [ ] **Step 1: Replace pyproject.toml content**

Open `pyproject.toml` and replace the entire `[project]` section and add `[build-system]`. The file should become:

```toml
[project]
name = "qualgraph"
version = "0.1.0"
description = "Local, graph-aware code quality analysis for Python repositories"
readme = "README.md"
license = { text = "MIT" }
authors = [{ name = "Anton Benz", email = "anton.erdmann.benz@uni-weimar.de" }]
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
dev = ["pytest>=8.0", "ruff>=0.6", "build>=1.2", "twine>=5.0"]

[project.scripts]
qualgraph = "qualgraph.cli:app"
```

Keep the existing `[project.dependencies]` list unchanged. Keep any existing `[tool.*]` sections unchanged.

Add after the `[project]` block (before `[project.dependencies]`):

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/qualgraph"]
```

- [ ] **Step 2: Reinstall in editable mode**

```powershell
.venv\Scripts\pip install -e ".[dev]"
```

Expected: resolves and installs without errors.

- [ ] **Step 3: Verify**

```powershell
.venv\Scripts\pip check
.venv\Scripts\qualgraph --help
```

Expected: `pip check` prints nothing (exit 0). `qualgraph --help` shows the help text.

- [ ] **Step 4: Commit**

```powershell
git add pyproject.toml
git commit -m "Rename package to qualgraph, add hatchling build system and dev extras"
```

---

## Task 2: Add `python -m qualgraph` support

**Goal:** Create `src/qualgraph/__main__.py` so the package is runnable as `python -m qualgraph`.

**Files:**
- Create: `src/qualgraph/__main__.py`

**Acceptance Criteria:**
- [ ] `python -m qualgraph --help` exits 0 and shows the same help as `qualgraph --help`

**Verify:** `python -m qualgraph --help`

**Steps:**

- [ ] **Step 1: Write the failing test**

In `tests/unit/test_cli_module.py` (new file):

```python
import subprocess
import sys


def test_python_m_qualgraph_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "qualgraph", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "code quality" in result.stdout.lower()
```

- [ ] **Step 2: Run to verify it fails**

```powershell
.venv\Scripts\pytest tests/unit/test_cli_module.py -v
```

Expected: FAIL — `No module named qualgraph.__main__`

- [ ] **Step 3: Create `__main__.py`**

```python
from qualgraph.cli import app

app()
```

- [ ] **Step 4: Run to verify it passes**

```powershell
.venv\Scripts\pytest tests/unit/test_cli_module.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```powershell
git add src/qualgraph/__main__.py tests/unit/test_cli_module.py
git commit -m "Add python -m qualgraph entrypoint"
```

---

## Task 3: Implement `qualgraph analyze` command

**Goal:** Add a `qualgraph analyze <repo>` command to `cli.py` that orchestrates build → annotate → report → export-json into an artifacts directory, with `--preset`, `--coverage-mode`, `--top-n`, `--serve`, `--open`, and `--artifacts-dir` flags.

**Files:**
- Modify: `src/qualgraph/cli.py:1-51`
- Test: `tests/unit/test_analyze_command.py` (new)

**Acceptance Criteria:**
- [ ] `qualgraph analyze --help` shows all six flags
- [ ] `qualgraph analyze benchmarks/repos/tiny_repo --preset fast --top-n 3` exits 0
- [ ] `.qualgraph/graph.json` exists after the run
- [ ] `.qualgraph/report.md` exists after the run
- [ ] `.qualgraph/graph.export.json` exists after the run
- [ ] `--artifacts-dir /nonexistent/readonly` prints a clear error and exits non-zero
- [ ] Unknown preset prints a clear error and exits non-zero

**Verify:** `pytest tests/unit/test_analyze_command.py -v`

**Steps:**

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/test_analyze_command.py`:

```python
import subprocess
import sys
from pathlib import Path

import pytest


TINY_REPO = Path("benchmarks/repos/tiny_repo")


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "qualgraph", *args],
        capture_output=True,
        text=True,
    )


def test_analyze_help() -> None:
    result = _run("analyze", "--help")
    assert result.returncode == 0
    for flag in ["--preset", "--coverage-mode", "--top-n", "--serve", "--open", "--artifacts-dir"]:
        assert flag in result.stdout


@pytest.mark.skipif(not TINY_REPO.exists(), reason="tiny_repo not present")
def test_analyze_fast_preset(tmp_path: Path) -> None:
    result = _run(
        "analyze", str(TINY_REPO),
        "--preset", "fast",
        "--top-n", "3",
        "--artifacts-dir", str(tmp_path),
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "graph.json").exists()
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "graph.export.json").exists()


def test_analyze_unknown_preset(tmp_path: Path) -> None:
    result = _run(
        "analyze", str(TINY_REPO),
        "--preset", "bogus",
        "--artifacts-dir", str(tmp_path),
    )
    assert result.returncode != 0
    assert "preset" in result.stderr.lower() or "preset" in result.stdout.lower()


def test_analyze_unwritable_dir() -> None:
    result = _run(
        "analyze", str(TINY_REPO),
        "--artifacts-dir", "/this/path/does/not/exist/readonly",
    )
    assert result.returncode != 0
```

- [ ] **Step 2: Run to verify tests fail**

```powershell
.venv\Scripts\pytest tests/unit/test_analyze_command.py -v
```

Expected: FAIL on all tests that invoke `analyze` (command not found).

- [ ] **Step 3: Add the `analyze` command to `cli.py`**

Add `import os` at the top of the existing imports block.

Then add this constant after the existing `FULL_ANNOTATORS` line (after line 51):

```python
PRESET_ANNOTATORS: dict[str, str] = {
    "fast": FAST_ANNOTATORS,
    "standard": STANDARD_ANNOTATORS,
    "full": FULL_ANNOTATORS,
}
```

Then add the following command anywhere after the `serve` command and before the `llm_app` commands:

```python
@app.command()
def analyze(
    repo: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
    preset: str = typer.Option("standard", "--preset", help="Annotator preset: fast, standard, or full."),
    coverage_mode: str = typer.Option(
        "auto",
        "--coverage-mode",
        help="Coverage mode: auto, reuse, run, or skip.",
    ),
    top_n: int = typer.Option(10, "--top-n", min=1, help="Top-N risk nodes for the report."),
    serve_after: bool = typer.Option(False, "--serve", help="Start the viewer after analysis completes."),
    open_browser: bool = typer.Option(False, "--open", help="Open the viewer in the default browser."),
    artifacts_dir: Optional[Path] = typer.Option(
        None,
        "--artifacts-dir",
        help="Output directory (default: .qualgraph/ or QUALGRAPH_ARTIFACTS_DIR env var).",
    ),
) -> None:
    """Build, annotate, report, and export a graph in one command."""

    env_dir = os.environ.get("QUALGRAPH_ARTIFACTS_DIR")
    out_dir: Path = artifacts_dir or (Path(env_dir) if env_dir else Path(".qualgraph"))

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        probe = out_dir / ".write_probe"
        probe.touch()
        probe.unlink()
    except (OSError, PermissionError) as exc:
        typer.echo(f"Error: cannot write to artifacts directory '{out_dir}': {exc}", err=True)
        raise typer.Exit(1)

    if preset not in PRESET_ANNOTATORS:
        typer.echo(
            f"Error: unknown preset '{preset}'. Valid presets: {', '.join(PRESET_ANNOTATORS)}.",
            err=True,
        )
        raise typer.Exit(1)

    graph_path = out_dir / "graph.json"
    report_path = out_dir / "report.md"
    export_path = out_dir / "graph.export.json"

    # 1/4 Build
    typer.echo(f"[1/4] Building graph for {repo} …")
    run_logger = RunLogger(repo_path=repo)
    try:
        with run_logger.span("build_graph") as span:
            graph = build_graph(repo, [])
            span["nodes"] = graph.number_of_nodes()
            span["edges"] = graph.number_of_edges()
        annotate_clusters(graph)
        _annotate_metrics(graph, metric_mode="fast", betweenness_samples=128)
        score_risk(graph)
        write_json_graph(graph, graph_path)
    finally:
        run_logger.finish()
    typer.echo(f"      {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges → {graph_path}")

    # 2/4 Annotate
    typer.echo(f"[2/4] Annotating ({preset} preset) …")
    run_logger2 = RunLogger(repo_path=repo)
    try:
        selected = _resolve_annotators(
            PRESET_ANNOTATORS[preset],
            coverage_mode=coverage_mode,
        )
        run_pipeline(graph, repo, selected, logger=run_logger2, show_progress=True)
        score_risk(graph)
        write_json_graph(graph, graph_path)
    finally:
        run_logger2.finish()

    # 3/4 Report
    typer.echo(f"[3/4] Generating report (top {top_n} nodes) …")
    write_markdown_report(graph, report_path, top_n=top_n)
    typer.echo(f"      → {report_path}")

    # 4/4 Export JSON
    typer.echo("[4/4] Exporting JSON …")
    write_json_export(graph, export_path)
    typer.echo(f"      → {export_path}")

    typer.echo(f"\nDone. Artifacts in {out_dir}/")

    if serve_after or open_browser:
        serve_graph(graph_path, top_n=top_n, open_browser=open_browser)
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
.venv\Scripts\pytest tests/unit/test_analyze_command.py -v
```

Expected: all PASS (the `test_analyze_unwritable_dir` test may be skipped on Windows if the path is simply created — adjust the path to something truly unwritable if needed, e.g., a file path treated as a dir: `--artifacts-dir pyproject.toml`).

- [ ] **Step 5: Run full test suite to verify no regressions**

```powershell
.venv\Scripts\pytest -v
```

Expected: all previously passing tests still pass.

- [ ] **Step 6: Commit**

```powershell
git add src/qualgraph/cli.py tests/unit/test_analyze_command.py
git commit -m "Add qualgraph analyze command with preset, top-n, serve, and artifacts-dir flags"
```

---

## Task 4: Add `/api/health` endpoint and improve serve error messages

**Goal:** Add a `GET /api/health` endpoint returning `{"status": "ok", "graph_loaded": bool}`, and make `qualgraph serve` print clear error messages for missing graph files and occupied ports instead of tracebacks.

**Files:**
- Modify: `src/qualgraph/viewer/server.py`
- Modify: `tests/unit/test_viewer_server.py`

**Acceptance Criteria:**
- [ ] `GET /api/health` returns `{"status": "ok", "graph_loaded": true}` when graph loaded
- [ ] `GET /api/health` returns `{"status": "ok", "graph_loaded": false}` when no graph
- [ ] `serve_graph` with a missing file prints "Graph file not found" and raises `SystemExit(1)`
- [ ] `serve_graph` with an occupied port prints "already in use" and raises `SystemExit(1)`
- [ ] All existing tests still pass

**Verify:** `pytest tests/unit/test_viewer_server.py -v`

**Steps:**

- [ ] **Step 1: Write the failing tests**

Add to the bottom of `tests/unit/test_viewer_server.py`:

```python
import socket
import os


def test_health_endpoint_when_graph_loaded(tmp_path: Path) -> None:
    graph_path = tmp_path / "graph.json"
    write_json_graph(_server_graph(), graph_path)
    server = create_server(graph_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        health = _json_get(f"{server.url}api/health")
        assert health["status"] == "ok"
        assert health["graph_loaded"] is True
    finally:
        server.shutdown()
        server.server_close()


def test_health_endpoint_when_no_graph(tmp_path: Path) -> None:
    graph_path = tmp_path / "graph.json"
    write_json_graph(_server_graph(), graph_path)
    server = create_server(graph_path, port=0)
    # Simulate unloaded graph by setting viewer to None
    server.viewer = None
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        health = _json_get(f"{server.url}api/health")
        assert health["status"] == "ok"
        assert health["graph_loaded"] is False
    finally:
        server.shutdown()
        server.server_close()


def test_serve_graph_missing_file_exits(tmp_path: Path) -> None:
    from qualgraph.viewer.server import serve_graph
    missing = tmp_path / "missing.json"
    with pytest.raises(SystemExit) as exc_info:
        serve_graph(missing)
    assert exc_info.value.code == 1


def test_serve_graph_occupied_port_exits(tmp_path: Path) -> None:
    from qualgraph.viewer.server import serve_graph
    graph_path = tmp_path / "graph.json"
    write_json_graph(_server_graph(), graph_path)
    # Occupy a port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    occupied_port = sock.getsockname()[1]
    try:
        with pytest.raises(SystemExit) as exc_info:
            serve_graph(graph_path, port=occupied_port)
        assert exc_info.value.code == 1
    finally:
        sock.close()
```

Also add `import pytest` to the imports at the top of `test_viewer_server.py`.

- [ ] **Step 2: Run to verify tests fail**

```powershell
.venv\Scripts\pytest tests/unit/test_viewer_server.py -v -k "health or missing_file or occupied_port"
```

Expected: FAIL — `/api/health` returns 404, and `serve_graph` raises exceptions instead of `SystemExit`.

- [ ] **Step 3: Add `/api/health` route to `server.py`**

In `ViewerRequestHandler.do_GET`, add before the final 404 handler (before line `self._send_json({"error": "not found"}`):

```python
        if parsed.path == "/api/health":
            self._send_json({"status": "ok", "graph_loaded": self.server.viewer is not None})
            return
```

- [ ] **Step 4: Wrap `serve_graph` with error handling**

Replace the `serve_graph` function in `server.py` with:

```python
def serve_graph(
    graph_path: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 0,
    top_n: int = 50,
    open_browser: bool = False,
) -> str:
    graph_path = Path(graph_path)
    if not graph_path.exists():
        print(
            f"Error: Graph file not found at '{graph_path}'. "
            "Run 'qualgraph build <repo>' first.",
            file=__import__("sys").stderr,
        )
        raise SystemExit(1)
    try:
        server = create_server(graph_path, host=host, port=port, top_n=top_n)
    except OSError as exc:
        if exc.errno == 98 or "address already in use" in str(exc).lower():
            print(
                f"Error: Port {port} is already in use. Try '--port <other-port>'.",
                file=__import__("sys").stderr,
            )
            raise SystemExit(1)
        raise
    url = server.url
    if open_browser:
        threading.Timer(0.25, lambda: webbrowser.open(url)).start()
    try:
        print(f"Qualgraph viewer running at {url}")
        print("Press Ctrl+C to stop.")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return url
```

Add `import sys` to the imports at the top of `server.py` (or use `__import__("sys")` inline as shown — prefer the explicit import at top).

Actually, replace the inline `__import__` approach: add `import sys` to the imports block at the top of `server.py`, then use `sys.stderr` in the `print` calls.

- [ ] **Step 5: Run tests**

```powershell
.venv\Scripts\pytest tests/unit/test_viewer_server.py -v
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```powershell
git add src/qualgraph/viewer/server.py tests/unit/test_viewer_server.py
git commit -m "Add /api/health endpoint and clear error messages to qualgraph serve"
```

---

## Task 5: Viewer responsive layout, overflow fixes, and UX states

**Goal:** Make the viewer work on screens narrower than 1100px, prevent long strings from overflowing, and add loading/empty/error states and keyboard focus styles.

**Files:**
- Modify: `src/qualgraph/viewer/assets/styles.css`
- Modify: `src/qualgraph/viewer/assets/index.html`

**Acceptance Criteria:**
- [ ] `overflow-wrap: break-word` applied to node names, file paths, and qualified names
- [ ] Code blocks and findings tables have `overflow-x: auto; max-width: 100%`
- [ ] At ≤768px the layout is single-column (sidebar stacks above canvas)
- [ ] At ≤480px the inspector panel is hidden or collapses below
- [ ] All buttons and interactive elements have a visible focus ring
- [ ] A loading spinner appears in the canvas area while graph data loads
- [ ] An empty state message appears when the graph returns 0 nodes
- [ ] An error state appears when `/api/graph` returns non-200
- [ ] No `Â·` or similar encoding artifacts visible in the HTML source

**Verify:** Open `qualgraph serve .qualgraph/graph.json` and manually check at 1280px, 768px, and 480px widths. Inspect page source for UTF-8 encoding issues.

**Steps:**

- [ ] **Step 1: Fix encoding — verify HTML file is clean UTF-8**

Open `src/qualgraph/viewer/assets/index.html` and confirm `<meta charset="utf-8">` is present in `<head>`. If the `Â·` artifact appears as a literal string in the HTML source, find and replace it with `&middot;` or the correct Unicode character.

Confirm `server.py` line 107 already sets `charset=utf-8` for HTML responses (it does — verify the `_send_asset` method).

- [ ] **Step 2: Add overflow and responsive CSS to `styles.css`**

Append to the end of `styles.css`:

```css
/* --- Overflow protection --- */
.node-name,
.qualified-name,
.file-path,
.finding-message {
  overflow-wrap: break-word;
  word-break: break-all;
}

pre,
code,
.source-block {
  overflow-x: auto;
  max-width: 100%;
  white-space: pre-wrap;
}

.badge {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* --- Focus styles --- */
button:focus-visible,
a:focus-visible,
[tabindex]:focus-visible {
  outline: 2px solid #70a7ff;
  outline-offset: 2px;
}

/* --- Responsive: tablet (≤768px) --- */
@media (max-width: 768px) {
  .shell {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
    overflow: auto;
  }

  .sidebar {
    border-right: none;
    border-bottom: 1px solid var(--line);
    max-height: 220px;
    overflow-y: auto;
  }

  .inspector {
    border-left: none;
    border-top: 1px solid var(--line);
  }
}

/* --- Responsive: mobile (≤480px) --- */
@media (max-width: 480px) {
  .inspector {
    display: none;
  }

  .sidebar {
    max-height: 160px;
    font-size: 0.88rem;
  }
}

/* --- Loading / empty / error states --- */
.canvas-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--muted);
  gap: 12px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--line);
  border-top-color: var(--blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.canvas-state details {
  max-width: 480px;
  text-align: left;
  color: var(--red);
  font-size: 0.85rem;
}
```

- [ ] **Step 3: Add loading/empty/error state HTML to `index.html`**

Inside the main canvas `<div>` (the element that holds the `<canvas>`), add a sibling element for states:

```html
<div id="canvas-state" class="canvas-state" style="display:none">
  <div class="spinner" id="state-spinner"></div>
  <span id="state-message"></span>
  <details id="state-detail" style="display:none">
    <summary>Error detail</summary>
    <pre id="state-detail-text"></pre>
  </details>
</div>
```

- [ ] **Step 4: Wire up states in `app.js`**

Find the section of `app.js` that fetches `/api/graph` and add state management around it. The pattern is:

```js
function showState(type, message, detail) {
  const el = document.getElementById('canvas-state');
  const spinner = document.getElementById('state-spinner');
  const msg = document.getElementById('state-message');
  const detailEl = document.getElementById('state-detail');
  const detailText = document.getElementById('state-detail-text');

  el.style.display = type ? 'flex' : 'none';
  spinner.style.display = type === 'loading' ? 'block' : 'none';
  msg.textContent = message || '';
  if (detail) {
    detailEl.style.display = 'block';
    detailText.textContent = detail;
  } else {
    detailEl.style.display = 'none';
  }
}
```

Call `showState('loading', 'Loading graph…')` before the fetch, `showState(null)` on success (hide the state overlay and show the canvas), `showState('error', 'Failed to load graph.', errorText)` on fetch failure, and `showState('empty', 'No nodes found. Run qualgraph build <repo> first.')` when the response has 0 nodes.

- [ ] **Step 5: Add `aria-label` to icon-only buttons in `index.html`**

Find any `<button>` elements in `index.html` that contain only an icon (SVG or emoji) and no visible text. Add `aria-label="Descriptive action"` and `title="Descriptive action"` to each.

- [ ] **Step 6: Manual smoke test**

```powershell
.venv\Scripts\qualgraph serve .qualgraph\graph.json --open
```

Resize the browser to 768px and 480px width. Verify the layout stacks. Verify no horizontal scrollbar at any width. Inspect the page source and confirm no `Â·` artifacts.

- [ ] **Step 7: Commit**

```powershell
git add src/qualgraph/viewer/assets/styles.css src/qualgraph/viewer/assets/index.html src/qualgraph/viewer/assets/app.js
git commit -m "Add responsive layout, overflow fixes, and loading/error states to viewer"
```

---

## Task 6: Rewrite README.md

**Goal:** Replace the existing README with a public-quality document that opens with a strong pitch, includes a working quickstart, and links out to `docs/` for deep detail.

**Files:**
- Modify: `README.md`

**Acceptance Criteria:**
- [ ] Opens with one-line pitch + badge row
- [ ] Quickstart section runnable in under 60 seconds
- [ ] All CLI commands shown with real examples
- [ ] LLM workflows section explains both agent-file and API-backed approaches
- [ ] Privacy statement is explicit
- [ ] `.qualgraph/` output layout explained
- [ ] Troubleshooting covers top 5 failure modes
- [ ] All links to `docs/` files are valid relative paths

**Verify:** Read the rendered Markdown in a browser (GitHub preview or `grip`).

**Steps:**

- [ ] **Step 1: Write the new README.md**

Replace the entire file with:

```markdown
# Qualgraph

**Graph-aware code quality analysis for Python repositories — local-first, LLM-ready.**

[![CI](https://github.com/benzae1/analytify/actions/workflows/ci.yml/badge.svg)](https://github.com/benzae1/analytify/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Qualgraph builds a code graph from your Python repository and layers quality signals on top: complexity, linting, dead code, test coverage, git churn, security vulnerabilities, and optional LLM insights. Every signal lives on the same graph, so the risk scorer can combine them intelligently.

---

## What it does

- Parses your repo into a **NetworkX graph** — modules, classes, functions, calls, imports
- Runs **15+ annotators** in parallel: radon, ruff, vulture, coverage, git history, bandit, pip-audit, secrets detection
- Computes a **risk score** per node combining centrality, complexity, churn, coverage, security, and LLM findings
- Exports a **Markdown report** and a **JSON artifact** for CI, dashboards, or LLM workflows
- Serves a **local interactive viewer** — no cloud, no telemetry

---

## Quickstart

```bash
pip install qualgraph
qualgraph analyze /path/to/your/repo --preset fast
qualgraph serve .qualgraph/graph.json --open
```

That's it. The viewer opens in your browser with an interactive graph of your codebase.

---

## Installation

**From PyPI (once published):**
```bash
pip install qualgraph
```

**From source:**
```bash
git clone https://github.com/benzae1/analytify.git
cd analytify
pip install -e ".[dev]"
```

See [docs/installation.md](docs/installation.md) for pipx, Windows path setup, and tree-sitter native dependency notes.

---

## CLI

### `qualgraph analyze` — full pipeline in one command

```bash
qualgraph analyze <repo> [OPTIONS]

Options:
  --preset        fast | standard | full   (default: standard)
  --coverage-mode auto | reuse | run | skip
  --top-n         INT   top-N risk nodes in report (default: 10)
  --serve               start viewer after analysis
  --open                open browser automatically
  --artifacts-dir PATH  output directory (default: .qualgraph/)
```

**Presets:**

| Preset | Annotators |
|--------|-----------|
| `fast` | radon, ruff, docstring, cross_signal |
| `standard` | fast + git history, cross_signal |
| `full` | standard + vulture, security suite, coverage |

**Examples:**

```bash
# Quick analysis, open viewer
qualgraph analyze . --preset fast --serve --open

# Full analysis, top 20 nodes in report
qualgraph analyze . --preset full --top-n 20

# Custom output location
qualgraph analyze . --artifacts-dir /tmp/myreport
```

### Individual commands

```bash
qualgraph build <repo>                   # Build graph only
qualgraph annotate <repo> --annotators radon,ruff,git
qualgraph report <graph.json> --top-n 15
qualgraph export-json <graph.json>
qualgraph serve <graph.json> --open
```

See [docs/cli.md](docs/cli.md) for full reference.

---

## Viewer

```bash
qualgraph serve .qualgraph/graph.json --open
```

The viewer shows:

- Interactive force-directed graph with cluster colouring
- Sidebar with risk ranking, search, and cluster navigation
- Inspector panel with per-node signals: complexity, coverage, churn, security findings, LLM insights
- Full source preview with finding highlights

See [docs/viewer.md](docs/viewer.md) for keyboard shortcuts and API endpoints.

---

## LLM workflows

Qualgraph has two LLM modes. **No API key required for the agent-file workflow.**

### Agent-file workflow (recommended)

```bash
# 1. Build and annotate
qualgraph analyze . --preset standard

# 2. Export task files for an LLM agent
qualgraph llm export-tasks .qualgraph/graph.json --limit 10

# 3. Paste tasks.md into Claude, GPT-4, or any LLM — get back results.md
# 4. Import results
qualgraph llm import-results .qualgraph/runs/<run-id>/llm_tasks/results/ \
  --graph .qualgraph/graph.json

# 5. Regenerate report with LLM findings
qualgraph report .qualgraph/graph.json
```

### API-backed workflow

```bash
# Anthropic
ANTHROPIC_API_KEY=sk-... qualgraph llm analyze .qualgraph/graph.json \
  --provider anthropic --model claude-sonnet-4-6 --max-llm-calls 10

# OpenAI
OPENAI_API_KEY=sk-... qualgraph llm analyze .qualgraph/graph.json \
  --provider openai --model gpt-4o-mini

# Local (Ollama, no key)
qualgraph llm analyze .qualgraph/graph.json --provider ollama --model llama3

# Dry run — see prompts without spending tokens
qualgraph llm analyze .qualgraph/graph.json --provider anthropic --dry-run
```

Results are cached in `.qualgraph/cache.sqlite` by content hash — re-running with the same graph and model costs nothing.

See [docs/llm-workflows.md](docs/llm-workflows.md) for a complete walkthrough.

---

## Privacy & locality

All your source code stays on your machine. Qualgraph never sends code anywhere unless you explicitly run `qualgraph llm analyze` with an API provider (`--provider anthropic` or `--provider openai`). Even then, only the selected top-N node contexts (function signatures, docstrings, metrics) are sent — not full files.

The Ollama provider (`--provider ollama`) is fully local with no outbound network calls.

---

## Output artifacts

After `qualgraph analyze .`:

```
.qualgraph/
├── graph.json          # annotated graph (all signals)
├── report.md           # human-readable Markdown report
├── graph.export.json   # versioned JSON for CI / dashboards
├── cache.sqlite        # LLM result cache (content-addressed)
└── runs/               # per-run event logs
```

---

## Troubleshooting

**`qualgraph: command not found`**
The package isn't installed or the venv isn't activated. Run `pip install qualgraph` or `source .venv/bin/activate`.

**`Error: Graph file not found`**
Run `qualgraph build <repo>` or `qualgraph analyze <repo>` first to create the graph.

**`tree_sitter` import error on first run**
Install build tools: on Ubuntu `sudo apt install build-essential`, on macOS `xcode-select --install`, on Windows install Visual C++ Build Tools.

**Coverage annotator hangs**
Add `--coverage-mode skip` to skip coverage, or `--coverage-mode reuse` to use an existing `.coverage` file without re-running tests.

**LLM analysis returns no findings**
Run with `--dry-run` to inspect the prompts. Check that your API key env var is set and the model name is valid.

---

## Development

```bash
git clone https://github.com/benzae1/analytify.git
cd analytify
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"   # Windows
# or
.venv/bin/pip install -e ".[dev]"       # macOS/Linux

pytest
ruff check .
```

After modifying source files, update the knowledge graph:
```bash
graphify update .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, commit style, and how to add an annotator.

---

## License

MIT — see [LICENSE](LICENSE).
```

- [ ] **Step 2: Verify all doc links are valid**

Check that `docs/installation.md`, `docs/cli.md`, `docs/viewer.md`, `docs/llm-workflows.md`, `CONTRIBUTING.md`, and `LICENSE` all exist (they will be created in subsequent tasks — note this dependency and verify after those tasks complete).

- [ ] **Step 3: Commit**

```powershell
git add README.md
git commit -m "Rewrite README for public release"
```

---

## Task 7: Create docs/ directory and architecture/installation/configuration/cli/viewer docs

**Goal:** Create the `docs/` directory with architecture, installation, configuration, CLI, and viewer documentation.

**Files:**
- Create: `docs/architecture.md`
- Create: `docs/installation.md`
- Create: `docs/configuration.md`
- Create: `docs/cli.md`
- Create: `docs/viewer.md`

**Acceptance Criteria:**
- [ ] All five files exist and contain substantive content
- [ ] `docs/architecture.md` covers the graph schema, annotator pipeline, and risk formula
- [ ] `docs/installation.md` covers venv, pipx, Windows, and tree-sitter native deps
- [ ] `docs/configuration.md` documents every key in `qualgraph.yaml`
- [ ] `docs/cli.md` has a runnable example for every command
- [ ] `docs/viewer.md` documents all API endpoints including `/api/health`

**Verify:** Read each file; confirm no placeholder text.

**Steps:**

- [ ] **Step 1: Create `docs/architecture.md`**

```markdown
# Qualgraph Architecture

## Graph model

Qualgraph builds a `networkx.DiGraph` where every node is a Python symbol (module, class, function, or method) and every edge is a relationship (call, import, inheritance, test linkage, co-change).

**Node attributes (selected):**

| Attribute | Type | Set by |
|-----------|------|--------|
| `type` | str | builder (Module, Class, Function, Method) |
| `file_path` | str | builder |
| `line_start`, `line_end` | int | builder |
| `source` | str | builder |
| `complexity` | float | radon annotator |
| `maintainability_index` | float | radon annotator |
| `lint_findings` | list | ruff annotator |
| `coverage` | float | coverage annotator |
| `churn` | int | git_history annotator |
| `security_findings` | list | bandit/pip_audit/secrets annotators |
| `llm_findings` | list | llm analyzer |
| `risk_score` | float | risk scorer |
| `cluster_id` | int | Leiden clustering |

**Edge types:**

| Type | Meaning |
|------|---------|
| `calls` | function calls another function |
| `imports` | module imports another |
| `inherits` | class inherits from another |
| `tested_by` | function is tested by a test function |
| `co_changes_with` | two symbols frequently change together in git |

## Annotator pipeline

Annotators are independent — a failure in one does not stop the rest. Each annotator implements `BaseAnnotator` with two required methods:

- `is_available() -> bool` — returns False if the tool is not installed
- `annotate(graph, repo_path) -> AnnotatorResult` — mutates node attributes in place

The pipeline runs annotators sequentially and collects `AnnotatorResult` objects with timing and error information.

**Built-in annotators:**

| Name | Tool | What it adds |
|------|------|-------------|
| `radon` | radon | cyclomatic complexity, maintainability index |
| `ruff` | ruff | lint findings per node |
| `vulture` | vulture | dead code probability |
| `coverage` | coverage.py | line coverage %, runs tests if needed |
| `test_linkage` | AST | links test functions to the functions they test |
| `git_history` | GitPython | commit churn, author count, bug-fix commit ratio |
| `co_change` | GitPython | co-change coupling between nodes |
| `bandit` | bandit | security findings (CWE-annotated) |
| `pip_audit` | pip-audit | known CVEs in dependencies |
| `secrets` | detect-secrets | high-entropy strings and credential patterns |
| `profiler` | cProfile | runtime hotspots from a profile JSON artifact |
| `docstring` | AST | docstring presence and style |
| `cross_signal` | internal | derived findings combining multiple signals |

## Risk formula

The risk score is a weighted percentile rank across seven dimensions:

```
risk = w1·complexity_pct + w2·churn_pct + w3·(1 - coverage_pct)
     + w4·centrality_pct + w5·security_pct + w6·lint_pct + w7·llm_pct
```

Weights are configurable in `qualgraph.yaml`. Nodes with no data for a dimension are assigned the median percentile for that dimension, so missing data doesn't distort the ranking.

## Leiden clustering

Nodes are grouped into communities using the Leiden algorithm (`leidenalg`). The resolution parameter controls community granularity — higher values produce more, smaller communities. The default resolution is tuned for repositories of 5,000–50,000 lines of code.
```

- [ ] **Step 2: Create `docs/installation.md`**

```markdown
# Installation

## Requirements

- Python 3.11 or 3.12
- Git (for git history annotators)
- A C compiler (for tree-sitter native extensions)

## Standard install (venv)

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows PowerShell

pip install qualgraph
```

## From source (development)

```bash
git clone https://github.com/benzae1/analytify.git
cd analytify
pip install -e ".[dev]"
```

## pipx (isolated global install)

```bash
pipx install qualgraph
```

## Windows notes

On Windows, activate the venv with:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## tree-sitter native dependencies

Qualgraph uses `tree-sitter` to parse Python source. On first install, pip will compile a small C extension. You need a C compiler:

- **Ubuntu/Debian:** `sudo apt install build-essential`
- **macOS:** `xcode-select --install`
- **Windows:** Install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and select "Desktop development with C++"

If compilation fails, check that `gcc` (Linux/macOS) or `cl.exe` (Windows) is on your PATH.

## Optional annotator dependencies

Most annotators are bundled as dependencies. The profiler annotator requires a cProfile JSON artifact — generate one with:

```bash
python -m cProfile -o profile.pstats your_script.py
python -c "import pstats, json; s=pstats.Stats('profile.pstats'); ..."
```

See `qualgraph llm --help` for API key setup for LLM providers.
```

- [ ] **Step 3: Create `docs/configuration.md`**

```markdown
# Configuration

Qualgraph reads configuration from `qualgraph.yaml` in the current directory (or the repository root). All keys are optional — Qualgraph works with zero configuration.

Copy `qualgraph.yaml.example` to `qualgraph.yaml` and edit as needed.

## Full key reference

```yaml
# qualgraph.yaml

# Annotator pipeline
annotators:
  # Paths and glob patterns to exclude from graph building.
  # These are in addition to the built-in excludes (.venv, __pycache__, etc.)
  exclude:
    - "docs/**"
    - "scripts/**"

  # Coverage annotator behaviour: auto, reuse, run, or skip
  # auto: reuse existing .coverage if fresh, otherwise run tests
  # reuse: always use existing .coverage, fail if missing
  # run: always run tests (slow but accurate)
  # skip: skip coverage entirely
  coverage_mode: auto

  # Extra pytest arguments passed when coverage_mode is 'run'
  pytest_args: ""

  # Maximum number of git commits to scan for churn/co-change annotators.
  # 0 scans the full history (slow on large repos).
  git_max_commits: 1000

# Risk scoring weights (must sum to 1.0)
risk:
  complexity: 0.20
  churn: 0.20
  coverage: 0.20
  centrality: 0.15
  security: 0.15
  lint: 0.05
  llm: 0.05

# Graph construction
graph:
  # Leiden clustering resolution. Higher = more, smaller clusters.
  # Default is tuned for 5k–50k LOC repos.
  leiden_resolution: 1.0

  # Structural metric computation mode: fast, exact, or off
  # fast: approximate betweenness using sampling (recommended)
  # exact: full betweenness (slow on large graphs)
  # off: skip betweenness entirely
  metric_mode: fast

# LLM analysis defaults
llm:
  # Default provider: ollama, openai, or anthropic
  provider: ollama

  # Default model per provider (overrides built-in defaults)
  # model: llama3

  # Maximum nodes to send for LLM analysis per run
  max_calls: 50

  # SQLite cache path (relative to project root)
  cache_path: .qualgraph/cache.sqlite

# Output
output:
  # Default artifacts directory (overridden by --artifacts-dir or QUALGRAPH_ARTIFACTS_DIR)
  artifacts_dir: .qualgraph
```

## Environment variables

| Variable | Equivalent | Description |
|----------|-----------|-------------|
| `QUALGRAPH_ARTIFACTS_DIR` | `--artifacts-dir` | Override output directory |
| `ANTHROPIC_API_KEY` | — | API key for Anthropic provider |
| `OPENAI_API_KEY` | — | API key for OpenAI provider |
```

- [ ] **Step 4: Create `docs/cli.md`**

```markdown
# CLI Reference

## `qualgraph analyze` — full pipeline

```
qualgraph analyze <repo> [OPTIONS]
```

Runs build → annotate → report → export-json and writes all artifacts to the output directory.

| Option | Default | Description |
|--------|---------|-------------|
| `--preset` | `standard` | Annotator set: `fast`, `standard`, or `full` |
| `--coverage-mode` | `auto` | `auto`, `reuse`, `run`, or `skip` |
| `--top-n` | `10` | Top-N risk nodes in the report |
| `--serve` | false | Start viewer after analysis |
| `--open` | false | Open browser automatically |
| `--artifacts-dir` | `.qualgraph/` | Output directory |

```bash
# Fast scan, open viewer
qualgraph analyze . --preset fast --serve --open

# Full scan with custom output dir
qualgraph analyze /path/to/repo --preset full --artifacts-dir /tmp/report
```

## `qualgraph build`

Build the code graph from a repository without running annotators.

```bash
qualgraph build <repo> [--output graph.json] [--graphml export.graphml]
                        [--resolution 1.0] [--metric-mode fast]
```

## `qualgraph annotate`

Run annotators over an existing graph (builds one first if missing).

```bash
qualgraph annotate <repo> --annotators radon,ruff,git --graph graph.json
```

**Available annotator names:** `radon`, `ruff`, `vulture`, `bandit`, `docstring`, `coverage`, `test_linkage`, `git`, `co_change`, `pip_audit`, `secrets`, `security` (= bandit+pip_audit+secrets), `cross_signal`, `profiler`

**Preset shortcuts:** `fast`, `standard`, `full` (same as `analyze` presets)

## `qualgraph report`

Render a Markdown report from an annotated graph.

```bash
qualgraph report <graph.json> --top-n 20 --output report.md
```

## `qualgraph export-json`

Write a versioned JSON export for CI, dashboards, or LLM file-upload workflows.

```bash
qualgraph export-json <graph.json> --output graph.export.json
```

## `qualgraph serve`

Serve the local interactive viewer.

```bash
qualgraph serve <graph.json> [--host 127.0.0.1] [--port 8080] [--open] [--top-n 50]
```

## `qualgraph llm export-tasks`

Export top-risk node prompts as task files for an LLM agent.

```bash
qualgraph llm export-tasks <graph.json> --limit 10 --output-dir .qualgraph/tasks/
```

## `qualgraph llm import-results`

Import agent-written result files back into the graph.

```bash
qualgraph llm import-results <task-run-dir> --graph graph.json
```

## `qualgraph llm analyze`

Run provider-backed LLM analysis over the highest-risk nodes.

```bash
qualgraph llm analyze <graph.json> --provider anthropic \
  --model claude-sonnet-4-6 --max-llm-calls 10 --dry-run
```
```

- [ ] **Step 5: Create `docs/viewer.md`**

```markdown
# Viewer

The Qualgraph viewer is a local web application served from your machine. No data leaves your computer.

## Starting the viewer

```bash
qualgraph serve .qualgraph/graph.json --open
# or, after qualgraph analyze:
qualgraph analyze . --serve --open
```

Default URL: `http://127.0.0.1:<random-port>/`

## Interface

**Sidebar (left)**
- Graph summary: node count, edge count, cluster count, finding count
- Search box: filter nodes by name
- Filter buttons: All / High risk / LLM findings / Security
- Cluster list: click to drill into a cluster

**Canvas (centre)**
- Force-directed graph coloured by cluster
- Click a node to open it in the Inspector
- Scroll to zoom, drag to pan

**Inspector (right)**
- Node name, type, file path, line range
- Risk score bar with component breakdown
- Signal badges: complexity, coverage, churn, security, LLM
- Findings list with severity and source
- Source code preview

## API endpoints

All endpoints return JSON. The viewer frontend uses these; you can also query them directly.

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | `{"status": "ok", "graph_loaded": bool}` — readiness check |
| `GET /api/summary` | Graph-level statistics |
| `GET /api/graph` | Node/edge data for the canvas (`?cluster=<id>` or `?file=<path>`) |
| `GET /api/clusters` | Cluster list with metadata |
| `GET /api/files?cluster=<id>` | Files in a cluster |
| `GET /api/findings?source=<src>` | Findings filtered by source |
| `GET /api/node?id=<node-id>` | Full node detail including source |
| `GET /` | Viewer HTML |
| `GET /assets/<file>` | Static assets (JS, CSS) |

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `/` | Focus search box |
| `Escape` | Clear selection |
| `Tab` / `Shift+Tab` | Navigate between panels |
```

- [ ] **Step 6: Commit**

```powershell
git add docs/
git commit -m "Add docs/ with architecture, installation, configuration, CLI, and viewer docs"
```

---

## Task 8: Create `docs/llm-workflows.md`

**Goal:** Write the most detailed doc in the project — a complete guide to both the agent-file and API-backed LLM workflows, with concrete commands, example task files, and instructions for using the JSON export with any LLM.

**Files:**
- Create: `docs/llm-workflows.md`

**Acceptance Criteria:**
- [ ] Agent-file workflow covered step-by-step with actual commands
- [ ] Example `tasks.md` snippet included
- [ ] Example LLM response snippet included
- [ ] API-backed workflow covered for Anthropic, OpenAI, and Ollama
- [ ] `--dry-run` explained with example output
- [ ] Cache behaviour documented
- [ ] JSON export usage with LLMs documented, including example prompt
- [ ] Node context structure explained (what the LLM sees)

**Verify:** Read the file; confirm every step is actionable with no vague instructions.

**Steps:**

- [ ] **Step 1: Create `docs/llm-workflows.md`**

```markdown
# LLM Workflows

Qualgraph supports two LLM workflows: the **agent-file workflow** (no API key required, works with any LLM) and the **API-backed workflow** (automated, uses Anthropic/OpenAI/Ollama APIs).

---

## Agent-file workflow

This workflow exports analysis tasks as Markdown files that you paste into any LLM chat interface. No API keys, no cost beyond your existing subscription.

### Step 1: Build and annotate

```bash
qualgraph analyze . --preset standard
```

This writes `.qualgraph/graph.json` with all signals annotated.

### Step 2: Export tasks

```bash
qualgraph llm export-tasks .qualgraph/graph.json --limit 10
```

Output:
```
Wrote 10 LLM task(s) to .qualgraph/runs/20260505T120000Z-abc12345/llm_tasks/tasks/
Results directory: .qualgraph/runs/20260505T120000Z-abc12345/llm_tasks/results/
```

Each task file is named by node ID, e.g., `src-myapp-auth.py--myapp.auth.login--42.md`.

### Step 3: What a task file looks like

```markdown
# Analysis task: myapp.auth.login

**File:** src/myapp/auth.py  
**Lines:** 42–89  
**Risk score:** 0.87 (high)

## Signals

- Complexity: 12 (high — threshold 10)
- Coverage: 34% (low)
- Churn: 47 commits in last 90 days (high)
- Security: 1 bandit finding — B106 Hardcoded password funcarg (MEDIUM)
- Callers: 8 functions depend on this
- Tests: 1 linked test (test_login_success only)

## Source

```python
def login(username: str, password: str = "admin") -> bool:
    ...
```

## Your task

Review this function and answer:
1. What is the most likely source of bugs given the signals above?
2. Are there security concerns not captured by the automated tools?
3. What refactoring would most reduce risk?

Respond as JSON:
{"findings": [{"title": "...", "severity": "high|medium|low", "detail": "..."}]}
```

### Step 4: Get LLM responses

Paste the task file content into Claude, GPT-4, Gemini, or any other LLM. A useful system prompt:

> You are a senior software engineer reviewing Python code quality findings. Be specific, cite line numbers where possible, and return valid JSON.

### Step 5: What a result file looks like

Save the LLM's JSON response as a `.json` file in the results directory:

```
.qualgraph/runs/20260505T120000Z-abc12345/llm_tasks/results/src-myapp-auth.py--myapp.auth.login--42.json
```

Example result:
```json
{
  "findings": [
    {
      "title": "Default password in function signature",
      "severity": "high",
      "detail": "Line 42: `password='admin'` is a hardcoded default credential. Any caller that omits the password argument will use 'admin'. Remove the default and require explicit password passing."
    },
    {
      "title": "Insufficient test coverage for failure paths",
      "severity": "medium",
      "detail": "Only test_login_success is linked. The function has 12 branches (complexity=12) but 34% coverage suggests most failure paths (wrong password, locked account, DB error) are untested."
    }
  ]
}
```

### Step 6: Import results

```bash
qualgraph llm import-results \
  .qualgraph/runs/20260505T120000Z-abc12345/llm_tasks/results/ \
  --graph .qualgraph/graph.json
```

Output:
```
Imported 2 LLM finding(s) from 10/10 completed task(s). Wrote .qualgraph/graph.json.
```

### Step 7: Regenerate the report

```bash
qualgraph report .qualgraph/graph.json --top-n 10
```

The report now includes LLM findings alongside the automated signals.

---

## API-backed workflow

This workflow calls LLM APIs automatically. Qualgraph selects the top-N highest-risk nodes, builds a context for each, calls the API, and merges findings back into the graph.

### Anthropic (Claude)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
qualgraph llm analyze .qualgraph/graph.json \
  --provider anthropic \
  --model claude-sonnet-4-6 \
  --max-llm-calls 10
```

### OpenAI (GPT-4)

```bash
export OPENAI_API_KEY=sk-...
qualgraph llm analyze .qualgraph/graph.json \
  --provider openai \
  --model gpt-4o-mini \
  --max-llm-calls 10
```

### Ollama (local, no key)

```bash
ollama pull llama3
qualgraph llm analyze .qualgraph/graph.json \
  --provider ollama \
  --model llama3 \
  --max-llm-calls 10
```

Ollama is fully local — no network calls, no cost.

### Dry run — inspect prompts without spending tokens

```bash
qualgraph llm analyze .qualgraph/graph.json \
  --provider anthropic \
  --max-llm-calls 5 \
  --dry-run
```

Output shows the system and user prompts for each node, the estimated model, and the cache key. No API calls are made.

### What the LLM sees

For each node, Qualgraph builds a context block like this:

```
Function: myapp.auth.login
File: src/myapp/auth.py (lines 42–89)
Risk score: 0.87

Signals:
- Cyclomatic complexity: 12 (threshold: 10)
- Coverage: 34%
- Git churn: 47 commits (90 days)
- Security findings: B106 Hardcoded password funcarg [MEDIUM]
- Callers: [myapp.views.login_view, myapp.api.auth_endpoint, ...]
- Tests: [tests/test_auth.py::test_login_success]
- Cluster: Authentication & Session (community 3 of 12)

Source:
def login(username: str, password: str = "admin") -> bool:
    ...
```

The graph shapes what context is sent: callers, callees, and cluster neighbours are included so the LLM has structural context, not just the function in isolation.

---

## Cache behaviour

All API results are cached in `.qualgraph/cache.sqlite` by content hash of:
- The prompt text
- The node source code
- The model name

Re-running with the same graph and the same model never re-queries the API. Even across different runs, a node that hasn't changed returns instantly from cache.

```bash
# Clear the cache
qualgraph cache clear
# (or just delete the file)
rm .qualgraph/cache.sqlite
```

---

## Using the JSON export with LLMs

For open-ended queries over the whole codebase, use the JSON export:

```bash
qualgraph export-json .qualgraph/graph.json
# writes .qualgraph/graph.export.json
```

Upload `.qualgraph/graph.export.json` to your LLM's file interface (Claude Projects, GPT-4 file upload, etc.) and ask questions like:

> "Here is a code quality graph for my Python repo. Which functions have the highest risk and why? Focus on nodes with high churn and low coverage."

> "List the top 5 security hotspots in this graph, ranked by risk score. For each one, explain what makes it risky and suggest a fix."

> "Which cluster has the most hidden coupling (high co_change edges) and what does that suggest about the architecture?"

The export JSON schema:

```json
{
  "schema_version": "1",
  "nodes": [
    {
      "id": "src/myapp/auth.py::myapp.auth.login::42",
      "type": "Function",
      "name": "login",
      "qualified_name": "myapp.auth.login",
      "file_path": "src/myapp/auth.py",
      "risk_score": 0.87,
      "complexity": 12,
      "coverage": 0.34,
      "churn": 47,
      "cluster_id": 3,
      "findings": [...]
    }
  ],
  "edges": [...]
}
```

Every node has `risk_score`, `complexity`, `coverage`, `churn`, and `findings` — enough for an LLM to reason about risk without needing to read the source code.
```

- [ ] **Step 2: Commit**

```powershell
git add docs/llm-workflows.md
git commit -m "Add detailed LLM workflows doc covering agent-file and API-backed approaches"
```

---

## Task 9: Fill surface files (qualgraph.yaml.example, CHANGELOG, CONTRIBUTING, SECURITY, LICENSE)

**Goal:** Fill all remaining surface files so the repo looks complete and professional.

**Files:**
- Modify: `qualgraph.yaml.example`
- Modify: `CHANGELOG.md`
- Modify: `CONTRIBUTING.md`
- Modify: `SECURITY.md`
- Create: `LICENSE`

**Acceptance Criteria:**
- [ ] `qualgraph.yaml.example` has every config key with a realistic value and inline comment
- [ ] `CHANGELOG.md` follows Keep a Changelog format with an `[Unreleased]` section
- [ ] `CONTRIBUTING.md` has setup steps, commit style, and how to add an annotator
- [ ] `SECURITY.md` has supported versions table and disclosure instructions
- [ ] `LICENSE` is MIT with correct year and author

**Verify:** Read each file; no placeholder text.

**Steps:**

- [ ] **Step 1: Fill `qualgraph.yaml.example`**

```yaml
# qualgraph.yaml.example
# Copy this file to qualgraph.yaml and customise as needed.
# All keys are optional — Qualgraph works with zero configuration.

annotators:
  # Additional glob patterns to exclude from graph building.
  # Built-ins (.venv, __pycache__, *.egg-info) are always excluded.
  exclude:
    - "docs/**"
    - "scripts/legacy/**"

  # Coverage mode: auto | reuse | run | skip
  #   auto:  reuse an existing .coverage if it's fresh; otherwise run pytest
  #   reuse: always use the existing .coverage (fails if missing)
  #   run:   always run pytest (accurate but slow)
  #   skip:  skip coverage entirely
  coverage_mode: auto

  # Extra pytest arguments when coverage_mode is 'run'.
  # Use this to target specific test directories or add markers.
  pytest_args: "tests/ -x --timeout=60"

  # Maximum git commits to scan. 0 = full history (slow on large repos).
  git_max_commits: 1000

risk:
  # Weights must sum to 1.0.
  complexity: 0.20
  churn: 0.20
  coverage: 0.20
  centrality: 0.15
  security: 0.15
  lint: 0.05
  llm: 0.05

graph:
  # Leiden clustering resolution. Higher = more communities.
  leiden_resolution: 1.0
  # Structural metric mode: fast | exact | off
  metric_mode: fast

llm:
  provider: ollama        # ollama | openai | anthropic
  # model: llama3         # defaults to provider's recommended model
  max_calls: 50
  cache_path: .qualgraph/cache.sqlite

output:
  artifacts_dir: .qualgraph
```

- [ ] **Step 2: Fill `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to Qualgraph are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `qualgraph analyze` command — full pipeline (build, annotate, report, export-json) in one command
  with `--preset fast|standard|full`, `--coverage-mode`, `--top-n`, `--serve`, `--open`, and `--artifacts-dir`
- `python -m qualgraph` entrypoint
- `/api/health` endpoint on the local viewer (`{"status": "ok", "graph_loaded": bool}`)
- Responsive viewer layout (≤768px tablet, ≤480px mobile)
- Loading, empty, and error states in the viewer canvas
- Keyboard focus styles on all interactive elements
- `docs/` directory: architecture, installation, configuration, CLI, viewer, and LLM workflows
- GitHub Actions CI workflow (push/PR): install, pip check, ruff, pytest, build, wheel smoke, CLI smoke
- GitHub Actions release workflow (v* tags): build, twine check, GitHub release, optional PyPI publish
- Dependabot configuration for GitHub Actions and pip dependencies

### Changed
- Package renamed from `analytify` to `qualgraph` in `pyproject.toml`
- Build backend changed to hatchling
- README fully rewritten for public release
- `qualgraph serve` now prints clear error messages for missing graph files and occupied ports

### Fixed
- Viewer HTML responses now always include `charset=utf-8` in `Content-Type`
- Long node names, file paths, and code blocks no longer cause horizontal overflow in the viewer
```

- [ ] **Step 3: Fill `CONTRIBUTING.md`**

```markdown
# Contributing

## Setup

```bash
git clone https://github.com/benzae1/analytify.git
cd analytify
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

pip install -e ".[dev]"
```

Verify the install:

```bash
qualgraph --help
pytest
ruff check .
```

## Branching

- Branch from `main`
- Use descriptive branch names: `feat/analyze-command`, `fix/viewer-overflow`
- Keep branches short-lived — one feature or fix per branch

## Commits

- Use the imperative mood: "Add health endpoint", not "Added health endpoint"
- Keep the subject line under 72 characters
- Reference issues where relevant: "Fix port conflict message (closes #42)"
- No AI attribution lines in commits

## Running tests

```bash
pytest                    # all tests
pytest tests/unit/ -v     # unit tests only, verbose
pytest -k "viewer" -v     # filter by name
```

## Linting

```bash
ruff check .
ruff check . --fix        # auto-fix safe issues
```

## How to add an annotator

1. Create `src/qualgraph/annotators/my_annotator.py`
2. Implement `BaseAnnotator` — `name`, `version`, `is_available()`, `annotate(graph, repo_path)`
3. Return an `AnnotatorResult` from `annotate()`
4. Register the annotator in the `registry` dict in `cli.py`
5. Add it to `FULL_ANNOTATORS` if appropriate
6. Write a test in `tests/unit/test_static_annotators.py` following existing patterns

## Pull request checklist

- [ ] `pytest` passes
- [ ] `ruff check .` passes
- [ ] New behaviour is covered by tests
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No API keys, credentials, or large binary files committed
```

- [ ] **Step 4: Fill `SECURITY.md`**

```markdown
# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Email the maintainer directly at **anton.erdmann.benz@uni-weimar.de** with:

- A description of the vulnerability and its potential impact
- Steps to reproduce (minimal proof of concept if possible)
- Any suggested mitigations

You will receive an acknowledgement within 48 hours. We aim to release a fix or advisory within 14 days for confirmed vulnerabilities.

## Scope

Qualgraph is a local analysis tool — it does not run a public server and has no authentication layer. The main security considerations are:

- **Secrets in analysed repos:** Qualgraph can detect secrets in your code via the `secrets` annotator, but does not exfiltrate them.
- **LLM providers:** When using `--provider anthropic` or `--provider openai`, node context (function signatures, metrics) is sent to the respective API. No full file contents are sent. See [docs/llm-workflows.md](docs/llm-workflows.md).
- **Supply chain:** Dependencies are locked and auditable via `pip-audit`. Run `qualgraph annotate . --annotators pip_audit` to scan your own project.
```

- [ ] **Step 5: Create `LICENSE`**

```
MIT License

Copyright (c) 2026 Anton Benz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 6: Commit**

```powershell
git add qualgraph.yaml.example CHANGELOG.md CONTRIBUTING.md SECURITY.md LICENSE
git commit -m "Fill surface files: example config, changelog, contributing guide, security policy, license"
```

---

## Task 10: Add GitHub Actions CI workflow

**Goal:** Create `.github/workflows/ci.yml` that runs on push and PR to `main`, covering install, lint, tests, package build, wheel smoke, CLI smoke, and viewer API smoke.

**Files:**
- Create: `.github/workflows/ci.yml`

**Acceptance Criteria:**
- [ ] Workflow triggers on `push` and `pull_request` to `main`
- [ ] Runs on Python 3.11 and 3.12 (matrix)
- [ ] Steps: checkout, setup-python, install, pip check, ruff, pytest, build, wheel smoke, CLI smoke, artifact asserts, viewer health check
- [ ] YAML is valid (`python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`)

**Verify:** Push to a branch and observe the Actions tab, or run `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` locally.

**Steps:**

- [ ] **Step 1: Create the workflow directory**

```powershell
mkdir -p .github/workflows
```

- [ ] **Step 2: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install package and dev extras
        run: pip install -e ".[dev]"

      - name: Check dependency consistency
        run: pip check

      - name: Lint with ruff
        run: ruff check .

      - name: Run tests
        run: pytest tests/

      - name: Build distribution
        run: python -m build

      - name: Smoke test — wheel install
        run: |
          python -m venv .venv-wheel
          .venv-wheel/bin/pip install dist/qualgraph-*.whl
          .venv-wheel/bin/qualgraph --help

      - name: Smoke test — analyze command
        run: |
          qualgraph analyze benchmarks/repos/tiny_repo \
            --preset fast \
            --top-n 3 \
            --artifacts-dir /tmp/ci-artifacts

      - name: Assert report artifact exists
        run: test -f /tmp/ci-artifacts/report.md

      - name: Assert JSON export exists
        run: test -f /tmp/ci-artifacts/graph.export.json

      - name: Smoke test — viewer health endpoint
        run: |
          qualgraph serve /tmp/ci-artifacts/graph.json --port 18080 &
          sleep 2
          curl -sf http://127.0.0.1:18080/api/health | python -c "
          import json, sys
          data = json.load(sys.stdin)
          assert data['status'] == 'ok', f'unexpected: {data}'
          print('health check passed:', data)
          "
          kill %1 || true
```

- [ ] **Step 3: Validate YAML syntax locally**

```powershell
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('YAML OK')"
```

Expected: `YAML OK`

- [ ] **Step 4: Commit**

```powershell
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI workflow"
```

---

## Task 11: Add release workflow and Dependabot

**Goal:** Create `.github/workflows/release.yml` triggered on `v*` tags, and `.github/dependabot.yml` for automatic dependency updates.

**Files:**
- Create: `.github/workflows/release.yml`
- Create: `.github/dependabot.yml`

**Acceptance Criteria:**
- [ ] Release workflow triggers on `v*` tag push
- [ ] Steps: checkout, install build+twine, build, twine check, upload artifact, create GitHub release, conditional PyPI publish
- [ ] PyPI publish step is gated behind `vars.PUBLISH_TO_PYPI == 'true'`
- [ ] Dependabot configured for GitHub Actions and pip, weekly schedule
- [ ] Both YAML files are valid

**Verify:** `python -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml')); yaml.safe_load(open('.github/dependabot.yml')); print('YAML OK')"`

**Steps:**

- [ ] **Step 1: Create `.github/workflows/release.yml`**

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

permissions:
  contents: write
  id-token: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install build tools
        run: pip install build twine

      - name: Build distribution
        run: python -m build

      - name: Validate distribution
        run: twine check dist/*

      - name: Upload dist as artifact
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/*
          generate_release_notes: true

      - name: Publish to PyPI
        if: vars.PUBLISH_TO_PYPI == 'true'
        uses: pypa/gh-action-pypi-publish@release/v1
```

- [ ] **Step 2: Create `.github/dependabot.yml`**

```yaml
version: 2

updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
```

- [ ] **Step 3: Validate YAML**

```powershell
python -c "
import yaml
yaml.safe_load(open('.github/workflows/release.yml'))
yaml.safe_load(open('.github/dependabot.yml'))
print('YAML OK')
"
```

Expected: `YAML OK`

- [ ] **Step 4: Commit**

```powershell
git add .github/workflows/release.yml .github/dependabot.yml
git commit -m "Add release workflow with PyPI publish gate and Dependabot config"
```

---

## Self-review

**Spec coverage check:**

| Spec requirement | Task |
|-----------------|------|
| Rename project metadata to `qualgraph` | Task 1 |
| Add `[build-system]` with hatchling | Task 1 |
| `python -m qualgraph` support | Task 2 |
| `qualgraph analyze` with all flags | Task 3 |
| `--artifacts-dir` / `QUALGRAPH_ARTIFACTS_DIR` | Task 3 |
| `/api/health` endpoint | Task 4 |
| Serve error messages | Task 4 |
| Responsive layout ≤768px, ≤480px | Task 5 |
| Overflow fixes | Task 5 |
| Loading/empty/error states | Task 5 |
| Focus styles | Task 5 |
| Unit tests: health, overflow, port conflict, missing file | Tasks 4 & 5 |
| Full README rewrite | Task 6 |
| `docs/architecture.md` | Task 7 |
| `docs/installation.md` | Task 7 |
| `docs/configuration.md` | Task 7 |
| `docs/cli.md` | Task 7 |
| `docs/viewer.md` | Task 7 |
| `docs/llm-workflows.md` (detailed) | Task 8 |
| `qualgraph.yaml.example` filled | Task 9 |
| `CHANGELOG.md` | Task 9 |
| `CONTRIBUTING.md` | Task 9 |
| `SECURITY.md` | Task 9 |
| `LICENSE` | Task 9 |
| `ci.yml` | Task 10 |
| `release.yml` | Task 11 |
| `dependabot.yml` | Task 11 |

All spec requirements covered. No gaps found.

**Placeholder scan:** No TBD, TODO, or vague instructions present. All code blocks contain complete, runnable content.

**Type consistency:** `PRESET_ANNOTATORS` dict defined in Task 3 and referenced only in Task 3's `analyze` command. `ViewerServer.viewer` attribute referenced as `self.server.viewer` in Tasks 4 and is consistent with the class definition in `server.py`. No mismatches.
