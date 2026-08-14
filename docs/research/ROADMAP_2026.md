# KrishokChat Improvement Roadmap 2026 — Post-Auth Product Lane

Date: 2026-08-14. Source of truth for decisions: `docs/research/CRITIC_GAPS_2026.md`
(adversarial review of 19 candidates from `docs/research/LITERATURE_SCOUT_2026.md`
and `docs/competitive-landscape.md`). This lane is **product/engineering** —
separate from the frozen research thesis in
`paper/system_evolution_plan_2026/execution_planning_2026_08_12/` (which remains
the research execution authority and is untouched by this roadmap).

Horizon: 3–4 minute investor demo first; marketplace readiness second. All five
phases are additive, respect root `AGENTS.md` hard rules (locked stack, one
FastAPI + one Next.js process, auth never gates demo, precomputed indexes only,
no fabricated metrics), and feed real data into the existing agent trace + safety
panel (AGENTS.md §4).

---

## A. Execution order with dependency graph

```
P1 Verifier hardening (dosage enforcement + refusal metrics)
   │
   ├──► P2 Dual-view metrics (needs P1 verdict fields in the audit log)
   │
   └──► P4 Golden benchmark (needs P1 verifier behavior to measure;
         benchmark exists BEFORE P1 acceptance criteria are certified)
   │
P3 Hybrid RRF retrieval + dialect expansion   (independent of P1/P2/P4;
   │   runs after P5-style infra only)        (no dependency on others)
   │
P5 Voice: TTS read-aloud first, ASR optional (depends on nothing; run last
                                               or in parallel — UI-only)
```

Critical path: **P1 → P2 → P4** (verifier → metrics → benchmark) is the demo's
credibility spine. **P3** and **P5** are parallelizable side-lanes; P3 has the
longest silent risk (dense index build + retrieval quality) and should start
early so regressions surface before demo week.

Correction recorded from `paper/system_evolution_plan_2026/MEMORY.md` (T03/T04):
**the dense/FAISS channel does NOT exist at runtime today** (BM25-only). P3 must
therefore first BUILD the dense index offline (`scripts/build_rag_index.py`,
run once, per root AGENTS.md §5) before any RRF fusion claim. No hybrid claim may
be made until that index exists and is wired.

---

## B. Per-phase work breakdown

### P1 — Verifier hardening: dosage-claim enforcement + refusal metrics
**Depends on:** nothing (pipeline step 4 exists).

Files:
- `backend/app/ports/verifier.py` — extend existing verifier port with
  `VerifierRequest`/`VerifierResult` contracts (claims list, verdicts).
- `backend/app/application/verifier.py` — rule-based claim decomposition:
  split answer into sentences; regex-extract (chemical, crop, number, unit)
  tuples; entailment check = every element must appear in the retrieved
  passages (normalized); verdicts: `grounded` / `unsupported` / `no_dosage`.
  **Annotate-and-drop, never hard-block**: unsupported dosage claims are
  stripped from the returned answer and annotated in the UI + audit log.
- `backend/app/infrastructure/dosage/` — normalization utilities (unit table,
  Banglish numeral map, chemical synonym list from the existing corpus).
- `backend/tests/test_verifier.py` — 20-item dosage test set (10 grounded,
  10 unsupported), 10 fully grounded answers must produce zero false blocks.
- Audit log: append per-claim verdicts + refusal counters (TRUST-SCORE-style:
  over-responsiveness, excessive refusal) to the existing JSONL.
- `.env.example` — no new vars expected (rule-based). Note if any.

DoD: pytest green; every stripped claim carries a logged reason; safety panel
shows live checked/passed/flagged counts; AGENTS.md §6 note written.

Evidence: Wallat et al., ICTIR 2025 (DOI 10.1145/3731120.3744592) — up to 57% of
citations are post-rationalized; VeriCite arXiv:2510.11394; TRUST-SCORE
arXiv:2409.11242.

### P2 — Dual-view metrics wired to agent trace + safety panel
**Depends on:** P1 (verdict fields), audit log schema.

Files:
- `backend/app/application/audit.py` — extend each JSONL entry with per-step
  validity: router category correctness, retrieval hit/miss + top-1 relevance,
  verifier pass/flag, refusal type.
- `backend/app/api/safety.py` — `GET /safety-metrics` reads the local log,
  returns counts by category, refusal rate, verifier pass rate. **Numbers are
  computed from the log at request time; the PANEL is rendered from these live
  counts** (this is live telemetry of real decisions, not fabricated benchmark
  data — the benchmark panel stays precomputed per hard rule 2).
- Frontend: `qa-panel.tsx` stepper states bound 1:1 to logged decisions;
  safety panel on the existing metrics surface.
- `backend/tests/test_audit.py` — log schema + endpoint tests.

DoD: each demo query updates the counts; stepper matches log 1:1; pytest green.

Evidence: AgroTools arXiv:2605.22366 (dual-view scoring; instrument
tool/argument validity first); scout risk #9 (traces without real logging read
as fake).

### P3 — Hybrid RRF retrieval + dialect query expansion
**Depends on:** dense index build (prerequisite, see correction above).

Files:
- `scripts/build_rag_index.py` — offline dense index build (FAISS) over the
  verified corpus; run once, artifacts on disk under `backend/ml_assets/rag_index/`.
  Record embedding model + version (verify current stable via registry search
  per root rule 7; the project's existing dense channel config is the default
  candidate — confirm before pinning).
- `backend/app/application/retrieval.py` — rank-level reciprocal-rank fusion of
  BM25 + dense; `BM25-only` fallback flag; query expansion via
  `dataset_release/safety/phase4_dialect_map.json` (110 words) + AgriEnBn
  glossary (colloquial → standard, e.g. "Magra" → "Stem Borer"); expanded query
  surfaced in the agent trace.
- `backend/tests/test_retrieval.py` — Recall@5 / nDCG on the golden set
  (from P4): hybrid ≥ single-channel on ≥80% of dialectal queries; no
  regression on standard queries.

DoD: index built + hashed; pytest green; trace shows mapped query; no hybrid
claim until index exists.

Evidence: Agri-Query arXiv:2508.18093; AHR-RAG Smart Agriculture 2026 (RRF);
TraSe LM4UC 2025 (aclanthology.org/2025.lm4uc-1.2).

### P4 — Expert-grounded golden benchmark with unanswerables
**Depends on:** P1 (to measure); runs in parallel with P2.

Files:
- `dataset_release/benchmark/golden_qa_v1.jsonl` — 40–60 questions sampled from
  the existing 1,001 real farmer queries; categories: dosage, timing,
  pest identification, off-topic, ≥10 unanswerable; reference answers from
  extension sources (BARI/BRRI/DAE); 2 human evaluators score each answer
  (correct / partial / unsupported / refused); disagreement log kept.
- `backend/app/api/benchmark.py` — serve PRECOMPUTED stats only (hard rule 2).
- Research panel: per-category scores; dose and timing broken out; refusal rate
  on unanswerable items.

DoD: inter-evaluator agreement recorded; panel published numbers; refusal rate
on unanswerables ≥90% at demo time.

Evidence: PubMed 38341517 (chatbot loses exactly on dose/timing); AIEP
arXiv:2601.11537 (golden sets, expert scoring); ACL 2025 Findings
(2025.findings-acl.368) — no pure LLM-as-judge.

### P5 — Voice: TTS read-aloud first, ASR optional
**Depends on:** nothing (frontend surface; pipeline untouched).

Files:
- `frontend/src/components/audio/read-aloud.tsx` — listen button on answer
  cards; Bengali TTS via ElevenLabs v3 (bn) or Google TTS `bn-IN` (NOTE: no
  `bn-BD` TTS locale exists — state the locale honestly); <2s render target;
  loading/fail states with graceful silent fallback.
- Optional: `backend/app/api/speech.py` — `POST /asr` proxying Google STT
  `bn-BD` (chirp_2) or local Whisper-family model; key stays server-side;
  recognized text routes through the SAME text pipeline (zero agent changes);
  any ASR failure falls back to text input with a visible notice.
- `.env.example` — ASR/TTS keys (optional lane).
- Tests: manual E2E script for 3 scripted phrases + read-aloud render timing.

DoD: read-aloud renders <2s; ASR path reproduces text-typed result for 3
phrases; failure mode = graceful fallback, never wrong-language answer.
**Standard Bengali only — no dialect claims (Ben-10 IJCNLP-AACL 2025:
foundation ASRs fail on Bengali dialects).**

Evidence: FarmSaarthi JETIR2604936 (87.3% vs 62.1% decision accuracy);
AIEP arXiv:2601.11537; KrishokBondhu arXiv:2510.18355.

---

## C. Effort estimates and critical path

| Phase | Effort | Demo impact | Critical path |
|---|---|---|---|
| P1 Verifier hardening | Med (~2 days) | High | ✅ |
| P2 Dual-view metrics | Low–Med (~1.5 days) | High | ✅ |
| P3 Hybrid RRF + dialect | Med (~2.5 days incl. index build) | Med–High | side-lane |
| P4 Golden benchmark | Med (~2 days, human-scored) | Med–High | ✅ (parallel) |
| P5 Voice | Low–Med (~1.5 days TTS; +1 ASR optional) | High | side-lane |

Total: ~7–9 person-days; critical path P1→P2→P4 ≈ 5.5 days.

---

## D. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Bengali NLI models scarce → entailment unreliable | Rule-based deterministic check first (chemical/crop/number/unit must all match passages); annotate-and-drop, never hard-block; NLI deferred |
| RRF fusion regresses recall vs today's BM25 | BM25-only fallback flag; golden-set A/B (P4) gates merge |
| Dense index build fails/quality poor | Build offline first, hash artifacts; keep BM25 as default until A/B passes |
| TTS demo failure / wrong voice | Fallback chain (no audio → text only); <2s target measured on demo hardware |
| Benchmark scoring bias | 2 evaluators + recorded disagreement; never LLM-as-judge as sole gold |
| Voice ASR garbles Bengali dialects | Standard Bengali only at demo; visible text fallback; dialect claims forbidden |
| Scope creep toward GraphRAG/offline/B2B | Explicitly out of scope (Section E); any new service violates hard rules |

---

## E. Explicitly out of scope (critic verdicts)

- **ADOPT-LATER:** query-type routing (scout #2); entity KG + community summaries
  (scout #6); clarify-or-respond slots (scout #11); offline-first PWA (landscape
  #6 — undemonstrable in a conference room, Krishoker Janala precedent only
  11.3% "highly effective"); B2B dealer/SAAO layer (landscape #7 — role-based
  multi-tenancy forbidden by hard rule 1 at demo phase).
- **REJECT:** AI front-end to 16123 (landscape #3 — no public API/integration
  surface; the shipped canned redirect + 16123 contact already carries the
  story; a mock would violate the no-fabrication rule).
- **REJECT now, revisit later:** DPO "learn to refuse" alignment of the 4-bit
  model (LoRA measured +0.5–0.85% grounding — Sem-RAG; refusal METRICS are the
  cheap half, in P1).

---

## F. Suggested commit sequence (repo style: short imperative lines)

1. `verifier hardening: dosage claim enforcement + refusal metrics (P1)`
2. `dual-view audit metrics + /safety-metrics endpoint (P2)`
3. `hybrid RRF retrieval + dialect query expansion (P3)`
4. `golden benchmark with unanswerables + panel stats (P4)`
5. `voice read-aloud + optional ASR input (P5)`

---

## G. Demo story (from critic §D)

Open with a Chittagonian farmer's question; the agent trace shows each real
step — router classifying, retrieval expanding dialect terms and fusing BM25 +
dense, verifier checking every claim against passages (dosage claim either
green-flagged with its source or stripped as unsupported). One out-of-scope
question shows the graceful refusal with the 16123 escalation. Close on the
safety panel (live counts from the actual log) and the research tab (pre-scored
golden benchmark proving dose/timing correctness — the exact category where
generic chatbots fail). Story: *the only Bengali agri assistant where every
claim is verified, every decision is traceable, and the safety numbers are
real.*