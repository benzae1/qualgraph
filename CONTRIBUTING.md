# Contributing

Thanks for improving Qualgraph.

## Development Setup

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
```

## Checks

Run these before opening a pull request:

```bash
python -m ruff check .
python -m pytest
python -m build
python -m twine check dist/*
```

Viewer e2e tests require Chromium:

```bash
python -m playwright install chromium
python -m pytest tests/e2e -q
```

After code changes in this repository, refresh the repo graph:

```bash
graphify update .
```

## Pull Request Guidelines

- Keep changes focused.
- Add tests for new behavior.
- Update docs when public commands, configuration, outputs, or workflows change.
- Do not commit generated `.qualgraph/`, `.pytest_cache/`, `.ruff_cache/`, or virtual environment files.
