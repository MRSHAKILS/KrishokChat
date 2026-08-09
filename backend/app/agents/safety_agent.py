"""Safety / Router Agent — classifies queries before retrieval."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import dotenv

_SELF_HARM_PATTERNS = [
    "আত্মহত্যা", "suicide", "kill myself", "বিষ খাবো", "poison myself",
    "end my life", "জীবন শেষ", "harm myself", "self harm", "নিজেকে ক্ষতি",
    "die", "মরতে চাই", "insecticide drink", "কীটনাশক পান",
]
_INJECTION_PATTERNS = [
    "ignore previous", "ignore instructions", "you are now", "system prompt",
    "new instructions", "ignore all", "forget your instructions", "DAN mode",
    "jailbreak", "override safety", "pretend you are", "act as",
]
_BANNED_CHEMICAL_PATTERNS = [
    "methyl parathion", "paraquat", "ddt", "endosulfan", "carbofuran",
    "restricted pesticide", "banned chemical", "নিষিদ্ধ কীটনাশক",
]

dotenv.load_dotenv(Path(__file__).resolve().parents[3] / ".env")


def _gemini_keys() -> list[str]:
    keys = []
    for i in range(1, 30):
        k = os.getenv(f"GEMINI_API_KEY_{i}")
        if k:
            keys.append(k)
    if not keys:
        k = os.getenv("GEMINI_API_KEY")
        if k:
            keys.append(k)
    return keys


_last_call: dict[int, float] = {}
_key_idx = 0


def _next_key() -> str:
    global _key_idx
    keys = _gemini_keys()
    if not keys:
        return ""
    key = keys[_key_idx % len(keys)]
    _key_idx += 1
    return key


def _precheck(query: str) -> dict | None:
    q = query.lower()
    for pat in _SELF_HARM_PATTERNS:
        if pat.lower() in q:
            return {
                "category": "self_harm_or_poisoning_risk",
                "confidence": 1.0,
                "reasoning": f"Emergency keyword: '{pat}'",
                "canned_response": (
                    "আপনার জীবন মূল্যবান। যদি আপনি বা কেউ বিপদে থাকেন, "
                    "অনুগ্রহ করে অবিলম্বে ৯৯৯ নম্বরে কল করুন অথবা নিকটতম হাসপাতালে যান। "
                    "কৃষি সংক্রান্ত সহায়তার জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
                ),
            }
    for pat in _INJECTION_PATTERNS:
        if pat.lower() in q:
            return {
                "category": "prompt_injection",
                "confidence": 1.0,
                "reasoning": f"Prompt injection: '{pat}'",
                "canned_response": None,
            }
    for pat in _BANNED_CHEMICAL_PATTERNS:
        if pat.lower() in q:
            return {
                "category": "banned_or_restricted_chemical",
                "confidence": 1.0,
                "reasoning": f"Banned chemical keyword: '{pat}'",
                "canned_response": (
                    "এই রাসায়নিকটি বাংলাদেশে কৃষিকাজে ব্যবহারের অনুমতি নেই বা নিষিদ্ধ। "
                    "অনুমোদিত বিকল্প জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
                ),
            }
    return None


def classify_query(query: str, crop: str = None, disease: str = None) -> dict:
    pre = _precheck(query)
    if pre:
        return pre

    keys = _gemini_keys()
    if not keys:
        return {
            "category": "low_confidence", "confidence": 0.0,
            "reasoning": "No Gemini API keys configured",
            "canned_response": None,
        }

    key = _next_key()
    if not key:
        return {"category": "low_confidence", "confidence": 0.0,
                "reasoning": "No API key", "canned_response": None}

    # Build context for better classification
    context = ""
    if crop and disease:
        context = f"\n\nContext: The user previously uploaded an image that was detected as {crop} with {disease} disease. The query likely relates to this."
    elif crop:
        context = f"\n\nContext: The user previously uploaded an image of {crop}. The query likely relates to this."

    time.sleep(1.5)

    try:
        from google import genai
        client = genai.Client(api_key=key)
        from google import genai
        client = genai.Client(api_key=key)
        resp = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=(
                "Classify this agricultural query into exactly ONE category.\n"
                "Categories: safe_agri, banned_or_restricted_chemical, "
                "self_harm_or_poisoning_risk, off_topic, prompt_injection, low_confidence\n\n"
                f"Query: {query}{context}\n\n"
                'Respond ONLY as JSON: {"category": "...", "reasoning": "..."}'
            ),
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json", temperature=0.1
            ),
        )
        _last_call[id(key)] = time.time()
        data = json.loads(resp.text.strip())
        cat = data.get("category", "low_confidence")
        valid = {"safe_agri", "banned_or_restricted_chemical",
                 "self_harm_or_poisoning_risk", "off_topic",
                 "prompt_injection", "low_confidence"}
        if cat not in valid:
            cat = "low_confidence"

        canned = None
        if cat == "banned_or_restricted_chemical":
            canned = (
                "এই রাসায়নিকটি বাংলাদেশে কৃষিকাজে ব্যবহারের অনুমতি নেই বা নিষিদ্ধ।"
                " অনুমোদিত বিকল্প জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
            )
        elif cat == "off_topic":
            canned = (
                "এই প্রশ্নটি কৃষি সম্পর্কিত মনে হচ্ছে না। আমি শুধুমাত্র কৃষি বিষয়ে সাহায্য করতে পারি।"
                " ফসল, রোগ, বা কীটনাশক সম্পর্কে জিজ্ঞাসা করুন।"
            )
        elif cat == "prompt_injection":
            canned = "অনুগ্রহ করে কৃষি সংক্রান্ত প্রশ্ন করুন।"

        return {"category": cat, "confidence": 0.9,
                "reasoning": data.get("reasoning", ""), "canned_response": canned}
    except Exception as e:
        return {"category": "low_confidence", "confidence": 0.3,
                "reasoning": "API error: " + str(e), "canned_response": None}
