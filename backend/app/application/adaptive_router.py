"""Stage 2B: Adaptive Retrieval Router (PRISM-RAG Module 2B.4).

Dynamically dispatches agricultural queries to specialized retrieval routes
rather than treating every input as an undifferentiated vector search.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.domain.concept_normalizer import ConceptNormalizer, NormalizedConceptResult
from app.domain.query_extractor import QueryExtractor, QueryInformationState
from app.domain.working_memory import AgriculturalWorkingMemory


class RetrievalRoute(str, Enum):
    """Specialized retrieval routes in PRISM-RAG."""

    ROUTE_A_FACT_BASE = "fact_base"
    ROUTE_B_DOCUMENT_RAG = "document_rag"
    ROUTE_C_CONCEPT_HYPOTHESES = "concept_hypotheses"
    ROUTE_D_CONVERSATIONAL_FOLLOW_UP = "conversational_follow_up"


@dataclass(frozen=True)
class AdaptiveRoutingDecision:
    """Decision output detailing the selected route and rewritten query terms."""

    route: RetrievalRoute
    primary_query: str
    expanded_queries: tuple[str, ...] = field(default_factory=tuple)
    candidate_hypotheses: tuple[str, ...] = field(default_factory=tuple)
    rationale: str = ""


class AdaptiveRetrievalRouter:
    """Intelligently routes queries based on information state and conversational memory."""

    @classmethod
    def route(
        cls,
        query: str,
        working_memory: AgriculturalWorkingMemory | None = None,
    ) -> AdaptiveRoutingDecision:
        memory = working_memory or AgriculturalWorkingMemory()
        info_state: QueryInformationState = QueryExtractor.extract(query)

        # Merge new observations with memory
        effective_crop = info_state.crop or memory.crop
        effective_symptom = info_state.symptom or memory.symptom
        effective_location = info_state.location or memory.location

        # 1. Route D: Conversational Follow-Up
        if info_state.intent == "follow_up" and (memory.crop or memory.disease_candidate):
            context_query = f"{memory.crop or ''} {memory.disease_candidate or memory.symptom or ''} প্রতিকার চিকিৎসা দমন"
            return AdaptiveRoutingDecision(
                route=RetrievalRoute.ROUTE_D_CONVERSATIONAL_FOLLOW_UP,
                primary_query=context_query.strip(),
                expanded_queries=(query, context_query.strip()),
                candidate_hypotheses=memory.candidate_hypotheses,
                rationale="Follow-up query bound to active session working memory.",
            )

        # 2. Route A: Structured Fact Base (Fertilizer, seed rate, quantitative numbers)
        if info_state.intent in ("fertilizer", "crop_calendar") or any(
            kw in query.lower() for kw in ("কতটুকু সার", "কেজি সার", "ইউরিয়া কত", "বীজের হার", "দূরত্ব")
        ):
            crop_kw = info_state.crop_bn or (info_state.crop if info_state.crop else "")
            fact_query = f"{crop_kw} {query}".strip()
            return AdaptiveRoutingDecision(
                route=RetrievalRoute.ROUTE_A_FACT_BASE,
                primary_query=fact_query,
                expanded_queries=(fact_query,),
                rationale="Direct quantitative/dosage fact lookup routed to structured fact base.",
            )

        # 3. Route C: Concept & Symptom Hypotheses (Colloquial symptom without fixed disease name)
        concept_res: NormalizedConceptResult = ConceptNormalizer.normalize(
            query,
            crop=effective_crop,
        )
        if concept_res.concept_id or (effective_symptom and not memory.disease_candidate):
            hypotheses = concept_res.retrieval_hypotheses
            crop_prefix = effective_crop or ""
            expanded = tuple(
                f"{crop_prefix} {h}".strip() for h in hypotheses
            )
            return AdaptiveRoutingDecision(
                route=RetrievalRoute.ROUTE_C_CONCEPT_HYPOTHESES,
                primary_query=query,
                expanded_queries=expanded or (query,),
                candidate_hypotheses=hypotheses,
                rationale=f"Symptom expression normalized to concept '{concept_res.concept_id or 'symptom'}' with {len(hypotheses)} diagnostic hypotheses.",
            )

        # 4. Route B: Standard Grounded Document RAG
        context_parts = [query]
        if effective_crop and effective_crop not in query.lower():
            context_parts.append(effective_crop)
        if effective_location and effective_location not in query:
            context_parts.append(effective_location)

        primary = " ".join(context_parts)
        return AdaptiveRoutingDecision(
            route=RetrievalRoute.ROUTE_B_DOCUMENT_RAG,
            primary_query=primary,
            expanded_queries=(primary,),
            candidate_hypotheses=(),
            rationale="Standard grounded semantic document retrieval.",
        )
