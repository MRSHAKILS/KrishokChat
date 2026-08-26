# R13 — Grounded Chunk Fallback (nodes first, MD chunks as gated evidence before refusal)

**Status:** ✅ DONE — 2026-08-27 (Amendment 03 APPROVED and implemented same day)
**Depends on:** R1, R3, R4 (flag pattern), R9 (offline precedent)
**Delivers:** coverage lift on zero-source queries without weakening fail-closed refusal; chunk hit
logs that feed the node-authoring queue (E24); E26 experiment substrate.
**Baseline rule:** one task, one branch, one agent; standing gates (full suite, golden replay 50/50,
`pnpm build`) hold before merge.

## Completion record (2026-08-27)

- Offline build (`tools/rag/15_build_chunk_index.py`): **4,815 chunks**, BM25Okapi k1=2.2/b=0.4,
  tokenization identical to the runtime resolver; precision-first node→MD map at
  `provenance/node_to_md_map.json` (**1,713/2,120 nodes**, 1,042 MD files, method in meta);
  `indexes/chunks_sha256.txt` pin. Artifacts: `chunks_bm25.pkl` (12 MB), `chunks_corpus.jsonl`
  (2 MB, path+offsets+sha256 — no text duplication).
- Runtime (`backend/app/application/chunk_fallback.py`): lazy, thread-safe, zero LLM; sha256 pin +
  sampled-slice integrity gate — tampered/rotated corpus disables the fallback (fail-closed).
- Pipeline: one gated touch point — only the zero-node-source branch that today REFUSES consults
  the fallback (`qa_pipeline.py` retrieval stage). `CHUNK_FALLBACK_ENABLED=false` default
  (`.env.example` updated).
- Deviations (conservative, recorded in Amendment 03 §7): no overlap (exact file slices), BM25-only
  v1, separate pin file instead of touching the R2 node pin.
- Gates: 17/17 new tests; **559 passed / 7 skipped / 0 new failures** full suite (5 live-e2e
  failures pre-existing/environmental — verified identical with change stashed); **golden replay
  50/50, invariants PASS with the flag ON**; frontend untouched (no `pnpm build` impact).
- Remaining before the flag may default ON: E26 frozen + accepted per
  `experiments/ACCEPTANCE_PROTOCOL.md`.

## Goal

When node retrieval yields zero usable sources (today: immediate REFERRAL/T4), attempt retrieval
over an offline-precomputed index of chunked `source_md/` documents; generate through the existing
grounded path; verify with the existing 11-slot verifier; label as evidence-grounded with
institution provenance. If verification empties the answer, refuse exactly as today.

## Non-goals

- Changing node-first ordering, tier semantics, retrieval defaults, or the golden set.
- Any runtime chunking/index-building (hard rule 2).
- Auto-promotion of chunks to nodes (human data op per the R1 ingestion contract).

## Implementation sketch

1. `tools/rag/15_build_chunk_index.py` (offline, run once): heading-based chunking of
   `backend/ml_assets/rag_index/source_md/**/*.md` per Amendment 03 §4; BM25 + mE5 + FAISS into
   `indexes/chunks_*`; write `provenance/node_to_md_map.json` from node `citation` fields; stamp
   chunk `covered_by_node` accordingly; extend `index_sha256.txt` pin.
2. `backend/app/application/chunk_fallback.py`: pure resolver — given a query, return top-k chunk
   sources (prefer uncovered chunks at equal rank). No LLM, no tier changes.
3. `qa_pipeline.py` no_sources branch: if `CHUNK_FALLBACK_ENABLED` and chunk sources exist →
   generation + verifier with chunk evidence + evidence-grounded label; else existing REFERRAL.
   One touch point, behind the flag.
4. `.env.example`: `CHUNK_FALLBACK_ENABLED=false` with one-line comment.
5. Audit: log GCF activations (query, chunk ids, verdict) in the existing local audit lane.

## Tests (new)

- Unit: chunker invariants (sizes, overlap, boilerplate drop, sha256 stable).
- Unit: `node_to_md_map` precision spot-check against hand-labeled sample (≥20 nodes).
- Integration: node-hit query NEVER queries the chunk index (flag on) — node-first proof.
- Integration: GCF-only fixture (MD-only content) → grounded answer + label; MD-only chemical
  content failing verification → T4 refusal (fail-closed preserved).
- Regression: golden replay 50/50 with flag on; full suite grows.

## Acceptance

Amendment 03 §5 gates, then E26 (`experiments/specs/E26_chunk_fallback_coverage_safety.spec.yaml`)
frozen and signed. Only after both may the flag default change, and only if E26 shows hazard
unchanged (0 fail-closed violations) with meaningful coverage lift.
