"""POST /api/qa — full agentic pipeline (JSON + SSE stream)."""
from __future__ import annotations

import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.agents.orchestrator import run_qa_streaming
from app.models.schemas import QARequest, QAResponse

router = APIRouter()


@router.post("/api/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest):
    """Non-streaming: runs the full pipeline, returns the final response."""
    final = None
    async for chunk in run_qa_streaming(request.query):
        if chunk.startswith("final:"):
            final = chunk[len("final:"):].strip()
    if final:
        return QAResponse.model_validate_json(final)
    return QAResponse(query=request.query, category="low_confidence",
                     answer="Pipeline error.", sources=[], confidence="low_confidence")


@router.post("/api/qa/stream")
async def qa_stream(request: QARequest):
    """Streaming SSE: emits agent stage events, then the final QAResponse."""
    async def event_gen():
        async for chunk in run_qa_streaming(request.query):
            yield chunk
    return StreamingResponse(event_gen(), media_type="text/event-stream")


@router.get("/api/safety/metrics")
async def safety_metrics():
    """Returns safety audit breakdown."""
    from pathlib import Path
    log_path = Path(__file__).resolve().parent.parent / "logs" / "safety_audit.jsonl"
    entries = []
    if log_path.exists():
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except Exception:
                        pass
    by_cat: dict[str, int] = {}
    flagged = 0
    for e in entries:
        cat = e.get("category", "unknown")
        by_cat[cat] = by_cat.get(cat, 0) + 1
        if e.get("flagged"):
            flagged += 1
    return {
        "total_queries": len(entries),
        "by_category": by_cat,
        "flagged_count": flagged,
        "recent": entries[-10:],
    }
