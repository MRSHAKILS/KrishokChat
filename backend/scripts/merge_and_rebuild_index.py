"""Merge generated knowledge nodes into main RAG index and rebuild BM25."""
import json
import pathlib
import pickle
import sys

sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
MAIN_NODES = ROOT / "ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl"
GENERATED_NODES = ROOT / "ml_assets/advisory/generated_knowledge_nodes.jsonl"
BM25_INDEX = ROOT / "ml_assets/rag_index/indexes/bm25_index.pkl"


def merge_nodes():
    """Append generated nodes to main index, avoiding duplicates by ID."""
    existing_ids = set()
    existing_lines = []
    with open(MAIN_NODES, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            node = json.loads(line)
            existing_ids.add(node["id"])
            existing_lines.append(line)

    generated = []
    with open(GENERATED_NODES, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            node = json.loads(line)
            if node["id"] not in existing_ids:
                generated.append(line)
                existing_ids.add(node["id"])

    # Append to main file
    with open(MAIN_NODES, "a", encoding="utf-8") as f:
        for line in generated:
            f.write(line + "\n")

    print(f"Existing nodes: {len(existing_lines)}")
    print(f"Generated nodes added: {len(generated)}")
    print(f"Total nodes: {len(existing_lines) + len(generated)}")
    return len(existing_lines) + len(generated)


def rebuild_bm25():
    """Rebuild BM25 index from updated nodes file."""
    try:
        from rank_bm25 import BM25Okapi
    except ImportError:
        print("rank_bm25 not installed, skipping BM25 rebuild")
        return False

    nodes = []
    with open(MAIN_NODES, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                nodes.append(json.loads(line))

    # Build corpus from bm25_text
    corpus = [n.get("bm25_text", "") for n in nodes]
    tokenized = [doc.lower().split() for doc in corpus]
    bm25 = BM25Okapi(tokenized)

    # Save index with metadata
    index_data = {
        "bm25": bm25,
        "nodes": nodes,
        "corpus": corpus,
        "ids": [n["id"] for n in nodes],
    }
    with open(BM25_INDEX, "wb") as f:
        pickle.dump(index_data, f)

    print(f"BM25 index rebuilt: {len(nodes)} documents")
    return True


def main():
    total = merge_nodes()
    rebuild_bm25()
    print("\nDone. RAG index updated.")


if __name__ == "__main__":
    main()
