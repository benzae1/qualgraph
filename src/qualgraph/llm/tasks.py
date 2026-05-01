"""Filesystem protocol for agent-completed LLM analysis tasks."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import networkx as nx

from qualgraph.annotators.findings import add_finding
from qualgraph.llm.context import build_context, build_node_analysis_prompt, evidence_corpus
from qualgraph.llm.parser import parse_analysis_response
from qualgraph.scoring.risk import score as score_risk
from qualgraph.scoring.risk import top_risk_nodes


TASK_SCHEMA_VERSION = "0.1.0"


def export_tasks(
    graph: nx.DiGraph,
    output_dir: str | Path,
    limit: int = 20,
    prompt_template: str = "node_analysis",
) -> dict[str, Any]:
    score_risk(graph)
    task_dir = Path(output_dir)
    result_dir = task_dir.parent / "llm_results"
    task_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    tasks = []
    for index, (node_id, attrs) in enumerate(top_risk_nodes(graph, limit=limit), start=1):
        task_id = f"{index:04d}"
        output_path = result_dir / f"{task_id}.json"
        task_path = task_dir / f"{task_id}.{_slug(attrs.get('qualified_name') or node_id)}.md"
        system, user = build_node_analysis_prompt(graph, node_id)
        task = {
            "task_id": task_id,
            "node_id": node_id,
            "qualified_name": attrs.get("qualified_name"),
            "prompt_template": prompt_template,
            "task_path": task_path.as_posix(),
            "output_path": output_path.as_posix(),
            "risk_score": attrs.get("risk_score"),
        }
        task_path.write_text(_task_markdown(task, system, user), encoding="utf-8")
        tasks.append(task)

    manifest = {
        "schema_version": TASK_SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "task_dir": task_dir.as_posix(),
        "result_dir": result_dir.as_posix(),
        "tasks": tasks,
    }
    (task_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def import_results(graph: nx.DiGraph, run_dir: str | Path, strict: bool = False) -> dict[str, Any]:
    base = Path(run_dir)
    manifest_path = base / "llm_tasks" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    imported = 0
    missing = 0
    findings_added = 0
    touched_nodes: set[str] = set()
    proposed_count = 0
    rejected_count = 0

    for task in manifest.get("tasks", []):
        output_path = Path(task["output_path"])
        if not output_path.is_absolute():
            output_path = Path(output_path)
        if not output_path.exists():
            missing += 1
            if strict:
                raise FileNotFoundError(output_path)
            continue
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        node_id = task["node_id"]
        context = build_context(graph, node_id)
        parsed = parse_analysis_response(json.dumps(payload), evidence_corpus(context))
        proposed_count += int(parsed.get("proposed_count") or 0)
        rejected_count += int(parsed.get("rejected_count") or 0)
        imported += 1
        for finding in parsed.get("findings", []) or []:
            normalized = _normalize_finding(finding)
            if add_finding(graph.nodes[node_id], normalized):
                findings_added += 1
                touched_nodes.add(node_id)

    for node_id in touched_nodes:
        graph.nodes[node_id]["llm_severity_max"] = max(
            (
                float(finding.get("severity_num") or 0.0)
                for finding in graph.nodes[node_id].get("findings", []) or []
                if isinstance(finding, dict) and finding.get("source") == "llm"
            ),
            default=0.0,
        )
    score_risk(graph)
    graph.graph["llm_validation"] = {
        "tasks": len(manifest.get("tasks", []) or []),
        "imported": imported,
        "proposed": proposed_count,
        "accepted": proposed_count - rejected_count,
        "rejected": rejected_count,
    }
    return {
        "tasks": len(manifest.get("tasks", []) or []),
        "imported": imported,
        "missing": missing,
        "findings_added": findings_added,
        "nodes_touched": len(touched_nodes),
        "proposed": proposed_count,
        "accepted": proposed_count - rejected_count,
        "rejected": rejected_count,
    }


def _task_markdown(task: dict[str, Any], system: str, user: str) -> str:
    return (
        "# Qualgraph LLM Task\n\n"
        f"- Task ID: {task['task_id']}\n"
        f"- Node ID: `{task['node_id']}`\n"
        f"- Qualified name: `{task.get('qualified_name')}`\n"
        f"- Prompt template: `{task['prompt_template']}`\n"
        f"- Write JSON output to: `{task['output_path']}`\n\n"
        "## Instructions\n\n"
        "Read the system and user prompt below. Write only valid JSON to the output path. "
        "Do not edit the graph directly.\n\n"
        "## System\n\n"
        f"{system}\n\n"
        "## User\n\n"
        f"{user}\n"
    )


def _normalize_finding(finding: dict[str, Any]) -> dict[str, Any]:
    severity = str(finding.get("severity") or "low").lower()
    kind = str(finding.get("kind") or finding.get("dimension") or finding.get("code") or "llm_finding")
    title = str(finding.get("title") or kind.replace("_", " ").title())
    description = str(finding.get("description") or finding.get("message") or title)
    return {
        "source": "llm",
        "code": kind,
        "severity": severity.upper(),
        "severity_num": _severity_num(severity),
        "confidence": finding.get("confidence") or "INFERRED",
        "message": description,
        "dimension": finding.get("dimension"),
        "title": title,
        "description": description,
        "evidence": finding.get("evidence") or "",
        "suggested_action": finding.get("suggested_action"),
        "line": finding.get("line"),
    }


def _severity_num(severity: str) -> float:
    return {"CRITICAL": 1.0, "HIGH": 0.85, "MEDIUM": 0.66, "LOW": 0.33}.get(severity.upper(), 0.0)


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return slug[:80] or "node"
