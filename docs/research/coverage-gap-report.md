# Coverage-Gap Report — 1,000 real farmer queries vs the corpus (C1)

**Date:** 2026-08-15 · **Evidence artifact:** `backend/ml_assets/rag_index/eval/coverage_gaps_v1.json`
(per-query records; reproduce with `uv run python ml_assets/rag_index/scripts/13_coverage_gap_analysis.py`
from `backend/`) · **Corpus:** 2,135 cleaned knowledge nodes (BARC/BARI/BRRI/DAE/CABI/DLS/DoF/…)

## Method

The REAL runtime retrievers (container wiring: BM25 + BGE-M3 dense + RRF k=20 +
dialect expansion) ran over **all 1,000** queries in `farmer_benchmark_1000.jsonl`
(real farmer questions; 8 parallel workers). Per query we recorded: hybrid
passage count, top-1 RRF weight, raw BM25 top-1 score, raw dense top-1 cosine,
and dialect-expansion matches. Bucketing by returned-passage count is a
**term-overlap proxy only** — relevance/answer quality is the golden set's job
(`golden_qa_v1.jsonl`, 100 judged queries).

## Results

| Signal | Value |
|---|---|
| Queries with ≥3 retrieved passages | **1,000 / 1,000 (100%)** |
| Queries with 0 passages | 0 (0.0%) |
| BM25 term overlap (non-empty top-1) | 997 / 1,000 (99.7%) |
| Dense top-1 cosine — median / p10 / min | **0.627 / 0.569 / 0.448** |
| BM25 top-1 raw score — median / min | 16.4 / 3.7 |
| Dense rescue (BM25 empty → dense found) | 3 queries |
| Dialect-expansion hits | 6 / 1,000 (0.6%) |

## Findings

### 1. Retrieval-layer coverage is complete on this benchmark
Every one of the 1,000 real farmer questions retrieves ≥3 passages with a
semantic floor of **0.448 cosine** (BGE-M3 query–passage similarity). The
corpus has term-level and semantic-level coverage for the questions real
farmers ask in this benchmark. This is a coverage statement — not relevance,
not answer quality (the golden set measures those).

### 2. The distribution floor is Romanized (Banglish) input
All 12 lowest-cosine queries and all 3 BM25-empty queries are **Romanized
Bengali**:

- `amar labu gase a ful thore na` (আমার লাউ গাছে ফুল ধরে না) — cosine 0.448
- `chad bagan korte koto khoroc hoy` (চাঁদ বাগান করতে কত খরচ হয়) — BM25 empty, dense 0.456
- `Patol ar poka Damon paddhati janty chay` — BM25 empty, dense 0.488
- `Drame lagano dalim gase dalim fol...` , `Bendi gash more jashe`, `lebu gaser pata kuchkano hoy keno???` …

The corpus is Bangla-script; the term map has little Banglish coverage, so
Romanized queries sit at the cosine floor and are the only queries BM25 misses.
**The dense channel rescues them** (all 3 BM25-empty cases found by hybrid),
but they remain the weakest retrievals in the distribution.

### 3. Dialect expansion is near-silent → FIXED by C3 (2026-08-15)
6 / 1,000 queries matched the expansion map (0.6% — consistent with
`hybrid_smoke.json`). The original 110-word real dialect map
(`dataset_release/safety/phase4_dialect_map.json`) was **not present in the
workspace or git history** (Q4). C3 rebuilt it honestly: a **16-pair map
derived deterministically** from the frozen, reviewed T09 treatment-QA splits
(1,440 cells; difflib 1:1 token replace alignment of dialect vs standard
variants of the same `cell_id`, flanking-context + frequency-2 + dominance
filters; zero LLM calls — no fabrication). Reproduce:
`uv run python ml_assets/rag_index/scripts/14_derive_dialect_map.py`.
**Verified lift on the real T09 dialect questions (dev+test, 3,628):**
**0.03% → 33.49% (1,215 hits; 165 barishal, 305 chittagonian, 250 noakhailli,
201 rangpuri, 294 sylheti).** Examples: `ক্ষেতত→ক্ষেতে`, `গাছত→গাছে`,
`অইলে→হলে`, `লাগি→জন্য`, `লাই→জন্য`, `প্রয়োগর→প্রয়োগের`, `সিডিউলটা→সময়সূচী`.
Scope: the map normalizes dialectal morphology to standard Bengali (helps the
dense BGE-M3 channel); it does not cover Banglish (Romanized) input.

### 4. Answerability is a separate layer (already measured)
Retrieval coverage ≠ answerability. The golden set measures the answer layer:
12/12 unanswerable queries are refused after the D1a coverage gate (before D1a:
0/12). Relevance judgments (scoring sheet) remain pending two evaluators.

## Honest limits

- Coverage ≠ relevance: ≥3 passages can still be off-topic; no recall claim is
  made from this artifact.
- The passage-count buckets (no_sources/thin/adequate) are degenerate here —
  BM25's 0.2×max threshold returns up to 5 passages whenever any term overlaps,
  so count buckets cannot discriminate quality. Raw channel scores are the
  discriminating signal and are recorded per query.
- Top-1 RRF weights are quantized (1/(20+rank)); every query's top doc scores
  0.0476 (rank-1 in exactly one channel), so RRF weight is not a quality signal
  either. Both-channel rank-1 agreement was never observed.
- Dense availability depends on the OpenRouter key; without it the hybrid runs
  BM25-only and the 3 Banglish-rescue queries return empty (fail-closed path).

## Recommendations

1. **C3 — DONE (2026-08-15):** the dialect map was unrecoverable (absent from
   workspace and git history); a 16-pair map was **derived** from the frozen
   reviewed T09 splits instead (`14_derive_dialect_map.py`), lifting expansion
   hits on real dialect questions from 0.03% to 33.49%. The original
   Gemini-generated 110-word map remains unrecoverable — if the researcher has
   a copy, it can be merged on top (schema-compatible, dict form).
2. **Banglish lane (scope-gated, future):** add a small Romanized→Bangla
   expansion map for the highest-frequency Banglish terms seen here
   (examples above); the dense channel already covers the long tail.
3. **Relevance:** the scoring sheet (`dataset_release/benchmark/scoring_sheet_v1.csv`)
   is the missing quality layer; fill it before any recall/quality claim.