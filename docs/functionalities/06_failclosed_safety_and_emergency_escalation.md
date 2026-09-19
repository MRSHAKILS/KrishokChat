# 06 — Fail-Closed Safety & Emergency Escalation

> **Module Ref:** Module 6 / Tier 0 Deterministic Safety Gate (Layer E03)  
> **Status:** Verified & Integrated (`backend/app/domain/safety_policy.py`, `backend/app/domain/chemical_registry.py`)  
> **Test Suite:** `backend/tests/test_chemical_registry.py` (12 / 12 Passed, 468 subtests)

---

## 1. Architectural Motivation & Problem Formulation

Agricultural advisory platforms can be exposed to severe life-safety and environmental hazards:
1. Inquiries about banned/prohibited agrochemicals (e.g., Paraquat, Furadan/Carbofuran, DDT, Endosulfan).
2. Acute accidental poisonings (e.g. pesticide in eyes, ingestion by children).
3. Self-harm, poisoning framings, and prompt injections.

General LLMs frequently attempt to provide "helpful" usage instructions or speculative safety bounds for banned toxic substances. KrishokTech enforces an absolute **Fail-Closed Deterministic Tier 0 Precheck**.

---

## 2. Safety Gate Decision Ladder

The deterministic precheck runs in $0.32\,\text{ms}$ before any retrieval or LLM call is scheduled:

```
                            [ Incoming User Query ]
                                       │
                                       ▼
                       [ Tier 0 Deterministic Precheck ]
                                       │
         ┌───────────────────┬─────────┴─────────┬───────────────────┐
         │                   │                   │                   │
         ▼                   ▼                   ▼                   ▼
  [ Self-Harm /      [ Banned Chemical   [ Prompt Injection  [ Out-of-Coverage /
   Poisoning ]        Active / Brand ]    Payload ]           Livestock ]
         │                   │                   │                   │
         ▼                   ▼                   ▼                   ▼
  [ Emergency Redirect] [ Calm Refusal &    [ Strict Boundary   [ Out-of-Scope
   Call 999 & 16123 ]    Call 16123 ]        Notice ]            Refusal & 16123 ]
         │                   │                   │                   │
         └───────────────────┴─────────┬─────────┴───────────────────┘
                                       │
                                       ▼
                       [ 0 Retrieval | 0 LLM Tokens ]
```

---

## 3. Bangladesh Banned & Cancelled Agrochemical Registry

Attributed to official gazettes from the Department of Agricultural Extension (DAE) Plant Protection Wing and Import Policy Order:

| Active Ingredient | Common Brand Aliases | Bengali Aliases | Legal Regulatory Status |
|---|---|---|---|
| **Carbofuran** | Furadan, Curaterr | কার্বোফুরান, ফুরাডান, কুরাটার | Cancelled / Banned in BD |
| **Paraquat** | Gramoxone | প্যারাকোয়াট, পরাকুয়াট, গ্রামোক্সোন | Cancelled / Banned in BD |
| **Phosphamidon** | Dimecron | ফসফামিডন, ডাইমেক্রন | Cancelled / Banned in BD |
| **DDT** | — | ডিডিটি | Banned (POP listed) |
| **Dieldrin / Aldrin / Endrin** | — | ডিলড্রিন, অ্যালড্রিন, এনড্রিন | Prohibited since 1962 |
| **Endosulfan** | — | এন্ডোসালফান | Banned in BD |
| **Monocrotophos** | Azodrin, Nuvacron | মনোক্রোটোফস, নুভাক্রন, এজোড্রিন | Cancelled in BD |
| **Dichlorvos (DDVP)** | Vapona, Nogos | ডাইক্লোরভস | Cancelled in BD |
| **Methyl Bromide** | Mebrom | মিথাইল ব্রোমাইড | Controlled / Banned |

---

## 4. Emergency Accidental Poisoning Routing

When symptoms of acute toxicity, accidental swallowing, or ocular pesticide exposure are detected:
* **Immediate Response:**
  > *"আপনার জীবন মূল্যবান। আপনি বা কেউ এখন বিপদে থাকলে অবিলম্বে ৯৯৯ নম্বরে কল করুন বা নিকটস্থ হাসপাতালে যান। কৃষি সহায়তার জন্য কৃষক কল সেন্টার: ১৬১২৩।"*
* **One-Touch Dial:** Immediate click-to-call affordances for `tel:999` and `tel:16123`.

---

## 5. Measured Safety Metrics

* **Toxic Leak Rate:** $0.0\%$ (0/70 adversarial chemical/poisoning probes leaked).
* **Deterministic Precheck Latency:** p50 $0.32\,\text{ms}$ (p95 $0.85\,\text{ms}$).
* **Token Cost:** $0$ tokens.
