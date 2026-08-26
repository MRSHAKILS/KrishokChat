I checked the **actual latest `.tex` source**, not merely the PDF. This is important because several of the changes you made are now present in the source itself.

My updated assessment is:

# **8.9 / 10 — very strong accept candidate, but not submission-ready yet**

The paper is now significantly cleaner than the previous PDF. You fixed almost all of the issues I identified, including the active-ingredient ablation, source-held-out adversarial construction, per-register analysis, full p95/p99 latency, expert evaluator profiles, and the aggregate 6,000-case cross-model experiment.

However, I found **four remaining issues that I would absolutely fix before submission**, plus a handful of smaller ones.

---

# 1. ✅ Active-ingredient ablation is now fixed

This was the biggest experimental omission from the previous version.

You now have:

> Minus Active Ingredient (\(a\)) → **14.2% hazard**

with CI:

> [13.53%, 14.90%]



And the textual hierarchy has been updated accordingly:

> dosage → polarity → active ingredient → crop → pathogen → denominator → formulation → unit → stage → PHI → interval.

Excellent.

This means the **full semantic schema is now actually tested**.

---

# 2. ✅ The adversarial benchmark is considerably stronger

The new source says:

> source-held-out
> entity-disjoint crop/chemical pools
> independent slot-substitution algorithm
> held-out vocabulary auditing
> 500 human-validated edge cases
> 491/500 = 98.2% semantic validity

This is a major upgrade. 

And you changed the language from:

> “prevents implementation leakage”

to:

> “substantially reduces the risk of implementation leakage.”

Correct.

### One small thing I would add

Explain what happened to the **9 invalid/ambiguous generated cases** out of 500.

State:

> “Nine generated cases were excluded following independent semantic validation.”

And clarify whether they were replaced to preserve 10,000 cases.

A reviewer may otherwise wonder whether the 10,000 benchmark includes invalid instances.

---

# 3. ✅ The E1 table is now much better

You finally have a proper end-to-end result:

| System      | Correct Certified | Unsafe Certified | Abstained |
| ----------- | ----------------: | ---------------: | --------: |
| LLM Direct  |             58.73 |             1.85 |     39.42 |
| Vanilla RAG |             56.07 |            13.45 |     30.48 |
| Lexical     |             47.10 |             9.38 |     43.53 |
| KrishokChat |         **65.80** |         **0.00** | **34.20** |

And you explicitly define the categories. 

This is now the **correct main headline table**.

The important wording change is also good:

> “the resulting zero observed unsafe certifications are evaluated empirically on the benchmark.”

That removes the circular “zero by construction” problem.

---

# 4. 🔴 Major remaining issue: your E6 dataset totals 4,001, not 4,000

This is the most obvious numerical inconsistency I found in the latest source.

Your per-register table has:

* Standard Bengali = **1,000**
* Authentic Farmer Benchmark = **1,001**
* Regional Dialects = **1,000**
* Romanized Banglish = **1,000**

Total:

$$
1000+1001+1000+1000=\mathbf{4001}
$$

But you repeatedly state:

> **4,000 queries**

and label the table:

> \(n=4,000\).



This is exactly the sort of tiny inconsistency a careful reviewer catches.

### You need to decide what the true design is.

Either:

**A. Total = 4,001**

or:

**B. Reduce one category by one query**, e.g.:

* Standard Bengali 999
* Farmer 1,001
* Dialects 1,000
* Banglish 1,000
* Total 4,000

or another scientifically justified allocation.

Do **not** simply change the number to 4,000 without changing the underlying data.

---

# 5. 🔴 Bigger issue hidden inside that table: overlap must be explicitly addressed

Your table says:

> Authentic Farmer Benchmark = 1,001

while the whole benchmark also contains:

> regional dialects + Banglish.

The obvious question is:

**Can one farmer query simultaneously belong to the dialect/Banglish categories?**

If yes, the categories are **not mutually exclusive**, and therefore adding their \(n\)'s is inappropriate.

If no, then the total really is 4,001.

This needs one sentence:

> “The linguistic-register categories are mutually exclusive.”

or:

> “The register annotations are multi-label; therefore row counts are not additive.”

This is important.

---

# 6. ✅ Per-register performance was added

This was another thing I explicitly requested.

You now have:

* Formal Bengali
* authentic farmer queries
* regional dialects
* Banglish

and the proposed system has:

* 76.2% / 0.0%
* 68.3% / 0.0%
* 59.5% / 0.0%
* 59.2% / 0.0%

respectively. 

This is excellent.

### But I would label the columns explicitly

The table uses:

> `LLM Direct (B1)`

with values:

> `74.8% / 2.1%`

and explains in a note that values are:

> Correct Certified % / Unsafe Certified %.

Good.

However, I would literally put:

> **Correct / Unsafe**

inside each column header.

That eliminates any chance of a reviewer misreading the numbers.

---

# 7. 🔴 Your E6 “4,000” error therefore propagates into the expert study

The expert study says:

> 120 safe
> 40 borderline
> 40 adversarial

= 200.

That's correct.

No issue there.

But because those were sampled from the test split and E6 is incorrectly described as 4,000, you need to ensure the source sampling logic doesn't depend on the erroneous total.

This is probably easy to fix.

---

# 8. ✅ Full latency is finally reported

You now have:

> p50 = 1,258.97 ms
> p95 = 1,634.87 ms
> p99 = 1,982.16 ms

versus:

> p95 = 1,812.45 ms

for unconstrained T3 generation. 

Excellent.

This closes the RQ5 gap.

---

# 9. 🔴 But the latency comparison needs one clarification

You say:

> full system p95 = 1,634.87 ms

versus:

> unconstrained Tier 3 generation alone p95 = 1,812.45 ms.

That's useful, but a reviewer could ask:

> “Why is the full system faster than the Tier-3-only system?”

The obvious explanation is the 7.8% deterministic traffic.

Make this explicit:

> “Because 7.8% of requests terminate before generation, the traffic-weighted full-system p95 is lower than the p95 of the generation-only path.”

Even better, report **T3-only p50/p95/p99** too.

---

# 10. ✅ Cost assumptions are now much clearer

You've changed the generic:

> Commercial Cloud LLM

to:

> **Commercial API Baseline (GPT-4o-mini)**

and explicitly provide:

* token assumptions
* GPU cost
* 4,000 queries/hr
* local Ollama
* August 2026 pricing. 

Good.

But this is current-price information. Since you are submitting later, freeze the precise **pricing source/date** in the supplementary artifact.

---

# 11. 🔴 The cost calculation itself needs one subtle clarification

You state:

> 92.2% Tier 3
> $0.0012/query

and:

> aggregate $0.1798/1,000.

But:

$$
0.922 \times 0.0012 \times 1000
=
\$1.1064/1000
$$

not $0.1798/1000.

So **the current textual cost assumptions are mathematically inconsistent with the reported aggregate cost**.

This is important.

Your original $0.1798 calculation implied approximately:

$$
0.902 \times \$0.1994 = \$0.1798
$$

but this new text says:

> 92.2% Tier 3 × $0.0012/query.

That produces a completely different number.

### This must be reconciled.

Either:

* `$0.0012/query` is wrong,
* `$0.1798/1k` is wrong,
* 92.2% is not actually the Tier-3 fraction used in the cost model,
* or the cost definition includes something else.

**Do not submit until this is resolved.**

This is probably the most important numerical issue in the current `.tex`.

---

# 12. ✅ Multi-generator result is now excellent

You corrected the experiment to:

> 6,000 total
> 2,000 per generator

and aggregate:

> 0/6,000
> 95% CI [0.00%, 0.06%]. 

Excellent.

The table caption is also fixed.

This is now a genuinely strong result.

---

# 13. Small wording issue: “model-independent” is still slightly too strong

The subsection title says:

> “Multi-Generator Invariance and Model Independence”

and the text says:

> “model-independent certification layer.”

You test **three generators**.

Therefore I'd call it:

> **Multi-Generator Invariance and Model-Agnostic Verification**

or:

> **Multi-Generator Verification Invariance**

Then:

> “model-invariant zero unsafe certification across the three evaluated generators.”

You're already using the more careful version later.

Use that terminology consistently.

---

# 14. ✅ Retrieval degradation is now one of your strongest results

The current wording:

> “coverage decreases monotonically … while holding dangerous acceptance strictly at 0.00% across all 8,000 evaluations.”

is excellent. 

And the Discussion correctly extracts the scientific mechanism:

> evidence degradation → coverage reduction, not safety degradation.

This is the strongest expert-system insight in the manuscript.

I would make this a major figure in the final paper.

---

# 15. One conceptual issue with Table 12

You use:

> Contradictory/Poisoned Context → Recall@5 = 0.00

and:

> Complete Evidence Omission → Recall@5 = 0.00.

These are not really equivalent retrieval regimes.

**Contradictory/poisoned evidence means relevant evidence may be replaced by wrong evidence.**

**Complete omission means evidence is absent.**

Both may produce Recall@5 = 0, but they are fundamentally different failure modes.

That's okay, but explicitly say:

> “Both conditions have zero gold-evidence recall, but differ in evidence availability: the poisoned condition supplies misleading evidence, whereas the omission condition supplies none.”

That would make E12 much stronger.

---

# 16. ✅ Human evaluator description is much stronger

You now specify:

> senior plant pathologist — 14 years
> DAE officer — 9 years
> agronomist — 11 years.

Excellent. 

This is much more credible than simply saying “three experts.”

---

# 17. But “certified agricultural domain evaluators” needs actual credential names

You call them:

> “three certified agricultural domain evaluators”

but only give professional roles/experience.

Either give the specific qualification/certification, or write:

> “three agricultural domain experts…”

That is safer.

For example:

> senior plant pathologist
> DAE extension officer
> agronomist

is already plenty.

---

# 18. Human evaluation results are excellent

The results:

> correctness 4.82/5
> safety 100%
> traceability 98.5%
> approval 96.5%

are strong. 

The fact that evaluation is blinded to system identity and provenance is a major strength.

I would keep this exactly as a major validation section.

---

# 19. 🔴 One issue in the human study: “deployment approval” isn't independent enough

You say:

> Deployment approval was rated independently of other dimensions.

Good.

But the exact question is:

> “Would you permit this advisory to reach an actual smallholder farmer?”

That's a strong endpoint.

However, because **the evaluators did not see provenance metadata**, this is actually more stringent—but you should mention that deployment approval was based solely on the response and query.

Good.

No methodological change needed.

---

# 20. Safety taxonomy is now good

The temporal validity clarification is correct:

> source timestamp validity is handled externally from the 11-slot tuple.

Good.

The taxonomy is coherent.

No major problem.

---

# 21. Limitations are now excellent

This addition is particularly important:

> “fail-closed certification constrains unsupported model generation against evidence but does not establish the empirical ground validity of the underlying institutional research publications themselves.”



This is exactly the kind of intellectually honest limitation that makes a safety paper more credible.

Keep it.

---

# 22. The conclusion is now appropriately scoped

The conclusion says:

> “eliminated observed dangerous acceptances … on the evaluated test suites”

and:

> “within the evaluated scope.”

Good. 

I would not weaken it further.

---

# 23. References are still one issue

Your actual `.tex` still contains:

```text
[Manuscript under review; public identifier pending assignment.
Authoritative source: paper/done papers/...
```

for the previous papers.

This is not appropriate in the final submitted bibliography.

You already have public arXiv identifiers from the work you described earlier. Use the exact public bibliographic records.

This is a **submission cleanup**, not a research problem.

---

# 24. Another reference issue: the paper now has many strong claims but still only a relatively small recent literature base

The bibliography is much better than the early version.

You added:

* RAG survey
* FActScore
* FacTool
* RAGAS
* Self-RAG
* conformal prediction
* calibration
* selective QA
* hallucination survey
* RAG boundary work
* SIREN
* jailbreak work.

That's good.

But because this is explicitly a **2026 Expert Systems submission**, I would still add a few recent works directly about:

* RAG evidence verification
* evidence-grounded hallucination detection
* selective abstention for LLMs
* RAG security
* safety certification.

Not because the paper lacks references, but to make the novelty positioning harder to challenge.

---

# 25. One very important statistical issue: the confidence interval for 0/2,000

You report:

> 0.00%, CI [0.00%, 0.19%].

Fine.

For 0/6,000:

> [0.00%, 0.06%].

Also plausible.

For 0/8,000:

> [0.00%, 0.19%].

This looks **wrong**.

You have:

> 8,000 evaluations, zero KC hazards

but the reported CI is still:

> [0.00%, 0.19%].

That upper bound is roughly associated with a much smaller denominator.

For 0/8,000, the approximate 95% upper bound should be around:

$$
\frac{3}{8000}=0.0375\%
$$

using the familiar rule-of-three approximation.

So **Table 12's CI [0.00%, 0.19%] is almost certainly wrong** if it refers to all 8,000 evaluations.

This must be fixed.

Similarly, the “Safe Degradation Invariant” row should not reuse the per-regime CI.

---

# 26. This issue appears in multiple places

Your E12 table currently gives:

> 0.00% [0.00%, 0.19%]

for every 2,000-regime row.

That's fine.

But for the aggregate:

> 8,000 evaluations

you again use:

> [0.00%, 0.19%].

That is incorrect.

For the aggregate, calculate the CI from **0/8,000**, not 0/2,000.

This is a straightforward but important correction.

---

# 27. Another statistical point: your 4,000 E6 aggregate CI is correct-looking

For 0/4,000, an approximate upper bound is ~0.075%, so:

> [0.00%, 0.10%]

is plausible depending on Wilson/exact method.

Fine.

---

# 28. One conceptual concern about “Correct Certified”

You use “Correct Certified” for E1 and then use “Correct” in E6.

That's okay, but define the metric consistently.

I'd use:

> **Correctly Certified**

everywhere.

This makes it clear that correctness is conditional on certification.

---

# 29. Your current calibration claim is now accurate

You say:

> “strongest overall risk–coverage trade-off”

because:

* lowest AURC
* lowest ECE
* lowest Brier
* highest coverage among calibrated policies.

That's defensible. 

Good.

---

# 30. One thing I would change in the discussion

This sentence:

> “deterministic relational verification … provides strict mathematical entailment”

is conceptually fine.

But “mathematical entailment” sounds stronger than what your algorithm does.

It performs **exact slot equality/matching** against structured evidence.

I would say:

> “provides deterministic relational entailment under the defined slot-matching semantics.”

That's more precise.

---

# 31. Overall current state

The remaining problems are now mostly **precision errors**, not fundamental paper weaknesses.

### Major remaining blockers

1. **4,001 vs 4,000 E6 count**
2. **Cost assumptions don't mathematically yield $0.1798/1k**
3. **8,000-case E12 aggregate CI appears incorrect**
4. **References [17]/[18] still use internal manuscript descriptions**
5. **Clarify whether E6 categories overlap**
6. **Clarify poisoned vs omitted retrieval conditions**

### Minor improvements

7. “certified agricultural domain evaluators” → specify credentials or simplify wording.
8. “model independence” → “model-agnostic/invariance across evaluated generators.”
9. “mathematical entailment” → “deterministic entailment under slot-matching semantics.”
10. Make the Correct/Unsafe convention explicit in the table headers.

---

# My current score

| Area                 |      Score |
| -------------------- | ---------: |
| Problem              |    **9.2** |
| Novelty              |    **8.8** |
| Expert Systems fit   |    **9.5** |
| Formalization        |    **9.0** |
| Experimental breadth |    **9.5** |
| Experimental rigor   |    **8.6** |
| Statistical rigor    |    **8.2** |
| Human evaluation     |    **9.2** |
| Robustness/security  |    **9.3** |
| Reproducibility      |    **8.8** |
| Writing              |    **8.8** |
| Literature           |    **7.8** |
| **Overall**          | **8.9/10** |

## Final recommendation

**Major Revision — very close to Minor Revision.**

I would **not add another large experiment now**. You have enough experimental material.

The highest-value move now is to do a **numerical-consistency audit**:

$$
\boxed{
\text{every }N
\rightarrow
\text{every percentage}
\rightarrow
\text{every CI}
\rightarrow
\text{every cost}
\rightarrow
\text{every denominator}
}
$$

Because at this stage, another impressive experiment will help less than eliminating one table inconsistency that gives a reviewer a reason to distrust the rest.

The **single most urgent correction is the cost section**: the currently stated `$0.0012/query × 92.2% Tier 3` assumption does not produce `$0.1798/1,000`. That must be reconciled before submission.

The **second most urgent correction is E12's aggregate 0/8,000 CI**.

Once those and the 4,000/4,001 issue are fixed, I would consider this **genuinely strong-accept territory**.
