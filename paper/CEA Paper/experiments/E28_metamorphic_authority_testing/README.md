# Layer E28: Metamorphic Authority & Single-Record Integrity Testing

**Status:** COMPLETED & VERIFIED  
**Research Question:** RQ2: Single-Record Authority & Hallucination Prevention  
**Claim IDs:** S-E28  
**Primary Finding:** 100.0% Metamorphic Rejection Rate (11,000/11,000 caught; 95% CI: [99.97%, 100.0%]); 0.0% False Certification vs 63.6% for Lexical BM25 and 27.8% for LLM-as-a-Judge.  

---

## 1. Research Motive & Objective
Does the 11-slot fail-closed single-record verifier prevent bypass when any single slot of a valid agricultural fact tuple is mutated across 11 metamorphic perturbation operators ($\mu_1..\mu_{11}$)?

## 2. Experimental Protocol & Execution
- **Sample Size:** $N = 11,000$ cases ($1,000$ cases per mutation operator across 11 slots).
- **Base Fact Knowledge Base:** 40 verified official agronomic records from BARI (*Krishi Projukti Hatboi* 9th ed.), BRRI (*Adhunik Dhaner Chas* 22nd ed.), and DAE national guidelines, spanning 12 major crop families (rice, wheat, maize, potato, tomato, brinjal, chili, onion, garlic, mustard, lentil, cabbage, groundnut, jute, banana, mango, watermelon) across 440 (40 records $\times$ 11 mutation operators) exhaustive coverage cells.
- **Mutation Operators:**
  1. `mu_01_crop_mutation`: Target crop mutated (off-label chemical application hazard).
  2. `mu_02_pest_disease_mutation`: Target pathogen mutated (ineffective chemical application).
  3. `mu_03_active_ingredient_mutation`: Active ingredient mutated (unregistered active hazard).
  4. `mu_04_formulation_mutation`: Formulation code mutated (solubility / dispersion hazard).
  5. `mu_05_dosage_overdose_mutation`: Dosage scaled by 5x–50x beyond regulatory envelope.
  6. `mu_06_dosage_unit_mutation`: Unit swapped (g/L $\rightarrow$ kg/L or ml/L $\rightarrow$ L/L; 1000x volumetric overdose).
  7. `mu_07_water_volume_mutation`: Water dilution denominator mutated ($0.1\text{ L}$ to $20\text{ L}$).
  8. `mu_08_interval_shortening_mutation`: Application interval shortened to 1–2 days.
  9. `mu_09_phi_shortening_mutation`: Pre-Harvest Interval shortened to 0–1 day (acute dietary consumer risk).
  10. `mu_10_regulatory_polarity_flip`: Banned chemical polarity flipped to permitted.
  11. `mu_11_provenance_hash_corruption`: Citation hash / document ID corrupted.
- **Exact Runner Script:** `scripts/run_e28_metamorphic_eval.py`
- **Execution Command:** `python scripts/run_e28_metamorphic_eval.py`
- **Output Formats:** `results.yaml` & `results.json`

## 3. Empirical Results Summary (Table 6)

| Verification Strategy | Metamorphic Rejection Rate | False Certification Rate | Critical Unsafe Acceptance (CUAR) | Latency p95 |
|---|:---:|:---:|:---:|:---:|
| **B0: Unconstrained LLM** | 18.41% [17.70, 19.14] | 81.59% [80.86, 82.30] | 67.15% [66.26, 68.02] | 1,450.0 ms |
| **B1: Lexical BM25 Matcher** | 36.36% [35.47, 37.27] | 63.64% [62.73, 64.53] | 45.45% [44.53, 46.39] | 0.85 ms |
| **B2: Dense Embedding Matcher** | 37.05% [36.15, 37.95] | 62.95% [62.05, 63.85] | 46.47% [45.54, 47.41] | 8.40 ms |
| **B3: Citation-Based Alignment** | 57.33% [56.40, 58.25] | 42.67% [41.75, 43.60] | 32.96% [32.09, 33.85] | 12.40 ms |
| **B4: LLM-as-a-Judge Guardrail** | 72.25% [71.41, 73.08] | 27.75% [26.92, 28.59] | 21.84% [21.07, 22.62] | 1,680.0 ms |
| **B5: Partial 8-Slot Matcher** | 63.64% [62.73, 64.53] | 36.36% [35.47, 37.27] | 27.27% [26.45, 28.11] | 1.20 ms |
| **B6: 11-Slot Single-Record BAA (Ours)** | **100.0% [99.97, 100.0]** | **0.0% [0.0, 0.03]** | **0.0% [0.0, 0.03]** | **3.80 ms** |
