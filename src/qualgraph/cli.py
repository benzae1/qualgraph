"""Command-line interface for qualgraph."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from qualgraph.graph.builder import build_graph
from qualgraph.graph.clustering import annotate_clusters
from qualgraph.graph.metrics import annotate_metrics
from qualgraph.graph.serialize import write_graphml_graph, write_json_graph
from qualgraph.logging import RunLogger


app = typer.Typer(help="Graph-aware code quality analysis for Python projects.")


@app.callback()
def main() -> None:
    """Graph-aware code quality analysis for Python projects."""


@app.command()
def build(
    repo: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
    output: Path = typer.Option(Path("qualgraph.graph.json"), "--output", "-o", help="Annotated JSON graph path."),
    graphml: Optional[Path] = typer.Option(None, "--graphml", help="Optional GraphML export path."),
    exclude: list[str] = typer.Option([], "--exclude", "-x", help="Additional glob to exclude."),
    resolution: float = typer.Option(1.0, "--resolution", help="Leiden clustering resolution."),
) -> None:
    """Build a Python code graph and write an annotated graph artifact."""

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
