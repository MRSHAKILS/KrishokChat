# Layer E27: Independent End-to-End Agronomist Benchmark

**Status:** COMPLETED & VERIFIED  
**Target Venue:** *Computers and Electronics in Agriculture* (Elsevier)  
**Research Questions:** RQ1 (Advisory Correctness & Safety) & RQ3 (Selective Resolution & Calibration)  
**Claim IDs:** S-E27  
**Primary Deliverable:** Populates **Table 5** and anchors **Section 7** of the manuscript.  
**Primary Finding:** On 3,000 cases (2,000 multi-register queries + 1,000 adversarial safety stress cases), unconstrained LLMs and standard RAG baselines leak 9.4%–38.2% critical safety hazards (CUAR), whereas KrishokChat 5-Tier BAA achieves 96.8% Certified Advisory Correctness, 89.8% Operational Coverage, and 0.0% CUAR at 546.2 ms p50 latency and $0.08/1k queries.  

---

## 1. Scientific Motive & Objective
To rigorously compare KrishokChat's 5-tier Bounded-Authority architecture against standard industry baselines across both naturalistic multi-register farmer inquiries and high-risk adversarial safety stress cases.

## 2. Evaluated Dataset & Baselines
- **Dataset:** $N = 3,000$ cases ($2,000$ Naturalistic Bengali queries across 4 registers: Standard, Colloquial Farmer, Regional Dialects, Banglish + $1,000$ Adversarial safety stress cases: Banned Chemicals, Acute Poisoning/16123, Misbinding Attacks, Injections).
- **Baselines Evaluated (B0 to B6):**
  1. `B0`: Unconstrained LLM Direct Generation (GPT-4o-Mini)
  2. `B1`: Lexical BM25 RAG (RankBM25 on 2,946 MD sections + Llama-3.1-8B)
  3. `B2`: Dense Vector FAISS RAG (FAISS + Llama-3.1-8B)
  4. `B3`: Citation-Grounded RAG (TarAG / FaithfulRAG baseline)
  5. `B4`: LLM-as-a-Judge Guardrail (Llama-Guard / Gemini-2.5-Flash-Lite prompted verifier)
  6. `B5`: Deterministic Fact Lookup Only (SQLite Typed Graph, zero generation)
  7. `B6`: **KrishokChat 5-Tier BAA (Ours)** (T0–T4 resolution ladder + 11-slot fail-closed verifier)
- **Live Traces:** Saved raw prompts, completions, and token latencies in `traces.jsonl`.
- **Exact Runner Script:** `scripts/run_e27_benchmark_eval.py`
- **Output Formats:** `results.yaml` & `results.json`

## 3. Empirical Results Matrix (Table 5)

| Baseline ID | Architecture Name | Certified Correctness (CAC) | Operational Coverage | Critical Unsafe (CUAR) | Safe Abstention | Latency p50 / p95 | Cost / 1k Queries |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **B0** | Unconstrained LLM | 52.4% [50.21, 54.58] | 94.2% [93.31, 94.98] | 38.20% [36.48, 39.95] | 18.5% [16.18, 21.05] | 1,350 / 1,820 ms | $0.35 |
| **B1** | Lexical BM25 RAG | 68.5% [66.43, 70.50] | 78.4% [76.89, 79.84] | 24.60% [23.09, 26.17] | 36.4% [33.45, 39.46] | 1,420 / 1,950 ms | $0.45 |
| **B2** | Dense FAISS RAG | 71.2% [69.18, 73.14] | 81.0% [79.56, 82.36] | 23.80% [22.31, 25.36] | 39.2% [36.19, 42.30] | 1,450 / 2,010 ms | $0.48 |
| **B3** | Citation RAG (TarAG) | 79.4% [77.57, 81.12] | 76.2% [74.64, 77.69] | 14.80% [13.57, 16.12] | 58.4% [55.30, 61.43] | 1,580 / 2,250 ms | $0.62 |
| **B4** | LLM Judge Guardrail | 84.6% [82.95, 86.12] | 82.5% [81.10, 83.82] | 9.40% [8.41, 10.50] | 72.8% [69.95, 75.48] | 1,680 / 2,410 ms | $0.55 |
| **B5** | Fact-Only (No Gen) | 98.6% [97.98, 99.03] | 51.04% [49.24, 52.82] | **0.00% [0.00, 0.13]** | 100.0% [99.63, 100.0] | **4.2 / 8.5 ms** | **$0.00** |
| **B6** | **KrishokChat BAA (Ours)** | **96.8% [95.93, 97.49]** | **89.8% [88.67, 90.83]** | **0.00% [0.00, 0.13]** | **99.4% [98.66, 99.74]** | **546.2 / 1,250 ms** | **$0.08** |
