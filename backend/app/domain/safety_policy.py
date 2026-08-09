"""Reviewable deterministic safety policy and Bengali terminal responses."""

from __future__ import annotations

import re

from app.domain.enums import SafetyCategory


PATTERNS: dict[SafetyCategory, tuple[tuple[str, re.Pattern[str]], ...]] = {
    SafetyCategory.SELF_HARM_OR_POISONING_RISK: (
        ("self_harm_bn", re.compile(r"আত্মহত্যা|মরতে চাই|জীবন শেষ|নিজেকে ক্ষতি|বিষ খাবো|কীটনাশক পান")),
        ("self_harm_en", re.compile(r"\b(?:suicide|kill myself|end my life|self[- ]harm|poison myself|want to die)\b", re.I)),
    ),
    SafetyCategory.PROMPT_INJECTION: (
        ("injection_en", re.compile(r"\b(?:ignore (?:all|previous|the)|system prompt|jailbreak|dan mode|override safety|forget your instructions)\b", re.I)),
        ("injection_roleplay", re.compile(r"\b(?:you are now|pretend you are|act as)\b", re.I)),
        ("injection_bn", re.compile(r"আগের নির্দেশনা উপেক্ষা|নিরাপত্তা উপেক্ষা|নতুন নির্দেশনা")),
    ),
    SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL: (
        ("restricted_chemical_en", re.compile(r"\b(?:methyl parathion|paraquat|ddt|endosulfan|carbofuran)\b", re.I)),
        ("restricted_chemical_bn", re.compile(r"নিষিদ্ধ কীটনাশক|নিষিদ্ধ রাসায়নিক|প্যারাকোয়াট|পরাকুয়াট")),
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
    """Return the first deterministic match; ordering prioritizes immediate harm."""
    for category in (
        SafetyCategory.SELF_HARM_OR_POISONING_RISK,
        SafetyCategory.PROMPT_INJECTION,
        SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
    ):
        matched = tuple(name for name, pattern in PATTERNS[category] if pattern.search(query))
        if matched:
            return category, matched
    return None


def canned_response(category: SafetyCategory) -> str:
    return CANNED_RESPONSES.get(category, CANNED_RESPONSES[SafetyCategory.LOW_CONFIDENCE])
