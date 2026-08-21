"""T15 structured verifier candidate — fail-closed unit tests.

Required coverage (spec row T15): unit/dimension, denominator, interval, PHI,
polarity, applicability, conflict, missing evidence, Bengali numerals, plus a
batch asserting that HARD FAILURES NEVER CERTIFY (the T15 gate).

Fail-closed expectations honored here:
- R1/R2 (dosage/chemical) claims REQUIRE a resolved chemical identity to certify.
- R3 (cultural/timing, no chemical) claims certify on a supported relation.
- non-affirmed polarity, source conflict, and parse failures never certify.

The candidate modules under backend/app/infrastructure/verification/ are new
files; the runtime pipeline and `dosage.py` are untouched.

Run:  python -m pytest research_artifacts/tests -q
"""
from __future__ import annotations

import sys
from pathlib import Path

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

from app.domain.contracts import RetrievedSource  # noqa: E402
from app.infrastructure.verification.structured import StructuredVerifier  # noqa: E402

VERIFIER = StructuredVerifier()


def src(bn: str) -> RetrievedSource:
    return RetrievedSource(id="SRC-1", score=1.0, content_bn=bn)


def verdict(answer: str, bn: str):
    return VERIFIER.verify(answer, [src(bn)] if bn else [], source_ids=("SRC-1",))


# ---------------------------------------------------------------------------
class TestBengaliNumerals:
    def test_bengali_digits_parse_and_match(self) -> None:
        v = verdict("Ripcord প্রতি লিটার পানিতে ৫০ মিলি ব্যবহার করুন।",
                    "Ripcord প্রতি লিটার পানিতে ৫০ মিলি ব্যবহার করুন।")
        assert v.confidence == "verified"

    def test_decimal_bengali(self) -> None:
        v = verdict("১.৫ কেজি ইউরিয়া দিন।", "১.৫ কেজি ইউরিয়া দিন।")
        assert v.confidence == "verified"

    def test_comma_decimal(self) -> None:
        v = verdict("2,5 লিটার ঔষধ মেশান।", "2,5 লিটার ঔষধ মেশান।")
        assert v.confidence == "verified"


# ---------------------------------------------------------------------------
class TestUnitDimension:
    def test_matching_unit_supported(self) -> None:
        v = verdict("Ripcord প্রতি লিটারে 2 ml মেশান।", "Ripcord প্রতি লিটারে 2 ml মেশান।")
        assert v.confidence == "verified"

    def test_wrong_unit_is_not_certified(self) -> None:
        # claim ml, evidence g -> unit dimension conflict -> abstain
        v = verdict("Ripcord প্রতি লিটারে 2 ml মেশান।", "Ripcord প্রতি লিটারে 2 g মেশান।")
        assert v.confidence == "flagged-unverified"
        assert all(not c.certifiable for c in v.claims)

    def test_wrong_amount_is_not_certified(self) -> None:
        v = verdict("Ripcord প্রতি লিটারে 5 ml মেশান।", "Ripcord প্রতি লিটারে 2 ml মেশান।")
        assert v.confidence == "flagged-unverified"

    def test_bare_amount_without_unit_is_not_certified(self) -> None:
        # parse failure: number present but no amount+unit parse -> fail closed
        v = verdict("সার ৫০ ব্যবহার করুন।", "সার ৫০ ব্যবহার করুন।")
        assert v.confidence == "flagged-unverified"
        assert v.parse_failures


# ---------------------------------------------------------------------------
class TestDenominator:
    def test_matching_denominator_supported(self) -> None:
        v = verdict("Ripcord ১০ কেজি প্রতি হেক্টর দিন।", "Ripcord ১০ কেজি প্রতি হেক্টর দিন।")
        assert v.confidence == "verified"

    def test_mismatched_denominator_not_certified(self) -> None:
        v = verdict("Ripcord ১০ কেজি প্রতি হেক্টর দিন।", "Ripcord ১০ কেজি প্রতি শতক দিন।")
        assert v.confidence == "flagged-unverified"
        assert any("denominator" in r for c in v.claims for r in c.reasons)

    def test_denominator_absent_in_evidence_not_certified(self) -> None:
        v = verdict("Ripcord ১০ কেজি প্রতি হেক্টর দিন।", "Ripcord ১০ কেজি দিন।")
        assert v.confidence == "flagged-unverified"


# ---------------------------------------------------------------------------
class TestInterval:
    def test_matching_interval_supported(self) -> None:
        # R3 timing claim: certifies on supported relation without a chemical
        v = verdict("৭ দিন পরপর স্প্রে করুন।", "প্রতি ৭ দিন পরপর স্প্রে করুন।")
        c = v.claims[0]
        assert c.relation == "supported", c.reasons
        assert v.confidence == "verified"

    def test_conflicting_interval_not_certified(self) -> None:
        v = verdict("৭ দিন পরপর স্প্রে করুন।", "১০ দিন পরপর স্প্রে করুন।")
        assert v.confidence == "flagged-unverified"
        assert any("interval" in r for c in v.claims for r in c.reasons)


# ---------------------------------------------------------------------------
class TestPHI:
    def test_matching_phi_supported(self) -> None:
        v = verdict("Ripcord ফসল তোলার ৭ দিন আগে স্প্রে করুন।",
                    "Ripcord ফসল তোলার ৭ দিন আগে স্প্রে করুন।")
        assert v.confidence == "verified"

    def test_conflicting_phi_not_certified(self) -> None:
        v = verdict("Ripcord ফসল তোলার ৭ দিন আগে স্প্রে করুন।",
                    "Ripcord ফসল তোলার ১৪ দিন আগে স্প্রে করুন।")
        assert v.confidence == "flagged-unverified"

    def test_phi_missing_in_evidence_not_certified(self) -> None:
        v = verdict("Ripcord ফসল তোলার ৭ দিন আগে স্প্রে করুন।", "Ripcord স্প্রে করুন।")
        assert v.confidence == "flagged-unverified"
        assert any("phi" in r for c in v.claims for r in c.reasons)


# ---------------------------------------------------------------------------
class TestPolarity:
    def test_negated_claim_never_certifies(self) -> None:
        v = verdict("Ripcord ব্যবহার করবেন না।", "Ripcord ব্যবহার করবেন না।")
        assert v.confidence == "flagged-unverified"
        assert all(not c.certifiable for c in v.claims)

    def test_prohibited_never_certifies(self) -> None:
        v = verdict("রোগাক্রান্ত অংশে ঔষধ প্রয়োগ নিষিদ্ধ।", "রোগাক্রান্ত অংশে ঔষধ প্রয়োগ নিষিদ্ধ।")
        assert v.confidence == "flagged-unverified"

    def test_conditional_never_certifies(self) -> None:
        v = verdict("যদি রোগ দেখা দেয় তবে Ripcord 2 ml স্প্রে করুন।",
                    "যদি রোগ দেখা দেয় তবে Ripcord 2 ml স্প্রে করুন।")
        assert v.confidence == "flagged-unverified"


# ---------------------------------------------------------------------------
class TestApplicability:
    def test_claim_condition_blocks_certification(self) -> None:
        # conditional polarity is non-affirmed -> blocked by design
        v = verdict("পোকার আক্রমণ হলে Ripcord প্রতি লিটারে 2 ml স্প্রে করুন।",
                    "প্রতি লিটারে 2 ml স্প্রে করুন।")
        assert v.confidence == "flagged-unverified"
        assert any("polarity" in r for c in v.claims for r in c.reasons)


# ---------------------------------------------------------------------------
class TestConflict:
    def test_source_conflict_is_ambiguous_never_certifies(self) -> None:
        v = verdict("Ripcord 2 ml স্প্রে করুন।",
                    "Ripcord প্রতি লিটারে 2 ml স্প্রে করুন। অথবা Ripcord 5 ml স্প্রে করুন।")
        assert v.confidence == "flagged-unverified"
        assert all(not c.certifiable for c in v.claims)


# ---------------------------------------------------------------------------
class TestMissingEvidence:
    def test_no_sources_with_claims_is_flagged(self) -> None:
        v = verdict("Ripcord প্রতি লিটারে 2 ml ব্যবহার করুন।", "")
        assert v.confidence == "flagged-unverified"

    def test_no_sources_without_claims_is_low_confidence(self) -> None:
        v = verdict("পরিষ্কার পানি ব্যবহার করুন।", "")
        assert v.confidence == "low_confidence"

    def test_claim_chemical_absent_from_evidence_is_unsupported(self) -> None:
        v = verdict("Ripcord 2 ml স্প্রে করুন।", "শুধু পাতা পরিষ্কার রাখুন।")
        assert v.confidence == "flagged-unverified"
        assert all(c.relation == "unsupported" for c in v.claims)


# ---------------------------------------------------------------------------
class TestFailClosedBatch:
    """The T15 gate: hard failures never certify (confidence != verified)."""

    HARD_FAILURES = [
        ("unit dimension mismatch", "Ripcord 2 ml", "Ripcord 2 g"),
        ("amount mismatch", "Ripcord 5 ml", "Ripcord 2 ml"),
        ("denominator mismatch", "Ripcord 10 kg per ha", "Ripcord 10 kg per শতক"),
        ("interval mismatch", "7 দিন পরপর", "10 দিন পরপর"),
        ("phi mismatch", "Ripcord ফসল তোলার 7 দিন আগে", "Ripcord ফসল তোলার 14 দিন আগে"),
        ("source conflict", "Ripcord 2 ml", "Ripcord 2 ml অথবা 5 ml"),
        ("negated polarity", "Ripcord ব্যবহার করবেন না", "Ripcord ব্যবহার করবেন না"),
        ("bare number", "সার 50", "সার 50"),
        ("chemical unknown", "2 ml দিন", "2 ml দিন"),
    ]

    def test_no_hard_failure_certifies(self) -> None:
        for name, claim_side, ev_side in self.HARD_FAILURES:
            v = verdict(f"{claim_side} স্প্রে করুন।", f"{ev_side} স্প্রে করুন।")
            assert v.confidence != "verified", f"certified under hard failure: {name}"


# ---------------------------------------------------------------------------
class TestOracleFieldMode:
    def test_oracle_override_enables_decomposition(self) -> None:
        # parser cannot resolve chemical; oracle supplies it -> matching may certify
        v = VERIFIER.verify(
            "2 ml স্প্রে করুন।",
            [src("Ripcord 2 ml স্প্রে করুন।")],
            oracle_fields={0: {"chemicals": ["ripcord"]}},
        )
        assert v.claims[0].oracle_override is True
        assert v.claims[0].relation == "supported"
        assert v.confidence == "verified"

    def test_oracle_can_force_fail(self) -> None:
        v = VERIFIER.verify(
            "Ripcord 2 ml স্প্রে করুন।",
            [src("Ripcord 2 ml স্প্রে করুন।")],
            oracle_fields={0: {"amount_pairs": [(9.0, "kg")]}},
        )
        assert v.confidence == "flagged-unverified"


if __name__ == "__main__":
    raise SystemExit(0)