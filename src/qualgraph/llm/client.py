"""Provider-agnostic LLM client with built-in cost/timing logging."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from time import perf_counter

from qualgraph.logging import RunLogger


@dataclass(slots=True)
class LLMRequest:
    system: str
    user: str
    max_tokens: int = 2000
    temperature: float = 0.0
    cache_keys: list[str] = field(default_factory=list)
    node_id: str | None = None
    prompt_template: str | None = None


@dataclass(slots=True)
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int
    model_id: str
    cost_usd: float = 0.0


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, req: LLMRequest) -> LLMResponse:
        ...

    @property
    @abstractmethod
    def model_id(self) -> str:
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
        try:
            response = self.provider.complete(request)
        except Exception as exc:
            if self.run_logger is not None:
                self.run_logger.log_llm_call(
                    node_id=request.node_id,
                    prompt_template=request.prompt_template,
                    model=self.provider.model_id,
                    duration_ms=_elapsed_ms(started),
                    status="failed",
                    error=exc,
                )
            raise

        if self.run_logger is not None:
            self.run_logger.log_llm_call(
                node_id=request.node_id,
                prompt_template=request.prompt_template,
                model=response.model_id,
                duration_ms=_elapsed_ms(started),
                input_tokens=response.input_tokens,
                cached_input_tokens=response.cached_input_tokens,
                output_tokens=response.output_tokens,
                cost_usd=response.cost_usd,
            )
        return response


def _elapsed_ms(started: float) -> float:
    return round((perf_counter() - started) * 1000, 3)
