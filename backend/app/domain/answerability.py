"""Stage 2: Answerability-Aware Adaptive Routing (KAERA / PRISM).

Evaluates the 5-level answerability scale:
  A1  fully_supported       — accredited fact row (T1/T2); direct 0-LLM resolution
  A2  strong_evidence       — complete RAG grounding + verified dosage & PHI
  A3  partial_evidence      — missing exact chemical dose; progressive cultural guidance + observation checklist
  A4  missing_critical_info — underspecified query ($crop = \\emptyset$); minimum necessary clarification
  A5  unsafe_action         — banned chemical / crisis probe; refuse action + 16123 referral
"""

from __future__ import annotations

from typing import Any

from app.domain.contracts import RetrievedSource
from app.domain.enums import AnswerabilityLevel, SafetyCategory
from app.domain.intent import Intent


class AnswerabilityEvaluator:
    """Computes the exact AnswerabilityLevel and structured guidance frame."""

    @staticmethod
    def evaluate(
        *,
        category: SafetyCategory,
        intent: Intent | None,
        query: str,
        has_crop: bool,
        retrieved_sources: list[RetrievedSource] | None = None,
        is_fact_resolved: bool = False,
        matched_rules: tuple[str, ...] = (),
    ) -> AnswerabilityLevel:
        # A5: High-risk, banned chemical, self-harm, or security probe
        if category is not SafetyCategory.SAFE_AGRI:
            return AnswerabilityLevel.A5_UNSAFE_ACTION

        # A1: Fully accredited institutional fact row (0-LLM resolution)
        if is_fact_resolved:
            return AnswerabilityLevel.A1_FULLY_SUPPORTED

        # A4: Missing critical crop slot on treatment/problem question
        if intent is not None and intent.is_ambiguous and not has_crop:
            return AnswerabilityLevel.A4_MISSING_CRITICAL_INFO

        # Check retrieval evidence strength
        sources = retrieved_sources or []
        if not sources:
            # When safe_agri has zero sources, partial agronomic guidance is safer than hallucination
            return AnswerabilityLevel.A3_PARTIAL_EVIDENCE

        # Check if sources contain explicit chemical dosage keywords or verified summaries
        has_verified_dosage = False
        for s in sources:
            content = (s.content_bn or s.content_en).lower()
            metadata = s.metadata or {}
            if metadata.get("treatment_summary_bn") or metadata.get("dosage"):
                has_verified_dosage = True
                break
            # Look for active measurement indicators (e.g. মিলি, গ্রাম, লিটার, ইসি, ডব্লিউপি)
            if any(unit in content for unit in ("মিলি", "গ্রাম", "লিটার", "ইসি", "ডব্লিউপি", "ec", "wp", "প্রতি শতক")):
                has_verified_dosage = True
                break

        if has_verified_dosage and len(sources) >= 1:
            return AnswerabilityLevel.A2_STRONG_EVIDENCE

        # If general cultural or disease info is present but exact chemical dose is absent
        return AnswerabilityLevel.A3_PARTIAL_EVIDENCE

    @staticmethod
    def build_progressive_guidance(
        *,
        crop: str | None,
        problem: str | None,
        sources: list[RetrievedSource] | None = None,
    ) -> dict[str, Any]:
        """Constructs a structured progressive help frame for A3 queries.

        Ensures zero chemical invention while providing practical field guidance.
        """
        crop_label = crop or "ফসল"
        problem_label = problem or "সমস্যা"

        return {
            "mode": "progressive_cultural_guidance",
            "crop": crop,
            "problem": problem,
            "is_non_chemical": True,
            "title_bn": f"{crop_label}-এর {problem_label} সংক্রান্ত পর্যবেক্ষণ ও পরিবেশবান্ধব পরিচর্যা",
            "field_checks_bn": [
                "আক্রান্ত পাতার উপরের ও নিচের পিঠে কোনো ছত্রাকের গুঁড়া, দাগ বা পোকা আছে কি না খেয়াল করুন।",
                "গাছের কান্ড বা ডগায় কোনো ছিদ্র ও মলম বা পচন দেখা যাচ্ছে কি না পরীক্ষা করুন।",
                "সমগ্র জমিতে সমস্যা ছড়িয়ে পড়েছে নাকি কয়েকটি নির্দিষ্ট গাছে শুরু হয়েছে তা চিহ্নিত করুন।",
            ],
            "cultural_controls_bn": [
                "আক্রান্ত পাতা বা ডগা সাবধানে কেটে জমি থেকে দূরে মাটিতে পুঁতে ফেলুন বা পুড়িয়ে ধ্বংস করুন।",
                "জমিতে অতিরিক্ত পানি জমে থাকলে দ্রুত নিষ্কাশনের ব্যবস্থা করুন।",
                "জমিতে সুষম সার ব্যবহার করুন এবং অতিরিক্ত নাইট্রোজেন (ইউরিয়া) প্রয়োগ সাময়িক স্থগিত রাখুন।",
                "জমি সর্বদা আগাছামুক্ত ও পর্যাপ্ত আলো-বাতাস চলাচলের উপযোগী রাখুন।",
            ],
            "safety_boundary_bn": (
                "সঠিক মাত্রা নিশ্চিত না হয়ে কোনো রাসায়নিক কীটনাশক প্রয়োগ করবেন না। "
                "মাঠ পরিদর্শনের পর নির্দিষ্ট ওষুধের জন্য স্থানীয় উপ-সহকারী কৃষি কর্মকর্তা (SAAO) বা "
                "কৃষি কল সেন্টারে (১৬১২৩) যোগাযোগ করুন।"
            ),
        }
