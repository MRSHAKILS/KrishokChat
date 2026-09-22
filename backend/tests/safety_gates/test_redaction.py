"""T1-04: PII redaction — best-effort regex tests.

Covers Bangladeshi phone (01 / +880, Bengali digits ০-৯), email, name-adjacent
patterns. Verifies stored audit query text is scrubbed while the pipeline's
user-visible answer path is untouched (tested at integration level elsewhere).
"""

from __future__ import annotations

import unittest

from app.core.redaction import redact_email, redact_name, redact_phone, redact_pii


class PhoneRedactionTests(unittest.TestCase):
    def test_ascii_11_digit(self) -> None:
        self.assertEqual(redact_phone("call 01711111111 please"), "call [REDACTED_PHONE] please")
        self.assertEqual(redact_phone("01712-345678"), "[REDACTED_PHONE]")
        self.assertEqual(redact_phone("01712 345 678"), "[REDACTED_PHONE]")

    def test_plus_880(self) -> None:
        self.assertEqual(redact_phone("+8801711111111"), "[REDACTED_PHONE]")
        self.assertEqual(redact_phone("+880 1711111111"), "[REDACTED_PHONE]")
        self.assertEqual(redact_phone("8801711111111"), "[REDACTED_PHONE]")

    def test_bengali_digits(self) -> None:
        # ০১৭১১১১১১১১১ is the Bengali-digit form of 01711111111
        self.assertIn("[REDACTED_PHONE]", redact_phone("আমার নম্বর ০১৭১১১১১১১১১ কল করুন"))
        self.assertIn("[REDACTED_PHONE]", redact_phone("০১৭১২৩৪৫৬৭৮"))
        self.assertIn("[REDACTED_PHONE]", redact_phone("+৮৮০১৭১১১১১১১১১"))
        # Mixed Bengali/ASCII with separators
        self.assertIn("[REDACTED_PHONE]", redact_phone("০১৭১১-১১১১১১"))

    def test_non_phone_numbers_untouched(self) -> None:
        # Short numbers, landlines, or non-mobile prefixes should ideally not match;
        # but 01-based 11-digit is the contract — plain 1000 stays.
        self.assertEqual(redact_phone("ধান ১০০০ কেজি"), "ধান ১০০০ কেজি")
        self.assertEqual(redact_phone("price 500 taka"), "price 500 taka")


class EmailRedactionTests(unittest.TestCase):
    def test_simple_email(self) -> None:
        self.assertEqual(redact_email("contact me at foo@example.com"), "contact me at [REDACTED_EMAIL]")
        self.assertEqual(redact_email("a.b+tag@bari.gov.bd"), "[REDACTED_EMAIL]")

    def test_multiple(self) -> None:
        self.assertEqual(redact_email("a@b.com and c@d.org"), "[REDACTED_EMAIL] and [REDACTED_EMAIL]")

    def test_non_email_untouched(self) -> None:
        self.assertEqual(redact_email("hello @ world"), "hello @ world")
        self.assertEqual(redact_email("ধান @ মাঠ"), "ধান @ মাঠ")


class NameRedactionTests(unittest.TestCase):
    def test_bengali_name_label(self) -> None:
        self.assertEqual(redact_name("নাম: করিম"), "নাম: [REDACTED]")
        self.assertEqual(redact_name("নাম： রহিম উদ্দিন, ধান"), "নাম： [REDACTED], ধান")

    def test_english_name_label(self) -> None:
        self.assertEqual(redact_name("name: Rahim"), "name: [REDACTED]")
        self.assertEqual(redact_name("Name: Karim Hossain, query"), "Name: [REDACTED], query")
        self.assertEqual(redact_name("NAME: Test"), "NAME: [REDACTED]")

    def test_no_label_untouched(self) -> None:
        # Standalone names without label are NOT redacted (best-effort allow-list).
        self.assertEqual(redact_name("আমি করিম, ধান চাষ করি"), "আমি করিম, ধান চাষ করি")


class CombinedRedactionTests(unittest.TestCase):
    def test_all_patterns_together(self) -> None:
        raw = "নাম: করিম, phone 01711111111, email karim@example.com, +8801711111111"
        redacted = redact_pii(raw)
        self.assertIn("[REDACTED]", redacted)
        self.assertIn("[REDACTED_PHONE]", redacted)
        self.assertIn("[REDACTED_EMAIL]", redacted)
        self.assertNotIn("01711111111", redacted)
        self.assertNotIn("karim@example.com", redacted)

    def test_bengali_digits_and_email(self) -> None:
        raw = "আমার নাম: রহিম, নম্বর ০১৭১১১১১১১১১, ইমেইল test@bari.gov.bd"
        redacted = redact_pii(raw)
        self.assertNotIn("০১৭১১১১১১১১১", redacted)
        self.assertNotIn("test@bari.gov.bd", redacted)
        self.assertIn("[REDACTED_PHONE]", redacted)
        self.assertIn("[REDACTED_EMAIL]", redacted)

    def test_empty_and_none_safe(self) -> None:
        self.assertEqual(redact_pii(""), "")
        self.assertEqual(redact_pii("no pii here"), "no pii here")

    def test_idempotent(self) -> None:
        raw = "01711111111"
        once = redact_pii(raw)
        twice = redact_pii(once)
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
