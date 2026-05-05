# Agent Skill

Qualgraph ships with a repo-local skill definition at [`.agents/skills/qualgraph/SKILL.md`](../.agents/skills/qualgraph/SKILL.md).

Use this when you want an LLM coding agent such as Codex to run the full Qualgraph workflow as a reusable skill instead of manually typing each command.

## What The Skill Does

The skill guides an agent through:

1. Preparing a working Python environment.
2. Building a code graph.
3. Annotating the graph with quality signals.
4. Exporting LLM task files for the highest-risk nodes.
5. Completing those task files with structured JSON findings.
6. Importing the results back into the graph.
7. Rendering a final Markdown report.

It is designed for local, agent-driven analysis and does not require API keys.

## Repo-Local Usage

If the agent is running inside this repository, no extra installation is needed. The skill already lives under `.agents/skills/qualgraph`.

Typical prompts:

- `Use the qualgraph skill on this repo.`
- `Run /qualgraph on . and summarize the top findings.`
- `Use the qualgraph skill on C:\path\to\target-repo`

## Global Installation For Codex

If you want to reuse the skill across repositories in Codex, copy the skill directory into your Codex skills home.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force $HOME\.codex\skills\qualgraph | Out-Null
Copy-Item .agents\skills\qualgraph\* $HOME\.codex\skills\qualgraph -Recurse -Force
```

macOS/Linux:

```bash
mkdir -p ~/.codex/skills/qualgraph
cp -R .agents/skills/qualgraph/* ~/.codex/skills/qualgraph/
```

After that, a Codex session can use the skill from any repository with prompts such as:

- `Use the qualgraph skill on .`
- `Use the qualgraph skill on ~/src/my-project and write the report`

## Skill Inputs

The skill accepts either:

- the current repository via `.`
- an explicit target path

If no path is given, the skill defaults to the current working directory.

## Expected Outputs

The skill writes its analysis under `.qualgraph/`, including:

- `.qualgraph/graph.json`
- `.qualgraph/annotated.graph.json`
- `.qualgraph/final.graph.json`
- `.qualgraph/report.md`
- `.qualgraph/runs/<run_id>/...`

## Recommended Agent Prompt

For the most consistent behavior, ask the agent for both execution and summary in one request:

```text
Use the qualgraph skill on this repository, generate the final report, and summarize the highest-signal risks.
```

## Notes

- The skill prefers an existing `.venv` when one is available.
- On Windows it uses `.venv\Scripts\qualgraph`; on Unix-like systems it uses `.venv/bin/qualgraph`.
- Coverage-aware analysis is optional. The default fast path does not require running tests.
- If `.qualgraph/runs` is not writable, Qualgraph falls back to the configured artifacts directory or a temp directory.
