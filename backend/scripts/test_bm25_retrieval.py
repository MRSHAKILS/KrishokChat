"""Test BM25 retrieval with new generated nodes."""
import json
import pathlib
import pickle
import sys

sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
BM25_INDEX = ROOT / "ml_assets/rag_index/indexes/bm25_index.pkl"


def search_bm25(query, top_k=3):
    """Search BM25 index and return top results."""
    with open(BM25_INDEX, "rb") as f:
        index_data = pickle.load(f)

    bm25 = index_data["bm25"]
    nodes = index_data["nodes"]

    tokens = query.lower().split()
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
                "score": float(scores[idx]),
                "category": node.get("category", ""),
            })
    return results


def main():
    test_queries = [
        "wheat black point disease treatment",
        "fusarium foot rot wheat",
        "cauliflower bacterial soft rot",
        "potato late blight treatment",
        "rice blast disease",
        "brassica downy mildew",
        "corn common rust",
    ]

    print("BM25 Retrieval Tests")
    print("=" * 60)
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = search_bm25(query, top_k=3)
        if not results:
            print("  No results")
        for r in results:
            print(f"  [{r['score']:.2f}] {r['id'][:40]:40s} {r['title_en'][:40]}")


if __name__ == "__main__":
    main()
