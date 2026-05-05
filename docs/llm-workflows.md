# LLM Workflows

Qualgraph supports two LLM modes.

## Agent File Workflow

This mode works with subscription LLM tools and does not require API keys.

```bash
qualgraph llm export-tasks .qualgraph/annotated.graph.json --limit 20
```

Qualgraph writes task Markdown files and a manifest under
`.qualgraph/runs/<run_id>/llm_tasks/`. An agent reads the tasks and writes JSON
results under the sibling `llm_results/` directory.

Import results:

```bash
qualgraph llm import-results .qualgraph/runs/<run_id> \
  --graph .qualgraph/annotated.graph.json \
  --output .qualgraph/final.graph.json
```

Then render a final report:

```bash
qualgraph report .qualgraph/final.graph.json --output .qualgraph/report.md
```

## API-Backed Workflow

```bash
qualgraph llm analyze .qualgraph/annotated.graph.json --provider ollama --dry-run
qualgraph llm analyze .qualgraph/annotated.graph.json --provider openai --model gpt-4o-mini
qualgraph llm analyze .qualgraph/annotated.graph.json --provider anthropic --model claude-3-5-sonnet-latest
```

API-backed analysis is limited to top-risk nodes to control cost and context
size. Ollama runs locally and has zero provider cost.
