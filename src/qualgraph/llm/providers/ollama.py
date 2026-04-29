"""Ollama local LLM provider."""

from __future__ import annotations

import httpx

from qualgraph.llm.client import LLMProvider, LLMRequest, LLMResponse


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        model: str = "llama3.1",
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ) -> None:
        self._model_id = model
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    @property
    def model_id(self) -> str:
        return self._model_id

    def complete(self, req: LLMRequest) -> LLMResponse:
        response = httpx.post(
            f"{self._base_url}/api/chat",
            json={
                "model": self._model_id,
                "stream": False,
                "messages": [
                    {"role": "system", "content": req.system},
                    {"role": "user", "content": req.user},
                ],
                "options": {
                    "temperature": req.temperature,
                    "num_predict": req.max_tokens,
                },
            },
            timeout=self._timeout,
        )
        response.raise_for_status()
        payload = response.json()
        return LLMResponse(
            text=(payload.get("message") or {}).get("content") or payload.get("response") or "",
            input_tokens=int(payload.get("prompt_eval_count") or 0),
            output_tokens=int(payload.get("eval_count") or 0),
            cached_input_tokens=0,
            model_id=str(payload.get("model") or self._model_id),
            cost_usd=0.0,
        )
