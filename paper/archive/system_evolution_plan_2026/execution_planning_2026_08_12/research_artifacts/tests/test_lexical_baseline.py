"""T12 lexical baseline unit tests — Bengali digit/unit fixtures + parity.

Parity block reproduces the captured runtime tests
(`backend/tests/test_pipeline.py::VerifierTests`) with identical inputs and
asserts against the SAME imported runtime module — this pins the baseline to the
captured revision: any behavioral drift in the copied expectations fails here.

Run (research harness, offline only):
  python -m pytest research_artifacts/tests -q
"""
from __future__ import annotations

import sys
from pathlib import Path

# --- bootstrap backend import path (same bootstrap as run_lexical_baseline.py) ---
_SCRIPT_DIR = Path(__file__).resolve().parent
_BACKEND = None
_p = _SCRIPT_DIR.parent
for _ in range(6):
    if (_p / "backend" / "app" / "infrastructure" / "verification" / "dosage.py").exists():
        _BACKEND = _p / "backend"
        break
    _p = _p.parent
if _BACKEND is None:
    raise RuntimeError("backend/ not located from research_artifacts/tests/")
sys.path.insert(0, str(_BACKEND))
# ------------------------------------------------------------------------------

from app.domain.contracts import RetrievedSource  # noqa: E402
from app.infrastructure.verification.dosage import DosageVerifier  # noqa: E402


def src(content_bn: str) -> RetrievedSource:
    return RetrievedSource(id="SRC-1", score=1.0, content_bn=content_bn)


class TestParityWithCapturedRuntimeTests:
    """Identical to backend/tests/test_pipeline.py::VerifierTests (captured revision)."""

    def test_bengali_numeral_dosage_is_matched_after_normalization(self) -> None:
        source = src("প্রতি লিটার পানিতে ২ মিলি ব্যবহার করুন।")
        result = DosageVerifier().verify("প্রতি লিটার পানিতে 2 ml ব্যবহার করুন।", [source])
        assert result.confidence.value == "verified"

    def test_ungrounded_dosage_is_flagged(self) -> None:
        source = src("পাতা পরিষ্কার রাখুন।")
        result = DosageVerifier().verify("প্রতি লিটারে ৫০ মিলি ব্যবহার করুন।", [source])
        assert result.confidence.value == "flagged-unverified"
        assert result.unverified_claims


class TestBengaliDigitFixtures:
    """All ten Bengali digits transliterate and match ASCII forms."""

    def test_all_bengali_digits_match_ascii(self) -> None:
        source = src("প্রতি লিটার পানিতে ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯ গ্রাম ব্যবহার করুন।")
        result = DosageVerifier().verify(
            "প্রতি লিটার পানিতে 0 1 2 3 4 5 6 7 8 9 g ব্যবহার করুন।", [source])
        assert result.confidence.value == "verified"

    def test_bengali_decimal_amount(self) -> None:
        source = src("১.৫ কেজি সার প্রয়োগ করুন।")
        result = DosageVerifier().verify("1.5 kg সার প্রয়োগ করুন।", [source])
        assert result.confidence.value == "verified"

    def test_bengali_comma_decimal_matches_dot_form(self) -> None:
        source = src("২,৫ লিটার পানি মেশান।")
        result = DosageVerifier().verify("2.5 l পানি মেশান।", [source])
        assert result.confidence.value == "verified"


class TestBengaliUnitFixtures:
    """Unit alias canonicalization: Bengali spellings match canonical codes."""

    def test_mililitre_alias(self) -> None:
        source = src("প্রতি লিটারে ৫ মিলিলিটার ঔষধ।")
        result = DosageVerifier().verify("প্রতি লিটারে 5 ml ঔষধ।", [source])
        assert result.confidence.value == "verified"

    def test_mili_alias(self) -> None:
        source = src("প্রতি লিটারে ৫ মিলি ঔষধ।")
        result = DosageVerifier().verify("প্রতি লিটারে 5 ml ঔষধ।", [source])
        assert result.confidence.value == "verified"

    def test_miligram_alias(self) -> None:
        source = src("৫ মিলিগ্রাম ওষুধ।")
        result = DosageVerifier().verify("5 mg ওষুধ।", [source])
        assert result.confidence.value == "verified"

    def test_gram_alias(self) -> None:
        source = src("১০ গ্রাম কীটনাশক।")
        result = DosageVerifier().verify("10 g কীটনাশক।", [source])
        assert result.confidence.value == "verified"

    def test_kilo_alias(self) -> None:
        source = src("২ কেজি ইউরিয়া।")
        result = DosageVerifier().verify("2 kg ইউরিয়া।", [source])
        assert result.confidence.value == "verified"

    def test_litre_alias(self) -> None:
        source = src("৩ লিটার পানি।")
        result = DosageVerifier().verify("3 l পানি।", [source])
        assert result.confidence.value == "verified"

    def test_case_insensitive_english_units(self) -> None:
        source = src("5 MG প্রতি লিটারে।")
        result = DosageVerifier().verify("5 mg প্রতি লিটারে।", [source])
        assert result.confidence.value == "verified"


class TestFractionFixtures:
    """Fraction claims (আধা/অর্ধেক + unit) extract and match."""

    def test_half_spoon_claim_is_verified_against_source(self) -> None:
        source = src("প্রতি লিটারে আধা চামচ ওষুধ মেশান।")
        result = DosageVerifier().verify("প্রতি লিটারে আধা চামচ ওষুধ মেশান।", [source])
        assert result.confidence.value == "verified"

    def test_half_cup_mismatch_is_flagged(self) -> None:
        source = src("প্রতি লিটারে এক চামচ ওষুধ মেশান।")
        result = DosageVerifier().verify("প্রতি লিটারে অর্ধেক কাপ ওষুধ মেশান।", [source])
        assert result.confidence.value == "flagged-unverified"
        assert any("অর্ধেক" in c for c in result.unverified_claims)


class TestSourceBoundaryBehavior:
    """Runtime branch order (captured): unverified claims checked BEFORE no-source.
    So claims with no sources -> flagged-unverified; only no-claims + no-sources
    reaches low_confidence."""

    def test_no_sources_with_claims_is_flagged_unverified(self) -> None:
        # Captured behavior: the unverified branch precedes the no-source branch.
        result = DosageVerifier().verify("প্রতি লিটারে 2 ml ব্যবহার করুন।", [])
        assert result.confidence.value == "flagged-unverified"
        assert list(result.unverified_claims) == ["2 ml"]

    def test_no_source_with_no_claims_is_low_confidence(self) -> None:
        result = DosageVerifier().verify("পরিষ্কার পানি ব্যবহার করুন।", [])
        assert result.confidence.value == "low_confidence"


class TestClaimExtractionBoundaries:
    """Regex boundaries: amount+unit only; no bare amounts; no cross-unit grab."""

    def test_bare_amount_without_unit_is_not_a_claim(self) -> None:
        source = src("সার ৫০ ব্যবহার করুন।")
        result = DosageVerifier().verify("সার ৫০ ব্যবহার করুন।", [source])
        assert result.confidence.value == "verified"  # no claim -> nothing to flag

    def test_number_then_unit_across_unicode_boundary(self) -> None:
        source = src("৫ কেজি/হেক্টর।")
        result = DosageVerifier().verify("5 কেজি প্রতি হেক্টরে।", [source])
        # Different claim surface: "5 কেজি" vs "৫ কেজি" normalize equal, so verified.
        assert result.confidence.value == "verified"

    def test_comma_separated_quantities_normalize_to_dot_and_match(self) -> None:
        # Captured behavior: _normalize converts "," -> "." so "2 kg, 3 kg" and
        # "২ কেজি, ৩ কেজি" both become "2 kg. 3 kg" -> both claims present -> verified.
        source = src("২ কেজি, ৩ কেজি সার।")
        result = DosageVerifier().verify("2 kg, 3 kg সার।", [source])
        assert result.confidence.value == "verified"


if __name__ == "__main__":
    raise SystemExit(0)