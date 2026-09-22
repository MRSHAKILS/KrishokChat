# X5 — Knowledge update without retraining (leave-one-out, frozen generator)

**Priority 5 · 45 min · $0 (plus ~1 min of local generation, optional)**

## Why this adds value
The paper claims that agricultural knowledge "can be revised without retraining the
generator", but shows no example (reviewer E55; experiment_suggestions **L**). A small,
reproducible update gives this claim concrete evidence and a nice demo moment, at no risk:
it cannot produce a negative headline.

## Design: leave-one-out, so no guidance is invented
Use **real curated passages** only. For each of 10 target passages:
1. **Before**: build an isolated index copy with the passage **removed**; run its query.
2. **After**: add the passage back (the "update"), rebuild the copy; run the same query.
3. Keep generator weights untouched; record their SHA-256 before and after.

## Facts (verified)
- Corpus: `backend/ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl` (2,135 nodes; field `bm25_text`).
- Index: `backend/ml_assets/rag_index/indexes/bm25_index.pkl`, a pickled dict with a `BM25Okapi`
  built on `bm25_text.lower().split()` (same as `BM25Retriever._tokenize`).
- `backend/scripts/merge_and_rebuild_index.py` rebuilds BM25 **in place** and hard-codes the
  old path `D:\KrishokChat Advisory System\backend`. **Do not run it.** Reuse only its
  `rebuild_bm25` logic inside an isolated temp directory.
- `knowledge_nodes_refined.jsonl` has no nodes outside the clean set, so there is no held-out real passage; hence leave-one-out.

## Steps
1. Folder `experiments/X5_evidence_update/` with `README.md`, `scripts/run_x5.py`, `results/`.
2. **Equivalence check first:** rebuild the index from the unchanged corpus into
   `tmp/x5_index_full.pkl`; for the 400 PRISM B/C/D/I queries (see README for restoring PRISM),
   top-5 ids must equal those from the frozen index. Abort if not identical.
3. Choose 10 targets with a fixed rule (seed 42): passages that (a) contain a dose pattern,
   (b) name one of the six supported crops, (c) are the **rank-1** result for a PRISM query of
   the same crop with the full index. Record query id and node id.
4. For each target: build `index_minus_i` (corpus without node *i*), run the query → record
   rank of node *i* (absent) and top-5 ids; then use the full index ("after") → record rank.
5. Record: `llm_weights_sha256` of the local GGUF (`krishokchat-4b`) before and after (path from
   the Ollama/llama.cpp config on the machine); index SHA-256 before/after; wall-clock rebuild time.
6. **Optional, 10 × 2 local calls (~8 min):** run the full pipeline with `krishokchat-4b` for 3 of
   the targets before and after; save both answers and their citations. Otherwise use the
   StubLLM pipeline from `tests/e2e/test_smoke_qa_pipeline.py` to show citation changes only.
7. Output `results/x5_update_<date>.json`: per target `{query_id, node_id, rank_before (None), rank_after, cited_after}`,
   rebuild time, hashes.

## Expected result
10/10 targets absent before and rank-1 after, generator hash unchanged, rebuild in seconds.

## Paper updates
**If 10/10 (or ≥ 9/10):**
- **§3.2 (`sec:system_retrieval`)**, end of the first paragraph: add
  "Adding a passage only requires rebuilding the index; in a leave-one-out test, {k} of 10 withheld guideline passages were retrieved at rank 1 after re-insertion, with the generator weights unchanged (Appendix~\ref{app:deployment})."
  If page 6 has no room, put the sentence only in App. B.
- **App. B**: new subsection "Knowledge Update" with the numbers, rebuild time, and hashes.
- **App. E `tab:evidence_b`**: row "Knowledge update | {k}/10 withheld passages rank 1 after re-insertion; LLM hash unchanged; rebuild {t}\,s | 10 | Measured | Leave-one-out on real passages; not new-crop support".
- **Limitations**: keep "adding a crop also needs a classifier, aliases, and policy rules" (still true).

**If fewer than 9/10:** report in App. B only, with the ranks, and do not add the §3.2 sentence.
