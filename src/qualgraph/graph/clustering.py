"""Leiden community detection for code graphs."""

from __future__ import annotations

import igraph as ig
import leidenalg
import networkx as nx


DEFAULT_RESOLUTION = 0.35


def cluster_leiden(g: nx.DiGraph, resolution: float = DEFAULT_RESOLUTION) -> dict[str, int]:
    """Return ``node_id -> cluster_id`` using Leiden on an undirected graph."""

    if g.number_of_nodes() == 0:
        return {}

    h = _to_igraph(g)
    if h.ecount() == 0:
        return {vertex["name"]: index for index, vertex in enumerate(h.vs)}

    partition = leidenalg.find_partition(
        h,
        leidenalg.RBConfigurationVertexPartition,
        resolution_parameter=resolution,
    )
    return {
        h.vs[index]["name"]: cluster_id
        for cluster_id, members in enumerate(partition)
        for index in members
    }


def annotate_clusters(g: nx.DiGraph, resolution: float = DEFAULT_RESOLUTION) -> dict[str, int]:
    clusters = cluster_leiden(g, resolution=resolution)
    for node_id, cluster_id in clusters.items():
        g.nodes[node_id]["cluster_id"] = cluster_id
    g.graph["cluster_count"] = len(set(clusters.values()))
    g.graph["cluster_resolution"] = resolution
    return clusters


def _to_igraph(g: nx.DiGraph) -> ig.Graph:
    undirected = g.to_undirected()
    h = ig.Graph()
    node_ids = list(undirected.nodes())
    h.add_vertices(node_ids)
    if undirected.number_of_edges() > 0:
        h.add_edges(list(undirected.edges()))
    return h
