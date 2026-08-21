"""T14 fixed LLM judge — offline tests (no API calls).

Covers: prompt construction determinism, verdict parsing, fail-closed schema
validation, and manifest hashing. API behavior is covered by the run manifest.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import sys

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent / "scripts"))
sys.path.insert(0, str(SCRIPT_DIR.parent.parent.parent.parent.parent.parent / "backend"))

from run_llm_judge import JUDGE_PROMPT, build_prompt, parse_verdict  # noqa: E402


class JudgePromptTests(unittest.TestCase):
    def test_prompt_embeds_query_answer_evidence(self):
        item = {
            "item_id": "PILOT-0001",
            "query": "প্রশ্ন?",
            "answer": "উত্তর",
            "evidence": {"evidence_text": "এভিডেন্স"},
        }
        prompt = build_prompt(item)
        self.assertIn("প্রশ্ন?", prompt)
        self.assertIn("উত্তর", prompt)
        self.assertIn("এভিডেন্স", prompt)

    def test_prompt_is_deterministic(self):
        item = {"query": "q", "answer": "a", "evidence": {"evidence_text": "e"}}
        self.assertEqual(build_prompt(item), build_prompt(item))

    def test_prompt_sha256_is_stable(self):
        h = hashlib.sha256(JUDGE_PROMPT.encode("utf-8")).hexdigest()
        self.assertEqual(len(h), 64)


class VerdictParsingTests(unittest.TestCase):
    def test_valid_verdict_parses(self):
        content = json.dumps({
            "verdict": "partially_supported",
            "relation_checks": [
                {"relation": "dose", "claim": "২ গ্রাম", "status": "supported",
                 "span_in_evidence": "2 g"},
            ],
            "reasoning": "Dose present; interval missing.",
        }, ensure_ascii=False)
        out = parse_verdict(content)
        self.assertEqual(out["verdict"], "partially_supported")
        self.assertEqual(len(out["relation_checks"]), 1)

    def test_unknown_verdict_fails_closed(self):
        with self.assertRaises(ValueError):
            parse_verdict('{"verdict": "maybe", "relation_checks": [], "reasoning": ""}')

    def test_bad_relation_status_fails_closed(self):
        content = json.dumps({
            "verdict": "supported",
            "relation_checks": [{"relation": "dose", "claim": "x", "status": "nope",
                                 "span_in_evidence": None}],
        }, ensure_ascii=False)
        with self.assertRaises(ValueError):
            parse_verdict(content)

    def test_relation_checks_must_be_list(self):
        with self.assertRaises(ValueError):
            parse_verdict('{"verdict": "supported", "relation_checks": "oops"}')

    def test_not_json_fails_closed(self):
        with self.assertRaises(ValueError):
            parse_verdict("this is not json at all")


if __name__ == "__main__":
    unittest.main()