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
from qualgraph.annotators.docstring import DocstringAnnotator
from qualgraph.annotators.git_history import GitHistoryAnnotator
from qualgraph.annotators.pipeline import run_pipeline
from qualgraph.annotators.pip_audit import PipAuditAnnotator
from qualgraph.annotators.radon import RadonAnnotator
from qualgraph.annotators.ruff import RuffAnnotator
from qualgraph.annotators.secrets import SecretsAnnotator
from qualgraph.annotators.test_linkage import TestLinkageAnnotator
from qualgraph.annotators.vulture import VultureAnnotator
from qualgraph.graph.builder import build_graph
from qualgraph.graph.clustering import annotate_clusters
from qualgraph.graph.metrics import annotate_metrics
from qualgraph.graph.serialize import read_json_graph, write_graphml_graph, write_json_graph
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

        selected = _resolve_annotators(annotators)
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


def _resolve_annotators(names: str) -> list:
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
        else:
            selected.append(annotator())
    return selected


def _default_llm_task_dir() -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    return Path(".qualgraph") / "runs" / run_id / "llm_tasks"
