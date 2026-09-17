# E08 — Cross-Modal Contradiction Disambiguation (REAL RUN)

**Status:** DONE_REAL · **Runner:** `scripts/run_real_e08_crossmodal.py` · **Run:** 2026-08-30T15:28:49Z · **Seed:** 42 · **git:** 83d5eff  
**Target Venue:** *EACL 2027 System Demonstrations*

> **Supersedes notice (2026-09-17):** a previous version of this README documented `run_e21.py` (a 4,000-query fixed-probability simulation, 0.07 s runtime) and claimed "100.0% conflict detection." That content describes a different, simulated experiment and is **withdrawn** from this layer. The simulation script was relocated to `scripts/archive/run_e21_SIMULATION_DO_NOT_CITE.py`. The real result is below.

---

## 1. Question

When the text crop signal conflicts with the photo crop signal, does the pipeline visibly diverge instead of silently merging the two into one answer?

## 2. Protocol

- **n = 80** real field images from `backend/ml_assets/vision/test_images/full_library/`.
- Per image, two runs through the real `VisionPipeline` (`.pt` via Ultralytics, no boxes; BM25-only StubLLM QA):
  - **image-only:** `vision.detect(img, crop_hint=None)`.
  - **conflict:** `vision.detect(img, crop_hint=<conflicting crop>)` per hint map (Potato→brinjal, Rice→potato, Cabbage→rice, Cauliflower→rice, Tomato→potato, Chili→potato, Eggplant→potato, Gourd→potato, Guava→potato).
- **Divergence definition (frozen):** `mismatch_detected = (conflict.crop != image_only.crop) or (conflict.status != image_only.status)`.
- Artifact: `results_real_crossmodal.json` (summary + 15 stored samples) · input manifest hash recorded in provenance.

## 3. Result

- **68/80 = 85.0% divergence** (`n_mismatch: 68`).
- Conflict-run status distribution: diagnosed 57, healthy 18, not_recognized 5.
- **Non-divergent cases (12/80):** stored samples show the pattern — Potato image + `brinjal` hint returns Potato both times because no brinjal disease model exists, so the hint is unroutable and the pipeline falls back to image classification. Safe default (never merges), but counts as non-divergent under the frozen definition. Full 80-record persistence is recommended on re-run; only 15 samples were stored.
- Related simulation traces (`traces.jsonl`, 300 rows, E21 schema) are **not** part of this result.

## 4. Baseline context: E31 reprocessing (real API calls, cross-track reuse)

`results.json` / `results.yaml` / `traces.jsonl` (300 rows) come from reprocessing CEA E31 traces
(`paper/CEA Paper/experiments/E31_multimodal_perception_uncertainty/traces.jsonl`,
100 conflict cases × 3 baseline arms, live OpenRouter calls). Each case pairs a text claim for
Crop A with high-confidence classifier metadata for Crop B; correct behavior is clarification,
dangerous behavior is wrong-crop chemical delivery (CUAR).

| Arm | Clarify | CUAR | Source |
|---|---|---|---|
| B0 GPT-4o-mini (unconstrained) | 20.0% [13.34, 28.88] | 54.0% [44.26, 63.44] | E31 traces |
| B1 Llama-3.1-8B (mixed RAG) | 13.0% [7.76, 20.98] | 55.0% [45.24, 64.39] | E31 traces |
| B4 Gemini-2.5-flash (prompted judge) | 26.0% [18.4, 35.37] | 0.0% [0.0, 3.7] | E31 traces |

Baselines clarify rarely and (B0/B1) poison the wrong crop in >50% of conflicts.
`key_result.baa_*` fields in `results.json` currently repeat the B4 row — **B4 is a prompted
judge, not the BAA gate. Do not cite them as BAA numbers.**

The BAA gate result (B6: 100% clarification trigger [96.3, 100.0], 0% CUAR [0, 3.7],
p50 1.25ms, n=100) lives in **CEA E31**, not in this folder. For the EACL paper, re-run the
deterministic gate locally (`qa_pipeline.py` cross-modal halt) on the same 100 conflict cases
to mint a demo-track artifact — no API cost. Until then, cite B6 as companion-track evidence
with explicit cross-track disclosure, never as an EACL-measured number.

## 5. Honest framing for the paper

- Report as **"68/80 output divergence under conflicting crop hints (real .pt + BM25-stub harness)"** — evidence that conflicts propagate visibly rather than being silently absorbed.
- Do NOT report as a user-facing badge rate. The badge path (`qa_pipeline.py` cross-modal halt → clarification + A4) is implemented; its trigger rate on real text+image pairs is a separate pending study.
- Do NOT quote 100% or any E21 coverage/hazard number from this layer.
