"""Generator for advisory workflow — calibrated confidence-gated responses.

4-way decision gate based on literature review:
  🟢 FULLY_GROUNDED  → KB has strong match, answer from KB + LLM synthesis
  🟡 PARTIALLY_GROUNDED → KB has partial info, answer KB + general LLM + refer
  🔴 GENERAL_GUIDANCE → KB weak, LLM provides safe general info with disclaimer
  ⚪ REFER_EXPERT    → KB empty + treatment-critical, refer to 16123

Never hallucinates chemical dosages. Escalates critical treatment gaps to Krishi Call Center.
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


TREATMENT_INTENTS = {"treatment", "prevention"}
CRITICAL_DOSAGE_WORDS = {"মাত্রা", "dosage", "প্রতি লিটার", "per liter", "ml", "গ্রাম", "gram", "কেজি", "kg"}


def is_treatment_critical(intent, query):
    """Check if query is asking for specific treatment/dosage."""
    if intent in TREATMENT_INTENTS:
        return True
    q = query.lower()
    return any(w in q for w in CRITICAL_DOSAGE_WORDS)


def compute_confidence_gate(retrieved_nodes, detected_crop, detected_disease, intent, query):
    """4-way confidence gate. Returns mode, confidence, explanation."""
    nodes = retrieved_nodes or []
    if not nodes and not detected_disease:
        if is_treatment_critical(intent, query):
            return "REFER_EXPERT", 0.1, "no_kb_treatment"
        return "GENERAL_GUIDANCE", 0.3, "no_kb_general"

    if not nodes:
        return "GENERAL_GUIDANCE", 0.4, "no_kb_has_context"

    top_score = max((n.get("score", 0) for n in nodes), default=0)
    top_match = nodes[0]
    tags = [t.lower() for t in top_match.get("tags", [])]
    crop_match = detected_crop and detected_crop.lower() in tags
    disease_match = detected_disease and detected_disease.lower().replace(" ", "_") in tags

    has_treatment = bool(top_match.get("treatment_summary_bn") or
                        (top_match.get("content_bn") and "প্রতিকার" in top_match.get("content_bn", "")))

    if top_score > 15 and crop_match and (disease_match or not detected_disease):
        if has_treatment:
            return "FULLY_GROUNDED", min(0.95, top_score / 25), "kb_strong_treatment"
        return "PARTIALLY_GROUNDED", 0.7, "kb_strong_no_treatment"

    if top_score > 8 and (crop_match or disease_match):
        if is_treatment_critical(intent, query):
            return "PARTIALLY_GROUNDED", 0.6, "kb_partial_critical"
        return "FULLY_GROUNDED", 0.75, "kb_moderate_safe"

    if top_score > 3:
        if is_treatment_critical(intent, query):
            return "PARTIALLY_GROUNDED", 0.5, "kb_weak_critical"
        return "GENERAL_GUIDANCE", 0.4, "kb_weak_safe"

    if is_treatment_critical(intent, query):
        return "REFER_EXPERT", 0.2, "kb_none_critical"
    return "GENERAL_GUIDANCE", 0.3, "kb_none_safe"


def build_prompt(query, detected_crop, detected_disease, intent, retrieved_nodes, disease_details=None):
    """Build a grounded prompt with calibrated instructions based on confidence gate."""
    gate_mode, confidence, gate_reason = compute_confidence_gate(
        retrieved_nodes, detected_crop, detected_disease, intent, query
    )

    context_parts = []
    if detected_crop:
        context_parts.append(f"ফসল: {detected_crop}")
    if detected_disease:
        context_parts.append(f"শনাক্ত রোগ: {detected_disease}")

    nodes_used = []
    if retrieved_nodes:
        if gate_mode == "FULLY_GROUNDED":
            nodes_used = retrieved_nodes[:3]
        elif gate_mode == "PARTIALLY_GROUNDED":
            nodes_used = retrieved_nodes[:2]
        elif gate_mode == "GENERAL_GUIDANCE":
            nodes_used = retrieved_nodes[:1]

        if nodes_used:
            context_parts.append("\nজ্ঞান ভান্ডার থেকে প্রাপ্ত তথ্য:")
            for i, node in enumerate(nodes_used):
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

    # Mode-specific instructions
    if gate_mode == "FULLY_GROUNDED":
        instructions = (
            "১. নিচে দেওয়া তথ্যের ভিত্তিতে সম্পূর্ণ উত্তর দাও\n"
            "২. ঔষধ/কীটনাশকের নাম ও মাত্রা দেওয়া থাকলে সেগুলো উল্লেখ করো\n"
            "৩. সংক্ষিপ্ত ও প্রাঞ্জল বাংলায় উত্তর দাও"
        )
    elif gate_mode == "PARTIALLY_GROUNDED":
        instructions = (
            "১. নিচে দেওয়া তথ্যের ভিত্তিতে উত্তর দাও\n"
            "২. তথ্য অসম্পূর্ণ হলে সৎভাবে বলো কোনো অংশের তথ্য নেই\n"
            "৩. নির্দিষ্ট মাত্রা না জানলে বলো 'বিস্তারিত মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩'\n"
            "৪. সংক্ষিপ্ত বাংলায় উত্তর দাও"
        )
    elif gate_mode == "GENERAL_GUIDANCE":
        instructions = (
            "১. এই তথ্য সাধারণ কৃষি জ্ঞান থেকে দাও — এটি নির্দিষ্ট ডাটাবেস নয়\n"
            "২. কখনোই নির্দিষ্ট ঔষধের মাত্রা দিও না — এটি বিপজ্জনক হতে পারে\n"
            "৩. শেষে উল্লেখ করো: 'নির্দিষ্ট মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩'\n"
            "৪. সংক্ষিপ্ত বাংলায় উত্তর দাও"
        )
    else:
        return (
            "দুঃখিত, এই রোগের নির্দিষ্ট তথ্য আমাদের ডাটাবেসে নেই। "
            "সঠিক পরামর্শের জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।",
            gate_mode, confidence, gate_reason, []
        )

    prompt = f"""তুমি একজন বাংলাদেশী কৃষি বিশেষঞ্জ সহায়ক। কৃষকদের কৃষি সমস্যার সমাধান দাও।

নিয়ম:
{instructions}

প্রসঙ্গ:
{context}

কৃষকের প্রশ্ন: {query}

উত্তর:"""

    return prompt, gate_mode, confidence, gate_reason, nodes_used


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
