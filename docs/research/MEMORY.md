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
**P2 COMPLETE (2026-08-14):** Dual-view metrics shipped. Audit entries now
carry per-step validity evidence (`pipeline_version: 2`): router
(confidence/reason/matched_rules), retrieval (count/top-1 score/hit), verifier
(passed verdict) — the exact decisions the chat stepper animates. Metrics
endpoint aggregates only v2 entries (`pipeline_queries`) so legacy log rows
can't distort the panel; `/api/safety/metrics` now serves `router`
(blocked/refusal_rate), `retrieval` (answered/hit_rate/avg_top1/avg_sources),
`verifier` (pass_rate). Frontend: pipeline-stats section (3 stage cards:
Router/Retrieval/Verifier) + per-row step dots on the audit list. Test
pollution of the live demo log eliminated (test_api/test_soil now build
isolated apps with tmp audit paths — pre-existing quirk where contract tests
wrote paraquat/soil entries into the demo log). Verified: 66/66 pytest, tsc
clean, live probe (2 v2 entries, hit_rate 1.0, honest empty pass_rate when
no dosage claims). Next: P3 (dense/FAISS index build + RRF) — longest lead,
start as side-lane; then P4 (gold-label offline benchmark reusing audit v2
fields), P5 (refusal-reason UI + panel polish).

## Key Decisions
- P1: rule-based dosage entailment (chemical/crop/number/unit vs passages),
  annotate-and-drop (never hard-block), TRUST-SCORE-style refusal counters.
- P2: /safety-metrics reads the actual JSONL audit log; stepper bound 1:1 to log.
- P3: dense/FAISS index DOES NOT EXIST yet (BM25-only runtime) — must be built
  offline before any hybrid claim; RRF + 110-word dialect map expansion.
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

## Next Actions
1. Get researcher approval on the Top-5 (or a subset).
2. P1 → P2 → P4 critical path; P3 index build in parallel.
3. Commit each phase per ROADMAP §F.

## Key Files
`docs/competitive-landscape.md`, `docs/research/LITERATURE_SCOUT_2026.md`,
`docs/research/CRITIC_GAPS_2026.md`, `docs/research/ROADMAP_2026.md`.