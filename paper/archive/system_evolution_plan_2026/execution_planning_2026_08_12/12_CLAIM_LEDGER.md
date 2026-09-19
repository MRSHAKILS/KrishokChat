# Claim Ledger

## Safe Claims

| ID | Safe claim | Evidence | Allowed wording |
|---|---|---|---|
| S01 | The captured runtime wires BM25 as its only retriever. | `../T04_BEHAVIOR_SNAPSHOT.md:10-20`; active code references there | "The evaluated runtime uses BM25 retrieval." |
| S02 | The captured verifier normalizes limited Bengali/English dosage forms and performs source substring matching. | `../T04_BEHAVIOR_SNAPSHOT.md:22-32` | "The current verifier is a normalized lexical dosage matcher." |
| S03 | Safety classification precedes retrieval, and terminal/error outcomes fail closed in the captured tests. | `../T04_BEHAVIOR_SNAPSHOT.md:34-54,159-173` | "The pipeline enforces safety before retrieval in the captured revision." |
| S04 | JSON and SSE endpoints share one QA pipeline in the captured revision. | `../T04_BEHAVIOR_SNAPSHOT.md:56-62` | "Both transports use the same QA use case." |
| S05 | Checked vision artifacts perform classification and return no boxes. | `../T02_T03_ARTIFACT_INVENTORY.md:161-229`; `../T04_BEHAVIOR_SNAPSHOT.md:64-72` | "The vision workflow performs crop and disease classification, not localization." |
| S06 | The current vision fallback can label source-empty treatment text as verified. | `../T04_BEHAVIOR_SNAPSHOT.md:74-83` | "A verified-status provenance defect exists in the fallback path." |
| S07 | ~~The benchmark endpoint is a placeholder.~~ **SUPERSEDED by S12 (2026-08-14).** | `../T04_BEHAVIOR_SNAPSHOT.md:85-97` | See S12. |
| S08 | A local LoRA adapter artifact exists with recorded hashes and metadata. | `../T02_T03_ARTIFACT_INVENTORY.md:246-272` | "A local adapter checkpoint is present." Do not add performance wording. |
| S09 | Root `dataset_release/` was not found during the artifact inventory. | `../T02_T03_ARTIFACT_INVENTORY.md:345-355` | "The inventory did not find a root dataset release directory." |
| S10 | Broad A and broad B are rejected by the 2026-08-12 adjudication. | `02_NOVELTY_ATTACK.md`; `03_THESIS_DECISION.md` | "The work tests a narrow combined setting rather than claiming general method priority." |
| S11 | **Hybrid RRF retrieval (BM25 + BGE-M3 dense FAISS) is the default runtime path** (2026-08-14, supersedes F01). Offline index: 2,135 nodes, sha256 `0f6f711829…cb524`. Expansion hit rate measured 0.6% (6/1,000). Smoke eval coverage-only. | commits `9358def`; `backend/app/infrastructure/retrieval/{hybrid,dense,bm25,expansion}.py`; `backend/ml_assets/rag_index/eval/hybrid_smoke.json`; live audit `retrieval_top1_score 0.0476`; `17_FINDINGS_LOG_2026_08_14.md` F5 | "Hybrid RRF retrieval is the default runtime path; expansion hit rate 0.6% on 1,000 farmer queries." No recall/relevance wording (judgments pending). |
| S12 | **`GET /api/benchmark` serves PRECOMPUTED golden-benchmark stats** (supersedes S07/F05). Artifact: `dataset_release/benchmark/golden_stats_v1.json` from `11_publish_golden_stats.py`. | commit `684886b`; `backend/app/api/benchmark.py`; `17_FINDINGS_LOG_2026_08_14.md` F1–F3 | "The benchmark endpoint serves precomputed offline evaluation artifacts; it computes nothing live." |
| S13 | **Golden probe: 0/12 out-of-corpus questions refused** (dangerous non-abstention; P4 DoD ≥90% unmet). All 12 answered with 5 sources, verifier `verified`. | `dataset_release/benchmark/golden_runs_v1.json`; `17_FINDINGS_LOG_2026_08_14.md` F3 | "In a 46-item golden probe, all 12 out-of-corpus questions received answers; the runtime does not abstain on missing evidence." |
| S14 | Verifier flagged 6/46 golden answers (`flagged-unverified`, unsupported numeric claims); flagged answers still displayed (annotate-and-drop). | `dataset_release/benchmark/golden_runs_v1.json`; F2 | "The verifier flags unsupported dosage claims; flagged answers remain displayed with annotation." |
| S15 | **RRF top1 audit scores are quantized** (1/(20+rank) steps); dense/BM25 raw scores do NOT separate unanswerable from answerable queries (overlapping distributions). | `backend/ml_assets/rag_index/eval/golden_retrieval_probe.json`; F4 | "Retrieval-score magnitude alone cannot gate abstention." |
| S16 | Golden set provenance: 46 rows from 1,001 real farmer queries, pinned sample, 3-pass reviewed categories; `gold_answer` fields are `expert_provided: false` (pipeline-generated). | `dataset_release/benchmark/golden_qa_v1.jsonl`; F1 | "The golden set is human-categorized; answer correctness awaits two-evaluator scoring." |
| S17 | **Deterministic corpus-coverage gate (D1a) shipped in the safety precheck** (2026-08-14): six keyword families (training incl. farmer typo `প্রশিক্ষন`, export, availability, institutional, livestock incl. Banglish `koel palon`, government assistance) → `low_confidence` terminal refusal with the 16123 referral, ordered AFTER self-harm/injection/banned rules. Post-D1a forced golden re-run (46/46 fresh): **unanswerable refused 12/12, off-topic 2/2, answerable refused by gate 0/32** (q75 banned-chemical refusal unchanged); live probe + audit `safety_matched_rules` recorded. Gate is keyword-scoped, not semantic — unseen out-of-corpus intents remain unmeasured. | commit (D1a); `backend/app/domain/safety_policy.py`; `backend/tests/test_coverage_gate.py`; `dataset_release/benchmark/golden_runs_v1.json`; `17_FINDINGS_LOG_2026_08_14.md` F10 | "The runtime refuses out-of-corpus queries matching the deterministic coverage gate (14/14 in the golden probe; 0/32 answerable refused)." Do NOT claim gate coverage of all out-of-corpus queries (unmeasured). |

## Forbidden Claims

| ID | Forbidden claim | Reason/source |
|---|---|---|
| F01 | Hybrid BM25+dense retrieval is active. **SUPERSEDED by S11 (2026-08-14, commit `9358def`)** — hybrid RRF is now the default; row kept for history. | Dense/FAISS files are absent and the container wires BM25 only: T02/T03 and T04. |
| F02 | The current verifier is semantic, relation-aware, or calibrated. | T04 shows regex/substring logic and categorical labels without calibration. |
| F03 | Safety data are present under root `dataset_release/`. | T02/T03 did not find that directory. |
| F04 | Vision fallback treatment is source verified. | T04 reproduces `verified` with empty sources. |
| F05 | The benchmark endpoint serves computed or precomputed results. **SUPERSEDED by S12 (2026-08-14)** — it now serves precomputed stats. | T04 shows `not_implemented`. |
| F06 | Local Gemma achieves any quality, safety, latency, or benchmark value. | Checkpoint presence is not an inference evaluation. |
| F07 | Current vision artifacts detect/localize disease or produce bounding boxes. | Artifacts report classification and boxes are empty. |
| F08 | KrishokTech is the first agricultural claim verifier, first selective certifier, first Bengali agricultural RAG system, or first dialect/Banglish RAG study. | Direct literature threats in `02_NOVELTY_ATTACK.md`. |
| F09 | Normalization improves safety because it improves retrieval. | E4/E5 require independent safety invariance; the relation is not assumed. |
| F10 | An LLM judge supplies gold labels or proves factuality. | Expert labels are required by the protocol. |
| F11 | Any PDF-extracted number is verified before T05 reconciliation. | `../T01_PDF_EXTRACTION.md:8-10`. |
| F12 | UI traces, local audit counts, or demo behavior prove farmer benefit, trust, usability, or agronomic outcomes. | No controlled human/outcome study supports these claims. |
| F13 | The system abstains when evidence is missing / refuses out-of-corpus queries. | Golden probe shows 0/12 unanswerable refused (S13). **Partially superseded by S17 (2026-08-14):** refusal now holds for queries matching the deterministic coverage gate (keyword-scoped). The general claim remains FORBIDDEN — semantic abstention on unseen out-of-corpus intents is unmeasured (F10). |
| F14 | The golden answers are expert-verified / expert gold. | `expert_provided: false` provenance; scoring pending (S16). |
| F15 | Unanswerable refusal rate meets the ≥90% P4 target. | Measured 0% (S13). **Superseded by S17 (2026-08-14):** post-D1a measurement is 12/12 (100%) on the pinned golden set — report the measured value, do not assert a standing capability. |
| F16 | Retrieval-score thresholds gate abstention / recall improved. | Probe shows overlapping distributions; no relevance judgments (S15, F4). |
| F17 | Dialect normalization evaluated / expansion effective. | **Updated 2026-08-15 (C3, F15):** original 110-word map unrecoverable; a 16-pair map was DERIVED deterministically from frozen reviewed T09 splits (zero LLM) — expansion hits on real T09 dialect questions (dev+test, 3,628): 1/3,628 (0.03%) → 1,215/3,628 (33.49%). Claim scope: dialectal-morphology normalization only; Banglish (Romanized) input remains uncovered (F14 floor); do not compare the 0.6% (benchmark population) with 33.49% (T09 population) directly. |

## TODO and Unverified Claims

| ID | Claim/status | Required proof | Source path/URL |
|---|---|---|---|
| U01 | Local-PDF dataset sizes, splits, model results, percentages, and sample properties: **NEEDS RECONCILIATION**. | T05 artifact-level path, hash, count/query method, conflict resolution. | `../T01_PDF_EXTRACTION.md`; authoritative filenames listed in root policy. |
| U02 | Safety parent/split mismatch interpretation. | Record membership analysis and released-split policy; do not assume omitted records' role. | `../T02_T03_ARTIFACT_INVENTORY.md:22-33`. |
| U03 | Stable evidence spans can be reconstructed for enough agrochemical claims. | T05/T07 source-ID and offset audit. | In-repo RAG corpora and external treatment resources inventoried in T02/T03. |
| U04 | Structured verifier improves dangerous non-abstention. | E1 frozen test with expert gold and paired inference. **Preliminary (2026-08-14):** golden probe shows dangerous non-abstention 12/12 on out-of-corpus items and the verifier passes non-dose claims (F3) — motivates the fix, proves nothing. | `dataset_release/benchmark/golden_runs_v1.json`; `17_FINDINGS_LOG_2026_08_14.md` F3. |
| U05 | Calibration meets risk/coverage constraints. | E2 development-only fit and untouched test. | `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`. |
| U06 | Dictionary normalization improves retrieval while preserving safety. | E4/E5 paired native-reviewed study. | BanglaLP/FIRE threat URLs in `02_NOVELTY_ATTACK.md`. |
| U07 | Optional NLI adds value. | E8 accuracy, latency, reproducibility, and safety gates. | Generic verification threats in `02_NOVELTY_ATTACK.md`. |
| U08 | A learned normalizer is justified. | Dictionary development gap plus all learned-normalizer gates. | `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`. |
| U09 | Narrow combination remains distinct after full-text literature verification. | T07 bibliography archive and method/result comparison. | All URLs in `02_NOVELTY_ATTACK.md`. |
| U10 | Integrated system-level safety improves. | Vision repair, verifier integration, and T23 expert evaluation. **Preliminary (2026-08-14):** 45/46 golden runs safety-categorized; 1 policy refusal pending expert review (Q1); dangerous non-abstention blocks any improvement claim (F3). | T04 defect evidence and `08_FINAL_SYSTEM_ARCHITECTURE_CONTRACT.md`; `17_FINDINGS_LOG_2026_08_14.md` F2–F3. |

## Citation Sources

- Local implementation and artifact claims cite repository paths and hashes.
- Authoritative KrishokTech papers may be referenced only by the filenames/paths allowed in `docs/PAPER_POLICY.md` until public identifiers are supplied.
- Literature claims use the URLs listed in `02_NOVELTY_ATTACK.md` after T07 full-text verification.
- Do not promote a TODO by repeating it in prose. Update this ledger with a run or artifact ID first.
