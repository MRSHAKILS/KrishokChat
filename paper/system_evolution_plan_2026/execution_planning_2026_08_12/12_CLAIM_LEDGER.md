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
| S07 | The benchmark endpoint is a placeholder. | `../T04_BEHAVIOR_SNAPSHOT.md:85-97` | "Research metrics are generated offline; the endpoint is not an evidence source." |
| S08 | A local LoRA adapter artifact exists with recorded hashes and metadata. | `../T02_T03_ARTIFACT_INVENTORY.md:246-272` | "A local adapter checkpoint is present." Do not add performance wording. |
| S09 | Root `dataset_release/` was not found during the artifact inventory. | `../T02_T03_ARTIFACT_INVENTORY.md:345-355` | "The inventory did not find a root dataset release directory." |
| S10 | Broad A and broad B are rejected by the 2026-08-12 adjudication. | `02_NOVELTY_ATTACK.md`; `03_THESIS_DECISION.md` | "The work tests a narrow combined setting rather than claiming general method priority." |

## Forbidden Claims

| ID | Forbidden claim | Reason/source |
|---|---|---|
| F01 | Hybrid BM25+dense retrieval is active. | Dense/FAISS files are absent and the container wires BM25 only: T02/T03 and T04. |
| F02 | The current verifier is semantic, relation-aware, or calibrated. | T04 shows regex/substring logic and categorical labels without calibration. |
| F03 | Safety data are present under root `dataset_release/`. | T02/T03 did not find that directory. |
| F04 | Vision fallback treatment is source verified. | T04 reproduces `verified` with empty sources. |
| F05 | The benchmark endpoint serves computed or precomputed results. | T04 shows `not_implemented`. |
| F06 | Local Gemma achieves any quality, safety, latency, or benchmark value. | Checkpoint presence is not an inference evaluation. |
| F07 | Current vision artifacts detect/localize disease or produce bounding boxes. | Artifacts report classification and boxes are empty. |
| F08 | KrishokChat is the first agricultural claim verifier, first selective certifier, first Bengali agricultural RAG system, or first dialect/Banglish RAG study. | Direct literature threats in `02_NOVELTY_ATTACK.md`. |
| F09 | Normalization improves safety because it improves retrieval. | E4/E5 require independent safety invariance; the relation is not assumed. |
| F10 | An LLM judge supplies gold labels or proves factuality. | Expert labels are required by the protocol. |
| F11 | Any PDF-extracted number is verified before T05 reconciliation. | `../T01_PDF_EXTRACTION.md:8-10`. |
| F12 | UI traces, local audit counts, or demo behavior prove farmer benefit, trust, usability, or agronomic outcomes. | No controlled human/outcome study supports these claims. |

## TODO and Unverified Claims

| ID | Claim/status | Required proof | Source path/URL |
|---|---|---|---|
| U01 | Local-PDF dataset sizes, splits, model results, percentages, and sample properties: **NEEDS RECONCILIATION**. | T05 artifact-level path, hash, count/query method, conflict resolution. | `../T01_PDF_EXTRACTION.md`; authoritative filenames listed in root policy. |
| U02 | Safety parent/split mismatch interpretation. | Record membership analysis and released-split policy; do not assume omitted records' role. | `../T02_T03_ARTIFACT_INVENTORY.md:22-33`. |
| U03 | Stable evidence spans can be reconstructed for enough agrochemical claims. | T05/T07 source-ID and offset audit. | In-repo RAG corpora and external treatment resources inventoried in T02/T03. |
| U04 | Structured verifier improves dangerous non-abstention. | E1 frozen test with expert gold and paired inference. | `05_MINIMUM_EXPERIMENT_MATRIX.md`. |
| U05 | Calibration meets risk/coverage constraints. | E2 development-only fit and untouched test. | `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`. |
| U06 | Dictionary normalization improves retrieval while preserving safety. | E4/E5 paired native-reviewed study. | BanglaLP/FIRE threat URLs in `02_NOVELTY_ATTACK.md`. |
| U07 | Optional NLI adds value. | E8 accuracy, latency, reproducibility, and safety gates. | Generic verification threats in `02_NOVELTY_ATTACK.md`. |
| U08 | A learned normalizer is justified. | Dictionary development gap plus all learned-normalizer gates. | `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`. |
| U09 | Narrow combination remains distinct after full-text literature verification. | T07 bibliography archive and method/result comparison. | All URLs in `02_NOVELTY_ATTACK.md`. |
| U10 | Integrated system-level safety improves. | Vision repair, verifier integration, and T23 expert evaluation. | T04 defect evidence and `08_FINAL_SYSTEM_ARCHITECTURE_CONTRACT.md`. |

## Citation Sources

- Local implementation and artifact claims cite repository paths and hashes.
- Authoritative KrishokChat papers may be referenced only by the filenames/paths allowed in `docs/PAPER_POLICY.md` until public identifiers are supplied.
- Literature claims use the URLs listed in `02_NOVELTY_ATTACK.md` after T07 full-text verification.
- Do not promote a TODO by repeating it in prose. Update this ledger with a run or artifact ID first.
