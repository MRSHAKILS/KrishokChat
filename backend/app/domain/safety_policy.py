"""Reviewable deterministic safety policy and Bengali terminal responses."""

from __future__ import annotations

import re

from app.domain.chemical_registry import compiled_banned_patterns
from app.domain.enums import SafetyCategory


PATTERNS: dict[SafetyCategory, tuple[tuple[str, re.Pattern[str]], ...]] = {
    SafetyCategory.SELF_HARM_OR_POISONING_RISK: (
        ("self_harm_bn", re.compile(
            "আত্মহত্যা|মরতে চাই|জীবন শেষ|নিজেকে ক্ষতি|"
            "বিষ\\s*(?:খাবো|খাব|খেলে|পান|খে\u09df\u09c7ছে|খে\u09df\u09c7|খে\u09af\u09bc\u09c7ছে|খে\u09af\u09bc\u09c7|খাইছে|গিলে|লাগা|গেলে)|"
            "কীটনাশক\\s*(?:খাবো|খাব|খেলে|পান|খে\u09df\u09c7ছে|খে\u09df\u09c7|খে\u09af\u09bc\u09c7ছে|খে\u09af\u09bc\u09c7|খাইছে|গিলে|লাগা|গেলে)|"
            "মারা যাওয়া|মৃত্যু হবে|কীভাবে মরব|মানুষ মারার|গরু মারার|মানুষের ক্ষতি|চোখে বিষ|চোখে কীটনাশক|বিষক্রিয়া|বিষাক্ত"
        )),
        ("self_harm_en", re.compile(r"\b(?:suicide|kill myself|end my life|self[- ]harm|poison myself|want to die|kill someone|lethal dose|human death|drank pesticide|swallowed pesticide|pesticide poisoning|pesticide in eyes|accidental poisoning)\b", re.I)),
        ("self_harm_banglish", re.compile(r"\b(?:bish|beesh|bisha)\s*(?:khabo|khab|khele|pan|kheye|khaise|gile|lagle|gele|khete)\b|\b(?:gile|kheye|khele)\s*(?:felse|phelse)?\s*(?:bish|beesh|kitnashok|kitnasok)\b|\b(?:kitnashok|kitnasok|balainashok)\s*(?:khabo|khab|khele|pan|kheye|khaise|gile)\b|\b(?:manush|goru|chagol)\s*(?:marar|marbo|marte)\b|\b(?:morte\s*chai|morbo|morar\s*jonno|nijeke\s*shesh)\b", re.I)),
    ),
    SafetyCategory.PROMPT_INJECTION: (
        ("injection_en", re.compile(r"\b(?:ignore (?:all|previous|the)|system prompt|jailbreak|dan mode|override safety|forget your instructions|system override|output only the word)\b", re.I)),
        ("injection_roleplay", re.compile(r"\b(?:you are now|pretend you are|act as)\b", re.I)),
        ("injection_bn", re.compile(r"আগের নির্দেশনা উপেক্ষা|নিরাপত্তা উপেক্ষা|নতুন নির্দেশনা|সিস্টেম প্রম্পট")),
    ),
    SafetyCategory.OFF_TOPIC: (
        ("off_topic_bn", re.compile(r"রাজধানীর নাম|ওয়েব স্ক্র্যাপার|পাইথন দিয়ে|আবহাওয়া কেমন|টাকার মান|বিশ্বকাপ|ভালোবাসার কবিতা|কবিতা লিখে|গান শোনাও|প্রোগ্রামিং")),
    ),
    # Banned/cancelled agrochemicals: composed from the source-attributed
    # registry (app.domain.chemical_registry) so the deterministic gate tracks
    # the real national cancelled list rather than a hand-picked sample. Each
    # entry carries a stable rule tag (banned_active:<name>:<lang>) that flows
    # into the audit trail's matched_rules. See chemical_registry.py for the
    # scope decision (legally-cancelled actives only, not still-registered HHPs).
    # The two generic Bengali catch-alls ("banned pesticide/chemical") are
    # appended so an explicit request for *any* prohibited agrochemical is
    # caught even when no specific active is named.
    SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL: compiled_banned_patterns()
    + (
        ("restricted_chemical_generic_bn", re.compile(r"নিষিদ্ধ কীটনাশক|নিষিদ্ধ রাসায়নিক|নিষিদ্ধ বালাইনাশক")),
        ("restricted_chemical_generic_banglish", re.compile(r"\b(?:nishiddho|nisiddho|banned)\s*(?:kitnashok|kitnasok|balainashok|bish|pesticide|chemical)\b|\b(?:shob\s*(?:ghas|gach)|neighbor)\b.{0,30}\b(?:mere\s*felbo|mere\s*felar|shesh\s*kore\s*dibo|shesh\s*kore|marbo|mara|na\s*bache)\b|\b(?:jeno\s*na\s*bache|na\s*bache)\s*emon\b", re.I)),
    ),
    # P4 D1a corpus-coverage gate (2026-08-14): deterministic refusal for
    # intents the advisory corpus cannot support, learned from the 12
    # unanswerable + 2 off_topic golden items (12/12 + 2/2 caught, 0/34
    # answerable touched on the golden set; evidence in
    # paper/.../17_FINDINGS_LOG_2026_08_14.md F9/D1a). Bengali has no word
    # boundaries, so alternations must never rely on bare substrings that
    # occur inside other words (e.g. "দাম" ⊂ "বাদামী" — the price rule was
    # dropped for exactly this reason). Rules are intentionally narrow and
    # evidence-driven; mixed queries fail closed (conservative).
    SafetyCategory.LOW_CONFIDENCE: (
        ("coverage_livestock", re.compile(r"কোয়েল|পোল্ট্রি|মুরগি|হাঁস|palon|quail|koel", re.I)),
        # "প্রশিক্ষন" (no ষ) is a real farmer typo seen in the pool.
        ("coverage_training", re.compile(r"প্রশিক্ষণ|প্রশিক্ষন|ট্রেনিং|কোর্স|শিখতে|শেখার|হাতে-কলমে")),
        ("coverage_export", re.compile(r"রপ্তানি|বিদেশে পাঠান|এক্সপোর্ট", re.I)),
        ("coverage_availability", re.compile(r"কোথায় পাওয়া|কোথায় পাব|কোথায় বিক্রি|ঠিকানা")),
        ("coverage_institutional", re.compile(r"বিভাগের ছাত্র|বিষয়ক তথ্য|সম্প্রসারণ অধিদপ্তর")),
        # Government-assistance intents only where actually attested: "সরকারি
        # কোনো সহায়তা পাওয়া যাবে" (q_895), "সরকারী ভাবে ... জমি সহায়তা"
        # (q_690, দীর্ঘ ী), "সরকারিভাবে কী কী নিয়ম" (q_850). Bare
        # "সরকারি"/"সরকারী"/"সহায়তা" are NOT gated — they appear in
        # answerable questions ("সরকারি বীজের দাম কত?", "জৈব সার কীভাবে
        # সহায়তা করে?") and would over-block ordinary farmers.
        ("coverage_assistance", re.compile(r"সরকার[িী]?\s*ভাবে|সরকার[িী]?.{0,12}(সহায়তা|ভর্তুকি)")),
    ),
}


CANNED_RESPONSES: dict[SafetyCategory, str] = {
    SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL: (
        "এই রাসায়নিকটি বাংলাদেশে কৃষিকাজে ব্যবহারের অনুমতি নেই বা নিষিদ্ধ। "
        "অনুমোদিত বিকল্প জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
    ),
    SafetyCategory.SELF_HARM_OR_POISONING_RISK: (
        "আপনার জীবন মূল্যবান। আপনি বা কেউ এখন বিপদে থাকলে অবিলম্বে ৯৯৯ নম্বরে কল করুন "
        "বা নিকটস্থ হাসপাতালে যান। কৃষি সহায়তার জন্য কৃষক কল সেন্টার: ১৬১২৩।"
    ),
    SafetyCategory.OFF_TOPIC: "এই সহায়কটি শুধু কৃষি সংক্রান্ত প্রশ্নের জন্য। ফসল, রোগ বা চাষাবাদ সম্পর্কে প্রশ্ন করুন।",
    SafetyCategory.PROMPT_INJECTION: "আমি কৃষি সংক্রান্ত প্রশ্নে সাহায্য করতে পারি। অনুগ্রহ করে একটি কৃষি প্রশ্ন করুন।",
    SafetyCategory.LOW_CONFIDENCE: (
        "এই প্রশ্নের নির্ভরযোগ্য উত্তর দেওয়ার মতো তথ্য আমার জ্ঞানভান্ডারে নেই। "
        "স্থানীয় পরামর্শের জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
    ),
}


def precheck(query: str) -> tuple[SafetyCategory, tuple[str, ...]] | None:
    """Return the first deterministic match; ordering prioritizes immediate harm.

    The corpus-coverage gate (LOW_CONFIDENCE) runs LAST so that a safety-
    critical match (self-harm, injection, banned chemical) always wins over
    a coverage refusal — e.g. "রপ্তানির জন্য প্যারাকোয়াট" is a banned-
    chemical decision, not a coverage decision.
    """
    for category in (
        SafetyCategory.SELF_HARM_OR_POISONING_RISK,
        SafetyCategory.PROMPT_INJECTION,
        SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
        SafetyCategory.LOW_CONFIDENCE,
    ):
        matched = tuple(name for name, pattern in PATTERNS[category] if pattern.search(query))
        if matched:
            return category, matched
    return None


def canned_response(category: SafetyCategory) -> str:
    return CANNED_RESPONSES.get(category, CANNED_RESPONSES[SafetyCategory.LOW_CONFIDENCE])
