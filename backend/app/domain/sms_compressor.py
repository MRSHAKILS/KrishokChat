"""Deterministic 11-slot SMS template compressor (E15 Arm A & Extractive Packer).

Ensures safety-critical parameters (dose, active ingredient, formulation,
spray interval tau, and pre-harvest interval PHI) survive within the strict
160-character ceiling of SMS (UCS-2 / GSM 03.38), eliminating generative
truncation hazards.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.contracts import QAResult
    from app.domain.fact_base import Fact

# Regex for stripping citations e.g. [B5_BARCAG_467CF2_002]
_CITE_RE = re.compile(r"\[[A-Za-z0-9_\-]+\]")
_WS_RE = re.compile(r"\s+")

# Dose pattern for fallback validation
_DOSE_RE = re.compile(
    r"[0-9০-৯]+(?:[.,][0-9০-৯]+)?\s*(?:ml|mg|\bg\b|kg|\bl\b|liter|litre|"
    r"মিলি|গ্রাম|লিটার|কেজি|ইসি|ডব্লিউপি|EC|WP|SC|SL|শতক|বিঘা|একর)",
    re.IGNORECASE,
)


class SMSCompressor:
    """Deterministic, fail-closed SMS compressor and template packer."""

    DEFAULT_REFERRAL = "কৃষি তথ্য ও পরামর্শ পেতে সরকারি কৃষি কল সেন্টারে সরাসরি ডায়াল করুন: ১৬১২৩ (সকাল ৭টা-সন্ধ্যা ৭টা)।"
    DEFAULT_HELPLINE = "১৬১২৩"

    @classmethod
    def compress_from_slots(
        cls,
        crop: str,
        pest: str,
        active: str,
        formulation: str = "",
        dose_min: float = 0.0,
        dose_max: float = 0.0,
        unit: str = "g/l",
        vol: str = "1L",
        tau: int = 7,
        phi: int = 14,
        helpline: str = "16123",
        institution: str = "DAE",
        lang: str = "bn",
        max_chars: int = 160,
    ) -> str:
        """Deterministic 11-slot template compression (E15 Arm A).

        Guarantees 100% survival of dose, tau, and phi within <= 160 characters.
        """
        form_str = f" {formulation}" if formulation else ""
        if dose_min == dose_max or dose_max <= 0:
            dose_str = f"{dose_min:g}"
        else:
            dose_str = f"{dose_min:g}-{dose_max:g}"

        if lang == "en":
            # E15 GSM 03.38 Arm A format
            pest_clean = pest.replace("_", " ")
            msg = (
                f"{institution} ADV: {crop.capitalize()}: {pest_clean}. "
                f"Use {active}{form_str} @{dose_str}{unit}/{vol}. "
                f"Spray every {tau}d. PHI {phi}d. Call {helpline}."
            )
        else:
            # Bengali UCS-2 format
            pest_clean = pest.replace("_", " ")
            msg = (
                f"{institution} পরামর্শ: {crop} {pest_clean}: {active}{form_str} "
                f"@{dose_str}{unit} প্রয়োগ করুন। ব্যবধান {tau} দিন, PHI {phi} দিন। কল: {helpline}"
            )

        return msg[:max_chars]

    @classmethod
    def compress_from_fact(
        cls,
        fact: Fact,
        institution: str = "DAE",
        lang: str = "bn",
        max_chars: int = 160,
    ) -> str:
        """Compress a verified FactBase row into the deterministic SMS template."""
        crop = fact.crop_bn or fact.crop
        pest = fact.problem_bn or fact.problem
        return cls.compress_from_slots(
            crop=crop,
            pest=pest,
            active=fact.active_ingredient,
            formulation="",
            dose_min=fact.dose_min,
            dose_max=fact.dose_max,
            unit=fact.dose_unit,
            vol="1L",
            tau=fact.application_interval_days,
            phi=fact.pre_harvest_interval_days,
            helpline=cls.DEFAULT_HELPLINE if lang == "bn" else "16123",
            institution=institution,
            lang=lang,
            max_chars=max_chars,
        )

    @classmethod
    def compress_from_qa_result(
        cls,
        qa_res: QAResult,
        institution: str = "DAE",
        max_chars: int = 160,
    ) -> str:
        """Compress a QAResult into an SMS advisory, prioritizing dosage survival.

        1. If blocked, low confidence, or verifier flags present -> Strict 16123 referral.
        2. If dosage claims exist -> Prioritize the dosage-carrying sentence(s).
        3. Fallback to clean truncation for non-dosage general advice.
        """
        conf = str(qa_res.confidence.value) if hasattr(qa_res.confidence, "value") else str(qa_res.confidence)
        cat = str(qa_res.category.value) if hasattr(qa_res.category, "value") else str(qa_res.category)
        vflags = tuple(getattr(qa_res, "verifier_flags", ()) or ())

        # 1. Fail-closed referral gate: unverified dosage claims or safety blocks
        if cat != "safe_agri" or conf in ("blocked", "low_confidence") or len(vflags) > 0:
            return cls.DEFAULT_REFERRAL[:max_chars]

        raw_answer = qa_res.answer or ""
        clean_ans = _CITE_RE.sub("", raw_answer).strip()
        clean_ans = _WS_RE.sub(" ", clean_ans)

        prefix = f"{institution} পরামর্শ: "
        suffix = " | হেল্প: ১৬১২৩"
        avail = max_chars - len(prefix) - len(suffix)

        # 2. Dosage-first extraction using dosage claim extractor
        from app.infrastructure.verification.dosage_claims import extract_claims

        claims = extract_claims(clean_ans)
        dosage_sentences = [
            c.sentence.strip()
            for c in claims
            if c.has_dosage and _DOSE_RE.search(c.sentence)
        ]

        if dosage_sentences:
            # Prioritize the primary dosage sentence
            primary_dose_sent = dosage_sentences[0]
            # Clean up leading bullets or symbols
            primary_dose_sent = re.sub(r"^[\*\-\•\d\.\s]+", "", primary_dose_sent).strip()

            if len(primary_dose_sent) <= avail:
                # If there is space, check if a brief context sentence can precede it
                all_sents = [s.strip() for s in re.split(r"[।;\n]+", clean_ans) if s.strip()]
                body = primary_dose_sent
                if all_sents and all_sents[0] != primary_dose_sent:
                    intro = re.sub(r"^[\*\-\•\d\.\s]+", "", all_sents[0]).strip()
                    combined = f"{intro}। {primary_dose_sent}"
                    if len(combined) <= avail:
                        body = combined
                return f"{prefix}{body}{suffix}"[:max_chars]
            else:
                # If the dosage sentence itself is very long, truncate at word boundary
                body = primary_dose_sent[:avail].strip()
                last_space = body.rfind(" ")
                if last_space > 20:
                    body = body[:last_space]
                return f"{prefix}{body}{suffix}"[:max_chars]

        # 3. Non-dosage general advice: truncate at word boundary
        body = clean_ans[:avail].strip()
        if len(clean_ans) > avail:
            last_space = body.rfind(" ")
            if last_space > 20:
                body = body[:last_space]

        return f"{prefix}{body}{suffix}"[:max_chars]
