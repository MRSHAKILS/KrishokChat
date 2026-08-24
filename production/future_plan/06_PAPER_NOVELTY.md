# 06 — Paper Novelty & Evaluation

**Parent:** `00_SCOPE_OUTLINE.md` (§8)
**Status:** PLANNING — no code changes.
**Goal:** defensible, testable novelty claims to get the paper accepted and support the funding pitch.
**Paper policy:** authoritative papers are in `paper/done papers/`; the arXiv v1 is DEPRECATED — never cite it (AGENTS.md hard rule #9, `docs/PAPER_POLICY.md`).

---

## 1. The framing rule

Frame novelty as the **combination** (safety-verifier + DAE-grounded dosage + provenance + dialect + edge), **not** any single well-trodden component. Do **NOT** claim "first Bengali agri RAG" or "first fine-tuned Bengali agri model" — prior art exists (KrishokBondhu etc.). The novelty is the *safety-critical, provenance-traceable, practically-deployable* integration.

---

## 2. Five defensible, testable claims

| # | Claim | Evaluation to substantiate it |
|---|---|---|
| **N1** | First Bengali agri assistant with a **chemical-dosage safety verifier grounded in DAE/PPW registered-pesticide data** (+ HHP/banned flags) | Held-out dosage/chemical query set; verifier precision/recall on out-of-range doses + banned mentions; contradiction rate vs baseline |
| **N2** | First to **structurally guarantee citation provenance** (deterministic injection, not LLM-generated citations) | Citation-hallucination rate = 0 by construction; every claim's entity present in the cited passage |
| **N3** | First to pair a **genuine BD dialect map** with **on-device edge diagnosis** | Retrieval/answer accuracy: dialect-rewritten vs Standard Bengali (report the register gap); on-device vs cloud latency/accuracy |
| **N4** | First Bengali agri pipeline with a **safety/router gating retrieval BEFORE generation** + local audit trail | Classification accuracy on the 6 safety categories; over-refusal (144 tests) vs harm-catch trade-off; per-category audit breakdown |
| **N5** | First to **counter documented pro-chemical bias** by grounding in DAE + surfacing IPM/non-chemical alternatives | Fraction of pesticide-query responses that surface a non-chemical/IPM option + correctly redirect banned chemicals to 16123 |

---

## 3. Why these are safe (the gaps are documented as unfilled)

- General agri-LLMs produce "incorrect pesticide dosages"; no published framework combines atomic decomposition + expert verification + safety-critical contradiction detection for Bengali agriculture.
- Independent audits show proprietary agri-AI (incl. KissanAI) has **systematic pro-chemical bias** ([Wyckhuys et al., WUR](https://edepot.wur.nl/721621)).
- **Plantix rejected** adding weather/planting-date checks and pivoted to selling pesticides ([WIRED](https://www.wired.com/story/plantix-pesticides-venture-capital-app/)) — the safety/IPM angle is genuinely open.
- Farmers get dose advice from pesticide **retailers** with a conflict of interest (92.5% for mango — [JAE 2025](https://www.ajol.info/index.php/jae/article/view/301277)).

---

## 4. Datasets / assets already available for evaluation

- **Safety dataset:** 20,112 records (T3 refusal 3,216 + T4 requery 16,896), 110-word dialect map → directly supports N3, N4, N5.
- **Golden 50/50 QA + injection cases** (Phase 0) → supports N2, N4.
- **Audit trail** (local JSONL/SQLite) → supports N4 per-category breakdown, N5 redirect counts.

---

## 5. Suggested evaluation build order (align with the §10 spine)

1. **N1 dosage verifier** eval on potato fungicide doses (the spine crop) grounded in PPW/BAMIS — highest-value, matches spine step 2.
2. **N4 safety-router** eval reusing the existing 20,112-record dataset + 144 over-refusal tests.
3. **N2 provenance** — report 0 citation hallucination by construction.
4. **N5 pro-chemical-bias counter** — measure IPM-surfacing + banned-redirect fraction.
5. **N3 dialect + edge** — once on-device export (U1) exists, report the latency/accuracy comparison.

## 6. Guardrails

- Never cite the deprecated arXiv v1; reference `paper/done papers/` by filename only.
- No fabricated metrics — every number from a real eval run or marked `TODO`.
- No invented arXiv IDs/URLs.
- Claim the *combination*, not any single commoditized component.
