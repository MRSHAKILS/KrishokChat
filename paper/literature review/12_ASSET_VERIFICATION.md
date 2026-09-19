# Asset Verification — What Is Actually on Disk (2026-08-21)

**Purpose:** Grounds every number in `10_SYNTHESIS_GAPS_POSITIONING.md` + `11_RESEARCH_GAPS_competitive_matrix.md` + `paper/manuscript/expert-systems-skeleton.md`. No reviewer trap.

**Method:** `Get-ChildItem` + `Get-FileHash` + `Measure-Object` on 2026-08-21 (see `docs/ARCHITECTURE_ASSETS.md` for full map). `TODO` where not on disk.

---

## 1. RAG Corpus & Retrieval — VERIFIED

| Asset | Expected (old docs) | Verified | Path | Hash / Count |
|---|---|---|---|---|
| Knowledge nodes (clean) | 2,120 | **2,135** lines | `backend/ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl` | 2,135 |
| Source MDs | 2,946 | **2,946** | `backend/ml_assets/rag_index/source_md/` | 2,946 |
| BM25 corpus tokens | — | 4.7 MB | `indexes/bm25_corpus_tok.pkl` | 4,685,526 B |
| BM25 index | — | 17 MB | `indexes/bm25_index.pkl` | 17,013,819 B |
| Dense embeddings | — | 8.7 MB | `indexes/embeddings.npy` | 8,745,088 B |
| FAISS | — | 8.7 MB | `indexes/nodes.faiss` | 8,745,005 B |
| Node IDs | — | 52 KB | `indexes/node_ids.json` | 51,952 B |
| Term map | — | 23 KB | `indexes/term_map.json` | 23,291 B |
| Index SHA256 | — | 109 B | `indexes/index_sha256.txt` | 109 B |
| Institutions | 13 | **11** top-level dirs — BARI 1,506 / DAE 340 / BARC 321 / DoF 241 / CABI 222 / DLS 92 / WorldFish 85 / MoA_NARS_SRDI 73 / BRRI_IRRI 43 / CDB 15 / BSRTI 8 | `backend/ml_assets/rag_index/provenance/corpus_manifest_v1.json` | Write **11**, not 13 (R2 manifest, 2026-08-22). |

**Action:** Write **2,135** not 2,120. Cite `index_sha256.txt`.

---

## 2. Vision — VERIFIED (all `task: classify`)

| Model | Expected | Verified | File | Size |
|---|---|---|---|---|
| crop_classifier | 6 families | 6 | `vision/crop_classifier/model.pt` | 12.0 MB |
| rice_disease | 8 | 8 | `vision/rice_disease/model.pt` | 3.1 MB |
| corn_disease | 4 | 4 | `vision/corn_disease/model.pt` | 10.5 MB |
| potato_disease | 3 | 3 | `vision/potato_disease/model.pt` | 10.5 MB |
| brassica_disease | 11 | 11 | `vision/brassica_disease/model.pt` | 10.5 MB |
| wheat_disease | 11 | 11 | `vision/wheat_disease/model.pt` | 9.0 MB |

All have `class_names.json`. `verification_report_live.md` in `vision/` is SSOT. **Never claim boxes.**

---

## 3. Soil — PARTIALLY VERIFIED

| Asset | Expected | Verified | Path | Note |
|---|---|---|---|---|
| Frozen 722 imgs, 6 types, EfficientNet-B0 5-fold | 722 | **13** jpgs in `soil_moisture/` (1 preview + 12 thumbnails) | `dataset_release/soil_moisture/` | **722 are in `soil-moisture-detection/dataset/{raw,clean}/` (722 each, 956 MB, gitignored)** — do not claim 722 in `soil_moisture`. |
| EfficientNet-B0 folds | 5×16.9 MB | 5×16.9 MB | `backend/ml_assets/soil/effnetb0_fold*.pt` | Verified. |
| OOF csv | — | 178 KB | `backend/ml_assets/soil/oof_predictions.csv` | Verified. |

**Action:** Write “722 raw in `soil-moisture-detection` (ignored, 956 MB), 13 thumbnails in `soil_moisture` (tracked)” — per `docs/ARCHITECTURE_ASSETS.md`.

---

## 4. Safety — RECOVERED & VERIFIED (2026-08-21, from HuggingFace `RaiyanKhaan/krishokChat`)

| Asset | Expected | Verified | Path | Hash / Count |
|---|---|---|---|---|
| T3 refusal | 3,216 | **3,216** lines, 3.64 MB | `dataset_release/safety/t3_refusal.jsonl` | sha256 `27acdb644c9e3794…` |
| T4 requery | 16,896 | **16,896** lines, 15.85 MB | `dataset_release/safety/t4_requery.jsonl` | sha256 `a578023429cf3cc4…` |
| **Total** | 20,112 | **20,112** ✅ | — | 3,216 + 16,896 |
| Slots | — | 1,870 B | `dataset_release/safety/slots.json` | sha256 `f00faa765059c11d…` |
| Taxonomy | — | 7,136 B | `dataset_release/safety/taxonomy.json` | sha256 `a2b9040c7faa8450…` |
| Dialect map | — | 1,830 B | `dataset_release/safety/phase4_dialect_map.json` | sha256 `f034ad136a6469dd…` |
| Helpline 16123 | — | Verified | `backend/app/domain/safety_policy.py` | Correct. |

**Composition (verified by field-count):**
- **6 dialects**, evenly balanced: T3 = 536 each (standard/sylheti/chittagonian/noakhailli/rangpuri/barishal); T4 = 2,816 each.
- **T3 = 12 categories** (chemical_misuse, dosage_safety, veterinary_scope, human_medical_scope, legal_scope, dialect_discrimination, over_promise, ethical_boundary, scope_missing_crop, scope_unknown_pest, diagnostic_overshoot, financial_advice); **9 patterns** (direct/urgent/vague/authority/bypass/escalate/scope_creep/adversarial + 144 over_refusal_test).
- **T3 fields:** `safety_id, category, severity, pattern, dialect, persona, harmful_prompt, safe_response, refusal_type, over_refusal_test, adversarial_rewrite, safety_check, source`.
- **T4 fields:** `safety_id, missing_slots, missing_slot_count, highest_dp_slot, dp_score, dialect, persona, incomplete_query, requery_response, safety_check, source, source_node_id, source_org, source_crop`.

**Action:** Write **20,112 (3,216 T3 + 16,896 T4), 6 dialects** — now on disk with hashes. HF canonical path `RaiyanKhaan/krishokChat/safety_qa/{t3_refusal,t4_requery}.jsonl`. Local audit `backend/app/logs/safety_audit.jsonl` (1.7 MB) is separate runtime telemetry, not the dataset.

---

## 5. Gemma — VERIFIED (with truncation warning)

| Asset | Expected | Verified | Path | Hash |
|---|---|---|---|---|
| krishoktech.f16.gguf | 1.36 GB | 1.36 GB, SHA `1D627304F745` | `backend/ml_assets/gemma/krishoktech.f16.gguf` | `1D627304F74520284844812600F5F0E172240C8A23C88126BA7D1C1F73B84673` |
| model.gguf | 1.36 GB | hardlink to above (2 entries, 0 extra) | `backend/ml_assets/gemma/model.gguf` | same |
| Modelfile | — | 1,990 B, hardlinked to `scripts/Modelfile` | `backend/ml_assets/gemma/Modelfile` | — |

**Truncated** — must not serve. Verified runtime is external Q4_K_M + LoRA via `tools/ops/start_krishoktech_local.ps1` per `paper/archive/system_evolution_plan_2026/.../14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`.

---

## 6. Paper Assets — VERIFIED

| Asset | Path | Count |
|---|---|---|
| done papers | `paper/done papers/` | 2 PDFs |
| manuscript skeleton | `paper/manuscript/expert-systems-skeleton.md` | 335 lines |
| literature review | `paper/literature review/00..11` | 12 files |
| system_evolution_plan_2026 | `paper/archive/system_evolution_plan_2026/` | 101 files (archived) |

---

## 7. Reviewer Trap Checklist (write only verified)

- [ ] Every number cites a path above or `TODO`.
- [ ] No `arXiv:2606.29243` outside `docs/PAPER_POLICY.md` allowlist.
- [ ] No detection boxes claim.
- [x] Safety 20,112 recovered on-disk with hashes (2026-08-21) — claim allowed.
- [ ] No 722 in `soil_moisture` claim.
