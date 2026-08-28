# 02 — Phase 0: Cleanup — Remove Corrupted Material

> **CONFIRMED AUTHOR DECISIONS (read before anything else):**  
> `Q1 = NO` → T0-1 = **BRANCH B only** (E13 study never happened — delete all references)  
> `Q2 = YES` → T0-2 = **BRANCH A only** (system exists — keep §7.1, delete only B6 row)

**Who runs this:** Gemini 2.5 Flash  
**Rule:** ONE task per session. Stop and report after STOP CONDITION check. Wait for author approval.  
**Type of work:** Deletions and minimal edits only. No new content written in this phase.  
**Estimated effort:** 5–7 hours

> ⛔ **DO NOT skip STOP CONDITION checks.** Every task requires you to run the listed grep command and paste its EXACT output in your report. If you say "I deleted it" without the grep output proving zero results, the task is rejected.

> ⛔ **DO NOT do two tasks in one session.** If T0-1 is assigned, stop after T0-1. Do not start T0-2.

---

## T0-1 — Delete all E13 references (BLOCKING — do this first)

**Decision: BRANCH B (Q1=NO — study never happened)**  
**Claim affected:** CL-4 — deleted entirely  
**Why blocking:** Fabricated human-subjects data in an Elsevier submission is a desk-reject.

> Branch A does not apply. Skip it. The study did not happen.

### BRANCH B — Delete everything (ACTIVE)

BEFORE EDITING: Run this grep and paste the output in your working notes (so you know what needs to be deleted):
```powershell
cd "D:\KrishokChat Advisory System\paper\CEA Paper"
grep -rn "agronomist\|Gwet\|AC1\|HumanGwet\|4.82\|E13\|chemical-safety pass" manuscript/sections/
```

READ these files first:
- `paper/CEA Paper/manuscript/sections/06_experimental_methodology.tex` (§6.5 block)
- `paper/CEA Paper/manuscript/sections/07_results_advisory_quality.tex` (§7.2 block)
- `paper/CEA Paper/experiments/E13_human_expert_validation/results.yaml`

EDIT:
1. `experiments/E13_human_expert_validation/results.yaml` — replace all literal numbers with real data from rating sheets. Fix `evaluation_duration_seconds: 0.0` to actual duration.
2. `manuscript/sections/06_experimental_methodology.tex` §6.5 — add paragraph: ethics approval reference number, institution, consent procedure, rater recruitment, blinding confirmation.
### BRANCH B — Study did NOT happen (delete everything)

READ these files first:
- `manuscript/krishokchat_cea_main.tex` — find and delete `\HumanGwetAC` macro definition and any usage
- `manuscript/sections/01_introduction.tex` — find Table 1, line with "Gwet" or "agronomist" in RQ1 row
- `manuscript/sections/06_experimental_methodology.tex` — find §6.5 entire subsection
- `manuscript/sections/07_results_advisory_quality.tex` — find §7.2 entire subsection AND opening sentence mentioning "100.0% chemical-safety pass"
- `manuscript/sections/14_discussion.tex` — grep: agronomist, E13, expert, Gwet, AC1, 4.82
- `manuscript/sections/18_conclusion.tex` — grep same terms

EDIT steps (do ALL of them — do not skip any):
1. `07_results_advisory_quality.tex`: Delete the entire `\subsection{Agronomist Validation (E13)}` block including its content. Leave placeholder comment: `% [CL-4 REMOVED: Q1=NO — study did not take place. Author confirmed 2026-08-28.]`
2. `07_results_advisory_quality.tex` opening sentence: Remove "confirmed by three independent agronomists with a 100.0% chemical-safety pass rate" and any surrounding clause that references it.
3. `06_experimental_methodology.tex`: Delete the entire §6.5 subsection (the one describing the blinding/randomised presentation protocol for agronomists). If the surrounding text becomes broken, add one bridge sentence.
4. `01_introduction.tex` Table 1 RQ1 row: Remove "as judged by expert agronomists" phrase. Remove "Gwet's AC1" from the metric column.
5. `14_discussion.tex`: For each of these terms — agronomist, E13, Gwet, AC1, 4.82, "chemical-safety pass" — delete the entire sentence containing it. Do not soften, do not paraphrase. Delete.
6. `18_conclusion.tex`: Same — delete every sentence containing those terms.
7. `manuscript/krishokchat_cea_main.tex`: Delete the `\HumanGwetAC` macro definition. Search for `\HumanGwetAC` usage sites and delete those lines too.
8. `manifest.yaml`: Add to the comments block: `# E13 claim removed — Q1=NO, study never happened, see reviews/refinement plans/POST_EXPERIMENT_AUDIT.md`

STOP CONDITION — run this command and paste the EXACT output:
```powershell
grep -r "4.82\|Gwet\|AC1\|agronomist\|HumanGwet\|E13\|chemical-safety pass\|expert validation" manuscript/sections/
```
If the output is ANYTHING other than empty/zero matches: you are not done. Fix and re-run.

REPORT FORMAT (required):
```
## TASK T0-1 REPORT
**Files modified:** [list each file with one-line description of change]
**STOP CONDITION output:** [paste exact grep output here]
**Result:** PASS (if empty) / FAIL (if any matches remain)
**Observations outside scope:** [list any other problems noticed but not fixed]
```

---

## T0-2 — Handle CL-3 / E27 (Decision: BRANCH A — system exists)

**Decision: BRANCH A (Q2=YES — system exists, re-measurement scheduled)**  
**Claim affected:** CL-3 — "97.0% CAC / 0.0% CUAR" — mark as PENDING, not deleted  
**Why:** B6 arm had zero traces. But since the system is runnable, we will re-measure in Phase 4 (T4-1). Until then, the B6 row is deleted from the table but §7.1 is kept.

> Branch B does not apply. Skip it.

### BRANCH A — Active (system exists)

BEFORE EDITING: Run this and paste in your working notes:
```powershell
grep -rn "97\.0\|0\.0.*CUAR\|B6.*CAC\|live.*benchmark.*BAA" manuscript/sections/
```

EDIT steps (all required):
1. `07_results_advisory_quality.tex` §7.1: Where the B6 CAC/CUAR number appears, replace it with: `[PENDING: BAA arm to be measured in Task X2, Phase~4. Real number will replace this placeholder.]`
2. `manuscript/tables/tab5_end_to_end_advisory.tex`: Delete the B6 row entirely. Keep B0, B1, B4 rows. Change the caption to end with: "BAA arm excluded pending controlled re-measurement (Task X2, Phase~4)."
3. `08_results_authority_safety.tex` opening: If it contains "97.0\% CAC" as a reference to the live benchmark, remove that specific phrase. Keep any sentence that refers to E28 (metamorphic) results — those are untouched.
4. `18_conclusion.tex`: Replace "provides 97.0\% certified correctness on live farmer queries" with "will be benchmarked end-to-end in controlled conditions (Task X2)."

STOP CONDITION — run and paste EXACT output:
```powershell
grep -r "97\.0.*CAC\|97\.0.*certified\|0\.0.*CUAR" manuscript/sections/
```
Must return zero (no fabricated B6 numbers). Then confirm:
```powershell
grep -r "74\|73\|B0\|B1\|B4" manuscript/sections/07_results_advisory_quality.tex
```
Must return non-empty (baseline rows still exist).

REPORT FORMAT:
```
## TASK T0-2 REPORT
**Files modified:** [list]
**STOP CONDITION output (fabricated claims grep):** [paste]
**Baseline survival check output:** [paste]
**Result:** PASS / FAIL
**Observations outside scope:** [list]
```

---

## T0-3 — Delete E32–E39 from manuscript

**Why:** "BAA" arm in these layers is `gemini-2.5-flash-lite` with an advisory system prompt. Not the architecture under test. Publishing the §8 "deliberate predicate bypass" explanation would be the largest integrity exposure in the paper.

READ:
- `manuscript/sections/08_results_authority_safety.tex` (lines 11-12)
- `manuscript/sections/15_deployment_implications.tex`
- `manuscript/sections/10_results_robustness.tex`

EDIT:
1. In `08_results_authority_safety.tex`: delete the entire paragraph starting "Two exploratory layers (E32, oracle-vs-predicted routing; E33, high-confidence wrong metadata)..." Do not replace it with anything.
2. In `15_deployment_implications.tex`: remove every sentence citing E38 or "escalation queue."
3. In `10_results_robustness.tex`: remove every sentence citing E35, E36, E37, or E39.
4. In `manifest.yaml`: change `total_layers` and `completed_layers_count` to reflect removal. Add comment: `# E32-E39 removed: prompted LLM mislabelled as BAA. See POST_EXPERIMENT_AUDIT.md`

STOP CONDITION — run and paste EXACT output:
```powershell
grep -r "E32\|E33\|E34\|E35\|E36\|E37\|E38\|E39\|predicate bypass\|escalation queue\|IPM balance" manuscript/sections/
```
Must return zero. Then read §8 opening aloud — if the transition is broken after removing the paragraph, add ONE sentence to bridge the flow.

REPORT FORMAT:
```
## TASK T0-3 REPORT
**Files modified:** [list]
**STOP CONDITION output:** [paste exact grep output]
**§8 transition readable?** YES / NO (describe if NO)
**Result:** PASS / FAIL
**Observations outside scope:** [list]
```

---

## T0-4 — Delete fabricated BAA rows from E29, E30, E31 tables and text

**Why:** BAA arms in these layers have no traces. Keep ALL baseline rows — they are real.

READ:
- `manuscript/sections/08_results_authority_safety.tex` (§8.4, §8.5, §8.6)
- `manuscript/tables/tab8_multimodal_robustness.tex`
- `manuscript/sections/09_results_selective_reliability.tex` (check for duplicate E30)

EDIT:
1. **§8.4 (E29):** Delete "The BAA mode achieved 100.0% evidence adherence and 0.0% parametric intrusion in every model/mode cell, because the deterministic 11-slot resolver makes parametric memory irrelevant..." Add instead: "The BAA arm was not included in this layer's traces and is excluded from this characterisation."
2. **§8.5 (E30):** Delete "BAA achieved 100.0% current-gazette adherence (95% CI [96.30, 100.0]) with 0.0% obsolete leakage (CI [0.0, 3.7])..." Add: "The BAA arm is excluded pending controlled re-measurement." Keep ALL baseline numbers (LLM 39%, RAG 39%, LLM-judge 75%).
3. **§8.6 (E31):** Delete "BAA triggered a safe clarification request in 100.0% of conflicted inputs (95% CI [98.77, 100.0]) and delivered 0.0% wrong chemical recommendations." Keep: "The unconstrained multimodal LLM delivered the wrong recommendation in 54.0% of cases." Add: "BAA arm excluded."
4. In `tab8_multimodal_robustness.tex`: delete the BAA/B6 row. Add footnote: "BAA arm excluded from this layer; see §8.6."
5. In `09_results_selective_reliability.tex`: grep for "E30". If E30 data appears here (duplicate), delete it — keep it only in §8.5.

STOP CONDITION — run TWO checks, paste EXACT output of both:
```powershell
# Check 1: fabricated BAA claims gone
grep -r "100\.0.*gazette\|100\.0.*clarification\|0\.0.*parametric intrusion\|0\.0.*CUAR.*BAA" manuscript/sections/
# Check 2: real baseline findings still present
grep -r "75.*obsolete\|LLM-judge.*75\|39.*gazette" manuscript/sections/08_results_authority_safety.tex
```
Check 1 must return zero. Check 2 must return non-empty (the 75% LLM-judge finding must survive).

REPORT FORMAT:
```
## TASK T0-4 REPORT
**Files modified:** [list]
**STOP CONDITION Check 1 output (fabricated claims):** [paste]
**STOP CONDITION Check 2 output (baseline survival):** [paste]
**Result:** PASS / FAIL
**Observations outside scope:** [list]
```

---

## T0-5 — Rewrite §17 Data Availability statement

**Why:** §17 promises all runner scripts. Those scripts contain fabricated outputs. Do not submit a promise that the scripts contradict.

READ: `manuscript/sections/17_reproducibility.tex`

EDIT:
1. Replace `\subsection{Submission Package}` paragraph with:
```latex
\subsection{Data and Code Availability}
The submission bundle contains: the \LaTeX{} sources, per-layer README files and results
YAML files for surviving layers, the E28 metamorphic evaluation harness
(\texttt{run\_e28\_metamorphic\_eval.py}), and the E23 tamper-detection harness. Runner
scripts for layers E32--E39 are not included in this submission; those layers have been
withdrawn. The institutional corpus (2,946 BARI/BRRI/DAE extension documents) is not
redistributed but is available through the respective institutions' public release channels.
All evaluation seeds and environment specifications are recorded in the per-layer README
files.
```
2. In `\subsection{Experiment Registry}`: change "Layers E02--E26 additionally record a verification block" to "Layers E02, E14, E19, E23, E25, E28 carry full verification blocks."

STOP CONDITION — read §17 in full and answer each question:
1. Does any sentence promise scripts for E32–E39? Must be NO.
2. Does any sentence describe data that does not exist? Must be NO.
3. Is the E28 harness correctly named? Must be YES.

REPORT FORMAT:
```
## TASK T0-5 REPORT
**Files modified:** [list]
**Q1 — E32-E39 scripts still promised?** YES (FAIL) / NO (PASS)
**Q2 — Any non-existent data promised?** YES (FAIL) / NO (PASS)
**Q3 — E28 harness filename correct?** YES (PASS) / NO (FAIL)
**Result:** PASS / FAIL
**Observations outside scope:** [list]
```

---

## T0-6 — Delete "≈60,000 cases" and "36 experimental layers" everywhere

**Why:** These totals include simulated draws and constant tables. The most attackable sentence in the paper.

GREP to find all occurrences:
```
grep -rn "60,000\|60000\|36 experimental\|36 layers\|36.*layer" manuscript/sections/
```

EDIT each occurrence:

- In `01_introduction.tex` line 53 (contribution 3): replace `spanning 36 experimental layers and $\approx$60,000 evaluation cases` with `spanning an exhaustive metamorphic authority test suite, an adversarial misbinding battery, and real live-API baseline characterisations`
- In `18_conclusion.tex` line 10: replace `Across 36 experimental layers spanning $\approx$60,000 cases, the architecture demonstrates` with `Across adversarial and metamorphic evaluation suites, the architecture demonstrates`
- In `06_experimental_methodology.tex`: remove any sentence stating total layer count or total case count.

STOP CONDITION — run and paste EXACT output:
```powershell
grep -r "60,000\|60000\|36 experimental\|36 layers" manuscript/sections/
```
Must return zero.

REPORT FORMAT:
```
## TASK T0-6 REPORT
**Files modified:** [list]
**STOP CONDITION output:** [paste exact grep output]
**Result:** PASS / FAIL
**Observations outside scope:** [list]
```

---

## T0-7 — Delete §14.4 national-scale extrapolation

**Why:** Extrapolates a CI upper bound from the E27 benchmark that was never run.

READ: `manuscript/sections/14_discussion.tex`

GREP: `grep -n "37,000\|national.*scale\|37000\|hazard.*intervention\|14\.4" manuscript/sections/14_discussion.tex`

EDIT: Delete the subsection §14.4 and its paragraph(s) about national-scale 37,000-hazard interventions. If removing the heading leaves the surrounding structure broken, fix only the section flow.

STOP CONDITION — run and paste EXACT output:
```powershell
grep -r "37,000\|37000\|national.*scale.*hazard" manuscript/sections/14_discussion.tex
```
Must return zero.

REPORT FORMAT:
```
## TASK T0-7 REPORT
**Files modified:** [exact path + what was removed]
**STOP CONDITION output:** [paste exact grep output]
**Result:** PASS / FAIL
**Observations outside scope:** [list]
```

---

## T0-8 — Fix manifest.yaml and remove duplicate E30

**Why:** Three minor but reviewer-visible inconsistencies: manifest lists 38 layers/18 sections, a E30 duplicate exists in §9, and the FROZEN_AND_VERIFIED label contradicts §16's own concession.

READ:
- `paper/CEA Paper/manifest.yaml`
- `manuscript/sections/09_results_selective_reliability.tex` (grep for "E30")

EDIT:
1. `manifest.yaml`:
   - `total_layers: 38` → `total_layers: 20`
   - `completed_layers_count: 36` → `completed_layers_count: 12`
   - `planned_layers_count: 2` → `planned_layers_count: 5`
   - Add comment: `# Counts updated 2026-08-28 after audit. Removed: E32-E39 (8 layers), E20, E16, E40 (3 layers). Planned: M1, M6, X4, X5, X2.`
2. Remove §11, §12, §13 from `manifest.yaml` sections list (they don't exist as .tex files)
3. In `09_results_selective_reliability.tex`: if E30 data appears, delete it — keep only in §8.5.

STOP CONDITION — answer ALL of the following, paste evidence for each:
```powershell
# 1. What are the current manifest counts?
grep -E "total_layers|completed_layers|planned_layers" "paper/CEA Paper/manifest.yaml"

# 2. Does manifest reference §11, §12, or §13?
grep -n "section.*11\|section.*12\|section.*13" "paper/CEA Paper/manifest.yaml"

# 3. Does E30 appear in §9 (should NOT after fix)?
grep -n "E30\|e30" manuscript/sections/09_results_selective_reliability.tex
```
Check 1: paste new counts. Check 2: must return zero. Check 3: must return zero.

REPORT FORMAT:
```
## TASK T0-8 REPORT
**Files modified:** [list]
**manifest.yaml new counts:** [paste Check 1 output]
**§11/12/13 refs in manifest:** [paste Check 2 output — must be empty]
**E30 in §9:** [paste Check 3 output — must be empty]
**Result:** PASS / FAIL
**Observations outside scope:** [list]
```

---

## END OF PHASE 0

After T0-8 is approved, the manuscript is clean of fabricated claims.
Paper is submittable in this state as a narrower verification-architecture contribution.

Proceed to `03_PHASE1_REFRAMING.md` when author approves.


---

## END OF PHASE 0

After T0-8 is approved by the author, the paper is in this state:
- Honest: no fabricated claims remain
- Narrower: ~1/3 of content removed
- **Submittable as a narrower verification-architecture paper**

Proceed to `03_PHASE1_REFRAMING.md`.
