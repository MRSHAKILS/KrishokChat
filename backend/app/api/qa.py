"""QA HTTP adapters. All behavior is delegated to one application pipeline."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.application.container import AppContainer
from app.application.qa_pipeline import QAInput
from app.domain.contracts import PipelineEvent, QAResult, RetrievedSource
from app.models.schemas import AgentStageEvent, QARequest, QAResponse, SourceNode, VerifierClaimOut
from app.api.dependencies import get_container

router = APIRouter()

# P0-2: SSE keep-alive interval. When the pipeline produces no event for this
# long (cold local model, slow provider), the route emits an SSE comment line
# so proxies/NAT do not drop the idle connection. Comments are ignored by
# EventSource clients, so the event protocol is unchanged.
SSE_HEARTBEAT_SECONDS = 15.0


ContainerDep = Annotated[AppContainer, Depends(get_container)]


def _input(request: QARequest) -> QAInput:
    return QAInput(
        query=request.query,
        session_id=request.session_id,
        crop=request.crop,
        disease=request.disease,
        history=request.history,
        model=request.model,
    )


PUBLISHER_MAP_BN = {
    "DAE": "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)",
    "BARC": "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)",
    "BARI": "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)",
    "BRRI": "বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI)",
    "SRDI": "মৃত্তিকা সম্পদ উন্নয়ন ইনস্টিটিউট (SRDI)",
    "BSRTI": "বাংলাদেশ রেশম গবেষণা ও প্রশিক্ষণ ইনস্টিটিউট (BSRTI)",
    "CDB": "তুলা উন্নয়ন বোর্ড (CDB)",
    "DoF": "মৎস্য অধিদপ্তর (DoF)",
    "DLS": "প্রাণিসম্পদ অধিদপ্তর (DLS)",
    "IRRI": "আন্তর্জাতিক ধান গবেষণা ইনস্টিটিউট (IRRI)",
    "CABI": "সিএবিআই ক্রপ স্পেকট্রাম (CABI)",
    "WorldFish": "ওয়ার্ল্ডফিশ (WorldFish)",
    "Ministry of Agriculture": "কৃষি মন্ত্রণালয়, গণপ্রজাতন্ত্রী বাংলাদেশ সরকার",
    "NARS": "জাতীয় কৃষি গবেষণা সিস্টেম (NARS)",
}


def _source(source: RetrievedSource) -> SourceNode:
    pub_raw = str(source.metadata.get("publisher") or "").strip()
    pub_bn = PUBLISHER_MAP_BN.get(pub_raw, pub_raw)
    if not pub_bn:
        sid = source.id.upper()
        if sid.startswith("DAE"):
            pub_bn = "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)"
        elif sid.startswith("BARC") or sid.startswith("B4") or sid.startswith("B5"):
            pub_bn = "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)"
        elif sid.startswith("BARI"):
            pub_bn = "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)"
        elif sid.startswith("BRRI"):
            pub_bn = "বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI)"
        elif sid.startswith("CABI"):
            pub_bn = "সিএবিআই ক্রপ স্পেকট্রাম (CABI)"
        elif sid.startswith("IRRI"):
            pub_bn = "আন্তর্জাতিক ধান গবেষণা ইনস্টিটিউট (IRRI)"
        else:
            pub_bn = "জাতীয় কৃষি গবেষণা সংস্থা"

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
        publisher=pub_raw or None,
        publisher_bn=pub_bn,
        title_bn=source.title_bn or source.metadata.get("title_bn") or None,
        title_en=source.title_en or source.metadata.get("title_en") or None,
        citation=source.citation or source.metadata.get("citation") or None,
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
        verifier_claims=[
            VerifierClaimOut(claim=claim.text, verdict=claim.verdict, reason=claim.reason)
            for claim in result.verifier_claims
        ],
        model=result.model or None,
        matched_rules=list(result.matched_rules),
        safety_reason=result.safety_reason,
    )


@router.post("/api/qa", response_model=QAResponse)
async def qa_endpoint(payload: QARequest, container: ContainerDep) -> QAResponse:
    return _response(await container.qa.run(_input(payload)))


@router.post("/api/qa/stream")
async def qa_stream(payload: QARequest, container: ContainerDep) -> StreamingResponse:
    # P0-2: SSE keep-alive via task+queue pattern.
    #
    # IMPORTANT: do NOT use asyncio.wait_for(anext(pipeline_items), timeout)
    # directly. When wait_for times out it cancels the underlying anext()
    # coroutine, which propagates CancelledError into the async generator and
    # kills the Ollama/httpx connection mid-flight. This is the root cause of
    # the "no final response" error with the local CPU model (~75s inference).
    #
    # Fix: run the pipeline in a separate asyncio Task that drains items into
    # a Queue. The SSE generator reads from the queue with a short timeout and
    # emits keepalive comments when empty. The pipeline task is never cancelled
    # by a keepalive timeout, so the Ollama call runs to completion.
    _SENTINEL = object()
    queue: asyncio.Queue[object] = asyncio.Queue()

    async def _drain_pipeline() -> None:
        try:
            async for item in container.qa.stream(_input(payload)):
                await queue.put(item)
        except Exception as exc:  # noqa: BLE001
            await queue.put(exc)
        finally:
            await queue.put(_SENTINEL)

    pipeline_task = asyncio.create_task(_drain_pipeline())

    async def event_generator():
        try:
            while True:
                try:
                    item = await asyncio.wait_for(queue.get(), SSE_HEARTBEAT_SECONDS)
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
                    continue

                if item is _SENTINEL:
                    break
                if isinstance(item, Exception):
                    # Surface the error as a final safety-rejection response
                    # so the frontend shows something rather than silently failing.
                    import logging
                    logging.getLogger("krishokchat.stream").error(
                        "Pipeline error during SSE stream: %s", item, exc_info=item
                    )
                    break
                if isinstance(item, PipelineEvent):
                    if item.event_type == "token":
                        yield f"token: {json.dumps({'text': item.text or ''}, ensure_ascii=False)}\n\n"
                        continue
                    event = AgentStageEvent(
                        stage=item.stage.value,
                        status=item.status.value,
                        detail=item.detail,
                    )
                    yield f"data: {event.model_dump_json()}\n\n"
                else:
                    response = _response(item)
                    yield f"final: {response.model_dump_json()}\n\n"
        finally:
            # Always cancel the pipeline task if the client disconnects early.
            pipeline_task.cancel()

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
    verifier_checked = verifier_grounded = verifier_unsupported = 0
    answered_without_sources = 0
    router_blocked = 0
    refusal_rules: dict[str, int] = {}
    retrieval_answered = retrieval_hits = 0
    top1_scores: list[float] = []
    source_counts: list[int] = []
    # Pipeline aggregates count only v2 entries (recorded by the current
    # pipeline with per-step validity fields). Legacy rows stay visible in
    # `recent` but cannot skew the live panel.
    v2_entries = [e for e in entries if e.get("pipeline_version") == 2]
    # B1 demo cache: cached=true rows are exact replays of previously verified
    # answers. They count toward totals and the category mix (they are real
    # queries served), but are excluded from per-stage aggregates — a replay
    # performs no new retrieval or verification work.
    cached_entries = [e for e in v2_entries if e.get("cached")]
    stage_entries = [e for e in v2_entries if not e.get("cached")]
    for entry in v2_entries:
        category = entry.get("category", "unknown")
        by_category[category] = by_category.get(category, 0) + 1
        flagged += int(bool(entry.get("flagged")))
    for entry in stage_entries:
        # P1: verifier aggregates come from the actual logged verdicts.
        verifier_checked += int(entry.get("verifier_checked", 0))
        verifier_grounded += int(entry.get("verifier_grounded", 0))
        verifier_unsupported += int(entry.get("verifier_unsupported", 0))
        answered_without_sources += int(bool(entry.get("answered_without_sources", False)))
        # P2 per-step aggregates: router refusals, retrieval hit-rate and
        # top-1 scores, all computed from the same logged decisions the
        # UI stepper renders (dual-view, nothing fabricated).
        if entry.get("action") == "blocked-canned-response":
            router_blocked += 1
            for rule in entry.get("safety_matched_rules") or []:
                refusal_rules[rule] = refusal_rules.get(rule, 0) + 1
        if entry.get("category") == "safe_agri" and entry.get("action") == "answered":
            retrieval_answered += 1
            retrieval_hits += int(bool(entry.get("retrieval_hit", False)))
            if isinstance(entry.get("retrieval_top1_score"), (int, float)):
                top1_scores.append(float(entry["retrieval_top1_score"]))
            if isinstance(entry.get("retrieved_count"), int):
                source_counts.append(int(entry["retrieved_count"]))
    total = len(v2_entries) or 1
    return {
        "total_queries": len(entries),
        "pipeline_queries": len(v2_entries),
        "by_category": by_category,
        "flagged_count": flagged,
        "cached": {
            "replays": len(cached_entries),
        },
        "verifier": {
            "checked": verifier_checked,
            "grounded": verifier_grounded,
            "unsupported": verifier_unsupported,
            "pass_rate": (verifier_grounded / verifier_checked) if verifier_checked else None,
        },
        "refusals": {
            "answered_without_sources": answered_without_sources,
        },
        "router": {
            "blocked": router_blocked,
            "refusal_rate": router_blocked / total,
            "refusal_rules": refusal_rules,
        },
        "retrieval": {
            "answered": retrieval_answered,
            "hit_rate": (retrieval_hits / retrieval_answered) if retrieval_answered else None,
            "avg_top1_score": (sum(top1_scores) / len(top1_scores)) if top1_scores else None,
            "avg_sources": (sum(source_counts) / len(source_counts)) if source_counts else None,
        },
        "recent": entries[-10:][::-1],
    }
