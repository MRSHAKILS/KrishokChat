# Research Lane Memory — Product Improvement Roadmap 2026

## Project State
KrishokChat product lane (post-auth). Auth + premium saved-history SHIPPED and
pushed (commits 6290eef, af0659e). Next: execute the 5-phase improvement
roadmap (`docs/research/ROADMAP_2026.md`) before the investor demo.

## Completed Milestones (2026-08-14)
- Multi-agent research completed: 3 parallel lanes (industry → `docs/competitive-landscape.md`;
  literature → `docs/research/LITERATURE_SCOUT_2026.md`; engineering readiness — inline report).
- Adversarial review: `docs/research/CRITIC_GAPS_2026.md` — 19 candidates scored:
  13 ADOPT (scoped), 5 ADOPT-LATER, 1 REJECT (16123 front-end).
- Roadmap: `docs/research/ROADMAP_2026.md` — P1–P5 with dependency graph,
  effort, risks, out-of-scope, commit sequence. (Architect agent failed
  silently; roadmap written by orchestrator with the critic's evidence.)

## Active Phase
**P3 COMPLETE (2026-08-14):** Hybrid RRF retrieval + dialect expansion shipped.
Dense index built offline: 2,135 knowledge nodes → `embeddings.npy`
(2135×1024) via **BGE-M3 (`BAAI/bge-m3`) through OpenRouter** (user-supplied
key, `03_build_embeddings_api.py`; e5-small local download aborted by user —
repo prefers the OpenRouter path), `nodes.faiss` (IndexFlatIP, L2-normalized,
sha256 `0f6f711829db5bc7687046ee2483322cef877a2ced896cf624fd4eb6234cb524`),
`term_map.json` (134 corpus-title-derived bn→en pairs). Runtime:
`retrieval/nodes.py`, `expansion.py`, `dense.py`, `hybrid.py`; `bm25.py`
refactored with `candidates()` (threshold-free RRF input); `HybridRetriever`
RRF k=20 / candidate_depth=50, dedup by id, mode `hybrid`|`bm25`,
`last_expansion`; `RETRIEVAL_BM25_ONLY` flag; expansion surfaced in agent
trace ("· bn→en …"). Verified: 77/77 pytest (11 new in `tests/test_retrieval.py`;
fixture lesson — tiny corpora give query tokens df≥N/2 → idf 0 → all-BM25
scores 0; fixtures need df=1), live probe shows RRF fusion score
(`retrieval_top1_score 0.0476` = 1/21, hit, v2 audit), smoke eval in
`ml_assets/rag_index/eval/hybrid_smoke.json` (100 of 1,000 farmer queries:
BM25 non-empty 0.99 → hybrid 1.00, dense active 100%).
**Known limitation (honest):** expansion hit rate 0.6% (6/1,000 queries) —
title-derived term map is narrow; the 110-word real dialect map
(`dataset_release/safety/phase4_dialect_map.json`) is MISSING from the
workspace (never committed) and merges automatically when restored.

**P4 IN PROGRESS (2026-08-14, commit `684886b`):** golden benchmark shipped.
Golden set pinned & fully reviewed: `dataset_release/benchmark/golden_qa_v1.jsonl`
— 46 rows from the 1,001 real farmer queries (pinned sample + 21 overrides;
`08_build_golden_set.py`): dosage 10, timing 10, pest_disease 10, general 2,
off_topic 2, unanswerable 12. Every row human-reviewed (3 passes; Bengali
regex traps: `গান`⊂"লাগানো", `ভর্তি`⊂"ধান ভর্তি", `কবে`⊂"থাকবে",
`মাত্রা`⊂"তাপমাত্রা", `পরিমাণ`⊂"পর্যাপ্ত পরিমাণ" → boundary patterns).
Real-pipeline runs (`09_run_golden_eval.py`) on all 46: 45 answered, 1 refused
(farmer_q_75 — Lumectin dose, safety-classified `banned_or_restricted_chemical`,
a policy catch to review); verifier flagged 6 of 45 as unsupported.
**HONEST FINDING — DoD unmet:** unanswerable refusal rate is **0/12 (0%)**
(target ≥90%); all 12 answered with 5 sources + "verified" (loose retrieval
neighbors + confident generation). Exposed by P4, not fixed yet — next step
is a low-confidence referral rule (retrieval top1 score / verifier gate)
before the demo. Scoring pipeline shipped: `10_scoring_sheet.py` →
`scoring_sheet_v1.csv` (46 rows, full text) + `scoring_rubric_v1.md`;
`11_publish_golden_stats.py` → `golden_stats_v1.json` + copy in
`frontend/src/lib/golden_stats.json` (Cohen's kappa, per-category results,
validated refusal rate; emits honest `pending_scores` until both evaluators
fill the sheet). API: `GET /api/benchmark` serves the precomputed artifact
(replaced stub; never live-computed). Frontend: benchmark page Section G —
live-system golden eval (mechanical table, unanswerable-refusal callout,
pending banner, scored table when filled). Verified: 78/78 pytest (+1
benchmark contract test), `tsc --noEmit` clean, `pnpm build` green, live
probe of `/api/benchmark` serving pending state.
**Open work:** 1) researcher + second evaluator fill `scoring_sheet_v1.csv`
→ rerun `11` → stats go live (kappa required for DoD); 2) the 0% refusal
finding needs a pipeline fix decision; 3) P5 (refusal-reason UI + panel polish).

## Key Decisions
- P1: rule-based dosage entailment (chemical/crop/number/unit vs passages),
  annotate-and-drop (never hard-block), TRUST-SCORE-style refusal counters.
- P2: /safety-metrics reads the actual JSONL audit log; stepper bound 1:1 to log.
- P3: dense index BUILT (BGE-M3 via OpenRouter, 2,135 nodes, FAISS FlatIP);
  RRF k=20/candidate_depth=50; BM25-only fallback flag; expansion surface in
  trace; smoke eval is coverage-only (no recall claims — P4 golden set adds
  relevance judgments).
- P4: golden set from 1,001 real farmer queries, ≥10 unanswerables, 2 human
  evaluators, precomputed panel stats. Sample PINNED (override changes never
  re-sample — golden set is a fixed reviewed artifact, not a generator).
  Unanswerable refusal DoD ≥90% — currently 0%, exposed, fix pending.
- P5: TTS read-aloud first (no bn-BD TTS locale — use bn-IN/other, state
  honestly); ASR optional (bn-BD via Google STT or local Whisper), same text
  pipeline, graceful fallback, standard Bengali only.
- Out of scope now: KG/GraphRAG, offline PWA, B2B layer, query routing,
  clarify-slots, 16123 integration (REJECTED), DPO alignment.

## Risks
Bengali NLI scarcity → rule-based first. RRF regression → BM25 fallback flag +
golden-set A/B. Demo-horizon: never claim hybrid/voice-dialect until live-verified.
Expansion coverage risk: term map is title-derived (0.6% hit rate) — restore
`dataset_release/safety/phase4_dialect_map.json` (110-word real map) to raise it.
**NEW (P4):** unanswerable queries get confident answers (0/12 refused) —
unsupported-content risk at demo; low-confidence referral rule needed before
the demo. Scoring churn risk handled by pinned sample.

## Next Actions
1. **Researcher: fill `dataset_release/benchmark/scoring_sheet_v1.csv`** (2
   evaluators, per `scoring_rubric_v1.md`), then rerun `11_publish_golden_stats.py`.
2. Decide the unanswerable-refusal fix (low retrieval-top1-score referral
   rule vs verifier gate) and implement before the demo.
3. P5 (refusal-reason UI + panel polish) after scores land.

## Key Files
`docs/competitive-landscape.md`, `docs/research/LITERATURE_SCOUT_2026.md`,
`docs/research/CRITIC_GAPS_2026.md`, `docs/research/ROADMAP_2026.md`.
P4: `dataset_release/benchmark/{golden_qa_v1.jsonl, golden_runs_v1.json,
scoring_sheet_v1.csv, scoring_rubric_v1.md, golden_review_dump_v1.md,
golden_stats_v1.json}` + `frontend/src/lib/golden_stats.json`;
`backend/ml_assets/rag_index/scripts/08..11_*.py`; `backend/app/api/benchmark.py`.