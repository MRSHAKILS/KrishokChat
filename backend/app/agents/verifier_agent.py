"""Verifier Agent — checks groundedness and flags unverified claims."""
from __future__ import annotations

import re

_DOSAGE_RE = re.compile(r"\d+\s*(ml|gm|g|kg|l|liter|মিলি|গ্রাম|কেজি|লিটার|টেবিল চামচ|কাপ)", re.I)


def verify(answer: str, sources: list[dict]) -> dict:
    flags = []
    flagged_unverified = []

    source_text = " ".join(
        (s.get("content_bn", "") + " " + s.get("content_en", "")) for s in sources
    ).lower()

    # Flag dosages not found in sources
    for m in _DOSAGE_RE.finditer(answer):
        token = m.group(0).lower().strip()
        if token not in source_text:
            flagged_unverified.append(token)

    if flagged_unverified:
        flags.append(f"Unverified dosages: {flagged_unverified}")

    # Groundedness: overlap of answer tokens with source tokens
    ans_tokens = set(answer.lower().split())
    src_tokens = set(source_text.split())
    if ans_tokens:
        overlap = len(ans_tokens & src_tokens) / len(ans_tokens)
        if overlap < 0.3:
            flags.append(f"Low groundedness ({overlap:.0%} token overlap)")

    confidence = "verified" if not flags else "flagged-unverified"
    return {"confidence": confidence, "flags": flags, "flagged_unverified": flagged_unverified}
