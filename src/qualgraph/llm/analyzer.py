"""High-level LLM analysis entry points."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from qualgraph.llm.client import LLMClient, LLMRequest, LLMResponse


@dataclass(slots=True)
class NodeAnalysisRequest:
    node_id: str
    context: str


class LLMAnalyzer:
    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def analyze_node(self, request: NodeAnalysisRequest) -> LLMResponse:
        return self.client.complete(
            LLMRequest(
                prompt=request.context,
                operation="node_analysis",
                metadata={"node_id": request.node_id},
            )
        )

    def analyze_nodes(self, requests: Iterable[NodeAnalysisRequest]) -> list[LLMResponse]:
        return [self.analyze_node(request) for request in requests]
