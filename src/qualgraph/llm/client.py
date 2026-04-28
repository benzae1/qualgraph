"""Provider-agnostic LLM client with built-in cost/timing logging."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Protocol

from qualgraph.logging import RunLogger


@dataclass(slots=True)
class LLMRequest:
    prompt: str
    operation: str = "completion"
    system: str | None = None
    temperature: float = 0.0
    max_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LLMResponse:
    text: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int | None = None
    cost_usd: float = 0.0
    raw: Any = None


class LLMProvider(Protocol):
    name: str
    model: str

    def complete(self, request: LLMRequest) -> LLMResponse:
        ...


class LLMClient:
    def __init__(
        self,
        provider: LLMProvider,
        run_logger: RunLogger | None = None,
    ) -> None:
        self.provider = provider
        self.run_logger = run_logger

    def complete(self, request: LLMRequest) -> LLMResponse:
        started = perf_counter()
        provider_name = getattr(self.provider, "name", type(self.provider).__name__)
        model = getattr(self.provider, "model", "unknown")
        try:
            response = self.provider.complete(request)
        except Exception as exc:
            if self.run_logger is not None:
                self.run_logger.log_llm_call(
                    provider=provider_name,
                    model=model,
                    operation=request.operation,
                    duration_ms=_elapsed_ms(started),
                    status="failed",
                    error=exc,
                )
            raise

        if self.run_logger is not None:
            self.run_logger.log_llm_call(
                provider=response.provider or provider_name,
                model=response.model or model,
                operation=request.operation,
                duration_ms=_elapsed_ms(started),
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens,
                total_tokens=response.total_tokens,
                cost_usd=response.cost_usd,
            )
        return response


def _elapsed_ms(started: float) -> float:
    return round((perf_counter() - started) * 1000, 3)
