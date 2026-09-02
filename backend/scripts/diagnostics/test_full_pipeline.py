"""Test full advisory pipeline: detection -> intent -> retrieval -> response."""
import json
import pathlib
import pickle
import sys

sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")

from app.services.advisory.intent_classifier import classify_intent

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
MAP_FILE = ROOT / "ml_assets/advisory/disease_knowledge_map.json"
BM25_INDEX = ROOT / "ml_assets/rag_index/indexes/bm25_index.pkl"

mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))


def search_bm25(query, crop=None, top_k=3):
    """Search BM25 with optional crop filter."""
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
                "score": float(scores[idx]),
                "category": node.get("category", ""),
                "has_treatment": bool(node.get("treatment_summary_bn") or (node.get("content_bn") and "প্রতিকার" in node.get("content_bn", ""))),
            })
    return results


def pipeline(query, detected_crop=None, detected_disease=None):
    """Run full pipeline: intent -> retrieval -> assemble context."""
    # 1. Classify intent
    intent_result = classify_intent(query, detected_crop, detected_disease)
    print(f"Query: {query}")
    print(f"  Intent: {intent_result['intent']} (safety: {intent_result['safety_flag']})")

    if intent_result["safety_flag"] in ("emergency", "blocked"):
        print(f"  BLOCKED: {intent_result.get('canned_response', 'N/A')[:60]}")
        return intent_result

    # 2. Get mapping for detected disease
    disease_key = None
    for cls, info in mapping.items():
        if info["disease_name"] == detected_disease and info["crop"] == detected_crop:
            disease_key = cls
            break

    if disease_key:
        info = mapping[disease_key]
        print(f"  Detected: {detected_crop} / {detected_disease} -> Category {info['category']}")
        print(f"  RAG nodes: {len(info['rag_node_ids'])} | has_details: {info['has_disease_details']}")
    else:
        print(f"  No mapping for {detected_crop}/{detected_disease}")

    # 3. BM25 retrieval
    search_query = f"{detected_disease} {detected_crop} {intent_result['intent']}"
    results = search_bm25(search_query, detected_crop, top_k=3)
    print(f"  Retrieved {len(results)} nodes:")
    for r in results:
        print(f"    [{r['score']:.1f}] {r['id'][:40]:40s} treatment={r['has_treatment']}")

    return {
        "intent": intent_result,
        "mapping": mapping.get(disease_key) if disease_key else None,
        "retrieved_nodes": results,
    }


def main():
    test_cases = [
        ("আলুর দেরি ব্লাইট রোগের প্রতিকার কি?", "Potato", "Late Blight"),
        ("ধানের ব্লাস্ট রোগ কী?", "Rice", "Leaf Blast"),
        ("ফুলকপির ব্যাকটেরিয়াল সফট রট দূর করুন", "Brassica", "Cauliflower__Bacterial_Soft_Rot"),
        ("গমের ব্লাস্ট রোগের প্রতিকার", "Wheat", "Blast"),
        ("What is the capital of France?", None, None),
    ]

    for query, crop, disease in test_cases:
        print("\n" + "=" * 60)
        pipeline(query, crop, disease)


if __name__ == "__main__":
    main()
