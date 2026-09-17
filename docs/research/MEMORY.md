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
**HONEST FINDING — DoD unmet (fixed 2026-08-14):** unanswerable refusal rate
was **0/12 (0%)** (target ≥90%) — all 12 answered with 5 sources + "verified"
(loose retrieval neighbors + confident generation). Exposed by P4, then fixed:
**D1a deterministic corpus-coverage gate shipped** (`safety_policy.py`
`LOW_CONFIDENCE` pattern group, ordered LAST after self-harm/injection/banned;
6 keyword families: training incl. farmer typo `প্রশিক্ষন`, export,
availability, institutional, livestock incl. Banglish `koel palon`, government
assistance). Forced golden re-run (46/46 fresh): **unanswerable 12/12 refused,
off-topic 2/2, gate never fires on 0/32 answerable** (q75 banned refusal
unchanged); live probe + audit `safety_matched_rules`; 87/87 pytest (+9
coverage-gate tests), tsc + build green. Gate is keyword-scoped, not semantic
(unseen out-of-corpus intents unmeasured — documented F10/S17, demo wording
must stay scoped). Scoring pipeline shipped: `10_scoring_sheet.py` →
`scoring_sheet_v1.csv` (46 rows, full text) + `scoring_rubric_v1.md`;
`11_publish_golden_stats.py` → `golden_stats_v1.json` + copy in
`frontend/src/lib/golden_stats.json` (Cohen's kappa, per-category results,
validated refusal rate; emits honest `pending_scores` until both evaluators
fill the sheet). API: `GET /api/benchmark` serves the precomputed artifact
(replaced stub; never live-computed). Frontend: benchmark page Section G —
live-system golden eval (mechanical table, unanswerable-refusal callout now
DYNAMIC: green leaf state when rate ≥90%, clay warning otherwise, pending
banner, scored table when filled). Verified: 87/87 pytest (+1 benchmark
contract test), `tsc --noEmit` clean, `pnpm build` green, live probe of
`/api/benchmark` serving pending state.
**Open work:** 1) researcher + second evaluator fill `scoring_sheet_v1.csv`
→ rerun `11` → stats go live (kappa required for DoD); 2) Q1: Lumectin
refusal correctness (expert review pending); 3) Q4: restore
`dataset_release/safety/` dialect map to raise expansion hit rate.
**P5-polish (refusal-reason UI, done 2026-08-14):** QAResult/QAResponse now
carry `matched_rules` + `safety_reason`; `/api/safety/metrics` adds per-rule
`refusal_rules` breakdown; SafetyNotice shows Bengali reason chips (shared
`refusalRuleLabel` map — backend rule ids never reach farmers), analytics
pipeline card lists refusal reasons, chat passes matched_rules through.
Verified 87/87 pytest, tsc + build green, live probe (refused → coverage_training,
answered → empty).

**P5 VOICE (read-aloud TTS, done 2026-08-14):** Phase 1 TTS SHIPPED, user
approved the plan ("Go, but don't ruin other parts") — strictly additive.
Backend: `speech.py` (`POST /api/tts`, `GET /api/tts/voices`,
`POST /api/tts/prewarm`, `POST /api/transcribe`), edge-tts 7.2.8 (PyPI-verified
2026-03-22), real `bn-BD` voices (Nabanita/Pradeep Neural — the ROADMAP's
"no bn-BD locale" note applied to ElevenLabs/Google, NOT edge-tts), cache
sha256(voice|text) cap 256, retries ×3 (1s/2s), `app.state.settings` +
`SettingsDep` pattern (speech.py reads app-injected settings). Frontend:
`read-aloud.tsx` ReadAloudButton (Web Audio context resumed in click gesture;
fallback chain backend TTS → speechSynthesis → text + inline error),
`chat-message.tsx` swapped, `qa-panel.tsx` barge-in (`stopAllSpeech()` on send
and mic start; Web Speech mic ALREADY existed there). Verified: 102/102 pytest
(+15 mocked speech tests), pnpm build green, live probe (cold 200 @ 2.3 s
cache-miss, warm **41 ms cache-hit**, male voice 745 ms, prewarm 200,
transcribe 501 without key). **DoD <2 s only on cached audio → prewarm exact
demo answers 2–3 min ahead.** ASR: Groq endpoint ready but NOT wired to UI
(needs user free key; deferred, zero risk).
**CRITICAL probe lesson:** PowerShell 5.1 mangles Bengali in piped stdin AND
argv (OEM codepage → `?`). All earlier "in-process fails / CLI works" probe
results were encoding artifacts — clean UTF-8 on-disk probes show in-process
TTS works identically (both 26,928 B, ~1.3 s). Browser→server (JSON/UTF-8) is
unaffected. Use on-disk UTF-8 .py probes, never piped Bengali.
**Stale-server lesson:** an old reload-mode uvicorn (PID 13700) hot-reloaded
new code and owned port 8000; killed, fresh server now owns it (uvicorn
launcher shim 7508 → real child 17304). Docs updated: ROADMAP P5 STATUS,
findings log F11 (voice honest limits: unofficial keyless endpoint, upstream
rate-window flakiness #460, standard Bengali only, internet-dependent, typed
text always works). Commit pending.

**B1 DEMO ANSWER CACHE (done 2026-08-15):** exact-replay cache for the
curated demo questions — `DemoAnswerCache` (`backend/app/infrastructure/cache/demo.py`,
JSON file at `demo-assets/cached_responses.json`, key = normalized query +
crop/disease/model, cap 100, thread-safe, atomic tmp+replace writes,
best-effort persistence). Wired into `QAPipeline` as an OPTIONAL
`answer_cache` param (None = untouched behavior, existing tests unchanged);
container builds it only when `demo_mode`. Cache rules: only safe_agri results
with no generation error are stored; terminal refusals ALWAYS re-run safety;
corrupt entries degrade to miss and self-heal on the next live run. Replays:
re-emit the stored agent trace through the event channel (stepper animates
normally) and audit with `cached:true` — metrics count replays in totals +
category mix but exclude them from per-stage (retrieval/verifier/router)
aggregates. Prewarm script `backend/scripts/prewarm_demo_cache.py` runs the
REAL pipeline over the 7 curated demo questions (writes audit to a throwaway
temp file — demo metrics never polluted). Verified: 115/115 pytest (+13 new
cache tests), prewarm cached 3/7 (4 terminal correctly not cached), live
replay **47 ms** (vs 5.5 s live run) with intact sources/trace/verifier
stamps; audit row `cached:true`; metrics `cached.replays=1`.

**A1 QUERY REWRITING (done 2026-08-15):** follow-ups -> standalone retrieval
queries. `ConversationalQueryRewriter` (`backend/app/application/rewrite.py`):
heuristic gate (follow-up deixis markers + history non-empty) then one cheap
LLM call (same intent model) rewriting to a self-contained query; any failure
falls back to raw (fail-open retrieval, NEVER safety). Retrieval used the raw
query before (history only reached the generation prompt). Now: rewritten
query feeds `build_retrieval_query`; safety classifier STILL sees the raw
query; audit adds `retrieval_query_used` + `retrieval_query_rewritten`; trace
detail appends "· rewritten". Wired in container when `query_rewrite_enabled`
(default true; off-switch env). Single-turn questions never trigger a call —
cached demo lane untouched (verified: curated Q1 still 16 ms replay).
Verified: 127/127 pytest (+12 rewrite tests), live probe: turn1 9.5 s,
follow-up "তাহলে ইউরিয়া কতটুকু দেব?" -> rewritten query
"ধান চাষে ইউরিয়া সার কতটুকু দেব? rice fertilizer safe_agri", 5 sources,
grounded answer, audit rewritten=True.

**C1 COVERAGE-GAP MINING (done 2026-08-15):** ran the REAL runtime retrievers
(BM25 + BGE-M3 dense + RRF) over ALL 1,000 farmer_benchmark queries (script
`ml_assets/rag_index/scripts/13_coverage_gap_analysis.py`, artifact
`eval/coverage_gaps_v1.json`, 8 workers). Result: retrieval coverage is
COMPLETE — 100% ≥3 passages, BM25 overlap 99.7%, dense top-1 cosine median
0.627 / floor 0.448; dense rescued the 3 BM25-empty queries. **The
distribution floor is Romanized (Banglish) input** — all 12 weakest + all 3
BM25-empty queries are Banglish (corpus is Bangla-script; term map lacks
Banglish coverage; dense rescues them). Expansion hit rate 6/1000 (0.6% —
dialect map missing, C3). Method lessons: passage-count buckets are
degenerate (BM25 0.2×max threshold returns 5 whenever any term overlaps);
RRF weights quantized (top-1 always 0.0476, single channel). Report:
`docs/research/coverage-gap-report.md`. No recall/relevance claim — golden
set owns that (12/12 refused post-D1a; scoring sheet pending).

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
  Unanswerable refusal DoD ≥90% — **MET post-D1a: 12/12 (100%) on the pinned
  golden set**; gate is keyword-scoped (unseen intents unmeasured).
- P5: TTS read-aloud first (no bn-BD TTS locale — use bn-IN/other, state
  honestly); ASR optional (bn-BD via Google STT or local Whisper), same text
  pipeline, graceful fallback, standard Bengali only.
- B1: demo cache replays ONLY verified pipeline outputs (safe_agri, no error);
  cached replays are honest (audit rows + metrics split); never cache
  terminal refusals; cache key includes crop/disease/model.
- A1: rewriting is retrieval-only — safety classification always sees the raw
  surface query; rewrite fires only on follow-up markers with history
  (budget-free: zero cost for single-turn/cached questions).
- C1: retrieval coverage measured on ALL 1,000 farmer queries (not a sample);
  bucket counts are degenerate → raw channel scores are the evidence; never
  claim recall/relevance from coverage artifacts.
- **C3: NEVER fabricate the dialect map.** The original 110-word map was
  unrecoverable (workspace + git history) — derived a 16-pair REAL map from
  the frozen reviewed T09 splits instead (deterministic alignment, zero LLM).
  If the researcher's original copy resurfaces, merge it (dict-form,
  schema-compatible) and re-measure.
- Out of scope now: KG/GraphRAG, offline PWA, B2B layer, query routing,
  clarify-slots, 16123 integration (REJECTED), DPO alignment.

## Risks
Bengali NLI scarcity → rule-based first. RRF regression → BM25 fallback flag +
golden-set A/B. Demo-horizon: never claim hybrid/voice-dialect until live-verified.
Expansion coverage risk: term map is title-derived (0.6% hit rate) — **C3
FIXED (2026-08-15): derived 16-pair dialect map lifts expansion hits on real
T09 dialect questions from 0.03% to 33.49%**; Banglish (Romanized) input
remains the uncovered floor (dense rescues; scope-gated future lane).
**NEW (P4):** unanswerable queries got confident answers (0/12 refused) —
**FIXED by the D1a coverage gate (12/12 now)**; residual risk: unseen
out-of-corpus intents the keyword gate doesn't cover. Scoring churn risk
handled by pinned sample.

## Completed Milestones — Architecture Version 2.0 (2026-09-03)
- **E02 Multimodal Edge Perception & Hazard Elimination SHIPPED:**
  - 10-Class Primary Crop Classifier deployed (`yolo26s` base).
  - Chilli Disease Specialist deployed (`yolo26n-cls`, 8 classes, 5.91 MB ONNX INT8, 99.68% held-out test accuracy).
  - Calibrated Botanical Confusion Gate ($C_d \ge 0.85$, $M_d \ge 0.18$) halts Solanaceae cross-crop misclassification.
  - Replay on 436 field-image benchmark: **$0.00\%$ cross-crop toxic hazard** ($0/436$), $48.62\%$ direct safe automation, $97.94\%$ total containment.
  - Fail-closed Gate Disambiguation Cards implemented in frontend (`UncertainClarificationCard`, `SecondImageCard`, `OutOfDistributionCard`).
- **Agronomic & Field Usability Hardening SHIPPED:**
  - Integrated Pre-Harvest Interval (PHI: 7–14 days) and DAE Golden Spray Rules across UI and printable prescription slips.
  - De-mystified soil tensiometer kPa metrics into tactile 'Jo' condition states and field squeeze tests.
  - Added rural household matchbox powder benchmark (1 matchbox $\approx$ 10–12 g) in Dosage Calculator.
  - Both paper tracks (EACL Demo v2.0 and CEA Research v2.0) compiling with 0 LaTeX errors.

## Next Actions
1. **Researcher: fill `dataset_release/benchmark/scoring_sheet_v1.csv`** (2
   evaluators, per `scoring_rubric_v1.md`), then rerun `11_publish_golden_stats.py`.
2. Q1: expert review of the Lumectin refusal (`farmer_q_75`) correctness.
3. **Demo prep:** add the prewarm step to the demo script (run 2–3 min before
   demo; then curated questions replay at ~16–47 ms).
4. Optional: if the researcher finds the ORIGINAL 110-word
   `dataset_release/safety/phase4_dialect_map.json` (July dataset phase), drop
   it in place (dict form, schema-compatible) and re-measure the hit rate.
5. Menu next: **golden scoring sheet** (2 evaluators) — the only open
   quality layer. Optional future (scope-gated): Banglish→Bangla expansion
   map for the high-frequency Romanized terms found by C1.

## Key Files
`docs/competitive-landscape.md`, `docs/research/LITERATURE_SCOUT_2026.md`,
`docs/research/CRITIC_GAPS_2026.md`, `docs/research/ROADMAP_2026.md`,
`docs/research/SYSTEM_SYNTHESIS_V2.md`, `docs/research/competitive/`.
P4: `dataset_release/benchmark/{golden_qa_v1.jsonl, golden_runs_v1.json,
scoring_sheet_v1.csv, scoring_rubric_v1.md, golden_review_dump_v1.md,
golden_stats_v1.json}` + `frontend/src/lib/golden_stats.json`;
`backend/ml_assets/rag_index/scripts/08..11_*.py`; `backend/app/api/benchmark.py`.
Vision 2.0: `backend/app/domain/vision.py`, `backend/ml_assets/vision/`,
`frontend/src/lib/vision-ondevice.ts`, `frontend/src/components/detect/diagnosis-card.tsx`.