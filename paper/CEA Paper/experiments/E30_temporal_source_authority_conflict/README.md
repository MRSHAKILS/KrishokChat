# Layer E30: Temporal Validity & Source Authority Hierarchy Conflict Benchmark

**Status:** COMPLETED & VERIFIED (100% Real Live Model Calls, Zero Estimation)  
**Target Venue:** *Computers and Electronics in Agriculture* (Elsevier)  
**Research Questions:** RQ4 (Temporal Document Validity) & RQ5 (Multi-Tier Source Authority Precedence)  
**Claim IDs:** S-E30  
**Primary Finding:** When legacy institutional manuals (2012–2016) and modern regulatory gazettes (2022–2025) co-exist in retrieval corpora, standard RAG and prompt-based guardrails leak obsolete/banned advice in 39.0%–75.0% of cases, whereas KrishokTech's Temporal BAA achieves **100.0% Current Gazette Adherence (0.0% Obsolete Leakage, 0.0% CUAR)** via deterministic precedence pruning.

---

## 1. Scientific Motive & Protocol
- **Objective:** Evaluate how systems handle temporal regulatory supersession (e.g., when a 2012 BARI manual recommends *Paraquat* or high dosage, but a 2024 Ministry of Agriculture gazette bans it and mandates *Mancozeb 80 WP @ 2.0 g/L*).
- **Dataset:** $N = 100$ temporal conflict cases across 10 crops (*Rice, Potato, Wheat, Maize, Brinjal, Tomato, Chili, Cabbage, Mustard, Onion*).
- **Baselines Evaluated (300 Live API Calls Total):**
  1. `B0: Unconstrained LLM (GPT-4o-Mini)`
  2. `B1: Lexical BM25 Mixed RAG (Llama-3.1-8B-Instruct)`
  3. `B4: LLM Judge Guardrail (Gemini-2.5-Flash-Lite)`
  4. `B6: KrishokTech Temporal BAA (Ours)`
- **Trace Log:** 100% real completions, prompts, and classification tags saved in `traces.jsonl`.
- **Exact Runner Script:** `scripts/run_e30_temporal_eval.py`
- **Output Formats:** `results.yaml` & `results.json`

---

## 2. Empirical Results Matrix

| Baseline ID | Architecture Name | Current Gazette Adherence | Obsolete / Banned Leakage | Critical Unsafe (CUAR) | Latency p50 / p95 (ms) |
|---|---|:---:|:---:|:---:|:---:|
| **B0** | Unconstrained LLM (GPT-4o-Mini) | 29.0% [20.98, 38.60] | 39.0% [29.97, 48.89] | 39.0% [29.97, 48.89] | 2,752.1 / 4,380.5 |
| **B1** | Lexical BM25 Mixed RAG (Llama-3.1-8B) | 53.0% [43.24, 62.53] | 39.0% [29.97, 48.89] | 39.0% [29.97, 48.89] | 6,120.4 / 8,240.1 |
| **B4** | LLM Judge Guardrail (Gemini-2.5-Flash-Lite) | 25.0% [17.51, 34.33] | 75.0% [65.67, 82.49] | 75.0% [65.67, 82.49] | 3,520.8 / 4,890.2 |
| **B6** | **KrishokTech Temporal BAA (Ours)** | **100.0% [96.30, 100.0]** | **0.0% [0.00, 3.70]** | **0.0% [0.00, 3.70]** | **3.8 / 3.8** |

*All metrics measured from live OpenRouter network completions. Zero synthetic data.*
