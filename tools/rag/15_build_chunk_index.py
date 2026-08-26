"""R13 — Build the grounded-chunk-fallback index from source_md (offline, run once).

Reads backend/ml_assets/rag_index/source_md/<INSTITUTION>/<doc>/sections/*.md,
chunks sections on exact character spans (every chunk is a verifiable substring
of its source file — sha256-checkable at runtime), builds a BM25 index, and
derives a precision-first node->MD coverage map from knowledge-node
citation/section_title fields.

v1 note (deviation from Amendment 03 §4): no sliding-window overlap — chunks are
clean paragraph-boundary slices so runtime reconstruction stays exact. The corpus
is pre-split into per-section files, which already provides natural boundaries.

Outputs (all under rag_index/):
  indexes/chunks_corpus.jsonl     one record per chunk (path+offsets, no text copy)
  indexes/chunks_bm25.pkl         pickled BM25Okapi over heading+slice tokens
  provenance/node_to_md_map.json  md_path -> node_ids (precision-first, scored)
  indexes/chunks_sha256.txt       pin of the two index files

This is an OFFLINE data op (AGENTS.md hard rule 2): never run at request time.
Runtime reader: backend/app/application/chunk_fallback.py
"""
from __future__ import annotations

import hashlib
import json
import pickle
import re
import sys
from pathlib import Path

from rank_bm25 import BM25Okapi

BACKEND = Path(__file__).resolve().parents[2] / "backend" / "ml_assets" / "rag_index"
SOURCE_MD = BACKEND / "source_md"
NODES_PATH = BACKEND / "raw" / "knowledge_nodes.json"
OUT_INDEX = BACKEND / "indexes"
OUT_PROV = BACKEND / "provenance"

MAX_CHARS = 2800   # ~400 whitespace tokens of mixed Bengali/English
MIN_CHARS = 200
MIN_WORDS = 30
MATCH_THRESHOLD = 0.7  # node<->md slug token-overlap (precision-first)


def _heading_of(seg: str, fallback: str) -> str:
    for line in seg.splitlines():
        if line.startswith("#"):
            return line.lstrip("# ").strip() or fallback
    return fallback


def chunk_text(text: str, display: str) -> list[dict]:
    """Chunk on exact char spans. Every emitted chunk satisfies
    chunk_text_file[char_start:char_end] == the hashed slice."""
    spans: list[tuple[int, int]] = []
    start = 0
    for part in text.split("\n\n"):
        end = start + len(part)
        if part.strip():
            spans.append((start, end))
        start = end + 2
    # Hard-split pathological paragraphs (> 2*MAX_CHARS) at whitespace so no
    # single span forces an oversize chunk.
    norm: list[tuple[int, int]] = []
    for s, e in spans:
        while e - s > 2 * MAX_CHARS:
            cut = text.rfind(" ", s, s + MAX_CHARS)
            if cut <= s:
                cut = s + MAX_CHARS
            norm.append((s, cut))
            s = cut
            while s < e and text[s].isspace():
                s += 1
        norm.append((s, e))

    chunks: list[dict] = []
    buf_start = buf_end = None

    def emit() -> None:
        nonlocal buf_start, buf_end
        if buf_start is None or buf_end is None or buf_end <= buf_start:
            buf_start = buf_end = None
            return
        seg = text[buf_start:buf_end]
        if len(seg) >= MIN_CHARS and len(seg.split()) >= MIN_WORDS:
            chunks.append({
                "heading": _heading_of(seg, display),
                "char_start": buf_start,
                "char_end": buf_end,
                "n_words": len(seg.split()),
                "sha256": hashlib.sha256(seg.encode("utf-8")).hexdigest(),
            })
        buf_start = buf_end = None

    for ps, pe in norm:
        if buf_start is None:
            buf_start, buf_end = ps, pe
        elif pe - buf_start <= MAX_CHARS:
            buf_end = pe
        else:
            emit()
            buf_start, buf_end = ps, pe
    emit()
    return chunks


def build_corpus() -> list[dict]:
    records: list[dict] = []
    for md in sorted(SOURCE_MD.rglob("*.md")):
        rel = md.relative_to(SOURCE_MD).as_posix()
        parts = rel.split("/")
        text = md.read_text(encoding="utf-8", errors="replace")
        display = re.sub(r"^\d+[_\-\s]*", "", md.stem).replace("_", " ").strip() or md.stem
        for idx, ch in enumerate(chunk_text(text, display)):
            records.append({
                "chunk_id": hashlib.md5(f"{rel}#{idx}".encode("utf-8")).hexdigest(),
                "md_path": rel,
                "institution": parts[0] if parts else "",
                "doc_dir": parts[1] if len(parts) > 2 else "",
                **ch,
            })
    return records


def _slug_tokens(s: str) -> set[str]:
    def norm(t: str) -> str:
        # light plural folding so "ecosystems" matches "ecosystem"
        return t[:-1] if t.endswith("s") and len(t) > 3 else t

    return {norm(t) for t in re.split(r"[^0-9a-z\u0980-\u09ff]+", s.lower()) if len(t) > 1}


# citation-prefix -> source_md folder aliases (folders are the canonical names)
INST_ALIASES: dict[str, list[str]] = {
    "MOA_NARS_SRDI": ["MOA", "NARS", "SRDI", "MINISTRY OF AGRICULTURE"],
    "BRRI_IRRI": ["BRRI", "IRRI"],
    "WORLDFISH": ["WORLDFISH", "WORLD FISH"],
}


def _inst_dirs() -> dict[str, list[tuple[set[str], str]]]:
    """All MD files keyed by every institution name/alias that can cite them."""
    by_inst: dict[str, list[tuple[set[str], str]]] = {}
    for md in sorted(SOURCE_MD.rglob("*.md")):
        rel = md.relative_to(SOURCE_MD)
        toks = _slug_tokens(re.sub(r"^\d+[_\-\s]*", "", md.stem).replace("_", " "))
        folder = rel.parts[0].upper()
        for key in [folder, *INST_ALIASES.get(folder, [])]:
            by_inst.setdefault(key, []).append((toks, rel.as_posix()))
    return by_inst


def build_node_map(records: list[dict]) -> dict:
    """Precision-first node->MD mapping: institution (citation prefix or alias)
    must match the MD folder, then section-title slug tokens must overlap
    >= threshold on either side (node-title or filename ratio, common >= 2)."""
    nodes = json.loads(NODES_PATH.read_text(encoding="utf-8"))
    by_inst = _inst_dirs()

    matched: dict[str, list[str]] = {}
    n_matched = 0
    for node in nodes:
        inst = str(node.get("citation", "")).split(".")[0].strip().upper()
        node_toks = _slug_tokens(f"{node.get('section_title', '')} {node.get('title_en', '')}")
        if not inst or not node_toks or inst not in by_inst:
            continue
        best_score, best_rel = 0.0, None
        for toks, rel in by_inst[inst]:
            if len(toks) < 2:
                continue
            common = node_toks & toks
            if len(common) < 2:
                continue
            score = max(len(common) / len(node_toks), len(common) / len(toks))
            if score > best_score:
                best_score, best_rel = score, rel
        if best_rel is not None and best_score >= MATCH_THRESHOLD:
            matched.setdefault(best_rel, []).append(str(node.get("node_id", "")))
            n_matched += 1

    for rec in records:
        rec["covered_by_node"] = matched.get(rec["md_path"], [])
    sample = [
        {"md_path": rel, "n_nodes": len(ids), "node_ids": ids[:3]}
        for rel, ids in sorted(matched.items(), key=lambda kv: -len(kv[1]))[:20]
    ]
    return {
        "meta": {
            "method": "institution(citation prefix) + section-title slug token-overlap >= "
                      f"{MATCH_THRESHOLD} (precision-first)",
            "nodes_total": len(nodes),
            "nodes_mapped": n_matched,
            "md_files_matched": len(matched),
            "sample_top20": sample,
        },
        "md_paths": matched,
    }


def main() -> int:
    if not SOURCE_MD.exists():
        print(f"missing {SOURCE_MD}", file=sys.stderr)
        return 1
    OUT_INDEX.mkdir(parents=True, exist_ok=True)
    OUT_PROV.mkdir(parents=True, exist_ok=True)

    print("Chunking source_md ...")
    records = build_corpus()
    if not records:
        print("no chunks produced", file=sys.stderr)
        return 1
    print(f"  {len(records)} chunks")

    print("Deriving node->MD coverage map ...")
    node_map = build_node_map(records)
    print(f"  {node_map['meta']['nodes_mapped']}/{node_map['meta']['nodes_total']} nodes mapped, "
          f"{node_map['meta']['md_files_matched']} MD files covered")

    corpus_path = OUT_INDEX / "chunks_corpus.jsonl"
    with corpus_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # BM25 text = heading + exact file slice, tokenized exactly like the runtime
    # resolver (lower().split()) so build and query tokenization can never drift.
    print("Tokenizing + building BM25Okapi (k1=2.2, b=0.4) ...")
    by_path: dict[str, list[dict]] = {}
    for rec in records:
        by_path.setdefault(rec["md_path"], []).append(rec)
    texts: list[list[str]] = []
    for rec in records:
        text = by_path[rec["md_path"]][0].get("_text")
        if text is None:
            text = (SOURCE_MD / rec["md_path"]).read_text(encoding="utf-8", errors="replace")
            by_path[rec["md_path"]][0]["_text"] = text
        seg = text[rec["char_start"]:rec["char_end"]]
        texts.append(f"{rec['heading']}\n{seg}".lower().split())
    bm25 = BM25Okapi(texts, k1=2.2, b=0.4)
    bm25_path = OUT_INDEX / "chunks_bm25.pkl"
    with bm25_path.open("wb") as f:
        pickle.dump(bm25, f)

    map_path = OUT_PROV / "node_to_md_map.json"
    map_path.write_text(json.dumps(node_map, ensure_ascii=False, indent=2), encoding="utf-8")

    pins = []
    for p in (corpus_path, bm25_path):
        pins.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}")
    (OUT_INDEX / "chunks_sha256.txt").write_text("\n".join(pins) + "\n", encoding="utf-8")

    print(f"  wrote {corpus_path.name}, {bm25_path.name}, {map_path.name}, chunks_sha256.txt")
    print("done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
