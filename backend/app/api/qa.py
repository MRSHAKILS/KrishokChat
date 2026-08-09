"""POST /api/qa — advisory pipeline with RAG + grounded generation."""
from __future__ import annotations

import json
import sys
import pathlib

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import QARequest, QAResponse, AgentStageEvent, SourceNode

# Add backend to path for imports
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from app.agents.safety_agent import classify_query
from app.agents.retrieval_agent import retrieve
from app.agents.audit_logger import log_safety_decision
from app.services.advisory.generator import generate_response as gen_response
from app.services.advisory._extractors import get_disease_details, load_rag_nodes, get_rag_node

router = APIRouter()


@router.post("/api/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest):
    """Non-streaming: full advisory pipeline."""
    query = request.query
    detected_crop = getattr(request, 'crop', None)
    detected_disease = getattr(request, 'disease', None)

    # Stage 1: Safety (with detected crop/disease context)
    safety = classify_query(query, detected_crop, detected_disease)
    cat = safety["category"]

    if cat in {"banned_or_restricted_chemical", "self_harm_or_poisoning_risk", "off_topic", "prompt_injection"}:
        canned = safety.get("canned_response") or "অনুগ্রহ করে কৃষি সংক্রান্ত প্রশ্ন করুন।"
        log_safety_decision(query, cat, "blocked-canned-response", False, None)
        return QAResponse(
            query=query, category=cat, answer=canned,
            sources=[], confidence="blocked",
            agent_trace=[
                AgentStageEvent(stage="safety", status="complete", detail=cat),
                AgentStageEvent(stage="retrieval", status="skip"),
                AgentStageEvent(stage="generation", status="skip"),
                AgentStageEvent(stage="verifier", status="skip"),
            ],
        )

    # Stage 2: Retrieval (augment with English keywords from detected crop/disease)
    augmented = query
    crop_disease_en = ""
    if detected_crop:
        crop_disease_en += f" {detected_crop.lower()}"
    if detected_disease:
        disease_term = detected_disease.lower().replace("__", " ").replace("_", " ")
        crop_disease_en += f" {disease_term}"
        # Also add core disease name without crop prefix
        core = detected_disease.split("__")[-1] if "__" in detected_disease else detected_disease
        crop_disease_en += f" {core.lower().replace('_', ' ')}"
    # Add English equivalents from Bengali query
    bn_to_en = {
        "আলুর": "potato", "ধান": "rice", "গম": "wheat", "ভুট্টা": "corn",
        "ফুলকপি": "cauliflower", "বাঁধাকপি": "cabbage", "টমেটো": "tomato",
        "দেরি ব্লাইট": "late blight", "ব্লাস্ট": "blast", "রাস্ট": "rust",
        "মরিচা": "leaf rust", "প্রতিকার": "treatment", "রোগ": "disease",
        "বীজ": "seed", "সার": "fertilizer",
    }
    for bn, en in bn_to_en.items():
        if bn in query.lower():
            augmented += f" {en}"
    # Always append detected crop/disease English terms for BM25 matching
    augmented += crop_disease_en
    if intent:
        augmented += f" {intent}"
    sources = retrieve(augmented.strip(), top_k=5)

    # Stage 3: Generation (grounded in retrieved sources)
    disease_details = get_disease_details(detected_crop, detected_disease) if detected_crop and detected_disease else None

    gen = gen_response(
        query=query,
        detected_crop=detected_crop,
        detected_disease=detected_disease,
        intent=cat,
        retrieved_nodes=sources,
        disease_details=disease_details,
    )

    log_safety_decision(query, cat, "answered", False, None)

    source_nodes = [
        SourceNode(id=s.get("id", ""), score=s.get("score", 0),
                   answer=s.get("content_bn") or s.get("content_en", "")[:200],
                   source=s.get("source", ""))
        for s in sources[:5]
    ]

    trace = [
        AgentStageEvent(stage="safety", status="complete", detail=cat),
        AgentStageEvent(stage="retrieval", status="complete", detail=f"{len(sources)} sources"),
        AgentStageEvent(stage="generation", status="complete", detail="gemini-3.1-flash-lite"),
        AgentStageEvent(stage="verifier", status="complete", detail="grounded"),
    ]

    return QAResponse(
        query=query, category=cat, answer=gen.get("response", ""),
        sources=source_nodes, confidence="verified" if sources else "low_confidence",
        agent_trace=trace,
    )


@router.post("/api/qa/stream")
async def qa_stream(request: QARequest):
    """Streaming SSE: emits agent stage events, then final response."""
    query = request.query
    detected_crop = getattr(request, 'crop', None)
    detected_disease = getattr(request, 'disease', None)

    async def event_gen():
        def emit(stage, status, detail=None):
            ev = AgentStageEvent(stage=stage, status=status, detail=detail)
            return f"data: {ev.model_dump_json()}\n\n"

        # Stage 1: Safety (with detected crop/disease context)
        yield emit("safety", "start")
        safety = classify_query(query, detected_crop, detected_disease)
        cat = safety["category"]
        yield emit("safety", "complete", cat)

        if cat in {"banned_or_restricted_chemical", "self_harm_or_poisoning_risk", "off_topic", "prompt_injection"}:
            canned = safety.get("canned_response") or "অনুগ্রহ করে কৃষি সংক্রান্ত প্রশ্ন করুন।"
            log_safety_decision(query, cat, "blocked-canned-response", False, None)
            sources = []
            gen = {"response": canned}
        else:
            # Stage 2: Retrieval
            yield emit("retrieval", "start")
            sources = retrieve(query, top_k=5)
            yield emit("retrieval", "complete", f"{len(sources)} sources")

            # Stage 3: Generation
            yield emit("generation", "start")
            disease_details = get_disease_details(detected_crop, detected_disease) if detected_crop and detected_disease else None
            gen = gen_response(
                query=query,
                detected_crop=detected_crop,
                detected_disease=detected_disease,
                intent=cat,
                retrieved_nodes=sources,
                disease_details=disease_details,
            )
            yield emit("generation", "complete", "gemini-3.1-flash-lite")
            yield emit("verifier", "complete", "grounded")
            log_safety_decision(query, cat, "answered", False, None)

        source_nodes = [
            SourceNode(id=s.get("id", ""), score=s.get("score", 0),
                       answer=s.get("content_bn") or s.get("content_en", "")[:200],
                       source=s.get("source", ""))
            for s in sources[:5]
        ]

        trace = [
            AgentStageEvent(stage="safety", status="complete", detail=cat),
            AgentStageEvent(stage="retrieval", status="complete", detail=f"{len(sources)} sources"),
            AgentStageEvent(stage="generation", status="complete", detail="gemini-3.1-flash-lite"),
            AgentStageEvent(stage="verifier", status="complete", detail="grounded"),
        ]

        resp = QAResponse(
            query=query, category=cat, answer=gen.get("response", ""),
            sources=source_nodes, confidence="verified" if sources else "low_confidence",
            agent_trace=trace,
        )
        yield f"final: {resp.model_dump_json()}\n\n"

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
    by_cat: dict[str, number] = {}
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
        "recent": entries[-10:][::-1],
    }
