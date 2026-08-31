# 04 — Grounded Contextual Multi-Turn Chat Engine

> **Module Ref:** Module 4 / Conversational Grounding & Verifier Hardening  
> **Status:** Verified & Integrated (`backend/app/application/rewrite.py`, `backend/app/application/generation.py`, `backend/app/application/verifier.py`)  
> **Test Suite:** `backend/tests/test_rewrite.py` (13 / 13 Passed), `backend/tests/test_verifier_hardening.py` (19 / 19 Passed)

---

## 1. Architectural Motivation & Problem Formulation

In real farm practice, a farmer rarely stops at a single diagnosis. They ask conversational follow-up questions:
* *"বৃষ্টি হলে কী করব?"* (*"What if it rains after spraying?"*)
* *"সার সাথে মেশানো যাবে কি?"* (*"Can I tank-mix this with fertilizer?"*)
* *"আমি এটা আগে দিয়েছি, এখন কতদিন পর আবার দেব?"* (*"I sprayed this before, how long before re-application?"*)

If multi-turn follow-ups are routed to an unconstrained LLM, conversational drift often causes the model to suggest alternative unverified chemicals, escalate dosages, or forget safety intervals.

---

## 2. Multi-Turn Conversational Architecture

```
                  [ Farmer Follow-Up: "এখন বৃষ্টি হলে কী করব?" ]
                                         │
                                         ▼
                 [ Heuristic Gate: ConversationalQueryRewriter ]
                 - Checks Agricultural Deixis Markers
                 - Checks Conversation History
                                         │
                                  ┌──────┴──────┐
                                  │             │
                              Needs Rewrite   Self-Contained
                                  │             │
                                  ▼             │
                        [ Rewrite with LLM ]    │
                        "আলুর লেট ব্লাইটে       │
                         ম্যানকোজেব স্প্রে করার │
                         পর বৃষ্টি হলে করণীয়"  │
                                  │             │
                                  └──────┬──────┘
                                         │
                                         ▼
                     [ Seed-Bounded Grounded Retrieval ]
                     - Prior Certified Sources Injected First
                     - New Supplemental Passages Retrieved
                                         │
                                         ▼
                     [ GroundedAnswerGenerator Prompt ]
                     - Negative Constraint Directives
                     - Verbatim Field Directives
                                         │
                                         ▼
                     [ HardenedDosageVerifier (P1) ]
                     - Entailment Check on Chemicals & Dosages
                     - Outlier Detection vs Registered Rates
                     - Annotate-and-Drop on Unsupported Claims
```

---

## 3. Agricultural Deixis Markers

The heuristic gate triggers conversational rewriting when recent history exists and any of the following markers are detected:
* **Deixis / Pronouns:** `"তাহলে"`, `"তবে"`, `"এটা"`, `"সেটা"`, `"এগুলো"`, `"ওটা"`
* **Action & Question Phrases:** `"কী করব"`, `"কী করি"`, `"কী দেব"`, `"কত দেব"`, `"কতটা"`, `"কতটুকু"`, `"কীভাবে"`
* **Agricultural Follow-ups:** `"বৃষ্টি"`, `"বৃষ্টির পর"`, `"বৃষ্টি হলে"`, `"কী হবে"`, `"আগে দিয়েছি"`, `"সার মেশানো"`, `"একসাথে"`, `"মিক্স"`, `"কতদিন পর"`, `"কত দিন পর"`

---

## 4. Hardened Relational Verification Guard

`HardenedDosageVerifier` extracts all candidate triples $(Active, Amount, Unit)$ from the generated text:
1. **Entailment Check:** Validates that the active ingredient and numerical amount appear in at least one retrieved evidence passage.
2. **Gross Outlier Rejection:** Rejects claims exceeding registered upper bounds ($> 1.2\times$ registered max rate) even if asserted in a retrieved passage.
3. **Annotate-and-Drop (`sanitize_answer`):** Strips ungrounded claims cleanly from the rendered text and flags the audit ledger without crashing the session.

---

## 5. Token Protection & Cost Discipline

* **Rewrite Gating:** Single-turn questions bypass the rewriter completely ($0$ rewrite tokens).
* **Generation Token Cap:** Strict `max_output_tokens=250` (local) / `500` (cloud).
* **Zero Leakage:** Unsupported claims fail closed to the official record or 16123 referral.
