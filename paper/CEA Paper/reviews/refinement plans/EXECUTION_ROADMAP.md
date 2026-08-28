# Submission Execution Roadmap
**Project:** Bounded-Authority Agricultural Advisory (KrishokChat / BAA) → *Computers and Electronics in Agriculture*
**Date:** 2026-08-28
**Starting point:** current state of `D:\Downloads\CEA Paper`
**Objective:** maximum scientific strength and submission readiness per unit of effort. Not perfection.

---

## 0. THREE EXECUTION FACTS ESTABLISHED BY TESTING, NOT INFERENCE

I ran things on your machine before writing this plan. These change the ordering materially.

**Fact 1 — E28 is fully self-contained and reproduces exactly, offline, in ~30 seconds.**
I copied `run_e28_metamorphic_eval.py` to a scratch directory, repointed two path constants, and ran it. It regenerated its own 11,000-case dataset from the in-script `BASE_FACT_TEMPLATES` and reproduced the published numbers to the decimal: B6 100.0%, B5 63.64%, B4 72.25%, B3 57.33%, B0 18.41%. **No external dataset, no API key, no network.** Python 3.10.12 and pyyaml 6.0.3 are present.

→ Consequence: **every cheap fix in this roadmap retargets onto the E28 harness.** M-A, M-B, M1 (slot ablation) and M6 (benign control) are all edits to one file that demonstrably runs in half a minute. This is an afternoon, not a sprint.

**Fact 2 — E02 cannot currently be re-run.** It reads `research_artifacts/datasets/attacks/relational_misbinding/misbinding_attack_suite_v2.jsonl`, which is outside the connected folder. Until that file surfaces, E02 is frozen evidence you can re-describe but not re-measure.

→ Consequence: **do not build the plan on E02.** E28 subsumes it (11 operators vs 10 families, 7 systems vs 2). Lead with E28.

**Fact 3 — the "11,000 cases" collapse to 11 independent determinations, and I measured this exactly.**
I instrumented the verifiers across the generated dataset:

```
B6: operator-level cells = 11, cells with any within-cell verdict variation = 0
    (operator × base-crop) cells = 77, varying = 0
B5: identical — 11 cells, 0 varying; 77 cells, 0 varying
distinct base crops = 7 (potato, rice, tomato, chili, maize, wheat, brinjal) from 8 templates
```

Every one of the 77 cells is internally constant. For a deterministic rule-based verifier this is not a defect in the data — **it is what a deterministic rule does.** The defect is describing it as a 11,000-sample proportion with a Wilson interval.

→ Consequence: **the fix is free and makes the result stronger.** Stop reporting `100.0% [99.96, 100.0]` over n=11,000. Report it as what it is: **exhaustive property-based testing** — the certification rule was evaluated against all 11 mutation classes across 8 base records (77 class×record cells) and rejected every one, with behaviour invariant within each cell. That is a *proof-by-cases coverage claim*, which is a legitimate and respected form of evidence for a deterministic verifier, and it cannot be attacked on statistical grounds because it makes no statistical claim. It costs one table and zero experiments.

This single reframing (task **W4**) is the highest impact-to-effort action in the entire project.

---

## 1. PRIORITIZATION PRINCIPLE APPLIED

Ordering weights used throughout: effort (impl + analysis + writing) · dependency depth · risk of creating new problems · scope expansion · likelihood of changing the final decision · whether a local artifact already answers it.

The resulting shape of this project is unusual and worth stating plainly: **almost all of its remaining value is in deletion and reframing, not in experiments.** Roughly 80% of the achievable gain sits in Tiers 0–1, which are writing tasks. Four experiments remain; three of them are edits to one file that runs in 30 seconds.

---

## 2. WORK TIERS

### TIER 0 — SUBMISSION BLOCKERS
*Nothing below Tier 0 matters until these are done. Most are deletions and cost hours.*

| # | Task | Type | Effort |
|---|---|---|---|
| **T0-1** | **Decide E13.** Do rating sheets, rater consent and ethics approval exist? If yes → produce them and add an ethics statement (§6.5 + a Declarations block). If no → delete every trace of the study: abstract sentence, §6.5 protocol paragraph, §7.2 entirely, §14 references, §18, and the `\HumanGwetAC` macro in the driver. | Decision + edit | 1 h (delete) / days (document) |
| **T0-2** | **Decide CL-3.** Does a runnable system exist at `d:\KrishokChat Advisory System`? If no → delete the abstract's "97.0% CAC / 0.0% CUAR on a 100-case live benchmark", §7.1, Table 5's B6 row, and the E27 claim throughout. If yes → it becomes **X2** in Tier 3. | Decision + edit | 1 h (delete) |
| **T0-3** | **Delete E32–E39 from the manuscript and the battery count.** Their "BAA" arm is `gemini-2.5-flash-lite` with an advisory system prompt. Remove §8's paragraph explaining E32/E33's non-zero CUAR as a "deliberate predicate bypass" — the code does not support that explanation. Remove E38 from §15.3. | Edit | 1 h |
| **T0-4** | **Delete the BAA/L4/L5 rows of E27, E29, E30, E31, E34.** Keep the baseline halves — they are real, traced and publishable. | Edit | 1 h |
| **T0-5** | **Rewrite §17 Data Availability.** It currently promises the scripts. Do not submit that sentence while the scripts contradict the paper. State precisely what is released. | Writing | 30 min |
| **T0-6** | **Delete "≈60,000 evaluation cases" and "36 experimental layers"** from abstract, §1 contribution 3, §6.2, §18. Replace with the two suites that are real. | Edit | 30 min |
| **T0-7** | **Delete §14.4's national-scale 37,000-hazard extrapolation.** It extrapolates a CI upper bound from a benchmark that was not run. | Edit | 15 min |
| **T0-8** | **Tell your co-author** before submission, not after. | Communication | — |

**Tier 0 total: roughly 5–6 hours of editing, plus two decisions only you can make.** At the end of Tier 0 the paper is honest, narrower, and — for the first time — submittable.

### TIER 1 — VERY HIGH RETURN (small changes, substantial benefit)

| # | Task | Type | Effort | Why |
|---|---|---|---|---|
| **W4** | **Reframe E28 as exhaustive property-based coverage testing.** Replace the Wilson CI with an 11×8 coverage table (operator × base record). State the invariance explicitly. | Writing | 2–3 h | Fact 3. Converts the paper's headline from statistically indefensible to logically airtight. Zero experiments. |
| **W1** | **Narrow CL-18.** "mathematically impossible" → "structurally rejected by the certification predicate whenever the contract fields are correctly extracted and the authority record is valid." 3 occurrences (§4.6, §8.1, §14.1). | Writing | 30 min | Closes reviewer §18/§119. Strictly stronger because defensible. |
| **W2** | **Relabel all economics/latency as an analytical model.** §10.1–10.3, §7.1 footnote, abstract's "2.28×" and "89.7%". Add a parameter table. Split latency into measured / component-modelled / workload-weighted (reviewer §64). | Writing | 3–4 h | Defensible as a model, indefensible as measurement. Closes A8. |
| **W3** | **Reframe E29/E30/E31 as measured baseline-failure findings.** "LLM-judge guardrails cite obsolete gazette entries in 75% of cases — worse than no guardrail" is real, traced, and a genuinely good CEA result. | Writing | 2–3 h | Recovers real value from layers you would otherwise lose entirely. |
| **W5** | **Deduplicate E30** — it appears in both §8.5 and §9.7 with the same numbers. | Edit | 15 min | Pure inconsistency fix. |
| **W6** | **Fix `manifest.yaml`** — lists 18 sections; 15 exist (§11–13 were merged). | Edit | 10 min | Trivial, but an artifact reviewer will notice. |
| **W7** | **Add an evaluation-unit definitions paragraph** to §6 (case / mutation / system-case / configuration), per reviewer §44. | Writing | 1 h | Closes A12; makes the coverage reframing in W4 legible. |
| **W8** | **Change the registry status label** from `FROZEN_AND_VERIFIED`. §16 already concedes E27–E39 lack verification blocks; the label contradicts the concession. | Edit | 15 min | Closes A11. |
| **W9** | **Add the E28 mutation-design table** (operator / example / expected disposition / why harmful / n), per reviewer §17. The data is all in the script. | Writing | 2 h | Pre-empts A4, the most likely substantive attack on your best layer. |
| **W10** | **Strip vision-capability framing**; keep the cross-modal failure result. Delete §16's SAM/YOLOv11-seg future-work sentence — it advertises a gap in a vision-heavy journal. | Edit | 30 min | Closes A14 and removes a whole review axis. |

**Tier 1 total: ~2 days. This is where the paper stops being fragile.**

### TIER 2 — HIGH RETURN (moderate work, meaningful benefit)

| # | Task | Type | Effort | Why |
|---|---|---|---|---|
| **X1** | **M1 — real slot ablation on the E28 harness.** Disable one slot at a time in `eval_b6_11slot_single_record_baa` and re-run. Replaces E03's hardcoded table. | Experiment | 1 day | The only unavoidable experiment. CL-2 is currently unsupported. |
| **X3** | **M6 — benign-mutation control.** Add 3–4 harmless mutation operators (paraphrase, unit-equivalent restatement, formatting, whitespace) and report false-rejection rate beside harmful rejection. | Experiment | 1 day | Highest credibility-per-hour in the project. Converts "rejects everything" into "discriminates". |
| **X4** | **M-B — expand base records 8 → 40+.** Extend `BASE_FACT_TEMPLATES` from the existing fact store, covering ≥5 crop families. Broadens the coverage table from 77 to ~400+ cells. | Data | 1–2 days | Makes the coverage claim substantive rather than narrow. |
| **X5** | **M5 — Tier-0 interception count.** Run the deterministic gate over the 1,400 injection payloads; report the real count. Drop the drawn baseline percentages. | Experiment | 2–3 h | Replaces a fabricated number with a real one, cheaply. Requires the payload file. |
| **W11** | **Condense the triplicate groups:** E06/E17/E21 → one register subsection; E09/E18/E20 → one modelled economics subsection; E15/E22 → one delivery subsection. | Writing | 1 day | 12 of 36 layers are 4 results. Closes A9. |
| **W12** | **Move E12, E24, E26 to supplementary.** | Edit | 2 h | Keeps them without having to defend them. |
| **W13** | **Rewrite abstract and conclusion** from what survives. Do this *after* X1/X3/X4. | Writing | 1 day | Must be last among writing tasks. |

**Tier 2 total: ~1 week.**

### TIER 3 — OPTIONAL STRENGTHENING

| # | Task | Effort | Condition |
|---|---|---|---|
| **X2** | **M2 — controlled end-to-end benchmark, n=300**, arms A0–A4, same frozen generator/prompts/corpus. Metrics: CUAR, CAC-over-certified, coverage, appropriate **and false** abstention, per-slot violation. | 2–3 wk | **Only if a runnable system exists.** Otherwise CL-3 stays deleted. |
| **X6** | **M4 — real retrieval Hit@1 by Bengali register** on a real index. | 3–5 d | Only if CL-12 remains a motivating claim. |
| **X7** | Real LLM SMS composition for CL-11's comparison half. | 1 d | Only if CL-11 keeps a quantitative LLM comparison. |
| **X8** | A genuine, ethics-approved 3-rater expert study. | 3–4 wk | Highest standing gain at CEA; only in a full-strengthening timeline. |
| **W14** | Reviewer_1's presentation/framing items (§7–§9, §35–§39, §101–§113). Mostly good advice. | 2–3 d | Apply last, after content is settled. |

### TIER 4 — RESEARCH EXPANSION (next paper, not this one)
Coverage–safety–latency Pareto sweep (rev. §143) · model-invariance across generators (§142) · provenance-removal isolation (§94) · authority-hierarchy as its own layer (§95) · paraphrase-invariance (§96) · adversarial numerical paraphrases (§97, unless folded into X3) · localized disease segmentation.

### TIER 5 — DO NOT DO
Hardware/battery profiling (E16/E40) · telecom economics at national scale (E20) · IPM balance (E39) · escalation queueing (E38) · any field/yield/adoption study · scaling any benchmark before a measured version exists · **adding experiments to rescue a claim that a run has contradicted.**

---

## 3. STOP-ANYTIME CHECKPOINTS

Each checkpoint leaves the manuscript independently submittable and strictly better than the previous one.

### CHECKPOINT A — "if I had to submit today" *(≈ 6 hours)*
I have to be straight with you: **you cannot submit today, and Checkpoint A is the work that makes today possible.** It is almost entirely deletion.

Do T0-1 through T0-8. Then W5, W6, W8 (45 minutes of consistency fixes).

**State of the paper at A:** a verification-architecture paper whose central claim is E28's property-based rejection result plus the real baseline-failure characterisations from E29/E30/E31, with an honest limitations section. Narrower than the current draft, and the first version that is actually submittable. **Submittable: yes.**

### CHECKPOINT B — "a few more hours" *(+ ≈ 6 hours)*
Do **W4** (the E28 coverage reframing — the single highest-return task in the project), then W1, W7, W10.

**State at B:** the headline result is now stated in a form that cannot be attacked statistically, the overclaiming is gone, and the vision review axis is closed. **Submittable: yes, and meaningfully stronger.**

### CHECKPOINT C — "another day or two" *(+ ≈ 2 days)*
Do W2, W3, W9, then W12.

**State at C:** every number in the paper is either measured, or explicitly labelled as an analytical model. The recovered baseline-failure findings give the paper a second real contribution. **Submittable: yes. This is a genuinely respectable CEA submission.**

### CHECKPOINT D — "substantially more time" *(+ 1–2 weeks, or +6 weeks with X2)*
Do X1, X3, X4 (all on the E28 harness), then X5, W11, and finally W13. If a runnable system exists, add X2 and X6.

**State at D:** CL-2 restored with real evidence, the core claim falsifiable and broadly covered, scope controlled. With X2, the end-to-end claim returns. **This is the version I would want to submit.**

**Monotonicity check:** no checkpoint depends on a later one. W13 (abstract rewrite) is deliberately last within each scope so that stopping early never leaves an abstract describing work you didn't finish. X1/X3/X4 are independent of each other and each independently improves the paper.

---

## 4. LOCAL-FIRST EXECUTION — WHAT ALREADY EXISTS

| Question | Search result | Verdict |
|---|---|---|
| Can the core safety result be re-measured? | **Yes — E28 runs offline in 30 s, verified** | Re-run existing script. No new code. |
| Can the slot ablation be done without new code? | **Yes** — `eval_b6_11slot_single_record_baa` already implements all 11 slots; ablation = commenting out conjuncts | Modify existing experiment (step 4 of your sequence, not step 5) |
| Can the benign control be done without new code? | **Mostly** — reuse `generate_metamorphic_dataset()`, add benign operators alongside the 11 harmful ones | Modify existing experiment |
| Can E02 be re-run? | **No** — external dataset absent | Re-describe only; do not build on it |
| Do the baseline-failure results already exist? | **Yes** — E29/E30/E31 traces are real and complete for B0/B1/B4 | Reanalyse existing results (step 3). No re-run. |
| Is the latency/cost story recoverable? | **Yes, as a model** — parameters are all in the scripts | Reanalyse + relabel. No experiment. |
| Does the injection payload file exist? | **Unknown** — E07/E08 generates payloads in-script from templates | Check before scheduling X5 |
| Does a runnable advisory system exist? | **Unknown** — folder not connected | **Blocks X2 only** |

**No task in this roadmap requires writing a new experimental harness from scratch.** Three of the four experiments are edits to a file that already runs.

---

## 5. EXPERIMENT DEPENDENCY CONTROL

### X1 — Real slot ablation *(replaces E03)*
- **Purpose:** measure each contract slot's contribution to hazard rejection.
- **Claim:** CL-2 (central, currently unsupported).
- **Input:** `run_e28_metamorphic_eval.py`; `eval_b6_11slot_single_record_baa`; the generated 11,000-case set.
- **Output:** 11 single-slot-disabled configurations × rejection rate per mutation class, as a coverage table.
- **Success:** each slot shows a non-trivial rejection loss on the classes it governs → CL-2 restored.
- **Failure:** a slot shows ~zero contribution → **report it and consider a 10-slot contract.** This is a *good* outcome, not a problem.
- **Stop when:** all 11 configurations have run once on the expanded record set.
- **Follow-ups allowed?** **No.** Specifically: no multi-slot interaction ablation, no slot-ordering study, no re-tuning to make a weak slot look load-bearing.
- **Max scope:** one run of 11 configurations. ~1 day.

### X3 — Benign-mutation control
- **Purpose:** establish that the verifier *discriminates* rather than merely rejects.
- **Claim:** CL-1's falsifiability.
- **Input:** same generator; add 3–4 semantically-harmless operators.
- **Output:** false-rejection rate on benign mutations, reported beside harmful rejection.
- **Success:** low FRR → the rule discriminates. **Failure:** high FRR → that is the measured cost of fail-closed; put it in Discussion beside the coverage trade-off. Either result is publishable.
- **Stop when:** FRR is reported once.
- **Follow-ups allowed?** **No.** Do not tune the verifier to improve FRR. If you tune, you must re-run everything and you have started a chain.
- **Max scope:** ~1 day.

### X4 — Base-record expansion
- **Purpose:** broaden the coverage claim from 8 records to 40+.
- **Claim:** CL-1's generality.
- **Input:** `BASE_FACT_TEMPLATES` + the existing fact store.
- **Output:** coverage table across ~40 records × 11 classes.
- **Stop when:** 40–50 records spanning ≥5 crop families are in place and the suite runs.
- **Follow-ups allowed?** **No.** Do not push toward hundreds — diversity is the point, volume is not, and volume is exactly the error the current paper already made.
- **Branching risk:** if expansion reveals records the verifier mishandles, **that is a finding** — report it as a scope boundary. Do not launch a repair project.

### X5 — Tier-0 interception count
- **Purpose:** replace CL-9's drawn numbers with a real count.
- **Precondition:** the 1,400 payloads exist or can be regenerated from E07/E08's in-script templates.
- **Output:** actual interception count. **Stop when:** the count exists. **Follow-ups:** none — do not attempt to measure the LLM baselines; drop those numbers instead.

### X2 — End-to-end benchmark *(conditional)*
- **Precondition:** a runnable system. **If absent, this experiment does not exist and CL-3 stays deleted.**
- **Scope cap:** n=300, five arms, one run. **Do not scale to 500 or 1,000 until n=300 exists.**
- **Failure interpretation:** a small non-zero CUAR is *more* credible than 0.0% and does not invalidate the architecture — report it.
- **Follow-ups allowed?** One, and only one: if n=300 shows a wide CI on the primary endpoint, extending to n=500 is permitted. Nothing else.

**Global chain-breaker:** if an experiment confirms the existing conclusion, stop. If it contradicts it, narrow the claim. Do not run a further experiment to recover the original wording. The project's current state is what happens when this rule is absent.

---

## 6. FINAL EXECUTION TABLE

| P | Task | Why | Type | Claim | Local? | Effort | Benefit | Risk | Depends | Stop when | Done when |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **T0-1** Decide/delete E13 | Desk-reject + integrity | Decision | CL-4 | No | 1 h–days | Blocking | — | — | Documented or removed | No trace of an undocumented study |
| 2 | **T0-2** Decide/delete CL-3 | No traces exist | Decision | CL-3 | Unknown | 1 h | Blocking | — | — | Evidenced or removed | Abstract matches evidence |
| 3 | **T0-3** Remove E32–E39 | Prompted LLM labelled "BAA" | Edit | — | Yes | 1 h | Very high | None | — | All refs gone | grep finds none |
| 4 | **T0-4** Remove unmeasured BAA rows | Verdicts assigned | Edit | CL-3,6,7,8 | Yes | 1 h | Very high | None | — | Rows gone, baselines kept | Tables consistent |
| 5 | **T0-5** Rewrite Data Availability | Promises contradicting scripts | Writing | — | — | 30 m | Very high | None | 3,4 | Statement is accurate | — |
| 6 | **T0-6** Delete "60,000 / 36 layers" | Evidence inflation | Edit | — | — | 30 m | High | None | — | Both gone | grep finds none |
| 7 | **T0-7** Delete §14.4 extrapolation | From an unrun benchmark | Edit | — | — | 15 m | High | None | — | Paragraph gone | — |
| 8 | **W5/W6/W8** Consistency fixes | Contradictions | Edit | — | Yes | 45 m | Medium | None | — | Fixed | — |
| 9 | **W4** E28 coverage reframing | **Highest return in project** | Writing | CL-1 | Yes | 2–3 h | **Very high** | None | — | CI replaced by coverage table | 11×8 table in §8 |
| 10 | **W1** Narrow CL-18 | Overclaiming | Writing | CL-18 | — | 30 m | High | None | — | 3 sites reworded | — |
| 11 | **W7** Evaluation-unit definitions | Comparability | Writing | — | — | 1 h | Medium | None | 9 | Paragraph in §6 | — |
| 12 | **W10** Strip vision framing | Closes a review axis | Edit | — | — | 30 m | Medium | None | — | Framing + future-work line gone | — |
| 13 | **W2** Relabel economics as model | Model ≠ measurement | Writing | CL-10 | Yes | 3–4 h | High | None | — | Parameter table added | — |
| 14 | **W3** Reframe E29/30/31 | Recovers real value | Writing | CL-6,7,8 | Yes | 2–3 h | High | None | 4 | Baseline framing done | — |
| 15 | **W9** Mutation-design table | Pre-empts A4 | Writing | CL-1 | Yes | 2 h | Medium-high | None | 9 | Table complete | — |
| 16 | **W12** E12/E24/E26 → supplement | Undefendable if kept | Edit | — | Yes | 2 h | Medium | None | — | Moved | — |
| 17 | **X1** Real slot ablation | CL-2 unsupported | Experiment | CL-2 | **Yes** | 1 d | Very high | Low | 20 | 11 configs run once | Table replaces E03 |
| 18 | **X3** Benign control | Makes CL-1 falsifiable | Experiment | CL-1 | **Yes** | 1 d | **Very high** | Low | 20 | FRR reported | Reported beside harmful |
| 19 | **X5** Tier-0 count | Real number for CL-9 | Experiment | CL-9 | Partial | 3 h | High | Low | payloads | Count exists | — |
| 20 | **X4** Expand base records | Generality | Data | CL-1 | Yes | 1–2 d | Very high | Low | — | 40–50 records | Suite runs |
| 21 | **W11** Condense triplicates | 12 layers = 4 results | Writing | CL-10,11,12 | Yes | 1 d | High | None | 13 | Three groups merged | — |
| 22 | **X2** End-to-end n=300 | Restores CL-3 | Experiment | CL-3 | Unknown | 2–3 wk | High | Medium | system | n=300 run once | — |
| 23 | **X6** Real register Hit@1 | Underwrites CL-12 | Experiment | CL-12 | Partial | 3–5 d | High | Low | index | Measured once | — |
| 24 | **W13** Rewrite abstract/conclusion | Must match final evidence | Writing | All | — | 1 d | High | None | **all** | Matches | Every number traceable |
| 25 | **W14** Reviewer framing items | Good advice, low urgency | Writing | — | Yes | 2–3 d | Medium | None | 24 | Applied | — |

---

## 7. CHRONOLOGICAL CHECKLIST

**Checkpoint A — become submittable (~6 h)**
- [ ] 1. Answer: did the E13 agronomist study happen, with consent and ethics approval?
- [ ] 2. Answer: does a runnable system exist at `d:\KrishokChat Advisory System`?
- [ ] 3. Execute the E13 branch — document fully, or delete every reference (abstract, §6.5, §7.2, §14, §18, `\HumanGwetAC`)
- [ ] 4. Execute the CL-3 branch — schedule X2, or delete abstract sentence, §7.1, Table 5 B6 row
- [ ] 5. Remove E32–E39 everywhere, including §8's "deliberate predicate bypass" paragraph and §15.3's E38 citation
- [ ] 6. Remove the BAA/L4/L5 rows of E27, E29, E30, E31, E34 — keep every baseline
- [ ] 7. Rewrite §17 Data Availability to state exactly what is released
- [ ] 8. Delete "≈60,000 evaluation cases" and "36 experimental layers" (abstract, §1, §6.2, §18)
- [ ] 9. Delete §14.4's national-scale extrapolation
- [ ] 10. Fix `manifest.yaml` (18→15 sections); deduplicate E30 (§8.5 / §9.7); change the `FROZEN_AND_VERIFIED` label
- [ ] 11. Tell your co-author
- [ ] **→ PAPER IS SUBMITTABLE**

**Checkpoint B — strengthen the headline (+6 h)**
- [ ] 12. Reframe E28 as property-based coverage testing: replace the Wilson CI with an 11×8 operator×record coverage table; state within-cell invariance explicitly
- [ ] 13. Narrow "mathematically impossible" at its 3 sites
- [ ] 14. Add the evaluation-unit definitions paragraph to §6
- [ ] 15. Strip vision-capability framing; delete the SAM/YOLOv11-seg future-work sentence
- [ ] **→ STILL SUBMITTABLE, MATERIALLY STRONGER**

**Checkpoint C — every number honest (+2 d)**
- [ ] 16. Relabel all economics/latency as an analytical model; add a parameter table; split the latency story three ways
- [ ] 17. Reframe E29/E30/E31 as measured baseline-failure findings
- [ ] 18. Add the E28 mutation-design table
- [ ] 19. Move E12, E24, E26 to supplementary
- [ ] **→ RESPECTABLE CEA SUBMISSION**

**Checkpoint D — restore the mechanism (+1–2 wk)**
- [ ] 20. Expand `BASE_FACT_TEMPLATES` from 8 to 40–50 records across ≥5 crop families
- [ ] 21. Run X1 — 11 single-slot ablation configurations; replace E03's table
- [ ] 22. Run X3 — add benign operators; report false-rejection rate beside harmful rejection
- [ ] 23. Run X5 — Tier-0 interception count over the injection payloads
- [ ] 24. Condense E06/E17/E21, E09/E18/E20, E15/E22 into one subsection each
- [ ] 25. *(If system exists)* Run X2 at n=300; optionally X6
- [ ] 26. Rewrite abstract and conclusion from what survives — **last**
- [ ] 27. Apply reviewer_1's framing items (§7–§9, §35–§39, §101–§113)
- [ ] **→ THE VERSION WORTH SUBMITTING**

---

## 8. FINAL SUBMISSION GATE

Verification only. Do not add work here unless a genuine submission-critical problem remains.

**Claims and evidence**
- [ ] Every central claim is either measured, labelled as an analytical model, or removed — none is asserted from an assigned verdict
- [ ] No claim in the abstract lacks a corresponding result section with real evidence
- [ ] No statistical interval is computed over replicates of a deterministic condition
- [ ] The certification claim is stated as coverage over classes × records, not as a sampled proportion
- [ ] "Impossible" / "guarantee" language is scoped to the predicate's stated conditions

**Scope**
- [ ] No component remains whose cascading reviewer expectations exceed its claim-support value
- [ ] Layers with no supporting claim are removed or in supplementary
- [ ] Triplicate layer groups are condensed
- [ ] No aggregate case/layer counts that sum simulations and constants

**Experiments**
- [ ] Required experiments complete (X1, X3, X4 at minimum, if you reached D)
- [ ] Every experiment run had a stated stopping condition and stopped there
- [ ] No experiment triggered an unplanned follow-up chain
- [ ] Removed experiments are removed from text, tables, figures, macros and the battery count alike

**Consistency**
- [ ] Every number in the text matches its table, figure and results file
- [ ] Table 5 and §7 agree after the B6 row removal
- [ ] Figures 3, 4, 5, 6 match the surviving results (regenerate any that plot deleted rows)
- [ ] LaTeX macros in the driver correspond only to surviving claims
- [ ] Section cross-references resolve (§11–13 no longer exist)
- [ ] `manifest.yaml`, `README.md` and `results.yaml` layer counts agree with the manuscript

**Reviewer-critical issues**
- [ ] A1 (replicate counting) — resolved by the coverage reframing
- [ ] A2 (missing traces) — resolved by evidencing or removing CL-3
- [ ] A3 (ethics) — resolved by documentation or removal
- [ ] A4 (synthetic ease) — resolved by the benign control and mutation-design table
- [ ] A5 (self-evaluation) — stated plainly: E28 evaluates the certification *rule*, not the deployed implementation
- [ ] A10 (E32/E33 contradiction) — resolved by removal

**Venue and reproducibility**
- [ ] Ethics approval and consent statement present if any human-subjects claim survives
- [ ] Declaration of generative-AI use present per Elsevier policy
- [ ] Data Availability statement describes exactly what is released and is true
- [ ] Released scripts do not contradict the manuscript
- [ ] Agricultural relevance is explicit throughout — crop protection, not RAG security
- [ ] Competing interests and CRediT statements complete

---

## CLOSING

The shortest honest path is six hours of deletion, then two days of rewriting, then — if you want the mechanism back — three edits to a script that runs in thirty seconds.

The most valuable single thing you can do costs an afternoon and no experiments: **stop claiming 11,000 samples and start claiming exhaustive coverage of 11 mutation classes across 8 records.** That is what you actually did, it is a legitimate and respected form of evidence for a deterministic verifier, and unlike the current framing it cannot be taken apart.
