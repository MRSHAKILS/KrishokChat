"""Intent Classifier for advisory workflow — uses OpenRouter with Gemini-2.5-Flash-Lite.

Classifies user queries into intents and checks safety before any retrieval.
"""
import json
import os
import pathlib
import time

import dotenv

# Load env
ROOT = pathlib.Path(__file__).resolve().parents[3]
dotenv.load_dotenv(ROOT / ".env.local")
dotenv.load_dotenv(ROOT / ".env")

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite-preview-06-17")

# Safety precheck patterns (no API call needed)
_SELF_HARM_PATTERNS = [
    "আত্মহত্যা", "suicide", "kill myself", "বিষ খাবো", "poison myself",
    "end my life", "জীবন শেষ", "harm myself", "self harm", "নিজেকে ক্ষতি",
    "die", "মরতে চাই", "insecticide drink", "কীটনাশক পান", "want to die",
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


def _precheck(query: str) -> dict | None:
    """Fast regex precheck — no API call."""
    q = query.lower()
    for pat in _SELF_HARM_PATTERNS:
        if pat.lower() in q:
            return {
                "intent": "self_harm_or_poisoning_risk",
                "safety_flag": "emergency",
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
                "intent": "prompt_injection",
                "safety_flag": "blocked",
                "confidence": 1.0,
                "reasoning": f"Prompt injection: '{pat}'",
                "canned_response": None,
            }
    for pat in _BANNED_CHEMICAL_PATTERNS:
        if pat.lower() in q:
            return {
                "intent": "banned_or_restricted_chemical",
                "safety_flag": "blocked",
                "confidence": 1.0,
                "reasoning": f"Banned chemical keyword: '{pat}'",
                "canned_response": (
                    "এই রাসায়নিকটি বাংলাদেশে কৃষিকাজে ব্যবহারের অনুমতি নেই বা নিষিদ্ধ। "
                    "অনুমোদিত বিকল্প জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
                ),
            }
    return None


def classify_intent(query: str, detected_crop: str = None, detected_disease: str = None) -> dict:
    """Classify query intent using Gemini via OpenRouter.

    Args:
        query: User's text query
        detected_crop: Crop from YOLO detection (optional)
        detected_disease: Disease from YOLO detection (optional)

    Returns:
        dict with intent, safety_flag, confidence, reasoning, canned_response
    """
    # Precheck first (no API call)
    pre = _precheck(query)
    if pre:
        return pre

    if not OPENROUTER_KEY:
        return {
            "intent": "safe_agri",
            "safety_flag": "ok",
            "confidence": 0.5,
            "reasoning": "No OpenRouter key configured, defaulting to safe_agri",
            "canned_response": None,
        }

    # Build context
    context = ""
    if detected_crop:
        context += f"\nDetected crop: {detected_crop}"
    if detected_disease:
        context += f"\nDetected disease: {detected_disease}"

    prompt = f"""Classify this agricultural query into exactly ONE intent category.

Categories:
- treatment: asking for treatment/cure/solution for a disease
- prevention: asking how to prevent a disease
- general_info: asking what a disease is, symptoms, cause
- variety: asking about crop varieties or seeds
- fertilizer: asking about fertilizer/nutrition
- pest: asking about pest/insect management
- off_topic: unrelated to agriculture
- other: agriculture-related but not fitting above

Query: {query}{context}

Respond ONLY as JSON: {{"intent": "...", "confidence": 0.0-1.0, "reasoning": "..."}}"""

    try:
        import httpx
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 200,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()

        # Parse JSON from response
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        result = json.loads(content)
        intent = result.get("intent", "other")
        valid = {"treatment", "prevention", "general_info", "variety", "fertilizer", "pest", "off_topic", "other"}
        if intent not in valid:
            intent = "other"

        canned = None
        if intent == "off_topic":
            canned = "এই প্রশ্ন কৃষি সম্পর্কিত নয়। আমি শুধুমাত্র কৃষি বিষয়ে সাহায্য করতে পারি।"

        return {
            "intent": intent,
            "safety_flag": "blocked" if intent == "off_topic" else "ok",
            "confidence": result.get("confidence", 0.8),
            "reasoning": result.get("reasoning", ""),
            "canned_response": canned,
        }
    except Exception as e:
        return {
            "intent": "safe_agri",
            "safety_flag": "ok",
            "confidence": 0.3,
            "reasoning": f"API error: {e}",
            "canned_response": None,
        }
