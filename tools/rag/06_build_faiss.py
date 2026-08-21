"""06 — Build the FAISS dense index from the embeddings produced by
03_build_embeddings.py. Offline, run once; artifacts live under indexes/.
The manifest's dense spec (intfloat/multilingual-e5-small, 384-dim,
IndexFlatIP over L2-normalized vectors) is the project's existing config.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import faiss
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
INDEXES = RAG_ROOT / "indexes"
EMB_PATH = INDEXES / "embeddings.npy"
IDS_PATH = INDEXES / "node_ids.json"
FAISS_PATH = INDEXES / "nodes.faiss"
HASH_PATH = INDEXES / "index_sha256.txt"
MANIFEST_PATH = RAG_ROOT / "manifest.json"


def main() -> None:
    if not EMB_PATH.exists() or not IDS_PATH.exists():
        raise SystemExit(
            f"Missing embeddings.npy or node_ids.json — run 03_build_embeddings.py first. ({EMB_PATH})"
        )

    vectors = np.load(EMB_PATH)
    node_ids = json.loads(IDS_PATH.read_text(encoding="utf-8"))
    dim = int(vectors.shape[1])
    if len(node_ids) != vectors.shape[0]:
        raise SystemExit(
            f"Mismatch: {len(node_ids)} ids vs {vectors.shape[0]} vectors"
        )

    print(f"vectors: {vectors.shape}, dtype={vectors.dtype}, dim={dim}")
    print("building faiss.IndexFlatIP ...")
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)  # vectors are already L2-normalized (03 does this)
    faiss.write_index(index, str(FAISS_PATH))
    print(f"wrote: {FAISS_PATH} ({FAISS_PATH.stat().st_size / 1e6:.1f} MB)")

    digest = hashlib.sha256(FAISS_PATH.read_bytes()).hexdigest()
    HASH_PATH.write_text(f"sha256  {digest}\ncreated {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n", encoding="utf-8")
    print(f"sha256: {digest} -> {HASH_PATH}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["retrieval"]["dense"] = {
        "model": "intfloat/multilingual-e5-small",
        "dimension": dim,
        "file": "indexes/embeddings.npy",
        "ids_file": "indexes/node_ids.json",
        "nodes": vectors.shape[0],
        "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": digest,
    }
    manifest["retrieval"]["faiss"] = {
        "type": "IndexFlatIP",
        "file": "indexes/nodes.faiss",
        "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manifest updated: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()