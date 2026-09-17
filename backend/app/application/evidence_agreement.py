"""Stage 2B: Evidence Disagreement Detection & Discriminative Clarification (Modules 2B.5 & 2B.6).

Detects when retrieved documents or symptom hypotheses conflict between
different pathogens, triggering Maximum Information Gain Clarification (MNC)
rather than blending dangerous chemical treatments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvidenceAgreementResult:
    """Result of analyzing agreement among retrieved evidence items."""

    is_conflicting: bool = False
    agreement_score: float = 1.0
    competing_diseases: tuple[str, ...] = field(default_factory=tuple)
    discriminative_question: str | None = None
    quick_reply_chips: tuple[str, ...] = field(default_factory=tuple)


# Curated pairwise discriminative disambiguation rules
_DISCRIMINATIVE_PAIRS: dict[frozenset[str], dict[str, Any]] = {
    frozenset(["blast", "brown_spot"]): {
        "question": "দাগগুলো কি ডিম্বাকৃতি গাঢ় বাদামি, নাকি মাঝখানে ছাইরঙা ও দুই প্রান্ত সুঁচালো চোখের মতো?",
        "chips": ("ডিম্বাকৃতি বাদামি দাগ (Brown Spot)", "মাঝখানে ছাই ও সুঁচালো দাগ (Blast)", "পাতার কিনারা পুড়ে গেছে"),
    },
    frozenset(["late_blight", "early_blight"]): {
        "question": "পাতার দাগে কি বৃত্তাকার পর্যায়ক্রমিক রিং দেখা যায়, নাকি পানিসেঁচসেঁচে দ্রুত বিস্তারকারী কালো দাগ?",
        "chips": ("বৃত্তাকার রিং বা চক্রাকার দাগ (Early Blight)", "পানিসেঁচসেঁচে কালো দাগ (Late Blight)", "ডগা শুকিয়ে গেছে"),
    },
    frozenset(["bacterial_wilt", "fusarium_wilt"]): {
        "question": "গাছের কাণ্ড কাটলে কি সাদাটে রস বা ব্যাকটেরিয়াল ওজ বের হয়, নাকি শিকড় পচে শুকিয়ে গেছে?",
        "chips": ("সাদাটে আঠালো রস বের হয় (Bacterial Wilt)", "শিকড় পচে শুকনো বাদামি (Fusarium)", "পাতায় হলদে দাগ"),
    },
    frozenset(["leaf_curl", "thrips"]): {
        "question": "পাতা কি ওপরের দিকে নৌকার মতো কুঁকড়েছে, নাকি নিচের দিকে মোচড়ানো ও পাতা খসখসে?",
        "chips": ("ওপরের দিকে কুঁকড়ানো (Thrips)", "নিচের দিকে মোচড়ানো ও খসখসে (Mites/Virus)", "পাতা স্বাভাবিক কিন্তু হলুদ"),
    },
}

# Known disease identifier aliases for frequency extraction
_DISEASE_KEYS: dict[str, tuple[str, ...]] = {
    "blast": ("ব্লাস্ট", "blast", "लीफ ब्लास्ट"),
    "brown_spot": ("বাদামি দাগ", "brown spot", "brown_spot", "বাদামী দাগ"),
    "late_blight": ("নাবি ধসা", "late blight", "late_blight", "নাবি ধ্বসা", "লেট ব্লাইট"),
    "early_blight": ("আগাম ধসা", "early blight", "early_blight", "আর্লি ব্লাইট"),
    "bacterial_wilt": ("ব্যাকটেরিয়াল উইল্ট", "bacterial wilt", "bacterial_wilt", "ঢলে পড়া"),
    "fusarium_wilt": ("ফিউজারিয়াম", "fusarium", "fusarium_wilt"),
    "leaf_curl": ("পাতা কোঁকড়ানো", "leaf curl", "leaf_curl", "কুকড়ানো"),
    "thrips": ("থ্রিপস", "thrips", "চুষি পোকা", "মাইট"),
}



class EvidenceAgreementGate:
    """Evaluates inter-source evidence agreement and generates targeted clarifications."""

    @classmethod
    def evaluate(
        cls,
        sources: list[dict[str, Any]] | list[str],
        candidate_hypotheses: tuple[str, ...] | list[str] | None = None,
    ) -> EvidenceAgreementResult:
        if not sources or len(sources) < 2:
            return EvidenceAgreementResult(is_conflicting=False, agreement_score=1.0)

        # 1. Collate source text
        full_text = " ".join(
            (s.get("content", "") if isinstance(s, dict) else str(s)).lower()
            for s in sources
        )

        # 2. Count disease mentions across retrieved sources
        disease_counts: dict[str, int] = {}
        for disease_id, aliases in _DISEASE_KEYS.items():
            count = sum(full_text.count(alias.lower()) for alias in aliases)
            if count > 0:
                disease_counts[disease_id] = count

        # Check if hypotheses also hint at multiple diseases
        if candidate_hypotheses:
            for h in candidate_hypotheses:
                h_lowered = h.lower()
                for d_id, aliases in _DISEASE_KEYS.items():
                    if any(a in h_lowered for a in aliases):
                        disease_counts[d_id] = disease_counts.get(d_id, 0) + 1

        # 3. Detect conflicting pair
        top_diseases = sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)
        if len(top_diseases) >= 2:
            top_1_name, top_1_count = top_diseases[0]
            top_2_name, top_2_count = top_diseases[1]

            # If the second candidate has at least 50% frequency of the top candidate,
            # this represents genuine diagnostic ambiguity
            if top_2_count >= 1 and (top_2_count / top_1_count) >= 0.5:
                pair_key = frozenset([top_1_name, top_2_name])
                pair_rule = _DISCRIMINATIVE_PAIRS.get(pair_key)

                if pair_rule:
                    return EvidenceAgreementResult(
                        is_conflicting=True,
                        agreement_score=0.45,
                        competing_diseases=(top_1_name, top_2_name),
                        discriminative_question=pair_rule["question"],
                        quick_reply_chips=pair_rule["chips"],
                    )
                else:
                    return EvidenceAgreementResult(
                        is_conflicting=True,
                        agreement_score=0.55,
                        competing_diseases=(top_1_name, top_2_name),
                        discriminative_question=f"লক্ষণটি কি মূলত {top_1_name}-এর মতো নাকি {top_2_name}-এর মতো?",
                        quick_reply_chips=(top_1_name, top_2_name, "লক্ষণ স্পষ্ট নয়"),
                    )

        return EvidenceAgreementResult(
            is_conflicting=False,
            agreement_score=0.92,
            competing_diseases=tuple(d[0] for d in top_diseases[:1]),
        )
