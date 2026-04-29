"""Anthropic LLM provider."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from anthropic import Anthropic

from qualgraph.llm.client import LLMProvider, LLMRequest, LLMResponse


@dataclass(frozen=True, slots=True)
class TokenPricing:
    input_per_million: float = 0.0
    output_per_million: float = 0.0
    cached_input_per_million: float = 0.0


class AnthropicProvider(LLMProvider):
    def __init__(
        self,
        model: str = "claude-3-5-sonnet-latest",
        client: Anthropic | None = None,
        pricing: TokenPricing | None = None,
    ) -> None:
        self._model_id = model
        self._client = client or Anthropic()
        self._pricing = pricing or TokenPricing()

    @property
    def model_id(self) -> str:
        return self._model_id

    def complete(self, req: LLMRequest) -> LLMResponse:
        response = self._client.messages.create(
            model=self._model_id,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            system=_system_blocks(req),
            messages=[{"role": "user", "content": req.user}],
        )
        usage = response.usage
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        cached_input_tokens = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
        return LLMResponse(
            text=_message_text(response.content),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_input_tokens=cached_input_tokens,
            model_id=self._model_id,
            cost_usd=_cost(input_tokens, output_tokens, cached_input_tokens, self._pricing),
        )


def _system_blocks(req: LLMRequest) -> list[dict[str, Any]] | str:
    block: dict[str, Any] = {"type": "text", "text": req.system}
    if req.cache_keys:
        block["cache_control"] = {"type": "ephemeral"}
    return [block]


def _message_text(content: Any) -> str:
    parts: list[str] = []
    for block in content or []:
        text = getattr(block, "text", None)
        if text:
            parts.append(str(text))
    return "\n".join(parts)


def _cost(input_tokens: int, output_tokens: int, cached_input_tokens: int, pricing: TokenPricing) -> float:
    billable_input_tokens = max(0, input_tokens - cached_input_tokens)
    return (
        billable_input_tokens * pricing.input_per_million
        + cached_input_tokens * pricing.cached_input_per_million
        + output_tokens * pricing.output_per_million
    ) / 1_000_000
