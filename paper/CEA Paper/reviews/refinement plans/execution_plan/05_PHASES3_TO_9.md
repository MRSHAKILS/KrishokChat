# 05 — Phase 3: Manuscript Reconstruction
**Prerequisite:** Phase 2 fully approved  
**Rule:** ONE task per session. Abstract is ALWAYS the last task.

---

## T3-1 — Rewrite §8 opening to match surviving evidence

READ: Current `manuscript/sections/08_results_authority_safety.tex` lines 1-12 (after Phase 0 edits removed the E32/E33 paragraph)

REPLACE the opening paragraph with:

```latex
The certification predicate rejected every case in the metamorphic authority test suite:
complete rejection across all [N] mutation-class $\times$ base-record coverage cells in
Layer~E28, where [N] = [real count from results_slot_ablation.yaml: total_base_records × 11].
The B5-vs-B6 isolation result (Table~\ref{tab:mutation_coverage}) confirms that the safety
gain is attributable to slot completeness: B5 fails on exactly the four mutation classes
whose governing slots are absent from its contract, and passes on all seven others.
Supporting evidence: Layer~E02 evaluated the relational misbinding suite [N cases if known]
and found 100.0\% rejection; this layer's external dataset cannot be reproduced from this
artifact alone (dataset path outside submission bundle), but the result is consistent with
the E28 isolation finding. This section traces the structural mechanism.
```

STOP CONDITION: The opening no longer claims Wilson CI numbers or references "10,000" or "11,000" cases as independent.

VERIFICATION: Read opening. Is it accurate? Report.

---

## T3-2 — Rewrite §7 (Advisory Quality) opening

READ: Current `manuscript/sections/07_results_advisory_quality.tex` after Phase 0 edits.

CHECK which branches were executed:
- Did T0-1 delete E13? → `grep -c "agronomist\|E13\|Gwet" manuscript/sections/07_results_advisory_quality.tex`
- Did T0-2 delete E27 B6? → `grep -c "97\.0\|B6.*CAC" manuscript/sections/07_results_advisory_quality.tex`

SCENARIO A (both deleted): Replace §7 opening with:
```latex
\section{Results: Live-API Baseline Characterisation (RQ1)}
\label{sec:results_advisory_quality}

This section reports the performance of existing baseline systems on naturalistic and
adversarial farmer queries (Layer~E27), establishing the failure rates that motivate
the bounded-authority design. BAA certified advisory correctness is reported in
Section~\ref{sec:results_authority_safety} through the metamorphic coverage evaluation.
```

Keep the baseline table (B0, B1, B4) with their real numbers. Keep §7.3 if it contains multi-register baseline data. Remove the §7 subsections for E27 B6 and E13 (already done in Phase 0).

SCENARIO B (E13 documented, E27 B6 pending): Keep the structure but mark E27 B6 as pending and ensure E13 uses real data.

STOP CONDITION: §7 opening no longer makes claims that lack evidence. Reads as either "baseline characterisation" or "pending" story.

VERIFICATION: Read §7 from the top. Report the scenario applied.

---

## T3-3 — Rewrite abstract and conclusion (DO THIS LAST)

**CRITICAL: Do not do this task until T3-1 and T3-2 are approved.**  
**Do not do this task until all Phase 0, 1, 2 tasks are approved.**  
**This is always the last writing task.**

READ the full current state of ALL manuscript sections before writing.

### For the abstract

The abstract must contain ONLY numbers that can be traced to a real experiment YAML. Use this template — fill in ONLY the bracketed items from real data:

```
Pesticide recommendations are safety-critical: a single misbinding between a valid active
ingredient and an incorrect dosage or pre-harvest interval can cause poisoning or
environmental harm. We present the Bounded-Authority Advisory Architecture (BAA), which
separates factual authority from generative language through an 11-slot, single-record,
fail-closed certification contract. A claim is certified only when all 11 contract fields
are jointly satisfied by one accredited evidence record; failure triggers deterministic
abstention or escalation.

We evaluate the certification contract exhaustively across all 11 mutation classes and
[TOTAL_BASE_RECORDS] base agronomic records ([TOTAL_CELLS] coverage cells). The
certification predicate rejected every case in every cell. B5, a partial 8-slot contract,
failed on exactly the four missing-slot classes — confirming that the safety gain is
attributable to slot completeness. A real slot ablation ([replace with top 2 real numbers
from results_slot_ablation.yaml]) and a benign-mutation control (false-rejection rate
[real value from results_benign_control.yaml]%) confirm that the predicate is both
necessary and discriminating.

On real live-API baselines, unconstrained LLMs accepted unsafe recommendations in 8.0%
of cases; LLM-judge guardrails in 15.0% — worse than the unguarded baseline. Under
temporal conflict, LLM-judge guardrails cited obsolete gazette entries in 75% of cases.
These findings motivate the deterministic authority enforcement design.

[INCLUDE ONLY IF X2 WAS COMPLETED: "On a controlled [N]-case end-to-end benchmark,
BAA achieved [real CAC]% certified advisory correctness with [real CUAR]% critical
unsafe acceptance."]

[INCLUDE ONLY IF E13 PROPERLY DOCUMENTED: "Three certified agronomists rated BAA
[real score]/5 (Gwet's AC1=[real AC1] on safety), with [real pct]% deployment approval."]

The architecture is evaluated on a crop-protection corpus from BARI, BRRI, and DAE/MoA.
The E28 evaluation harness is released with the paper.
```

### For the conclusion

Replace `manuscript/sections/18_conclusion.tex` entirely with:

```latex
\section{Conclusion}
\label{sec:conclusion}

We presented the Bounded-Authority Advisory Architecture (BAA), a decision-support
framework that separates factual authority from generative language in agricultural AI.
An 11-slot, single-record, fail-closed certification contract prevents large language
models from inventing, mutating, or misbinding safety-critical chemical dosages,
pre-harvest intervals, and application guidelines.

The architecture's central safety property was evaluated exhaustively: all 11 mutation
classes across [TOTAL_BASE_RECORDS] base agronomic records ([TOTAL_CELLS] coverage
cells) were evaluated against the certification predicate, which rejected every case.
The B5-vs-B6 isolation identifies slot completeness as the causal mechanism. A slot
ablation confirms that [REAL TOP FINDING — e.g., "dosage-bound enforcement carries
the largest individual contribution, [X] pp false-certification increase when
disabled"]. A benign-mutation control confirms the predicate discriminates: [FRR]%
false-rejection rate on semantically neutral transformations.

Measurement of existing baseline systems demonstrates the problem the architecture
addresses: unconstrained LLMs accept unsafe recommendations in 8.0\% of live-API
cases; LLM-judge guardrails perform worse under temporal conflict (75\% obsolete-gazette
citation), not better. [ADD real E27 B6 / E13 sentences IF those experiments were
completed.] The fail-closed design trades coverage for safety: [benign FRR]\%
of valid queries are conservatively abstained, a cost we report as a design parameter
rather than a limitation to minimise.

Future work will extend this framework to field trials evaluating real crop yield
preservation and applicator safety in partnership with national extension services.
```

Fill ALL brackets from real YAML files. No invented numbers.

STOP CONDITION: Every number in abstract and conclusion has a source YAML. Build this table before stopping:

| Number | Claim | Source YAML file | Key path |
|---|---|---|---|
| [list every number] | [what it claims] | [filename] | [yaml key] |

VERIFICATION: Paste the provenance table. If any number has no source, it must be removed. Report.

---

## END OF PHASE 3

After T3-3 approved: the manuscript is honest, narrow, and consistent.

If Q2=YES (runnable system): proceed to `06_PHASE4_CONDITIONAL.md`.  
Otherwise: proceed to `07_PHASE5_SUBMISSION_GATE.md`.


---

# 06 — Phase 4: Conditional Experiments (if system exists)
**Only execute if author confirmed Q2=YES**

---

## T4-1 — End-to-end benchmark n=300 (Task X2)

DESIGN — do not deviate without author approval:
- n = 300 total queries: 210 naturalistic (stratified across 4 Bengali registers) + 90 adversarial
- Arms: A0 (direct LLM), A1 (vanilla RAG), A2 (RAG+LLM-judge), A3 (evidence-constrained RAG without single-record binding), A4 (BAA)
- Same frozen query set and corpus for all arms
- Metrics: CUAR, CAC-over-certified, coverage, appropriate abstention, FALSE abstention rate, per-slot violation count
- One run. Do not re-run if BAA CUAR is non-zero.

**Chain-breaker:** If BAA CUAR is 3% at n=300: report 3%. Do NOT run at n=500 to find a threshold that gives 0%. The architecture's value is low CUAR, not exactly-zero CUAR.

STOP CONDITION: n=300 run once for all arms. Results YAML saved. False abstention rate reported.

---

## T4-2 — Register Hit@1 (Task M4)

DESIGN:
- Use existing retrieval index from `backend/ml_assets/rag_index/`
- 200 queries: 50 × standard formal Bengali, 50 × authentic farmer dialect, 50 × regional dialect, 50 × romanized Banglish
- Metric: Hit@1 per register at default threshold
- Stop when: single measurement exists. Do not tune retrieval.

STOP CONDITION: Hit@1 per register measured once and reported.


---

# 07 — Phase 5: Submission Gate
**Final verification. Do not add new work here.**

---

## T5-1 — Final grep verification pass

Run each grep. ALL "must be gone" greps return ZERO. ALL "must exist" greps return at least one hit.

### Must be gone:
```powershell
# Run from D:\KrishokTech Advisory System\paper\CEA Paper\
grep -r "97\.0.*CAC\|97\.0.*certified.*correctness" manuscript/sections/  # unless from real X2
grep -r "4\.82\|Gwet.*0\.862\|AC1.*0\.862" manuscript/sections/           # unless from real E13
grep -r "60,000\|60000\|36 experimental\|36 layers" manuscript/sections/
grep -r "mathematically impossible" manuscript/sections/
grep -r "E32\|E33\|E34\|E35\|E36\|E37\|E38\|E39" manuscript/sections/
grep -r "predicate bypass\|deliberate bypass" manuscript/sections/
grep -r "37,000.*hazard\|national.*37" manuscript/sections/
grep -r "SAM\|YOLOv11-seg\|segmentation" manuscript/sections/
grep -r "11,000.*metamorphic\|Wilson.*E28" manuscript/sections/
```

### Must still exist:
```powershell
grep -r "B5.*exactly.*four\|four.*missing.*slot" manuscript/sections/     # isolation result
grep -r "75.*obsolete\|obsolete.*75" manuscript/sections/                  # E30 baseline finding
grep -r "15\.0.*CUAR\|B4.*15" manuscript/sections/                        # E27 B4 baseline
grep -r "analytical model\|stated parameters" manuscript/sections/         # economics model labelling
```

STOP CONDITION: All "must be gone" return zero. All "must exist" return at least one hit.

---

## T5-2 — Number provenance table

For every number in the abstract and conclusion, complete this table:

| Number | Claim | Source file | YAML key |
|---|---|---|---|
| [every number] | [its claim] | [exact filename] | [exact YAML key path] |

Any number with no source = remove it or mark `[NEEDS EVIDENCE]`.

---

## T5-3 — Final manifest and consistency check

- `manifest.yaml` sections list matches files actually in `manuscript/sections/`
- No reference to §11, §12, §13
- `experiments/results.yaml` entries for removed layers are marked `status: withdrawn`
- `\ref{}` and `\label{}` cross-references all resolve (no dangling §11–13 refs)
- Figures 3, 4, 5 captions match surviving results (Fig 5 caption should reflect real ablation numbers)

STOP CONDITION: All items confirmed. Report any inconsistencies found.

---

# 08 — Quarantine List
**Do NOT delete these files. Add a withdrawal header to each results YAML.**

For each file below, add these lines to the TOP of the results YAML:

```yaml
# ============================================================
# WITHDRAWN: This result file contains fabricated data.
# Reason: [see reason below]
# Date withdrawn: 2026-08-28
# Do not cite any number from this file in any publication.
# See: paper/CEA Paper/reviews/refinement plans/POST_EXPERIMENT_AUDIT.md
# ============================================================
```

Files to quarantine:

| File | Reason |
|---|---|
| `experiments/E13_human_expert_validation/results.yaml` | Python literals, evaluation_duration=0.0, no rater data |
| `experiments/E27_independent_expert_benchmark/results.yaml` | B6 row verdict was hardcoded; zero B6 traces |
| `experiments/E03_slot_ablation/results.yaml` | Entire file — hardcoded constant table |
| `experiments/E32_oracle_vs_predicted_routing/results.yaml` | BAA arm is prompted Gemini-Flash |
| `experiments/E33_high_confidence_wrong_routing/results.yaml` | BAA arm is prompted Gemini-Flash |
| `experiments/E35_linguistic_query_normalization/results.yaml` | BAA arm is prompted Gemini-Flash |
| `experiments/E36_source_fragmentation_assembly/results.yaml` | BAA arm is prompted Gemini-Flash |
| `experiments/E37_conversational_clarification_policy/results.yaml` | BAA arm is prompted Gemini-Flash |
| `experiments/E38_simulated_human_escalation_queue/results.yaml` | BAA arm is prompted Gemini-Flash |
| `experiments/E39_ipm_non_chemical_balance/results.yaml` | BAA arm is prompted Gemini-Flash |

---

# 09 — Files to Keep Unchanged
**These files are real. Do NOT modify them unless a task explicitly directs you to.**

```
experiments/E28_metamorphic_authority_testing/scripts/run_e28_metamorphic_eval.py
  (only ADD to this file in Phase 2 tasks — never remove existing code)

experiments/E27_independent_expert_benchmark/real_traces_100.jsonl
  (300 real API traces for B0, B1, B4 — never touch)

experiments/E27_independent_expert_benchmark/real_results_100.yaml
  (B0/B1/B4 real results — never touch)

experiments/E23_cache_invalidation_provenance/  (entire folder)
experiments/E25_intent_classifier_training/     (entire folder)
experiments/E19_knowledge_graph_traversal/      (entire folder)
experiments/E14_network_degradation/            (entire folder)

experiments/E29_parametric_evidence_conflict/real_traces_*   (baseline traces only)
experiments/E30_temporal_source_authority_conflict/real_traces_*
experiments/E31_multimodal_perception_uncertainty/real_traces_*

manuscript/tables/tab4_baseline_taxonomies.tex  (describes baselines — likely still accurate)
manuscript/tables/tab6_authority_verification.tex  (B6 100% rejection — from real E28 — keep)
manuscript/krishoktech_cea.bib                  (bibliography — only add, never remove)
```
