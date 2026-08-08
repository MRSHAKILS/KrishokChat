"""Generator for advisory workflow — produces grounded responses using Gemini free keys.

Uses detected disease context + retrieved knowledge nodes to generate
accurate, non-hallucinated responses in Bengali.
"""
import json
import os
import pathlib
import time

import dotenv

# Load env from project root (parents[4] = .../backend/app/services/advisory -> .../backend -> .../project)
ROOT = pathlib.Path(__file__).resolve().parents[4]
PROJECT_ROOT = ROOT
BACKEND_ROOT = ROOT / "backend"
dotenv.load_dotenv(PROJECT_ROOT / ".env", override=False)
dotenv.load_dotenv(BACKEND_ROOT / ".env.local", override=False)

# Gemini model for generation (free keys)
GEN_MODEL = os.getenv("GEN_MODEL", "gemini-3.1-flash-lite")
MAX_TOKENS = 1000


def get_gemini_keys():
    """Get free Gemini API keys from project .env and backend/.env.local."""
    keys = []
    # Also load from project root .env
    for env_path in [ROOT / ".env", ROOT / ".env.local"]:
        if env_path.exists():
            dotenv.load_dotenv(env_path, override=False)
    for i in range(1, 30):
        k = os.getenv(f"GEMINI_API_KEY_{i}")
        if k:
            keys.append(k)
    k = os.getenv("GEMINI_API_KEY")
    if k:
        keys.append(k)
    return keys


_key_idx = 0
_last_call = {}


def next_key(keys):
    global _key_idx
    key = keys[_key_idx % len(keys)]
    _key_idx += 1
    elapsed = time.time() - _last_call.get(id(key), 0)
    if elapsed < 1.5:
        time.sleep(1.5 - elapsed)
    _last_call[id(key)] = time.time()
    return key


def build_prompt(query, detected_crop, detected_disease, intent, retrieved_nodes, disease_details=None):
    """Build a grounded prompt for the generator."""

    # Context sections
    context_parts = []

    if detected_crop:
        context_parts.append(f"ফসল: {detected_crop}")
    if detected_disease:
        context_parts.append(f"শনাক্ত রোগ: {detected_disease}")

    # Retrieved knowledge nodes
    if retrieved_nodes:
        context_parts.append("\nজ্ঞান ভান্ডার থেকে প্রাপ্ত তথ্য:")
        for i, node in enumerate(retrieved_nodes[:3]):
            title = node.get("title_en", "") or node.get("title_bn", "")
            content = node.get("content_bn", "") or node.get("content_en", "")
            treatment = node.get("treatment_summary_bn", "")
            if treatment:
                content += f" প্রতিকার: {treatment}"
            prevention = node.get("prevention_bn", "")
            if prevention:
                content += f" প্রতিরোধ: {prevention}"
            if content:
                context_parts.append(f"  [{i+1}] {title}: {content[:300]}")

    # Disease details (from YOLO model's disease_details.json)
    if disease_details:
        desc = disease_details.get("description_bn", "")
        sol = disease_details.get("solution_bn", "")
        cause = disease_details.get("cause_bn", "")
        if desc:
            context_parts.append(f"\nরোগের বিবরণ: {desc[:300]}")
        if cause:
            context_parts.append(f"কারণ: {cause[:200]}")
        if sol:
            context_parts.append(f"প্রতিকার: {sol[:300]}")

    context = "\n".join(context_parts)

    # Missing info handling
    has_knowledge = bool(retrieved_nodes or disease_details)
    if not has_knowledge:
        context += "\n\nগুরুত্বপূর্ণ: এই রোগের কোনো তথ্য জ্ঞান ভান্ডারে পাওয়া যায়নি।"

    prompt = f"""তুমি একজন বাংলাদেশী কৃষি বিশেষজ্ঞ সহায়ক। কৃষকদের কৃষি সমস্যার সমাধান দাও।

নিয়ম:
১. শুধুমাত্র নিচে দেওয়া তথ্যের ভিত্তিতে উত্তর দাও
২. যদি তথ্য অপর্যাপ্ত হয়, সৎভাবে বলো "এই রোগের বিস্তারিত তথ্য আমাদের ডাটাবেসে নেই"
৩. ঔষধ/কীটনাশকের নার্ম বা মাত্রা বলতে গিয়ে অজানা হলে বলো "কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩"
৴. সংক্ষিপ্ত ও প্রাঞ্জল বাংলায় উত্তর দাও

প্রসঙ্গ:
{context}

কৃষকের প্রশ্ন: {query}

উত্তর:"""

    return prompt, has_knowledge


def generate_response(query, detected_crop=None, detected_disease=None, intent=None,
                     retrieved_nodes=None, disease_details=None, model=None):
    """Generate a grounded response using Gemini free keys.

    Args:
        query: User's question
        detected_crop: Crop from YOLO
        detected_disease: Disease from YOLO
        intent: Classified intent
        retrieved_nodes: List of retrieved knowledge nodes
        disease_details: Disease details from disease_details.json
        model: Gemini model name (default: from env)

    Returns:
        dict with response text, grounded flag, sources
    """
    keys = get_gemini_keys()
    if not keys:
        return {
            "response": "দুঃখিত, এখন উত্তর দেওয়া সম্ভব নয়। কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।",
            "grounded": False,
            "sources": [],
        }

    prompt, has_knowledge = build_prompt(
        query, detected_crop, detected_disease, intent,
        retrieved_nodes or [], disease_details
    )

    model = model or GEN_MODEL
    key = next_key(keys)

    try:
        from google import genai
        client = genai.Client(api_key=key)
        resp = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=MAX_TOKENS,
            ),
        )
        _last_call[id(key)] = time.time()

        response_text = resp.text.strip()

        return {
            "response": response_text,
            "grounded": has_knowledge,
            "sources": [n.get("id", "") for n in (retrieved_nodes or [])[:3]],
            "model_used": model,
            "has_knowledge": has_knowledge,
        }
    except Exception as e:
        # Fallback: try next key
        try:
            key2 = next_key(keys)
            from google import genai
            client = genai.Client(api_key=key2)
            resp = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=MAX_TOKENS,
                ),
            )
            _last_call[id(key2)] = time.time()
            return {
                "response": resp.text.strip(),
                "grounded": has_knowledge,
                "sources": [n.get("id", "") for n in (retrieved_nodes or [])[:3]],
                "model_used": "gemini-2.5-flash-lite (fallback)",
                "has_knowledge": has_knowledge,
            }
        except Exception as e2:
            return {
                "response": (
                    "দুঃখিত, এখন উত্তর তৈরি করতে সমস্যা হচ্ছে। "
                    f"{'এই রোগের তথ্য ডাটাবেসে নেই। ' if not has_knowledge else ''}"
                    "কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
                ),
                "grounded": False,
                "sources": [],
                "error": str(e2),
            }
