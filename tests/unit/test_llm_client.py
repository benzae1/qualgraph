import json
from pathlib import Path
from types import SimpleNamespace

import networkx as nx

from qualgraph.cache.sqlite import Cache
from qualgraph.graph.schema import NodeAttrs, NodeType, node_attrs_to_graph
from qualgraph.llm.analyzer import LLMAnalyzer, NodeAnalysisRequest, analyze_top_n
from qualgraph.llm.client import LLMClient, LLMProvider, LLMRequest, LLMResponse
from qualgraph.llm.providers.anthropic import AnthropicProvider, TokenPricing as AnthropicPricing
from qualgraph.llm.providers.ollama import OllamaProvider
from qualgraph.llm.providers.openai import OpenAIProvider, TokenPricing as OpenAIPricing
from qualgraph.logging import RunLogger


class FakeProvider(LLMProvider):
    @property
    def model_id(self) -> str:
        return "fake-model"

    def complete(self, req: LLMRequest) -> LLMResponse:
        return LLMResponse(
            text=f"{req.system}\n{req.user}",
            input_tokens=10,
            output_tokens=4,
            cached_input_tokens=3,
            model_id=self.model_id,
            cost_usd=0.012,
        )


class FindingProvider(LLMProvider):
    def __init__(self) -> None:
        self.calls = 0

    @property
    def model_id(self) -> str:
        return "finding-model"

    def complete(self, req: LLMRequest) -> LLMResponse:
        self.calls += 1
        return LLMResponse(
            text=json.dumps(
                {
                    "findings": [
                        {
                            "dimension": "reliability",
                            "severity": "high",
                            "confidence": "INFERRED",
                            "title": "Unhandled risky call",
                            "description": "The risky call is returned without local handling.",
                            "evidence": "return risky()",
                            "suggested_action": "Handle the error or document propagation.",
                        }
                    ]
                }
            ),
            input_tokens=20,
            output_tokens=10,
            cached_input_tokens=5,
            model_id=self.model_id,
            cost_usd=0.01,
        )


def test_llm_client_logs_call_telemetry_jsonl(tmp_path: Path) -> None:
    logger = RunLogger(repo_path=Path("."), artifacts_dir=tmp_path, run_id="run-1")
    client = LLMClient(FakeProvider(), run_logger=logger)

    response = client.complete(
        LLMRequest(
            system="system",
            user="user",
            node_id="node-1",
            prompt_template="node_analysis",
        )
    )
    logger.finish()

    assert response.text == "system\nuser"
    rows = [json.loads(line) for line in (tmp_path / "run-1" / "llm_calls.jsonl").read_text().splitlines()]
    assert rows == [
        {
            "cached_tokens": 3,
            "cost_usd": 0.012,
            "input_tokens": 10,
            "latency_ms": rows[0]["latency_ms"],
            "model": "fake-model",
            "node_id": "node-1",
            "output_tokens": 4,
            "prompt_template": "node_analysis",
            "status": "ok",
        }
    ]
    summary = json.loads((tmp_path / "run-1" / "run_summary.json").read_text())
    assert summary["llm"]["calls"] == 1
    assert summary["llm"]["cached_input_tokens"] == 3


def test_analyzer_builds_node_analysis_request() -> None:
    client = LLMClient(FakeProvider())
    response = LLMAnalyzer(client).analyze_node(NodeAnalysisRequest(node_id="node-1", context="inspect me"))

    assert "careful code quality analyst" in response.text
    assert "inspect me" in response.text


def test_analyze_top_n_calls_provider_caches_and_attaches_findings(tmp_path: Path) -> None:
    graph = _graph_with_risky_function()
    provider = FindingProvider()
    logger = RunLogger(repo_path=Path("."), artifacts_dir=tmp_path / "runs", run_id="run-1")
    cache = Cache(tmp_path / "cache.db")

    summary = analyze_top_n(graph, top_n=1, provider=provider, cache=cache, logger=logger)
    logger.finish()

    assert summary.analyzed == 1
    assert summary.llm_calls == 1
    assert summary.cache_hits == 0
    assert summary.findings_added == 1
    assert provider.calls == 1
    assert graph.nodes["function"]["llm_findings"][0]["dimension"] == "reliability"
    assert graph.nodes["function"]["llm_severity_max"] == 0.85
    assert graph.nodes["function"]["risk_components"]["llm"] == 0.85
    assert graph.nodes["function"]["findings"][0]["source"] == "llm"
    rows = [json.loads(line) for line in (tmp_path / "runs" / "run-1" / "llm_calls.jsonl").read_text().splitlines()]
    assert rows[0]["prompt_template"] == "analysis-v1"

    cached_summary = analyze_top_n(graph, top_n=1, provider=provider, cache=cache)

    assert cached_summary.cache_hits == 1
    assert cached_summary.llm_calls == 0
    assert provider.calls == 1
    cache.close()


def test_analyze_top_n_dry_run_returns_prompts_without_provider_call(tmp_path: Path) -> None:
    graph = _graph_with_risky_function()
    provider = FindingProvider()
    cache = Cache(tmp_path / "cache.db")

    summary = analyze_top_n(graph, top_n=1, provider=provider, cache=cache, dry_run=True)

    assert summary.dry_run is True
    assert summary.ranked == 1
    assert summary.dry_run_tasks[0]["node_id"] == "function"
    assert "return risky()" in summary.dry_run_tasks[0]["user"]
    assert provider.calls == 0
    assert "llm_findings" not in graph.nodes["function"]
    cache.close()


def test_anthropic_provider_uses_ephemeral_system_cache_block() -> None:
    class Messages:
        def __init__(self) -> None:
            self.kwargs = None

        def create(self, **kwargs):
            self.kwargs = kwargs
            return SimpleNamespace(
                content=[SimpleNamespace(text="ok")],
                usage=SimpleNamespace(input_tokens=100, output_tokens=20, cache_read_input_tokens=40),
            )

    messages = Messages()
    provider = AnthropicProvider(
        model="claude-test",
        client=SimpleNamespace(messages=messages),
        pricing=AnthropicPricing(input_per_million=3, output_per_million=15, cached_input_per_million=0.3),
    )

    response = provider.complete(LLMRequest(system="sys", user="usr", cache_keys=["system"]))

    assert messages.kwargs["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert response.text == "ok"
    assert response.cached_input_tokens == 40
    assert response.cost_usd == ((60 * 3) + (40 * 0.3) + (20 * 15)) / 1_000_000


def test_openai_provider_maps_usage_and_cached_tokens() -> None:
    class Completions:
        def create(self, **_kwargs):
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))],
                usage=SimpleNamespace(
                    prompt_tokens=100,
                    completion_tokens=20,
                    prompt_tokens_details=SimpleNamespace(cached_tokens=25),
                ),
            )

    client = SimpleNamespace(chat=SimpleNamespace(completions=Completions()))
    provider = OpenAIProvider(
        model="gpt-test",
        client=client,
        pricing=OpenAIPricing(input_per_million=2, output_per_million=8, cached_input_per_million=0.5),
    )

    response = provider.complete(LLMRequest(system="sys", user="usr"))

    assert response.text == "ok"
    assert response.input_tokens == 100
    assert response.output_tokens == 20
    assert response.cached_input_tokens == 25
    assert response.cost_usd == ((75 * 2) + (25 * 0.5) + (20 * 8)) / 1_000_000


def test_ollama_provider_posts_to_local_chat_api(monkeypatch) -> None:
    captured = {}

    class Response:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {
                "model": "llama-test",
                "message": {"content": "ok"},
                "prompt_eval_count": 11,
                "eval_count": 5,
            }

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr("qualgraph.llm.providers.ollama.httpx.post", fake_post)

    response = OllamaProvider(model="llama-test").complete(LLMRequest(system="sys", user="usr"))

    assert captured["url"] == "http://localhost:11434/api/chat"
    assert captured["json"]["stream"] is False
    assert response.text == "ok"
    assert response.cost_usd == 0.0


def _graph_with_risky_function() -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_node(
        "function",
        **node_attrs_to_graph(
            NodeAttrs(
                id="function",
                type=NodeType.FUNCTION,
                name="work",
                qualified_name="sample.work",
                file_path="sample.py",
                line_start=1,
                line_end=2,
                source="def work():\n    return risky()\n",
                risk_score=2.0,
            )
        ),
    )
    return graph
