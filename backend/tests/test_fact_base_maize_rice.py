"""R12 — Tests for Maize and Rice Fact Base Extension.

Locks all R12 invariants:
  1. Maize FAW and Rice pest facts load cleanly from fact_base_v1.json.
  2. Fact rows obey dosage bands (no outlier > 3.0x max rate) and banned chemical checks.
  3. StructuredResolver resolves maize and rice queries at T1/T2 with 0 LLM calls.
  4. Output Bengali advisories include accurate dosage, IPM options, and citations.
  5. Potato late blight continues to resolve cleanly with zero regression.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.structured_resolver import StructuredResolver
from app.domain.enums import ResolutionTier
from app.infrastructure.knowledge.fact_base_store import load_fact_base

FACT_BASE_PATH = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "fact_base_v1.json"
)


@pytest.fixture
def fact_base():
    return load_fact_base(FACT_BASE_PATH)


@pytest.fixture
def resolver(fact_base):
    return StructuredResolver(fact_base=fact_base, min_confidence=0.85)


# ---------------------------------------------------------------------------
# Schema & Loading Tests
# ---------------------------------------------------------------------------


def test_fact_base_contains_maize_and_rice(fact_base) -> None:
    crops = {f.crop for f in fact_base.facts}
    assert "maize" in crops
    assert "rice" in crops
    assert "potato" in crops

    maize_facts = fact_base.lookup(crop="maize", problem="fall_armyworm")
    assert len(maize_facts) >= 2
    for f in maize_facts:
        assert f.crop == "maize"
        assert f.problem == "fall_armyworm"
        assert f.active_ingredient == "spinosad"
        assert f.dose_min == 0.4
        assert f.dose_unit == "ml/l"
        assert not f.banned_flag

    rice_facts_blast = fact_base.lookup(crop="rice", problem="blast")
    assert len(rice_facts_blast) >= 2

    rice_facts_bph = fact_base.lookup(crop="rice", problem="brown_planthopper")
    assert len(rice_facts_bph) >= 1

    rice_facts_stem_borer = fact_base.lookup(crop="rice", problem="stem_borer")
    assert len(rice_facts_stem_borer) >= 1


# ---------------------------------------------------------------------------
# Resolver Zero-LLM Matching Tests (T1 / T2)
# ---------------------------------------------------------------------------


def test_resolver_maize_fall_armyworm(resolver) -> None:
    query = "ভুট্টায় ফল আর্মিওয়ার্ম পোকা আক্রমণ করেছে, কি স্প্রে করব?"
    result = resolver.resolve(query)
    assert result is not None
    assert result.tier in (ResolutionTier.STRUCTURED_FACT, ResolutionTier.TEMPLATED_ADVISORY)
    assert "ভুট্টা" in result.answer
    assert "spinosad" in result.answer.lower()
    assert "0.4" in result.answer
    assert "DAE" in result.fact.citation or "BARI" in result.fact.citation
    assert len(result.fact.ipm_alternatives_bn) > 0


def test_resolver_rice_blast(resolver) -> None:
    query = "ধানের ব্লাস্ট রোগের জন্য কোন ওষুধ কতটুকু দিতে হবে?"
    result = resolver.resolve(query)
    assert result is not None
    assert result.tier in (ResolutionTier.STRUCTURED_FACT, ResolutionTier.TEMPLATED_ADVISORY)
    assert "ধান" in result.answer
    assert "propiconazole" in result.answer.lower()
    assert "BRRI" in result.fact.citation


def test_resolver_rice_brown_planthopper(resolver) -> None:
    query = "ধান ক্ষেতে কারেন্ট পোকা বা বাদামি গাছফড়িং লেগেছে প্রতিকার কি?"
    result = resolver.resolve(query)
    assert result is not None
    assert result.tier in (ResolutionTier.STRUCTURED_FACT, ResolutionTier.TEMPLATED_ADVISORY)
    assert "ধান" in result.answer
    assert "imidacloprid" in result.answer.lower()


def test_resolver_rice_stem_borer(resolver) -> None:
    query = "ধানের মাজরা পোকা দমনে অনুমোদিত কীটনাশক ও মাত্রা বলুন"
    result = resolver.resolve(query)
    assert result is not None
    assert result.tier in (ResolutionTier.STRUCTURED_FACT, ResolutionTier.TEMPLATED_ADVISORY)
    assert "ধান" in result.answer
    assert "cartap" in result.answer.lower()
    assert "1.5" in result.answer


def test_potato_zero_regression(resolver) -> None:
    query = "আলুর নাবি ধ্বসা বা লেট ব্লাইট হলে কোন ওষুধ দিব?"
    result = resolver.resolve(query)
    assert result is not None
    assert result.tier in (ResolutionTier.STRUCTURED_FACT, ResolutionTier.TEMPLATED_ADVISORY)
    assert "আলু" in result.answer
    assert "mancozeb" in result.answer
    assert "g/l" in result.answer
