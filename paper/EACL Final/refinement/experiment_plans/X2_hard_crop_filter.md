# X2 — Hard crop filter on retrieved evidence + N08 re-run

**Priority 2 · 45 min · $0 · code change + deterministic re-run**

## Why this adds value
The N08b audit (`experiments/N08_fence_study/results_residual_audit.json`) showed that the 30%
residual cross-crop retrieval under gold-crop binding comes from **12 single-crop passages**
about other crops (none multi-crop), because the bound crop only enters the query text and
nothing filters candidates. A post-retrieval crop filter should remove almost all of it. This
turns the weakest headline number (36.25% → 30.0%) into a strong one, **if** relevant evidence
is preserved, which this plan measures with an independent check.

## Code facts (verified)
- Deployment builds a `HybridRetriever` (BM25 + dense), `backend/app/application/container.py` lines 90–107.
- The pipeline calls `self.retriever.retrieve(retrieval_query, top_k=self.top_k)` at
  `backend/app/application/qa_pipeline.py` line ~571. `effective_crop` is computed at line ~197.
- `BM25Retriever.retrieve` (`infrastructure/retrieval/bm25.py`) has **no crop argument**; it keeps
  the top `2*top_k` above `0.2 × max score`.
- Passages carry no crop field; crops are inferred from text with `_CROP_ALIASES`
  (`app/domain/intent.py`), the same rule used by the N01/N08 metric.

## Part A — implement the filter (retriever-agnostic)
1. New function in `backend/app/domain/crop_scope.py`:
   ```python
   def passage_crops(source) -> frozenset[str]   # same alias logic as source_crops() in N01
   def filter_by_crop(sources, crop, top_k) -> list[RetrievedSource]:
       # keep a source if its crop set is empty (crop-neutral, e.g. soil/general) OR contains `crop`
       # preserve original order; return the first top_k kept
   ```
   Cache `passage_crops` by source id (`functools.lru_cache` on id+text hash).
2. In `qa_pipeline.py` at the retrieve call: when `effective_crop` is set **and** env flag
   `RETRIEVAL_CROP_FILTER` is not `"0"`, call `retrieve(..., top_k=self.top_k * 4)` and then
   `filter_by_crop(retrieved, effective_crop, self.top_k)`. Otherwise unchanged.
   Emit a trace event `crop_filter` with `{crop, removed_n}` so the Why panel can show it.
3. Map crop ids consistently: `effective_crop` values and `_CROP_ALIASES` keys must match
   (check `rice/potato/brinjal/chilli/tomato/wheat/maize`; PRISM uses these ids).
4. Tests: add `backend/tests/rag_pipeline/test_crop_filter.py` (neutral passage kept; other-crop
   passage dropped; order preserved; flag off = old behaviour). Run the full backend suite
   (`pytest backend/tests -q -m "not live_llm"`); it must stay green.

## Part B — re-run N08 with three arms
Script: `experiments/N08_fence_study/scripts/run_n08c_filter.py` (copy the header, `build_query`
and `source_crops` from `audit_n08_residual.py`; PRISM from git history, see README).
For each of the 400 PRISM B/C/D/I rows:
- **open**: `retrieve(q_open, top_k=5)`
- **bound** (= frozen N08 fenced arm): `retrieve(q_fenced, top_k=5)`
- **bound+filter**: `filter_by_crop(retrieve(q_fenced, top_k=20), gold, 5)`

Metrics per arm (separate lists; do **not** copy the `open_pure = fenced_pure = []` bug):
1. Cross-crop rate (N08 definition): any top-5 passage whose crop set is non-empty and excludes gold.
2. **Coverage**: share of queries with ≥ 1 returned passage; mean passages returned.
3. **Independent relevance check (not crop-based):** disease hit@5 = any returned passage
   contains the gold disease string (`true_disease_if_known`, Bengali; also try its English
   alias via `ConceptNormalizer` if available). Only rows with a non-null disease count.
4. Gold-crop purity = passages naming gold only / passages with a known crop.
5. Paired McNemar bound vs bound+filter on cross-crop (exact, from `run_n01_blind_arm.mcnemar_exact`).
6. **Manual spot check (independent):** randomly sample 30 bound+filter queries (seed 42), print
   query + top-5 titles to `n08c_spotcheck.md`; a team member marks each top-5 as
   "on-crop or general / other crop". Report k/30. This avoids scoring the filter only with its own rule.

Sanity: the bound arm must reproduce 120 (frozen) or 121 (current code; extra `PRISM_C_005`) flagged queries.

Output: `experiments/N08_fence_study/results_n08c_filter.json` + `n08c_spotcheck.md`.

## Decision rules and paper updates
Let `X` = bound+filter cross-crop rate, `C` = coverage, `H0/H1` = disease hit@5 bound vs bound+filter.

**Use as headline if** `X` ≤ 5%, `C` ≥ 95%, and `H1` ≥ `H0` − 2 pp:
- **Abstract**: "Binding the crop lowered top-five cross-crop retrieval from 36.25\% to 30.0\% on 400 stress queries" →
  "Binding the crop and filtering candidates by crop lowered top-five cross-crop retrieval from 36.25\% to {X}\% on 400 stress queries without losing relevant passages".
- **§3.2 (`sec:system_retrieval`)**: replace the sentence "This scoping narrows the evidence but does not exclude other crops: …" with
  "After retrieval, passages that name only other crops are removed; crop-neutral passages such as soil guidance are kept."
- **§5.2 (`sec:eval-fence`)**: keep the 36.25 → 30.0 result as the query-binding step; replace the audit paragraph with
  "An audit traced the remaining 30\% to 12 generic passages about other crops. Filtering candidates by crop lowers the rate to {X}\% ({k}/400), keeps at least one passage for {C}\% of queries, and leaves disease hit@5 at {H1}\% (vs {H0}\%); in a manual check, {m}/30 filtered result lists contained no other-crop passage."
- **Table 1**: `Crop binding (C2) & 400 stress & cross-crop 36.25\% $\rightarrow$ {X}\%`.
- **Limitations**: delete "and crop binding leaves 30\% cross-crop retrieval even with the correct crop, almost all from 12 generic passages".
- **App. E `tab:evidence_a`**: new row "Crop filter | cross-crop {X}\%; coverage {C}\%; disease hit@5 {H0}→{H1}\%; manual {m}/30 | 400 | Measured | Gold crop bound (simulated routing); filter uses text crop mentions".
- **Screencast/demo**: nothing to re-record; the Why panel may show the new `crop_filter` event.

**If coverage or hit@5 drops beyond the thresholds:** keep the current paper text; add one
App. E row with the trade-off numbers and the sentence "A strict crop filter removes the
residual but drops {100−C}\% of queries to no evidence; we keep query-level binding in the release."
Set `RETRIEVAL_CROP_FILTER=0` as default.

## Commit
Code (`crop_scope.py`, pipeline change, test), script, results, spot-check file. Note the
flag and its default in the commit message.
