# T05 Reconciliation Evidence Manifest — v1

**Date:** 2026-08-12
**Ledger:** `T05_CLAIM_LEDGER_v1.md`
**Repo revision:** `621911a492eb35314d43e553c397b6b24ce54b6f`

This manifest records the exact commands and on-disk artifacts used to reconcile each number
in the ledger. All counts below are independent re-derivations (line counts / field counts /
config reads), not copies of T02/T03.

## 1. Dataset file line counts + SHA-256 (external corpus)

Root: `E:\CSE498R\Agri-LLM\KrishokChat\krishokchat_dataset_main`

| File | Lines | Size (bytes) | SHA-256 (first 16) | Matches T02? |
|---|---|---|---|---|
| `farmers_benchmark/farmer_benchmark_1000.jsonl` | 1,000 | 5,648,266 | `e2adc30d69aed9de...` | Yes |
| `farmers_benchmark/splits/test.jsonl` | 350 | 2,122,297 | `69ce51e70bc1ed04...` | Yes |
| `text_qa/safety/safety_refusal_t3.jsonl` | 3,216 | 3,636,107 | `27acdb644c9e3794...` | Yes |
| `text_qa/safety/safety_requery_t4.jsonl` | 16,896 | 15,854,076 | `a578023429cf3cc4...` | Yes |
| `text_qa/safety/splits/dev.jsonl` | 2,025 | 1,977,155 | `7be6cc2014cf58af...` | Yes |
| `text_qa/safety/splits/test.jsonl` | 323 | 307,261 | `96101a6ed1e8ec96...` | Yes |
| `text_qa/safety/splits/train.jsonl` | 16,070 | 15,572,076 | `13115239ef8e1bd0...` | Yes |
| `text_qa/general/general_full.jsonl` | 28,993 | 40,490,278 | `6ee95fe936e830aa...` | Yes |
| `text_qa/treatment/treatment_full.jsonl` | 11,224 | 22,026,143 | `dc9b87a04dd49680...` | Yes |
| `table_qa/qa/tableqa_all.jsonl` | 9,022 | 6,904,746 | `26e3a9f6e93cc15d...` | Yes |
| `table_qa/qa/dialects/tableqa_all_dialects.jsonl` | 25,650 | 17,040,666 | `ba8362ad37d05011...` | Yes |
| `image_qa/image_qa_pairs.jsonl` | 2,045 | 5,306,535 | `5829d1a53ad080ce...` | Yes |
| `markdown_corpus/qa/complete_queries.jsonl` | 1,536 | 1,613,671 | `073c83aa62aa8c2d...` | Yes |
| `markdown_corpus/qa/critical_treatment.jsonl` | 2,190 | 5,361,262 | `414d17f5ecd1a210...` | Yes |
| `markdown_corpus/qa/general_sft_diverse_full.jsonl` | 28,993 | 34,923,017 | `d8a32c3a32328291...` | Yes |
| `markdown_corpus/retriever/retriever_train.jsonl` | 9,231 | 73,865,004 | `5a8ff2e45dcccaf4...` | Yes |

Hashing/counting method: read file in 1 MiB blocks, `hashlib.sha256`; line count skipped blank
lines (`if line.strip()`).

## 2. Derived reconciliations

| Check | Result | Source |
|---|---|---|
| Total 4-track instances | 28,993 + 11,224 + (3,216+16,896) + 25,650 = **85,979** | line-count sums |
| Treatment chemical-bearing | 7,437 / 11,224 = **66.3%** (non-null `chemical_trace`) | programmatic field count |
| Safety test split modes | n=**323**, `refusal=51`, `requery=272` | programmatic `safety_mode` count |
| Safety splits sum | dev 2,025 + test 323 + train 16,070 = **18,418** vs parent 20,112 → **skew 1,694** (splits are a proper subset) | line-count sums |
| Table QA dialects | 6 dialects × **4,275** = 25,650 (standard/sylheti/chittagonian/noakhailli/rangpuri/barishal) | programmatic `dialect` count |
| Farmer benchmark channels | `field_sourced_farmer=300`, `fb_group_real_farmer=483`, `krishibangla.com=217`, total 1,000 | programmatic `metadata.source` count |

## 3. Knowledge base + checkpoint

- `agritrust knowledge nodes/master/knowledge_nodes.json` → JSON array length **2,120** (PDF B
  claims 2,882 → **CONFLICTED**).
- `agritrust knowledge nodes/image_nodes/image_nodes_high_quality.jsonl` → **1,022** lines
  (matches PDF B image-linked node claim).
- `backend/ml_assets/gemma/raw/checkpoint-4020/adapter_config.json`:
  `base=unsloth/gemma-4-E4B-it-unsloth-bnb-4bit`, `r=32`, `lora_alpha=64`, `lora_dropout=0`,
  `peft_type=LORA`, `task_type=CAUSAL_LM`, `target_modules` is a **regex** (not enumerable).
- `backend/ml_assets/gemma/raw/checkpoint-4020/trainer_state.json`:
  `global_step=4020`, `max_steps=5362`, `epoch=1.499...`, `learning_rate` observed
  max=`2.00e-04`, min=`6.72e-06`.
- **Finding:** checked-in checkpoint is an intermediate 1.5-epoch (step 4,020) checkpoint,
  not the released one-epoch (step 2,680) model. Bucketed as **CONFLICTED** for the
  "released = 1-epoch" claim.

## 4. Gate result

- All primary dataset/sample counts VERIFIED against stable artifacts.
- STOP avoided for dataset-size claims (all have artifacts).
- **Conflict resolution (project decision, 2026-08-12):** where the KrishokChat paper makes a
  claim (2,946 semantic units; 284 source publications; released one-epoch step-2,680 model),
  the paper's value is adopted as authoritative. Conflicting on-disk artifacts (2,120
  knowledge nodes; checkpoint-4020 at step 4,020) are documented as different artifacts, not
  used to override the paper, and not promoted in their place.
- AgriTrust-specific claims (2,882 nodes; 19,768/17,501 entities/triples; 284 source PDFs)
  remain NOT promoted — they are not KrishokChat paper claims and lack matching artifacts.
- Evaluation/metric numbers are non-primary TODOs.

## 5. Recovery / reproduction

Re-run: the inline scripts under
`C:\Users\raiya\AppData\Local\Temp\opencode\t05_*.py` (recount, derive, semantic, training).
For a persistent, tracked harness these should be moved under
`research_artifacts/scripts/` before reuse by later tasks.