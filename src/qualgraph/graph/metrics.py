"""Structural metrics and cluster role heuristics."""

from __future__ import annotations

from collections import defaultdict
from statistics import median

import networkx as nx


def annotate_metrics(g: nx.DiGraph) -> None:
    """Write structural metrics back onto graph nodes.

    Betweenness is useful for bridge-finding, but it is often exactly zero in
    small sparse code graphs. ``centrality`` is therefore a composite structural
    score for ranking, while raw betweenness remains available separately.
    """

    if g.number_of_nodes() == 0:
        return

    if g.number_of_nodes() > 5000:
        bw = nx.betweenness_centrality(g, k=500, seed=42)
    else:
        bw = nx.betweenness_centrality(g)

    degree = _degree_centrality(g)
    pagerank = _pagerank(g)
    structural_scores = _structural_scores(bw, degree, pagerank)

    for node_id in g.nodes:
        g.nodes[node_id]["betweenness_centrality"] = float(bw.get(node_id, 0.0))
        g.nodes[node_id]["degree_centrality"] = float(degree.get(node_id, 0.0))
        g.nodes[node_id]["pagerank"] = float(pagerank.get(node_id, 0.0))
        g.nodes[node_id]["structural_score"] = float(structural_scores.get(node_id, 0.0))
        g.nodes[node_id]["centrality"] = float(structural_scores.get(node_id, 0.0))
        g.nodes[node_id]["in_degree"] = int(g.in_degree(node_id))
        g.nodes[node_id]["out_degree"] = int(g.out_degree(node_id))

    annotate_cluster_roles(g)


def annotate_cluster_roles(g: nx.DiGraph) -> None:
    """Classify each node's role within its cluster using simple topology."""

    if g.number_of_nodes() == 0:
        return

    clusters: dict[int | str, list[str]] = defaultdict(list)
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
                g,
                node_id,
                in_degree=in_degree,
                out_degree=out_degree,
                centrality=centrality,
                high_in=high_in,
                high_out=high_out,
                centrality_floor=centrality_floor,
            )


def _cluster_role(
    g: nx.DiGraph,
    node_id: str,
    in_degree: int,
    out_degree: int,
    centrality: float,
    high_in: int,
    high_out: int,
    centrality_floor: float,
) -> str:
    if out_degree >= high_out and centrality >= centrality_floor:
        return "hub"
    if in_degree >= high_in and out_degree <= 1:
        return "utility"
    if _is_pipeline_node(g, node_id, in_degree, out_degree):
        return "pipeline"
    if in_degree == 0 and out_degree == 0:
        return "isolated"
    return "member"


def _is_pipeline_node(g: nx.DiGraph, node_id: str, in_degree: int, out_degree: int) -> bool:
    if in_degree > 1 or out_degree > 1:
        return False
    weak_component = nx.node_connected_component(g.to_undirected(), node_id)
    if len(weak_component) < 3:
        return False
    subgraph = g.subgraph(weak_component)
    return all(subgraph.in_degree(node) <= 1 and subgraph.out_degree(node) <= 1 for node in subgraph.nodes)


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


def _pagerank(g: nx.DiGraph) -> dict[str, float]:
    try:
        return nx.pagerank(g)
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
