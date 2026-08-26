I read the **full 19-page version line-by-line**, including all 13 evaluation layers, every table, algorithm, definitions, discussion, limitations, and all references. This is the first version where I would say the manuscript is genuinely close to a submission-quality *Expert Systems* paper.

My assessment has improved, but there are still several things I would fix before submission.

## Updated verdict

**Score: 8.6/10**

**Current recommendation: Major Revision**

**After the remaining corrections: ~9.0–9.2/10**

The revision is materially better than the previous version. In particular, you corrected several issues I previously identified:

* E1–E13 is now explicit.
* The missing E1 experiment is now present.
* The 11-slot definition is clarified.
* The source-held-out adversarial benchmark is now described.
* The CI for CBC is correctly labeled.
* ASR/UCR are formally defined.
* The multi-generator aggregate is now explicitly **0/6,000**, with an aggregate CI.
* The 2,135 items are correctly called production-active nodes.
* Temporal validity is explicitly separated into the provenance-policy layer.
* The human expert sampling protocol is much more rigorous.
* The calibration-vs-hard-gate distinction is now clearly explained.

Those are meaningful improvements.  

---

# 1. The paper is now scientifically coherent

The central architecture is now very clear:

$$
\text{Query}
\rightarrow
\text{Safety Guard}
\rightarrow
\text{Deterministic Facts}
\rightarrow
\text{RAG}
\rightarrow
\text{Hard Relational Gate}
\rightarrow
\text{Calibration}
\rightarrow
\text{CERTIFY/ABSTAIN/ESCALATE}
$$

The distinction between the **hard binary entailment gate** and the **soft operational confidence score** is particularly important. You now explicitly explain that calibration does not replace logical verification; it operates only after the hard relational gate succeeds. 

That was one of the biggest conceptual weaknesses in the previous version, and you have now fixed it properly.

---

# 2. The abstract is now very good

The abstract is probably around **8.8–9.0/10**.

Especially good:

> “0.0% dangerous acceptance on a 10,000-case adversarial misbinding suite”

and

> “84.56% coverage at 1.26% selective risk”

and

> “0.0% risk at ≤80% coverage”

and the new wording:

> “100.0% top-1 consistency with full-precision reference outputs (engineering validation).”

The last phrase is a very good correction because you no longer imply that ONNX/PyTorch agreement equals classifier accuracy. 

### One remaining problem

The abstract says:

> “Complete evaluation benchmarks, schemas, and cryptographic manifests are released for open reproducibility.”

Your references later say the prior papers may still have public identifiers pending assignment, and the current paper references local repository paths. 

Before submission, make sure the **current paper's actual artifact repository is publicly accessible**. Otherwise say:

> “are prepared for release”

or provide the actual DOI/GitHub/Hugging Face/repository URL.

Don't make a release claim that isn't already verifiable.

---

# 3. Figure 1 is now fixed

You added:

> “The four architectural stages correspond to the five operational tiers, with Tier 1 and Tier 2 jointly implemented within Stage 2.”

Excellent. 

That completely resolves the previous Stage/Tier ambiguity.

---

# 4. Your Introduction is now much stronger

The opening now has proper citations:

* 16 million households
* extension ratio
* safety claims
* hallucination literature. 

That's much better.

However, I would still carefully verify the exact factual wording of:

> “the national ratio of extension officers to farming households routinely exceeds 1:1,000.”

The citation [8] needs to support exactly that statement, not merely agricultural-extension statistics generally.

---

# 5. RQ5 is now corrected

You changed:

> “preserving a 100% fail-closed safety boundary”

to:

> “preserving zero unsafe certification on the evaluated safety suites.”

Excellent. 

That is scientifically much more defensible.

Keep that wording.

---

# 6. The adversarial benchmark is much stronger now

This is an important upgrade.

You now explicitly state:

> source-held-out protocol

> entity-disjoint held-out crop and chemical pools

> independent slot-substitution corruption algorithm

> held-out entity vocabulary auditing

> 500 manually annotated edge cases.



That directly addresses my previous concern about implementation leakage.

### One wording correction

You currently say:

> “This construction prevents implementation leakage…”

That's slightly too absolute.

The construction **reduces or guards against** implementation leakage; it doesn't mathematically prove that no leakage exists.

Change to:

> “This construction substantially reduces the risk of implementation leakage…”

That is safer.

### More importantly

You say **500 edge cases were human-annotated**, but you don't report the resulting agreement/validity rate.

Add something like:

> “Independent annotation confirmed X/Y (X%) of generated corruptions as semantically valid.”

If all 500 were valid, report:

> 500/500, 100%.

This would provide evidence that your corruption generator is actually producing meaningful attacks.

---

# 7. The strongest remaining concern: Table 3's B7 zero hazard is partially circular

This is the biggest methodological issue left.

Table 3 says:

> “For B7, zero Unsafe Certified certifications arise by construction of the typed relational verifier.” 

This is dangerous wording.

The reviewer may say:

> “Of course B7 has zero unsafe certification—it was defined to certify only exact slot matches.”

But the actual research question isn't:

> “Can a deterministic exact matcher reject a corrupted tuple?”

It is:

> **“Does that rule correctly distinguish safe from unsafe real-world advisories?”**

That's why your human evaluation and ecological benchmark are important.

Change:

> “zero Unsafe Certified certifications arise by construction”

to something like:

> “The verifier's hard gate disallows certification when any required relational slot fails to match the authoritative record; the resulting zero observed unsafe certifications are evaluated empirically on the benchmark.”

This prevents the result from sounding tautological.

---

# 8. Table 3 is now much better

This table is exactly what I wanted as E1:

| System      | Correct Certified | Unsafe Certified | Abstained |
| ----------- | ----------------: | ---------------: | --------: |
| LLM         |             58.73 |             1.85 |     39.42 |
| RAG         |             56.07 |            13.45 |     30.48 |
| Lexical     |             47.10 |             9.38 |     43.53 |
| KrishokChat |             65.80 |             0.00 |     34.20 |



This is now a much more meaningful headline table.

### But I want one extra column:

**Evidence-supported certification precision**

because the paper is fundamentally about certification.

---

# 9. There is still a problem with the 65.80% correctness interpretation

You now clearly define:

> Correct Certified = certified **and agronomically correct**. 

Good.

But it would be stronger to give:

$$
Precision_{cert}
=
\frac{Correctly\ Certified}
{All\ Certified}
$$

For KrishokChat:

$$
\frac{65.80}{65.80+0}=100\%
$$

But that is only because unsafe/mistaken certifications are zero under the defined hazard category.

A reviewer may still ask about:

> certified but incomplete
> certified but agronomically suboptimal
> certified but missing contextual conditions

Human evaluation helps here, but report a broader correctness breakdown.

---

# 10. Table 4 remains the one odd-looking experiment

You still have:

* wrong crop → lexical 0%
* wrong pathogen → lexical 0%
* nearly everything else → 100%



This is not inherently invalid, but you haven't explained why.

Your prose says:

> “because all isolated words exist within the retrieved evidence pool.”

That explanation does not account for the two 0% categories.

A reviewer will notice.

### Fix

Add one sentence explaining the construction:

> “Crop and pathogen substitutions were evaluated using entity-level lexical matching of the complete generated phrase rather than independent token presence; these substitutions therefore produced zero false acceptance for B4, whereas numerical and cross-row substitutions preserved lexical overlap.”

Or whatever the actual implementation is.

The benchmark and baseline protocol need to be exactly clear here.

---

# 11. The ablation is now excellent

Table 5 is substantially more convincing.

The hierarchy:

1. dosage
2. regulatory polarity
3. crop
4. pathogen
5. denominator
6. formulation
7. unit
8. stage
9. PHI
10. interval

is a nice result. 

And you correctly softened the conclusion to:

> “each semantic slot contributes measurable protection on the evaluated attack suite.”

Perfect.

I would keep that sentence.

---

# 12. One issue with the ablation methodology remains

You call this:

> “11-Slot Schema Ablation”

but there are **10 single-slot ablations + full system + lexical baseline**.

That's okay, because there are 11 semantic slots and dosage is composite, but a reviewer could expect exactly 11 ablation configurations.

Count them:

* dosage
* polarity
* crop
* pathogen
* denominator
* formulation
* unit
* stage
* PHI
* interval

That's **10 removals**.

Where is **active ingredient \(a\)**?

It is missing.

This is now the most obvious experimental omission in the new version.

Your schema has:

$$
c,p,s,a,f,[d_{min},d_{max}],u,v,\tau,\phi,\rho
$$

yet there is no:

> **Minus Active Ingredient (a)**

experiment.

### You absolutely need to add it.

This is not a cosmetic issue.

The active ingredient is one of the most safety-critical slots.

I would consider this a **major revision blocker**.

---

# 13. Add “Minus Active Ingredient” immediately

The result table should have:

> Minus Active Ingredient \(a\)

with actual measured hazard.

I expect it could be highly important, but **don't predict the number**. Run it.

This also gives you the full semantic-slot ablation:

**11/11 semantic slots tested.**

---

# 14. Calibration section is now strong

Table 6 is solid.

KrishokChat:

* AURC = 0.0153
* ECE = 0.0785
* Brier = 0.0116
* coverage = 84.56%
* test risk = 1.26%



This is one of the stronger quantitative sections.

### But your RQ2 says:

> “does it outperform generic uncertainty baselines?”

You need to be explicit about **which metric establishes superiority**.

You have lower AURC and Brier, but the LLM judge actually has lower test risk (0.54%) at much lower coverage (36.6%).

So don't say:

> “KrishokChat has the lowest risk.”

It doesn't.

Say:

> “KrishokChat achieves the strongest overall risk–coverage trade-off, with the lowest AURC and highest evaluated coverage among the tested policies.”

That's much more precise.

---

# 15. Table 7 CBC is now properly fixed

Excellent.

You changed:

> “95% CI for P(CERTIFY|CF)”

rather than pretending it is the CI for CBC. 

This was exactly the correction I wanted.

---

# 16. E6 now needs one more thing: per-register results

You say:

> 4,000 queries spanning standard Bengali, 1,001 authentic farmer queries, regional dialects, and Banglish. 

But Table 8 only gives aggregate results.

Since RQ4 specifically asks about dialectal robustness, I strongly recommend adding:

| Register         |     N | Correct | Abstain | Unsafe |
| ---------------- | ----: | ------: | ------: | -----: |
| Standard Bengali |       |         |         |        |
| Farmer           | 1,001 |         |         |        |
| Chittagong       |       |         |         |        |
| Sylhet           |       |         |         |        |
| Noakhali         |       |         |         |        |
| Barisal          |       |         |         |        |
| Banglish         |       |         |         |        |

This is one of the most natural reviewer requests.

---

# 17. Your security definitions are now good

ASR and UCR are clearly defined. 

No major problem.

One nuance:

> “For prompt injection attacks, UCR and ASR coincide when any successful attack produces a certified unsafe output.”

Correctly phrased as a condition, not universally.

Good.

---

# 18. Security experiment: impressive, but add attack-family breakdown

You report 1,400 attacks across seven families, but Table 9 aggregates them.

A reviewer will likely ask:

> Which attacks were hardest?

You should give a supplementary table:

| Attack family       |  N | B1 ASR | B2 ASR | B5 ASR | B7 ASR |
| ------------------- | -: | -----: | -----: | -----: | -----: |
| Direct override     |    |        |        |        |        |
| Evidence override   |    |        |        |        |        |
| Retrieval poisoning |    |        |        |        |        |
| Delimiter           |    |        |        |        |        |
| Bengali             |    |        |        |        |        |
| Banglish            |    |        |        |        |        |
| Code-switch         |    |        |        |        |        |

This would make your security evaluation substantially stronger.

---

# 19. Economics is now much more reproducible

This is a major improvement.

You now explicitly state:

> GPT-4o-mini pricing assumptions
> 1,000 input + 500 output tokens
> A100 $2.80/hr
> 4,000 queries/hr
> Gemma via local Ollama
> August 2026 pricing. 

Much better.

### But one thing bothers me:

You compare:

> Commercial Cloud LLM = GPT-4o-mini

while the actual system is using:

> Gemma-4 local Ollama.

That's fair as a deployment-cost comparison, but call it:

> **commercial API baseline**

not “Commercial Cloud LLM” generically.

Otherwise a reviewer can accuse you of cherry-picking a specific cheap model.

Also, because pricing is current as of August 2026, the actual provider pricing should be cited in the final paper.

---

# 20. The “92.2% cost reduction” is correct, but define baseline

You should explicitly show:

$$
1-\frac{0.1798}{2.30}=92.18\%
$$

Then reviewers don't have to calculate it.

Also say:

> “relative to the GPT-4o-mini baseline under the stated token assumptions.”

This is more rigorous.

---

# 21. Latency is still incomplete

You state:

> aggregate weighted latency p50 = 1,258.97 ms

but RQ5 asks for **p95 latency**.

The deterministic stage has p95 ≤ 0.94ms, but the **full system p95** is not reported.

This remains a gap.

You need:

| Configuration | p50 | p95 | p99 |
| ------------- | --: | --: | --: |
| Full system   |     |     |     |
| T0–T2         |     |     |     |
| T3            |     |     |     |

This is necessary for RQ5.

---

# 22. Multi-generator experiment is now properly fixed

Excellent.

You now explicitly say:

> 0/6,000 cross-model cases

and:

> aggregate CI [0.00%, 0.06%]. 

This resolves my previous concern.

You also changed the claim to:

> “model-invariant zero unsafe certification across the three evaluated generators.”

Much better than “strictly model-independent.”

Keep this.

---

# 23. Table 11's caption is technically misleading

It says:

> “across 2,000 Queries”

but the experiment contains:

> 2,000 per generator × 3 = 6,000.

You clarify this in the text, but the table caption should say:

> **“across 6,000 evaluations (2,000 per generator)”**

The individual model rows are each 2,000.

The aggregate is 6,000.

Fix the caption.

---

# 24. Safe degradation is now one of the strongest parts

This is excellent.

You show:

| Retrieval | RAG Hazard | KC Coverage | KC Hazard |
| --------- | ---------: | ----------: | --------: |
| 1.00      |      10.0% |      84.56% |         0 |
| 0.60      |      19.2% |      54.30% |         0 |
| 0.00      |      33.2% |           0 |         0 |
| omission  |      23.2% |           0 |         0 |



That is a very strong result.

I would actually make this **one of the main figures**, not just a table.

The visual message is:

> **Retrieval quality ↓ → coverage ↓, not safety ↓**

That is the central expert-system insight.

---

# 25. But “monotonic safe degradation” is slightly imprecise

You say:

> “certification coverage smoothly drops from 84.56% to 0.00%.”

But there are only four points.

“Monotonic across the evaluated regimes” is safer than “smoothly.”

Use:

> “coverage decreases monotonically across the evaluated retrieval regimes.”

---

# 26. Human evaluation is now genuinely strong

This is much better than the previous version.

You now specify:

* 200 responses
* 120 safe
* 40 borderline/complex
* 40 adversarial/security
* identical queries
* randomized output order
* blinded
* no provenance metadata
* independent deployment approval
* response-level CIs. 

This is exactly the kind of methodological detail I wanted.

The result:

> 4.82/5 correctness
> 100% safety
> 98.5% traceability
> 96.5% approval

is potentially very persuasive. 

---

# 27. One concern about the human study

You say:

> “three certified agricultural extension specialists and agronomists”

That could mean:

* three people, all certified?
* some extension specialists, some agronomists?
* what certifications?

Give the exact evaluator profile in supplementary material:

> E1: Plant pathology specialist, X years
> E2: agricultural extension officer, X years
> E3: agronomist, X years

This is much more credible.

Also state whether they were paid.

---

# 28. Human evaluation: your baseline rejection statement needs more careful wording

You say:

> LLM Direct and Vanilla RAG were rejected by human agronomists in 62.0% and 47.5% cases.

But what exactly does “rejected” mean?

Was it:

> Deployment Approval = No

or:

> Safety = Fail?

Those are different.

Use:

> “received no deployment approval in 62.0%…”

if that's what the table measures.

Don't interchange “rejected” with “unsafe.”

---

# 29. Failure taxonomy is now fully coherent

The temporal-expiration problem is fixed beautifully:

> “source timestamp validity enforced by a provenance-policy layer external to the 11-slot claim tuple.”

That is exactly the correct solution. 

No issue there.

---

# 30. There is a potential naming inconsistency: “Symptom Ambiguity”

Table 14 says:

> R6 Dialectal Symptom Ambiguity.

But the system is agricultural advisory.

“Symptom” sounds more clinical.

Use:

> **Dialectal Query Ambiguity**

or:

> **Dialectal Agronomic Ambiguity**

This is minor but worth fixing.

---

# 31. One serious concern: you say “all 11 slots” but your adversarial benchmark has 10 hazard families

That's fine.

But RQ3 asks:

> Which relational slots contribute most critically?

You need the active ingredient ablation, as mentioned.

Again:

### This is the one remaining obvious experimental omission.

Add:

> **Minus Active Ingredient (a)**

and rerun Table 5.

---

# 32. Your conclusion is now appropriately cautious

The new conclusion says:

> “rigorous, auditable safety controls … within the evaluated scope.”

Excellent. 

This is the correct level of claim.

Don't make it stronger.

---

# 33. Reference section: still the biggest non-experimental issue

Your references [17] and [18] now appear as:

> manuscript under review; public identifier pending assignment; authoritative local source…



This is acceptable for internal drafting, but I would **not submit it that way**.

Since you actually have arXiv records for your prior work, use those actual bibliographic entries.

You explicitly gave me:

* `2606.29243`
* `2608.14886`

So use those.

That is much more normal academically.

---

# 34. Another important bibliographic issue

Your reference [18]:

> “AgriTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval.”

Make absolutely sure this is the exact title of `2608.14886`.

Don't rely on an internal working title.

Your manuscript must use the exact public paper title/authors/version.

---

# 35. Your related work is now adequate, but I would still add 5–10 recent papers

The paper is no longer embarrassingly under-referenced.

But because this is 2026, and because your novelty is specifically:

> evidence verification + relation binding + selective certification

you should add a few recent 2025/2026 papers on:

* RAG hallucination detection
* evidence-grounded verification
* LLM abstention
* conformal selective prediction
* RAG security

Not because you need more citations, but because the reviewer may otherwise say:

> “The literature review stops too early.”

---

# 36. One wording issue throughout the paper: “eliminate”

You still use:

> “eliminating false acceptances”

in Contribution C1. 

And:

> “eliminates dangerous acceptances”

in the conclusion. 

Given your empirical evidence, use:

> “eliminating observed dangerous acceptances in the evaluated suites”

or:

> “reducing dangerous acceptance to zero on the evaluated suites.”

This is more rigorous.

---

# 37. One subtle problem: “fail-closed” isn't equivalent to “safe”

Your system can fail closed, but if the underlying authoritative knowledge record is wrong, the system can still certify a wrong recommendation.

Your paper mostly acknowledges scope limitations, which is good.

Add one explicit sentence:

> “Fail-closed certification constrains unsupported generation but does not establish the correctness of the underlying authoritative source material.”

That is an important philosophical limitation.

---

# 38. Another important issue: the source authority hierarchy isn't formally defined

You repeatedly use:

> “authoritative evidence”

and:

> “official institutional record.”

But what happens if:

* two BARI records conflict?
* BRRI contradicts DAE?
* an older source conflicts with a newer source?

You don't experimentally test this.

You don't necessarily need another major experiment, but add a subsection:

## Source Authority and Conflict Policy

Define:

$$
Authority(source)
$$

and:

* institution
* publication date
* regulatory status
* scope
* version

Then state:

> conflicting authoritative records trigger abstention/escalation rather than arbitrary selection.

That would significantly strengthen the expert-system aspect.

---

# 39. Current paper structure is now very good

The 19 pages are justified.

You now have:

1. Introduction
2. Related work
3. Formal problem
4. Architecture
5. Experiment methodology
6. Results
7. Failure taxonomy
8. Discussion
9. Limitations/ethics
10. Reproducibility
11. Conclusion

This is exactly where I would stop.

I would **not expand the manuscript further** unless adding a genuinely necessary experiment.

---

# 40. My current scorecard

| Criterion            |   Score |
| -------------------- | ------: |
| Importance           | **9.0** |
| Novelty              | **8.7** |
| Expert Systems fit   | **9.5** |
| Formal method        | **8.8** |
| Experimental breadth | **9.3** |
| Experimental rigor   | **8.2** |
| Statistical rigor    | **8.3** |
| Baselines            | **8.4** |
| Human validation     | **9.0** |
| Robustness           | **9.0** |
| Reproducibility      | **8.6** |
| Writing              | **8.7** |
| Literature           | **7.5** |
| Overall              | **8.6** |

---

# 41. The remaining “must fix” list

At this point, I would reduce everything to **eight concrete actions**.

### 1. Add the missing active-ingredient ablation

This is the most important experimental fix.

### 2. Report the 500-edge-case annotation result

You claim 500 were human checked; show what they found.

### 3. Add per-register dialect results

Standard Bengali / farmer / each dialect / Banglish.

### 4. Give full-system p95/p99 latency

Not only T0–T2 p95.

### 5. Fix Table 11 caption

Say **6,000 total evaluations**, not 2,000.

### 6. Replace “eliminate” with “zero observed on evaluated suites”

Where appropriate.

### 7. Replace internal/local references [17–18] with the exact public bibliographic records

Especially your two prior arXiv papers.

### 8. Add a source-conflict policy

Even a small formal subsection is enough.

---

# 42. What I would NOT change

Don't:

* redesign the architecture
* add more random datasets
* add more vision experiments
* make the paper longer just for length
* change the title
* remove the expert evaluation
* remove the retrieval-degradation study
* remove the multi-generator study
* weaken the central relational-certification idea

Those are now the strengths.

---

# Final referee recommendation

**This is now a serious submission candidate.**

The current manuscript has crossed the threshold where I would no longer describe it as “an application paper trying to become an Expert Systems paper.” It now genuinely presents a **knowledge-engineered expert-system framework**, with formal relational representation, deterministic reasoning, selective certification, provenance, robustness testing, system economics, and human expert validation. The six-layer lineage architecture is especially effective. 

The remaining work is primarily **scientific polishing and auditability**, not conceptual redesign.

My expected trajectory is:

**Current: 8.6/10 — Major Revision**

→ add active-ingredient ablation + per-register results + full latency + source-conflict policy + final citation cleanup

→ **~9.0/10 — strong accept candidate**

The single most important scientific message I would preserve in the final version is your E12 result:

> when retrieval quality deteriorates, KrishokChat loses **coverage rather than safety**.

That is the result that most clearly demonstrates why the proposed architecture is an **expert system**, rather than simply another RAG pipeline. 
