"""T16 normalization harness acceptance tests (unittest).

Covers the four spec-row acceptance criteria:
  1. slot/polarity preservation        (unicode + dictionary passes)
  2. unknown-term no-op                (dictionary pass)
  3. low-confidence raw fallback       (dictionary pass confidence gate)
  4. same-BM25 assertion               (stub and real index)

Plus edit-trace format and the deterministic no-learned-work property.
Fixtures are synthetic; no frozen test data is accessed (AGENTS.md rule 15).

NOTE (2026-08-13): converted from pytest to unittest to match the repo's
research-test convention — pytest is not installed in the backend venv and
adding it would be an unnecessary dependency. Integration test now reuses
the harness's own BACKEND/CORPUS_PATH constants instead of hard-coded
path traversal.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT / "scripts"))

from run_normalization_harness import (  # noqa: E402
    BACKEND,
    BENGALI_DIGITS,
    CORPUS_PATH,
    INDEX_PATH,
    dictionary_pass,
    diff_trace,
    flip_kind,
    passes_of,
    unicode_pass,
)

# --------------------------------------------------------------------------- #
# Slot/polarity preservation
# --------------------------------------------------------------------------- #
SLOT_SENTENCE = (
    "ঢলে পোড়া রোগে প্রতি শতকে ২ লিটার ভিটাভ্যাক্স-২০০ মিশানো পানি ৭ দিনে "
    "১ বার ছিটান, কৃষি কর্মকর্তার পরামর্শ ছাড়া ব্যবহার করবেন না।"
)


class TestUnicodePass(unittest.TestCase):
    def test_preserves_slots_and_polarity(self):
        out, edits = unicode_pass(SLOT_SENTENCE)
        # amount/unit/denominator/interval values survive; Bengali digits are
        # mapped to ASCII per the unicode-pass spec (canonical comparison form).
        assert "লিটার" in out and "ভিটাভ্যাক্স-200" in out and "শতক" in out
        assert "দিনে" in out and "বার" in out and "কৃষি কর্মকর্তা" in out
        assert "2" in out and "7" in out and "1" in out  # digits mapped, not lost
        assert "করবেন না" in out  # polarity marker survives
        assert edits, "expected edit trace for digit mapping"

    def test_slot_tokens_never_removed(self):
        out, _ = unicode_pass(SLOT_SENTENCE)
        for tok in ("লিটার", "ভিটাভ্যাক্স", "শতক", "কৃষি কর্মকর্তা", "না"):
            assert tok in out

    def test_digit_mapping_count_preserved(self):
        out, _ = unicode_pass("২২ মিলি এবং ৩ কেজি")
        assert out == "22 মিলি এবং 3 কেজি"

    def test_is_deterministic_and_nfc(self):
        src = "\u09a7\u09be\u09a8"  # already-NFC ধান
        out1, _ = unicode_pass(src)
        out2, _ = unicode_pass(src)
        assert out1 == out2
        # ZWJ/ZWNJ removed
        assert "\u200d" not in unicode_pass("কৃষি\u200dসেবা")[0]
        assert "\u200c" not in unicode_pass("কৃষি\u200cসেবা")[0]

    def test_edit_trace_format(self):
        out, edits = unicode_pass("২ লিটার")
        for e in edits:
            assert set(e) == {"pass", "operation", "from_start", "from_end",
                              "from_text", "to_text", "record_id"}
            assert e["pass"] == "unicode"
            assert e["operation"] in ("replace", "delete", "insert")
            assert isinstance(e["from_start"], int) and isinstance(e["from_end"], int)
        assert edits, "digit mapping must produce edits"
        assert all(e["from_text"] != e["to_text"]
                   for e in edits if e["operation"] == "replace")


class TestDictionaryPass(unittest.TestCase):
    def test_preserves_slots_and_polarity(self):
        records = [
            {"id": "D1", "surface": "ঢলে পোড়া", "target": "শীথ ব্লাইট",
             "confidence": 0.95, "source_records": ["fixture"]},
            {"id": "D2", "surface": "ছিটান", "target": "প্রয়োগ করুন",
             "confidence": 0.99, "source_records": ["fixture"]},
        ]
        out, edits, fallback = dictionary_pass(
            "ঢলে পোড়া রোগে প্রতি শতকে ২ লিটার ছিটান, ব্যবহার করবেন না।",
            records, 0.8)
        assert fallback == ""
        assert "শীথ ব্লাইট" in out and "প্রয়োগ করুন" in out
        assert "লিটার" in out and "শতক" in out and "করবেন না" in out  # slots + polarity
        assert len(edits) == 2
        assert {e["record_id"] for e in edits} == {"D1", "D2"}

    def test_unknown_terms_are_noops(self):
        records = [{"id": "X", "surface": "ঠ্যাংরা", "target": "শীথ ব্লাইট",
                    "confidence": 0.9, "source_records": ["fixture"]}]
        text = "ধান গাছে রোগ দেখা দিলে ২ লিটার ভিটাভ্যাক্স-২০০ ছিটান।"  # no dict surface
        out, edits, fallback = dictionary_pass(text, records, 0.8)
        assert out == text
        assert edits == []
        assert fallback == ""

    def test_empty_records_is_pure_noop(self):
        text = "যেকোনো পাঠ্য ১২৩ এবং বাংলা ১২৩"
        out, edits, fallback = dictionary_pass(text, [], 0.8)
        assert out == text and edits == [] and fallback == ""
        # the dictionary pass from passes_of must also be a pure no-op
        # (the unicode pass legitimately maps Bengali digits to ASCII —
        # that is independent of the dictionary and checked elsewhere)
        for pass_name, pass_text, pass_edits, pass_fb in passes_of(text, [], 0.8):
            if pass_name == "dictionary":
                assert pass_text == text and pass_edits == [] and pass_fb == ""

    def test_no_invented_mapping(self):
        records = [{"id": "Y", "surface": "মাটি", "target": "জমি", "confidence": 0.9,
                    "source_records": ["fixture"]}]
        text = "মাটির গুণাগুণ ভালো"  # "মাটি" is a PREFIX, not a whole token match
        out, edits, _ = dictionary_pass(text, records, 0.8)
        assert "জমি" not in out  # substring prefix must not be replaced
        assert out == text and edits == []

    def test_low_confidence_record_triggers_raw_fallback(self):
        records = [{"id": "L", "surface": "ঢলে পোড়া", "target": "শীথ ব্লাইট",
                    "confidence": 0.4, "source_records": ["fixture"]}]
        text = "ঢলে পোড়া রোগে ২ লিটার ছিটান"
        out, edits, fallback = dictionary_pass(text, records, 0.8)
        assert fallback == "raw"
        assert out == text  # raw text returned verbatim
        assert edits == []  # suppressed edits

    def test_confidence_at_or_above_gate_is_applied(self):
        records = [{"id": "G", "surface": "ঢলে পোড়া", "target": "শীথ ব্লাইট",
                    "confidence": 0.8, "source_records": ["fixture"]}]
        out, edits, fallback = dictionary_pass("ঢলে পোড়া রোগ", records, 0.8)
        assert fallback == "" and "শীথ ব্লাইট" in out and len(edits) == 1


class StubRetriever:
    """Records call history; returns fake top-k objects matching BM25Retriever
    result shape (id/score attributes, not dicts)."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, list[dict]]] = []

    def retrieve(self, query: str, *, top_k: int = 10) -> list:
        from types import SimpleNamespace

        self.calls.append((query, []))
        return [SimpleNamespace(id="doc0", score=1.0),
                SimpleNamespace(id="doc1", score=0.5)]


class TestSameBM25Assertion(unittest.TestCase):
    def test_unchanged_query_calls_once(self):
        """An unchanged query must hit the retriever a single time (raw pass only).
        Exercises the real harness dedup path: unicode + dictionary passes that
        leave text untouched reuse the raw ranking instead of re-querying."""
        import argparse

        from run_normalization_harness import StructuredVerifier, emit_pair_side

        stub = StubRetriever()
        pair = {"pair_id": "S1", "intent_id": "stub", "variety": "stub",
                "standard": "no changes here", "variant": "no changes here",
                "polarity": "affirm", "slots": {}}
        args = argparse.Namespace(safety="none", retrieve="index",
                                  confidence_gate=0.8)
        run_records, ranking_records, failures = [], [], []
        raw_rank_cache: dict = {}
        pass_counts: dict = {}
        safety_flips: dict = {}
        assertions = {"checked": 0, "violated": 0}

        emit_pair_side(pair, "standard", pair["standard"], [], args, stub,
                       StructuredVerifier(), run_records, ranking_records,
                       failures, raw_rank_cache, pass_counts, safety_flips,
                       assertions)

        # raw pass is the ONLY retrieval; unicode + dictionary passes reuse it
        assert len(stub.calls) == 1
        assert assertions["checked"] == 2   # unicode + dictionary dedup
        assert assertions["violated"] == 0
        assert failures == []
        # reused passes carry the same top-k as the raw pass
        raw_top = [r["top_k"] for r in ranking_records if r["pass"] == "raw"][0]
        for r in ranking_records:
            if r["pass"] != "raw":
                assert r["reused_raw"] is True
                assert r["top_k"] == raw_top

    @unittest.skipUnless(INDEX_PATH.exists(), "precomputed BM25 index not present")
    def test_real_index_unchanged_pass(self):
        """Integration: with the real precomputed index, an unchangeable query
        yields identical top-k on first and second retrieval (determinism of
        the assertion). Uses the runtime corpus path (knowledge_nodes_clean.jsonl)."""
        sys.path.insert(0, str(BACKEND))
        from app.infrastructure.retrieval.bm25 import BM25Retriever

        retriever = BM25Retriever(INDEX_PATH, CORPUS_PATH)
        q = "rice disease"
        first = retriever.retrieve(q, top_k=10)
        second = retriever.retrieve(q, top_k=10)
        ids1 = [r.id for r in first]
        ids2 = [r.id for r in second]
        assert ids1 == ids2
        assert ids1, "real index returned nothing for a known agro-query"


class TestMisc(unittest.TestCase):
    def test_flip_kind_labels(self):
        assert flip_kind(None, None) == "none"
        assert flip_kind({"category": "B"}, None) == "harmful_to_benign"
        assert flip_kind(None, {"category": "B"}) == "benign_to_harmful"
        assert flip_kind({"category": "A"}, {"category": "B"}) == "different_category"
        assert flip_kind({"category": "A"}, {"category": "A"}) == "same_category"

    def test_BENGALI_DIGITS_table_complete(self):
        assert BENGALI_DIGITS is not None
        assert "০১২৩৪৫৬৭৮৯".translate(BENGALI_DIGITS) == "0123456789"


if __name__ == "__main__":
    unittest.main()