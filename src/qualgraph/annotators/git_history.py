"""Git history annotator."""

from __future__ import annotations

import collections
import re
import subprocess
from pathlib import Path
from typing import NamedTuple

import networkx as nx
from git import InvalidGitRepositoryError, Repo

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator


BUGFIX_KEYWORDS = re.compile(r"\b(fix|bug|issue|regression|hotfix)\b", re.I)
COMMIT_MARKER = "--QUALGRAPH-COMMIT--"


class CommitRecord(NamedTuple):
    author_email: str
    message: str
    files: list[str]


class GitHistoryAnnotator(BaseAnnotator):
    name = "git_history"
    version = "1.0"

    def __init__(self, max_commits: int | None = 1000) -> None:
        self.max_commits = max_commits

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        try:
            repo = Repo(repo_path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            return AnnotatorResult(name=self.name, errors=["not a git repository"])

        file_churn: collections.Counter[str] = collections.Counter()
        file_authors: collections.defaultdict[str, set[str]] = collections.defaultdict(set)
        file_bugfixes: collections.Counter[str] = collections.Counter()

        for commit in _commit_records(repo, repo_path, self.max_commits):
            is_bugfix = bool(BUGFIX_KEYWORDS.search(commit.message))
            for relative in commit.files:
                file_churn[relative] += 1
                file_authors[relative].add(commit.author_email)
                if is_bugfix:
                    file_bugfixes[relative] += 1

        nodes_annotated = 0
        for _node_id, attrs in graph.nodes(data=True):
            file_path = attrs.get("file_path")
            if not file_path:
                continue
            attrs["churn"] = file_churn[file_path]
            attrs["author_count"] = len(file_authors[file_path])
            attrs["bug_fix_keywords"] = file_bugfixes[file_path]
            nodes_annotated += 1

        return AnnotatorResult(name=self.name, nodes_annotated=nodes_annotated)


def _commit_records(repo: Repo, repo_path: Path, max_commits: int | None) -> list[CommitRecord]:
    root = Path(repo.working_tree_dir or repo_path).resolve()
    target_prefix = _target_prefix(repo, repo_path)
    command = [
        "git",
        "-C",
        str(root),
        "log",
        "--name-only",
        f"--pretty=format:{COMMIT_MARKER}%x00%ae%x00%s",
    ]
    if max_commits is not None and max_commits > 0:
        command.append(f"-n{max_commits}")
    command.append("--")
    if target_prefix:
        command.append(target_prefix)
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if completed.returncode != 0:
        return []
    return _parse_git_log(completed.stdout, target_prefix)


def _parse_git_log(output: str, target_prefix: str) -> list[CommitRecord]:
    records: list[CommitRecord] = []
    author_email = ""
    message = ""
    files: list[str] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(COMMIT_MARKER):
            if author_email or message or files:
                records.append(CommitRecord(author_email, message, files))
            parts = line.split("\x00", 2)
            author_email = parts[1] if len(parts) > 1 else ""
            message = parts[2] if len(parts) > 2 else ""
            files = []
            continue
        relative = _relative_to_target(line, target_prefix)
        if relative is not None:
            files.append(relative)
    if author_email or message or files:
        records.append(CommitRecord(author_email, message, files))
    return records


def _target_prefix(repo: Repo, repo_path: Path) -> str:
    root = Path(repo.working_tree_dir or repo_path).resolve()
    try:
        prefix = repo_path.resolve().relative_to(root).as_posix()
    except ValueError:
        return ""
    return "" if prefix == "." else prefix


def _relative_to_target(file_path: str, target_prefix: str) -> str | None:
    normalized = Path(file_path).as_posix()
    if not target_prefix:
        return normalized
    prefix = target_prefix.rstrip("/") + "/"
    if normalized.startswith(prefix):
        return normalized[len(prefix) :]
    return None
