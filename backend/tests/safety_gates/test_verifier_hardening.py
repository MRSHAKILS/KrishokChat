"""P1 verifier-hardening tests: dosage-claim entailment, annotate-and-drop,
refusal counters, and audit wiring.

Covers the 20-item dosage test set (10 grounded / 10 unsupported), the
chemical-binding regression, the 10 grounded no-false-block guarantee, and the
pipeline-level sanitization + audit behavior.
"""

from __future__ import annotations

import asyncio
import unittest

from app.application.generation import GroundedAnswerGenerator, REFERRAL
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.safety import SafetyClassifier
from app.application.verifier import HardenedDosageVerifier
from app.domain.contracts import RetrievedSource
from app.infrastructure.verification.dosage_claims import (
    claim_grounded,
    extract_claims,
    per_source_normalized,
    sanitize_answer,
)
from tests.test_pipeline import FakeAudit, FakeLLM, FakeRetriever, FakeSessions


def src(content_bn: str, source_id: str = "SRC-1") -> RetrievedSource:
    return RetrievedSource(id=source_id, score=1.0, content_bn=content_bn)


def make_pipeline(llm: FakeLLM, retriever: FakeRetriever, audit: FakeAudit) -> QAPipeline:
    return QAPipeline(
        safety=SafetyClassifier(llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(llm),
        verifier=HardenedDosageVerifier(),
        audit=audit,
        sessions=FakeSessions(),
        top_k=5,
    )


# ---- 20-item dosage test set: (answer, source, expected) -------------------
GROUNDED_CASES: list[tuple[str, str]] = [
    # 1-2: Bengali digits + BN chemical + unit alias
    ("প্রতি লিটার পানিতে ২ মিলি ম্যানকোজেব ব্যবহার করুন।", "প্রতি লিটার পানিতে ২ মিলি ম্যানকোজেব ব্যবহার করুন।"),
    ("ম্যানকোজেব 2 গ্রাম প্রতি লিটারে।", "ম্যানকোজেব 2 g প্রতি লিটার পানিতে।"),
    # 3: মিলিলিটার alias vs ml
    ("৫০ মিলিলিটার ডাইমেথোয়েট।", "ডাইমেথোয়েট 50 ml।"),
    # 4: kg + hectare
    ("ইউরিয়া ১০০ কেজি প্রতি হেক্টর।", "ইউরিয়া ১০০ কেজি প্রতি হেক্টর।"),
    # 5: fraction
    ("আধা চামচ কার্বেন্ডাজিম।", "আধা চামচ কার্বেন্ডাজিম।"),
    # 6: decimal
    ("প্রোপিকোনাজল 2.5 ml।", "প্রোপিকোনাজল 2.5 ml।"),
    # 7: BN digit ১ vs ASCII 1
    ("থায়ামেথক্সাম ১ গ্রাম।", "থায়ামেথক্সাম 1 g।"),
    # 8: English chemical
    ("Imidacloprid 2 ml।", "Imidacloprid 2 ml।"),
    # 9: decimal small
    ("টেবুকোনাজল 0.5 ml।", "টেবুকোনাজল 0.5 ml।"),
    # 10: litre + hectare
    ("ক্লোরপাইরিফস ২ লিটার প্রতি হেক্টর।", "ক্লোরপাইরিফস 2 লিটার প্রতি হেক্টর।"),
]

UNSUPPORTED_CASES: list[tuple[str, str]] = [
    # 11: amount present but DIFFERENT chemical — the binding regression
    ("ম্যানকোজেব 2 ml ব্যবহার করুন।", "ক্লোরপাইরিফস 2 ml ব্যবহার করুন।"),
    # 12: same chemical, different amount
    ("ইউরিয়া 5 কেজি দিন।", "ইউরিয়া 10 কেজি দিন।"),
    # 13: nothing relevant in source
    ("কার্বেন্ডাজিম 1 গ্রাম।", "পাতা পরিষ্কার রাখুন।"),
    # 14: chemical present, amount missing
    ("ডাইমেথোয়েট ৩০ মিলি।", "ডাইমেথোয়েট ব্যবহার করা যেতে পারে।"),
    # 15: same chemical, different amount
    ("গ্লাইফোসেট 2 লিটার।", "গ্লাইফোসেট মাত্র 1 লিটার।"),
    # 16: same unit, different amount
    ("প্রতি কাপে 3 চামচ সার।", "প্রতি কাপে 2 চামচ সার।"),
    # 17: decimal mismatch
    ("অ্যাজোক্সিস্ট্রোবিন 0.75 ml।", "অ্যাজোক্সিস্ট্রোবিন 0.5 ml।"),
    # 18: BN digit amount mismatch
    ("ফিপ্রোনিল ৫০ মিলি।", "ফিপ্রোনিল 100 মিলি।"),
    # 19: unit mismatch
    ("ডেল্টামেথ্রিন 1.25 লিটার।", "ডেল্টামেথ্রিন 1.25 কেজি।"),
    # 20: source empty of any claim element
    ("প্যারাকোয়াট 1 লিটার।", "গাছের পাতা সবুজ।"),
]

# 10 fully grounded answers used for the zero-false-block guarantee.
NO_FALSE_BLOCK_CASES: list[tuple[str, str]] = [
    ("ম্যানকোজেব ২ গ্রাম ব্যবহার করুন।", "ম্যানকোজেব ২ গ্রাম ব্যবহার করুন।"),
    ("ইউরিয়া ১০০ কেজি দিন।", "ইউরিয়া ১০০ কেজি দিন।"),
    ("ডাইমেথোয়েট ৫০ মিলি স্প্রে করুন।", "ডাইমেথোয়েট ৫০ মিলি স্প্রে করুন।"),
    ("কার্বেন্ডাজিম ১ গ্রাম মেশান।", "কার্বেন্ডাজিম ১ গ্রাম মেশান।"),
    ("প্রোপিকোনাজল 0.5 ml ব্যবহার করুন।", "প্রোপিকোনাজল 0.5 ml ব্যবহার করুন।"),
    ("ক্লোরপাইরিফস 2 লিটার দিন।", "ক্লোরপাইরিফস 2 লিটার দিন।"),
    ("থায়ামেথক্সাম ১ গ্রাম।", "থায়ামেথক্সাম ১ গ্রাম।"),
    ("ইমিডাক্লোপ্রিড 2 ml।", "ইমিডাক্লোপ্রিড 2 ml।"),
    ("টেবুকোনাজল 0.5 ml।", "টেবুকোনাজল 0.5 ml।"),
    ("আধা চামচ কার্বেন্ডাজিম।", "আধা চামচ কার্বেন্ডাজিম।"),
]


class DosageSetTests(unittest.TestCase):
    """The 20-item dosage test set: 10 grounded, 10 unsupported."""

    def test_grounded_cases_are_entailed(self) -> None:
        for answer, source_text in GROUNDED_CASES:
            with self.subTest(answer=answer):
                claims = [c for c in extract_claims(answer) if c.has_dosage]
                self.assertTrue(claims, f"no dosage claim extracted from: {answer}")
                self.assertTrue(
                    claim_grounded(claims[0], per_source_normalized([src(source_text)])),
                    f"expected grounded: {answer}",
                )

    def test_unsupported_cases_are_not_entailed(self) -> None:
        for answer, source_text in UNSUPPORTED_CASES:
            with self.subTest(answer=answer):
                claims = [c for c in extract_claims(answer) if c.has_dosage]
                self.assertTrue(claims, f"no dosage claim extracted from: {answer}")
                self.assertFalse(
                    claim_grounded(claims[0], per_source_normalized([src(source_text)])),
                    f"expected unsupported: {answer}",
                )

    def test_no_false_blocks_on_ten_grounded_answers(self) -> None:
        verifier = HardenedDosageVerifier()
        for answer, source_text in NO_FALSE_BLOCK_CASES:
            with self.subTest(answer=answer):
                result = verifier.verify(answer, [src(source_text)])
                self.assertEqual(result.unsupported_count, 0, answer)
                self.assertEqual(result.confidence.value, "verified", answer)
                self.assertEqual(result.flags, (), answer)
                self.assertIsNone(result.sanitized_answer, answer)


class ClaimExtractionTests(unittest.TestCase):
    def test_sentences_split_and_span_preserved(self) -> None:
        answer = "প্রতি লিটারে 2 ml ব্যবহার করুন। পাতায় পানি দিন"
        claims = extract_claims(answer)
        self.assertEqual(len(claims), 2)
        self.assertEqual(claims[0].amounts, ((2.0, "ml"),))
        self.assertEqual(claims[0].has_dosage, True)
        self.assertEqual(claims[1].has_dosage, False)
        self.assertEqual(answer[claims[0].start : claims[0].end], "প্রতি লিটারে 2 ml ব্যবহার করুন")

    def test_fraction_claim_parses(self) -> None:
        claims = extract_claims("আধা চামচ কার্বেন্ডাজিম মেশান।")
        self.assertEqual(claims[0].fractions, ((0.5, "চামচ"),))
        self.assertEqual(claims[0].chemicals, ("কার্বেন্ডাজিম",))

    def test_banglish_units_canonicalize(self) -> None:
        claims = extract_claims("৫০ মিলিলিটার ডাইমেথোয়েট দিন।")
        self.assertEqual(claims[0].amounts, ((50.0, "ml"),))

    def test_chemical_binding_is_detected(self) -> None:
        claims = extract_claims("ম্যানকোজেব 2 ml ব্যবহার করুন।")
        self.assertIn("ম্যানকোজেব", claims[0].chemicals)

    def test_sanitize_drops_only_unsupported_sentence(self) -> None:
        answer = "প্রতি লিটারে 50 মিলি ম্যানকোজেব ব্যবহার করুন। পাতায় পানি দিন।"
        claims = extract_claims(answer)
        unsupported = {claims[0].start}
        sanitized = sanitize_answer(answer, claims, unsupported)
        self.assertEqual(sanitized, "পাতায় পানি দিন।")

    def test_sanitize_returns_none_when_nothing_dropped(self) -> None:
        answer = "পাতায় পানি দিন।"
        claims = extract_claims(answer)
        self.assertIsNone(sanitize_answer(answer, claims, set()))


class HardenedVerifierTests(unittest.TestCase):
    def test_verified_when_all_claims_grounded(self) -> None:
        result = HardenedDosageVerifier().verify(
            "ম্যানকোজেব 2 গ্রাম ব্যবহার করুন।", [src("ম্যানকোজেব 2 গ্রাম ব্যবহার করুন।")]
        )
        self.assertEqual(result.confidence.value, "verified")
        self.assertEqual(result.checked_count, 1)
        self.assertEqual(result.grounded_count, 1)
        self.assertEqual(result.unsupported_count, 0)
        self.assertEqual(result.claims[0].verdict, "grounded")

    def test_binding_regression_different_chemical_same_amount(self) -> None:
        # The old lexical verifier would certify this: "2 ml" appears in the
        # source. The hardened verifier requires the SAME passage to contain
        # the chemical as well.
        result = HardenedDosageVerifier().verify(
            "ম্যানকোজেব 2 ml ব্যবহার করুন।", [src("ক্লোরপাইরিফস 2 ml ব্যবহার করুন।")]
        )
        self.assertEqual(result.confidence.value, "flagged-unverified")
        self.assertEqual(result.unsupported_count, 1)
        self.assertIn("ম্যানকোজেব", result.flags[0])

    def test_unsupported_claim_is_stripped_from_answer(self) -> None:
        answer = "প্রতি লিটারে 50 মিলি ম্যানকোজেব। পাতায় পানি দিন।"
        result = HardenedDosageVerifier().verify(answer, [src("পাতায় পানি দিন।")])
        self.assertEqual(result.sanitized_answer, "পাতায় পানি দিন।")
        self.assertEqual(result.claims[0].verdict, "unsupported")
        self.assertTrue(result.claims[0].reason)

    def test_no_sources_with_dosage_claim_is_flagged_not_verified(self) -> None:
        result = HardenedDosageVerifier().verify("2 ml ম্যানকোজেব।", [])
        self.assertEqual(result.confidence.value, "flagged-unverified")
        self.assertEqual(result.unsupported_count, 1)

    def test_no_sources_without_dosage_claim_is_low_confidence(self) -> None:
        result = HardenedDosageVerifier().verify("পাতায় পানি দিন।", [])
        self.assertEqual(result.confidence.value, "low_confidence")

    def test_no_dosage_sentences_are_informational(self) -> None:
        result = HardenedDosageVerifier().verify("পাতায় পানি দিন।", [src("পাতায় পানি দিন।")])
        self.assertEqual(result.confidence.value, "verified")
        self.assertEqual(result.claims[0].verdict, "no_dosage")
        self.assertEqual(result.checked_count, 0)


class PipelineHardeningTests(unittest.TestCase):
    def test_sanitized_answer_replaces_unsupported_dosage(self) -> None:
        source = src("পাতায় পানি দিন।")
        llm = FakeLLM(answer="প্রতি লিটারে 50 মিলি ম্যানকোজেব ব্যবহার করুন। পাতায় পানি দিন।")
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ম্যানকোজেব কত দেব?")))

        self.assertEqual(result.answer, "পাতায় পানি দিন।")
        self.assertEqual(result.confidence.value, "flagged-unverified")
        self.assertEqual(len(result.verifier_flags), 1)

    def test_empty_sanitized_answer_maps_to_referral(self) -> None:
        source = src("পাতায় পানি দিন।")
        llm = FakeLLM(answer="প্রতি লিটারে 50 মিলি ম্যানকোজেব ব্যবহার করুন।")
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ম্যানকোজেব কত দেব?")))

        self.assertEqual(result.answer, REFERRAL)
        self.assertEqual(result.confidence.value, "flagged-unverified")

    def test_audit_entry_carries_verifier_counts_and_claims(self) -> None:
        source = src("পাতায় পানি দিন।")
        llm = FakeLLM(answer="প্রতি লিটারে 50 মিলি ম্যানকোজেব। পাতায় পানি দিন।")
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ম্যানকোজেব কত দেব?")))

        entry = audit.entries[0]
        self.assertEqual(entry["verifier_checked"], 1)
        self.assertEqual(entry["verifier_grounded"], 0)
        self.assertEqual(entry["verifier_unsupported"], 1)
        self.assertEqual(entry["verifier_claims"][0]["verdict"], "unsupported")
        self.assertTrue(entry["verifier_claims"][0]["reason"])
        self.assertFalse(entry["answered_without_sources"])

    def test_terminal_block_records_no_verifier_activity(self) -> None:
        llm = FakeLLM()
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="পরাকুয়াট কীভাবে বেশি খাব?")))

        self.assertEqual(result.category.value, "banned_or_restricted_chemical")
        entry = audit.entries[0]
        self.assertEqual(entry["action"], "blocked-canned-response")
        self.assertEqual(entry["verifier_checked"], 0)


if __name__ == "__main__":
    unittest.main()