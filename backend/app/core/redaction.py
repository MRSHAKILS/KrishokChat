"""PII redaction — best-effort, regex-based, local-only.

Covers Bangladeshi mobile numbers (+880 / 01 variants including Bengali digits
০-৯), email addresses, and name-adjacent patterns. Applied at write time to
stored audit query text when ``PII_REDACTION_ENABLED=true``. Stored-text only —
the user-visible answer is never altered.

Best-effort: regex cannot be perfect. Documented as such; never claim perfect
redaction.
"""

from __future__ import annotations

import re

# Bangladeshi mobile: 11 digits starting 01[3-9], optionally prefixed by +880 / 880
# (including Bengali ৮৮০) and optionally spaced/hyphenated. Bengali digits ০-৯
# supported throughout. The pattern allows separators between any digit so
# "01711-111111" and "০১৭ ১১১ ১১১ ১১১" both match.
# Examples: 01711111111, +8801711111111, 01711-111111, ০১৭১১১১১১১১১, +৮৮০১৭১১১১১১১১১
PHONE_RE = re.compile(
    r"(?:\+?(?:880|৮৮০)[\s\-\.]*)?[0০]?[\s\-\.]*[1১][\s\-\.]*[3-9৩-৯](?:[\s\-\.]*[0-9০-৯]){8}"
)

# Simple email — covers farmed test cases, not RFC-perfect.
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# Name-adjacent: "name: X" / "নাম: X" — redact the value after the label.
# Keep the label, replace the value with [REDACTED]. Case-insensitive for EN.
NAME_EN_RE = re.compile(r"(name\s*[:：]\s*)([^\n,;]+)", re.IGNORECASE)
NAME_BN_RE = re.compile(r"(নাম\s*[:：]\s*)([^\n,;]+)")

# Generic phone label redaction is covered by PHONE_RE already; this handles
# "phone: 017..." style where the label is explicit but number is still the same.

_REDACTED_PHONE = "[REDACTED_PHONE]"
_REDACTED_EMAIL = "[REDACTED_EMAIL]"
_REDACTED_NAME = "[REDACTED]"


def redact_phone(text: str) -> str:
    return PHONE_RE.sub(_REDACTED_PHONE, text)


def redact_email(text: str) -> str:
    return EMAIL_RE.sub(_REDACTED_EMAIL, text)


def redact_name(text: str) -> str:
    # Apply Bengali first, then English (order does not matter, both labels kept).
    text = NAME_BN_RE.sub(rf"\g<1>{_REDACTED_NAME}", text)
    text = NAME_EN_RE.sub(rf"\g<1>{_REDACTED_NAME}", text)
    return text


def redact_pii(text: str) -> str:
    """Best-effort PII redaction for stored audit text.

    Applies phone, email, and name-adjacent patterns. Order matters only to
    avoid double-substitution side effects; phone/email are independent.
    """
    if not text:
        return text
    out = text
    out = redact_phone(out)
    out = redact_email(out)
    out = redact_name(out)
    return out
