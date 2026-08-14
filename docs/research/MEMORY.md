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
workspace (never committed) and merges automatically when restored. Fix at
P4 with the golden set. Next: P4 (gold-label benchmark: 40–60 questions from
1,001 farmer queries, ≥10 unanswerables, reuses audit v2 fields), P5
(refusal-reason UI + panel polish).

## Key Decisions
- P1: rule-based dosage entailment (chemical/crop/number/unit vs passages),
  annotate-and-drop (never hard-block), TRUST-SCORE-style refusal counters.
- P2: /safety-metrics reads the actual JSONL audit log; stepper bound 1:1 to log.
- P3: dense index BUILT (BGE-M3 via OpenRouter, 2,135 nodes, FAISS FlatIP);
  RRF k=20/candidate_depth=50; BM25-only fallback flag; expansion surface in
  trace; smoke eval is coverage-only (no recall claims — P4 golden set adds
  relevance judgments).
- P4: golden set from 1,001 real farmer queries, ≥10 unanswerables, 2 human
  evaluators, precomputed panel stats.
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

## Next Actions
1. Get researcher approval on the Top-5 (or a subset).
2. P1 → P2 → P4 critical path; P3 index build in parallel.
3. Commit each phase per ROADMAP §F.

## Key Files
`docs/competitive-landscape.md`, `docs/research/LITERATURE_SCOUT_2026.md`,
`docs/research/CRITIC_GAPS_2026.md`, `docs/research/ROADMAP_2026.md`.