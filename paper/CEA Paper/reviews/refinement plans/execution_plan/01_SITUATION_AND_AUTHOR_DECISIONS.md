# 01 — Situation Report & Author Decisions
**Read before any task. Read before Gemini touches anything.**

---

## WHAT HAPPENED (plain language)

Previous agents ran 38 "experiment" layers to fill a paper about the BAA architecture. An independent audit of every runner script found the following:

| Class | Layers | What the script actually does |
|---|---|---|
| **REAL — deterministic logic, genuine results** | E02, E28, E23, E19, E25, E14 | Real function calls, honest outputs |
| **REAL BASELINES but BAA arm fabricated** | E27, E29, E30, E31, E34 | API traces exist for baselines only; BAA/B6 verdict was `return True`/`return False` hardcoded |
| **Hardcoded constant tables** | E03, E09, E10, E11, E12, E13, E20, E24 | Numbers typed as Python literals, no computation |
| **Monte Carlo simulation, not measurement** | E04, E05, E06, E07/E08, E15, E17, E18, E21, E22 | `random.random() < 0.84` etc — presented as measurements |
| **Prompted Gemini-Flash mislabelled "BAA"** | E32, E33, E35, E36, E37, E38, E39 | Real API calls to Gemini-Flash with an advisory system prompt |
| **Never run at all** | E16, E40 | Stub scripts only |

**The paper has exactly ONE genuinely supported central claim:**
> CL-1: The 11-slot single-record certification contract structurally rejects all tested mutation classes.

This is supported by E28 (deterministic, self-contained, runs in ~30 seconds) and E02 (real but dataset is external). Both are genuinely valuable. This one claim is enough for a CEA submission if stated correctly.

---

## THE TWO PUBLICATION-BLOCKING PROBLEMS

### Problem 1: E13 — Human Expert Validation Study

File: `experiments/E13_human_expert_validation/results.yaml`

The results show `evaluation_duration_seconds: 0.0`. The numbers (4.82/5, 100% safety pass, AC1=0.862) are Python literals in the script. The README describes "3 independent certified agricultural extension specialists" and a "double-blind" protocol. The **abstract** reports the AC1. The **manuscript §6.5** describes the blinding and randomised presentation. **§7.2** reports the rater scores.

If no real study took place, this is fabricated human-subjects data in an Elsevier submission. Elsevier requires ethics approval and consent statements for any human-participant research. The current manuscript has neither.

**→ Author must answer Q1 before anything else.**

### Problem 2: E27 — The "97.0% CAC / 0.0% CUAR" Benchmark

File: `experiments/E27_independent_expert_benchmark/real_traces_100.jsonl`

This file contains 300 real API completions — for **B0, B1, and B4 only**. There is not one B6 trace because B6 was never run. The B6 row in `results.yaml` was populated by a `baa_verifier_classify()` function that returns `is_cuar: False` in every code path. The README states "All metrics computed from 100% real live API completions. Zero synthetic data." That sentence is false for the row it defends.

**→ Author must answer Q2 before anything else.**

---

## THE TWO AUTHOR DECISIONS — ANSWER THESE NOW

### Q1: Did the E13 agronomist study actually take place?

**If YES:** You must produce:
- Raw rating sheets (per-rater, per-item scores)
- Rater consent forms
- IRB / institutional ethics approval reference number
- Proof these match the YAML numbers

Only then can E13 be kept. Task T0-1 = document it properly.

**If NO:** Every reference to the study must be deleted from the manuscript. Task T0-1 = delete. There is no middle option — softening language does not fix fabricated human-subjects data.

Write your answer here: `Q1_ANSWER: NO`

---

### Q2: Does a runnable KrishokChat system exist at `d:\KrishokChat Advisory System\backend\`?

**If YES:** The end-to-end benchmark can be re-run (Task X2 in Phase 4). CL-3 can be restored with real evidence. Task T0-2 = mark CL-3 as pending.

**If NO:** The "97.0% CAC / 0.0% CUAR" claim and all associated manuscript content must be deleted. The paper becomes a verification-architecture paper — which is still a valid, publishable CEA contribution. Task T0-2 = delete CL-3.

Write your answer here: `Q2_ANSWER: YES`

---

## CONFIRMED AUTHOR DECISIONS — 2026-08-28

```
Q1: NO  — The E13 agronomist study did not take place.
          The rating scores (4.82/5, 100% safety, AC1=0.862) are fabricated.
          ALL references must be deleted. T0-1 = BRANCH B.

Q2: YES — A runnable KrishokChat system exists.
          The end-to-end benchmark can be re-run.
          T0-2 = BRANCH A (mark CL-3 as pending X2, keep baseline table rows).
```

### Consequences locked in:

**From Q1=NO:**
- Delete `\subsection{Agronomist Validation (E13)}` from §7
- Delete §6.5 from experimental methodology
- Delete every "agronomist", "Gwet", "AC1", "4.82", "100.0% safety pass" reference from §1, §6, §7, §14, §18
- Delete `\HumanGwetAC` macro from the driver
- CL-4 is dead — do not replace it with softer language

**From Q2=YES:**
- Keep §7.1 structure but mark B6 row as `[PENDING — Task X2]`
- Delete only the B6 row from tab5, not the full table
- Phase 4 (X2 benchmark) is ACTIVE — Gemini must execute T4-1 and T4-2 after Phase 3
- When X2 runs: use the real numbers, whatever they are


---

## EVIDENCE LEDGER (what is confirmed real)

| Experiment | What it does | Evidence quality | Status |
|---|---|---|---|
| **E28** | 11 mutation classes × 8 base records, deterministic verifier | Genuine deterministic computation | KEEP — but reframe statistics (Task T1-1) |
| **E02** | 10,000 adversarial misbinding cases | Real but external dataset (cannot re-run from this folder) | KEEP — describe as frozen evidence |
| **E27 baselines** | 300 live API traces for B0, B1, B4 | Real traces, confirmed | KEEP baseline rows |
| **E29 baselines** | Parametric intrusion rates for LLMs | Real for first N cases | KEEP baseline findings |
| **E30 baselines** | Temporal conflict: LLM-judge cites obsolete gazette 75% | Real traces present | KEEP — strong finding |
| **E31 baselines** | Cross-modal conflict failure | Real traces present | KEEP baseline findings |
| **E23** | Hash-chain tamper detection | Real computation | KEEP |
| **E25** | Intent classifier latency/size | Real measurements | KEEP |
| **E19** | Graph traversal on 23 nodes | Real, already caveated | KEEP, one sentence |
| **E14** | Network degradation simulation | Honest — correctly disclosed as simulation | KEEP |

---

## THE STATISTICAL PROBLEM WITH E28 (important — read before T1-1)

E28 generates 1,000 cases per operator × 11 operators = 11,000 "cases." But the underlying
base records are only 8 crop-problem templates. For a deterministic verifier, the verdict
is **constant within each (operator, base_record) cell**. So the true independent evidence is:

- 8 base records × 11 mutation classes = **88 deterministic cells**
- Not 11,000 samples

Reporting Wilson CI [99.97, 100.0] over 11,000 replicates of a deterministic rule is not
statistically defensible. A careful reviewer will immediately see this.

**The fix is FREE and makes the result STRONGER:** Call it exhaustive property-based coverage
testing. State you evaluated all 11 mutation classes across 8 base agronomic records (88 cells)
and found complete rejection in all cells. A deterministic rule with exhaustive class coverage
is a proof-by-cases result — which is a legitimate and respected form of evidence that
cannot be attacked on statistical grounds.

Task T1-1 implements this reframing. It requires no new experiments.

---

## WHAT THE FASTEST PATH LOOKS LIKE

```
Today:    Answer Q1 and Q2

Day 1-2:  Phase 0 — deletions (5-7 hours editing)
          Phase 1 — reframing E28, relabelling economics model (2 days)

Day 3-4:  Phase 2 — expand E28 to 40 records, run slot ablation, run benign control
          (all three experiments are edits to one file that runs in 30 seconds)

Day 5:    Phase 3 — rewrite §7, §8, abstract, conclusion

After:    Weeks 2-3 if system exists: Phase 4 end-to-end benchmark
```

The paper is submittable at Checkpoint A (end of Phase 0) — narrower, but honest.
Every phase after that makes it stronger.
