# R-Series Execution Index — Architecture Refinement Roadmap

**Status:** R1–R12 DONE (2026-08-25/26). R13 DONE (2026-08-27, Amendment 03 — grounded chunk fallback, dark-launched flag default-off pending E26).
**Date:** 2026-08-25 (updated 2026-08-27)
**Owner:** researcher (sole engineer); implementation by coder agents, one task at a time.

This is the **single entry point** for the architecture-refinement work. It says
what to execute, in what order, what external inputs each step needs, and how the
two tracks (innovation fair vs journal paper) diverge. Every row links to a
standalone task spec in this folder written in the same format as the completed
`T0-*` / `F1-*` / `PR1` / `P1_P2` tasks.

- **The why + the shape:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md`
- **What to build (menu + spine):** `production/future_plan/00_SCOPE_OUTLINE.md`
- **Weather data routes:** `production/future_plan/08_WEATHER_DATA_SOURCING.md`
- **Paper plan:** `paper/manuscript/README.md` (Wiley Expert Systems, locked)

---

## 1. The core idea (one paragraph)

Move from "every question → safety → retrieve → LLM generate → verify" to a
**five-tier resolution ladder**: answer deterministically from a
provenance-carrying fact base when we can prove the answer (T0 guard, T1 fact,
T2 templated), and use the LLM only to phrase or when nothing deterministic
applies (T3), else refuse honestly (T4). Doses are **composed from cited table
rows, never generated**. The measurable payoff is "% of queries served with zero
LLM calls" — the funder slide, the paper result (claim N6), and the ops KPI, all
one number.

---

## 2. Execution sequence (do these in order)

| # | Task spec | Delivers | Depends on | Status |
|---|---|---|---|---|
| 1 | `R3_resolution_tier_plumbing.md` | records how each answer was produced; **zero behavior change** | — | ✅ DONE — 2026-08-25 |
| 2 | `R1_knowledge_ingestion_contract.md` | "adding data = data op, not code" — tested + enforced | — | ✅ DONE — 2026-08-25 |
| 3 | `R2_fact_base_v1.md` | potato late-blight fact rows with provenance + build-time dose validation | R1, R3 | ✅ DONE — 2026-08-25 |
| 4 | `R4_structured_resolver.md` | T1/T2 answers, 0 LLM, behind a default-off flag | R2, R3 | ✅ DONE — 2026-08-25 |
| ∥ | `R8_real_weather_snapshot.md` | real RIMES weather → drops PR1 `is_sample` | — (parallel) | ✅ DONE — 2026-08-25 |
| 5 | `R5_merge_safety_intent.md` | one structured call instead of two; produces the routing `Intent` | R3 | ✅ DONE — 2026-08-25 |
| 6 | `R6_capability_registry.md` | seam for irrigation/drone/market modules + honest capability map | R5 | ✅ DONE — 2026-08-25 |
| 7 | `R7_cost_tier_mix_experiment.md` | price table + measured cost/1000 queries + p95 latency + zero-LLM rate | R4 | ✅ DONE — 2026-08-25 |
| 8 | `R9_offline_fact_pack.md` | works with no signal; tier ≤ 2 cached, T3 never | R4 | ✅ DONE — 2026-08-25 |
| 9 | `R10_ondevice_classifier_export.md` | mobile diagnosis latency claim (U1) + confidence-gated upload (U3) | R9 | ✅ DONE — 2026-08-26 |
| 10 | `R11_task_first_home_provenance.md` | task-first home + system-wide provenance badges | R3, R9 | ✅ DONE — 2026-08-26 |
| 11 | `R12_extend_fact_base_maize_rice.md` | proves "data op not rewrite" (maize FAW + rice pests) | R4 | ✅ DONE — 2026-08-25 |
| 12 | `R13_grounded_chunk_fallback.md` | nodes-first MD-chunk evidence fallback before T4 refusal; feeds E26 + the node-authoring queue | R1, R3, R4; **Amendment 03** | ✅ DONE — 2026-08-27 (dark launch, flag default-off; 4,815 chunks, 1,713/2,120 node map, golden replay 50/50 with flag on) |

**All 13 R-series tasks are DONE** (R13 under Amendment 03, APPROVED 2026-08-27;
implementation record in the amendment §7). Each spec is independently
executable by a fresh agent: it names exact file/line anchors, a stop/go gate,
invariants, and a rollback. **Next step for R13:** run experiment E26
(`experiments/specs/E26_chunk_fallback_coverage_safety.spec.yaml`) before the
flag may default ON.

**Suggested first sprint:** R3 → R1 → R2 → R4, with R8 in parallel (no deps).
R3 first because it is pure instrumentation and lands with no behavior change,
making everything after it measurable.

**Dependency graph (for parallel dispatch):**
```
R3 ─┬─► R2 ─► R4 ─┬─► R7
    │             ├─► R9 ─► R10
    ├─► R5 ─► R6  └─► R12
    └─────────────► R11 ◄── R9
R1 ─► R2
R8  (independent — start anytime)
```
Parallel-safe once R3+R1 land: R2 and R5 can run concurrently; after R4, then
R7/R9/R12 are mutually independent. R8 has no dependency at all.

**Rule between tasks:** one task, one coder agent, one branch. Each must pass its
own stop/go gate AND the standing baseline (full suite **410 passed / 7 skipped /
0 failed**, golden replay **50/50**, `pnpm build` green) before the next starts.

---

## 3. External inputs needed (and when)

| Need | For | Type | Have it? |
|---|---|---|---|
| OpenRouter key (`gemini-2.5-flash-lite`) | current pipeline, R5 | API key | ✅ configured |
| Groq key (`whisper-large-v3-turbo`) | existing ASR | API key | ✅ configured |
| RIMES upazila API `api.bdservers.site` | R8 | public API, no key (HTTP-only, offline fetch) | verify at R8 |
| BBS ADM3 P-codes for potato districts | R8 | one-time lookup | need lookup |
| DAE/PPW registered-pesticide list, BAMIS disease-weather calendars | R12 | public PDFs/HTML (offline ingest) | need download |
| BMD AIS observations (non-commercial) | paper rule-validation only | data, license-flagged | optional |
| Formal DAE Agromet / BMD data request | funding narrative | institutional letter (slow) | start early |
| **2 Bengali agronomy annotators + 1 adjudicator** | **paper Stages A–C** | **people, not code** | **recruit now** |

No new database engine, no message queue, no container orchestration — all
knowledge stays file/artifact-based (AGENTS.md rules 2 & 3).

---

## 4. Safety guardrails every task inherits (do not re-litigate)

- **T0 safety runs first, always.** No tier or resolver may bypass the safety
  precheck/classifier. (`07_...PLAN.md` Part B invariant.)
- **No fabricated data.** A missing dose/row/weather value is absent, not
  invented (AGENTS.md rule 5; the soil-honesty incident in PROJECT_HANDOFF).
- **No live scraping / index building at request time.** Offline scripts →
  versioned artifacts → fail-open loaders (rule 2).
- **A bad dose fails the build, not a request** (R2 build-time validation).
- **Anonymous/DEMO path stays byte-identical.** New features are additive and
  default-off or optional (rule 1). Regression-locked by the golden replay.
- **Every answer carries `resolution_tier` + provenance** into API, audit, UI
  (R3).
- **No published cost number without its measured tier mix** (R7 / plan E.2).
- **Deprecated arXiv v1 (`2606.29243`) is never cited** anywhere (rule 9,
  `docs/PAPER_POLICY.md`, CI gate).

---

## 5. What we get at the end

- Common, high-risk questions (doses/timing) answered in **milliseconds,
  offline, 0 LLM calls, correct by construction**.
- A **measured** zero-LLM rate → funding slide + paper claim N6.
- Knowledge scales by adding data files → the government-funding pitch is real,
  not aspirational.
- New capabilities plug into a registry without pipeline surgery.
- An honest weather-driven late-blight alert running on real forecast data.

---

## 6. Two tracks — they share a spine, then diverge

The tracks are **not** the same deliverable. Do not force every feature into the
paper; do not gate the fair on annotation.

**Shared spine (both tracks need these):** R2 fact base + R4 resolver + R7
measured tier mix — this is the demonstrable, publishable core.

### Track A — Innovation fair (product + further funding)
Favors **breadth and visibility**: R3 → R4 → R8 → R9 → R11. The story is
"offline, instant, safe, provenance-badged, not just a chatbot wrapper." Ship the
capability registry stub (R6) so drone/irrigation/market read as a roadmap, not
vapor. Metrics to show live: zero-LLM rate, p95 latency, dose-correctness,
safety category breakdown from the audit panel.

### Track B — Journal paper (Wiley Expert Systems, venue locked)
Favors **depth on one spine, rigorously evaluated**. The paper pipeline is
already defined in `paper/manuscript/README.md`:

- **Stage A (start now — people, long pole):** recruit 2 annotators + 1
  adjudicator → expert sign-off on the frozen schema → pilot →
  **gate: Krippendorff α ≥ 0.70**.
- **Stage B:** independent labeling of the frozen test split → adjudication →
  freeze gold labels + hashes.
- **Stage C:** confirmatory experiments E1–E9 (verifier vs baseline, calibration
  frozen before test access, dialect protocol, interaction).
- **Stage D:** writing — §2 Related Work + §3 Architecture + §4 Methods can draft
  **now** (no empirical blockers); results after Stage C.
- **Stage E:** independent reproduction + release gate.

**Claims to substantiate** (`00_SCOPE_OUTLINE.md` §8 / `06_PAPER_NOVELTY.md`):
N1 dosage safety verifier, N2 structural provenance (0 citation hallucination by
construction), N4 safety-router, N5 pro-chemical-bias counter, and the new **N6
tiered resolution / bounded LLM authority** that R2+R4+R7 produce.

**Honest assessment of journal-readiness:** the system, the 20,112-record safety
dataset, the provenance design, and the dialect map are strong enough for Expert
Systems. What makes it *a paper* rather than a system write-up is **expert
annotation + confirmatory statistics (Stage A–C)**. That gate is human effort,
not code — which is why annotator recruitment should start in parallel with the
R-series engineering, today. The R-series strengthens the paper (N6) but does not
replace the evaluation.

**STOP rules (from the paper thesis, non-negotiable):** no superiority claim if
reproduction fails; no calibration claim if thresholds moved after test access;
no subgroup inference below the frozen sample gate.

---

## 7. For an agent starting cold

1. Read this file top to bottom.
2. Read `07_ARCHITECTURE_REFINEMENT_PLAN.md` (the why) and the specific
   `R#_*.md` task you were assigned (the how — it has file/line anchors).
3. Check `docs/refactor/PROJECT_HANDOFF.md` for current build state and the
   standing test baseline.
4. Obey `AGENTS.md` hard rules and the guardrails in §4 above.
5. One task, one branch, pass the stop/go gate + the standing baseline, update
   the task's "Verification record", then stop.
