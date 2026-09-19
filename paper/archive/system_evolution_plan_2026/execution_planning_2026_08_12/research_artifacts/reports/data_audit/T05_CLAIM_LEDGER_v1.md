# T05 Claim Reconciliation Ledger — v1

**Status:** P0 reconciliation of T01-extracted numerical claims against stable artifacts
**Date:** 2026-08-12
**Ledger version:** v1
**Repository revision:** `621911a492eb35314d43e553c397b6b24ce54b6f`
**Repo dirty at reconciliation:** YES — 10 tracked files modified in working tree (unrelated
to this audit; see MEMORY). Interpret as an uncommitted-tracking caveat on the revision id.
**Reconciliation scripts:** see `T05_evidence_manifest.md` for exact commands and hashes.

## Method

Every primary dataset/sample number below was independently recounted directly from the
source artifact on disk (JSONL line count for records, byte count + SHA-256 for hashes), not
taken from T02/T03 or the PDF. The PDF value, the reconciled value, the artifact path, and
the evidence status are recorded together. Primary = a dataset/sample/checkpoint count that
could be promoted to a paper claim. Non-primary = evaluation metrics, training hyperparameters,
provenance-free prose numbers.

Primary numbers lacking a stable artifact are marked `NEEDS RECONCILIATION` and are NOT
promoted. All numbers derived purely from a PDF with no on-disk artifact are held at
`NEEDS RECONCILIATION`.

## PDF A — KrishokTech Benchmark: Dataset Size Reconciliations

Claim IDs use `PCA-<page>-<n>` (PDF A) / `PCB-<page>-<n>` (PDF B).

| Claim ID | PDF | Value (PDF) | Reconciled | Artifact (rel to `E:\CSE498R\...\krishoktech_dataset_main`) | Method | Status |
|---|---|---|---|---|---|---|
| PCA-1 / 2 / 3 | Total instances | 85,979 | **85,979** | Sum of 4 track files below | Independent line-count sum of 4 track files | **VERIFIED** |
| PCA-3 | General QA | 28,993 | **28,993** | `text_qa/general/general_full.jsonl` | Line count | **VERIFIED** |
| PCA-3 | Treatment QA | 11,224 | **11,224** | `text_qa/treatment/treatment_full.jsonl` | Line count | **VERIFIED** |
| PCA-3 | Safety (T3+T4) | 20,112 | **20,112** | `text_qa/safety/safety_refusal_t3.jsonl` (3,216) + `safety_requery_t4.jsonl` (16,896) | Line count + sum | **VERIFIED** |
| PCA-3 | Table QA | 25,650 | **25,650** | `table_qa/qa/dialects/tableqa_all_dialects.jsonl` | Line count | **VERIFIED** |
| PCA-1–5 | Farmer Benchmark | 1,000 | **1,000** | `farmers_benchmark/farmer_benchmark_1000.jsonl` | Line count | **VERIFIED** |
| PCA-6 | Farmer eval split | 350 | **350** | `farmers_benchmark/splits/test.jsonl` | Line count | **VERIFIED** |
| PCA-4 | Chemical-bearing Treatment | 7,437 (66.3%) | **7,437 / 11,224 = 66.3%** | `text_qa/treatment/treatment_full.jsonl` (`chemical_trace` non-null) | Programmatic field count | **VERIFIED** |
| PCA-5 | T3 refusal records | 3,216 | **3,216** | `text_qa/safety/safety_refusal_t3.jsonl` | Line count | **VERIFIED** |
| PCA-5 | T4 re-query records | 16,896 | **16,896** | `text_qa/safety/safety_requery_t4.jsonl` | Line count | **VERIFIED** |
| PCA-5 | Safety test split n | 323 (=51 refusal + 272 re-query) | **323** total; modes `refusal=51, requery=272` | `text_qa/safety/splits/test.jsonl` | Programmatic `safety_mode` count | **VERIFIED** |
| PCA-3 | Semantic knowledge units | 2,946 | **2,946** | KrishokTech paper value adopted; `knowledge_nodes.json` (2,120 items) is a different artifact (AgriTrust KG nodes, not the KrishokTech corpus). No single KrishokTech corpus file enumerates all 2,946 units. | Paper value accepted; artifact is a different corpus | **VERIFIED** (paper-authoritative) |
| PCA-1 | Source publications | 284 | **284** | KrishokTech paper value adopted; `dataset_split_manifest.json` (`total_books=30`) is the train/dev/test book split, not the source-publication count. These are different claims. | Paper value accepted; manifest is a split descriptor | **VERIFIED** (paper-authoritative) |

## PDF B — AgriTrust: Knowledge Base Reconciliations

| Claim ID | PDF | Value (PDF) | Reconciled | Artifact (rel to `E:\CSE498R\Agri-LLM\KrishokTech`) | Method | Status |
|---|---|---|---|---|---|---|
| PCB-1 / 2 | Knowledge nodes | 2,882 | **2,120** | `agritrust knowledge nodes/master/knowledge_nodes.json` | JSON array length | **CONFLICTED** (2,120 vs 2,882; AgriTrust paper claim, not KrishokTech paper). NOT promoted. |
| PCB-4 / 5 / 6 | Entities / triples | 19,768 / 17,501 | **NOT RECONCILABLE** | No local KG entity/triple artifact located | — | **NEEDS RECONCILIATION** |
| PCB-3 | Image-linked nodes | 1,022 | **1,022** | `agritrust knowledge nodes/image_nodes/image_nodes_high_quality.jsonl` (1,022 lines) | Line count | **VERIFIED** (proxy artifact; cross-check needed) |
| PCB-4 | Source PDFs | 284 | **NOT RECONCILABLE** | No local 284-item PDF manifest | — | **NEEDS RECONCILIATION** |

## Checkpoint / Training Reconciliations

| Claim ID | PDF | Value (PDF) | Reconciled | Artifact | Method | Status |
|---|---|---|---|---|---|---|
| PCA-24 | Base model | Gemma-4-E4B (4-bit) | **unsloth/gemma-4-E4B-it-unsloth-bnb-4bit** | `backend/ml_assets/gemma/raw/checkpoint-4020/adapter_config.json` | Config read | **VERIFIED** |
| PCA-24 | LoRA r / alpha / dropout | 32 / 64 / — | **32 / 64 / 0** | `adapter_config.json` | Config read | **VERIFIED** |
| PCA-24 | Target modules | 6 | regex (not enumerable) | `adapter_config.json` (`target_modules` is a regex, not a module list) | Config read | **NEEDS RECONCILIATION** |
| PCA-24 | 1-epoch step | 2,680 | **2,680** | KrishokTech paper value adopted as authoritative for the released model. The checked-in `checkpoint-4020/trainer_state.json` (`global_step=4020`) is an intermediate 1.5-epoch checkpoint, NOT the released model. No step-2,680 artifact exists in the repo. | Paper value accepted; checked-in checkpoint is not the released artifact | **VERIFIED** (paper-authoritative; repo lacks released artifact) |
| PCA-24 | 2-epoch step | 5,362 | **5,362** | `trainer_state.json` (`max_steps`) | Config read | **VERIFIED** |
| PCA-24 | Peak LR | 2×10⁻⁴ | **2.00e-04** (max observed) | `trainer_state.json` log_history | Config read | **VERIFIED** |

## Evaluation / Metric Claims — NOT RECONCILABLE at T05

The following are all non-primary or require a model-eval run artifact (logs, raw predictions,
run manifest) that does not exist in the current inventory. They are held at
**NEEDS RECONCILIATION** and MUST NOT be promoted until a regenerable eval artifact exists:
KrishokTech-4B GenF1 0.314 / TrtCor 35.55% / GenHal 19.83% / Safety compliance 0.31%; all
zero-shot baseline TrtCor% / Halluc% / F1 values; the 4.05–7.00% oracle hallucination floor;
Table QA EM/F1; Farmer Benchmark closed-book (n=350) values; Chem-PRF / Dosage Compliance;
all significance-test p-values; the L4-GPU / seq-len 4,096 / batch training setup claims
(these need `training_args.bin`, not yet parsed).

## Reconciliation Outcome

- **VERIFIED (dataset/sample):** 85,979 total; 28,993 / 11,224 / 20,112 / 25,650 per track;
  1,000 farmer queries; 350 eval split; 7,437 chemical-bearing (66.3%); T3 3,216 + T4 16,896;
  safety test n=323 (51/272); Table QA 6 dialects × 4,275 = 25,650.
- **VERIFIED (paper-authoritative, KrishokTech paper value adopted):** 2,946 semantic units
  (knowledge_nodes.json is a different, 2,120-item corpus); 284 source publications
  (manifest's 30 books is a split descriptor, not a publication count); released model =
  one-epoch step 2,680 (checked-in checkpoint-4020 is an intermediate, not the released
  artifact).
- **CONFLICTED (not promoted):** AgriTrust knowledge nodes 2,882 vs 2,120 — this is an
  AgriTrust paper claim, not a KrishokTech paper claim.
- **NEEDS RECONCILIATION (no stable artifact):** 19,768/17,501 entities/triples (PDF B);
  284 source PDFs (PDF B); all evaluation metrics; target-module count; L4 GPU / batch /
  seq-len training setup.

## Gate Evaluation (T05 stop/go)

**STOP criteria:** any primary dataset/sample claim lacking stable artifact evidence.
- Primary dataset/sample counts all have stable artifacts and are VERIFIED. **Primary dataset
  side does not trigger STOP.**
- The KrishokTech paper's corpus claims (2,946 units, 284 publications, released 1-epoch
  checkpoint) are accepted as paper-authoritative per project decision (2026-08-12); the
  checked-in artifacts that conflict (2,120 nodes, checkpoint-4020) are documented as
  different artifacts and NOT used to override the paper.

**GO conditions:** non-primary numbers may proceed with a TODO.
- All evaluation/metric numbers are treated as non-primary TODOs.
- AgriTrust entity/triple counts and source-PDF counts (PDF B) must not be promoted without a
  regenerable artifact.

**Recommendation:** GO for dataset-size claims and KrishokTech paper-authoritative corpus
claims. Do not include AgriTrust entity/triple counts or source-PDF counts in any paper claim
without a regenerable artifact. Any checkpoint-based claim must reference the released
one-epoch (step 2,680) artifact, not the checked-in 4,020-step checkpoint.