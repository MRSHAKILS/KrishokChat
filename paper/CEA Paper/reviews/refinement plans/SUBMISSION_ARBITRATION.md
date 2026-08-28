# Evidence and Scope Arbitration
**Project:** Bounded-Authority Agricultural Advisory (KrishokChat / BAA)
**Venue:** *Computers and Electronics in Agriculture* (Elsevier)
**Date:** 2026-08-28
**Inputs:** manuscript (15 §, 10 tables, 6 figures), reviewer_1.md (4,597 lines), the post-experiment audit, the claim–evidence matrix, local artifacts, CEA calibration.
**Role:** decide what happens to this project before submission. Not a review.

---

## 0. ONE NEW FINDING THAT MOVES THE ARBITRATION

While grounding the minimum-evidence set I re-examined the two layers the audit had classified as genuinely real. They are real — but **their statistics are inflated by replicate counting**, and this must be settled before anything else is decided.

- **E28.** `generate_metamorphic_dataset()` draws from **8 base fact templates** × 11 mutation operators. Mutation *values* vary; the underlying agronomic records do not. For the deterministic verifiers the verdict is fixed by operator class, which is why B5 scores exactly 63.64% (7/11), false-certifies exactly 36.36% (4/11), and shows CUAR 27.27% (3/11) — exact elevenths.
- **E02.** Per-family dangerous acceptance for the lexical baseline is exactly 100.0% in eight families and exactly 0.0% in two. No within-family variation whatsoever.

So the honest unit of independent evidence in the paper's strongest result is **8 base records × 11 mutation classes ≈ 88 cells**, not 21,000 cases. The reported "95% CI [99.96, 100.0]" on n=11,000 treats 1,000 replicates of one condition as 1,000 independent observations. It is not a defensible interval.

**This is good news, not bad.** The finding is real and the mechanism holds across every class tested. The fix is an **analysis fix plus a data-expansion task**, not a new experiment — and it is the single highest-leverage action available. See M-A and M-B in Part 8.

The arbitration below is gated on the two unresolved questions from the audit (E13 reality; runnable system). Where a decision depends on them, both branches are given.

---

## 1. CLAIM-FIRST DECISIONS

Intervention codes: **A** keep · **B** rewrite/narrow · **C** add analysis · **D** use existing local evidence · **E** run new experiment · **F** remove.

| Claim | Status | Intervention | Decision |
|---|---|---|---|
| **CL-1** Single-record 11-slot binding defeats relational misbinding | **Mostly established, statistically overstated** | **B + C (+ cheap data expansion)** | Keep the finding; recompute at the correct unit (mutation class × base record); report per-class rejection with class-level agreement rather than a Wilson CI on 11,000. Expand base templates 8 → 40+. **Do not run a new experiment.** |
| **CL-2** Each contract slot is individually load-bearing (dosage +31.6 pp, polarity +17.8 pp) | **Unsupported** — hardcoded constants | **E (smallest possible)** | The E02/E28 harness already computes this. Disabling one slot at a time and re-running is hours of work on existing code. Only genuine MUST-RUN in the project. |
| **CL-3** 97.0% CAC / 0.0% CUAR on live end-to-end benchmark | **Unsupported** — verdict assigned, zero traces | **F, or E if a real system exists** | **Branch 2A (system exists):** run one controlled benchmark, n=300. **Branch 2B (no system):** remove the claim from abstract, §7.1 and Table 5 entirely. Do not weaken it — remove it. |
| **CL-4** Agronomist study: 4.82/5, 100% safety pass, AC1 0.862 | **Unsupported** — literals, no data, no ethics statement | **F, or D if records exist** | **Branch 1A (study happened):** produce ratings + consent + ethics approval, add the statement, keep. **Branch 1B (it did not):** delete every reference — abstract, §6.5, §7.2, §14, §18. There is no intermediate option. |
| **CL-5** 84.56% coverage at 1.26% selective risk | **Weakly established** — Monte Carlo from `random.random() < 0.85` | **B** | Remove from abstract. Retain in §9.1 relabelled as a design-analysis of the selective policy under stated assumptions. No experiment. |
| **CL-18** Misbinding is "mathematically impossible" | **Overclaimed** | **B** | "Structurally rejected by the certification predicate whenever the contract fields are correctly extracted and the authority record is valid." Free; strictly stronger rhetorically because it is defensible. |
| **CL-6/7/8** Parametric / temporal / cross-modal (E29, E30, E31) | **Baseline half established; BAA half unsupported** | **B + D** | Reframe as measured failure characterisations of existing systems. "LLM-judge guardrails cite obsolete gazette entries in 75% of cases, worse than no guardrail" is real, traced, and a genuinely publishable CEA finding. Drop the BAA rows. |
| **CL-9** 0.0% injection survivability, 1,400 attacks | **Unsupported** — outcomes drawn from constants | **B + E(small)** | Narrow to what is deterministically checkable: run the Tier-0 gate over the payload file and report the actual interception count. Minutes of work. Drop the baseline percentages entirely — they were drawn. |
| **CL-10** 61.5% zero-LLM, 2.28×, 89.7% cost | **Weakly established as measurement; sound as a model** | **B** | Relabel throughout as an analytical model with parameters stated in a table. Reviewer §63–65 asks for exactly this. Zero experimental cost. |
| **CL-11** SMS: 100% slot fidelity vs 64.4% LLM hazard | **Half established** | **B + E(optional)** | Deterministic template side is checkable and true. LLM side was drawn — either measure it with one API loop or state the comparison qualitatively. |
| **CL-12** Register-dependent retrieval degradation; gating recovers it | **Weakly established** — Monte Carlo | **E (high value)** | This motivates the entire design. Retrieval Hit@1 by register is measurable without the advisory system. |
| **CL-13/14/15/17** Network sim, tamper detection, traversal, router | **Adequately established** | **A** | Keep as written. Already correctly caveated. |
| **CL-16** 18-minute gap closure | **Weakly established**, single case | **B → supplement** | One sentence or move out. |

**Count: one MUST-RUN (CL-2), one conditional MUST-RUN (CL-3), two small high-value runs (CL-9, CL-12), one records question (CL-4). Everything else is writing or analysis.**

---

## 2. EXPERIMENT DECISION MATRIX

| Layer | Decision | Sci. value | Claim support | Reviewer-risk ↓ | Scope risk | Redundancy | Cost | Changes conclusion? |
|---|---|---|---|---|---|---|---|---|
| **E02** misbinding | **KEEP + re-analyse** | High | CL-1 core | High | None | Overlaps E05, E28 | Low | No — but fixes its own statistics |
| **E28** metamorphic | **KEEP + re-analyse + expand base records** | **Highest in project** | CL-1 core, B5/B6 isolation | Very high | None | Subsumes E05 | Low–Med | No |
| **E03** slot ablation | **RUN** (on E02 harness) | High | CL-2 core | Very high | None | — | Low | Possibly — a slot may prove non-load-bearing, which is fine and publishable |
| **E05** counterfactual | **REMOVE** | Low | Duplicates CL-1 | — | None | Fully subsumed by E28 | — | No |
| **E04** risk-coverage | **LIGHT TOUCH** → design analysis | Medium | CL-5 | Medium | Medium | — | None | No |
| **E06 / E17 / E21** registers | **CONDENSE to one** + **RUN M4** | Medium–High | CL-12 | High | Low | Three views of one model | Low | Possibly |
| **E07/E08** injection | **CONDENSE** + **RUN** Tier-0 count | Medium | CL-9 | Medium | Low | E22 duplicates | Very low | No |
| **E09 / E18 / E20** latency & cost | **CONDENSE to one modelled subsection** | Medium | CL-10 | Medium | **High if left as measurement** | Three views of one model | None | No |
| **E10** failure taxonomy | **KEEP if the 100 cases were genuinely audited; else REMOVE** | Medium | Discussion | Medium | Low | — | None | No |
| **E11** multi-generator | **REMOVE** | Low | — | — | Medium | — | — | No |
| **E12** retrieval degradation | **MOVE TO SUPPLEMENT** or **RUN** | Medium | CL-1 robustness | Medium | Low | — | Low | No |
| **E13** human study | **AUTHOR DECISION — blocking** | — | CL-4 | — | — | — | — | **Yes, decisively** |
| **E14** network sim | **KEEP** (honest) | Medium | CL-13 | Low | Low | — | None | No |
| **E15 / E22** SMS | **CONDENSE to one** | Medium | CL-11 | Medium | Low | Duplicates | Low | No |
| **E16 / E40** hardware, battery | **DO NOT RUN · REMOVE** | Low | None | — | High | — | — | No |
| **E19** traversal (23 nodes) | **KEEP, one sentence** | Low–Med | CL-15 | Low | Medium | — | None | No |
| **E23** tamper detection | **KEEP** | Medium | CL-14 | Medium | Low | — | None | No |
| **E24** growth loop | **MOVE TO SUPPLEMENT** | Low | CL-16 | Low | Medium | — | — | No |
| **E25** intent router | **CONDENSE** to engineering detail | Medium | CL-17 | Low | Low | — | None | No |
| **E26** chunk fallback | **MOVE TO SUPPLEMENT** | Low–Med | Coverage | Low | Medium | — | — | No |
| **E27** live benchmark | **REMOVE as-is; RUN replacement if system exists** | — | CL-3 core | Very high | Low | Absorbs E34, E29/30/31 BAA rows | Med–High | **Yes** |
| **E29** parametric | **KEEP baseline half; REMOVE BAA row** | Medium–High | CL-6 | High | Low | — | None | No |
| **E30** temporal | **KEEP baseline half; REMOVE BAA row; deduplicate** (appears in §8.5 *and* §9.7) | High | CL-7 | High | Low | Self-duplicated | None | No |
| **E31** cross-modal | **KEEP baseline half; REMOVE BAA row** | Medium | CL-8 | Medium | **High** — invites a vision review axis | — | None | No |
| **E32 / E33** routing | **REMOVE** | None | None | **Removes a serious risk** | High | — | — | No |
| **E34** architectural ablation | **REMOVE**; role absorbed by the M2 benchmark | — | CL-3 | High | Low | — | — | No |
| **E35 / E36 / E37 / E38 / E39** | **REMOVE** | None | None | High | High | — | — | No |
| **M6** benign-mutation control | **RUN** | High | CL-1 falsifiability | **Highest per unit cost** | None | — | Low | Possibly — may reveal over-rejection |
| Reviewer §142 model invariance | **DO NOT RUN** | Low | — | Low | High | — | — | No |
| Reviewer §143 Pareto sweep | **DEFER** to next paper | Medium | — | Low | Very high | — | High | No |
| Reviewer §94/§95/§96/§97 | **DEFER / fold into M6** | Low–Med | — | Low | Medium | — | — | No |

**Net: 34 layers become ~12. Four experiments run, three of them cheap.**

---

## 3. OUT-OF-SCOPE TEST — CASCADING EXPECTATIONS

For each suspicious component: *if it stays, what does a reviewer now get to demand?*

| Component | Expectations it creates | Worth it? |
|---|---|---|
| **E20 telecom economics (BDT, national projections)** | Real tariff data · traffic modelling validation · sensitivity analysis · an economist reviewer · comparison to actual extension-service cost | **No.** Supports no central claim, opens an entire review axis CEA reviewers are unqualified to assess and will therefore treat as unverified. **REMOVE.** |
| **E31 multimodal / vision framing** | Detection vs classification comparison · standard vision baselines (YOLO, ViT) · a plant-disease image dataset · per-class accuracy · field images · a vision reviewer | **No, as a contribution.** CEA is a vision-heavy journal; foregrounding a classification-only vision component invites the harshest possible comparison. **Keep the cross-modal *baseline failure* result; strip the vision-capability framing.** §16's future-work sentence naming SAM/YOLOv11-seg should go — it advertises the gap. |
| **E16 / E40 hardware & battery** | Device matrix · thermal methodology · power measurement apparatus · comparison to on-device baselines | **No.** Never run. **REMOVE.** |
| **E38 escalation queue** | Queueing-theory validation · real call-centre data · staffing model · human-factors review | **No.** **REMOVE.** §15.3 must stop citing it. |
| **E39 IPM balance** | Agronomic IPM expertise review · non-chemical efficacy evidence · extension-practice comparison | **No.** This is the one that would draw the most hostile agronomist scrutiny for the least return. **REMOVE.** |
| **"≈60,000 cases / 36 layers"** | Per-layer scrutiny of all 36 · a reproducibility demand on each · the aggregation itself becomes the target | **No.** It converts a focused paper into 36 attack surfaces. **REMOVE both figures.** |
| **§14.4 national-scale 37,000-hazard extrapolation** | Deployment-scale evidence · population modelling · policy review | **No.** Extrapolates from a benchmark that was not run. **REMOVE.** |
| **§17 Data Availability promising all scripts** | Artifact inspection | Currently the highest-risk sentence in the manuscript. **Do not submit it until the scripts match the paper.** |
| **Selective-risk calibration in the abstract** | Conformal comparison · calibration methodology review · held-out validity | Borderline. **Demote to §9.** |
| **E02/E28 (kept)** | How were adversarial cases generated? Are they too easy? What is the base-record diversity? Is there a benign control? | **Yes, worth it** — this is the contribution. But the expectations are *predictable and cheap to satisfy* (M-A, M-B, M6). That is the definition of a component worth keeping. |

**Principle applied:** every removed component above is one whose cascading expectations exceed its claim-support value. Every retained component's expectations are answerable with work already scoped.

---

## 4. MINIMUM SUFFICIENT EVIDENCE SET

The smallest package that makes the central contribution convincing at CEA. Not the smallest paper — the smallest *sufficient* one.

**Problem establishment**
1. Real retrieval Hit@1 by Bengali register (**M4**, to be run) — establishes that the failure mode is real and language-driven.
2. Measured baseline failure characterisation from E29/E30/E31 baseline halves — establishes that current systems (including LLM-judge guardrails) fail in agronomically specific, dangerous ways. **Already measured, already traced.**

**Contribution and method**
3. The 11-slot contract, the certification predicate, and the authority/validity model (§3, §4, §5). Analytical, no evidence needed beyond clear statement.
4. Knowledge governance and provenance (§5) + **E23** tamper detection. Already real.

**Key result**
5. **E02 + E28, re-analysed at the correct unit and with an expanded base-record set** (**M-A, M-B**) — the core safety claim.
6. **E28's B5-vs-B6 isolation** — the causal attribution. This is the paper's best single piece of evidence and it already exists.
7. **E03 re-run for real** (**M1**) — per-slot contribution, the mechanistic argument.
8. **M6 benign-mutation control** — converts "rejects everything harmful" into "discriminates harmful from harmless". Without this, item 5 is unfalsifiable and a good reviewer will say so.

**Validity and supporting**
9. Deterministic Tier-0 interception count (**M5**, real).
10. Latency/cost as a clearly-labelled analytical model (E09/E18/E20 condensed).
11. E14 network simulation, kept as declared simulation.
12. E25 router + E19 traversal, one paragraph each.
13. Honest limitations section — the current §16 is already good and should be strengthened, not softened.

**Conditionally in the set**
14. **M2 end-to-end benchmark (n=300)** — required *only* if the paper claims end-to-end certified correctness. If no runnable system exists, item 14 drops out **and so does CL-3**, and the paper becomes a verification-architecture paper rather than a deployed-system paper. That is still a coherent, publishable CEA contribution.
15. **E13** — in the set only if the study is documented.

**What the MSE set is: 8 real evidence items, 4 experiments (3 cheap), 1 data-expansion task.** Against a current claimed battery of 36 layers.

---

## 5. REVIEWER ATTACK SURFACE

| # | Attack | Underlying concern | Current evidence | Sev. | Lik. | Affects acceptance? | Cheapest sufficient response | Class |
|---|---|---|---|---|---|---|---|---|
| A1 | "Your CI on 11,000 cases treats replicates as independent — you have 8 base records." | Statistical validity of the headline | E28 as written | **Critical** | **High** (any careful reviewer) | **Yes** | Recompute at class × record; expand to 40+ records | **ANALYSIS FIX + data** |
| A2 | "The 97% correctness row has no traces while the baselines do." | Provenance / integrity | None | **Fatal** | High if artifacts shared | **Yes — terminal** | Run M2, or remove CL-3 | **NEW EXPERIMENT or SCOPE REDUCTION** |
| A3 | "Where is the ethics approval for the three-agronomist study?" | Human-subjects compliance | None in manuscript | **Fatal** | **Certain** — Elsevier desk-check | **Yes — desk reject** | Produce records, or delete CL-4 | **AUTHOR DECISION** |
| A4 | "Your adversarial cases are synthetic and possibly trivially detectable." | Construct validity (reviewer §121) | Case generator | High | High | Yes | M6 benign control + a mutation-design table (reviewer §17) | **NEW EXPERIMENT (cheap) + WRITING** |
| A5 | "100% everything looks like a system evaluated against itself." | Independence of evaluation | Verifier is reimplemented in the harness, not the deployed system | High | Medium–High | Yes | State plainly that E02/E28 evaluate the *certification rule*, not the deployed implementation; that is an honest and still-valuable scope | **WRITING FIX** |
| A6 | "Is the LLM-judge baseline a strawman?" | Baseline fairness (reviewer §15) | §6.4 already concedes it | Medium | High | No | Existing concession; keep it prominent | **NO ACTION** |
| A7 | "'Mathematically impossible' is false — your own §16 lists bypass paths." | Overclaiming | — | Medium | High | No, but damages credibility | One-sentence rewrite | **WRITING FIX** |
| A8 | "Latency 3.8 ms compared against measured API wall-clock is not a comparison." | Measurement category error | §7.1 footnote already flags it | Medium | High | No | Split the latency story into measured / component / weighted (reviewer §64) | **WRITING FIX** |
| A9 | "60,000 cases across 36 layers — which of these actually bear on your claim?" | Evidence inflation | — | Medium–High | High | Possibly | Delete both figures; name the two real suites | **SCOPE REDUCTION** |
| A10 | "E32/E33 report 11% and 10% CUAR — your 0% headline is contradicted." | Internal inconsistency | §8 offers an explanation the code does not support | **High** | Medium | Yes if noticed | Remove E32/E33 entirely | **SCOPE REDUCTION** |
| A11 | "Registry says FROZEN_AND_VERIFIED but E27–E39 lack verification blocks." | Audit-trail integrity | §16 concedes it | Medium | Medium | No | Change the status label; the concession is already there | **WRITING FIX** |
| A12 | "What is a 'case'? Your units differ across layers." | Comparability (reviewer §44) | — | Medium | High | No | One definitions paragraph in §6 | **WRITING FIX** |
| A13 | "No field validation, no yield data." | External validity | — | Low–Medium | High | **No** — correctly disclaimed | Existing §15.6 / §16 | **NO ACTION** |
| A14 | "Vision is classification-only; compare to detection baselines." | Vision rigour (CEA is vision-heavy) | — | Medium | Medium | Only if vision is foregrounded | Strip vision-capability framing; keep cross-modal failure result | **SCOPE REDUCTION** |
| A15 | "Coverage falls 98%→70% — is this actually better?" | Whether the trade is worth it | E34 (unmeasured) | Medium | High | No | Own it explicitly as the paper's thesis; add false-abstention accounting from M2 | **WRITING FIX + ANALYSIS** |

**Six of fifteen attacks need only a writing fix. Three need analysis. Three need scope reduction. Two need an experiment. One needs your records.** That distribution is the whole argument against running more experiments.

---

## 6. THREE SCENARIOS

### SCENARIO A — SUBMIT NOW
**Verdict: do not.** This is not a risk judgement, it is a compliance one.

Submitting as-is means asserting in an abstract a human-subjects study whose data does not exist in the artifact, and a live benchmark result whose arm was never run, while a Data Availability statement offers the scripts that show both. Ordinary reviewer risk is not the issue. A3 alone is a desk-reject at Elsevier; A2 discovered post-acceptance is a retraction and an institutional matter for both named authors.

There is no version of "submit now" that is merely risky. **Scenario A is off the table until Part 8's author decisions are answered.**

### SCENARIO B — LIMITED REVISION *(recommended default)*
**Effort: ~2–3 weeks. Largest defensibility gain per unit work.**

1. Resolve E13 (document or delete) and CL-3 (run M2 or delete).
2. Delete E32–E39, E20, E16, E40, E05, E11, and the §14.4 extrapolation.
3. Re-analyse E02/E28 at the correct statistical unit (**M-A**); expand base records 8 → 40+ (**M-B**).
4. Run **M1** (real slot ablation) and **M6** (benign-mutation control) on the existing harness.
5. Run **M5** (Tier-0 interception count) — minutes.
6. Reframe E29/E30/E31 as measured baseline-failure findings; drop their BAA rows; deduplicate E30.
7. Relabel all economics/latency as an analytical model.
8. Apply the writing fixes: A5, A7, A8, A11, A12, A15; narrow CL-18; delete the "60,000 / 36 layers" framing.
9. Rewrite abstract and conclusion from what survives.

**Result:** a focused paper whose every number is either measured or explicitly labelled as a model. Roughly 12 evidence items. Strong CEA fit. Defensible.

### SCENARIO C — FULL STRENGTHENING
**Effort: 2–3 months. Only worth it if a real system exists.**

Everything in B, plus: **M2** at n=500 with the full A0–A4 arm ladder and false-abstention accounting; **M4** real register Hit@1 with a real retrieval index; a genuine agronomist validation study with proper ethics approval (this is the item that would most raise the paper's standing at CEA, and the one most damaged by the current E13); real LLM SMS composition for CL-11; and the mutation-design appendix from reviewer §17.

**Is C preferable? Not automatically.** C's marginal scientific value over B lives almost entirely in M2-at-500 and a real expert study. The rest is polish. If a real system exists, do **B plus those two items** and stop — that is roughly 5–6 weeks and captures ~85% of C's value. Full C risks the same failure mode that produced this situation: breadth substituting for depth.

---

## 7. STOP CONDITIONS

| Experiment | Run only if… | Stop when… | Do NOT chain into… |
|---|---|---|---|
| **M-A** re-analysis | Always — no precondition | Per-class rejection reported at class × record granularity with class-level agreement | A new statistical framework. Wilson at the right unit is enough. |
| **M-B** base-record expansion | Always | 40–50 base records drawn from the existing fact store, covering ≥5 crop families | Expanding to hundreds. Diversity matters, volume does not. |
| **M1** slot ablation | Always — CL-2 is currently unsupported | All 11 single-slot configurations report a rate on the expanded record set | Multi-slot interaction ablations. If a slot proves *not* load-bearing, **report that** and consider a 10-slot contract — do not run more experiments to rescue the 11. |
| **M6** benign control | Always | False-rejection rate on benign mutations is reported alongside harmful rejection | Tuning the verifier to improve it. If FRR is high, that is the honest cost of fail-closed and belongs in Discussion. |
| **M5** Tier-0 count | Always — minutes | An actual interception count over the 1,400 payloads exists | Re-running baselines. Drop the baseline percentages; do not attempt to measure them. |
| **M4** register Hit@1 | Only if CL-12 stays as a motivating claim | Hit@1 per register measured on a real index | Fixing retrieval. This measures the problem; solving it is another paper. |
| **M2** end-to-end benchmark | **Only if a runnable system exists.** Otherwise CL-3 is removed, not evidenced. | n=300 across the A0–A4 ladder with CUAR, CAC-over-certified, coverage, appropriate *and* false abstention | Scaling to 1,000. Do not scale until n=300 exists. If BAA's CUAR is non-zero at 300, **report it** — a small non-zero CUAR with correct framing is more credible than 0.0%, and does not invalidate the architecture. |
| **E13 replication** | Only if you choose to keep an expert claim **and** have ethics approval | 3 raters × ~100 outputs, blinded, with rating sheets retained | Expanding rater count or dimensions. Three raters is the CEA norm. |
| **Anything the reviewer proposed in §94–§97, §142, §143** | Only if a MUST-DO item fails and the gap it leaves is central | — | These are next-paper material. Explicitly deferred. |

**Global stop rule:** if an experiment confirms the existing conclusion, no follow-up is warranted. If it contradicts it, narrow the claim — do not run further experiments to recover the original wording. The project's current state is what happens when that rule is absent.

---

## 8. FINAL DECISION TABLE

| P | Item | Type | Claim | Current evidence | Action | Why | Effort | Benefit | Scope risk | Rev-risk ↓ | Local artifact? | New exp? | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **0** | E13 reality | Records | CL-4 | None | **Document or delete** | Desk-reject / integrity | — | Blocking | — | Fatal→0 | No | No | **HIGH** |
| **0** | Runnable system? | Fact | CL-3 | Unknown | **Determine** | Gates Scenario B vs reduced paper | — | Blocking | — | — | Not connected | No | **HIGH** |
| **1** | Remove E32–E39 | Scope | — | Prompted LLM as "BAA" | **REMOVE** | Publishing these is the single largest integrity exposure after E13/E27 | Hours | Very high | ↓↓ | Very high | Yes | No | **HIGH** |
| **1** | Remove E27 B6 / E34 / BAA rows of E29–E31 | Scope | CL-3, 6–8 | Assigned verdicts | **REMOVE rows, keep baselines** | Baseline halves are real, traced and publishable | Hours | Very high | ↓↓ | Very high | Yes | No | **HIGH** |
| **1** | Delete "60,000 cases / 36 layers", §14.4 | Writing | — | — | **REMOVE** | Evidence inflation; 36 attack surfaces | Hours | High | ↓↓ | High | — | No | **HIGH** |
| **2** | **M-A** re-analyse E02/E28 at correct unit | Analysis | CL-1 | Real but inflated | **DO** | Fixes the headline's statistics without new data | 1–2 d | **Very high** | None | Very high | Yes | No | **HIGH** |
| **2** | **M-B** expand base records 8→40+ | Data | CL-1 | 8 templates | **DO** | Converts the strongest result into a properly powered one | 2–4 d | **Very high** | None | Very high | Yes | Partly | **HIGH** |
| **2** | **M1** real slot ablation | Experiment | CL-2 | Hardcoded | **RUN** | Only unavoidable run; harness exists | 1–2 d | Very high | None | Very high | Yes (harness) | Yes | **HIGH** |
| **2** | **M6** benign-mutation control | Experiment | CL-1 | None | **RUN** | Makes the 100% claim falsifiable | 1–2 d | **Highest per unit cost** | None | Very high | Yes (harness) | Yes | **HIGH** |
| **3** | **M5** Tier-0 interception count | Experiment | CL-9 | Drawn | **RUN** | Minutes; replaces a fabricated number with a real one | Hours | High | None | High | Yes | Yes | **HIGH** |
| **3** | Relabel economics/latency as model | Writing | CL-10 | Model presented as measurement | **REWRITE** | Defensible as a model, indefensible as measurement | 1 d | High | ↓ | High | Yes | No | **HIGH** |
| **3** | Condense E06/E17/E21, E09/E18/E20, E15/E22 | Scope | CL-10–12 | 3×3 duplicate views | **CONDENSE** | 12 of 36 layers are 4 results | 1–2 d | High | ↓↓ | Medium | Yes | No | **HIGH** |
| **3** | Narrow CL-18, fix A5/A7/A8/A11/A12/A15 | Writing | Multiple | — | **REWRITE** | Six attacks closed by prose | 2 d | High | ↓ | High | — | No | **HIGH** |
| **4** | **M2** end-to-end n=300 | Experiment | CL-3 | None | **RUN if system exists** | Restores the end-to-end claim | 2–3 wk | High | Low | Very high | Unknown | Yes | **MED** |
| **4** | **M4** real register Hit@1 | Experiment | CL-12 | Monte Carlo | **RUN** | Underwrites the design motivation | 3–5 d | High | Low | High | Partly | Yes | **MED-HIGH** |
| **5** | Mutation-design appendix (rev. §17) | Writing | CL-1 | — | **ADD** | Pre-empts A4 | 1 d | Medium | None | Medium | Yes | No | **HIGH** |
| **5** | E12, E24, E26 → supplement | Scope | — | Weak | **MOVE** | Keeps them without defending them | Hours | Medium | ↓ | Medium | Yes | No | **MED-HIGH** |
| **6** | Real LLM SMS composition | Experiment | CL-11 | Drawn | **OPTIONAL** | One API loop | 1 d | Medium | None | Medium | Partly | Yes | **MED** |
| **6** | Genuine expert study | Experiment | CL-4 | — | **OPTIONAL / Scenario C** | Highest standing gain at CEA | 3–4 wk | High | Low | High | No | Yes | **MED** |
| — | Reviewer §142, §143, §94–97 | Experiment | — | — | **DO NOT RUN / DEFER** | Next paper | — | — | High | Low | — | — | **HIGH** |
| — | E16, E40 hardware/battery | Experiment | None | Never run | **DO NOT RUN** | No claim depends on it | — | — | High | — | Stubs | — | **HIGH** |
| — | Scale M2 to n=1,000 | Experiment | CL-3 | — | **DO NOT RUN** (yet) | Scaling before measuring is the wrong order | — | — | Medium | Low | — | — | **HIGH** |

### MUST DO
1. Answer: did the E13 study happen? Does a runnable system exist? *(blocking, both)*
2. Remove E32–E39, E27's B6 row, E34, the BAA rows of E29/E30/E31, E20, E16, E40, §14.4.
3. Delete the "≈60,000 cases / 36 layers" framing.
4. **M-A** re-analyse E02/E28 at the correct statistical unit.
5. **M-B** expand base fact records from 8 to 40+.
6. **M1** run the real slot ablation.
7. **M6** run the benign-mutation control.
8. Resolve CL-3 and CL-4 by their branch: evidence or deletion. No middle path.
9. Do not submit the current §17 Data Availability sentence.

### SHOULD DO
10. **M5** Tier-0 interception count.
11. Relabel all economics/latency as an analytical model.
12. Condense the three triplicate layer groups; deduplicate E30.
13. Reframe E29/E30/E31 as measured baseline-failure findings.
14. Narrow CL-18; apply writing fixes A5, A7, A8, A11, A12, A15.
15. Add the mutation-design table (reviewer §17).
16. Strip vision-capability framing; keep the cross-modal failure result.

### OPTIONAL IF TIME
17. **M4** real register Hit@1.
18. **M2** at n=500 rather than 300 *(only after 300 exists)*.
19. Real LLM SMS composition.
20. A genuine, ethics-approved expert study.
21. Reviewer's presentation and framing items (§7–§9, §35–§39, §101–§113) — mostly good, apply last.

### DO NOT DO
22. Model-invariance sweeps (§142); full Pareto sweep (§143); provenance-removal isolation (§94); authority-hierarchy as a separate layer (§95); paraphrase-invariance (§96) — all defer.
23. Hardware/battery profiling.
24. Any field, yield, or adoption study.
25. Scaling any benchmark before a measured version of it exists.
26. Adding experiments to rescue a claim that a run has contradicted.

### AUTHOR DECISION REQUIRED
27. **Did the E13 agronomist study take place?** Everything downstream branches here.
28. **Does a runnable KrishokChat system exist at `d:\KrishokChat Advisory System`?** Determines Scenario B vs. a reduced verification-architecture paper.
29. **Does your co-author know how these layers were produced?** Their name is on it; they should hear it from you, before submission.
30. **Have any of these numbers appeared in the prior benchmark paper or the companion EACL submission?** If so, that is a correction obligation, not a revision.
31. **Do the datasets in `research_artifacts/` exist and how were adversarial cases constructed and validated?** Reviewer §121 will ask regardless.

---

## ARBITRATION SUMMARY

The project's self-assessment is inverted. It believes it has abundant evidence needing polish. It has **one real result** — the certification rule rejects all tested corruption classes, with a clean B5-vs-B6 isolation — resting on **8 base agronomic records**, surrounded by simulations, constant tables, and arms that were never run.

The correct response is not more experiments. It is: **answer two questions, delete a third of the paper, fix the statistics on the one real result, expand its record base, and run four small things** — three of which reuse a harness that already works.

If a runnable system exists, this is a good CEA paper about six weeks away. If it does not, it is a narrower but still genuinely publishable paper about a verification architecture, and CL-3 and CL-4 must come out rather than be softened.

Either way, the largest single gain available is not experimental. It is **M-A and M-B** — correcting and broadening the evidence you already have.
