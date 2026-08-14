"""P4 D1a corpus-coverage gate tests (deterministic low_confidence refusal).

The gate refuses intents the advisory corpus cannot support (training venues,
export procedures, vendor/seedling availability, institutional requests,
livestock, government assistance). Rule set was derived from the 46-item
golden set: it must catch all 12 unanswerable + 2 off_topic items, never
touch the 34 answerable items, and never regress safety priority.
"""

from __future__ import annotations

import asyncio
import json
import unittest
from pathlib import Path

from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.safety import SafetyClassifier
from app.domain.contracts import RetrievedSource
from app.domain.safety_policy import canned_response, precheck
from app.domain.enums import SafetyCategory
from app.infrastructure.verification.dosage import DosageVerifier

from tests.test_pipeline import FakeAudit, FakeLLM, FakeRetriever, FakeSessions

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GOLDEN = REPO_ROOT / "dataset_release" / "benchmark" / "golden_qa_v1.jsonl"

UNANSWERABLE = {"unanswerable", "off_topic"}


def golden_rows() -> list[dict]:
    return [json.loads(line) for line in GOLDEN.read_text(encoding="utf-8").splitlines() if line.strip()]


def make_pipeline(llm: FakeLLM, retriever: FakeRetriever, audit: FakeAudit) -> QAPipeline:
    return QAPipeline(
        safety=SafetyClassifier(llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(llm),
        verifier=DosageVerifier(),
        audit=audit,
        sessions=FakeSessions(),
        top_k=5,
    )


class CoverageGateTests(unittest.TestCase):
    """Every out-of-corpus golden item must be refused deterministically."""

    def test_all_12_unanswerable_golden_items_refused(self) -> None:
        rows = [r for r in golden_rows() if r["golden_category"] == "unanswerable"]
        self.assertEqual(len(rows), 12)
        for row in rows:
            with self.subTest(row=row["row_id"]):
                match = precheck(row["question"])
                self.assertIsNotNone(match, f"{row['row_id']} not caught by gate")
                self.assertEqual(match[0], SafetyCategory.LOW_CONFIDENCE)

    def test_both_off_topic_golden_items_refused(self) -> None:
        rows = [r for r in golden_rows() if r["golden_category"] == "off_topic"]
        self.assertEqual(len(rows), 2)
        for row in rows:
            with self.subTest(row=row["row_id"]):
                match = precheck(row["question"])
                self.assertIsNotNone(match)
                self.assertEqual(match[0], SafetyCategory.LOW_CONFIDENCE)

    def test_no_answerable_golden_item_touched(self) -> None:
        rows = [r for r in golden_rows() if r["golden_category"] not in UNANSWERABLE]
        self.assertEqual(len(rows), 32)  # dosage 10 + timing 10 + pest 10 + general 2
        for row in rows:
            with self.subTest(row=row["row_id"]):
                self.assertIsNone(precheck(row["question"]))

    def test_gate_stops_before_llm_and_retrieval_with_canned_referral(self) -> None:
        row = next(r for r in golden_rows() if r["golden_category"] == "unanswerable")
        llm = FakeLLM()
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query=row["question"])))

        self.assertEqual(result.category.value, "low_confidence")
        self.assertEqual(result.confidence.value, "blocked")
        self.assertEqual(llm.classify_calls, 0)
        self.assertEqual(retriever.calls, 0)
        self.assertIn("১৬১২৩", result.answer)
        self.assertIn("জ্ঞানভান্ডারে নেই", result.answer)
        self.assertEqual(len(audit.entries), 1)
        entry = audit.entries[0]
        self.assertEqual(entry["action"], "blocked-canned-response")
        self.assertEqual(entry["category"], "low_confidence")
        self.assertTrue(entry["safety_matched_rules"])

    def test_farmer_typo_training_variant_caught(self) -> None:
        # "প্রশিক্ষন" without ষ — real spelling seen in the farmer pool.
        self.assertEqual(precheck("ফল চাষের প্রশিক্ষন কোথায় পাব?")[0], SafetyCategory.LOW_CONFIDENCE)

    def test_banglish_livestock_caught(self) -> None:
        self.assertEqual(precheck("Ami koel palon a agrohi.")[0], SafetyCategory.LOW_CONFIDENCE)

    def test_bengali_substring_traps_do_not_fire(self) -> None:
        # "বাদামী" contains "দাম"; "থাকবে" contains "কবে"; "লাগানো" contains
        # "গান" — these must never be gated (evidence-based rule design).
        for query in (
            "ধানের পাতায় বাদামী দাগ পড়ছে, কী করব?",   # brown spots — answerable
            "ধান কবে লাগাব?",
            "কীটনাশক কখন লাগানো উচিত?",
        ):
            with self.subTest(query=query):
                self.assertIsNone(precheck(query))

    def test_price_rule_absent(self) -> None:
        # Market-price queries are NOT gated: no evidence in the golden set,
        # and "দাম" is a substring of "বাদামী". Deliberately out of scope.
        self.assertIsNone(precheck("পটলের দাম কত?"))

    def test_safety_priority_over_coverage(self) -> None:
        # A banned-chemical mention must win over a coverage keyword even
        # when both match ("রপ্তানি" + "প্যারাকোয়াট").
        match = precheck("রপ্তানির জন্য প্যারাকোয়াট কীভাবে ব্যবহার করব?")
        self.assertEqual(match[0], SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL)
        self.assertNotEqual(canned_response(match[0]), canned_response(SafetyCategory.LOW_CONFIDENCE))


if __name__ == "__main__":
    unittest.main()