"""Structural metrics and cluster role heuristics."""

from __future__ import annotations

from collections import defaultdict
from statistics import median

import networkx as nx


EXACT_BETWEENNESS_NODE_LIMIT = 500
DEFAULT_BETWEENNESS_SAMPLES = 128


def annotate_metrics(
    g: nx.DiGraph,
    *,
    betweenness_samples: int | None = DEFAULT_BETWEENNESS_SAMPLES,
    exact_betweenness_node_limit: int = EXACT_BETWEENNESS_NODE_LIMIT,
    include_betweenness: bool = True,
) -> None:
    """Write structural metrics back onto graph nodes.

    Betweenness is useful for bridge-finding, but it is often exactly zero in
    small sparse code graphs. ``centrality`` is therefore a composite structural
    score for ranking, while raw betweenness remains available separately.
    """

    if g.number_of_nodes() == 0:
        return

    bw = _betweenness(
        g,
        samples=betweenness_samples,
        exact_node_limit=exact_betweenness_node_limit,
        enabled=include_betweenness,
    )

    degree = _degree_centrality(g)
    pagerank = _pagerank(g)
    structural_scores = _structural_scores(bw, degree, pagerank)
    in_degrees = dict(g.in_degree())
    out_degrees = dict(g.out_degree())

    for node_id in g.nodes:
        g.nodes[node_id]["betweenness_centrality"] = float(bw.get(node_id, 0.0))
        g.nodes[node_id]["degree_centrality"] = float(degree.get(node_id, 0.0))
        g.nodes[node_id]["pagerank"] = float(pagerank.get(node_id, 0.0))
        g.nodes[node_id]["structural_score"] = float(structural_scores.get(node_id, 0.0))
        g.nodes[node_id]["centrality"] = float(structural_scores.get(node_id, 0.0))
        g.nodes[node_id]["in_degree"] = int(in_degrees.get(node_id, 0))
        g.nodes[node_id]["out_degree"] = int(out_degrees.get(node_id, 0))

    annotate_cluster_roles(g)
    betweenness_mode = (
        "disabled"
        if not include_betweenness
        else "exact"
        if g.number_of_nodes() <= exact_betweenness_node_limit
        else "sampled"
    )
    g.graph["metrics"] = {
        "betweenness": betweenness_mode,
        "betweenness_samples": _betweenness_samples_used(g, betweenness_mode, betweenness_samples),
    }


def annotate_cluster_roles(g: nx.DiGraph) -> None:
    """Classify each node's role within its cluster using simple topology."""

    if g.number_of_nodes() == 0:
        return

    clusters: dict[int | str, list[str]] = defaultdict(list)
    pipeline_nodes = _pipeline_nodes(g)
    for node_id, data in g.nodes(data=True):
        clusters[data.get("cluster_id", "unclustered")].append(node_id)

    for node_ids in clusters.values():
        in_values = [int(g.nodes[node_id].get("in_degree") or 0) for node_id in node_ids]
        out_values = [int(g.nodes[node_id].get("out_degree") or 0) for node_id in node_ids]
        centrality_values = [float(g.nodes[node_id].get("centrality") or 0.0) for node_id in node_ids]
        high_in = max(3, _percentile(in_values, 0.75))
        high_out = max(3, _percentile(out_values, 0.75))
        centrality_floor = median(centrality_values) if centrality_values else 0.0

        for node_id in node_ids:
            in_degree = int(g.nodes[node_id].get("in_degree") or 0)
            out_degree = int(g.nodes[node_id].get("out_degree") or 0)
            centrality = float(g.nodes[node_id].get("centrality") or 0.0)
            g.nodes[node_id]["cluster_role"] = _cluster_role(
                in_degree=in_degree,
                out_degree=out_degree,
                centrality=centrality,
                high_in=high_in,
                high_out=high_out,
                centrality_floor=centrality_floor,
                is_pipeline_node=node_id in pipeline_nodes,
            )


def _cluster_role(
    in_degree: int,
    out_degree: int,
    centrality: float,
    high_in: int,
    high_out: int,
    centrality_floor: float,
    is_pipeline_node: bool,
) -> str:
    if out_degree >= high_out and centrality >= centrality_floor:
        return "hub"
    if in_degree >= high_in and out_degree <= 1:
        return "utility"
    if is_pipeline_node:
        return "pipeline"
    if in_degree == 0 and out_degree == 0:
        return "isolated"
    return "member"


def _pipeline_nodes(g: nx.DiGraph) -> set[str]:
    undirected = g.to_undirected(as_view=True)
    in_degrees = dict(g.in_degree())
    out_degrees = dict(g.out_degree())
    pipeline_nodes: set[str] = set()
    for component in nx.connected_components(undirected):
        if len(component) < 3:
            continue
        if all(in_degrees.get(node, 0) <= 1 and out_degrees.get(node, 0) <= 1 for node in component):
            pipeline_nodes.update(component)
    return pipeline_nodes


def _percentile(values: list[int], percentile: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = round((len(ordered) - 1) * percentile)
    return ordered[index]


def _degree_centrality(g: nx.DiGraph) -> dict[str, float]:
    if g.number_of_nodes() <= 1:
        return {node_id: 0.0 for node_id in g.nodes}
    denominator = 2 * (g.number_of_nodes() - 1)
    return {node_id: float(g.degree(node_id)) / denominator for node_id in g.nodes}


def _betweenness(
    g: nx.DiGraph,
    *,
    samples: int | None,
    exact_node_limit: int,
    enabled: bool,
) -> dict[str, float]:
    if not enabled:
        return {node_id: 0.0 for node_id in g.nodes}
    if g.number_of_nodes() <= exact_node_limit:
        return nx.betweenness_centrality(g)
    k = min(g.number_of_nodes(), max(1, samples or DEFAULT_BETWEENNESS_SAMPLES))
    return nx.betweenness_centrality(g, k=k, seed=42)


def _betweenness_samples_used(g: nx.DiGraph, mode: str, samples: int | None) -> int:
    if mode == "disabled":
        return 0
    if mode == "exact":
        return g.number_of_nodes()
    return min(g.number_of_nodes(), max(1, samples or DEFAULT_BETWEENNESS_SAMPLES))


def _pagerank(g: nx.DiGraph) -> dict[str, float]:
    try:
        return nx.pagerank(g, max_iter=100, tol=1.0e-6)
    except (ImportError, nx.PowerIterationFailedConvergence):
        return {node_id: 0.0 for node_id in g.nodes}


def _structural_scores(
    betweenness: dict[str, float],
    degree: dict[str, float],
    pagerank: dict[str, float],
) -> dict[str, float]:
    bw_norm = _normalize(betweenness)
    degree_norm = _normalize(degree)
    pagerank_norm = _normalize(pagerank)
    return {
        node_id: (
            0.45 * degree_norm.get(node_id, 0.0)
            + 0.35 * pagerank_norm.get(node_id, 0.0)
            + 0.20 * bw_norm.get(node_id, 0.0)
        )
        for node_id in set(betweenness) | set(degree) | set(pagerank)
    }


def _normalize(values: dict[str, float]) -> dict[str, float]:
    if not values:
        return {}
    maximum = max(values.values())
    if maximum <= 0:
        return {node_id: 0.0 for node_id in values}
    return {node_id: value / maximum for node_id, value in values.items()}
