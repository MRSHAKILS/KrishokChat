Yes. I reviewed the **new LaTeX draft itself**, compiled it, checked the internal logic of the methods/results, and compared the positioning against your two prior papers and the current *Expert Systems* guidance.

My verdict is quite different from the previous draft:

# Revised referee score

**Current draft: 7.4/10**

**Recommendation: Major Revision**

**Potential after fixing the issues below: 8.5–9.0/10**

So: **this is now a substantially stronger paper**, and the basic direction is right. The main danger is no longer “this looks like a generic RAG application.” The danger is now **overclaiming from experiments that are not yet sufficiently rigorous or internally consistent**.

The journal is a strong fit: *Expert Systems* explicitly targets knowledge engineering, knowledge representation/reasoning, AI and robust real-world system construction, and says detailed scientific evaluation is essential. ([Wiley Online Library][1])

---

# 1. What improved dramatically

These changes were exactly the right direction.

### The title is much better

> **“A Knowledge-Engineered Expert System for Relation-Aware Certification…”**

This is much more appropriate than framing the work simply as “a Bengali agricultural chatbot.”

You are now telling the reviewer:

**knowledge engineering + reasoning + certification + real deployment**

That maps directly to the journal.

### The RQs are excellent

The six RQs give the paper an actual scientific spine:

* relational certification
* calibration
* slot sensitivity
* ecological/dialect robustness
* economics/latency
* generator/retrieval invariance

That is a major improvement.

### The prior-work positioning is much better

Your explicit:

> Paper 1 = resource/SFT
> Paper 2 = retrieval diagnosis
> Paper 3 = expert system

is exactly what you needed.

And it matches what those papers actually do. The first paper establishes the 145,500-pair provenance-grounded resource and 1,001 authentic farmer queries; the second studies retrieval over 2,882 nodes and finds major differences by query type and language. ([arXiv][2])

This is now a coherent research program rather than three seemingly overlapping papers.

---

# 2. The biggest improvement: you now have a real mechanism

The strongest new part is your formal certification contract:

$$
\pi(x)=
\begin{cases}
CERTIFY & \text{if relationally entailed and calibrated}\\
ESCALATE & \text{if dangerous/crisis}\\
ABSTAIN & \text{otherwise}
\end{cases}
$$

That is excellent conceptually.

And the key condition:

> all slots must strictly match the evidence tuple

makes the paper much more concrete than the previous “similarity score” formulation.

This is the point where the paper begins to look like a **knowledge-engineered expert system**, rather than an LLM wrapper.

---

# 3. The 10,000-case misbinding experiment is potentially your strongest experiment

This is exactly the kind of experiment I wanted you to add.

The structure is very good:

* wrong dosage
* wrong unit
* wrong denominator
* wrong crop
* wrong pathogen
* wrong formulation
* wrong PHI
* wrong application interval
* polarity flip
* cross-row binding

Especially:

> **Cross-Row Entity Misbinding**

That directly tests the central thesis.

The claim:

> lexical matcher = 80% dangerous acceptance
> proposed verifier = 0/10,000

is extremely compelling **if the benchmark generation and evaluation protocol are independently rigorous**.

That “if” is important.

---

# 4. But there is a serious problem with the adversarial benchmark

Right now a reviewer can attack this result very easily:

> “The proposed verifier is almost guaranteed to win because the adversarial cases are generated directly from the verifier's own schema.”

That is the single biggest methodological vulnerability in the new draft.

You need to make the benchmark construction **independent of the implementation**.

### Specifically, document:

1. How a clean evidence record is selected.
2. How the corrupted claim is generated.
3. How the corruption target is chosen.
4. How corruption avoids producing trivial formatting clues.
5. Whether corruption can combine multiple slots.
6. Whether the verifier sees the corruption rules.
7. Whether attack generation uses the same templates as training.
8. Whether test attacks are generated from held-out source records.
9. Whether a separate annotator validates the intended corruption.

I would make a **source-held-out attack benchmark**:

> Build attacks from knowledge records whose specific source/chemical/crop combinations never occur during calibration or development.

That is much harder to dismiss.

---

# 5. Your lexical baseline result actually needs to be improved

Notice this:

| Attack            | Lexical false acceptance |
| ----------------- | -----------------------: |
| Wrong dosage      |                     100% |
| Wrong unit        |                     100% |
| Wrong denominator |                     100% |
| Wrong crop        |                   **0%** |
| Wrong pathogen    |                   **0%** |
| Wrong formulation |                     100% |
| …                 |                        … |

This is important.

Your prose says lexical matching fails because individual tokens occur somewhere in the evidence pool.

But if the wrong-crop and wrong-pathogen attacks produce **0% lexical false acceptance**, the story is more nuanced.

A reviewer may ask:

> “Why does your lexical baseline fail on numerical misbinding but not crop/pathogen substitution?”

You should explain this explicitly, or redesign the baseline so it actually tests the intended failure mode consistently.

Even better: compare several weak verifiers:

**entity presence**

→ **lexical overlap**

→ **slot-wise matching**

→ **semantic matching**

→ **LLM judge**

→ **full relational matcher**

That gives you a more believable progression.

---

# 6. The slot-ablation table has a major internal problem

Your title says:

> **11-Slot Schema Ablation**

But the tuple is:

$$
\langle c,p,s,a,f,d_{\min},d_{\max},u,v,\tau,\phi,\rho\rangle
$$

That is **12 scalar components** if \(d_{\min}\) and \(d_{\max}\) are counted separately, or 11 semantic slots if “dose bounds” is treated as one composite slot.

That is fine, but you need to explicitly say:

> “The schema contains 11 semantic slots; dosage is represented internally by the composite pair \([d_{\min},d_{\max}]\).”

Otherwise a technical reviewer may flag this.

### Bigger issue:

Your ablation table is missing **growth stage \(s\)**.

You have:

* PHI
* formulation
* interval
* denominator
* unit
* dosage
* pathogen
* crop
* polarity

but **no stage**.

That is a direct contradiction with the claimed 11-slot schema.

Fix it.

---

# 7. The ablation numbers are suspiciously uniform

This will attract reviewer attention immediately.

You report:

> every one of eight different ablations → exactly **10.0% hazard**

That is statistically possible, but scientifically it looks artificial.

A reviewer will wonder:

> “Why does removing PHI, formulation, interval, denominator, unit, dose, pathogen, and crop each produce exactly the same result?”

Especially when they represent very different semantic constraints.

This is one place where you absolutely should **not try to make the results look symmetrical**.

Run the actual experiments and let them differ.

I would much rather see:

```text
−PHI            2.7%
−formulation    5.8%
−interval       1.9%
−denominator    7.1%
−unit           5.4%
−dose          31.6%
−pathogen       8.2%
−crop          11.4%
−stage           4.9%
−polarity       17.8%
```

than a suspiciously perfect 10% everywhere.

Those numbers are examples only; obviously use actual measurements.

---

# 8. Your calibration section is much better—but currently has contradictions

This needs careful fixing.

You say:

> “20,112 rows partitioned into Train (12,068), Dev (4,022), Test (4,022)”

But your actual dataset table says:

* Train = **12,067**
* Dev = **4,022**
* Test = **4,023**

Those sum correctly to 20,112.

So the calibration paragraph is numerically inconsistent.

This should be fixed everywhere.

---

# 9. “Near-zero risk” is not a fair description of 1.26%

You write:

> “84.56% coverage and near-zero risk.”

But the table reports:

**Test risk = 1.26%**

That is not literally “near-zero” in a safety-critical setting.

More importantly, you say:

> “strictly bounding selective risk (0.0% risk at ≤80% coverage).”

That is a different claim from:

> 1.26% risk at the selected 84.56% coverage.

So you should report this transparently.

A much better statement would be:

> “At the target operating point, the method achieves 84.56% coverage with 1.26% test risk; at a more conservative coverage regime of ≤80%, observed test risk falls to 0% on the evaluated set.”

That is defensible.

---

# 10. Your “100% fail-closed safety boundary” claim is too strong

This appears multiple times.

For example:

> “preserving a 100% fail-closed safety boundary”

and:

> “ensuring 0.0% Unsafe Certification”

within the evaluated attack set.

The problem is the manuscript then generalizes this into:

> “suitable for safety-critical agricultural deployment”

and:

> “rigorous, verifiable biosecurity.”

A strict reviewer will say:

**10,000 synthetic attacks ≠ all possible attacks.**

You need to distinguish:

### Empirical guarantee

> 0/10,000 evaluated attacks.

from:

### Universal guarantee

> all possible future attacks.

You have evidence for the first, not the second.

I would change nearly every “100% safety guarantee” formulation to:

> **“100% fail-closed behavior on the evaluated safety test suite.”**

That is a big improvement scientifically.

---

# 11. Your formal “Entails” definition is currently too brittle

You define:

> `Entails(e,C) = 1 iff all 11 atomic slots strictly match the evidence tuple extracted from e.`

This creates a new problem.

What if a valid recommendation is supported by **two authoritative records**?

For example:

Source A:

> crop + pest + chemical + formulation

Source B:

> PHI + interval

Your verifier would reject because no single evidence node contains all slots.

That may be desirable for some safety claims, but then you need to **justify the single-record constraint**.

Otherwise reviewers will say the system has excessive conservatism.

A more general expert-system formulation could distinguish:

$$
Entails(\mathcal E,C)
$$

from:

$$
Entails(e,C)
$$

and allow multi-source reasoning under explicit provenance constraints.

At minimum, discuss this limitation.

---

# 12. You added “source conflict” conceptually—but the paper doesn't actually evaluate it

You now have a much richer provenance hierarchy, but the experiments still mostly assume one authoritative answer.

A real expert system should answer:

> What if BARI and DAE records disagree?

That is one of the strongest experiments you could still add.

Create a **source-conflict benchmark**:

* same crop
* same disease
* same chemical
* different dosage
* different PHI
* different regulatory status

Then evaluate:

**Does the system detect the conflict and abstain/escalate rather than arbitrarily select one?**

This would significantly strengthen the knowledge-engineering contribution.

---

# 13. Temporal validity is also currently asserted rather than demonstrated

You include:

> “Temporal Expiration”

in the failure taxonomy.

But your formal tuple does **not include time/source date**.

So the system cannot currently formally reason over temporal validity unless that exists elsewhere.

You should add provenance metadata such as:

$$
t_{source},\quad t_{valid}
$$

or explicitly say temporal handling is external to the certification tuple.

Right now the paper makes the capability sound more mature than the formal model demonstrates.

---

# 14. The farmer benchmark section is strong, but the dataset composition is unclear

You say:

> 4,000 queries spanning standard Bengali, 1,001 authentic farmer inquiries, four regional dialects, and Banglish.

But I cannot reconstruct the exact 4,000 composition from the manuscript.

You should give an exact table:

| Condition        |     N |
| ---------------- | ----: |
| Standard Bengali |       |
| Farmer queries   | 1,001 |
| Chittagong       |       |
| Sylhet           |       |
| Noakhali         |       |
| Barisal          |       |
| Banglish         |       |
| Total            | 4,000 |

And clarify whether the 1,001 farmer queries overlap with other groups.

This matters statistically.

---

# 15. Dialect robustness is better conceptually—but still needs stratified results

Your previous retrieval paper established that retrieval behavior can vary dramatically by language/query condition; for example, the published retrieval study reports BM25 and dense systems behaving very differently between Bengali, English, colloquial farmer, and formal safety conditions. ([arXiv][3])

That makes your current claim interesting.

But the paper should not collapse all conditions into:

> 0.00% dangerous acceptance.

Give the reviewer:

| Condition        | Coverage | Correct | Abstain | Dangerous |
| ---------------- | -------: | ------: | ------: | --------: |
| Standard Bengali |          |         |         |           |
| Farmer           |          |         |         |           |
| Chittagong       |          |         |         |           |
| Sylhet           |          |         |         |           |
| Noakhali         |          |         |         |           |
| Barisal          |          |         |         |           |
| Banglish         |          |         |         |           |

That will make the safety-noninferiority argument much stronger.

---

# 16. The security experiment is promising but currently not enough for “jailbreak” language

You report:

> 1,400 attacks
> 0% ASR
> 0% unsafe certification.

Very good.

But the reviewer will ask:

> How were these 1,400 attacks generated?

Also:

> Were they manually constructed, automatically generated, or adapted from existing attack sets?

And:

> Were the attacks evaluated on one model or several?

And most importantly:

> Is your “Attack Success Rate” actually the attacker's ability to force an unsafe answer, or simply the deterministic guard's keyword interception rate?

You say:

> Tier 0 blocks 92.1%
> post-generation verifier blocks 7.9%.

That's good, but turn this into a **two-stage defense analysis**.

For each attack:

$$
Attack
\rightarrow
Tier\ 0
\rightarrow
Verifier
\rightarrow
Unsafe\ Certification
$$

Then report the survival rate at each layer.

---

# 17. Retrieval poisoning deserves a separate result

Because you already have:

> “retrieval poisoning”

in the security attacks, reviewers will expect more.

Create a table:

| Poisoning type        | Tier 0 | Retrieval | Verifier | Unsafe certification |
| --------------------- | -----: | --------: | -------: | -------------------: |
| Fake dosage           |        |           |          |                      |
| Fake PHI              |        |           |          |                      |
| Instruction injection |        |           |          |                      |
| Source impersonation  |        |           |          |                      |

This would make the security story much more concrete.

---

# 18. The economics calculation is internally plausible, but still under-documented

The $0.1798/1k figure makes sense mathematically.

But the reviewer still needs:

* model
* provider
* hardware
* input/output tokens
* query assumptions
* concurrency
* pricing date
* cache assumptions

The table's:

> Commercial Cloud LLM = $2.30 / 1k

needs a citation or explicit calculation.

Same for:

> Cloud GPU Vanilla RAG = $0.85 / 1k.

Right now these look like unexplained constants.

The paper should include a short cost equation.

---

# 19. The “15× efficiency” metric is useful—but define it carefully

You define:

$$
C_{\text{safe}}
$$

but not fully enough.

Clarify:

$$
C_{\text{safe}}
=
\frac{C_{\text{serving}}}
{N_{\text{correctly certified safe answers}}}
$$

Then say whether:

* abstained answers count in denominator?
* unsafe answers?
* incorrectly certified answers?
* rejected queries?

This matters.

Otherwise “cost per safe answer” can be manipulated by the denominator definition.

---

# 20. The latency section needs p95/p99

You now report:

> aggregate weighted latency = 1,258.97 ms

But RQ5 specifically asks about p95 latency.

Give:

| Stage        | p50 | p95 | p99 |
| ------------ | --: | --: | --: |
| Router       |     |     |     |
| Retrieval    |     |     |     |
| Generation   |     |     |     |
| Verification |     |     |     |
| Total        |     |     |     |

This is much more credible.

The current:

> “≤0.94 ms p95”

only describes deterministic routing.

---

# 21. Your vision section remains too weak

The paper still reports:

> 100% top-1 parity

That's not enough.

**Parity is not accuracy.**

A reviewer will immediately ask:

> “100% agreement with what?”

You need:

* actual top-1 accuracy
* macro F1
* per-class performance
* test N
* confusion matrix
* FP32 vs INT8
* model size
* latency

Otherwise I would strongly consider shortening this section.

The core paper is now much more interesting than the vision component.

---

# 22. Your failure taxonomy is excellent—but it needs a denominator

The 100-case audit is a good idea.

But:

> 28% retrieval omission
> 22% generative misbinding
> 14% numerical ambiguity

What exactly are the 100 cases?

* all failures?
* all abstentions?
* random samples?
* worst cases?
* test errors?
* user queries?

And how were they sampled?

You need:

> “We randomly sampled 100 residual cases from X total failures using seed Y.”

Then the percentages are interpretable.

---

# 23. You should add a human expert study

After seeing this version, I consider this **the single highest-value experiment still missing**.

You already have an excellent computational evaluation.

Now have agricultural experts evaluate perhaps **200 final responses**.

Especially:

### Question 1

**Is the recommendation agronomically correct?**

### Question 2

**Is the recommendation safe?**

### Question 3

**Is the evidence sufficient?**

### Question 4

**Would you permit this answer to reach a farmer?**

Then compare:

* LLM
* RAG
* LLM judge
* KrishokChat

This would close the biggest remaining applied-AI gap.

---

# 24. Multi-generator evaluation is also still missing

RQ6 says:

> Does the verifier generalize across heterogeneous base generators?

But the results presented here are almost entirely Gemma-4 based.

That means **RQ6 isn't actually answered yet**.

At minimum:

**Generator A:** Gemma

**Generator B:** another open-weight model

**Generator C:** stronger model if feasible

Then keep the verifier unchanged.

This would transform the contribution from:

> “Gemma + custom safety pipeline”

to:

> **“model-independent certification layer.”**

That is much stronger.

---

# 25. The paper needs a genuine retrieval-quality experiment

The second paper tells us retrieval can fail badly on farmer-style queries. ([arXiv][3])

The new system paper says:

> “degrade safely under retrieval uncertainty.”

Good.

But where is the experiment?

You should deliberately manipulate retrieval quality:

### Gold retrieval

correct evidence available

### Top-k noisy

relevant evidence mixed with irrelevant

### Missing evidence

correct evidence removed

### Wrong evidence

relevant-looking but incorrect evidence

Then measure:

**certification rate + unsafe acceptance + abstention**

This would answer one of the most important system questions:

> **What does your expert system do when retrieval is wrong?**

---

# 26. I would add a “safe degradation curve”

This could become a signature result.

X-axis:

**retrieval recall**

Y-axis:

**unsafe certification**

and perhaps another line:

**coverage**

The desirable behavior is:

> retrieval quality ↓ → coverage ↓
> but unsafe certification remains ≈ 0.

That is a beautiful demonstration of the value of the certification layer.

---

# 27. The paper now needs a real comparison with generic conformal prediction

You added B6, which is good.

But:

> “standard softmax confidence thresholding calibrated via conformal prediction”

is not sufficiently precise.

What exact conformal method?

* split conformal?
* APS?
* RAPS?
* threshold calibration?
* coverage target?

And what is the validity guarantee under your data assumptions?

You need to state the exact method and cite it.

This is especially important because you are making a paper about **calibrated selective decision making**.

---

# 28. Your related work is still much too short

This is now one of the biggest remaining weaknesses.

The paper currently has only a handful of references.

For a serious 2026 Expert Systems submission, this is nowhere near enough.

The journal specifically asks reviewers to assess novelty against published work and whether similar work has already appeared and been properly cited. ([Wiley Online Library][4])

You need a substantially richer related-work section covering:

* agricultural expert systems
* RAG
* factuality
* evidence verification
* claim verification
* hallucination detection
* selective prediction
* conformal prediction
* safe refusal
* prompt injection
* retrieval poisoning
* low-resource Bengali
* agricultural advisory systems

And you need to cite actual peer-reviewed work, not just system names.

---

# 29. The bibliography is currently the biggest publication-readiness problem

You still have:

> `Authoritative Reference. (2026).`

That cannot go into the submitted paper.

Replace those with the actual bibliographic records for:

* your first paper
* your second paper

and add all methods/baselines.

This is a **must-fix before submission**.

---

# 30. Your abstract is now strong—but one sentence is too aggressive

This:

> “Evidence-linked relation verification and calibrated selective abstention transform unconstrained generative models into auditable, fail-closed expert systems suitable for safety-critical agricultural deployment.”

The phrase:

> **“suitable for safety-critical agricultural deployment”**

sounds like a real deployment safety claim.

I would soften to:

> “...supporting auditable, fail-closed operation within the evaluated agricultural safety scope.”

Much safer.

Similarly:

> “verifiable biosecurity”

is too strong.

Use:

> **“auditable safety controls.”**

---

# 31. Your abstract also has a numerical inconsistency in terminology

You write:

> “typed 11-slot relational tuples”

and then list 12 symbolic entries.

As discussed above, this is fixable by calling dosage a composite slot, but the abstract must be consistent with the formal section.

---

# 32. The paper currently has a subtle problem: the verifier is almost deterministic, so why is calibration necessary?

This is scientifically interesting and needs explanation.

You say:

> all 11 slots strictly match → entailment.

If that is exact deterministic matching, then what uncertainty is the calibration score measuring?

Presumably:

* tuple extraction
* evidence extraction
* retrieval quality
* partial evidence
* generator confidence
* parser confidence

But the paper doesn't clearly explain this.

A reviewer may ask:

> “If certification requires exact deterministic slot matching, what is the role of the calibrated confidence score?”

You need to distinguish:

### Logical validity

$$
L \in \{0,1\}
$$

from:

### Operational uncertainty

$$
g(x)\in[0,1]
$$

Then certification becomes:

$$
CERTIFY
\iff
L=1 \land g\ge \theta^*
$$

This is actually a nice architecture—just explain it.

---

# 33. This distinction should become a key conceptual contribution

I would call them:

### Hard constraints

* banned status
* exact dosage
* units
* slot binding
* provenance

and

### Soft uncertainty

* retrieval quality
* extraction confidence
* ambiguity
* generator reliability
* calibration

Then:

> **Hard constraints prevent logically invalid recommendations; calibrated uncertainty controls when the system should abstain despite formally matching evidence.**

That is a very strong expert-system idea.

---

# 34. One more important issue: your “formal certification contract” is not truly a proof of safety

The word:

> “formally”

is okay for defining the rule.

But don't imply mathematical proof that the agricultural recommendation itself is correct.

You can prove:

> If the evidence is authoritative and correct, and all required slots match, the system's certification rule won't accept a tuple violating those constraints.

You cannot prove:

> the authoritative source itself is never wrong.

This distinction should appear in limitations.

---

# 35. The source lineage is much better now

This is one of my favorite additions:

> Publications → Documents → Knowledge Nodes → Evidence Spans → Claim Tuples → Advisory Records

Excellent.

That is exactly the kind of knowledge-engineering structure the journal appreciates.

And it solves a major problem from the previous draft.

However, fix this line:

> “2,135 production-active nodes”

versus later:

> “2,135 curated national research documents”

Those are still inconsistent.

The **2,135 number must have one meaning throughout the paper.**

Your prior papers establish 2,882 nodes in the retrieval benchmark, so the 2,135 production-active subset can be perfectly legitimate—just define it clearly. ([arXiv][3])

---

# 36. Your prior-paper integration is now scientifically clean

This part is excellent.

The first paper establishes the verified agricultural resource and farmer-query benchmark. ([arXiv][2])

The second paper establishes the retrieval landscape and its failure modes. ([arXiv][3])

Your current paper then sits above them:

$$
Resource
\rightarrow
Retrieval
\rightarrow
Certification
\rightarrow
Deployment
$$

That is a strong publication architecture.

---

# 37. The paper is now much more aligned with *Expert Systems*

The journal describes its scope as:

> integration of AI and knowledge engineering in real-world complex systems

and explicitly lists knowledge representation/reasoning and domain-specific expert systems. ([Wiley Online Library][1])

Your revised paper now explicitly contains:

* knowledge hierarchy
* structured representation
* deterministic rules
* provenance
* relational reasoning
* conflict/safety logic
* selective decision policy
* runtime action selection
* real-world system evaluation

That alignment is now **very good**.

---

# 38. Submission formatting: one actual issue I found

I successfully compiled the `.tex` into a **13-page PDF**.

The compilation completes, but there are several LaTeX layout warnings:

* overfull tables around the results section
* one paragraph overflow
* underfull table alignments

In particular, several result tables are wider than the page.

This isn't a scientific problem, but it needs cleanup before submission.

The current result is **13 pages**, which is comfortably within the journal's 15,000-word maximum; Wiley currently permits free-format LaTeX submission and explicitly encourages LaTeX, while requiring the PDF version alongside the editable `.tex`. ([Wiley Online Library][1])

---

# 39. A critical journal-specific point: figures

The current Wiley guidance says figures should be uploaded as individual files rather than relying only on embedded versions, although embedded figures are acceptable for review/free-format preparation. ([Wiley Online Library][1])

So before submission:

* keep the embedded figures for review
* also prepare separate high-resolution figure files
* make sure every figure/table is referenced in the text
* provide proper legends

---

# 40. Current scorecard

| Category              | Previous | Current |
| --------------------- | -------: | ------: |
| Problem importance    |      7.0 | **8.5** |
| Novelty               |      7.5 | **8.0** |
| Expert-system fit     |      6.5 | **9.0** |
| Technical formulation |      5.5 | **8.0** |
| Experimental depth    |      4.0 | **8.0** |
| Baselines             |      4.0 | **7.5** |
| Robustness            |      4.0 | **8.0** |
| Human validation      |        0 |   **0** |
| Statistical rigor     |      2.5 | **6.5** |
| Reproducibility       |      4.5 | **7.5** |
| Literature            |      4.0 | **4.5** |
| Presentation          |      7.5 | **7.5** |
| **Overall**           |  **5.8** | **7.4** |

The biggest reason it isn't 8.5+ yet is **not lack of experiments**.

It is that several experiments look **too perfectly engineered**, and some claims/numbers don't yet line up perfectly.

---

# 41. My “red flag” list

These are the things I would fix **before doing anything else**:

### 🔴 1. Ablation table

Missing growth stage + suspicious identical 10% results.

### 🔴 2. Dataset split inconsistency

12,067/4,022/4,023 vs 12,068/4,022/4,022.

### 🔴 3. 11-slot terminology

12 tuple components unless dosage bounds are explicitly one composite slot.

### 🔴 4. 2,135 terminology

Nodes vs documents.

### 🔴 5. “Near-zero risk”

Reported test risk is 1.26%.

### 🔴 6. “100% safety boundary”

Overclaim.

### 🔴 7. Adversarial benchmark independence

Currently too easy for a skeptical reviewer to accuse of being schema-aligned.

### 🔴 8. Missing human evaluation

### 🔴 9. RQ6 not actually evaluated

Only Gemma is presented.

### 🔴 10. Bibliography

The “Authoritative Reference” placeholders must disappear.

---

# 42. What I would change before adding ANY new experiment

This is important.

Don't immediately build more experiments.

First, make the current paper **methodologically clean**.

I would do these in order:

**Step 1:** Fix all numerical inconsistencies.

**Step 2:** Fix schema terminology.

**Step 3:** Re-run the entire ablation suite from scratch.

**Step 4:** Freeze a proper adversarial benchmark protocol.

**Step 5:** Add exact baseline definitions.

**Step 6:** Define calibration mathematically.

**Step 7:** Replace every universal safety claim with an evaluated-scope claim.

**Step 8:** Replace placeholder references.

Only then add the remaining high-value experiments.

---

# 43. The three experiments I would add next

After cleaning the existing results, my priority order is:

## #1 — Multi-generator verification

Same knowledge base + same verifier.

Different generators.

This answers RQ6 and establishes model-independence.

---

## #2 — Retrieval degradation / safe-degradation curve

Use the retrieval failures from your second paper.

This creates a direct scientific bridge between Paper 2 and Paper 3.

It may become the most elegant experiment in the entire manuscript.

Your second paper has already shown that retrieval quality changes sharply by query type and linguistic condition. ([arXiv][3])

Now show:

> when retrieval quality drops, KrishokChat **abstains rather than hallucinating**.

That is extremely strong.

---

## #3 — Expert human evaluation

200–300 cases.

This closes the application-validation gap.

---

# 44. What I would expect after those three experiments

If the results are strong **and statistically clean**, I would move the paper approximately to:

**8.5–8.8/10**

My likely recommendation would then become:

> **Minor Revision**

rather than Major Revision.

That is the point where I would feel comfortable calling this a genuine **strong-accept candidate**.

---

# 45. My final referee decision on this exact `.tex`

### Recommendation

**Major Revision**

### But importantly:

**Not because the research direction is weak.**

Quite the opposite.

The revised manuscript now has a **strong central idea, good journal fit, substantially deeper experimentation, and a coherent relationship to the prior work**.

The remaining problem is:

> **the paper currently looks slightly “too perfect” in places and needs more methodological transparency and independent validation before its strongest claims become fully convincing.**

That is a fixable problem.

The strongest version of this paper is now very clear:

$$
\boxed{
\text{Retrieval}
\rightarrow
\text{Generation}
\rightarrow
\text{Relational Verification}
\rightarrow
\text{Calibration}
\rightarrow
\text{Safe Decision}
}
$$

with your previous papers supplying the **knowledge resource** and **retrieval diagnosis**, and this paper providing the **expert-system layer**. That positioning is strong and is well aligned with the journal's stated emphasis on knowledge engineering and robust system construction. ([Wiley Online Library][1])

**Bottom line: I would keep this architecture and results strategy. I would not scrap the paper. I would do one rigorous “integrity pass” on the existing experiments, then add multi-generator + retrieval-degradation + expert-human evaluation. That is the path I'd take toward a serious strong-accept submission.**

[1]: https://onlinelibrary.wiley.com/page/journal/14680394/homepage/forauthors.html?utm_source=chatgpt.com "Expert Systems"
[2]: https://arxiv.org/abs/2606.29243?utm_source=chatgpt.com "KrishokChat: A Citation-Grounded Dataset and Benchmark for Bengali Agricultural Advisory"
[3]: https://arxiv.org/abs/2608.14886?utm_source=chatgpt.com "Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory"
[4]: https://onlinelibrary.wiley.com/page/journal/14680394/homepage/reviewer-guidelines?utm_source=chatgpt.com "Expert Systems Reviewer Guidelines"
