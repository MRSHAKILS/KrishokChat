"""Build BM25 index from cleaned knowledge nodes."""
import json
import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
NODES_PATH = RAG_ROOT / "processed" / "knowledge_nodes_clean.jsonl"
OUT_DIR = RAG_ROOT / "indexes"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_nodes():
    nodes = []
    with open(NODES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            nodes.append(json.loads(line))
    return nodes


def main():
    print("Loading cleaned nodes...")
    nodes = load_nodes()
    print(f"  Loaded {len(nodes)} nodes")

    print("Tokenizing bm25_text...")
    corpus_tok = []
    for node in nodes:
        tokens = node["bm25_text"].split()
        corpus_tok.append(tokens)

    avg_len = sum(len(t) for t in corpus_tok) / len(corpus_tok)
    vocab = set(t for doc in corpus_tok for t in doc)
    print(f"  Avg doc length: {avg_len:.1f} tokens")
    print(f"  Vocabulary size: {len(vocab)}")

    print("Building BM25Okapi index (k1=2.2, b=0.4)...")
    bm25 = BM25Okapi(corpus_tok, k1=2.2, b=0.4)

    bm25_path = OUT_DIR / "bm25_index.pkl"
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)
    print(f"  Saved to {bm25_path}")

    tok_path = OUT_DIR / "bm25_corpus_tok.pkl"
    with open(tok_path, "wb") as f:
        pickle.dump(corpus_tok, f)
    print(f"  Saved tokenized corpus to {tok_path}")

    print("\nBM25 index build complete!")


if __name__ == "__main__":
    main()
