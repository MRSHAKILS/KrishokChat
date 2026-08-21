"""Generate embeddings via API (BGE-M3) and store locally.

Uses OpenRouter API (OpenAI-compatible) to generate BGE-M3 embeddings
without local CPU inference. Stores results as .npy for fast FAISS retrieval.

Usage:
    python scripts/03_build_embeddings_api.py --api-key $env:OPENROUTER_API_KEY
    python scripts/03_build_embeddings_api.py --api-key-file ..\.env
"""
import argparse
import json
import os
import time
from pathlib import Path

import numpy as np
import httpx

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SAG_DIR.parent if (SAG_DIR := SCRIPT_DIR).name == "scripts" else SCRIPT_DIR.parent
# Actually compute correctly:
RAG_ROOT = SCRIPT_DIR.parent
NODES_PATH = RAG_ROOT / "processed" / "knowledge_nodes_clean.jsonl"
OUT_DIR = RAG_ROOT / "indexes"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# OpenRouter API
OPENROUTER_URL = "https://openrouter.ai/api/v1/embeddings"
MODEL = "BAAI/bge-m3"  # Best for Bengali: dense + sparse + ColBERT
BATCH_SIZE = 50  # API batch size
CHECKPOINT_EVERY = 5


def load_nodes():
    nodes = []
    with open(NODES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            nodes.append(json.loads(line))
    return nodes


def get_api_key(args):
    if args.api_key:
        return args.api_key
    if args.api_key_file:
        with open(args.api_key_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
                if line.startswith("OPENROUTER_KEYS="):
                    # Take first key if multiple
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    return val.split(",")[0].strip()
    env_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_KEYS")
    if env_key:
        return env_key.split(",")[0].strip()
    raise ValueError("No API key found. Use --api-key, --api-key-file, or set OPENROUTER_API_KEY env var.")


def call_embedding_api(texts: list[str], api_key: str, model: str) -> np.ndarray:
    """Call OpenRouter embedding API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/KrishokChat-Advisory-System",
        "X-Title": "KrishokChat RAG",
    }
    payload = {
        "model": model,
        "input": texts,
    }

    resp = httpx.post(OPENROUTER_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    embeddings = []
    for item in data["data"]:
        embeddings.append(item["embedding"])
    return np.array(embeddings, dtype=np.float32)


def l2_normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-9)
    return (vectors / norms).astype(np.float32)


def main():
    parser = argparse.ArgumentParser(description="Generate BGE-M3 embeddings via API")
    parser.add_argument("--api-key", help="OpenRouter API key")
    parser.add_argument("--api-key-file", help="Path to .env file with API key")
    parser.add_argument("--model", default=MODEL, help="Embedding model")
    args = parser.parse_args()

    api_key = get_api_key(args)
    model = args.model

    print("Loading cleaned nodes...")
    nodes = load_nodes()
    n = len(nodes)
    print(f"  Loaded {n} nodes")
    print(f"  Model: {model}")

    texts = ["passage: " + node["embed_text"] for node in nodes]

    # Checkpoint
    checkpoint_path = OUT_DIR / "embeddings_checkpoint.npy"
    meta_path = OUT_DIR / "embeddings_checkpoint_meta.json"
    start_batch = 0
    dim = None

    if checkpoint_path.exists() and meta_path.exists():
        with open(meta_path) as f:
            meta = json.load(f)
        start_batch = meta["batch_idx"]
        dim = meta["dim"]
        all_embeddings = np.load(checkpoint_path)
        print(f"  Resuming from checkpoint (batch {start_batch})")
    else:
        all_embeddings = None

    n_batches = (n + BATCH_SIZE - 1) // BATCH_SIZE
    start_time = time.time()

    for i in range(start_batch, n_batches):
        batch_start = i * BATCH_SIZE
        batch_end = min(batch_start + BATCH_SIZE, n)
        batch_texts = texts[batch_start:batch_end]

        try:
            batch_emb = call_embedding_api(batch_texts, api_key, model)
        except Exception as e:
            print(f"  ERROR at batch {i+1}: {e}")
            # Save checkpoint and exit
            if all_embeddings is not None:
                np.save(checkpoint_path, all_embeddings[:batch_start])
                with open(meta_path, "w") as f:
                    json.dump({"batch_idx": i, "dim": dim or batch_emb.shape[1], "n": n}, f)
                print(f"  Checkpoint saved at batch {i}. Rerun to resume.")
            raise

        if dim is None:
            dim = batch_emb.shape[1]
            if all_embeddings is None:
                all_embeddings = np.zeros((n, dim), dtype=np.float32)

        all_embeddings[batch_start:batch_end] = batch_emb

        if (i + 1) % CHECKPOINT_EVERY == 0 or i == n_batches - 1:
            np.save(checkpoint_path, all_embeddings[:batch_end])
            with open(meta_path, "w") as f:
                json.dump({"batch_idx": i + 1, "dim": dim, "n": n}, f)
            elapsed = time.time() - start_time
            pct = batch_end / n * 100
            print(f"  Batch {i+1}/{n_batches} ({pct:.0f}%) — {elapsed:.0f}s — saved")

    total_time = time.time() - start_time
    print(f"  Done in {total_time:.1f}s")

    print("L2-normalizing...")
    all_embeddings = l2_normalize(all_embeddings)

    emb_path = OUT_DIR / "embeddings.npy"
    np.save(emb_path, all_embeddings)
    print(f"  Saved to {emb_path} ({emb_path.stat().st_size / 1e6:.1f} MB)")

    node_ids = [node["id"] for node in nodes]
    ids_path = OUT_DIR / "node_ids.json"
    with open(ids_path, "w", encoding="utf-8") as f:
        json.dump(node_ids, f, ensure_ascii=False)
    print(f"  Saved {len(node_ids)} node IDs")

    # Cleanup checkpoints
    if checkpoint_path.exists():
        checkpoint_path.unlink()
    if meta_path.exists():
        meta_path.unlink()

    print(f"\nDone! Shape: {all_embeddings.shape}")


if __name__ == "__main__":
    main()
