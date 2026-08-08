"""Full integration test: simulate complete advisory workflow via backend API."""
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")

import httpx
import json
import pathlib
import pickle

from app.services.advisory.intent_classifier import classify_intent
from app.services.advisory.generator import generate_response, get_gemini_keys

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
MAP_FILE = ROOT / "ml_assets/advisory/disease_knowledge_map.json"
BM25_INDEX = ROOT / "ml_assets/rag_index/indexes/bm25_index.pkl"

mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))


def search_bm25(query, crop=None, top_k=3):
    with open(BM25_INDEX, "rb") as f:
        index_data = pickle.load(f)
    bm25 = index_data["bm25"]
    nodes = index_data["nodes"]
    tokens = query.lower().split()
    if crop:
        tokens.append(crop.lower())
    scores = bm25.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    results = []
    for idx in top_indices:
        if scores[idx] > 0:
            node = nodes[idx]
            results.append({
                "id": node["id"],
                "title_en": node.get("title_en", ""),
                "title_bn": node.get("title_bn", ""),
                "content_bn": node.get("content_bn", ""),
                "content_en": node.get("content_en", ""),
                "treatment_summary_bn": node.get("treatment_summary_bn", ""),
                "prevention_bn": node.get("prevention_bn", ""),
                "score": float(scores[idx]),
            })
    return results


def get_disease_details(crop, disease_name):
    """Get disease details from nested disease_details.json."""
    VISION = ROOT / "ml_assets/vision"
    CROP_MODELS = {
        "Rice": VISION / "rice_disease",
        "Wheat": VISION / "wheat_disease",
        "Potato": VISION / "potato_disease",
        "Brassica": VISION / "brassica_disease",
        "Corn": VISION / "corn_disease",
    }
    model_dir = CROP_MODELS.get(crop)
    if not model_dir:
        return None
    dd_file = model_dir / "disease_details.json"
    if not dd_file.exists():
        return None
    details = json.loads(dd_file.read_text(encoding="utf-8"))
    for lib_key, lib_val in details.items():
        if isinstance(lib_val, dict) and "classes" in lib_val:
            for cls_entry in lib_val["classes"]:
                cls_name = cls_entry.get("class_name", "")
                norm = cls_name.lower().split("(")[0].strip().replace(" ", "").replace("_", "")
                dname_norm = disease_name.lower().replace(" ", "").replace("_", "")
                if norm == dname_norm:
                    return cls_entry
    return None


def full_pipeline(query, detected_crop=None, detected_disease=None):
    """Complete pipeline: intent -> retrieval -> generation."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    if detected_crop:
        print(f"Detected: {detected_crop} / {detected_disease}")

    # 1. Intent classification
    intent_result = classify_intent(query, detected_crop, detected_disease)
    print(f"  Intent: {intent_result['intent']} (safety: {intent_result['safety_flag']})")

    if intent_result["safety_flag"] in ("emergency", "blocked"):
        print(f"  -> BLOCKED: {intent_result.get('canned_response', 'N/A')[:80]}")
        return intent_result

    # 2. Retrieval
    search_q = f"{detected_disease or ''} {detected_crop or ''} {intent_result['intent']}"
    nodes = search_bm25(search_q, detected_crop, top_k=3)
    print(f"  Retrieved {len(nodes)} nodes")

    # 3. Disease details
    details = get_disease_details(detected_crop, detected_disease) if detected_crop and detected_disease else None

    # 4. Generation
    result = generate_response(
        query=query,
        detected_crop=detected_crop,
        detected_disease=detected_disease,
        intent=intent_result["intent"],
        retrieved_nodes=nodes,
        disease_details=details,
    )
    print(f"  Response: {result['response'][:200]}")
    print(f"  Grounded: {result['grounded']}, Model: {result.get('model_used')}")
    return result


def main():
    test_cases = [
        # Category A: full info
        ("আলুর দেরি ব্লাইট রোগের প্রতিকার কি?", "Potato", "Late Blight"),
        ("ধানের ব্লাস্ট রোগ কী?", "Rice", "Leaf Blast"),
        ("গমের লিফ রাস্ট দূর করতে কী করব?", "Wheat", "Leaf Rust"),
        # Category B: partial info
        ("ফুলকপির ব্যাকটেরিয়াল সফট রট দূর করুন", "Brassica", "Cauliflower Bacterial Soft Rot"),
        # Category C: no info
        ("গমের ফিউজেরিয়াম ফুট রট কীভাবে দূর করব?", "Wheat", "Fusarium Foot Rot"),
        # Safety
        ("What is the capital of France?", None, None),
        ("I want to commit suicide", None, None),
        # No detection, general question
        ("ভুট্টার কমন রাস্ট রোগ কী?", "Corn", "Common Rust"),
    ]

    for query, crop, disease in test_cases:
        full_pipeline(query, crop, disease)


if __name__ == "__main__":
    main()
