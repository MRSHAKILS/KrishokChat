# Beat D+E Experiment Plan — Fence, Badge, and Honest Degradation

**Status:** largely measured on old checkpoints; re-validation P0 after classifier update  
**Priority:** P0 E02 re-run (blocks every vision number); P0 README repair (editorial); P1 badge-rate + fence studies  
**Principle:** no vision number enters the paper until re-measured on current checkpoints.

## 1. Research questions

- **RQ-D1:** What is per-model accuracy on local labeled sets with current checkpoints? (re-run)
- **RQ-D2:** Do ONNX artifacts match `.pt` predictions? (re-run parity)
- **RQ-D3:** Which INT8 variants are reportable under the parity gate? (re-run)
- **RQ-D4:** What are real browser WASM timings? (re-run with current artifacts)
- **RQ-D5:** Does the image fence reduce retrieval scope and improve gold-in-scope? (pending — P1)
- **RQ-E1:** How often do conflicting crop signals visibly diverge vs silently merge? (measured 68/80 — keep with framing fix)
- **RQ-E2:** How often does the user-facing badge trigger on real text+image pairs? (pending — P1)

## 2. What is already measured (keep, pending re-run)

| Result | Artifact | Re-run needed? |
|---|---|---|
| Per-model top-1 (potato .900/rice .925/wheat .941/brassica .912/router .941) | `results_real_pt_baseline.json` | YES — old checkpoints |
| 100% ONNX parity, δ≤5e-05, n=1,237 | `results_real_onnx_parity.json` | YES |
| INT8 reportability (crop+wheat only) | `vision_int8_report.json` | YES |
| WASM 26–265ms browser harness | E02 browser record | YES — with current artifacts |
| 68/80 divergence | `results_real_crossmodal.json` | NO — runner is checkpoint-agnostic enough, but re-confirm counts after re-run |

## 3. P0: E02 re-run on current checkpoints

1. Confirm model inventory: 6 `.pt` + class lists (resolve chilli path/naming) + checkpoint dates/hashes.
2. Re-run: per-model top-1 on the same 1,237-image manifest (800 wheat + 437 full_library, 11 smoke excluded), ONNX parity, INT8 gates, browser WASM timings.
3. Update stale code comments (6-class/no-Rice) + STATE.md §4 to the 10-class checkpoint; decide wheat-mitigation fate (keep as safety net or remove as legacy — record the decision).
4. Write results to `plans/experiments/results/`; leave 2026-08-30 artifacts untouched.

## 4. P0 (editorial): E08 README repair

1. Rewrite README to the real runner (`run_real_e08_crossmodal.py`), real n=80, real 85.0%, divergence definition, seed, harness.
2. Remove or relocate stray `run_e21.py` + its simulation text from E08's folder.
3. Add the 12/80 non-divergence cause analysis (statuses/families).

## 5. P1: badge-rate study (the S3 vignette number)

Run real text-crop × image-crop pairs through the QA pipeline cross-modal path (L386): matched pairs (control) + mismatched pairs. Report badge-trigger rate, false-badge rate on matched pairs, and latency. This upgrades "divergence" to the user-visible claim.

## 6. P1: fence study (the scope claim)

Same text query with and without image-derived crop scope over the frozen chunk index: candidate-count delta, gold-in-scope delta, wrong-crop-source rate delta. Without this, "fence" is architecture prose; with it, it's a result.

## 7. P2 (optional): recovery + OOD characterization

Second-photo recovery success; OOD refusal precision on non-crop images; healthy-vs-disease calibration. Valuable but not load-bearing.

## 8. Status marks (for later agents)

- [x] Vision workflow implemented (tri-state gate, recovery, escalation, KB fallback, audit)
- [x] Cross-modal halt implemented (qa_pipeline L386)
- [x] Old-checkpoint measurements located (E02 set + E08 68/80)
- [x] Stale code comments fixed (vision_pipeline.py 10-class truth; wheat branch marked legacy)
- [x] E08 README rewritten (real runner + E31 baselines with B4/B6 attribution fix); stray run_e21.py relocated to scripts/archive/
- [x] 12/80 cause analysis (unroutable-hint fallback to image output — safe default)
- [x] Chilli path resolved (dir `chilli_disease/`, 8 classes; no manifest rows → unmeasured like corn)
- [x] N04 accuracy + parity measured on current hashes (critic ACCEPT-WITH-FIXES, all fixes applied, deterministic reproduction confirmed)
- [x] artifact_hashes.md regenerated post-export (critic fix #1)
- [ ] Wheat-mitigation removal decision (user; branch marked legacy, numbers unaffected)
- [ ] INT8 re-run (conditional — accuracy/parity passed, schedule next)
- [ ] WASM re-run (conditional — needs playwright + refreshed frontend models)
- [ ] P1: badge-rate study through QA pipeline (N07)
- [ ] P1: fence study (N08)
