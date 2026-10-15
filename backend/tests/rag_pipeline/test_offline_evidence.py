"""Keyless evidence lane: behavior with the safety classifier unreachable.

The lane is opt-in (offline_evidence=True). These tests pin the safety properties:
off by default, the deterministic precheck still wins, a crop is required, doses and
chemicals are withheld, and no LLM generation ever runs.
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.offline_evidence import (
    BOUNDARY_BN,
    clean_sentences,
    render_answer,
    select_excerpts,
)
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.safety import SafetyClassifier
from app.application.verifier import HardenedDosageVerifier
from app.domain.contracts import RetrievedSource
from app.domain.enums import ResolutionTier, SafetyCategory
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.sessions.memory import InMemorySessionStore
from app.infrastructure.verification.dosage_claims import extract_claims

CLEAN = "আলুর পাতায় বাদামী দাগ দেখা দিলে রোগের আক্রমণ বোঝা যায়।"
DOSE = "প্রতি লিটার পানিতে ২ গ্রাম ম্যানকোজেব মিশিয়ে স্প্রে করুন।"
CHEMICAL = "কার্বেন্ডাজিম ছত্রাকনাশক ব্যবহার করলে রোগ কমে যায় বলে জানা যায়।"


def _source(
    sid: str, text: str, *, title: str = "আলু রোগ নির্দেশিকা", title_en: str = "Potato guide"
) -> RetrievedSource:
    return RetrievedSource(
        id=sid, score=1.0, title_en=title_en, title_bn=title,
        content_en="", content_bn=text, source="BARI", citation="BARI",
    )


class _Retriever:
    def __init__(self, sources: list[RetrievedSource]) -> None:
        self.sources = sources
        self.calls = 0

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        self.calls += 1
        return self.sources[:top_k]


class _ForbiddenGenerator:
    """Fails the test if any generation path is reached."""

    client = None

    async def generate(self, *a, **k):
        raise AssertionError("generation must not run in the keyless lane")

    async def stream(self, *a, **k):
        raise AssertionError("generation must not run in the keyless lane")
        yield ""  # pragma: no cover

    async def generate_from_text(self, *a, **k):
        raise AssertionError("generation must not run in the keyless lane")


def _outage_classifier() -> SafetyClassifier:
    client = MagicMock()
    client.classify_json = AsyncMock(side_effect=RuntimeError("no provider key"))
    return SafetyClassifier(client)


def _pipeline(sources: list[RetrievedSource], *, offline: bool) -> tuple[QAPipeline, _Retriever]:
    retriever = _Retriever(sources)
    pipeline = QAPipeline(
        safety=_outage_classifier(),
        retriever=retriever,
        generator=_ForbiddenGenerator(),
        verifier=HardenedDosageVerifier(),
        audit=JSONLAuditSink(Path(tempfile.gettempdir()) / "krishokchat_offline_evidence_audit.jsonl"),
        sessions=InMemorySessionStore(max_turns=10, ttl_seconds=1800),
        top_k=5,
        offline_evidence=offline,
    )
    return pipeline, retriever


def _ask(pipeline: QAPipeline, query: str):
    return asyncio.run(pipeline.run(QAInput(query=query)))


# ---- unit: sentence screen ------------------------------------------------


def test_clean_sentences_keeps_descriptions_and_drops_doses_and_chemicals() -> None:
    kept = clean_sentences(" ".join([CLEAN, DOSE, CHEMICAL]))
    assert kept == [CLEAN.rstrip("।")] or kept == [CLEAN]
    assert not any("গ্রাম" in s or "ম্যানকোজেব" in s or "কার্বেন্ডাজিম" in s for s in kept)


def test_sentences_with_any_digit_or_imperative_are_withheld() -> None:
    glued = "কাঙ্ক্ষিত ফলন ৩০০ কেজিগাছবছর ধরা হয়েছে এই জাতের জন্য।"
    imperative = "আক্রান্ত পাতা সংগ্রহ করে জমি থেকে দূরে সরিয়ে ফেলুন এবং পুড়িয়ে দিন।"
    kept = clean_sentences(" ".join([glued, imperative, CLEAN]))
    assert kept in ([CLEAN], [CLEAN.rstrip("।")])


def test_precomposed_and_decomposed_yo_are_both_withheld() -> None:
    decomposed = "ছিপছিপে পানি থাকা অবস্থায় প্রয়োগ করে মাটির সাথে মিশিয়ে দেওয়া উত্তম।"
    precomposed = decomposed.replace("য়", "য়")
    assert precomposed != decomposed
    assert clean_sentences(decomposed) == []
    assert clean_sentences(precomposed) == []


def test_imperative_verbs_are_withheld() -> None:
    assert clean_sentences("কালো দাগ রোধ করতে ফল মাটিতে রাখা থেকে বিরত থাকুন বলে জানা যায়।") == []


def test_render_answer_ends_with_the_safety_boundary() -> None:
    answer = render_answer(select_excerpts([_source("a", CLEAN)], ["দাগ"]))
    assert answer.rstrip().endswith(BOUNDARY_BN)


# ---- pipeline -------------------------------------------------------------


def test_off_by_default_outage_stays_a_referral() -> None:
    pipeline, retriever = _pipeline([_source("a", CLEAN)], offline=False)
    result = _ask(pipeline, "আলুর পাতায় দাগ পড়েছে")
    assert result.resolution_tier is ResolutionTier.HONEST_REFUSAL
    assert result.category is SafetyCategory.LOW_CONFIDENCE
    assert retriever.calls == 0


def test_on_with_crop_returns_clean_excerpts_without_generation() -> None:
    pipeline, retriever = _pipeline(
        [_source("a", " ".join([CLEAN, DOSE, CHEMICAL]))], offline=True
    )
    result = _ask(pipeline, "আলুর পাতায় দাগ পড়েছে")
    assert retriever.calls == 1
    assert result.resolution_tier is ResolutionTier.PROGRESSIVE_GUIDANCE
    assert result.category is SafetyCategory.LOW_CONFIDENCE
    assert CLEAN.rstrip("।") in result.answer
    body = result.answer.replace(BOUNDARY_BN, "")
    assert "২ গ্রাম" not in body and "ম্যানকোজেব" not in body and "কার্বেন্ডাজিম" not in body
    assert not any(c.has_dosage or c.chemicals for c in extract_claims(
        "\n".join(l[2:] for l in body.splitlines() if l.startswith("• "))
    ))


def test_deterministic_precheck_still_blocks_before_the_lane() -> None:
    pipeline, retriever = _pipeline([_source("a", CLEAN)], offline=True)
    result = _ask(pipeline, "ধানে কীটনাশক হিসেবে প্যারাকোয়াট স্প্রে করলে কেমন হবে")
    assert result.resolution_tier is ResolutionTier.DETERMINISTIC_GUARD
    assert result.category is SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL
    assert retriever.calls == 0


def test_no_crop_means_no_lane_and_no_retrieval() -> None:
    pipeline, retriever = _pipeline([_source("a", CLEAN)], offline=True)
    result = _ask(pipeline, "আজকের আবহাওয়া কেমন থাকবে")
    assert result.resolution_tier is ResolutionTier.HONEST_REFUSAL
    assert retriever.calls == 0


def test_source_for_another_crop_is_not_shown() -> None:
    rice = _source("r", "ধানের পাতায় বাদামী দাগ দেখা দিলে রোগের আক্রমণ বোঝা যায়।", title="ধান রোগ নির্দেশিকা", title_en="Rice guide")
    pipeline, _ = _pipeline([rice], offline=True)
    result = _ask(pipeline, "আলুর পাতায় দাগ পড়েছে")
    assert result.resolution_tier is ResolutionTier.HONEST_REFUSAL


def test_clean_sentence_sharing_no_rare_word_with_the_question_is_not_shown() -> None:
    unrelated = _source("u", "আলু সংরক্ষণের জন্য শুকনো ও ঠান্ডা স্থান বেছে নেওয়া হয়।")
    pipeline, retriever = _pipeline([unrelated], offline=True)
    result = _ask(pipeline, "আলুর পাতায় দাগ পড়েছে")
    assert retriever.calls == 1
    assert result.resolution_tier is ResolutionTier.HONEST_REFUSAL


def test_passage_naming_several_crops_is_not_shown() -> None:
    mixed = _source("m", "ধান ও আলুর পাতায় বাদামী দাগ দেখা দিলে রোগের আক্রমণ বোঝা যায়।", title_en="Rice and potato guide")
    pipeline, _ = _pipeline([mixed], offline=True)
    result = _ask(pipeline, "আলুর পাতায় দাগ পড়েছে")
    assert result.resolution_tier is ResolutionTier.HONEST_REFUSAL


def test_only_withheld_sentences_fall_back_to_the_referral() -> None:
    pipeline, _ = _pipeline([_source("a", " ".join([DOSE, CHEMICAL]))], offline=True)
    result = _ask(pipeline, "আলুর পাতায় দাগ পড়েছে")
    assert result.resolution_tier is ResolutionTier.HONEST_REFUSAL


def test_crop_filter_disabled_disables_the_lane(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RETRIEVAL_CROP_FILTER", "0")
    pipeline, retriever = _pipeline([_source("a", CLEAN)], offline=True)
    result = _ask(pipeline, "আলুর পাতায় দাগ পড়েছে")
    assert result.resolution_tier is ResolutionTier.HONEST_REFUSAL
    assert retriever.calls == 0
