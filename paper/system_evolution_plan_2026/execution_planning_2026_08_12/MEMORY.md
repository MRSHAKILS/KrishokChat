# Adjudication Memory

## Frozen State: 2026-08-12

The prior broad A+B recommendation is superseded by **OPTION B: Keep A, modify B.**

Frozen thesis: `Evidence-linked, relation-aware selective certification for Bengali agrochemical advice under a BM25-only runtime, with dialect/Banglish normalization evaluated as a safety-constrained robustness axis.`

## Decisions

- A is primary: evidence-linked structured claim relations, deterministic-first verification, expert gold, and calibrated abstention.
- B is secondary: paired dialect/Banglish normalization as a safety-constrained robustness protocol.
- No learned normalizer is required. Start with raw, Unicode, and reviewed dictionary conditions.
- Runtime retrieval remains BM25. Do not build or imply dense/hybrid retrieval for this thesis.
- The primary verifier combines deterministic parsing/normalization with structured relation matching. Optional NLI is comparison/secondary only.
- No LLM judge serves as gold or mandatory runtime verifier.
- The active lexical dosage matcher is a baseline, not a semantic verifier.
- The source-empty vision fallback must be fixed before integrated safety claims.
- Broad novelty claims for A and B are rejected due to the threat set in `02_NOVELTY_ATTACK.md`.

## Evidence State

- T05 v1 reconciliation complete: dataset sizes VERIFIED (85,979 total; per-track counts; 7,437
  chemical-bearing / 66.3%; safety test n=323; 6 dialects × 4,275). KrishokChat-paper values
  adopted for 2,946 semantic units, 284 source publications, released 1-epoch step-2,680 model.
- T06 vision-defect spec + remediation complete: source-empty KB fallback is now marked
  `low_confidence` (not `verified`) in both branches of `vision_pipeline.py`.
- T07 protocol v1 complete (frozen draft): schema JSON Schema, label manual outline, risk
  taxonomy, endpoints/margins/multiplicity/latency/sample-gates manifest; pending expert
  sign-off on coverage floor 0.80, source-authority rules, label-manual adoption, agreement
  threshold.
- T02/T03 verified artifact locations, hashes, BM25 presence, missing dense files, external datasets, checkpoint presence, and vision classification artifacts.
- T04 verified BM25-only runtime, lexical verifier, safety-before-retrieval, fail-closed behavior, JSON/SSE parity, vision fallback defect, benchmark placeholder, and unverified local-model performance.
- Root policy controls all paper references. Do not use prohibited material.

## Required Order

T05 numerical reconciliation, T06 vision-defect specification, and T07 protocol freeze come first. Then run annotation/gold creation, lexical reproduction, structured verifier, calibration, dialect robustness, A/B interaction, engineering repair/integration, expert evaluation, paper assembly, and independent release audit.

The independent engineering lane `LM00-LM05` in `13_LOCAL_MODEL_INTEGRATION_PLAN.md` may proceed without changing the research order. It only enables the existing `krishokchat-4b` selector option through the existing generation adapter. It may not change safety classification, BM25 retrieval, verification, vision, audit behavior, or the default Gemini path.

## Change Protocol

Do not overwrite this state. Append a dated amendment containing: proposed change, evidence, affected hypotheses/experiments, invalidated runs, expert approval, and new freeze version. A code-level obstacle does not authorize research redesign.

## Current Blockers

- T07 protocol v1 is FROZEN DRAFT pending expert sign-off on: (1) E2 coverage floor 0.80 /
  cost-ratio default, (2) source authority/recency rules, (3) label-manual adoption, (4)
  agreement threshold (alpha ≥ 0.70). **No confirmatory test access until clear.**
- AgriTrust entity/triple counts (19,768 / 17,501) and source-publication counts (284, both
  PDFs) have no local artifact and must not be promoted without a regenerable source.
- The checked-in `checkpoint-4020` is a 1.5-epoch intermediate (step 4,020); the released
  one-epoch model (step 2,680) artifact is not present in the repo.
- Stable evidence-span coverage and expert availability are not yet proven.
- No proposed verifier or calibration result exists.
- Local Gemma serving performance remains unverified.
- Literature descriptions require T07 full-text verification before manuscript-level comparative detail.

## Vision Defect Status (post-T06)

- **FIXED in working tree:** `backend/app/application/vision_pipeline.py` both fallback
  branches now mark KB fallback `treatment_confidence="low_confidence"` (was `"verified"`).
  Existing vision tests pass (3/3). A dedicated regression test for the source-empty branch
  is the recommended next test artifact (can land with T21 implementation).

## Local Model Artifact Note: 2026-08-12

- Located GGUF: `backend/ml_assets/gemma/krishokchat.f16.gguf`.
- llama.cpp is reported installed locally but has not been reproducibly verified in this package.
- The `.f16.gguf` filename conflicts with an unverified 4-bit description. Quantization, architecture, embedded chat template, hash, and successful Bengali inference must be recorded before claims or runtime enablement.
- Active execution checklist: `13_LOCAL_MODEL_INTEGRATION_PLAN.md`.

## Amendment: Local Model Demo Runtime Verified, 2026-08-12

- Proposed change: permit direct `llama-server` serving for the existing
  `krishokchat-4b` generation option while retaining the same OpenAI-compatible adapter.
- Rationale and evidence: see `14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`.
- Research impact: none. No hypothesis, experiment, schema, split, threshold, or result is
  changed or invalidated.
- Runtime composition: Q4_K_M base GGUF plus trained KrishokChat LoRA adapter; no merged
  4-bit artifact is claimed.
- Verified path: safety -> BM25 retrieval -> selected local generation -> lexical verifier
  -> audit, through the existing shared `QAPipeline`.
- Verification: 11 backend tests passed; standalone Bengali generation passed; local
  OpenAI-compatible completion passed; `/api/models` availability passed; `/api/qa` local
  selection passed with five sources and a verified result.
- Remaining scientific blocker: local-model quality, safety, and latency have not completed
  a frozen benchmark. The observed ~4.8 generated tokens/second is smoke evidence only.
- Gate result: LM01 and demo-level LM03/LM04 pass. LM00 provenance is partial until the base
  GGUF hash is captured in a stable manifest. LM02 Ollama registration is superseded for the
  current machine by the dated direct-serving amendment. LM05 remains open for expanded
  local-server negative-path and frontend selector tests.

## Amendment: T05 Reconcile Claims — v1 complete, 2026-08-12

- Proposed change: complete P0 T05 (numerical claim reconciliation) against stable artifacts.
- Evidence: `research_artifacts/reports/data_audit/T05_CLAIM_LEDGER_v1.md` and
  `T05_evidence_manifest_v1.md` (independent line counts, field counts, config reads, hashes).
- Repo revision at reconciliation: `621911a492eb35314d43e553c397b6b24ce54b6f` (dirty tree: 10
  tracked files modified).
- Hypothesis/experiment/schema/route impact: none. Reconciliation only; no research redesign.
- Result — dataset sizes VERIFIED: 85,979 total (General 28,993 + Treatment 11,224 + Safety
  20,112 + Table 25,650); Farmer 1,000 (eval split 350); 7,437/11,224 (66.3%) chemical-bearing;
  T3 3,216 + T4 16,896; safety test n=323 (refusal 51 / requery 272); Table QA 6 dialects ×
  4,275.
- Result — CONFLICTED: AgriTrust knowledge nodes 2,882 vs 2,120; checked-in checkpoint step
  4,020 vs released one-epoch 2,680.
- Result — NEEDS RECONCILIATION (no stable artifact, NOT promoted): 2,946 semantic units; 284
  source publications (PDF A); 19,768/17,501 entities/triples (PDF B); 284 source PDFs; all
  evaluation/metric numbers; target-module count; L4/seq-len/batch training setup.
- Checkpoint facts verified from `adapter_config.json`/`trainer_state.json`: base
  `unsloth/gemma-4-E4B-it-unsloth-bnb-4bit`, r=32, alpha=64, dropout=0, max_steps=5,362,
  peak LR 2.00e-04.
- Breakthrough for downstream: local checkpoint is an intermediate 1.5-epoch checkpoint, not
  the released model — any checkpoint-based claim must target the released 1-epoch artifact.
- Gate result: GO for dataset-size claims; DO NOT promote entity/triple counts,
  source-publication counts, or evaluation metrics until a regenerable artifact/inventory.
- Effective next task: T06 (vision defect specification) runs in parallel; T07 (protocol
  freeze) may proceed on the verified dataset-size evidence.

## Amendment: T06 Vision Defect Remediation Applied, 2026-08-12

- Proposed change: fix the two source-empty vision fallback branches so KB fallback is never
  marked `verified`.
- Evidence: `research_artifacts/reports/t06_vision_defect_spec_v1.md`,
  `t06_evidence_manifest_v1.md`; code diff in `backend/app/application/vision_pipeline.py`.
- Change: `treatment_confidence = "verified"` -> `"low_confidence"` at the advisory-blocked/low
  branch and the no-advisory branch; `treatment_sources` stays empty.
- Research impact: none. Alignment fix; the research harness uses source-linked verifier path.
- Verification: 3/3 vision tests pass; backend suite 11/11 pass; all three demo services
  (llama-server :11435, FastAPI :8000, frontend :3100) healthy.
- Gate: inside the T21 boundary; no integrated safety claim is made from the fallback.

## Amendment: T07 Protocol Freeze v1 — DRAFT COMPLETE, 2026-08-12

- Proposed change: freeze protocol, schema, label manual, risk taxonomy, endpoints, margins,
  multiplicity, latency budget, and sample gates as v1.
- Evidence:
  - `research_artifacts/annotations/guidelines/T07_protocol_v1.md`
  - `research_artifacts/annotations/guidelines/T07_label_manual_v1.md`
  - `research_artifacts/annotations/guidelines/T07_risk_taxonomy_v1.md`
  - `research_artifacts/datasets/frozen/T07_claim_schema_v1.json` (JSON Schema, draft 2020-12,
    round-trip validated: valid supported claim passes; supported w/o evidence_span flagged;
    ambiguous w/o span passes)
  - `research_artifacts/manifests/T07_endpoints_margins_multiplicity_latency_v1.md`
- Hypothesis/experiments: freezes endpoints E1/E2/E4/E5 primary, E3/E6/E7 secondary-support.
- Defaults (v1): coverage floor 0.80; safety-flip non-inferiority margin 0.00; agreement alpha
  >= 0.70; min cell size 20; latency budgets declared (safety p95 <= 1.5s, retrieval <= 300ms,
  verifier <= 150ms).
- Blockers to GO: expert sign-off on coverage floor/cost ratio, source-authority rules,
  label-manual adoption, agreement threshold. No test access / confirmatory run until cleared.
- Gate result: stable evidence spans available (GO); expert support not yet available (STOP
  confirmatory runs). Protocol is a frozen draft, not final.
- Effective next tasks: **T08 annotation pilot** and **T09 manifests/splits** may begin (both
  feed T10 expert gold) once expert annotators are confirmed; T06 implementation test can be
  added with T21 integration.

## Amendment: T08/T09 Scaffold Complete, 2026-08-13

- Proposed change: prepare T08 (annotation pilot) and T09 (manifests/splits) deliverables
  now, so expert labeling can start immediately when annotators are confirmed. Human
  steps (pilot labeling, expert gold, native review, expert E2E) run at the END of the
  project; automatable steps proceed one by one ahead of them.
- T09 COMPLETE (automatable):
  - Split builder v2 `research_artifacts/scripts/build_splits.py`: union-find grouping
    by base intent (cell_id minus qtype suffix) OR exact-question OR normalized-question.
    v1 grouped by full cell_id and leaked: same base intent with different qtype suffix
    (e.g. `a8763d0e4c0b_ipm_method` vs `..._ipm_components`) landed in different
    splits. v2 fixed: 905 groups from 1,440 cells; 2 multi-base groups; 1 multi-source
    group (all reported in manifest).
  - Frozen splits (seed 20260813, 60/20/20 by group): train 6,805 recs / 543 groups,
    dev 2,152 / 181, test 2,267 / 181; input treatment_full.jsonl sha256
    `dc9b87a04dd4...`; per-split sha256 in `datasets/frozen/T09_split_manifest_v1.json`.
  - Leakage gate: `check_leakage.py` v2 reports intent-level checks (exact/norm
    question across splits) = **0 hits � GO**. Finding for expert sign-off: 4 answer
    texts repeat across splits (source-document boilerplate baked into generated
    answers, e.g. "Adverse Weather & Production-Increase Measures", "Back Cover",
    "Climate, Soil & Production-Technology Overview"); recorded in
    `reports/T09_leakage_report_v1.{json,md}` as a data-quality finding, not auto-stop.
  - Dry-run reconstruction: rerun with same input+seed reproduces byte-identical split
    hashes (verified).
  - Hash tool: `research_artifacts/scripts/hash_artifacts.py`; full artifact manifest
    `manifests/T09_artifact_hashes_v1.json` (24 files; the manifest's own hash entry is
    one generation stale by construction).
- T08 SCAFFOLDED (human steps deferred to project end):
  - `annotations/pilot/T08_pilot_items_v1.jsonl`: 24 items, DEV pool only (24/24 dev,
    zero test), strata disease+chem 6 / pest+chem 6 / fertilizer+chem 6 / non-chem 4 /
    other 2; every item embeds query + answer + first 4000 chars of source passage with
    source content SHA-256 (evidence status: 24/24 attached).
  - `annotations/pilot/T08_pilot_item_schema_v1.json`: JSON Schema, validated; 24/24
    items pass round-trip.
  - `annotations/pilot/README.md`: roles (2 annotators + lead adjudicator), run order,
    gate (alpha >= 0.70, at most one guideline revision, STOP otherwise).
  - `annotations/adjudicated/README.md`: T10 output landing zone.
- Not changed: no test data access, no application code modified, no runtime ports
  touched. All T08/T09 outputs are research artifacts under `research_artifacts/`.
- Effective next tasks: T09 done (splits frozen). Next automatable step: **T12 lexical
  baseline runner** (offline harness reproducing current DosageVerifier with fixture
  parity) can be scaffolded without expert labels. T10 (expert gold) and T08 labeling
  remain blocked on annotators.

## Amendment: T12 Lexical Baseline Complete, 2026-08-13

- Proposed change: reproduce the CURRENT lexical verifier offline as the frozen
  baseline for the T15 structured-verifier comparison (spec row P2 T12).
- Method: runner `research_artifacts/scripts/run_lexical_baseline.py` IMPORTS the
  exact runtime module `backend/app/infrastructure/verification/dosage.py` (no
  copy/reimplementation). Per-claim membership reuses the module's own
  `_normalize`/`_claims`. Evidence mode: each frozen record verified against its
  own generating source passage (`source_md`, full content); unreachable passages
  -> no sources -> runtime no-source branch. Scoping note: this isolates
  generation+verification from retrieval (E4 covers retrieval).
- Results (T09 frozen splits, 11,224 records, **0 failures**): verified 10,885,
  flagged-unverified 339 (3.0%), low-confidence 0; only 8.9% of answers carry
  regex-extractable dosage claims (994 records; 2,502 claim occurrences, 77 distinct
  claim strings; 1,521 in evidence / 981 not). Example flag: ''5 ml'' absent from
  own passage (answers may draw on other corpus passages) - T10 gold adjudicates.
- Captured behaviors pinned in `research_artifacts/tests/test_lexical_baseline.py`
  (19 tests, all pass): parity block byte-identical to
  `backend/tests/test_pipeline.py::VerifierTests`; Bengali digit/unit/fraction
  fixtures; branch order captured (unverified check precedes no-source branch, so
  claims with no sources -> flagged-unverified); comma->dot normalization; bare
  amounts without units are not claims.
- Captured runtime parity: backend `VerifierTests + PipelineTests` 6/6 pass
  (runtime module untouched).
- Gate: **GO** - fixture parity passes; failure log empty; inputs/outputs/code
  hashed in `manifests/T12_baseline_run_manifest_v1.json`; no silent baseline
  improvements.
- Effective next tasks: T15 structured verifier (parser/normalizer + relation
  matcher as a SEPARATE candidate against this frozen baseline) can proceed as the
  next automatable step; T10 expert gold remains the blocking human step for
  confirmatory evaluation.

## Amendment: T15 Structured Verifier Candidate Complete, 2026-08-13

- Proposed change: implement the deterministic parser/normalizer + structured relation
  matcher + fail-closed safety policy as a SEPARATE candidate against the frozen T12
  lexical baseline (spec row P2 T15; NOT wired into the runtime pipeline).
- New candidate files (dead code w.r.t. the runtime; `dosage.py` untouched):
  `backend/app/infrastructure/verification/{normalization,claim_parser,
  relation_matcher,structured}.py` + `research_artifacts/scripts/
  run_structured_verifier.py`.
- Gate: **GO offline** - 26 fail-closed tests pass (Bengali numerals, unit/dimension,
  denominator, interval, PHI, polarity, applicability, source conflict -> ambiguous,
  missing evidence branch order, oracle-field mode, and the 9-case hard-failure batch
  in which nothing certifies); 19 T12 lexical tests still pass; backend suite 11/11.
- Results (same frozen splits + evidence mode as T12; n=11,224; 0 failures):
  structured verified 770 (6.9%) vs T12 verified 10,885 (97%); flagged 10,454 vs 339;
  26,995 claims (R2 20,229 / R3 3,720 / R1 3,046); certifiable claims 179 (117/47/15).
  Relations: partially_supported 11,120, unsupported 8,899, not_applicable 3,074,
  ambiguous 2,278, supported 1,624.
- Dominant abstention causes (report + claims trace files): material fields absent
  from evidence (10,060), answer chemical absent from own passage (8,666), parse
  failures (9,904 after tightening trigger to quantity-intent), non-affirmed polarity
  (3,046), chemical identity unresolved (2,250). Sample inspection confirms real
  parser-coverage limits, not defects - candidate abstains rather than guessing.
- Interpretation: candidate is intentionally conservative (dangerous non-abstention
  ~0 by construction). The tradeoff is the T17/T18 subject: E1 contrast vs lexical and
  E2 coverage calibration on dev gold.
- Remaining human blockers unchanged (T07 sign-off; T08/T10 gold) - confirmatory
  endpoints (E1-E6) cannot be reported before expert gold exists.
- Effective next tasks: T17 (verifier evaluation vs gold) is formally gated on T10;
  automatable scaffolding available now: T16 normalization harness can be prepared
  offline (dictionary review part waits on T13 native review).

## Amendment: T21 Vision Regression Tests Added, 2026-08-13

- Proposed change: add the T06-recommended dedicated regression tests for the source-empty vision fallback branches (spec row P4 T21).
- Evidence: `backend/tests/test_vision.py` — 3 new tests:
  (1) advisory fails closed (BLOCKED) → KB fallback → `low_confidence`, empty `treatment_sources`, never `verified`;
  (2) advisory raises → ADVISORY skip → KB fallback → `low_confidence`, empty sources, never `verified`;
  (3) disease info without solution → no treatment claim at all (confidence None, no sources).
- Research impact: none. Test-only addition; no application code modified, no runtime behavior changed.
- Verification: `tests.test_vision` 6/6 pass (3 existing + 3 new); full backend suite 19/19 pass; all three demo services healthy (backend :8000, llama-server :11435, frontend :3100).
- Gate: T21 GO — both source-empty branches are now pinned by regression tests; no source-empty advice can be marked `verified`.
- Effective next tasks: paper skeleton (non-empirical sections) may be drafted; T14 LLM-judge baseline remains available; confirmatory endpoints still gated on T10 expert gold.

## Amendment: Paper Skeleton Drafted (T25 scaffold), 2026-08-13

- Proposed change: draft the non-empirical paper skeleton so manuscript assembly has a stable scaffold; no empirical claims promoted.
- Evidence: `paper/manuscript/T25_paper_skeleton_v1.md` (new manuscript output only; no application code or planning document modified).
- Content: sections 1–11 per `10_PAPER_BLUEPRINT.md` section plan (Intro, Related Work five-group taxonomy, Current System, ClaimSafe-BN, DialectSafe-RAG, Benchmark/Protocol, Results/Tables, Human Evaluation, Error Analysis, Limitations, Conclusion); Appendix A reproduces the G0–G9 gate checklist with 2026-08-13 status; Appendix B maps every section to its evidence file.
- Discipline: 18 `TODO (gate: G#)` markers; zero claims of improvement/superiority; forbidden-claim checks pass (no "reduces/improves/outperforms" wording); every empirical number deferred to a run/artifact ID.
- Research impact: none. Scaffold only; confirmatory endpoints remain gated on T10 expert gold.
- Gate: informational — drafting is safe; no gate blocks a skeleton. Submission remains blocked on G3/G5/G6/G7/G9.
- Effective next tasks: T14 (fixed LLM-judge baseline, offline) and T16 (normalization harness scaffold, dictionary review part waits on T13) remain the available automatable steps; T07 sign-off is the highest-value human step.

## Amendment: T14 Fixed LLM Judge Baseline Complete, 2026-08-13

- Proposed change: run the fixed LLM judge (secondary comparison baseline, NO gold authority) per spec row T14 on the 24 dev-only pilot items.
- Evidence:
  - Runner: `research_artifacts/scripts/run_llm_judge.py` (fixed prompt v1 sha256 `1741220f…`, fixed model `google/gemini-2.5-flash-lite` via OpenRouter, temperature 0.0, json_object; reuses the runtime `OpenAICompatibleClient` transport/retry path; re-imports runtime settings for the API key).
  - Tests: `research_artifacts/tests/test_llm_judge.py` — 8 tests (prompt determinism, verdict parsing, fail-closed schema validation) all pass.
  - Run manifest: `research_artifacts/manifests/T14_judge_run_manifest_v1.json` (run_id T14-20260813T113621Z; revision `621911a…` dirty).
  - Outputs: `runs/T14_judge_raw_v1.jsonl` (24 cached raw responses w/ usage+latency), `runs/T14_judge_predictions_v1.jsonl` (23 parsed), `runs/T14_failure_log_v1.jsonl` (1).
- Results: 23/24 parsed (12 supported, 6 partially_supported, 5 unsupported, 0 ambiguous); 43,440 tokens (23 calls with usage); 1 failure: PILOT-0009 returned JSON containing LaTeX escapes echoed from the source passage (`\\(50\\mathrm{g / kg}\\)) → invalid JSON, logged and raw-cached (no silent repair).
- Findings recorded for T17: (1) judge output is NOT byte-deterministic across calls even at temperature 0 (two reruns: 22 vs 23 ok; PILOT-0009/0010 flapped) — the deterministic structured candidate remains the primary method; (2) judge can echo LaTeX from evidence into JSON — parse robustness cannot be assumed for the LLM baseline; (3) pre-existing `research_artifacts/tests/test_normalization_harness.py` imports pytest (not installed) and fails discovery — pre-existing, untracked, belongs to T16, not touched.
- Research impact: none. Secondary baseline only; never gold; not wired into the runtime (F10 preserved). No application code modified.
- Verification: backend suite 19/19 pass; judge tests 8/8 pass; servers healthy (backend :8000, frontend :3100, llama :11435 — untouched).
- Gate: T14 GO — fixed prompt/model/version recorded, raw responses cached, cost/error logged, zero test-split access (pilot pool=dev verified).
- Effective next tasks: T16 normalization harness scaffold (minus dictionary review, which waits on T13); confirmatory endpoints still gated on T10 expert gold.

## Amendment: T16 Normalization Harness Complete, 2026-08-13

- Proposed change: complete the offline normalization harness (spec row T16) — deterministic only (STOP learned work by default), no runtime wiring.
- Evidence:
  - Runner: `research_artifacts/scripts/run_normalization_harness.py` (v1). Three deterministic passes: `raw` (baseline), `unicode` (NFC + ZWJ/ZWNJ strip + Bengali→ASCII digits + Latin casefold), `dictionary` (longest-match single-token lookup, unknown-term no-op, confidence-gated raw fallback, token-boundary aware). Safety before/after via the current deterministic port (`app.domain.safety_policy.precheck`), BM25 rankings via the runtime `BM25Retriever` port over the precomputed index (`bm25_index.pkl` + `knowledge_nodes_clean.jsonl`), verifier links into the T15 structured candidate, per-record edit traces with stable record ids (AGENTS.md rule 5).
  - Tests: `research_artifacts/tests/test_normalization_harness.py` — converted from pytest to unittest (pytest is not installed in the backend venv; unittest matches the repo's research-test convention, no new dependency). 16 tests cover the four spec acceptance criteria (slot/polarity preservation, unknown-term no-op, low-confidence raw fallback, same-BM25 assertion) plus edit-trace format and determinism.
  - Run manifest: `research_artifacts/manifests/T16_normalization_manifest_v1.json` (run_id T16-20260813T121247Z; revision `621911a…` dirty; dictionary artifact sha `142ab96d…`).
  - Outputs (hashes verified against manifest): `runs/T16_normalization_run_v1.jsonl` (24 records = 4 fixture pairs × 2 sides × 3 passes), `runs/T16_rankings_v1.jsonl` (24), `runs/T16_failure_log_v1.jsonl` (0 failures).
- Harness defects found & fixed (exposed by the previously unrunnable pytest tests):
  1. Dictionary pass matched substring PREFIXES (surface "মাটি" replaced inside "মাটির") — rewritten as a token-boundary-aware manual matcher (no regex substitution; flanks must be non-alnum/non-hyphen, so partial chemical tokens like "ভিটাভ্যাক্স" can never be substituted inside "ভিটাভ্যাক্স-২০০").
  2. Edit traces were char-level difflib fragments with `record_id: None` — rewritten as record-based edits (one op per applied record, stable `record_id`, original-text offsets preserved by applying right-to-left).
  3. Same-BM25 assertion re-queried the retriever for identical text 3× — now deduped: unchanged passes reuse the raw ranking (`reused_raw: true` in rankings; checked=12, violated=0 on the fixture run).
  4. Test-file bugs fixed: stub returned dicts (rank_pass needs id/score attributes); `passes_of` unpacked as a tuple; the dedup test now exercises the real `emit_pair_side` harness path.
- Fixture-mode results (synthetic pairs only — REAL T13 pairs still blocked on native review): 24 records, 0 failures; safety flips 21×none + 3×same_category; same-BM25 assertions checked=12 violated=0. F4 documents the honest precheck gap: English "carbofuran" → `banned_or_restricted_chemical`, Bengali-script "কার্বোফুরান" → no match (runtime LLM safety layer is the backstop; flip recorded, not hidden).
- Research impact: none. Offline harness only; no application code modified; dictionary remains EMPTY by design (`status: pending_T13_review`, populating it before T13 would fabricate mappings — AGENTS.md rules 15/16).
- Verification: normalization tests 16/16 pass; research suite 23/23 (16 + 7 judge); backend suite 19/19 pass; servers healthy (backend :8000, frontend :3100, llama :11435 — untouched).
- Gate: T16 GO for the scaffold — four acceptance criteria exercised offline; dictionary REVIEW part remains gated on T13 native review (when it lands: populate `T16_reviewed_dictionary_v1.json` records, re-run with `--pairs <T13 manifest>`).
- Effective next tasks: T13 native review (dictionary + pair manifest) is the only remaining block for the real T16 evaluation; T07 sign-off remains the highest-value human step. No further automatable research tasks remain before the expert gates.
