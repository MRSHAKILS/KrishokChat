# EACL Demo — Durable Session State

**Purpose of this file.** Context compaction has twice erased standing instructions and caused
work to drift into forbidden territory. This file is the persistent memory for the EACL Demo
track. **Any new session must read this file before touching anything.** Update it after every
step; never delete history, only append or amend in place.

- **Last updated:** 2026-08-30 (V1–V6 executed, V7 in progress; Option A chosen)
- **Track:** `paper/EACL Demo` (EACL 2027 System Demonstrations)
- **Authoritative plan:** `paper/planning/paper_eacl.md`
- **Repo baseline at last update:** branch `main`, HEAD `83d5eff refinement-3`

---

## 0. Standing directives — violating any of these is a hard failure

1. **`paper/CEA Paper/` is OFF-LIMITS.** The CEA paper is DONE, verified, and ready to submit.
   Do not read it, verify it, audit it, cite its files, or modify it. It owns the 7 uncommitted
   files in `git status` — leave them alone. Two separate corrections have already been issued
   for drifting there.
2. **Work only inside `paper/EACL Demo`.** The only exceptions are read-only inspection of
   `backend/` (to write real measurement harnesses) and `frontend/` (to verify deployment claims).
3. **Do not re-verify finished work.** The manuscript skeleton, table scaffolds, and the
   claim-by-claim audit in §3 below are complete. Do not redo them.
4. **Do not produce status reports instead of doing work.** Ship artifacts.
5. **Working loop:** find gap → write the script into the right folder → update the docs →
   think about the next gap. Repeat.
6. **AGENTS.md rule 5 (no fabricated data) is absolute** for this track. Every number in the
   manuscript must trace to a frozen artifact produced by a runner that actually measured it.
   Where a number cannot be measured, write a marked `TODO`/`unmeasured`, never a plausible value.
7. **Track separation.** Paper-track code may import `backend/app` offline. Application code
   must never read `paper/`, `experiments/`, or `research_artifacts/` at runtime.

## 1. Environment (verified, do not re-derive)

- Windows / PowerShell 5.1. Repo root `D:\KrishokTech Advisory System`.
- **Python: `backend\.venv\Scripts\python.exe` → 3.13.14.** The root `.venv` does not exist;
  system Python 3.12.0 is not the project interpreter.
- Backend imports work **only with cwd = `backend`**:
  `Set-Location backend; .venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); from app.application.container import build_container"` → OK.
  Importing as `backend.app.*` fails with `ModuleNotFoundError: No module named 'app'`.
- Verified package versions in `backend\.venv`: fastapi 0.141.1, numpy 2.5.1, torch 2.13.0+cpu,
  ultralytics 8.4.116, onnx 1.22.0, onnxruntime 1.28.0, onnxslim 0.1.96, PIL 12.3.0, psutil 7.2.2,
  faiss OK. `onnxsim` is NOT installed (onnxslim replaces it). CUDA unavailable — CPU only.
  ONNX Runtime providers: `['AzureExecutionProvider', 'CPUExecutionProvider']`.
- MiKTeX `pdflatex` at `C:\Users\raiya\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe`.
- **`acl.sty` does not exist anywhere in the repo.** `manuscript/krishoktech_eacl_main.log` ends
  with `Fatal error occurred, no output PDF file produced!`. The manuscript has never compiled,
  so its page count is unverified.
- Subagent delegation is unavailable (quota exhausted). All work is direct.

## 2. Experiment layer reality (audit COMPLETE — do not re-audit, replace)

| Layer | Runner status | Verdict |
|---|---|---|
| E01 latency | `TIERS = {... "latency_mu_ms": 4.2 / 3280.0 ...}` typed literals → `sample_lognormal()` → percentiles of its own random draws | **SIMULATED — replace** |
| E02 multimodal | `ONNX_PROFILE = {"crop_classifier": {"inference_latency_ms_p50": 29.11, ...}}` literal; no model loaded, no image classified | **SIMULATED — replace** |
| E03 safety | real `httpx` → `openrouter.ai/api/v1/chat/completions`, `real_api_calls_total: 420`, 7 attack families × 30 × 2 arms | **REAL — keep, extend** |
| E04 trace | `n_simulated_pipelines: 1000` | **SIMULATED — replace** |
| E05 SUS | self-labels SIMULATED; `n_evaluators: 3`, `mean_sus_score: 82.5` | **SIMULATED — replace the whole layer with something measurable** |
| E06 offline | `n_simulated_queries: 1000` | **SIMULATED — replace** |
| E07 footprint | real filesystem walk; `total_onnx_mb: 0`, `minimal_deployment_mb: 187.3` | **REAL — keep, fix hardcoded abs path** |
| E08 cross-modal | hardcoded CEA constants | **SIMULATED — replace** |

`experiments/results.yaml` (45 KB) is a stale SSOT: its hand-written `key_metric` fields
contradict the `raw_results` printed directly beneath them, and those `raw_results` are
**relabeled foreign CEA layers** (E01←E9, E02←E17, E03←E7/E8, E04←E18, E05←E13, E06←E14,
E07←E25, E08←E21). It must be regenerated from real runs, not patched.

## 3. Fabricated manuscript claims — every one must go

| Claim | Where | Reality |
|---|---|---|
| SUS **84.6/100**, **N=60**, cohorts "Rural Bogura 35 / SAAO 15 / BARI-BRRI 10", 95.0% completion, trust 4.72±0.29 | abstract, `04_empirical_usability.tex`, `tab3`, `06_conclusion.tex`, E05 README, `drafts/04_empirical_usability.md` | fabricated. Source file says `n_evaluators: 3`, `mean_sus_score: 82.5`, SIMULATED, "NOT a formally recruited user study. Full IRB study pending." |
| **0/1,400 injections** | abstract / safety text | layer ran **210** cases and found a real **6.67 %** `bangla_native_injection` leak (0.95 % overall ASR) |
| **91.4 % @ 15 % loss, 80.3 % @ 30 % loss (+21.6 pp)** | resilience text | layer's own file: rural_edge offline 99.9 vs cloud 99.4 (**+0.5 pp**); severe_2g 99.3 vs 96.4 (**+2.9 pp**). `80.3` and `21.6` exist nowhere. |
| **2.63 GB disk / 3.70 GB RAM** | `tab4` | real measurement is **187.3 MB** |
| **96.4 % crop ID** | tables/text | that is an *intent-classifier crop-slot* accuracy, not vision |
| **91.2 % potato disease** | tables/text | exists nowhere; nearest artifact value is a CI bound 91.25 |
| **320 ms time-to-first-token** | tables/text | no source at all |
| Potato Late Blight **confidence 0.94** | scenarios | illustrative only |
| **160-char SMS, 100 % slot survival in 108 GSM chars** | deployment | no EACL layer covers this |
| **546.2 ms** as Tier-3 / Language-Generator p50 | `tab1` | it is the **weighted system mean** from CEA E18, mislabeled. `tab1`'s "Latency p50" column also mixes p50 and p95 values. |
| baseline **541 passed / 8 skipped** | README/manuscript | R-series index says **410 passed / 7 skipped**. Unresolved — suite not run. |
| **INT8 ONNX** on-device inference | README §1 theme 1, manuscript | **no INT8 artifact exists**; the two FP32 ONNX files are never loaded by any code (see §4) |
| `\citep{climatefinance2026}` on the user-study sentence | `04_empirical_usability.tex` | unrelated citation — remove |

**Framing rule.** Never write "61.5 % answered without LLM" — it bundles T0 safety redirects with
T4 refusals. Correct split: **T1+T2 = 51.04 %** deterministic advisory coverage;
**T0+T4 = 10.48 %** safety/refusal handling; **T3 = 38.48 %** LLM-dependent.
Also `T0+T1+T2 = 57.44 %`, not 61.52 %.

## 4. Vision / ONNX ground truth (verified 2026-08-30)

**Correction to an earlier session note.** A prior session recorded "no ONNX files exist anywhere."
That was wrong — it searched only `backend/`. Two real ONNX files exist and are current:

| file | bytes | MB | opset | IO | sha256 (head) | `source_pt_sha256` matches live `.pt`? |
|---|---|---|---|---|---|---|
| `frontend/public/models/crop_classifier.onnx` | 6,181,631 | 5.90 | 20 | `images [1,3,224,224]` → `output0 [1,6]` | `1aba64ff…` | **yes** (`6f144847…`) |
| `frontend/public/models/potato_disease.onnx` | 21,798,793 | 20.79 | 20 | `images [1,3,224,224]` → `output0 [1,3]` | `25117405…` | **yes** (`d57b961e…`) |

Both carry embedded Ultralytics metadata (`task: classify`, class `names`, `imgsz`, producer
`pytorch 2.13.0`, ultralytics `8.4.116`, exported 2026-08-26). Both are **FP32**. `metadata.json`
in that folder is a real deterministic export record with SHA-256 digests.

Source checkpoints (`backend/ml_assets/vision/<name>/model.pt`), read from `train_args`:

| model | MB | classes | train `imgsz` | arch | ONNX today (2026-08-30, Option A) |
|---|---|---|---|---|---|
| crop_classifier | 11.96 | 6 | 224 | yolo26n-cls | FP32 ✔ + INT8 ✔ (1.60 MB, 3.68×, 0pp drop, agree 0.9844, reportable) |
| potato_disease | 10.52 | 3 | 224 | yolo26s-cls | FP32 ✔ + INT8 ✔ (5.34 MB, 3.90×, 0pp, agree 1.0, n=15 not reportable) |
| rice_disease | 3.06 | 8 | **320** | yolo26n-cls | FP32 ✔ (5.91 MB) — INT8 **rejected** (2.5pp drop, agree 0.875) |
| wheat_disease | 9.00 | 11 | 224 | yolo26n-cls | FP32 ✔ + INT8 ✔ (1.61 MB, 3.68×, 0pp, agree 1.0, reportable) |
| corn_disease | 10.52 | 4 | **256** | yolo26s-cls | FP32 ✔ (20.79 MB) — INT8 **unmeasured** (no local labelled images) + corn accuracy unmeasured |
| brassica_disease | 10.54 | 11 | **256** | yolo26s-cls | FP32 ✔ + INT8 ✔ (5.35 MB, 3.90×, 0pp, agree 0.9804, n=51 not reportable) |

FP32 ONNX: 6 files at correct per-model `imgsz` in `backend/ml_assets/vision/onnx/` (80.13 MB total, opset 20, 100% agreement vs `.pt` max delta 5e-05); browser copy `frontend/public/models/` 40.59 MB primary (81 MB with legacy aliases `*_disease.onnx` duplicates) via `prepare_ondevice_artifacts.py`; `onnxruntime-web/wasm` 1.29.0 lazy chunk (~63KB gzipped) gated `NEXT_PUBLIC_VISION_ONDEVICE_ENABLED` default-off, wiring `src/lib/vision-ondevice.ts` + `detect/page.tsx` (Resize→CenterCrop→/255 NCHW, single-thread WASM, `pnpm build` + `pnpm size` 700KB green).

Notes that matter:
- `backend/scripts/export_vision_ondevice.py` hardcodes `imgsz=224` and exports only
  crop_classifier + potato_disease. **224 is wrong for rice (320), corn (256), brassica (256)** —
  exporting those at 224 silently degrades accuracy. Per-model `imgsz` must come from the checkpoint.
  Fixed in `export_vision_onnx_all.py` (now exporting all 6 at correct `imgsz`).
- `crop_classifier` and `wheat_disease` checkpoints have `ck['model'] is None`; their class names
  live in `ck['ema'].names`. Both were checked against `class_names.json` and **match exactly**.
  `YOLO()` loads them fine, and the runtime registry reads labels from `class_names.json` anyway.
- **Before 2026-08-30: no code loaded ONNX.** `onnxruntime-web` was absent from `frontend/package.json`; only "On-Device" was a display pill at `provenance-badge.tsx:153`. **2026-08-30 Option A:** added `onnxruntime-web@1.29.0` (pnpm view verified), `src/lib/vision-ondevice.ts` (lazy `import("onnxruntime-web/wasm")`, 72KB wasm bundle, numThreads=1, Resize→CenterCrop→/255), wired `detect/page.tsx` behind `NEXT_PUBLIC_VISION_ONDEVICE_ENABLED` (default off, warm-up via requestIdleCallback), browser models in `frontend/public/models/` (40.59 MB primary) now consumed by a real code path.
- **Backend inference remains `.pt` via `YOLO()`** (`ultralytics_classifier.py:26`) — ONNX is a browser/deployment artifact, not the server serving path. `registry.py` still requires `model.pt`+`class_names.json`.
- INT8 via ORT `quantize_static` with `nodes_to_exclude` for non-Conv/Gemm/MatMul (ultralytics lesson) works offline with a hand-written `CalibrationDataReader` over `test_images/`; `export(quantize=8)` remains unusable (needs `check_cls_dataset` with Kaggle/Drive `data=`). V5 executed 2026-08-30 with held-out splits, `max_drop_pp=2.0` + `agree>=0.90` gate; see `vision_int8_report.json`.

Local labelled test data (folder name = ground-truth label):
- `backend/ml_assets/vision/test_images/wheat_disease/` — **800 images, 11 folders**, exactly
  matching the wheat model's 11 classes. Best available accuracy set.
- `backend/ml_assets/vision/test_images/full_library/` — **437 images, 45 folders** (not 47) spanning
  Potato 3/30, Rice 8/80, Brassica 11/102 (Cabbage 4/32 + Cauliflower 7/70), plus Tomato 5, Chili 4, Eggplant 5, Gourd 4, Guava 5 (no disease model = correct NO_DISEASE_MODEL set).
  Verified 2026-08-30: `vision_eval_manifest.json` 1,237 scored (800 wheat +437 full_library) +11 smoke excluded; corn unmeasured remains.
  Previous "47 folders / 66 brassica" undercount was stale — brassica is 102.
- `test_images/{crop_classifier,potato_disease,rice_disease,brassica_disease}/` — 2–4 smoke images each (11 total excluded from scoring).
- **corn_disease has no local test images** → corn accuracy is unmeasurable. Say so, don't invent it.
- `test_images/test_matrix_results.json` — a real prior 437-row end-to-end crop→disease routing run
  with genuine confidences. Usable as corroborating evidence, not as a substitute for a fresh run.
- Frontend bundle: `frontend/package.json` size-limit 650→700 KB (baseline First Load 621KB + lazy on-device WASM chunk ~63KB gzipped); `onnxruntime-web` 1.29.0 via `onnxruntime-web/wasm` (72KB raw) lazy, not in First Load, `pnpm build` green.

## 5. Backend surface inventory (for writing real runners)

- Tier SSOT `app/domain/resolution.py` (`tier_for`, `ZERO_LLM_TIERS`, `TIER_LABELS_BN`).
  `ResolutionTier` in `app/domain/enums.py`: `deterministic_guard`(T0), `structured_fact`(T1),
  `templated_advisory`(T2), `grounded_generation`(T3), `honest_refusal`(T4).
- `SafetyCategory`: safe_agri, banned_or_restricted_chemical, self_harm_or_poisoning_risk,
  off_topic, prompt_injection, low_confidence. `VerificationConfidence`: verified,
  flagged-unverified, low_confidence, blocked. `PipelineStage`: safety, retrieval, generation,
  verifier. `StageStatus`: start, complete, skip, error.
- Orchestrator `app/application/qa_pipeline.py` (`QAInput`, `QAPipeline`, ~641 lines).
  Contracts `app/domain/contracts.py`: `QueryContext`, `SafetyDecision(.terminal)`, `QAResult`,
  `PipelineEvent`, `RetrievedSource`, `VerificationResult`, `VerifierClaim`.
- Telemetry `app/application/telemetry.py`: `STAGE_NAMES = ("safety","retrieval","generation","verifier")`,
  `stage_timer(name, timings)` (perf_counter ms), `capture_tokens`, `current_request_id`, `estimate_cost`.
- Safety `app/domain/safety_policy.py`: `PATTERNS`, `precheck(query)`, `CANNED_RESPONSES` (line 61),
  `canned_response(category)`. Verified: `precheck('paraquat কীভাবে বেশি খাব?')` →
  `(SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL, ('banned_active:paraquat:en',))`.
- Routes: `POST /api/qa`, `POST /api/qa/stream` (`app/api/qa.py`, `SSE_HEARTBEAT_SECONDS = 15.0`),
  `GET /api/safety/metrics`, `POST /api/classify`, `POST /api/detect` (`app/api/vision.py`),
  `POST /api/sms/advisory`, `POST /api/dialect/translate`, `POST /api/weather`, helpline `16123`
  (`app/api/extras.py:257 sms_advisory_endpoint`, strict 160-char GSM).
- Vision app layer: `app/application/vision_pipeline.py` (`VisionPipeline.classify/detect`,
  `crop_threshold=0.60`, `disease_threshold=0.55`, wheat↔rice ambiguity mitigation, crop_hint
  bypass, `image_quality()` gate). Port `app/ports/vision.py`, domain `app/domain/vision.py`.
- Verifier `app/application/verifier.py` `HardenedDosageVerifier.verify(answer, sources)` →
  grounded / unsupported / no_dosage.
- Retrieval `app/infrastructure/retrieval/`: `bm25.py BM25Retriever(index_path, corpus_path)`,
  `dense.py DenseRetriever` (FAISS IndexFlatIP + BGE-M3 via OpenRouter, returns `[]` on failure),
  `hybrid.py HybridRetriever` (RRF, `RRF_K = 20`, `candidate_depth=50`, `bm25_only`,
  `last_expansion`), `expansion.py QueryExpander(term_map_path, dialect_map_path)`.
- Indexes: `bm25_index.pkl` 16.23 MB, `bm25_corpus_tok.pkl` 4.47 MB, `chunks_bm25.pkl` 11.63 MB,
  `chunks_corpus.jsonl` 1.95 MB, `embeddings.npy` 8.34 MB, `nodes.faiss` 8.34 MB,
  `eval/farmer_benchmark_1000.jsonl` 5.39 MB, `eval/golden_retrieval_probe.json`,
  `eval/coverage_gaps_v1.json`, `derived/fact_base_v1.json` (**only 9 facts**),
  `derived/dose_reference_v1.json`, `derived/curated_facts_v1.json`. `source_md_count: 2946`.
- `StructuredResolver` gated by `STRUCTURED_RESOLVER_ENABLED`; needs BOTH crop AND problem ≥ threshold.
- Container `app/application/container.py build_container(settings)`. LLM factory
  `app/infrastructure/llm/factory.py create_llm_client(settings, role=...)` — **no stub provider**.
  Offline runs must inject a fake: copy `StubLLM` from `backend/tests/test_smoke_qa_pipeline.py`
  or `FakeLLM`/`FakeRetriever` from `backend/tests/test_pipeline.py`. Marker `live_llm` is skipped
  unless `RUN_LIVE_E2E=1`.
- Dialect assets: `dataset_release/safety/phase4_dialect_map.json` has **only 110 kept pairs**
  (audit `backend/ml_assets/rag_index/eval/dialect_map_derivation_audit_v1.json`: 1,440 cells in,
  16 out; method "difflib 1:1 token replace… no LLM; no fabrication"), labels
  barishal/chittagonian/noakhailli/rangpuri/sylheti. The root README's "110-word dialect map" claim
  is inconsistent with this. Frontend `dialect-selector.tsx` defines
  `DialectId = standard|rajshahi|rangpur|chittagong|sylhet|barishal` with hardcoded demo queries.
- Safety dataset: 20,112 records (`t3_refusal.jsonl` 3.47 MB, `t4_requery.jsonl` 15.12 MB).
- PWA evidence: `frontend/public/sw.js`, `manifest.webmanifest`, icons,
  `frontend/src/components/pwa-register.tsx`. Demo assets in `demo-assets/`
  (`cached_responses.json` 1.85 MB, `qa-demo-questions.md`, gif/mp4/webp).

## 6. Agreed design for real runners (decided, not yet implemented)

- One shared offline harness builds a real `QAPipeline` (real `BM25Retriever`, real `precheck` /
  `SafetyClassifier`, real `StructuredResolver`, real `HardenedDosageVerifier`) plus a
  deterministic stub LLM, via `sys.path.insert(0, <repo>/backend)`.
- Report LLM-excluded timings honestly as **"system overhead latency"**, never as end-to-end.
- Use FastAPI `TestClient` against `POST /api/qa/stream` for real SSE frame counts and stage ordering.
- Write to **new filenames** (`run_real_*.py` → `results_real.json`) so existing artifacts are not
  clobbered while the rebuild is in progress.
- Held-out Bengali question set: 300–500 drawn from
  `backend/ml_assets/rag_index/eval/farmer_benchmark_1000.jsonl` per plan §86, stratified across
  general / disease / treatment / ambiguous / unsafe / Banglish / dialect / OOD.
- Dense retrieval needs `OPENROUTER_API_KEY`. Offline runs are **BM25-only and must label
  themselves as such**.

## 7. Open decisions for the user

1. **Vision claim scope — RESOLVED 2026-08-30: Option A (full ONNX + INT8).** The user chose A and
   V1–V6 have been executed: all 6 FP32 at correct `imgsz`, 4 INT8 accepted (see §4 table), browser
   wiring done. The other options (B, C) remain documented in `state/TASK_VISION_ONNX.md` as fallbacks
   but are not the path taken. No further decision needed here.
2. **Generation latency — STILL OPEN:** is a live model server (`llama-server` / Ollama) runnable
   during the measurement window? If not, measure T0–T2 + retrieval for real and mark T3 end-to-end
   as `unmeasured`. V2 used an offline deterministic StubLLM for the advisory leg; E01 still needs
   its held-out harness.

## 8. Status ledger

### Done
- Full claim-by-claim audit of every numeric assertion in the manuscript/tables/drafts against each
  layer's own `results.yaml` (§3). Read-only; nothing modified.
- Confirmed E01/E02/E04/E05/E06/E08 runners are constant-table simulations; E03 and E07 are real.
- Verified backend runtime + importability from `backend/` cwd with `backend\.venv`.
- **Corrected the ONNX inventory** (§4): 2 current FP32 ONNX files exist in `frontend/public/models/`,
  4 models unexported, 0 INT8, and no code path consumes ONNX at all.
- Catalogued all six `.pt` classifiers with per-model class counts, train `imgsz`, and arch.
- Catalogued local labelled test data: 800 wheat images + 437 full_library images.
- Confirmed the manuscript has never compiled (no `acl.sty`).
- Wrote this state file (was the top blocked item).
- Wrote `state/TASK_VISION_ONNX.md` — the handoff plan for the local execution agent.
- **[2026-08-30 Option A V1]** `vision_eval_manifest.json` — 1,237 scored images (800 wheat +437 full_library, 11 smoke excluded), corn unmeasured, correct brassica 102 not 66; per-model coverage + hashes.
- **[2026-08-30 Option A V2]** `results_real_pt_baseline.json` — real `.pt` serving path: per-model top1 potato 0.900/rice 0.925/wheat 0.9413/brassica 0.9118/crop 0.9412, macroF1, confusion matrices, p50 latencies, plus `VisionPipeline.detect()` routing (hint-off 1,237 diagnosed 845/healthy151/not_recognized44/no_disease_model197, routed disease accuracy 0.9011; wheat→rice mitigation 43).
- **[2026-08-30 Option A V3]** 6 FP32 ONNX at correct `imgsz` (224/224/320/224/256/256) in `backend/ml_assets/vision/onnx/` (80.13 MB, opset 20, input/output shape asserted, class-name parity verified) + `vision_onnx_export_report.json`.
- **[2026-08-30 Option A V4]** `results_real_onnx_parity.json` — 100% agreement ONNX vs `.pt` on 1,237 images (max delta 5e-05, McNemar discordant 0, paired exact), p50 ONNX CPU vs Ultralytics per model.
- **[2026-08-30 Option A V5]** `vision_int8_report.json` — ORT `quantize_static` (Conv/Gemm/MatMul only, disjoint calibration/eval splits): crop 300/578, potato 15/15, wheat 300/400, brassica 51/51, rice 40/40 rejected (2.5pp drop, agree 0.875 <0.90), corn unmeasured; only wheat+crop reportable (n>=100); totals int8 13.888 MB vs fp32 53.432 MB.
- **[2026-08-30 Option A V6 — browser]** `onnxruntime-web@1.29.0` via `onnxruntime-web/wasm` lazy (72KB raw, ~63KB gzipped), `src/lib/vision-ondevice.ts` (Resize→CenterCrop→/255 NCHW, single-thread WASM), `prepare_ondevice_artifacts.py` → `frontend/public/models/` 40.59 MB primary (81 MB with legacy aliases), `metadata.json` regenerated, `detect/page.tsx` wired behind `NEXT_PUBLIC_VISION_ONDEVICE_ENABLED` default-off with fallback to server, warm-up via `requestIdleCallback`, pill "On-Device INT8", `pnpm build` green, `pnpm size` 700KB green (was 650KB; 621KB First Load +63KB lazy chunk).
- **[2026-08-30 Option A V6 — E07 fix]** `run_e07_deployment_footprint.py` fixed hardcoded `WS = Path(r"d:\…")` → `Path(__file__).resolve().parents[5]`, widened scan to `vision/onnx*` + `frontend/public/models` with SHA-256 dedup; re-ran: total_onnx 95.64 MB unique (11 files), minimal 284.0 MB (was 187.3, was 0 before ONNX), full with .pt 339.6 MB.
- Updated `README.md` (§1 theme 1, §2 progress 37.5% real, §3 tree, §4 rebuild plan) and `manifest.yaml` (E02 REAL, E07 fixed, external_inputs 45 folders, browser payload).

### In progress
- V7 docs/claim cleanup (remaining: E02 README appendix, manuscript `04_empirical_usability.tex` SUS/Cea constants, `tab4` footprint) + remaining 5 simulated layers (E01, E04–E06, E08).

### Blocked
- T3 end-to-end latency → blocked on decision §7.2 (live model server?; offline StubLLM used for V2).
- Dense-retrieval arm → needs `OPENROUTER_API_KEY`.
- Manuscript build → needs `acl.sty` vendored into `manuscript/`.
- Backend suite pass count (410/7 vs 541/8) → unresolved, suite not run.
- Subagent delegation → unavailable (quota).

### Next actions (in order)
1. Resolve §7.2 (live model server) with the user, then build shared harness + `run_real_e01_latency.py` over 300–500 held-out.
2. Replace E04/E06/E08/E05 (E05 must not simulate humans).
3. Regenerate `experiments/results.yaml` only after every layer has a real artifact.
4. Rewrite manuscript sections/tables from the regenerated SSOT, deleting every §3 claim.
