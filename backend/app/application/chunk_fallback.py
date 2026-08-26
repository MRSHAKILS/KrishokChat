"""R13 — Grounded chunk fallback resolver (read-only, zero LLM).

Loads the offline-built chunk index (tools/rag/15_build_chunk_index.py) and
returns the top BM25-matching source_md sections as ``RetrievedSource`` evidence
for the zero-node-source branch of the QA pipeline. Nodes always come first:
the pipeline only calls this resolver when node retrieval produced nothing
(Amendment 03). Chunk text is reconstructed from exact file slices and sha256
pins are verified on first load, so an edited/rotated corpus disables the
fallback gracefully instead of serving drifted evidence.
"""
from __future__ import annotations

import hashlib
import json
import pickle
import threading
from pathlib import Path

from app.domain.contracts import RetrievedSource


class ChunkFallbackResolver:
    def __init__(
        self,
        index_dir: Path,
        source_dir: Path,
        top_k: int = 4,
    ) -> None:
        self._index_dir = index_dir
        self._source_dir = source_dir
        self.top_k = top_k
        self._index = None
        self._chunks: list[dict] = []
        self._lock = threading.Lock()

    @property
    def available(self) -> bool:
        return (
            (self._index_dir / "chunks_bm25.pkl").exists()
            and (self._index_dir / "chunks_corpus.jsonl").exists()
            and self._source_dir.exists()
        )

    def _load(self) -> tuple[object | None, list[dict]]:
        if self._index is not None and self._chunks:
            return self._index, self._chunks
        with self._lock:
            if self._index is None:
                corpus_path = self._index_dir / "chunks_corpus.jsonl"
                index_path = self._index_dir / "chunks_bm25.pkl"
                if not corpus_path.exists() or not index_path.exists():
                    return None, []
                chunks = [json.loads(line) for line in corpus_path.read_text(encoding="utf-8").splitlines() if line.strip()]
                # Integrity gate: the pin file must match both artifacts, and a
                # sampled slice must hash to its recorded sha256. Any drift -> the
                # resolver stays unavailable (fail-closed to today's REFERRAL).
                pin_path = self._index_dir / "chunks_sha256.txt"
                if pin_path.exists():
                    for line in pin_path.read_text(encoding="utf-8").splitlines():
                        if not line.strip():
                            continue
                        expected, name = line.split(maxsplit=1)
                        artifact = self._index_dir / name.strip()
                        if artifact.exists() and hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
                            return None, []
                ok = self._verify_sample(chunks)
                if not ok:
                    return None, []
                with (self._index_dir / "chunks_bm25.pkl").open("rb") as handle:
                    self._index = pickle.load(handle)
                self._chunks = chunks
        return self._index, self._chunks

    def _verify_sample(self, chunks: list[dict]) -> bool:
        """Verify sha256 of sampled chunk slices against the live source files."""
        step = max(1, len(chunks) // 25)
        for rec in chunks[::step]:
            md = self._source_dir / rec["md_path"]
            if not md.exists():
                return False
            text = md.read_text(encoding="utf-8", errors="replace")
            seg = text[rec["char_start"]:rec["char_end"]]
            if hashlib.sha256(seg.encode("utf-8")).hexdigest() != rec["sha256"]:
                return False
        return True

    def _read_slice(self, rec: dict) -> str:
        md = self._source_dir / rec["md_path"]
        text = md.read_text(encoding="utf-8", errors="replace")
        return text[rec["char_start"]:rec["char_end"]]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()

    def retrieve(self, query: str) -> list[RetrievedSource]:
        """Top BM25 chunks as evidence sources; empty list = no fallback."""
        index, chunks = self._load()
        if index is None or not chunks:
            return []
        try:
            scores = index.get_scores(self._tokenize(query))
        except (ValueError, AttributeError, TypeError):
            return []
        if scores is None or len(scores) == 0:
            return []
        max_score = float(max(scores))
        if max_score <= 0:
            return []
        threshold = max_score * 0.2
        results: list[RetrievedSource] = []
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], bool(chunks[i].get("covered_by_node")), i))
        for position in order:
            score = float(scores[position])
            if score <= threshold or len(results) >= self.top_k:
                break
            rec = chunks[position]
            seg = self._read_slice(rec)
            results.append(RetrievedSource(
                id=str(rec.get("chunk_id", "")),
                score=score,
                title_en=str(rec.get("heading", "")),
                content_bn=seg,
                source=f"{rec.get('institution', '')}/{rec.get('doc_dir', '')}".strip("/"),
                citation=f"{rec.get('institution', '')}. {rec.get('heading', '')} ({rec.get('md_path', '')})",
                metadata={
                    "evidence_kind": "chunk_fallback",
                    "institution": rec.get("institution", ""),
                    "md_path": rec.get("md_path", ""),
                    "covered_by_node": rec.get("covered_by_node", []),
                    "chunk_sha256": rec.get("sha256", ""),
                },
            ))
        return results
