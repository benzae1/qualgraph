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
    max_size = _max_cluster_size(len(clusters), target)
    clusters = _split_oversized_clusters(g, clusters, max_size)
    current_count = len(set(clusters.values()))
    if current_count <= target:
        return _compact_cluster_ids(clusters)

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
        neighbor_cluster = _nearest_kept_cluster(node_id, clusters, kept, undirected, mutable_sizes, max_size)
        segment_cluster = _segment_cluster(g.nodes[node_id], kept_by_segment, mutable_sizes, max_size)
        target_cluster = neighbor_cluster or segment_cluster or min(mutable_sizes, key=lambda item: (mutable_sizes[item], item))
        reassigned[node_id] = target_cluster
        mutable_sizes[target_cluster] += 1

    return _compact_cluster_ids(reassigned)


def _target_cluster_count(node_count: int) -> int:
    if node_count <= 100:
        return max(1, node_count)
    return max(25, min(140, int(max(math.sqrt(node_count), node_count / 50))))


def _max_cluster_size(node_count: int, target: int) -> int:
    return max(75, math.ceil(node_count / max(target, 1) * 3))


def _split_oversized_clusters(g: nx.DiGraph, clusters: dict[str, int], max_size: int) -> dict[str, int]:
    by_cluster: dict[int, list[str]] = defaultdict(list)
    for node_id, cluster_id in clusters.items():
        by_cluster[cluster_id].append(node_id)

    next_cluster_id = max(by_cluster, default=-1) + 1
    split: dict[str, int] = {}
    for cluster_id, node_ids in sorted(by_cluster.items()):
        if len(node_ids) <= max_size:
            for node_id in node_ids:
                split[node_id] = cluster_id
            continue
        by_segment: dict[str, list[str]] = defaultdict(list)
        for node_id in node_ids:
            by_segment[_path_segment(g.nodes[node_id]) or "misc"].append(node_id)
        for segment, segment_nodes in sorted(by_segment.items()):
            ordered = sorted(segment_nodes)
            for offset in range(0, len(ordered), max_size):
                chunk = ordered[offset : offset + max_size]
                target_cluster = cluster_id if segment == "misc" and offset == 0 else next_cluster_id
                if target_cluster == next_cluster_id:
                    next_cluster_id += 1
                for node_id in chunk:
                    split[node_id] = target_cluster
    return split


def _nearest_kept_cluster(
    node_id: str,
    clusters: dict[str, int],
    kept: set[int],
    undirected: nx.Graph,
    sizes: Counter[int],
    max_size: int,
) -> int | None:
    counts: Counter[int] = Counter()
    for neighbor in undirected.neighbors(node_id):
        cluster_id = clusters.get(neighbor)
        if cluster_id in kept and sizes[cluster_id] < max_size:
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


def _segment_cluster(
    attrs: dict,
    kept_by_segment: dict[str, list[int]],
    sizes: Counter[int],
    max_size: int,
) -> int | None:
    segment = _path_segment(attrs)
    if not segment:
        return None
    clusters = kept_by_segment.get(segment) or []
    for cluster_id in clusters:
        if sizes[cluster_id] < max_size:
            return cluster_id
    return None


def _compact_cluster_ids(clusters: dict[str, int]) -> dict[str, int]:
    id_map = {cluster_id: index for index, cluster_id in enumerate(sorted(set(clusters.values())))}
    return {node_id: id_map[cluster_id] for node_id, cluster_id in clusters.items()}


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
