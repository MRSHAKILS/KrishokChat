import pytest
from app.domain.answerability import AnswerabilityEvaluator
from app.domain.contracts import RetrievedSource
from app.domain.enums import AnswerabilityLevel, ResolutionTier, SafetyCategory, VerificationConfidence
from app.domain.intent import Intent
from app.application.generation import format_progressive_guidance_text


def test_a5_unsafe_action_on_banned_chemical():
    lvl = AnswerabilityEvaluator.evaluate(
        category=SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
        intent=None,
        query="কার্বোফিউরান দিলে কী হবে?",
        has_crop=True,
    )
    assert lvl == AnswerabilityLevel.A5_UNSAFE_ACTION


def test_a5_unsafe_action_on_self_harm():
    lvl = AnswerabilityEvaluator.evaluate(
        category=SafetyCategory.SELF_HARM_OR_POISONING_RISK,
        intent=None,
        query="বিষ খেয়ে ফেলেছি",
        has_crop=False,
    )
    assert lvl == AnswerabilityLevel.A5_UNSAFE_ACTION


def test_a1_fully_supported_on_fact_base():
    lvl = AnswerabilityEvaluator.evaluate(
        category=SafetyCategory.SAFE_AGRI,
        intent=Intent(kind="fertilizer", crop="rice"),
        query="ব্রি ধান ২৮ এ ইউরিয়া সারের মাত্রা কত?",
        has_crop=True,
        is_fact_resolved=True,
    )
    assert lvl == AnswerabilityLevel.A1_FULLY_SUPPORTED


def test_a4_missing_critical_info_without_crop():
    ambiguous_intent = Intent(
        kind="treatment",
        crop=None,
        problem="leaf spot",
        is_ambiguous=True,
    )
    lvl = AnswerabilityEvaluator.evaluate(
        category=SafetyCategory.SAFE_AGRI,
        intent=ambiguous_intent,
        query="পাতায় গোল বাদামি দাগ, কী ওষুধ দেব?",
        has_crop=False,
    )
    assert lvl == AnswerabilityLevel.A4_MISSING_CRITICAL_INFO


def test_a2_strong_evidence_with_verified_dosage():
    source = RetrievedSource(
        id="BARI_POTATO_01",
        score=0.89,
        title_bn="আলুর নাবি ধসা রোগ",
        content_bn="রিডোমিল গোল্ড প্রতি লিটার পানিতে ২ গ্রাম হারে স্প্রে করতে হবে।",
        metadata={"dosage": "2 g/L", "treatment_summary_bn": "রিডোমিল গোল্ড ২ গ্রাম/লি."},
    )
    lvl = AnswerabilityEvaluator.evaluate(
        category=SafetyCategory.SAFE_AGRI,
        intent=Intent(kind="treatment", crop="potato", problem="late blight"),
        query="আলুর নাবি ধসা রোগের ওষুধ ও ডোজ কত?",
        has_crop=True,
        retrieved_sources=[source],
    )
    assert lvl == AnswerabilityLevel.A2_STRONG_EVIDENCE


def test_a3_partial_evidence_without_dosage():
    source = RetrievedSource(
        id="BRRI_GENERAL_02",
        score=0.65,
        title_bn="ধানের ব্লাস্ট রোগ",
        content_bn="ধানের ব্লাস্ট একটি ক্ষতিকর ছত্রাকজনিত রোগ। রোগাক্রান্ত জমিতে অতিরিক্ত সার দেওয়া যাবে না।",
        metadata={},  # No verified dosage
    )
    lvl = AnswerabilityEvaluator.evaluate(
        category=SafetyCategory.SAFE_AGRI,
        intent=Intent(kind="treatment", crop="rice", problem="blast"),
        query="ধানের ব্লাস্ট হলে কী পরিচর্যা করব?",
        has_crop=True,
        retrieved_sources=[source],
    )
    assert lvl == AnswerabilityLevel.A3_PARTIAL_EVIDENCE


def test_build_progressive_guidance_structure():
    guidance = AnswerabilityEvaluator.build_progressive_guidance(
        crop="ধান",
        problem="পাতাপোড়া রোগ",
    )
    assert guidance["mode"] == "progressive_cultural_guidance"
    assert guidance["is_non_chemical"] is True
    assert len(guidance["field_checks_bn"]) >= 2
    assert len(guidance["cultural_controls_bn"]) >= 2
    assert "১৬১২৩" in guidance["safety_boundary_bn"]

    # Test formatted text rendering
    formatted = format_progressive_guidance_text(guidance)
    assert "মাঠে পর্যবেক্ষণ করুন" in formatted
    assert "পরিবেশবান্ধব ও সাধারণ পরিচর্যা" in formatted
    assert "সতর্কতা ও যোগাযোগ" in formatted
    assert "১৬১২৩" in formatted


@pytest.mark.asyncio
async def test_qa_pipeline_progressive_guidance_replaces_referral(tmp_path):
    from unittest.mock import AsyncMock, MagicMock
    from app.application.qa_pipeline import QAInput, QAPipeline
    from app.domain.contracts import GenerationResult, VerificationResult, SafetyDecision
    from app.ports.verifier import Verifier

    safety_decision = SafetyDecision(
        category=SafetyCategory.SAFE_AGRI,
        confidence=0.95,
        intent=Intent(kind="treatment", crop="বেগুন", problem="ডগা শুকানো"),
    )
    fake_safety = AsyncMock()
    fake_safety.classify = AsyncMock(return_value=safety_decision)

    fake_retriever = MagicMock()
    fake_retriever.retrieve = MagicMock(return_value=[])  # Empty sources -> would normally trigger REFERRAL

    fake_generator = MagicMock()
    fake_generator.generate = AsyncMock(
        return_value=GenerationResult(
            answer="দুঃখিত, এই প্রশ্নের নির্ভরযোগ্য উত্তর এখন দেওয়া সম্ভব নয়। স্থানীয় পরামর্শের জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।",
            used_source_ids=(),
            model="stub",
        )
    )
    fake_generator.client = None

    fake_verifier = MagicMock(spec=Verifier)
    fake_verifier.verify = MagicMock(
        return_value=VerificationResult(confidence=VerificationConfidence.VERIFIED)
    )

    fake_audit = MagicMock()
    fake_audit.record = MagicMock()
    fake_audit.path = tmp_path / "audit.jsonl"

    fake_sessions = MagicMock()
    fake_sessions.get = MagicMock(return_value=[])
    fake_sessions.append = MagicMock()

    pipeline = QAPipeline(
        safety=fake_safety,
        retriever=fake_retriever,
        generator=fake_generator,
        verifier=fake_verifier,
        audit=fake_audit,
        sessions=fake_sessions,
    )

    result = await pipeline.run(QAInput(query="আমার বেগুনের ডগা শুকিয়ে যাচ্ছে, কী করব?"))

    assert result.resolution_tier is ResolutionTier.PROGRESSIVE_GUIDANCE
    assert result.answerability_level is AnswerabilityLevel.A3_PARTIAL_EVIDENCE
    assert "মাঠে পর্যবেক্ষণ করুন" in result.answer
    assert "পরিবেশবান্ধব ও সাধারণ পরিচর্যা" in result.answer
    assert "১৬১২৩" in result.answer
    assert result.progressive_guidance is not None

