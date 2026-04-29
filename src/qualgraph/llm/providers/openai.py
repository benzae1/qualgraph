"""OpenAI LLM provider."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from qualgraph.llm.client import LLMProvider, LLMRequest, LLMResponse


@dataclass(frozen=True, slots=True)
class TokenPricing:
    input_per_million: float = 0.0
    output_per_million: float = 0.0
    cached_input_per_million: float = 0.0


class OpenAIProvider(LLMProvider):
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        client: OpenAI | None = None,
        pricing: TokenPricing | None = None,
    ) -> None:
        self._model_id = model
        self._client = client or OpenAI()
        self._pricing = pricing or TokenPricing()

    @property
    def model_id(self) -> str:
        return self._model_id

    def complete(self, req: LLMRequest) -> LLMResponse:
        response = self._client.chat.completions.create(
            model=self._model_id,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            messages=[
                {"role": "system", "content": req.system},
                {"role": "user", "content": req.user},
            ],
        )
        usage = response.usage
        input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        cached_input_tokens = _cached_input_tokens(usage)
        return LLMResponse(
            text=response.choices[0].message.content or "",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_input_tokens=cached_input_tokens,
            model_id=self._model_id,
            cost_usd=_cost(input_tokens, output_tokens, cached_input_tokens, self._pricing),
        )


def _cached_input_tokens(usage: Any) -> int:
    details = getattr(usage, "prompt_tokens_details", None)
    if details is None:
        return 0
    return int(getattr(details, "cached_tokens", 0) or 0)


def _cost(input_tokens: int, output_tokens: int, cached_input_tokens: int, pricing: TokenPricing) -> float:
    billable_input_tokens = max(0, input_tokens - cached_input_tokens)
    return (
        billable_input_tokens * pricing.input_per_million
        + cached_input_tokens * pricing.cached_input_per_million
        + output_tokens * pricing.output_per_million
    ) / 1_000_000
