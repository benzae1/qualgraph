"""Git history annotator."""

from __future__ import annotations

import collections
import re
from pathlib import Path

import networkx as nx
from git import InvalidGitRepositoryError, Repo

from qualgraph.annotators.base import AnnotatorResult, BaseAnnotator


BUGFIX_KEYWORDS = re.compile(r"\b(fix|bug|issue|regression|hotfix)\b", re.I)


class GitHistoryAnnotator(BaseAnnotator):
    name = "git_history"
    version = "1.0"

    def annotate(self, graph: nx.DiGraph, repo_path: Path) -> AnnotatorResult:
        try:
            repo = Repo(repo_path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            return AnnotatorResult(name=self.name, errors=["not a git repository"])

        target_prefix = _target_prefix(repo, repo_path)
        file_churn: collections.Counter[str] = collections.Counter()
        file_authors: collections.defaultdict[str, set[str]] = collections.defaultdict(set)
        file_bugfixes: collections.Counter[str] = collections.Counter()

        for commit in repo.iter_commits():
            is_bugfix = bool(BUGFIX_KEYWORDS.search(commit.message))
            for file_path in commit.stats.files:
                relative = _relative_to_target(file_path, target_prefix)
                if relative is None:
                    continue
                file_churn[relative] += 1
                file_authors[relative].add(commit.author.email)
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
