# CLI Reference

## Full Workflow

```bash
qualgraph analyze <repo> [options]
```

Important options:

- `--preset fast|standard|full`: choose the annotator set.
- `--coverage-mode auto|reuse|run|skip`: control coverage ingestion.
- `--top-n <count>`: report and viewer risk-node count.
- `--output-dir <path>`: output directory for graph, report, and export files.
- `--artifacts-dir <path>`: run-log directory.
- `--serve`: serve the generated viewer after analysis.
- `--open`: open the generated viewer; implies serving it.

Default outputs are written under `.qualgraph/`.

## Focused Commands

```bash
qualgraph build <repo> --output .qualgraph/graph.json
qualgraph annotate <repo> --graph .qualgraph/graph.json --output .qualgraph/annotated.graph.json
qualgraph report .qualgraph/annotated.graph.json --output .qualgraph/report.md
qualgraph export-json .qualgraph/annotated.graph.json --output .qualgraph/export.json
qualgraph serve .qualgraph/annotated.graph.json --open
```

## Annotator Presets

- `fast`: `radon`, `ruff`, `docstring`, `cross_signal`
- `standard`: `fast` plus `git`
- `full`: `standard` plus `vulture`, `security`, and `coverage`

## Run Logs

Run logs are JSON files under `.qualgraph/runs/<run_id>/` by default. Set
`QUALGRAPH_ARTIFACTS_DIR` or pass `--artifacts-dir` if the default location is
not writable.
