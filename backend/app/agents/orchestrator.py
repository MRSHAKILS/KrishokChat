"""Compatibility shim for the authoritative application QA pipeline."""

from __future__ import annotations

from typing import AsyncGenerator

from app.application.container import build_container
from app.application.qa_pipeline import QAInput
from app.core.config import settings
from app.domain.contracts import PipelineEvent, QAResult
from app.models.schemas import AgentStageEvent, QAResponse


async def run_qa_streaming(query: str) -> AsyncGenerator[str, None]:
    container = build_container(settings)
    async for item in container.qa.stream(QAInput(query=query)):
        if isinstance(item, PipelineEvent):
            event = AgentStageEvent(
                stage=item.stage.value,
                status=item.status.value,
                detail=item.detail,
            )
            yield f"data: {event.model_dump_json()}\n\n"
        elif isinstance(item, QAResult):
            response = QAResponse(
                query=item.query,
                category=item.category.value,
                answer=item.answer,
                sources=[],
                confidence=item.confidence.value,
                agent_trace=[],
            )
            yield f"final: {response.model_dump_json()}\n\n"
