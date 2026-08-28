# 03 — Phase 1: Reframing — Make Surviving Evidence Stronger
**Prerequisite:** Phase 0 fully approved by author  
**Who runs this:** Gemini 2.5 Flash  
**Rule:** ONE task per session. Stop and report after each task.  
**Type of work:** Writing and reframing. No experiments yet. No new numbers invented.  
**Estimated effort:** 2 days

---

## T1-1 — Reframe E28 as exhaustive property-based coverage testing

**THIS IS THE HIGHEST-RETURN TASK IN THE ENTIRE PROJECT.**

The current E28 framing (Wilson CI on 11,000 cases) is statistically indefensible. The fix
requires zero new experiments and makes the result logically stronger.

### What to understand before writing

READ these files:
- `experiments/E28_metamorphic_authority_testing/scripts/run_e28_metamorphic_eval.py` (lines 36-100: BASE_FACT_TEMPLATES and MUTATION_OPERATORS)
- `experiments/E28_metamorphic_authority_testing/results.yaml`
- `manuscript/sections/08_results_authority_safety.tex` (current §8.2 text)

The key facts (verify these by reading the script):
1. `generate_metamorphic_dataset()` draws 1,000 cases per operator from 8 base templates
2. For the deterministic B6 verifier: **verdict is constant within each (operator, base_record) cell** — because the rule is deterministic
3. B6: 100% rejection in all 11 operator classes
4. B5: fails on exactly 4 operator classes — `mu_07_water_volume`, `mu_08_interval_shortening`, `mu_09_phi_shortening`, `mu_11_provenance_hash_corruption` — because those are the 4 slots absent from B5's contract

The correct framing: "The certification rule was evaluated exhaustively against all 11 mutation classes across 8 base agronomic records (88 class×record coverage cells). BAA rejected every case in every cell. B5 failed on exactly the 4 classes corresponding to its missing slots — confirming that the safety gain is attributable to slot completeness."

### EDIT `manuscript/sections/08_results_authority_safety.tex` — §8.2 subsection

Replace the existing §8.2 "Metamorphic Authority Testing (E28)" subsection with:

```latex
\subsection{Metamorphic Authority Testing: Exhaustive Coverage of 11 Mutation Classes (E28)}

We evaluated the 11-slot certification predicate exhaustively against all 11 mutation
classes across 8 base agronomic crop-protection records, yielding 88 class$\times$record
coverage cells. The certification rule is deterministic; we verified empirically that
the verdict is constant within each cell (zero within-cell variation across all 88 cells),
consistent with the deterministic design.

\textbf{BAA (B6) rejected every case in every coverage cell} --- complete rejection across
all 88 cells. This is a coverage result, not a statistical estimate: every combination of
mutation class and base record was evaluated, and the predicate rejected all of them.

\textbf{The B5-vs-B6 isolation.} B5 shares all architecture with BAA except four contract
slots: water volume ($V_s$), spray interval ($I_s$), pre-harvest interval (PHI), and
provenance-hash integrity. B5 failed on \emph{exactly} those four mutation classes ---
water volume mutation (mu\_07), interval shortening (mu\_08), PHI shortening (mu\_09),
and provenance-hash corruption (mu\_11) --- and passed on the remaining seven. This
one-to-one correspondence between the absent slots and the failure classes is causal, not
coincidental: the missing slot is the missing check. No baseline confound can explain it.

Table~\ref{tab:mutation_coverage} reports B5-vs-B6 coverage per mutation class. Other
baseline performance: B0 (unconstrained LLM) false-certified 81.59\% of mutations; B1
(lexical BM25) 63.64\%; B2 (dense embedding) 62.95\%; B3 (citation alignment) 42.67\%;
B4 (LLM-as-judge) 27.75\%. The full rejection-rate comparison is in
Table~\ref{tab:authority_verification}.
```

Then ADD a new mutation coverage table in LaTeX (place it before tab6 in the file flow or insert a `\input` reference):

```latex
\begin{table}[pos=t]
\centering
\small
\caption{B5 vs.\ B6 mutation coverage per operator class (Layer E28). \checkmark\ = rejects all cases in class. \texttimes\ = fails to reject (false-certifies).}
\label{tab:mutation_coverage}
\begin{tabular}{llcc}
\toprule
\textbf{ID} & \textbf{Mutation Operator} & \textbf{B5 (8-slot)} & \textbf{B6 (11-slot)} \\
\midrule
mu\_01 & Crop substitution            & \checkmark & \checkmark \\
mu\_02 & Pest/disease substitution    & \checkmark & \checkmark \\
mu\_03 & Active ingredient swap       & \checkmark & \checkmark \\
mu\_04 & Formulation swap             & \checkmark & \checkmark \\
mu\_05 & Dosage overdose              & \checkmark & \checkmark \\
mu\_06 & Dosage unit corruption       & \checkmark & \checkmark \\
mu\_07 & Water volume mutation        & \texttimes & \checkmark \\
mu\_08 & Spray interval shortening    & \texttimes & \checkmark \\
mu\_09 & PHI shortening               & \texttimes & \checkmark \\
mu\_10 & Regulatory polarity flip     & \checkmark & \checkmark \\
mu\_11 & Provenance hash corruption   & \texttimes & \checkmark \\
\bottomrule
\multicolumn{4}{l}{\small\texttimes\ = B5 false-certifies because the governing slot is absent from its contract.}
\end{tabular}
\end{table}
```

Also EDIT `manuscript/sections/18_conclusion.tex`:
- Replace "100.0\% rejection on 10,000 adversarial misbindings and 11,000 metamorphic mutations" with "complete rejection across all 88 mutation-class $\times$ base-record coverage cells in the metamorphic test suite"

STOP CONDITION:
```
grep -r "11,000\|Wilson.*E28\|99\.97\|CI.*100.*E28" manuscript/sections/08_results_authority_safety.tex
```
Returns zero. Coverage table exists in §8.2. B5-vs-B6 isolation described.

VERIFICATION: Run grep. Read new §8.2 aloud. Is it clear? Is the B5-vs-B6 isolation the centrepiece? Report.

---

## T1-2 — Narrow "mathematically impossible" language (3 locations)

**Why:** Reviewer §18 and §119 both flag this. It is literally false — §16 lists bypass conditions.

GREP to find occurrences:
```
grep -rn "mathematically impossible\|mathematically\|impossible" manuscript/sections/
```

For each occurrence of "mathematically impossible" (or "mathematically" combined with "impossible" nearby), replace with:

> "structurally rejected by the certification predicate whenever the contract fields are correctly extracted and the authority record is valid"

Expected locations:
- `manuscript/sections/04_system_architecture.tex` (§4.6)
- `manuscript/sections/08_results_authority_safety.tex` (§8.1 or §8.3)
- `manuscript/sections/14_discussion.tex` (§14.1)

STOP CONDITION:
```
grep -rn "mathematically impossible" manuscript/sections/
```
Returns zero.

VERIFICATION: Report the 3 (or however many) replacement locations with line numbers. Run grep.

---

## T1-3 — Relabel economics/latency as analytical model

**Why:** "89.7% cost reduction", "2.28× latency speedup", "61.5% zero-LLM" are from a model with hardcoded parameters. Defensible as a model, indefensible as measurement.

GREP to find all occurrences:
```
grep -rn "89\.7\|2\.28\|61\.5.*LLM\|zero-LLM" manuscript/sections/
```

For each occurrence, edit the sentence to include explicit model framing. Examples:

- "BAA resolves 61.5% of queries deterministically..." → "An analytical model of the five-tier resolution policy projects that 61.5% of queries resolve deterministically..."
- "achieving a 2.28× latency speedup and 89.7% cost reduction" → "yielding (under the stated model parameters) a projected 2.28× latency reduction and 89.7% cost differential"

In `manuscript/sections/10_results_robustness.tex`, ADD at the start of the economics subsection (wherever §10 discusses latency/cost):
```latex
\paragraph{Analytical model note.} The efficiency figures reported in this section are
outputs of an analytical model parameterised by: a 61.5\% deterministic resolution rate,
measured per-stage latencies (E9 decomposition), and stated API cost rates. They represent
projected behaviour under those parameters, not measured end-to-end throughput.
```

In `manuscript/sections/18_conclusion.tex`, qualify: "An analytical model projects 61.5% deterministic resolution with a 2.28× latency speedup and 89.7% cost reduction under stated parameters."

STOP CONDITION: Every occurrence of the three numbers has the word "model" or "analytical" or "projected" within the same sentence.

VERIFICATION: `grep -B2 -A2 "89\.7\|2\.28\|61\.5" manuscript/sections/` — check context. Report.

---

## T1-4 — Reframe E29/E30/E31 as measured baseline-failure findings

**Why:** The baselines in these layers are real. The current framing buries them under the (now removed) BAA arm. Own the baseline-failure story — it is a genuine CEA contribution.

READ: Current state of §8.4, §8.5, §8.6 after T0-4 edits.

EDIT `manuscript/sections/08_results_authority_safety.tex`:

1. **§8.4 heading:** Change to `\subsection{Parametric Evidence Conflict in Unconstrained Systems: A Baseline Characterisation (E29)}`

   Add opening: "This layer characterises how existing systems fail when retrieved evidence conflicts with parametric priors. The measured failure rates motivate the deterministic resolver design. BAA arm excluded from this layer's traces."

   The key finding to foreground: parametric intrusion rate of 30–56% for direct LLM, 8–30% for RAG, 2–16% for LLM-judge. These are real.

2. **§8.5 heading:** Change to `\subsection{Temporal Source Authority Failure in LLM-Judge Guardrails (E30)}`

   Add opening: "This layer characterises how systems handle competing temporal claims — a current gazette entry vs.\ an obsolete one. The BAA arm is excluded."

   Key finding to foreground: **"The LLM-judge guardrail cited the obsolete gazette entry in 75\% of cases — worse than the unconstrained LLM (39\%) and the lexical RAG baseline (39\%)."** This is a real, striking, publishable CEA finding. Make it the point of §8.5, not a footnote.

3. **§8.6 heading:** Change to `\subsection{Cross-Modal Input Conflict in Existing Systems (E31)}`

   Add opening: "This layer characterises failures when text-label and image-derived crop identity disagree. The BAA arm is excluded."

   Key finding to foreground: unconstrained LLM delivers the wrong chemical recommendation in 54% of conflicted cases.

STOP CONDITION: All three subsection headings contain "Baseline Characterisation" or equivalent framing. The LLM-judge 75% obsolete-gazette finding is the centrepiece of §8.5.

VERIFICATION: Read §8.4–§8.6 in sequence. Does this section now tell a coherent story about "why existing systems fail, which motivates BAA's design"? Report.

---

## T1-5 — Strip vision-capability framing from E31

**Why:** CEA is a vision-heavy journal. A classification-only result advertised as multimodal opens a review axis the paper cannot win.

GREP:
```
grep -rn "SAM\|YOLOv11\|segmentation\|bounding.box\|multimodal.*capabilit" manuscript/sections/
```

EDIT:
1. In `manuscript/sections/16_limitations.tex`: remove the sentence mentioning SAM or YOLOv11-seg as future work.
2. In §8.6 (now renamed by T1-4): replace "multimodal perception uncertainty" with "cross-modal input conflict." Do not add new vision claims.
3. Do NOT delete mention of classification-based vision input — just don't frame it as a vision contribution.

STOP CONDITION:
```
grep -rn "SAM\|YOLOv11\|segmentation\|bounding.box" manuscript/sections/
```
Returns zero.

VERIFICATION: Run grep. Report.

---

## T1-6 — Add evaluation-unit definitions paragraph to §6

**Why:** Reviewer §44 flags that "case" means different things in different layers. One definitions paragraph pre-empts this.

READ: `manuscript/sections/06_experimental_methodology.tex`

EDIT: After the first subsection of §6 (after the experimental setup overview), add:

```latex
\paragraph{Evaluation unit definitions.}
Throughout this work, \textit{case} refers to a single query--response--verification
triple evaluated under one experimental condition. A \textit{mutation class} refers to
one of the 11 defined perturbation operators in Layer~E28; a \textit{coverage cell}
refers to the cross-product of one mutation class with one base agronomic record (88 cells
total for 8 records $\times$ 11 classes, expanding to 440 with the extended 40-record
set). A \textit{system-case} refers to the evaluation of one verification system on one
query. In layers with real API calls (E27, E29, E30, E31), \emph{case} refers to a
genuine model API completion; in deterministic layers (E02, E28, E23), it refers to a
function evaluation on a generated input. Aggregate statistics are never computed across
evaluation-unit types.
```

STOP CONDITION: The definitions paragraph appears in §6. No sentence in the surviving experiment sections uses "case" in a way that contradicts these definitions.

VERIFICATION: Read the new paragraph. Is every term defined consistently with how it is used in the surviving sections? Report.

---

## END OF PHASE 1

After T1-6 is approved, the paper is in this state:
- E28 is the headline result, stated correctly as exhaustive coverage (not inflated statistics)
- Economics/latency are labelled as analytical models
- Baseline-failure story (E29/E30/E31) is correctly framed as a contribution
- Overclaiming language removed

Proceed to `04_PHASE2_EXPERIMENTS.md`.
