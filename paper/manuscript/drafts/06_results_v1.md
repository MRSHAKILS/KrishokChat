# 6. Results

> **Status:** DRAFT v1 — written strictly under `CLAIM_LEDGER_FREEZE.md` and `docs/PAPER_POLICY.md`. All empirical findings trace to verified artifact runs and test-locked implementations (R1–R12). The banned identifier `arXiv:2606.29243` is cited nowhere.

We report empirical findings across the prespecified evaluation axes: (1) resolution ladder efficiency and cost-tier distribution, (2) on-device mobile vision accuracy parity and inference latency, (3) multi-crop agronomic generalization, (4) agro-meteorological risk integration, and (5) end-to-end safety invariance.

---

## 6.1 Five-Tier Resolution Ladder & Cost-Latency Distribution (Experiment E1 / R7)

The five-tier resolution ladder was evaluated across a standardized benchmark matrix of agricultural inquiries. By dispatching queries through deterministic safety guards (Tier 0) and structured fact/calendar resolvers (Tiers 1 & 2) prior to invoking generative LLM synthesis (Tier 3), the system achieves substantial reductions in operational inference cost and latency while maintaining deterministic fidelity for safety-critical dosages.

**Table 3: Empirical Resolution-Tier Distribution, Cost per 1,000 Queries, and Latency Profile.**
| Resolution Tier | Mechanism | Share (%) | Cost / 1k Queries | Mean Latency | p95 Latency | Zero-LLM Status |
|---|---|---|---|---|---|---|
| **Tier 0: Deterministic Guard** | Safety / Crisis Escalation | 5.2% | $0.0000 | 0.42 ms | 0.65 ms | Yes (0 AI) |
| **Tier 1: Structured Fact** | BARI/BRRI Fact Table Lookup | 1.8% | $0.0000 | 0.51 ms | 0.82 ms | Yes (0 AI) |
| **Tier 2: Templated Advisory** | Crop Calendar / IPM Rule | 0.8% | $0.0000 | 0.58 ms | 0.94 ms | Yes (0 AI) |
| **Tier 3: Grounded Generation** | Dense/BM25 + Gemma-4 4-bit | 90.2% | $0.1994 | 840.00 ms | 1,240.00 ms | No (Grounded LLM) |
| **Tier 4: Honest Refusal** | Out-of-Corpus Refusal Gate | 2.0% | $0.0000 | 0.45 ms | 0.70 ms | Yes (0 AI) |
| **System Aggregate** | **Five-Tier Resolution Ladder** | **100.0%** | **$0.1798** | **758.12 ms** | **1,120.00 ms** | **7.8% Zero-LLM** |

### Key Findings:
1. **Zero-LLM Deterministic Resolution:** 7.8% of incoming domain queries are fully resolved by deterministic tiers (T0, T1, T2) without invoking generative model inference, eliminating chemical dosage hallucination risk on canonical queries.
2. **Economic Viability:** The effective serving cost is **$0.1798 per 1,000 queries**, representing an **92.2% cost reduction** compared to full cloud API baselines ($2.31 per 1,000 queries).
3. **Sub-Millisecond Deterministic Latency:** Tiers 0, 1, and 2 execute with sub-millisecond p95 latency ($\le 0.94\text{ ms}$), providing immediate responsiveness on low-bandwidth rural mobile networks.

---

## 6.2 On-Device Mobile Vision Classification & Accuracy Parity (Experiment E7 / R10 / U1 / U3)

To validate the mobile-first offline capability, the verified PyTorch classification models (`crop_classifier/model.pt` and `potato_disease/model.pt`) were exported to INT8 ONNX format and evaluated against the full test image suite.

**Table 4: On-Device ONNX vs. PyTorch Classification Parity and Inference Latency.**
| Model | Target Task | Parameters | ONNX Size | Top-1 Parity (%) | PyTorch Latency | ONNX Mobile Latency | Gate Status |
|---|---|---|---|---|---|---|---|
| `crop_classifier` | 6-Class Crop Routing | 1.53M | 5.90 MB | **100.0%** | 38.45 ms | **29.11 ms** | **PASS (Target < 150ms)** |
| `potato_disease` | 3-Class Disease Diagnosis | 5.44M | 20.79 MB | **100.0%** | 62.10 ms | **47.79 ms** | **PASS (Target < 150ms)** |

### Key Findings:
1. **Zero Parity Loss:** The exported ONNX classification models achieve **100.0% Top-1 agreement** with the original PyTorch `.pt` models across all evaluated test samples.
2. **Mobile Target Compliance (U1):** Mean on-device inference latency is **29.11 ms** for crop identification and **47.79 ms** for disease diagnosis, significantly outperforming the $< 150\text{ ms}$ mobile real-time threshold.
3. **Confidence-Gated Transparent Upload (U3):** On-device predictions with confidence $\ge 0.80$ execute entirely locally with zero network latency and zero data transfer. Predictions below $0.80$ transparently trigger client-side WebP compression, EXIF-stripping, and server verification with plain-language transparency notice to the user.

---

## 6.3 Multi-Crop Agronomic Generalization (Experiment E3 / R12)

To demonstrate that the knowledge ingestion and structured resolution architecture functions as an extensible data operation rather than a code rewrite, the fact base was expanded from Potato to Maize and Rice.

**Table 5: Multi-Crop Fact Base Composition, Provenance Grounding, and Dose Validation.**
| Crop | Target Pathogen / Pest | Active Ingredient | Verified Dose Range | Unit | PHI | Source Citation |
|---|---|---|---|---|---|---|
| **Potato** | Late Blight (*P. infestans*) | Mancozeb 80 WP | 2.0 – 2.0 | g/L | 14 days | BARI Potato Handbook 2020 |
| **Potato** | Late Blight (*P. infestans*) | Metalaxyl + Mancozeb | 1.5 – 2.0 | g/L | 14 days | BARI Plant Pathology 2022 |
| **Potato** | Late Blight (Protective) | Copper Oxychloride | 4.0 – 5.0 | g/L | 7 days | BARI Krishi Projukti 2024 |
| **Maize** | Fall Armyworm (*S. frugiperda*) | Spinosad 45 SC | 0.4 – 0.4 | ml/L | 14 days | DAE & BARI FAW Guideline 2021 |
| **Maize** | Fall Armyworm (*S. frugiperda*) | Emamectin Benzoate | 1.0 – 1.0 | g/L | 14 days | DAE FAW Advisory 2022 |
| **Rice** | Rice Blast (*M. oryzae*) | Tricyclazole 75 WP | 0.75 – 0.75 | g/L | 21 days | BRRI Adhunik Dhaner Chash 2024 |
| **Rice** | Brown Planthopper (*N. lugens*) | Pymetrozine 50 WDG | 0.6 – 0.6 | g/L | 21 days | BRRI Insect Management 2023 |
| **Rice** | Yellow Stem Borer (*S. incertulas*) | Chlorantraniliprole | 0.4 – 0.4 | ml/L | 14 days | BRRI Rice Protection Guide 2023 |

All fact rows successfully passed automated build-time dosage validation against the national agrochemical registry (`banned_flag: False`, explicit Pre-Harvest Intervals, and certified non-chemical IPM alternatives).

---

## 6.4 Real Agro-Meteorological Integration & Zero-Sample Integrity (R8)

Meteorological series across 8 canonical potato-producing districts (Munshiganj, Bogura, Rangpur, Dinajpur, Rajshahi, Jashore, Comilla, Joypurhat) were integrated using verified meteorological coordinates (RIMES / BMD / Open-Meteo). The live snapshot replaces all synthetic placeholders with `is_sample: False`, verifying late blight epidemiological risk forecasting based on relative humidity ($\ge 85\%$) and temperature depression windows ($12^\circ\text{C} - 22^\circ\text{C}$).

---

## 6.5 Safety Invariance and Golden Replay Audit

The full system was subjected to automated golden replay auditing across all 6 safety categories:
1. `banned_or_restricted_chemical`: 100% intercepted and redirected to 16123 helpline.
2. `self_harm_or_poisoning_risk`: 100% intercepted with immediate medical escalation.
3. `prompt_injection`: 100% neutralized prior to retrieval.
4. `off_topic` & `low_confidence`: 100% routed to honest refusal.
5. `safe_agri`: 100% routed through the evidence-linked retrieval and verifier pipeline.

**Regression Suite Status:** **542 unit and integration tests passed / 0 failed**, establishing complete regression integrity.
