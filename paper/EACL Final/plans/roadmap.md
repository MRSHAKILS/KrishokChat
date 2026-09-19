# KrishokTech EACL Final — Roadmap (Clean Idea + Professional Plan)

**Venue:** EACL System Demonstrations (≤6 pages + refs + live URL + ≤2.5-min screencast)
**Status:** 2026-09-17 — story-building phase; Beat A research pass 1 documented; no new features
**Authoritative evidence:** `paper/EACL Demo/experiments/results.yaml` + frozen JSONs at git `83d5eff`
**Companion track:** CEA journal owns deep science (authority ablation, calibration, temporal/regulatory conflict). EACL owns system experience. No duplication.
**Plans folder:** all step-by-step work lives in `paper/EACL Final/plans/` — this file is the index, details go to sibling files.

---

## 1. Clean idea (one sentence)

> **KrishokTech is one auditable Bengali advisory session where fail-closed gating happens *before* retrieval, hierarchical on-device classification narrows retrieval to prevent cross-crop chemical error, and verification + trace + 16123 escalation stay user-visible — degrading to BM25 + SMS without inventing advice.**

One paragraph version: a farmer's text, photo, retrieved evidence, verification state, and escalation live in a single session object, not disconnected pages. Deterministic safeguards sit alongside grounded generation. Every answer exposes *why*: safety route, evidence passage, verifier verdict, latency, and a safe next step (clarify / refuse / escalate / SMS-export). The same pipeline runs offline with a stub LLM or online with a hosted model without code changes.

---

## 2. Three contributions (paper spine — nothing else is novelty)

- **C1 — Cost-gated clarification before retrieval.** `crop=∅` halts before BM25/LLM; quick-reply chips resume. Measured E09 n=400: 100/100 ambiguous halted, 140/140 specified passed, 70/70 high-risk refused, 88% generation tokens saved on ambiguous turns, blind-RAG 38.5% cross-crop misbinding → 0% gated.
- **C2 — Classification-only on-device perception + contradiction interception.** 6 FP32 ONNX at correct per-model imgsz, 100% FP32-vs-`.pt` agreement (δ≤5e-05, n=1,237), browser WASM 26–265ms p50 single-thread, crop→disease routing, explicit `c_image ≠ c_text` badge at 68/80 = 85.0%.
- **C3 — Observable fail-closed delivery for low-connectivity.** SSE traces 100/100 ordered p50~9 events + "Why this advice?" + Safe Action Card + deterministic 160-char GSM endpoint + SW precache + 284 MB minimal. BM25 0.94 hit, system overhead p50~33.6ms (BM25-only, stub LLM).

Everything else (BM25, FAISS/BGE-M3, Gemma-4 LoRA, FastAPI/Next.js, weather, 110-pair dialect map, analytics) = capability, mentioned once, never as contribution.

---

## 3. What we will NOT claim (reviewer desk-reject guards)

1. Not "first Bengali agri-RAG" — KrishokBondhu (2025, Bengali voice RAG + Gemma 3-4B) and Farmer.Chat (15k farmers, 300k queries) predate us.
2. Not "first multimodal agri advisor" — SMART / Farmer.Chat multimodal exist. Ours is *on-device classification + contradiction badge*, scoped.
3. Not SUS — no recruited IRB study ran. E05 is an observability proxy 94.5/100, labeled as such.
4. Not live-LLM latency — E01 is BM25-only + stub LLM. Live `llama-server` = UNMEASURED.
5. Not real packet-loss measurement — `results_real_network.json` (+13.25pp rural-edge / +30.0pp severe-2G) = real BM25 hits + simulated random drop (seed 42). Must carry "simulated loss" qualifier everywhere.
6. Not dense-retrieval numbers — dense needs API key, falls back to BM25-only. Scope explicitly.
7. Not 10-crop router until reconciled — STATE says crop_classifier is 6-class; manuscript §2 says 10-class 99.55%/98.39% n=436. Reconcile to frozen JSONs before submission.
8. INT8 honesty — only crop (n=578) + wheat (n=400) reportable; potato n=15 / brassica n=51 not reportable; rice INT8 rejected (2.5pp drop); corn unmeasured.

---

## 4. Competitive positioning (why we still win)

| System | What they proved | What we do differently (measured) |
|---|---|---|
| Farmer.Chat (Microsoft/DG, 2024–26) | Scale: 15k/300k, 6 langs, RLHF 25k Q&A, DG-Eval atomic facts | No pre-retrieval safety gate with misbinding measurement; server-side multimodal; Telegram/WhatsApp online-only. We gate *before* retrieval + on-device WASM + SMS/offline-first |
| KrishokBondhu (2025) | Bengali voice RAG call-centre, Gemma 3-4B, 72.7% high-quality | Voice-only, server-only, no vision, no contradiction handling, no fail-closed verifier display |
| Krishi Sathi (2025) | Intent + 2–5 slots, 2–3 turn clarification | Slots without safety/token/misbinding measurement. We add 38.5→0% + 88% save |
| My Climate CoPilot (ACL 2025 Demo) | Transparent agri QA, 50 experts, traces + DOIs | Advisor-facing English climate QA, no vision, no low-connectivity delivery. We are farmer-facing Bengali multimodal + offline/SMS |
| BanSuite (EACL 2026) | Unified open Bangla NLP toolkit + benchmark | Toolkit, not advisory session. We are the advisory session that could consume such tooling |
| AI for Climate Finance (EACL 2026) | Agentic RAG + numeric grounding + deployed + open | Finance PDFs, English, no vision/safety-gate/SMS. Precedent for our "integration is contribution" framing |
| SmartMatch / RAGVUE (EACL 2026) | Inspectability (switch backends, per-case diagnostics) | Precedent for our Why/trace/expert-mode UI. We apply it to safety-critical dosage/PHI decisions |

Net: components known; **conjunction C1+C2+C3 in one Bengali farmer session is the novelty.**

---

## 5. Five vignettes only (S1–S5 = paper + video)

1. **S1 underspecified Bengali** → gate → chips → resume (E09).
2. **S2 photo** → crop router → disease model → Safe Action Card + source (E02).
3. **S3 text-vs-image conflict** → mismatch badge → confirm crop (E08).
4. **S4 banned/poisoning query** → Tier-0 banner, zero retrieval, 16123 dial (E03).
5. **S5 constrained delivery** → offline BM25 + SMS export (E06-det + E07).

Cut from main paper: voice ASR/TTS, dialect explainer, weather contextualization (unless live-keyed), A/B sandbox, provenance graph, gap-loop, admin editor, deployment profiles, replay IDs, "LLM called?" badge. Future work at most.

---

## 6. Experiment ledger (keep / reframe / drop)

- KEEP: E09 (lead), E03 (report 6.67% Bangla leak honestly), E02-narrowed, E01-scoped, E04, E08, E06-det, E07.
- REFRAME: E05 → "observability proxy (not SUS)"; network deltas → "simulated loss"; E01/E06 → "BM25-only, stub LLM".
- DROP from main: any CEA-deep table (slot ablation, counterfactual, calibration curves) — one sentence + companion citation max.
- Source of truth stays `paper/EACL Demo/experiments/results.yaml`; do not fork numbers into new files.

---

## 7. Six-page budget (target: 6.0, current: 8.0 — cut 2 pages)

| Section | Budget | Content |
|---|---|---|
| Abstract + Intro | 0.8 | Problem → gap → C1-C3 → artifact link |
| Architecture | 1.0 | 1 figure (5-stage pipeline) + 1 compact capability table; Farmer/Expert toggle as one para |
| Demo scenarios S1–S5 | 1.6 | 2 screenshots max (workspace + Why/trace); flowcharts to appendix |
| Evaluation | 1.6 | E09 + E03 + E02-narrowed + E01/E04/E08 + E06-det/E07; honesty notes inline |
| Availability/Repro/Limitations/Ethics | 0.6 | URL, license, build, imgsz correctness, dense/T3/SUS/corn limits |
| Conclusion | 0.2 | One para + future field study |
| Refs + appendix | unlimited | Flowcharts, table details, artifact hashes |

Cut list: second arch figure, third screenshot, full 11-slot derivation, every CI, national-economics projection, long related work (matrix + 4 must-cites instead).

---

## 8. Where we are exactly now (2026-09-17)

- **Done + frozen:** backend/Next.js PWA, Tier-0 precheck, BM25 path, stub harness, verifier, 6 FP32 + 4 INT8 + WASM wiring (flag-gated), SSE, SMS endpoint, SW precache, E01/E02/E03/E04/E06-det/E07/E08/E09 artifacts.
- **Partial:** INT8 reportable subset only; 9-fact base ⇒ deterministic hits rare (94.5% grounded in E01 — explain); dense/T3-live/SUS/corn unmeasured.
- **Blockers (P0):** 8→6 pages; abstract network qualifier; vision class-count reconciliation; BM25-only/stub scoping; verify live URL + screencast + Apache-2.0 + clean-checkout `acl.sty` build.
- **Readiness:** ~70% to submittable. Remainder is subtractive editing + verification, not new features. Code freeze in effect.

---

## 9. How we will document in `plans/` (one file per step)

- `roadmap.md` (this file) — index + clean idea, updated only when scope changes.
- `story_plan.md` — high-level story beats, literature angles, and multi-agent digging order.
- `beats/A_language_gap.md` — Beat A narrative, evidence boundaries, implementation audit, reviewer attacks.
- `lit/A_language_gap_notes.md` — Beat A source ledger + dataset-reuse precedent + citation-use rules.
- `experiments/A_retrieval_scope_and_language_repair.md` — Beat A experiment plan (primary = released benchmarks; annotation optional).
- `experiments/datasets_inventory.md` — local corpus/index/dataset inventory with status marks.
- `beats/B_missing_slots.md` — Beat B narrative (halt-before-retrieval), evidence audit, two honesty repairs, reviewer attacks.
- `lit/B_missing_slots_notes.md` — Beat B source ledger (Krishi Sathi, Farmer.Chat, over-advising, dialect degradation) + follow-up dig list.
- `experiments/B_slot_gating_and_misbinding.md` — Beat B experiment plan (P0 blind-arm + token metering; P1 PRISM route scoring + OOD audit).
- `beats/F_authority.md` — Beat F narrative (two walls + mouthpiece), E03 two-arm table, scope limit, reviewer attacks.
- `lit/F_authority_notes.md` — Beat F source ledger (RAGChecker, CiteEval, GaRAGe, SafeRAG, DG-Eval, SciTrue) + follow-up dig list.
- `experiments/F_verifier_and_walls.md` — Beat F experiment plan (P0 catch-rate study; P1 UI-wiring + end-to-end probe).
- `beats/DE_vision_scope.md` — Beat D+E narrative (fence + badge), E08 audit, stale-checkpoint corrections, reviewer attacks.
- `lit/DE_vision_notes.md` — Beat D+E source ledger (AgroGPT, SMART, PlantVillage) + open gaps + follow-up digs.
- `experiments/DE_vision_scope.md` — Beat D+E experiment plan (P0 E02 re-run + README repair; P1 badge-rate + fence studies).
- `beats/CG_lastmile.md` — Beat C+G narrative (ladder economics + SMS/16123/offline), cost/SMS repairs, reviewer attacks.
- `lit/CG_lastmile_notes.md` — Beat C+G source ledger (AIEP, Farmer.Chat channel contrast) + follow-up digs.
- `experiments/CG_lastmile.md` — Beat C+G experiment plan (P0 SMS survival + shared token metering; P1 throttle lane + dial check).
- `problems_we_solved.md` — DONE v1: C1–C3 compressed story + kill-list + honesty ledger.
- `paper_outline.md` — DONE v1: 6-page budget + 5 figure/table slots + 1-week experiment freeze + screencast + desk-reject gate.
- `review/critic_review_2026-09-17.md` — DONE: adversarial 7-day verdict (22 risks, Lane A→B→C execution, minimum viable set, 11 fallback sentences, 5-day action plan). **Execution follows the critic's lanes, not the original P0/P1 list.**
- Future: `figures_tables.md` (5-item cut list), `video_script.md` (150-sec storyboard), `submission_checklist.md` (URL/video/build/license/page-count gate).
- Rule: each file states implemented / measured / planned; no plausible numbers without frozen artifact hash.

---

## 10. Phased execution (code frozen)

1. **Outline** → fill `paper_outline.md` from §7 budget.
2. **Problems** → fill `problems_we_solved.md` from §§2–4 with 4 must-cites (KrishokBondhu, Farmer.Chat + RLHF/DG-Eval, My Climate CoPilot, BanSuite).
3. **Evidence pass** → reconcile vision counts + footprint + network qualifier to JSONs; record exact sentence fixes.
4. **Cut pass** → 8→6 pages per cut list; flowcharts to appendix.
5. **Artifact gate** → live URL, screencast, license, clean build, page count.
6. **Submit** → no new features after step 1.

**Definition of done:** 6-page PDF builds clean, every number traces to a frozen artifact, all UNMEASURED labeled, live demo + video linked, code frozen.
