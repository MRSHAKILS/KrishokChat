"""QA HTTP adapters. All behavior is delegated to one application pipeline."""

from __future__ import annotations

import json
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.application.container import AppContainer
from app.application.qa_pipeline import QAInput
from app.domain.contracts import PipelineEvent, QAResult, RetrievedSource
from app.models.schemas import AgentStageEvent, QARequest, QAResponse, SourceNode
from app.api.dependencies import get_container

router = APIRouter()


ContainerDep = Annotated[AppContainer, Depends(get_container)]


def _input(request: QARequest) -> QAInput:
    return QAInput(
        query=request.query,
        session_id=request.session_id,
        crop=request.crop,
        disease=request.disease,
        history=request.history,
    )


def _source(source: RetrievedSource) -> SourceNode:
    return SourceNode(
        id=source.id,
        crop_bn=source.metadata.get("crop_bn") or None,
        crop_en=source.metadata.get("crop_en") or None,
        disease_bn=source.metadata.get("disease_bn") or None,
        question=source.metadata.get("question") or source.metadata.get("section_title") or None,
        score=source.score,
        answer=source.content_bn or source.content_en[:400],
        treatment=source.metadata.get("treatment_summary_bn") or None,
        source=source.source or source.metadata.get("citation") or None,
        expert_verified=bool(source.metadata.get("expert_verified", False)),
    )


def _response(result: QAResult) -> QAResponse:
    return QAResponse(
        query=result.query,
        category=result.category.value,
        answer=result.answer,
        sources=[_source(source) for source in result.sources],
        confidence=result.confidence.value,
        agent_trace=[
            AgentStageEvent(stage=event.stage.value, status=event.status.value, detail=event.detail)
            for event in result.trace
        ],
        verifier_flags=list(result.verifier_flags),
        model=result.model or None,
    )


@router.post("/api/qa", response_model=QAResponse)
async def qa_endpoint(payload: QARequest, container: ContainerDep) -> QAResponse:
    return _response(await container.qa.run(_input(payload)))


@router.post("/api/qa/stream")
async def qa_stream(payload: QARequest, container: ContainerDep) -> StreamingResponse:
    async def event_generator():
        async for item in container.qa.stream(_input(payload)):
            if isinstance(item, PipelineEvent):
                if item.event_type == "token":
                    yield f"token: {json.dumps({'text': item.text or ''}, ensure_ascii=False)}\n\n"
                    continue
                # Keep the existing frontend-compatible event envelope during migration.
                event = AgentStageEvent(
                    stage=item.stage.value,
                    status=item.status.value,
                    detail=item.detail,
                )
                yield f"data: {event.model_dump_json()}\n\n"
            else:
                response = _response(item)
                yield f"final: {response.model_dump_json()}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/api/safety/metrics")
async def safety_metrics(container: ContainerDep):
    """Read local audit data for the demo metrics panel; no metrics are fabricated."""
    path = container.qa.audit.path  # JSONLAuditSink is the configured local adapter.
    entries = []
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    if line.strip():
                        entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    by_category: dict[str, int] = {}
    flagged = 0
    for entry in entries:
        category = entry.get("category", "unknown")
        by_category[category] = by_category.get(category, 0) + 1
        flagged += int(bool(entry.get("flagged")))
    return {
        "total_queries": len(entries),
        "by_category": by_category,
        "flagged_count": flagged,
        "recent": entries[-10:][::-1],
    }
