# Configuration

`qualgraph.yaml.example` shows the intended configuration shape. The current CLI
also supports direct flags for all commonly used settings.

Recommended project defaults:

```yaml
analysis:
  preset: standard
  output_dir: .qualgraph
  artifacts_dir: .qualgraph/runs
  top_n: 10
  metric_mode: fast
  coverage_mode: auto

repository:
  exclude:
    - .venv/**
    - .git/**
    - .qualgraph/**
    - build/**
    - dist/**
```

Coverage-context test linkage is strongest when coverage.py records dynamic test
contexts:

```ini
[run]
branch = True
dynamic_context = test_function
```

Use `--coverage-mode run` to let Qualgraph create a temporary coverage rcfile
and run pytest with context recording.
