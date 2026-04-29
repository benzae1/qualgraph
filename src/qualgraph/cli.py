"""Command-line interface for qualgraph."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

import typer

from qualgraph.annotators.bandit import BanditAnnotator
from qualgraph.annotators.co_change import CoChangeAnnotator
from qualgraph.annotators.coverage import CoverageAnnotator
from qualgraph.annotators.cross_signal import CrossSignalAnnotator
from qualgraph.annotators.docstring import DocstringAnnotator
from qualgraph.annotators.git_history import GitHistoryAnnotator
from qualgraph.annotators.pipeline import run_pipeline
from qualgraph.annotators.pip_audit import PipAuditAnnotator
from qualgraph.annotators.profiler import ProfilerAnnotator
from qualgraph.annotators.radon import RadonAnnotator
from qualgraph.annotators.ruff import RuffAnnotator
from qualgraph.annotators.secrets import SecretsAnnotator
from qualgraph.annotators.test_linkage import TestLinkageAnnotator
from qualgraph.annotators.vulture import VultureAnnotator
from qualgraph.cache.sqlite import Cache
from qualgraph.graph.builder import build_graph
from qualgraph.graph.clustering import annotate_clusters
from qualgraph.graph.metrics import annotate_metrics
from qualgraph.graph.serialize import read_json_graph, write_graphml_graph, write_json_graph
from qualgraph.llm.analyzer import analyze_top_n
from qualgraph.llm.client import LLMProvider, LLMRequest, LLMResponse
from qualgraph.llm.providers import AnthropicProvider, OllamaProvider, OpenAIProvider
from qualgraph.llm.tasks import export_tasks as export_llm_tasks
from qualgraph.llm.tasks import import_results as import_llm_results
from qualgraph.logging import RunLogger
from qualgraph.report.markdown import write_markdown_report
from qualgraph.scoring.risk import score as score_risk


app = typer.Typer(help="Graph-aware code quality analysis for Python projects.")
llm_app = typer.Typer(help="Export and import agent-completed LLM analysis tasks.")
app.add_typer(llm_app, name="llm")


@app.callback()
def main() -> None:
    """Graph-aware code quality analysis for Python projects."""


@app.command()
def build(
    repo: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Annotated JSON graph path."),
    graphml: Optional[Path] = typer.Option(None, "--graphml", help="Optional GraphML export path."),
    exclude: list[str] = typer.Option([], "--exclude", "-x", help="Additional glob to exclude."),
    resolution: float = typer.Option(1.0, "--resolution", help="Leiden clustering resolution."),
) -> None:
    """Build a Python code graph and write an annotated graph artifact."""

    output = output or Path(f"{repo.name}.graph.json")
    run_logger = RunLogger(repo_path=repo)
    try:
        with run_logger.span("build_graph") as span:
            graph = build_graph(repo, exclude)
            span["nodes"] = graph.number_of_nodes()
            span["edges"] = graph.number_of_edges()

        with run_logger.span("annotate_clusters") as span:
            clusters = annotate_clusters(graph, resolution=resolution)
            span["cluster_count"] = len(set(clusters.values()))

        with run_logger.span("annotate_metrics") as span:
            annotate_metrics(graph)
            span["nodes"] = graph.number_of_nodes()

        with run_logger.span("score_risk") as span:
            score_risk(graph)
            span["nodes"] = graph.number_of_nodes()

        with run_logger.span("write_json_graph", output=output):
            write_json_graph(graph, output)

        if graphml is not None:
            with run_logger.span("write_graphml_graph", output=graphml):
                write_graphml_graph(graph, graphml)
    finally:
        summary = run_logger.finish()

    typer.echo(
        f"Wrote {output} "
        f"({graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges, "
        f"{graph.graph.get('cluster_count', 0)} clusters). "
        f"Run log: {summary.run_id}"
    )


@app.command()
def annotate(
    repo: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
    graph_path: Optional[Path] = typer.Option(None, "--graph", "-g", help="Existing graph JSON path."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Annotated graph JSON path."),
    annotators: str = typer.Option("radon,ruff,coverage,git", "--annotators", help="Comma-separated annotator names."),
    profile_json: Optional[Path] = typer.Option(None, "--profile-json", help="cProfile JSON artifact for the profiler annotator."),
) -> None:
    """Run annotators over a graph, building the graph first if needed."""

    graph_path = graph_path or Path(f"{repo.name}.graph.json")
    output = output or graph_path
    run_logger = RunLogger(repo_path=repo)
    try:
        if graph_path.exists():
            graph = read_json_graph(graph_path)
        else:
            graph = build_graph(repo, [])
            annotate_clusters(graph)
            annotate_metrics(graph)

        selected = _resolve_annotators(annotators, profile_json=profile_json)
        results = run_pipeline(graph, repo, selected, logger=run_logger)
        with run_logger.span("score_risk") as span:
            score_risk(graph)
            span["nodes"] = graph.number_of_nodes()
        with run_logger.span("write_json_graph", output=output):
            write_json_graph(graph, output)
    finally:
        summary = run_logger.finish()

    typer.echo(
        f"Annotated {output} with {len(results)} result(s). "
        f"Run log: {summary.run_id}"
    )


@app.command()
def report(
    graph: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Markdown report path."),
) -> None:
    """Render a Markdown report from an annotated graph JSON file."""

    output = output or graph.with_suffix(".report.md")
    code_graph = read_json_graph(graph)
    write_markdown_report(code_graph, output)
    typer.echo(f"Wrote {output}")


@llm_app.command("export-tasks")
def llm_export_tasks(
    graph: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-o", help="Directory for LLM task files."),
    limit: int = typer.Option(20, "--limit", "-n", min=1, help="Number of top-risk nodes to export."),
) -> None:
    """Export top-risk node prompts for an agent to complete from files."""

    code_graph = read_json_graph(graph)
    task_dir = output_dir or _default_llm_task_dir()
    manifest = export_llm_tasks(code_graph, task_dir, limit=limit)
    typer.echo(
        f"Wrote {len(manifest['tasks'])} LLM task(s) to {manifest['task_dir']}. "
        f"Results directory: {manifest['result_dir']}"
    )


@llm_app.command("import-results")
def llm_import_results(
    run_dir: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
    graph: Path = typer.Option(..., "--graph", "-g", exists=True, file_okay=True, dir_okay=False, readable=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Graph path to write after importing results."),
    strict: bool = typer.Option(False, "--strict", help="Fail if any expected result file is missing."),
) -> None:
    """Import agent-written LLM result JSON files back into a graph."""

    code_graph = read_json_graph(graph)
    summary = import_llm_results(code_graph, run_dir, strict=strict)
    output = output or graph
    write_json_graph(code_graph, output)
    typer.echo(
        f"Imported {summary['findings_added']} LLM finding(s) from "
        f"{summary['imported']}/{summary['tasks']} completed task(s). "
        f"Wrote {output}."
    )


@llm_app.command("analyze")
def llm_analyze(
    graph: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Graph path to write after analysis."),
    max_llm_calls: int = typer.Option(20, "--max-llm-calls", min=0, help="Maximum top-risk nodes to analyze."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print prompts without calling an LLM or writing output."),
    provider_name: str = typer.Option("ollama", "--provider", help="Provider: ollama, openai, or anthropic."),
    model: Optional[str] = typer.Option(None, "--model", help="Provider model id override."),
    cache_path: Path = typer.Option(Path(".qualgraph/cache.sqlite"), "--cache", help="SQLite LLM cache path."),
) -> None:
    """Run provider-backed LLM analysis over the highest-risk graph nodes."""

    code_graph = read_json_graph(graph)
    provider = _resolve_provider(provider_name, model, dry_run=dry_run)
    run_logger = RunLogger(repo_path=Path("."))
    try:
        if dry_run:
            summary = analyze_top_n(
                code_graph,
                top_n=max_llm_calls,
                provider=provider,
                cache=_NoopCache(),
                logger=run_logger,
                dry_run=dry_run,
            )
            _print_dry_run(summary.dry_run_tasks)
        else:
            with Cache(cache_path) as cache:
                summary = analyze_top_n(
                    code_graph,
                    top_n=max_llm_calls,
                    provider=provider,
                    cache=cache,
                    logger=run_logger,
                )
            output = output or graph
            write_json_graph(code_graph, output)
    finally:
        run_summary = run_logger.finish()

    if dry_run:
        typer.echo(
            f"Dry run printed {summary.ranked} LLM prompt(s). "
            f"No provider calls made. Run log: {run_summary.run_id}"
        )
    else:
        typer.echo(
            f"Analyzed {summary.analyzed} node(s): {summary.llm_calls} LLM call(s), "
            f"{summary.cache_hits} cache hit(s), {summary.findings_added} finding(s). "
            f"Wrote {output}. Run log: {run_summary.run_id}"
        )


def _resolve_annotators(names: str, profile_json: Path | None = None) -> list:
    registry = {
        "radon": RadonAnnotator,
        "ruff": RuffAnnotator,
        "vulture": VultureAnnotator,
        "bandit": BanditAnnotator,
        "docstring": DocstringAnnotator,
        "coverage": (CoverageAnnotator, TestLinkageAnnotator),
        "coverage_only": CoverageAnnotator,
        "test_linkage": TestLinkageAnnotator,
        "tests": TestLinkageAnnotator,
        "pip_audit": PipAuditAnnotator,
        "pipaudit": PipAuditAnnotator,
        "secrets": SecretsAnnotator,
        "security": (BanditAnnotator, PipAuditAnnotator, SecretsAnnotator),
        "git": (GitHistoryAnnotator, CoChangeAnnotator),
        "git_history": GitHistoryAnnotator,
        "co_change": CoChangeAnnotator,
        "cross_signal": CrossSignalAnnotator,
        "cross-signal": CrossSignalAnnotator,
        "derived": CrossSignalAnnotator,
        "profiler": lambda: ProfilerAnnotator(profile_json),
        "profile": lambda: ProfilerAnnotator(profile_json),
    }
    selected = []
    for raw_name in names.split(","):
        name = raw_name.strip()
        if not name:
            continue
        annotator = registry.get(name)
        if annotator is None:
            raise typer.BadParameter(f"unknown annotator: {name}")
        if isinstance(annotator, tuple):
            selected.extend(item() for item in annotator)
        elif callable(annotator) and not isinstance(annotator, type):
            selected.append(annotator())
        else:
            selected.append(annotator())
    return selected


def _default_llm_task_dir() -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    return Path(".qualgraph") / "runs" / run_id / "llm_tasks"


def _resolve_provider(name: str, model: str | None, dry_run: bool = False) -> LLMProvider:
    normalized = name.strip().lower()
    if dry_run:
        return _DryRunProvider(_default_model(normalized, model))
    if normalized == "ollama":
        return OllamaProvider(model=model or "llama3.1")
    if normalized == "openai":
        return OpenAIProvider(model=model or "gpt-4o-mini")
    if normalized == "anthropic":
        return AnthropicProvider(model=model or "claude-3-5-sonnet-latest")
    raise typer.BadParameter(f"unknown LLM provider: {name}")


def _default_model(provider_name: str, model: str | None) -> str:
    if model:
        return model
    return {
        "ollama": "llama3.1",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-sonnet-latest",
    }.get(provider_name, provider_name or "dry-run")


def _print_dry_run(tasks: list[dict]) -> None:
    for index, task in enumerate(tasks, start=1):
        typer.echo(f"\n--- LLM dry run task {index}: {task['node_id']} ---")
        typer.echo(f"model: {task['model']}")
        typer.echo(f"risk_score: {task['risk_score']}")
        typer.echo(f"cache_key: {task['cache_key']}")
        typer.echo("\nSYSTEM:\n")
        typer.echo(task["system"])
        typer.echo("\nUSER:\n")
        typer.echo(task["user"])


class _DryRunProvider(LLMProvider):
    def __init__(self, model_id: str) -> None:
        self._model_id = model_id

    @property
    def model_id(self) -> str:
        return self._model_id

    def complete(self, req: LLMRequest) -> LLMResponse:
        raise RuntimeError("dry-run provider must not be called")


class _NoopCache:
    def get(self, _key: str) -> None:
        return None

    def put(self, _key: str, _response: object) -> None:
        return None
