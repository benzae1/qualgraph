# Installation

Qualgraph requires Python 3.11 or 3.12.

## From Git

Until PyPI publishing is enabled, install from the current GitHub repository:

```bash
python -m pip install "git+https://github.com/benzae1/qualgraph.git"
qualgraph --help
python -m qualgraph --help
```

## Editable Development Install

```bash
git clone https://github.com/benzae1/qualgraph.git
cd qualgraph
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
git clone https://github.com/benzae1/qualgraph.git
cd qualgraph
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
```

## Verify The Install

```bash
python -m pip check
qualgraph --help
python -m qualgraph --help
qualgraph analyze benchmarks/repos/tiny_repo --preset fast --coverage-mode skip --top-n 5
```

## Optional Tool Notes

The default package installs the analyzers Qualgraph can orchestrate: Ruff,
Radon, Vulture, Bandit, pip-audit, detect-secrets, coverage.py, and GitPython.
Some annotators are best-effort. If a tool cannot run against a target repo,
Qualgraph records the failure in the run log and continues with the remaining
signals.
