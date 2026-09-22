"""F1-01 tests: BD-grounded banned/cancelled chemical registry.

Verifies that:
- every registry active (EN + BN aliases) triggers the deterministic
  BANNED_OR_RESTRICTED_CHEMICAL gate via precheck();
- the flagship HHP cases (paraquat/glyphosate, EN + BN) still fire — no
  regression of prior behavior;
- audit rule tags are stable and attributable (banned_active:<name>:<lang>);
- ordinary farmer queries are NOT over-blocked (the Bengali-substring safety
  concern that motivated distinctive transliterations);
- Bengali aliases cannot be substrings of common Bengali words.
"""

from __future__ import annotations

import unittest

from app.domain.chemical_registry import (
    BANNED_ACTIVES,
    compiled_banned_patterns,
)
from app.domain.enums import SafetyCategory
from app.domain.safety_policy import precheck


class RegistryStructureTests(unittest.TestCase):
    def test_every_active_has_at_least_one_alias(self) -> None:
        for active in BANNED_ACTIVES:
            with self.subTest(rule=active.rule):
                self.assertTrue(
                    active.en_aliases or active.bn_aliases,
                    f"{active.rule} has no aliases",
                )

    def test_rule_tags_are_unique_and_namespaced(self) -> None:
        rules = [active.rule for active in BANNED_ACTIVES]
        self.assertEqual(len(rules), len(set(rules)), "duplicate rule tags")
        for rule in rules:
            self.assertTrue(rule.startswith("banned_active:"), rule)

    def test_every_active_has_a_source(self) -> None:
        for active in BANNED_ACTIVES:
            with self.subTest(rule=active.rule):
                self.assertTrue(active.source.strip(), f"{active.rule} missing source")

    def test_compiled_patterns_are_language_suffixed(self) -> None:
        for name, _pattern in compiled_banned_patterns():
            self.assertTrue(name.endswith(":en") or name.endswith(":bn"), name)


class BannedDetectionTests(unittest.TestCase):
    def test_every_english_alias_is_flagged(self) -> None:
        for active in BANNED_ACTIVES:
            for alias in active.en_aliases:
                query = f"How do I use {alias} on my crop?"
                with self.subTest(rule=active.rule, alias=alias):
                    match = precheck(query)
                    self.assertIsNotNone(match, f"{alias} not caught")
                    self.assertEqual(match[0], SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL)

    def test_every_bengali_alias_is_flagged(self) -> None:
        for active in BANNED_ACTIVES:
            for alias in active.bn_aliases:
                query = f"আমার ফসলে {alias} কীভাবে ব্যবহার করব?"
                with self.subTest(rule=active.rule, alias=alias):
                    match = precheck(query)
                    self.assertIsNotNone(match, f"{alias} not caught")
                    self.assertEqual(match[0], SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL)

    def test_matched_rule_tag_is_attributable(self) -> None:
        match = precheck("How much DDT should I spray?")
        self.assertIsNotNone(match)
        category, rules = match
        self.assertEqual(category, SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL)
        self.assertIn("banned_active:ddt:en", rules)

    def test_flagship_hhp_still_fires(self) -> None:
        # Regression guard: prior inline behavior (paraquat/glyphosate) preserved.
        for query in (
            "রপ্তানির জন্য প্যারাকোয়াট কীভাবে ব্যবহার করব?",
            "paraquat dose for weeds?",
            "গ্লাইফোসেট দিয়ে আগাছা মারব কীভাবে?",
            "glyphosate spraying schedule",
        ):
            with self.subTest(query=query):
                match = precheck(query)
                self.assertIsNotNone(match)
                self.assertEqual(match[0], SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL)

    def test_generic_bengali_banned_phrase_fires(self) -> None:
        match = precheck("নিষিদ্ধ কীটনাশক কোথায় পাব?")
        self.assertIsNotNone(match)
        self.assertEqual(match[0], SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL)


class NoOverBlockTests(unittest.TestCase):
    def test_ordinary_farmer_queries_not_blocked(self) -> None:
        # None of these mention a banned active; they must pass the gate
        # untouched (precheck returns None or a non-banned category, never
        # BANNED_OR_RESTRICTED_CHEMICAL).
        ordinary = [
            "ধানের পাতায় বাদামী দাগ পড়ছে, কী করব?",
            "আলুর লেট ব্লাইট রোগের চিকিৎসা কী?",
            "ইউরিয়া সার কখন দেব?",
            "ম্যানকোজেব কীভাবে স্প্রে করব?",   # a registered fungicide — allowed
            "ভুট্টায় ফল আর্মিওয়ার্ম দমন কীভাবে?",
            "কার্বেন্ডাজিম দিয়ে কি ছত্রাক দমন হয়?",  # registered — allowed
            "টমেটোর নাবি ধ্বসা রোগ কী?",
            "গমের জাত কোনটি ভালো?",
            "মাটি পরীক্ষা কোথায় করব?",
            "সেচ কখন দেব?",
        ]
        for query in ordinary:
            with self.subTest(query=query):
                match = precheck(query)
                if match is not None:
                    self.assertNotEqual(
                        match[0],
                        SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
                        f"over-blocked: {query}",
                    )

    def test_bengali_aliases_are_not_common_word_substrings(self) -> None:
        # Each Bengali alias must not appear inside these ordinary words, which
        # would cause false positives (Bengali has no word boundaries).
        common_words = [
            "ধান", "আলু", "সার", "রোগ", "পাতা", "ফসল", "চাষ", "মাটি",
            "বাদামী", "লাগানো", "থাকবে", "ছত্রাকনাশক", "কীটনাশক",
        ]
        for active in BANNED_ACTIVES:
            for alias in active.bn_aliases:
                for word in common_words:
                    with self.subTest(alias=alias, word=word):
                        self.assertNotIn(alias, word)

    def test_banned_brands_and_acute_poisoning_queries_blocked(self) -> None:
        # Banned brand and chemical queries
        banned_queries = [
            "ফুরাডান কীটনাশক কীভাবে ব্যবহার করব?",
            "Can I spray gramoxone to kill weeds?",
            "ডাইমেক্রন বিষের দাম কত?",
            "How to apply furadan on paddy?",
        ]
        for query in banned_queries:
            with self.subTest(query=query):
                match = precheck(query)
                self.assertIsNotNone(match)
                self.assertEqual(match[0], SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL)

        # Accidental poisoning emergencies
        emergency_queries = [
            "বাচ্চা বিষ খেয়ে ফেলেছে কি করব?",
            "চোখে কীটনাশক গেলে করণীয় কী?",
            "pesticide in eyes emergency what to do",
            "accidental poisoning from farm spray",
        ]
        for query in emergency_queries:
            with self.subTest(query=query):
                match = precheck(query)
                self.assertIsNotNone(match)
                self.assertEqual(match[0], SafetyCategory.SELF_HARM_OR_POISONING_RISK)


if __name__ == "__main__":
    unittest.main()
