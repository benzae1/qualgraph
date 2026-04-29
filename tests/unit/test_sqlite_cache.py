import hashlib
import json
import sqlite3

from qualgraph.cache.sqlite import CACHE_KEY_FIELDS, Cache, cache_key, normalized_function_body


def test_cache_key_uses_exact_ordered_fields() -> None:
    values = {
        "language_version": "3.12",
        "grammar_version": "tree-sitter-python-0.21.0",
        "normalized_function_body": "def f():\n    return 1",
        "annotator_name": "llm",
        "annotator_version": "1.0",
        "model_id": "model",
        "prompt_template_version": "node-analysis-v1",
    }
    expected = hashlib.sha256()
    for field in CACHE_KEY_FIELDS:
        expected.update(field.encode())
        expected.update(b"\x00")
        expected.update(str(values[field]).encode())
        expected.update(b"\x00")

    assert cache_key(**values) == expected.hexdigest()


def test_normalized_function_body_preserves_format_but_normalizes_line_endings_and_trailing_space() -> None:
    source = "def f():\r\n    x = 1   \r\n    return x\t\r\n\r\n"

    assert normalized_function_body(source) == "def f():\n    x = 1\n    return x"


def test_normalized_function_body_can_strip_comments_without_black_formatting() -> None:
    source = "def f():\n    x = 1  # keep value\n    return x\n"

    assert normalized_function_body(source, strip_comments=True) == "def f():\n    x = 1\n    return x"


def test_cache_get_put_round_trips_json_and_replaces_existing_value(tmp_path) -> None:
    cache_path = tmp_path / "qualgraph.db"
    with Cache(cache_path) as cache:
        cache.put("abc", {"findings": [{"kind": "one"}]})
        assert cache.get("abc") == {"findings": [{"kind": "one"}]}
        cache.put("abc", {"findings": []})
        assert cache.get("abc") == {"findings": []}
        assert cache.get("missing") is None

    with sqlite3.connect(cache_path) as db:
        row = db.execute("SELECT response_json, created_at FROM llm_cache WHERE key = ?", ("abc",)).fetchone()

    assert json.loads(row[0]) == {"findings": []}
    assert row[1]
