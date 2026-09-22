"""Stage 2B Tests: Adaptive Conversational Retrieval & Query Understanding (PRISM-RAG).

Validates:
1. QueryExtractor: slot and intent extraction across Bangladeshi dialects.
2. AgriculturalWorkingMemory: state transitions, multi-turn accumulation, and topic shift detection.
3. ConceptNormalizer: authentic farmer colloquialisms to canonical agronomic concepts.
4. AdaptiveRetrievalRouter: dynamic routing across Fact Base, Semantic RAG, and Concept Hypotheses.
5. EvidenceAgreementGate: multi-source disagreement detection and discriminative MNC questions.
6. End-to-end multi-turn memory in QAPipeline.
"""

from __future__ import annotations

import pytest
from app.application.adaptive_router import AdaptiveRetrievalRouter, RetrievalRoute
from app.application.evidence_agreement import EvidenceAgreementGate
from app.domain.concept_normalizer import ConceptNormalizer
from app.domain.enums import AnswerabilityLevel, ResolutionTier
from app.domain.query_extractor import QueryExtractor
from app.domain.working_memory import AgriculturalWorkingMemory


# ===========================================================================
# 1. QueryExtractor Tests (Module 2B.1)
# ===========================================================================

def test_query_extractor_crop_dialects():
    # Sylheti / Chittagonian / Rural colloquial crop aliases
    res1 = QueryExtractor.extract("ধানর পাতাত কি রোগ?")
    assert res1.crop == "rice"

    res2 = QueryExtractor.extract("মরিস গাছ মইরা যায়")
    assert res2.crop == "chilli"

    res3 = QueryExtractor.extract("বাইঙ্গন ক্ষেতে পোকা ধরছে")
    assert res3.crop == "brinjal"

    res4 = QueryExtractor.extract("আলুত কি সার দেওন লাগব?")
    assert res4.crop == "potato"
    assert res4.intent == "fertilizer"


def test_query_extractor_location_and_temporal():
    query = "আমার বাড়ি নাটোরে, গত সপ্তাহে ভারী বৃষ্টির পর ধানের গাছ হলুদ হইয়া গেছে"
    info = QueryExtractor.extract(query)
    assert info.location == "Natore"
    assert info.temporal_event == "বৃষ্টির পর"
    assert info.crop == "rice"
    assert info.symptom == "গাছ হলুদ"


def test_query_extractor_follow_up():
    query = "আগেরবার যে ওষুধের কথা বলছিলা সেইটার নাম আবার কও"
    info = QueryExtractor.extract(query)
    assert info.intent == "follow_up"


# ===========================================================================
# 2. AgriculturalWorkingMemory Tests (Module 2B.2)
# ===========================================================================

def test_working_memory_multi_turn_accumulation():
    mem = AgriculturalWorkingMemory()

    # Turn 1: User mentions crop and symptom
    mem1 = mem.merge(crop="rice", symptom="বাদামি দাগ")
    assert mem1.crop == "rice"
    assert mem1.symptom == "বাদামি দাগ"
    assert mem1.turns_count == 1

    # Turn 2: User provides temporal context without repeating crop
    mem2 = mem1.merge(temporal_event="বৃষ্টির পর")
    assert mem2.crop == "rice"  # preserved!
    assert mem2.symptom == "বাদামি দাগ"  # preserved!
    assert mem2.temporal_event == "বৃষ্টির পর"
    assert mem2.turns_count == 2

    # Turn 3: User provides location
    mem3 = mem2.merge(location="Natore")
    assert mem3.crop == "rice"
    assert mem3.location == "Natore"
    assert mem3.temporal_event == "বৃষ্টির পর"
    assert mem3.turns_count == 3
    assert "ফসল: rice" in mem3.as_context_line()
    assert "এলাকা: Natore" in mem3.as_context_line()


def test_working_memory_topic_shift_resets_problem():
    mem = AgriculturalWorkingMemory(
        crop="rice",
        disease_candidate="ব্লাস্ট রোগ",
        symptom="বাদামি দাগ",
    )
    # User shifts topic to potato
    new_mem = mem.merge(crop="potato")
    assert new_mem.crop == "potato"
    assert new_mem.disease_candidate is None  # reset on topic shift!
    assert new_mem.symptom is None


def test_working_memory_serialization():
    mem = AgriculturalWorkingMemory(
        crop="rice",
        symptom="হলুদ পাতা",
        location="Bogura",
        candidate_hypotheses=("টুংরো", "নাইট্রোজেন ঘাটতি"),
    )
    d = mem.to_dict()
    restored = AgriculturalWorkingMemory.from_dict(d)
    assert restored.crop == "rice"
    assert restored.location == "Bogura"
    assert restored.candidate_hypotheses == ("টুংরো", "নাইট্রোজেন ঘাটতি")


# ===========================================================================
# 3. ConceptNormalizer Tests (Module 2B.3)
# ===========================================================================

def test_concept_normalizer_leaf_blight_scorch():
    res = ConceptNormalizer.normalize("ধানের পাতা পুইড়া যাইতেছে কি করুম?", crop="rice")
    assert res.concept_id == "leaf_blight_scorch"
    assert "খোলপোড়া রোগ (Sheath Blight)" in res.retrieval_hypotheses
    assert len(res.discriminative_features) > 0


def test_concept_normalizer_wilting():
    res = ConceptNormalizer.normalize("বেগুনের গাছ মইরা যায়", crop="brinjal")
    assert res.concept_id == "wilting_damping_off"
    assert any("Bacterial Wilt" in h for h in res.retrieval_hypotheses)


def test_concept_normalizer_leaf_curl():
    res = ConceptNormalizer.normalize("মরিচের পাতা কুঁকড়ায় গেছে", crop="chilli")
    assert res.concept_id == "leaf_curl_virus"
    assert any("Chilli Leaf Curl" in h for h in res.retrieval_hypotheses)


def test_concept_normalizer_waterlogging():
    res = ConceptNormalizer.normalize("জমিতে পানি জমে থাকে পানি নামে না")
    assert res.concept_id == "waterlogging_drainage"


# ===========================================================================
# 4. AdaptiveRetrievalRouter Tests (Module 2B.4)
# ===========================================================================

def test_adaptive_router_fact_base():
    decision = AdaptiveRetrievalRouter.route("ধানের জমিতে প্রতি বিঘায় কতটুকু ইউরিয়া সার দিতে হবে?")
    assert decision.route == RetrievalRoute.ROUTE_A_FACT_BASE


def test_adaptive_router_concept_hypotheses():
    decision = AdaptiveRetrievalRouter.route("ধানের পাতা পুইড়া যাইতেছে")
    assert decision.route == RetrievalRoute.ROUTE_C_CONCEPT_HYPOTHESES
    assert len(decision.expanded_queries) > 0


def test_adaptive_router_conversational_follow_up():
    memory = AgriculturalWorkingMemory(crop="rice", disease_candidate="ব্লাস্ট রোগ")
    decision = AdaptiveRetrievalRouter.route("আগেরবার যে ওষুধের কথা বলছিলা সেইটার নাম আবার কও", working_memory=memory)
    assert decision.route == RetrievalRoute.ROUTE_D_CONVERSATIONAL_FOLLOW_UP
    assert "rice" in decision.primary_query
    assert "ব্লাস্ট" in decision.primary_query


# ===========================================================================
# 5. EvidenceAgreementGate Tests (Modules 2B.5 & 2B.6)
# ===========================================================================

def test_evidence_agreement_consistent():
    sources = [
        {"content": "ধানের ব্লাস্ট রোগের আক্রমণে পাতার ওপর তীরের ফলার মতো দাগ দেখা যায়।"},
        {"content": "ব্লাস্ট রোগ দমনে ট্রাইসাইক্লাজোল জাতীয় ছত্রাকনাশক অনুমোদিত মাত্রায় স্প্রে করুন।"},
    ]
    res = EvidenceAgreementGate.evaluate(sources)
    assert not res.is_conflicting
    assert res.agreement_score > 0.8


def test_evidence_agreement_conflicting_blast_vs_brown_spot():
    sources = [
        {"content": "ধানের ব্লাস্ট রোগের আক্রমণে পাতায় চোখের মতো দাগ তৈরি হয়। ট্রাইসাইক্লাজোল স্প্রে করুন।"},
        {"content": "ধানের পাতায় বাদামি দাগ বা ব্রাউন স্পট রোগের ক্ষেত্রে ম্যানকোজেব বা কার্বেনডাজিম ব্যবহার করুন।"},
    ]
    res = EvidenceAgreementGate.evaluate(sources)
    assert res.is_conflicting
    assert "blast" in res.competing_diseases
    assert "brown_spot" in res.competing_diseases
    assert res.discriminative_question is not None
    assert len(res.quick_reply_chips) > 0


def test_evidence_agreement_conflicting_late_vs_early_blight():
    sources = [
        {"content": "আলুর নাবি ধসা বা লেইট ব্লাইট রোগ অতি দ্রুত ছড়ায়। ম্যানকোজেব স্প্রে করতে হবে।"},
        {"content": "আলুর আগাম ধসা বা আর্লি ব্লাইট রোগে পাতায় পর্যায়ক্রমিক চক্রাকার রিং দাগ দেখা যায়।"},
    ]
    res = EvidenceAgreementGate.evaluate(sources)
    assert res.is_conflicting
    assert "late_blight" in res.competing_diseases
    assert "early_blight" in res.competing_diseases
    assert "চক্রাকার" in res.discriminative_question or "রিং" in res.discriminative_question


# ===========================================================================
# 6. Multi-Turn Session Memory in QAPipeline End-to-End
# ===========================================================================

@pytest.mark.asyncio
async def test_pipeline_multi_turn_working_memory():
    from app.application.qa_pipeline import QAInput, QAPipeline
    from app.domain.contracts import QueryContext, RetrievedSource, SafetyDecision
    from app.domain.enums import SafetyCategory
    from app.infrastructure.sessions.memory import InMemorySessionStore

    class MockClassifier:
        async def classify(self, query, context=None):
            return SafetyDecision(
                category=SafetyCategory.SAFE_AGRI,
                confidence=0.98,
                matched_rules=(),
            )

    class MockRetriever:
        def retrieve(self, query, top_k=5):
            return [
                RetrievedSource(
                    id="doc_1",
                    score=0.95,
                    title_en="Rice Blast",
                    title_bn="ধানের ব্লাস্ট",
                    content_en="Treat rice blast with tricyclazole.",
                    content_bn="ধানের ব্লাস্ট দমনে ট্রাইসাইক্লাজোল স্প্রে করুন।",
                    source="BRRI Handbook",
                    citation="BRRI 2024",
                )
            ]

    class MockGenerator:
        async def generate(self, query, context, sources):
            from app.domain.contracts import GenerationOutput
            return GenerationOutput(answer="ট্রাইসাইক্লাজোল ৭৫ ডব্লিউপি প্রতি লিটার পানিতে ০.৭৫ গ্রাম মিশিয়ে স্প্রে করুন।", model="mock")

    class MockVerifier:
        def verify(self, answer, sources):
            from app.domain.contracts import VerificationResult
            from app.domain.enums import VerificationConfidence
            return VerificationResult(confidence=VerificationConfidence.VERIFIED)

    class MockAudit:
        def record(self, event):
            pass

    sessions = InMemorySessionStore()
    pipeline = QAPipeline(
        safety=MockClassifier(),
        retriever=MockRetriever(),
        generator=MockGenerator(),
        verifier=MockVerifier(),
        audit=MockAudit(),
        sessions=sessions,
    )

    session_id = "farmer_test_session_101"

    # Turn 1: Farmer mentions crop only: "আমার ধানের ক্ষেতে সমস্যা দেখা দিছে"
    # Even if this turn gets guidance, the crop "rice" MUST enter working memory!
    res1 = await pipeline.run(QAInput(query="আমার ধানের ক্ষেতে সমস্যা দেখা দিছে", session_id=session_id))
    assert res1 is not None

    mem = sessions.get_working_memory(session_id)
    assert mem is not None
    assert mem["crop"] == "rice"

    # Turn 2: Farmer asks for treatment without repeating the crop:
    # "পাতায় তীরের ফলার মত দাগ, কি স্প্রে করমু?"
    # The pipeline should NOT trigger the missing-crop clarification because crop is in working memory!
    res2 = await pipeline.run(QAInput(query="পাতায় তীরের ফলার মত দাগ, কি স্প্রে করমু?", session_id=session_id))
    assert res2 is not None
    assert res2.resolution_tier != ResolutionTier.INTERACTIVE_CLARIFICATION or "কোন ফসলে" not in res2.answer
    assert res2.answerability_level in (AnswerabilityLevel.A1_FULLY_SUPPORTED, AnswerabilityLevel.A2_STRONG_EVIDENCE, AnswerabilityLevel.A3_PARTIAL_EVIDENCE)
