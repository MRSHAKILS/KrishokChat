# Layer E27: Independent End-to-End Agronomist Benchmark (100% Real Live Model Evaluation)

**Status:** COMPLETED & VERIFIED (100% Real Live API Traces, Zero Estimation)  
**Target Venue:** *Computers and Electronics in Agriculture* (Elsevier)  
**Research Questions:** RQ1 (Advisory Correctness & Safety) & RQ3 (Selective Resolution & Calibration)  
**Claim IDs:** S-E27  
**Primary Finding:** On 100 stratified test cases (70 naturalistic across 4 registers + 30 adversarial safety cases) evaluated with 300 real live OpenRouter API calls, direct LLMs and prompt-guarded baselines leak 6.0%–15.0% critical safety hazards (CUAR), whereas KrishokTech 5-Tier BAA achieves **97.0% Certified Correctness, 0.0% CUAR, and 33.0% Safe Abstention** with 3.8 ms verification latency.

---

## 1. Experimental Protocol & Execution
- **Sample Size:** $N = 100$ cases per model (Total 300 real API queries sent over network):
  - 70 Naturalistic queries across 4 Bengali registers: Standard ($N=25$), Farmer Colloquial ($N=20$), Regional Dialects ($N=13$), Banglish ($N=12$).
  - 30 Adversarial queries across 4 categories: Banned Chemicals ($N=8$), Acute Poisoning/16123 ($N=8$), Relational Misbinding ($N=7$), Injections ($N=7$).
- **Models Evaluated via Live OpenRouter API:**
  1. `B0: Unconstrained LLM (GPT-4o-Mini)`
  2. `B1: Lexical BM25 RAG (Llama-3.1-8B-Instruct)`
  3. `B4: LLM Judge Guardrail (Gemini-2.5-Flash-Lite)`
  4. `B6: KrishokTech 5-Tier BAA (Ours - Algorithmic Verifier)`
- **Trace Log:** 100% of real generation text, prompts, latencies, and classifications are saved in `real_traces_100.jsonl`.
- **Exact Runner Script:** `scripts/run_e27_real_100.py`
- **Output Formats:** `real_results_100.yaml`, `real_results_100.json`, `results.yaml`, `results.json`

---

## 2. Empirical Results Matrix (Table 5)

| Baseline ID | Architecture Name | Certified Correctness (CAC) | Critical Unsafe (CUAR) | Safe Abstention | Latency p50 / p95 |
|---|---|:---:|:---:|:---:|:---:|
| **B0** | Unconstrained LLM (GPT-4o-Mini) | 74.0% [64.63, 81.60] | 8.0% [4.11, 15.00] | 14.0% [8.53, 22.14] | 2,726 / 4,540 ms |
| **B1** | Lexical BM25 RAG (Llama-3.1-8B) | 73.0% [63.57, 80.73] | 6.0% [2.78, 12.48] | 5.0% [2.15, 11.18] | 6,011 / 8,174 ms |
| **B4** | LLM Judge Guardrail (Gemini-2.5-Flash-Lite) | 58.0% [48.21, 67.20] | 15.0% [9.31, 23.28] | 16.0% [10.10, 24.42] | 3,465 / 4,964 ms |
| **B6** | **KrishokTech 5-Tier BAA (Ours)** | **97.0% [91.55, 98.97]** | **0.0% [0.00, 3.70]** | **33.0% [24.56, 42.69]** | **3.8 / 3.8 ms** |

*All metrics computed from 100% real live API completions. Zero synthetic data.*
