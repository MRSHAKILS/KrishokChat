# Amendment 03 — Grounded Chunk Fallback (nodes first, raw MD chunks as gated evidence before refusal)

**Date:** 2026-08-27
**Status:** APPROVED — 2026-08-27 (author go-ahead); R13 implemented same day (see §7 record)
**Tier:** architecture refinement (R-series continuation), additive and flag-gated
**Depends on:** R1 (ingestion contract), R3 (tier plumbing), R4 (flag pattern), R9 (offline pack precedent)
**Blocks:** R13 task execution; experiment E26
**Precedent:** 01_PRIVACY_GOVERNANCE_2026_08_21, 02_ADMIN_TIERS_BROADCAST_AMENDMENT_2026_08_22

## 1. Decision being requested

Today, a safe-agri query whose node retrieval returns zero usable sources gets **one retrieval
attempt over the 2,135-node JSON index and then an honest refusal (T4)** (`qa_pipeline.py` no_sources
path). Meanwhile 2,946 institution-tagged processed markdown documents sit in
`backend/ml_assets/rag_index/source_md/` as reference-only — never indexed.

Proposal: add a **Grounded Chunk Fallback (GCF)** — a second, strictly subordinate evidence source
built from offline-chunked versions of those MDs. Order of resolution is unchanged and non-negotiable:

```
nodes first (T1/T2 deterministic → T3 node-grounded generation)
  → zero usable node sources?
      → YES: chunk fallback retrieval → generation → SAME 11-slot verifier → T3 (evidence-grounded label)
                                      → unverifiable/empty → T4 refusal (terminal, fail-closed, unchanged)
```

Nothing about the node path changes; GCF only executes on the branch that today produces refusal.

## 2. Why (and the honest safety answer on MD vs JSON)

JSON nodes are **safer by construction**: schema-enforced, slot-verifiable, deterministically
routable. Raw MD chunks are not — no schema, mixed quality, institution style variance. So chunks
must never be treated as answers. They are safe **only as evidence** passed to the existing
generation→verifier path, where chemical dosage/PHI claims must be grounded in the chunk text itself
or be stripped/refused. Under that constraint GCF converts a subset of today's blanket refusals into
*verifiably grounded, provenance-labeled* answers — coverage wins without weakening fail-closed
behavior. Chunks are also **provenance-carrying** (institution folder + document + heading) and the
`manifest_md_to_qa.json` already maps MD paths to QA refs.

## 3. Design constraints (all binding)

1. **Node-first guarantee:** GCF triggers only on the existing zero-source branch. A test must prove
   node-hit queries never touch the chunk index (with the flag on).
2. **Offline index only (hard rule 2):** chunking + BM25/FAISS build runs once via a build script
   (same pattern as `tools/rag/02/03/06`); runtime loads from disk. No live index-building.
3. **Flag-gated, default off:** `CHUNK_FALLBACK_ENABLED=false` in `.env.example`; rollout mirrors
   R4's structured-resolver pattern. Demo path unaffected when off.
4. **Same stack (hard rule 6):** BM25Okapi + mE5-small embeddings + FAISS — already locked; no new
   services (hard rule 3).
5. **Verifier is the gate, not the chunk:** chunk-sourced answers pass the identical verifier;
   unverifiable chemical content → strip → empty ⇒ T4. T4 remains the terminal state.
6. **UI labeling:** answers sourced from chunks carry an "evidence-grounded: <institution> <doc>"
   badge, distinct from node provenance badges (R11).
7. **Audit:** every GCF activation logs query, chunk ids, verifier verdict locally (existing audit
   lane). Never external (prototype rule).
8. **Node→MD coverage map (the "don't waste" mechanism):** an offline build derives node→MD-file
   mappings from node `citation` fields (institution + document + `section_title`). Two uses:
   (a) prefer/mark **uncovered chunks** (not mapped to any node) during fallback, so fallback
   targets genuinely new knowledge; (b) **promotion loop** — GCF hit logs rank uncovered chunks by
   demand; the top ones become the prioritized authoring queue for certified nodes (E24 growth
   loop). When a chunk is later promoted to a node, the query resolves node-first automatically and
   the chunk demotes itself — zero wasted work, fully dynamic.

## 4. Chunking policy (first version, deliberately simple)

- Chunk by markdown heading sections; target ~512 tokens, 15% overlap; drop boilerplate (TOCs,
  repeated headers) and chunks under ~40 tokens.
- Each chunk record: `{chunk_id, md_path, institution, doc_title, heading_path, text, sha256,
  covered_by_node: [node_ids] | []}`.
- Indexes: `indexes/chunks_bm25.pkl`, `chunks.faiss`, `chunk_ids.json` + `index_sha256.txt` pin
  (mirroring the node index manifest contract).

## 5. Acceptance gates (must all hold before the flag may default on)

- Full suite green (baseline 410 passed / 7 skipped / 0 failed grows, never shrinks).
- Golden replay **50/50 unchanged with `CHUNK_FALLBACK_ENABLED=true`** (node-first proof).
- New tests: GCF-only fixtures (content present in MD but absent from nodes) resolve with
  provenance label; chemical content failing verification still refuses.
- E26 experiment frozen and accepted per `experiments/ACCEPTANCE_PROTOCOL.md`.

## 6. Explicitly out of scope

- No change to T0–T4 definitions or `tier_for()` semantics.
- No change to the node index, retrieval defaults, or golden set.
- No runtime authoring/promotion — promotion is a human data op under the R1 ingestion contract.

## 7. Implementation record (2026-08-27, R13)

Shipped (branch working tree, default-off dark launch):
- `tools/rag/15_build_chunk_index.py` — offline builder: 4,815 chunks from the 2,946
  source_md sections; BM25Okapi (k1=2.2, b=0.4, `lower().split()` matching the runtime
  tokenizer); precision-first node→MD map (`provenance/node_to_md_map.json`):
  **1,713/2,120 nodes mapped (81%), 1,042 MD files covered**, method + sample in map meta.
- `backend/app/application/chunk_fallback.py` — read-only resolver; lazy load, thread-safe,
  sha256 pin + sampled-slice integrity gate (any drift → fallback silently unavailable,
  never a crash, never drifted evidence).
- `backend/app/application/qa_pipeline.py` — one gated touch point inside the retrieval
  stage: consulted only when node retrieval AND seed sources are both empty (the branch
  that today REFUSES). Node-first is structurally guaranteed and test-proven.
- `backend/app/core/config.py` + `container.py` + root `.env.example` —
  `CHUNK_FALLBACK_ENABLED=false` default, `CHUNK_FALLBACK_TOP_K=4`.

Accepted v1 deviations from §3/§4 (all conservative):
- No sliding-window overlap — chunks are exact paragraph-boundary file slices so runtime
  reconstruction + sha256 verification stay exact (corpus is already pre-split per section).
- BM25-only channel for v1, consistent with the BM25-only evaluated-runtime claim; a dense
  chunk channel can be added later as a data op.
- Separate `indexes/chunks_sha256.txt` pin instead of extending the node `index_sha256.txt`
  (the R2 corpus pin is never touched).

Gates evidence:
- New suite `backend/tests/test_chunk_fallback.py`: **17/17 passed** (chunker exact-substring
  invariants, tamper fail-closed, node-first, flag-off byte-identical REFERRAL, fallback-hit
  T3 flow-through, fallback-miss still refuses, seed-sources preempt).
- Full backend suite: **559 passed / 7 skipped / 0 new failures** (5 `scripts/test_live_e2e.py`
  failures are pre-existing environmental — they require a live server and fail identically
  with the change stashed).
- Golden replay with `CHUNK_FALLBACK_ENABLED=true`: **50/50 replayed, 0 errors, invariants
  PASS** (16/16 unanswerable refused, 6/6 flag-worthy flagged).
- Flag remains default OFF; flipping the default additionally requires E26 frozen and
  accepted (§5), which is the next step in `experiments/registry.yaml`.
