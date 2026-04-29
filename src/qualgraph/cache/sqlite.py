"""SQLite-backed content-addressed cache."""

from __future__ import annotations

import hashlib
import io
import json
import sqlite3
import tokenize
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CACHE_KEY_FIELDS = [
    "language_version",
    "grammar_version",
    "normalized_function_body",
    "annotator_name",
    "annotator_version",
    "model_id",
    "prompt_template_version",
]


def cache_key(**kwargs: Any) -> str:
    h = hashlib.sha256()
    for field in CACHE_KEY_FIELDS:
        h.update(field.encode())
        h.update(b"\x00")
        h.update(str(kwargs[field]).encode())
        h.update(b"\x00")
    return h.hexdigest()


def normalized_function_body(source: str, strip_comments: bool = False) -> str:
    """Normalize source for cache identity without semantic reformatting."""

    normalized = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalized.split("\n")]
    normalized = "\n".join(lines).strip("\n")
    if strip_comments:
        normalized = _strip_comments(normalized)
    return normalized


class Cache:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS llm_cache(
              key TEXT PRIMARY KEY,
              response_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            )
            """
        )
        self.db.commit()

    def get(self, key: str) -> Any | None:
        row = self.db.execute("SELECT response_json FROM llm_cache WHERE key = ?", (key,)).fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def put(self, key: str, response: Any) -> None:
        self.db.execute(
            """
            INSERT OR REPLACE INTO llm_cache(key, response_json, created_at)
            VALUES (?, ?, ?)
            """,
            (key, json.dumps(response, sort_keys=True), datetime.now(timezone.utc).isoformat()),
        )
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "Cache":
        return self

    def __exit__(self, _exc_type: object, _exc: object, _tb: object) -> None:
        self.close()


def _strip_comments(source: str) -> str:
    tokens = []
    reader = io.StringIO(source).readline
    try:
        for token in tokenize.generate_tokens(reader):
            if token.type == tokenize.COMMENT:
                continue
            tokens.append(token)
    except tokenize.TokenError:
        return source
    stripped = tokenize.untokenize(tokens)
    lines = [line.rstrip() for line in stripped.split("\n")]
    return "\n".join(lines).strip("\n")
