# KrishokTech Functionality Specifications & Practical Flow Reference

> **SSOT Documentation for System Demonstrations & Scientific Papers**  
> Last Audited: 2026-09-01 | Architecture Version: 2.0  
> Direct Reference for: `paper/CEA Paper/`, `paper/EACL Demo/`, and Frontend/Backend Engineering Teams

---

## 1. Modular Functionality Map

| Module Ref | Functionality Title | Core Implementation Files | Test Suite | Zero-Token Guarantee |
|---|---|---|---|:---:|
| [**Module 1**](./01_safe_vision_ingestion_and_uncertainty_gating.md) | Safe Vision Ingestion & Calibrated Uncertainty Gate | `vision_pipeline.py`, `domain/vision.py` | `test_vision.py` | ✅ Yes ($0$ tok) |
| [**Module 2**](./02_cross_modal_contradiction_intercept.md) | Cross-Modal Contradiction Intercept | `domain/intent.py`, `qa_pipeline.py` | `test_intent_extraction.py` | ✅ Yes ($0$ tok) |
| [**Module 3**](./03_deterministic_government_fact_base_resolver.md) | Deterministic Government Fact Base Resolver | `structured_resolver.py`, `fact_base.py` | `test_structured_resolver.py` | ✅ Yes ($0$ tok) |
| [**Module 4**](./04_grounded_contextual_multiturn_chat.md) | Grounded Contextual Multi-Turn Chat Engine | `rewrite.py`, `generation.py`, `verifier.py` | `test_rewrite.py`, `test_verifier_hardening.py` | ✅ Bounded ($\le 250$ tok) |
| [**Module 5**](./05_dialect_and_nonstandard_language_normalization.md) | Dialect & Non-Standard Language Normalization | `domain/intent.py`, `query_builder.py` | `test_intent_extraction.py` | ✅ Keyword First / $\le 180$ tok |
| [**Module 6**](./06_failclosed_safety_and_emergency_escalation.md) | Fail-Closed Safety & Emergency Escalation | `safety_policy.py`, `chemical_registry.py` | `test_chemical_registry.py` | ✅ Yes ($0$ tok, $0.32\,\text{ms}$) |

---

## 2. Five-Tier Cost-Gated Decision Ladder

```
[ User Input (Voice / Text / Image) ]
                  │
                  ▼
[ Tier 0: Deterministic Safety Precheck ] (0.32 ms, 0 Tokens)
  ├── Banned Chemical Active / Brand ──► Instant 16123 Redirect (0 Tokens)
  ├── Accidental Poisoning / Crisis ──► Immediate 999 & 16123 Escalation (0 Tokens)
  │
  ▼ (Pass)
[ Module 2: Cross-Modal Contradiction Check ] (0.05 ms, 0 Tokens)
  ├── Image Crop != Query Crop ──► Fail-Closed Clarification Prompt (0 Tokens)
  │
  ▼ (Pass)
[ Tier 1/2: Deterministic Structured Resolver ] (< 5 ms, 0 Tokens)
  ├── Known Crop + Problem Match ──► Official BARI/BRRI Prescription Card (0 Tokens)
  │
  ▼ (Miss)
[ Tier 5: Dialect Normalization & Disambiguation ] (Keyword 0 ms / Gemini-2.5-flash-lite <= 180 Tokens)
  ├── Symptom Query with Crop == NULL ──► Interactive Quick-Reply Chips (0 Tokens)
  │
  ▼ (Crop Identified)
[ Tier 3: Grounded Multi-Turn RAG + Hardened Verifier ] (LoRA Gemma-4 / Cloud API <= 250 Tokens)
  └── Per-Claim Entailment Check + Dosage Outlier Drop
```
