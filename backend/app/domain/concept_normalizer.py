"""Stage 2B: Farmer Language Normalization & Agronomic Concept Layer (Module 2B.3).

Maps authentic rural colloquial Bangladeshi expressions into canonical
agronomic concepts and generates hypothesis-driven retrieval expansions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class NormalizedConceptResult:
    """Result of mapping colloquial expressions to agronomic concepts."""

    concept_id: str | None = None
    concept_label_bn: str | None = None
    matched_expression: str | None = None
    retrieval_hypotheses: tuple[str, ...] = field(default_factory=tuple)
    discriminative_features: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Farmer Expressions to Canonical Agronomic Concepts
# ---------------------------------------------------------------------------

_CONCEPT_REGISTRY: dict[str, dict[str, Any]] = {
    "leaf_blight_scorch": {
        "label_bn": "পাতা ঝলসানো ও ব্লাইট রোগ",
        "keywords": (
            "পাতা পুইড়া", "পাতা পোড়া", "পইড়া গেছে", "পুইড়া গেছে", "পুইড়া যাইতেছে",
            "ঝলসে গেছে", "ঝলসানো", "পোড়া পোড়া", "পোড়া দাগ", "পাতা পুড়ে",
            "বাদামি দাগ", "badami dag", "pata pura", "pata pora", "blight", "dag hoise", "dag", "দাগ পড়ছে", "দাগ",
        ),
        "crop_hypotheses": {
            "rice": (
                "খোলপোড়া রোগ (Sheath Blight)",
                "ব্যাকটেরিয়াল পাতা পোড়া (Bacterial Blight)",
                "ব্লাস্ট রোগ (Leaf Blast)",
            ),
            "potato": (
                "আলুর নাবি ধসা (Late Blight)",
                "আলুর আগাম ধসা (Early Blight)",
            ),
            "tomato": (
                "টমেটোর নাবি ধসা (Late Blight)",
                "টমেটোর আর্লি ব্লাইট",
            ),
            "chilli": (
                "মরিচের ডাইব্যাক ও ফল পচা",
                "অ্যানথ্রাকনোজ ব্লাইট",
            ),
        },
        "default_hypotheses": (
            "ব্লাইট বা ঝলসানো রোগ",
            "পাতার ছত্রাকজনিত পোড়া দাগ",
        ),
        "discriminative_question": "দাগগুলো কি বৃত্তাকার বাদামি, নাকি লম্বাটে চোখের মতো বা অনিয়মিত ভেজা?",
        "discriminative_chips": ("বৃত্তাকার বাদামি দাগ", "লম্বাটে চোখের মতো দাগ", "পানিসেঁচসেঁচে কালো দাগ"),
    },
    "wilting_damping_off": {
        "label_bn": "গাছ ঢলে পড়া ও গোড়া পচন",
        "keywords": (
            "গাছ মইরা", "গাছ শুকাচ্ছে", "গাছ ঢলে", "গাছ ঢইলা", "গাছ শুকাইয়া",
            "গাছ শুকায়", "গাছ মারা যায়", "গাছ মরে যায়", "গাছ মরে", "মইরা যার",
            "gach moira", "gach mara", "wilt",
        ),
        "crop_hypotheses": {
            "brinjal": (
                "বেগুনের ব্যাকটেরিয়াল উইল্ট (Bacterial Wilt)",
                "ফিউজারিয়াম ঢলে পড়া রোগ",
            ),
            "potato": (
                "আলুর ঢলে পড়া রোগ",
                "কান্ড পচা ও গোড়া পচন",
            ),
            "tomato": (
                "টমেটোর ব্যাকটেরিয়াল উইল্ট",
                "শিকড় ও গোড়া পচন",
            ),
            "rice": (
                "উফরা রোগ",
                "চারা পোড়া রোগ",
            ),
        },
        "default_hypotheses": (
            "ব্যাকটেরিয়াজনিত ঢলে পড়া রোগ",
            "ছত্রাকজনিত গোড়া ও শিকড় পচন",
        ),
        "discriminative_question": "গাছের কাণ্ড কাটলে কি সাদা তরল বা আঠা বের হয়, নাকি শিকড় শুকিয়ে কালো হয়ে গেছে?",
        "discriminative_chips": ("কাণ্ড থেকে সাদা তরল বের হয়", "শিকড় কালো ও পচা", "পাতা হলুদ হয়ে শুকায়"),
    },
    "leaf_curl_virus": {
        "label_bn": "পাতা কোঁকড়ানো ও ভাইরাস",
        "keywords": (
            "পাতা কুঁকড়ায়", "পাতা কোঁকড়া", "পাতা মুচড়ায়", "পাতা বাঁকা",
            "কুকড়াইয়া গেছে", "কুঁকড়ে গেছে", "পাতা কুকড়ায়", "পাতা কোঁকড়ানো",
            "কুকড়াই গেছে", "kukuraye", "kokrano", "leaf curl", "কুকড়ায়",
        ),
        "crop_hypotheses": {
            "chilli": (
                "মরিচের পাতা কোঁকড়ানো ভাইরাস (Chilli Leaf Curl)",
                "থ্রিপস ও মাকড়ের আক্রমণ",
            ),
            "tomato": (
                "টমেটোর লিফ কার্ল ভাইরাস",
                "সাদা মাছি বাহিত মোজাইক",
            ),
            "brinjal": (
                "লিটল লিফ রোগ",
                "মাইকোপ্লাজমা জনিত রোগ",
            ),
        },
        "default_hypotheses": (
            "পাতা কোঁকড়ানো ভাইরাসজনিত রোগ",
            "সাকিং পেস্ট (থ্রিপস/মাইট) আক্রমণ",
        ),
        "discriminative_question": "পাতা কি ওপরের দিকে নৌকার মতো কুঁকড়েছে, নাকি পাতার নিচে খুব ছোট পোকা/মাকড় দেখা যায়?",
        "discriminative_chips": ("ওপরের দিকে কুঁকড়ানো", "নিচের দিকে মোচড়ানো ও পোকা আছে", "পাতা খসখসে ও হলুদ"),
    },
    "chlorosis_deficiency": {
        "label_bn": "পাতা হলুদ হওয়া ও পুষ্টির ঘাটতি",
        "keywords": (
            "গাছ হলুদ", "পাতা হলুদ", "হলদেটে", "ফ্যাকাশে", "গাছ হলদে", "হলুদ দাগ",
            "হলদি", "gach holud", "pata holud", "yellow",
        ),
        "crop_hypotheses": {
            "rice": (
                "টুংরো ভাইরাস (Rice Tungro)",
                "নাইট্রোজেনের ঘাটতি",
                "সালফার ও জিংকের অভাব",
            ),
            "potato": (
                "নাইট্রোজেনের অভাব",
                "ম্যাগনেসিয়াম বা আয়রন ঘাটতি",
            ),
            "wheat": (
                "হলুদ মরিচা রোগ (Yellow Rust)",
                "নাইট্রোজেন ঘাটতি",
            ),
        },
        "default_hypotheses": (
            "পুষ্টি উপাদানের অভাবজনিত ক্লোরোসিস",
            "ভাইরাসজনিত হলুদ রোগ",
        ),
        "discriminative_question": "পুরো ক্ষেতের গাছ কি একসাথে হালকা হলুদ হয়েছে, নাকি শুধু কচি পাতা ফ্যাকাশে?",
        "discriminative_chips": ("পুরো ক্ষেত একসাথে ফ্যাকাশে", "শুধু কচি পাতা হলুদ", "পাতায় ছোপ ছোপ হলুদ দাগ"),
    },
    "pest_infestation": {
        "label_bn": "কীটপতঙ্গ ও পোকার আক্রমণ",
        "keywords": (
            "পোকা ধরছে", "পোঁকা", "পোকায় খায়", "পোকায় খায়", "মাজরা",
            "লেদা পোকা", "জাব পোকা", "কীটপতঙ্গ", "পোকার আক্রমণ", "পোকায় কাটছে",
            "পোকা লাগি", "পোকা", "poka", "chidro", "fota",
        ),
        "crop_hypotheses": {
            "rice": (
                "মাজরা পোকা (Stem Borer)",
                "বাদামি গাছফড়িং (BPH)",
                "পাতা মোড়ানো পোকা (Leaf Roller)",
            ),
            "brinjal": (
                "ডগা ও ফল ছিদ্রকারী পোকা (BFSB)",
                "এফিড বা জাব পোকা",
            ),
            "chilli": (
                "মরিচের থ্রিপস পোকা",
                "হলুদ মাকড় বা মাইট",
            ),
            "potato": (
                "কাটওয়ার্ম বা কাটুই পোকা",
                "জাব পোকা",
            ),
        },
        "default_hypotheses": (
            "কীটপতঙ্গ দমন ও সমন্বিত বালাই ব্যবস্থাপনা (IPM)",
            "ক্ষতিকর পোকার আক্রমণ",
        ),
        "discriminative_question": "পোকা কি পাতা কেটে খাচ্ছে, ডগার ভেতরে ছিদ্র করছে, নাকি পাতার রস চুষে খাচ্ছে?",
        "discriminative_chips": ("ডগা বা কান্ড ছিদ্র করছে", "পাতা চিবিয়ে খাচ্ছে", "পাতার রস চুষে খাচ্ছে"),
    },
    "waterlogging_drainage": {
        "label_bn": "পানি নিষ্কাশন ও জলমগ্নতা",
        "keywords": (
            "পানি দাঁড়ায়", "পানি জমছে", "বৃষ্টির পানি", "স্যাঁতসেঁতে", "পানি জমে থাকে",
            "পানি নামে না", "পানি আটকায়", "পানি আতকি", "পচি যারগা", "পানি জমা",
        ),
        "crop_hypotheses": {},
        "default_hypotheses": (
            "ক্ষেতের অতিরিক্ত পানি নিষ্কাশন ও নালার ব্যবস্থা",
            "জলমগ্নতাজনিত শিকড় পচন রোধ",
        ),
        "discriminative_question": "বৃষ্টির পানি কি জমিতে ২-৩ দিনের বেশি জমে থাকে?",
        "discriminative_chips": ("হ্যাঁ, পানি জমে থাকে", "না, দ্রুত নেমে যায়", "মাটি সবসময় স্যাঁতসেঁতে"),
    },
}



import unicodedata


def _canonical_bn(text: str) -> str:
    """Canonicalizes Bengali unicode variants (NFC + Nukta equivalence)."""
    t = unicodedata.normalize("NFC", text.lower())
    t = t.replace("\u09a1\u09bc", "\u09dc").replace("\u09a2\u09bc", "\u09dd").replace("\u09af\u09bc", "\u09df")
    t = t.replace("ড়", "ড়").replace("ঢ়", "ঢ়").replace("য়", "য়")
    return t


class ConceptNormalizer:
    """Normalizes colloquial Bengali agricultural text to canonical concepts."""

    @classmethod
    def normalize(
        cls,
        query: str,
        crop: str | None = None,
    ) -> NormalizedConceptResult:
        """Analyzes query text for known colloquial symptom patterns."""
        norm_query = _canonical_bn(query)
        clean_crop = crop.strip().lower() if crop else None

        for concept_id, spec in _CONCEPT_REGISTRY.items():
            for kw in spec["keywords"]:
                norm_kw = _canonical_bn(kw)
                if norm_kw in norm_query:
                    hypotheses = spec["crop_hypotheses"].get(
                        clean_crop,
                        spec["default_hypotheses"],
                    )
                    chips = spec.get("discriminative_chips", ())
                    return NormalizedConceptResult(
                        concept_id=concept_id,
                        concept_label_bn=spec["label_bn"],
                        matched_expression=kw,
                        retrieval_hypotheses=tuple(hypotheses),
                        discriminative_features=tuple(chips),
                    )

        return NormalizedConceptResult()
