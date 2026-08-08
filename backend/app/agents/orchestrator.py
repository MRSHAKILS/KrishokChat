"""Orchestrator — ties the 4-stage agent pipeline together."""
from __future__ import annotations

import json
from typing import AsyncGenerator

from app.agents.safety_agent import classify_query
from app.agents.retrieval_agent import retrieve
from app.agents.generation_agent import generate_answer
from app.agents.verifier_agent import verify
from app.agents.audit_logger import log_safety_decision
from app.models.schemas import AgentStageEvent, QAResponse, SourceNode


async def run_qa_streaming(query: str) -> AsyncGenerator[str, None]:
    """Yields SSE-formatted agent stage events, then the final QAResponse."""
    def emit(stage: str, status: str, detail: str | None = None) -> str:
        ev = AgentStageEvent(stage=stage, status=status, detail=detail)
        return f"data: {ev.model_dump_json()}\n\n"

    # Stage 1: Safety
    yield emit("safety", "start")
    safety = classify_query(query)
    cat = safety["category"]
    yield emit("safety", "complete", f"{cat} ({safety.get('reasoning', '')[:80]})")

    if cat in {"banned_or_restricted_chemical", "self_harm_or_poisoning_risk", "off_topic", "prompt_injection"}:
        canned = safety.get("canned_response") or "অনুগ্রহ করে কৃষি সংক্রান্ত প্রশ্ন করুন।"
        log_safety_decision(query, cat, "blocked-canned-response", False, None)
        resp = QAResponse(
            query=query, category=cat, answer=canned,
            sources=[], confidence="blocked",
            agent_trace=[
                AgentStageEvent(stage="safety", status="complete", detail=cat),
                AgentStageEvent(stage="retrieval", status="skip"),
                AgentStageEvent(stage="generation", status="skip"),
                AgentStageEvent(stage="verifier", status="skip"),
            ],
        )
        yield f"final: {resp.model_dump_json()}\n\n"
        return

    # Stage 2: Retrieval
    yield emit("retrieval", "start")
    sources = retrieve(query, top_k=5)
    yield emit("retrieval", "complete", f"{len(sources)} sources")

    # Stage 3: Generation
    yield emit("generation", "start")
    gen = generate_answer(query, sources)
    yield emit("generation", "complete", gen["confidence"])

    # Stage 4: Verifier
    yield emit("verifier", "start")
    ver = verify(gen["answer"], sources)
    yield emit("verifier", "complete", ver["confidence"])

    flagged = bool(ver["flags"])
    log_safety_decision(query, cat, "answered", flagged, "; ".join(ver["flags"]) or None)

    source_nodes = [
        SourceNode(id=s["id"], score=s["score"],
                   crop_bn=None, crop_en=None, disease_bn=None,
                   question=None, answer=s.get("content_bn") or s.get("content_en"),
                   source=s.get("source"), expert_verified=False)
        for s in sources[:5]
    ]

    trace = [
        AgentStageEvent(stage="safety", status="complete", detail=cat),
        AgentStageEvent(stage="retrieval", status="complete", detail=f"{len(sources)} sources"),
        AgentStageEvent(stage="generation", status="complete", detail=gen["confidence"]),
        AgentStageEvent(stage="verifier", status="complete", detail=ver["confidence"]),
    ]

    resp = QAResponse(
        query=query, category=cat, answer=gen["answer"],
        sources=source_nodes, confidence=ver["confidence"],
        agent_trace=trace,
    )
    yield f"final: {resp.model_dump_json()}\n\n"
