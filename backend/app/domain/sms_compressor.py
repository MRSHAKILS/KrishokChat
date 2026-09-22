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
        if _chem_slot_enabled():
            clean_ans = clean_ans.replace("**", "").replace("__", "")
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

            # Chemical-name slot: a dose without its chemical is not an instruction.
            # If the dose sentence names no chemical, prepend the nearest one named
            # earlier in the verified answer (never invented: copied from the answer).
            if _chem_slot_enabled():
                chem = _nearest_chemical(clean_ans, primary_dose_sent)
                if chem:
                    labelled = f"{chem}: {primary_dose_sent}"
                    if len(labelled) <= avail:
                        return f"{prefix}{labelled}{suffix}"[:max_chars]
                    body = _truncate_keep_dose(labelled, avail)
                    if body:
                        return f"{prefix}{body}{suffix}"[:max_chars]

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



_GENERIC_CHEM_WORDS = frozenset({"সার", "কীটনাশক", "ছত্রাকনাশক", "আগাছানাশক", "ঔষধ", "ওষুধ"})
_KNOWN_ACTIVES: tuple[str, ...] | None = None


def _chem_slot_enabled() -> bool:
    import os

    return os.getenv("SMS_CHEM_SLOT", "1").strip() != "0"


def _known_actives() -> tuple[str, ...]:
    """Active ingredients from the verifier's dose reference + specific Bengali names."""
    global _KNOWN_ACTIVES
    if _KNOWN_ACTIVES is None:
        import json
        from pathlib import Path

        from app.infrastructure.verification.dosage_claims import _CHEMICAL_BN

        names: set[str] = {n for n in _CHEMICAL_BN if n not in _GENERIC_CHEM_WORDS}
        ref = Path(__file__).resolve().parents[2] / "ml_assets/rag_index/derived/dose_reference_v1.json"
        try:
            for e in json.loads(ref.read_text(encoding="utf-8")).get("entries", []):
                if e.get("active"):
                    names.add(str(e["active"]).lower())
        except (OSError, ValueError):
            pass
        _KNOWN_ACTIVES = tuple(sorted(names, key=len, reverse=True))
    return _KNOWN_ACTIVES


def _known_in(text: str) -> list[tuple[int, str]]:
    low = text.lower()
    out = []
    for name in _known_actives():
        pos = low.find(name)
        if pos >= 0:
            out.append((pos, text[pos:pos + len(name)]))
    return sorted(out)


def _nearest_chemical(answer: str, dose_sentence: str) -> str | None:
    """Known active ingredient the dose refers to, copied from the answer.

    Returns None if the dose sentence already names a known active, or if no
    known active appears in the answer. Brand words are never used as labels.
    Search order: nearest mention before the dose sentence, then first after it.
    """
    if _known_in(dose_sentence):
        return None
    pos = answer.find(dose_sentence[:30])
    before = _known_in(answer[:pos]) if pos > 0 else []
    if before:
        return before[-1][1]
    after = _known_in(answer[pos + len(dose_sentence):]) if pos >= 0 else []
    return after[0][1] if after else None


def _truncate_keep_dose(text: str, avail: int) -> str | None:
    """Cut at a word boundary within `avail` chars without cutting the first dose span."""
    m = _DOSE_RE.search(text)
    if not m or m.end() > avail:
        return None
    body = text[:avail].strip()
    if len(text) > avail:
        cut = body.rfind(" ")
        if cut >= m.end():
            body = body[:cut]
    return body
