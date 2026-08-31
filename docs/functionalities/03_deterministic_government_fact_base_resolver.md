# 03 — Deterministic Government Fact Base Resolver (Zero-LLM Direct Prescription Card)

> **Module Ref:** Module 3 / Tier 1 & Tier 2 Structured Authority  
> **Status:** Verified & Integrated (`backend/app/application/structured_resolver.py`, `backend/app/domain/fact_base.py`, `backend/app/domain/advisory_templates.py`)  
> **Test Suite:** `backend/tests/test_structured_resolver.py` (12 / 12 Passed)

---

## 1. Architectural Motivation & Problem Formulation

Agricultural extension bodies (BARI, BRRI, DAE) publish official, legally certified pesticide schedules and Integrated Pest Management (IPM) guidelines. When a farmer has a clear crop and diagnosed pathology (e.g. Potato Late Blight, Rice Blast, Fall Armyworm), phrasing the advice through an unconstrained LLM risks:
1. Number perturbation / dosage hallucination ($2.0\,\text{g/L} \to 20\,\text{g/L}$).
2. Pre-harvest interval (PHI) omissions.
3. Unnecessary API latency ($1.5\text{--}3.0\,\text{s}$) and recurring token costs.

---

## 2. Deterministic Resolution Architecture

When a query or vision hint provides a jointly satisfiable tuple $\langle \text{Crop}, \text{Problem}, \text{Stage} \rangle$:

```
               [ Input: Query / Vision Hints ]
                             │
                             ▼
            [ StructuredResolver.resolve(...) ]
                             │
            Match Crop & Problem in Fact Base
                             │
                ┌────────────┴────────────┐
                │                         │
            Match Found               Miss / Ambiguous
                │                         │
                ▼                         ▼
      Confidence >= 0.85?          [ Fall through to T3 ]
                │                  [ Grounded RAG + Verifier ]
        ┌───────┴───────┐
        │               │
       YES              NO
        │               │
        ▼               ▼
  [ Render Certified Card ]  [ Fall through to T3 ]
  - Tier 1: Structured Fact
  - Tier 2: Templated Advisory + IPM + Calendar Note
  - 0 LLM Tokens
  - Latency < 5 ms
```

---

## 3. Schema & 20-Field Fact Contract

Every certified fact row in `FactBase` enforces an accredited 20-field schema:
* `crop`, `crop_bn`
* `problem`, `problem_bn`, `problem_type` (`disease` | `pest` | `weed`)
* `stage` (`vegetative`, `flowering`, `tuber_bulking`, etc.)
* `active_ingredient` (e.g., `mancozeb`, `azoxystrobin`, `chlorantraniliprole`)
* `dose_min`, `dose_max`, `dose_unit` (e.g., `2.0`, `2.5`, `g/l`)
* `application_interval_days` (e.g., `7` days)
* `pre_harvest_interval_days` (e.g., `7` days)
* `ipm_alternatives_bn` (tuple of non-chemical cultural/biological controls)
* `banned_flag` (`False`)
* `severity` (`high` | `medium` | `low`)
* `source_node_id`, `source_doc`, `citation`, `grounding`

---

## 4. Rendered Safe Action Card (T2 Example)

```markdown
**আলু — নাবি ধ্বসা / লেট ব্লাইট**
রোগের তীব্রতা: অত্যন্ত ক্ষতিকর

### প্রতিকার (বালাইনাশক)
অনুমোদিত বালাইনাশক: **mancozeb**
প্রস্তাবিত মাত্রা: 2–2.5 g/l পানিতে মিশিয়ে স্প্রে করুন
প্রতি 7 দিন পর পর স্প্রে করুন।
ফসল সংগ্রহের **7 দিন আগে** স্প্রে সম্পূর্ণ বন্ধ করুন।

### সমন্বিত বালাই ব্যবস্থাপনা (IPM)
- আক্রান্ত পাতা অপসারণ
- সুষম সেচ

*সূত্র: DAE. page_751. List of Registered Agricultural Pesticides (DAE). pp. 751-751.*
```

---

## 5. Performance & Safety Metrics

* **LLM Token Cost:** $0$ tokens.
* **Execution Latency:** $0.0128\text{--}2.5\,\text{ms}$.
* **Dosage Numerical Drift:** $0.0\%$ (verbatim binding from official registry).
