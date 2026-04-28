"""Structural metrics and cluster role heuristics."""

from __future__ import annotations

from collections import defaultdict
from statistics import median

import networkx as nx


def annotate_metrics(g: nx.DiGraph) -> None:
    """Write centrality and degree metrics back onto graph nodes."""

    if g.number_of_nodes() == 0:
        return

    if g.number_of_nodes() > 5000:
        bw = nx.betweenness_centrality(g, k=500, seed=42)
    else:
        bw = nx.betweenness_centrality(g)

    for node_id, value in bw.items():
        g.nodes[node_id]["centrality"] = value

    for node_id in g.nodes:
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
