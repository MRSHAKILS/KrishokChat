# KrishokTech Architecture 2.0 — Unified Multimodal & Agronomic Synthesis

> **CANONICAL RESEARCH & ARCHITECTURAL OVERVIEW**  
> **Last Audited:** 2026-09-03 | **Architecture Version:** 2.0  
> **Core Milestone:** Elimination of Cross-Crop Toxic Hazard ($38.5\% \to 0.00\%$) across Multimodal Perception and Grounded Advisory.

---

## 1. Executive Summary & The Core Breakthrough

Traditional agricultural chatbots and digital advisory tools operate as decoupled systems:
1. **Unconstrained Text LLMs:** Hallucinate unapproved active ingredients, misapply dosages, and answer poison/suicide queries without safety guardrails.
2. **Naive Image Classifiers:** Suffer from catastrophic cross-crop confusion (e.g., misclassifying solanaceous weed foliage or chili leaves as potato late blight, triggering lethal pesticide recommendations).
3. **Black-Box Web Apps (e.g., Gacher Doctor):** Print fake certification stamps on empty reports and compute teaspoon doses without active ingredient or chemical molecule inputs.

**KrishokTech 2.0 solves this through a closed-loop multimodal interlock:**
* An on-device edge perception pipeline classifies crop and disease with calibrated confidence and margin gates ($C_d \ge 0.85, M_d \ge 0.18$).
* Any narrow-margin botanical ambiguity (such as lobed Solanaceae leaves) triggers an interactive clarification intercept (`[আলু] [টমেটো] [বেগুন] [মরিচ]`), completely halting downstream generation.
* Validated diagnoses retrieve exact BARI/DAE monograph facts via a relational resolver, enforcing deterministic concentration math, Pre-Harvest Intervals (PHI), and household volume benchmarks (spoons, bottle caps, matchboxes).
* The result: On the 436-image real field replay, **cross-crop hazardous routing dropped to $0.00\%$ ($0/436$)** and safe containment reached **$97.94\%$**.

---

## 2. The Multi-Tier Cost-Gated Decision Ladder

```
[ User Input: Bangla Text or Foliar Image ]
                     │
                     ▼
[ Tier 0: Deterministic Safety Precheck ] (0.32 ms, 0 LLM Cost)
   ├── Banned Chemical (Paraquat, Carbofuran) / Poisoning / Crisis
   └── Instant Escalation to National Krishi Call Center 16123 (0 Tokens)
                     │
                     ▼ (Pass)
[ Tier 1: Multimodal Edge Perception Gate ] (ONNX Runtime / WASM, 26–58 ms)
   ├── Primary Crop Classifier: 10-Class YOLO26s (Rice, Wheat, Corn, Potato, Brassica, Chilli, etc.)
   ├── Botanical Confusion Gate: Intercepts narrow-margin Solanaceae foliage (Confidence >= 0.90, Margin >= 0.20)
   ├── Crop-Specific Disease Specialists:
   │     ├── Rice (7 classes, 320px FP32)
   │     ├── Potato (3 classes, 224px INT8)
   │     ├── Chilli (8 classes, 224px YOLO26n INT8, 99.68% held-out test accuracy)
   │     ├── Wheat (6 classes, 224px INT8)
   │     ├── Corn (4 classes, 256px FP32)
   │     └── Brassica (6 classes, 256px INT8)
   └── Out-of-Distribution / Uncertainty: Fails closed into Quick-Reply Clarification Chips
                     │
                     ▼ (Verified Perception Context)
[ Tier 2: Grounded Hybrid Retrieval & Structured Resolver ] (BM25 + BGE-M3 FAISS RRF, k=20)
   ├── Relational 11-Slot Fact Binding (Crop, Disease, Active Ingredient, Dosage, Water Volume, PHI)
   ├── D1a Deterministic Corpus-Coverage Gate (100% Unanswerable Refusal)
   └── Dialect Normalization (33.49% lift on regional Barishal, Chittagong, Sylhet, Rangpur phrasing)
                     │
                     ▼ (Pass)
[ Tier 3: Grounded Generation & Relational Verification ]
   ├── Local Low-Cost LoRA: krishoktech-4b (llama-server / Ollama)
   ├── Production Cloud NLU: google/gemini-2.5-flash-lite (<= 180 tokens, single JSON slot call)
   └── Verifier Claim Enforcement: Strips unsupported dosage numbers; annotates live audit trail
```

---

## 3. Empirical Benchmark & Paper Manifest

| Benchmark Dimension | Measured Result | Significance / Comparison |
|---|:---:|---|
| **Cross-Crop Hazard Rate** | **$0.00\%$ ($0 / 436$)** | Completely eliminates baseline unconstrained hazard ($38.5\%$). |
| **Safe Direct Automation** | **$48.62\%$ ($212 / 436$)** | High-precision instant advisory without manual intervention. |
| **Total Safe Containment** | **$97.94\%$ ($427 / 436$)** | Direct safe + interactive clarification + one-shot recovery + OOD halt. |
| **Adversarial Defenses** | **$100\%$ ($15 / 15$)** | Zero toxic leaks on banned chemicals, human poisoning, or non-agri inputs. |
| **Chilli Disease Accuracy** | **$99.68\%$ ($626 / 628$)** | YOLO26n-cls held-out field validation (5.91 MB ONNX, 11.3 ms mobile CPU). |
| **Unanswerable Refusal Rate** | **$100\%$ ($12 / 12$)** | Powered by D1a deterministic coverage gate on 1,000 farmer queries. |

### Research Publications Supported:
1. **EACL 2026 Demo Paper (8 pages):** Focuses on system features, interactive quick-reply chips, real-time latency, streaming provenance traces, and the official printable Prescription Slip (`krishoktech_eacl_main.pdf`).
2. **Computers and Electronics in Agriculture (CEA) Research Paper (21 pages):** Focuses on architectural safety theory, empirical selective reliability, elimination of cross-crop toxic hazard, and formal mathematical bounds (`krishoktech_cea_main.pdf`).

---

## 4. Production & Field Agronomic Polish

* **Pre-Harvest Interval (PHI) Enforcement:** Explicit safety harvest waiting periods ($7\text{--}14\text{ days}$) across all chemical advisory surfaces and the printable prescription sheet.
* **DAE Golden Spray Directives:** Integrated meteorological extension rules (never spray in midday sun, spray downwind, wear facial cloth/mask protection).
* **Tactile Soil Moisture Grounding:** De-mystified raw tensiometer suction ($\text{kPa}$) into traditional agrarian farmer states led by **মাটির আদর্শ 'জো' অবস্থা (Optimum 'Jo' Moisture)** alongside the traditional **"মাটি মুঠো পরীক্ষা" (Field Squeeze Test Guide)**.
* **Rural Measurement Equivalencies:** Interactive Dosage Calculator supporting standard $16\,\text{L}$ knapsack tanks, tea spoons ($\approx 2\,\text{g}$), bottle caps ($\approx 10\,\text{ml}$), and matchboxes ($\approx 10\text{--}12\,\text{g}$ powder).
