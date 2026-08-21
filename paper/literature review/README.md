# Literature Review — Final SSOT for Expert Systems Paper

**Folder:** `paper/literature review/` — **12 files, 2025→2026-08, no duplicates, verified against on-disk assets.**  
**Use this while writing:** every claim below is tied to a real file on disk (see `12_ASSET_VERIFICATION.md`). No `arXiv:2606.29243` (banned per `docs/PAPER_POLICY.md`).  
**How to follow:** Read `00` → `09` for cluster depth, then `10` (synthesis) + `11` (competitive matrix) + `12` (asset verification) for paper positioning. `paper/manuscript/expert-systems-skeleton.md` is built directly from `10` §4.

---

## 1. Verified Assets You Actually Have (write only what is on disk)

| Claim in old docs | Verified on disk 2026-08-21 | File | Action for paper |
|---|---|---|---|
| 2,120 nodes | **2,135** `knowledge_nodes_clean.jsonl` | `backend/ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl:1` | Write **2,135** (or 2,135/2,135), not 2,120. |
| 13 institutions, 2,946 MD | **2,946** MD in `source_md/` | `backend/ml_assets/rag_index/source_md/` | Correct. |
| BM25 `pkl` + FAISS `IndexFlatIP` 384-d mE5-small | **Yes** `bm25_index.pkl` 17 MB, `bm25_corpus_tok.pkl` 4.7 MB, `nodes.faiss` 8.7 MB, `embeddings.npy` 8.7 MB, `index_sha256.txt` 109 B | `backend/ml_assets/rag_index/indexes/` | Correct. Cite hashes. |
| 6 vision classifiers (rice 8 / corn 4 / potato 3 / brassica 11 / wheat 11) | **Yes** 6 `model.pt` (3.0–12.0 MB each) + `class_names.json` each, `verification_report_live.md` | `backend/ml_assets/vision/*/` | Correct, all `task: classify`. Never claim boxes. |
| Soil 722 imgs, 6 types, EfficientNet-B0 5-fold | **Partial** — `dataset_release/soil_moisture/` has **13** jpgs (1 preview + 12 thumbnails), **not 722**. **722 are in `dataset_release/soil-moisture-detection/dataset/{raw,clean}/` (722 each, 956 MB, gitignored)** + 5×16.9 MB `effnetb0_fold*.pt` in `backend/ml_assets/soil/` | `dataset_release/soil-moisture-detection/dataset/raw/P0001_8Kpa.jpg` etc | **Write "722 raw in `soil-moisture-detection` (ignored), 13 frozen thumbnails in `soil_moisture` (tracked)" — do not claim 722 in `soil_moisture`.** |
| 20,112 safety (3,216 T3 + 16,896 T4) 6 dialects | **RECOVERED 2026-08-21** — pulled from HuggingFace `RaiyanKhaan/krishokChat/safety_qa/`: `t3_refusal.jsonl` 3,216 lines sha256 `27acdb64…` + `t4_requery.jsonl` 16,896 lines sha256 `a578023…` + `slots.json`/`taxonomy.json`; field-verified 6 dialects × 536 (T3) / × 2,816 (T4), 12 categories, 9 patterns | `dataset_release/safety/t3_refusal.jsonl` etc | **Claim allowed with hashes** — write 20,112 (3,216+16,896), cite `12_ASSET_VERIFICATION.md` §4. |
| Gemma 4B 4-bit GGUF | **Yes** `krishokchat.f16.gguf` 1.36 GB hardlinked to `model.gguf`, SHA `1D627304F745`, but **truncated** (must not serve) per `PROJECT_HANDOFF.md`. Verified runtime is external Q4_K_M + LoRA via `tools/ops/start_krishokchat_local.ps1`. | `backend/ml_assets/gemma/` | Correct, with truncation note. |
| 16123 helpline | **Yes** — safety policy canned redirect, audit logs it. | `backend/app/domain/safety_policy.py` | Correct. |

**Rule:** If a number is not on disk, write `TODO` or `per HuggingFace` — never invent.

---

## 2. Folder Map — 12 Files (read in order)

| File | Angle | Why it exists | Key verified gap |
|---|---|---|---|
| `00_SCOPE_AND_ANGLES.md` | Master list: 9 clusters, 36 angles, 2025→2026-08 priority | Entry point — tells scouts what to hunt | — |
| `01_agentic_rag_verifier_systems.md` | Agentic RAG + verifier (Cluster 1) | System-track core: claim-level verifier, RAGChecker | Gap A: no agri claim-verifier |
| `02_llm_safety_low_resource.md` | Safety guardrails, Bengali gap (Cluster 2) | Guardrail models miss Bengali agrochemical | Gap B: no multi-dialect Bangla safety |
| `03_low_resource_nlp_bengali.md` | Bengali LLMs, dialects, synthetic data (Cluster 3) | BanglaLLM, BUNO, code-mixing | Gap D: no dialect→retrieval eval |
| `04_agri_ai_advisory_systems.md` | Farmer.Chat, AgriEval, deployment (Cluster 4) | Closest-domain systems | Gap C: no helpline escalation measured |
| `05_vision_crop_disease.md` | VLM vs supervised, calibration/OOD (Cluster 5) | Vision conventions | Gap F: no vision→grounded-treatment loop |
| `06_system_industry_track_conventions.md` | ACL/EMNLP/KDD/NeurIPS acceptance criteria (Cluster 6) | How system papers pass | — |
| `07_retrieval_low_resource_rag_eval.md` | MIRACL-bn, MILCO, RAGAS, CiteEval (Cluster 7) | Retrieval eval | Gap D/E: no nDCG by dialect |
| `08_edge_slm_streaming_systems.md` | Gemma 4, BnMMLU, TTFT/TBT (Cluster 8) | SLM + streaming | Gap E: no TTFT/verifier tradeoff |
| `09_ict4d_global_south.md` | 60dB, AIEP, RCT, helpline (Cluster 9) | Field evaluation | Gap C/E-G3: no field/UX eval |
| `10_SYNTHESIS_GAPS_POSITIONING.md` | **Synthesis: 6 gaps (A–F) + positioning + track ladder** | **Write paper from this** | — |
| `11_RESEARCH_GAPS_competitive_matrix.md` | Formal gap objects (calibration, taxonomy, safety-monotone) | Defensible novelty | — |
| `12_ASSET_VERIFICATION.md` | **This verification table (new)** | **Grounds every number** | — |

**No duplicates:** `LITERATURE_REVIEW.md` at root archived to `paper/archive/`, `system_evolution_plan_2026/` archived, `__pycache__` removed. `paper/` now 4 folders only.

---

## 3. How to Use While Writing (Expert Systems application track)

1. **Start from the R1 skeleton** — `paper/manuscript/expert-systems-skeleton.md` is the single SSOT (**venue locked 2026-08-21: Wiley Expert Systems journal**). `10`'s old ACL-demo positioning statement is superseded history — do NOT copy it. Every section maps to a cluster file.
2. **For each section, cite from its cluster file:** e.g., Related Work → `04` (Farmer.Chat, KrishokBondhu, 2601.02065) + `01` (verifier) + `02` (safety). Do not invent papers — each cluster file lists real 2025-2026 venue/year/title.
3. **For every number, check `12` first** — if `12` says TODO/missing, write TODO in manuscript, not a fake number.
4. **Before claiming novelty, check `11`** — its 3 formal gap objects are the defensible claims (calibration, taxonomy, safety-monotone). No other competitor has them.

**Enforcement:** `docs/PAPER_POLICY.md` — grep `2606.29243` must return 0 outside allowlist (enforced in CI `paper-policy` job per `d02efdc`).

---

## 4. Non-Repetitive Guarantee

* `00` is the only master list — `01-09` never repeat `00`'s angles, only deepen one cluster.
* `10` is the only synthesis — `11` is formal objects, `12` is asset verification; no overlap.
* `system_evolution_plan_2026/` is archived — not read while writing, only `10`/`11` are.

**Next:** Run `R2` benchmark freeze + `R3` ablation + `R4` human study to convert gaps D/E/A/B into results — then fill `expert-systems-skeleton.md` §5-6.
