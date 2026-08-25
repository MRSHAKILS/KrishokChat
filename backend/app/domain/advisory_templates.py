"""R4 — Bengali advisory template functions for T1/T2 structured answers.

Pure string composition from a ``Fact`` — no I/O, no LLM, no network.

Two templates:
  T1 (structured_fact)   — dose + interval + PHI only (direct, minimal)
  T2 (templated_advisory) — fuller advisory: dose + interval + PHI + IPM
                             alternatives + calendar-stage note

Both keep dose numbers verbatim from the fact row (never round or rephrase).
The tone follows the canned safety responses and P2 stage advisory strings.
"""

from __future__ import annotations

from app.domain.fact_base import Fact


# ---------------------------------------------------------------------------
# Severity labels
# ---------------------------------------------------------------------------

_SEVERITY_BN: dict[str, str] = {
    "high":   "অত্যন্ত ক্ষতিকর",
    "medium": "মাঝারি ক্ষতিকর",
    "low":    "কম ক্ষতিকর",
}

# ---------------------------------------------------------------------------
# T1 — structured_fact template (minimal, cite-only)
# ---------------------------------------------------------------------------


def render_t1(fact: Fact) -> str:
    """Render a T1 (structured_fact) Bengali advisory from a single Fact row.

    Format: crop problem → recommended dose + application interval + PHI.
    Numbers are verbatim from the fact row.
    """
    dose = _dose_str(fact)
    parts = [
        f"**{fact.crop_bn or fact.crop} — {fact.problem_bn or fact.problem}**",
        "",
        f"অনুমোদিত বালাইনাশক: **{fact.active_ingredient}**",
        f"প্রস্তাবিত মাত্রা: {dose}",
        f"প্রয়োগের ব্যবধান: প্রতি {fact.application_interval_days} দিনে একবার স্প্রে করুন।",
    ]
    if fact.pre_harvest_interval_days:
        parts.append(
            f"ফসল সংগ্রহের কমপক্ষে {fact.pre_harvest_interval_days} দিন আগে স্প্রে বন্ধ করুন।"
        )
    parts += [
        "",
        f"*সূত্র: {fact.citation or fact.source_doc}*",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# T2 — templated_advisory template (fuller advisory)
# ---------------------------------------------------------------------------


def render_t2(fact: Fact, stage_advisory_bn: str | None = None) -> str:
    """Render a T2 (templated_advisory) Bengali advisory from a Fact row.

    Includes IPM alternatives and an optional calendar-stage advisory note
    (from the crop_calendars artifact, passed in by the resolver).
    """
    dose = _dose_str(fact)
    severity = _SEVERITY_BN.get(fact.severity, "")

    parts = [
        f"**{fact.crop_bn or fact.crop} — {fact.problem_bn or fact.problem}**",
    ]
    if severity:
        parts.append(f"রোগের তীব্রতা: {severity}")
    parts += [
        "",
        "### প্রতিকার (বালাইনাশক)",
        f"অনুমোদিত বালাইনাশক: **{fact.active_ingredient}**",
        f"প্রস্তাবিত মাত্রা: {dose}",
        f"প্রতি {fact.application_interval_days} দিন পর পর স্প্রে করুন।",
    ]
    if fact.pre_harvest_interval_days:
        parts.append(
            f"ফসল সংগ্রহের **{fact.pre_harvest_interval_days} দিন আগে** স্প্রে সম্পূর্ণ বন্ধ করুন।"
        )

    if fact.ipm_alternatives_bn:
        parts += [
            "",
            "### সমন্বিত বালাই ব্যবস্থাপনা (IPM)",
        ]
        for alt in fact.ipm_alternatives_bn:
            parts.append(f"- {alt}")

    if stage_advisory_bn:
        parts += [
            "",
            "### বর্তমান পর্যায়ের পরামর্শ",
            stage_advisory_bn,
        ]

    parts += [
        "",
        f"*সূত্র: {fact.citation or fact.source_doc}*",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _dose_str(fact: Fact) -> str:
    """Format the dose range as a Bengali-readable string."""
    if fact.dose_min == fact.dose_max:
        return f"{fact.dose_min:g} {fact.dose_unit} পানিতে মিশিয়ে স্প্রে করুন"
    return f"{fact.dose_min:g}–{fact.dose_max:g} {fact.dose_unit} পানিতে মিশিয়ে স্প্রে করুন"
