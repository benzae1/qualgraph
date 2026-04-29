---
name: qualgraph
description: "Run Qualgraph on a Python repository end to end: build and annotate the code graph, export top-risk LLM task files, complete those task files using the current agent session, import the structured results, and render a final report. Use when the user asks for /qualgraph, code quality graph analysis, risk-ranked findings, or a finalized Qualgraph report without requiring API keys."
---

# Qualgraph

Use this skill to run a full Qualgraph analysis from local commands plus agent-completed LLM task files.

## Workflow

Use the requested path, or `.` if no path was provided.

1. Ensure the project environment works.
   - Prefer an existing `.venv`.
   - If none exists, create one and install the project/test dependencies.
   - On Windows, use `.venv\Scripts\qualgraph`; otherwise use `.venv/bin/qualgraph`.

2. Build the graph:
   ```powershell
   .venv\Scripts\qualgraph build INPUT_PATH --output .qualgraph\graph.json
   ```

3. Annotate the graph:
   ```powershell
   .venv\Scripts\qualgraph annotate INPUT_PATH --graph .qualgraph\graph.json --output .qualgraph\annotated.graph.json --annotators radon,ruff,coverage,git,security
   ```

4. Export LLM tasks:
   ```powershell
   .venv\Scripts\qualgraph llm export-tasks .qualgraph\annotated.graph.json --limit 20
   ```

5. Complete the task files yourself.
   - Read `.qualgraph/runs/<run_id>/llm_tasks/manifest.json`.
   - For each task, read the referenced Markdown task file.
   - Write valid JSON to the task's `output_path`.
   - The JSON must be:
     ```json
     {
       "findings": [
         {
           "kind": "short_snake_case",
           "severity": "LOW|MEDIUM|HIGH",
           "confidence": "EXTRACTED|INFERRED|AMBIGUOUS",
           "message": "one sentence",
           "evidence": {"key": "value"},
           "suggested_action": "one sentence",
           "line": 123
         }
       ]
     }
     ```
   - If no meaningful issue is present, write `{"findings": []}`.
   - Do not ask the user to copy or paste prompts.

6. Import LLM results:
   ```powershell
   .venv\Scripts\qualgraph llm import-results .qualgraph\runs\<run_id> --graph .qualgraph\annotated.graph.json --output .qualgraph\final.graph.json
   ```

7. Render the final report:
   ```powershell
   .venv\Scripts\qualgraph report .qualgraph\final.graph.json --output .qualgraph\report.md
   ```

8. Return the final report path and a concise summary of the highest-signal findings.

## Validation

Before finishing, run tests when feasible:

```powershell
$env:PYTHONPATH='src;benchmarks/repos/tiny_repo'
.venv\Scripts\python -m pytest
```

Also verify that report generation succeeded and `.qualgraph\report.md` exists.
