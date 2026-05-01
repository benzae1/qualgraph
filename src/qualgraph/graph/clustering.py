"""Leiden community detection for code graphs."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from pathlib import Path

import igraph as ig
import leidenalg
import networkx as nx


DEFAULT_RESOLUTION = 0.05


def cluster_leiden(g: nx.DiGraph, resolution: float = DEFAULT_RESOLUTION) -> dict[str, int]:
    """Return ``node_id -> cluster_id`` using Leiden on an undirected graph."""

    if g.number_of_nodes() == 0:
        return {}

    h = _to_igraph(g)
    if h.ecount() == 0:
        return _coarsen_clusters(g, {vertex["name"]: index for index, vertex in enumerate(h.vs)})

    partition = leidenalg.find_partition(
        h,
        leidenalg.RBConfigurationVertexPartition,
        resolution_parameter=resolution,
    )
    clusters = {
        h.vs[index]["name"]: cluster_id
        for cluster_id, members in enumerate(partition)
        for index in members
    }
    return _coarsen_clusters(g, clusters)


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


def _coarsen_clusters(g: nx.DiGraph, clusters: dict[str, int]) -> dict[str, int]:
    target = _target_cluster_count(len(clusters))
    current_count = len(set(clusters.values()))
    if current_count <= target:
        return clusters

    sizes = Counter(clusters.values())
    kept = {cluster_id for cluster_id, _size in sizes.most_common(target)}
    kept_by_segment = _kept_clusters_by_segment(g, clusters, kept)
    mutable_sizes = Counter({cluster_id: sizes[cluster_id] for cluster_id in kept})
    reassigned: dict[str, int] = {}
    undirected = g.to_undirected()

    for node_id, cluster_id in clusters.items():
        if cluster_id in kept:
            reassigned[node_id] = cluster_id
            continue
        neighbor_cluster = _nearest_kept_cluster(node_id, clusters, kept, undirected)
        segment_cluster = _segment_cluster(g.nodes[node_id], kept_by_segment)
        target_cluster = neighbor_cluster or segment_cluster or min(mutable_sizes, key=lambda item: (mutable_sizes[item], item))
        reassigned[node_id] = target_cluster
        mutable_sizes[target_cluster] += 1

    id_map = {cluster_id: index for index, cluster_id in enumerate(sorted(set(reassigned.values())))}
    return {node_id: id_map[cluster_id] for node_id, cluster_id in reassigned.items()}


def _target_cluster_count(node_count: int) -> int:
    if node_count <= 100:
        return max(1, node_count)
    return max(25, min(140, int(max(math.sqrt(node_count), node_count / 50))))


def _nearest_kept_cluster(
    node_id: str,
    clusters: dict[str, int],
    kept: set[int],
    undirected: nx.Graph,
) -> int | None:
    counts: Counter[int] = Counter()
    for neighbor in undirected.neighbors(node_id):
        cluster_id = clusters.get(neighbor)
        if cluster_id in kept:
            counts[cluster_id] += 1
    if not counts:
        return None
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _kept_clusters_by_segment(g: nx.DiGraph, clusters: dict[str, int], kept: set[int]) -> dict[str, list[int]]:
    by_segment: dict[str, Counter[int]] = defaultdict(Counter)
    for node_id, cluster_id in clusters.items():
        if cluster_id not in kept:
            continue
        segment = _path_segment(g.nodes[node_id])
        if segment:
            by_segment[segment][cluster_id] += 1
    return {
        segment: [cluster_id for cluster_id, _count in counts.most_common()]
        for segment, counts in by_segment.items()
    }


def _segment_cluster(attrs: dict, kept_by_segment: dict[str, list[int]]) -> int | None:
    segment = _path_segment(attrs)
    if not segment:
        return None
    clusters = kept_by_segment.get(segment) or []
    return clusters[0] if clusters else None


def _path_segment(attrs: dict) -> str | None:
    file_path = str(attrs.get("file_path") or "")
    if not file_path:
        return None
    ignored = {"", ".", "src", "tests", "test", "benchmarks", "repos", "scrapy", "starlette", "qualgraph"}
    parts = Path(file_path).with_suffix("").parts
    for part in reversed(parts[:-1]):
        lowered = part.lower()
        if lowered not in ignored and not lowered.startswith("test_") and not lowered.startswith("."):
            return lowered
    return None
