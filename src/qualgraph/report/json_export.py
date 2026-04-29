"""Versioned JSON export surface."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import networkx as nx

from qualgraph.annotators.bandit import BanditAnnotator
from qualgraph.annotators.co_change import CoChangeAnnotator
from qualgraph.annotators.coverage import CoverageAnnotator
from qualgraph.annotators.cross_signal import CrossSignalAnnotator
from qualgraph.annotators.docstring import DocstringAnnotator
from qualgraph.annotators.git_history import GitHistoryAnnotator
from qualgraph.annotators.pip_audit import PipAuditAnnotator
from qualgraph.annotators.profiler import ProfilerAnnotator
from qualgraph.annotators.radon import RadonAnnotator
from qualgraph.annotators.ruff import RuffAnnotator
from qualgraph.annotators.secrets import SecretsAnnotator
from qualgraph.annotators.test_linkage import TestLinkageAnnotator
from qualgraph.annotators.vulture import VultureAnnotator
from qualgraph.graph.serialize import to_node_link_data


EXPORT_SCHEMA_VERSION = "0.1.0"
ANNOTATOR_CLASSES = [
    BanditAnnotator,
    CoChangeAnnotator,
    CoverageAnnotator,
    CrossSignalAnnotator,
    DocstringAnnotator,
    GitHistoryAnnotator,
    PipAuditAnnotator,
    ProfilerAnnotator,
    RadonAnnotator,
    RuffAnnotator,
    SecretsAnnotator,
    TestLinkageAnnotator,
    VultureAnnotator,
]


def export_json_data(
    graph: nx.DiGraph,
    config: Mapping[str, Any] | None = None,
    run_timestamp: str | None = None,
) -> dict[str, Any]:
    active_config = dict(config or graph.graph.get("config") or {})
    return {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "metadata": {
            "run_timestamp": run_timestamp or datetime.now(timezone.utc).isoformat(),
            "config_hash": _config_hash(active_config),
            "config": _json_safe(active_config),
            "annotator_versions": _annotator_versions(),
        },
        "graph": to_node_link_data(graph),
    }


def write_json_export(
    graph: nx.DiGraph,
    path: str | Path,
    config: Mapping[str, Any] | None = None,
    run_timestamp: str | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(export_json_data(graph, config=config, run_timestamp=run_timestamp), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return output_path


def _annotator_versions() -> dict[str, str]:
    return {annotator.name: annotator.version for annotator in ANNOTATOR_CLASSES}


def _config_hash(config: Mapping[str, Any]) -> str:
    payload = json.dumps(_json_safe(dict(config)), sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    try:
        json.dumps(value)
    except TypeError:
        return str(value)
    return value
