I have now treated this as a **full CEA paper-design exercise**, not a rewrite of the current draft. I used the current 18-page draft, the new `master_results.yaml`, and current 2025–2026 literature/venue expectations. I also checked the current CEA scope carefully: CEA explicitly emphasizes **novelty/innovation and advancement of the state of the art in computers/electronics for agriculture**; merely applying existing software/hardware to a crop is not sufficient, whereas investigator-developed system innovations are in scope. That means this should be submitted as a **full Original Research Paper**, not an “Application Note.” ([Elsevier Shop][1])

The new master file is much stronger than the earlier manuscript. It is marked `FROZEN_AND_VERIFIED`, with 558 backend tests passing, 50/50 golden replay, and a green frontend build.  More importantly, you already have genuinely interesting safety evidence: the typed verifier rejects all 10,000 counterexamples in the current misbinding benchmark, while weaker approaches accept large fractions of corrupted evidence; the 11-slot ablation shows strong, heterogeneous contributions from dosage, regulatory status, active ingredient, crop, pathogen, units, formulation, stage, PHI, and interval.  

So I would now build the CEA paper around **that**, not around the previous “26 experiments” framing.

---

# Final CEA paper identity

## Recommended working title

**Bounded-Authority Agricultural Advisory: Selective Resolution and Evidence-Bound Verification for Safe Bengali Decision Support**

Two alternatives worth keeping during drafting:

**Safety-Critical Agricultural Advisory through Bounded Factual Authority and Selective Resolution**

**Evidence-Bound Agricultural Advisory under Resource Constraints: Selective Routing, Fail-Closed Verification, and Deployment Evaluation**

I prefer the first.

The word **authority** is important. It captures the deeper contribution better than “deterministic routing.”

---

# 1. The paper's central scientific idea

The paper should make one central argument:

> In safety-sensitive agricultural advisory, the component that generates fluent language should not necessarily be the component that determines factual authority. Separating factual authority from linguistic realization, and selectively routing requests among deterministic resolution, grounded generation, abstention, and escalation, can improve safety while retaining useful coverage and operational efficiency.

This is the conceptual center.

Your system therefore becomes:

### Factual authority

Structured, versioned, provenance-carrying agricultural facts.

### Linguistic realization

LLM-generated Bengali explanation.

### Decision authority

A policy that decides whether the system is allowed to:

* answer deterministically,
* generate from retrieved evidence,
* abstain,
* escalate.

That is substantially more interesting than “RAG + safety classifier.”

---

# 2. Why this is a credible CEA direction

The current CEA literature is moving rapidly toward agricultural RAG, structured knowledge, multimodal diagnosis, temporal reasoning, expert intervention, and decision-support systems.

Recent examples include:

* **TARAG**, which explicitly adds temporal knowledge handling and time-aware reranking to agricultural pest/disease RAG; ([ScienceDirect][2])
* **SMART**, which combines structured multimodal representations, retrieval and human-in-the-loop diagnosis; ([ScienceDirect][3])
* a **domain-first goat-farming RAG system** using tables and decision trees as structured knowledge; ([ScienceDirect][4])
* **DSSAT-LM**, which connects LLM semantic parsing with an agricultural crop simulation model and evaluates the resulting decision-support workflow; ([ScienceDirect][5])
* offline/contextual agricultural decision support such as **AgroTutor**; and current CEA work on edge computing and dependability/security in agriculture. ([ScienceDirect][6])

So you should **incorporate temporal validity, structured knowledge, expert evaluation, multimodal uncertainty, offline/edge evaluation and security testing** where they strengthen the architecture.

But you should not claim any of those as your headline novelty.

The novelty should be their integration into a **factual-authority-controlled decision architecture**, and the evidence demonstrating how that changes safety/coverage/efficiency.

---

# 3. What the paper must NOT claim

This is important enough to lock before experiments.

Do not claim:

> first Bengali agricultural RAG

Farmer.Chat is already a substantial multilingual deployed agricultural GenAI system, and KrishokBondhu already occupies the Bengali voice/RAG space. Farmer.Chat reports deployment in four countries with >15,000 farmers and >300,000 queries. ([Microsoft][7])

Do not claim:

> first agricultural multimodal RAG

Current CEA work already includes structured multimodal agricultural retrieval and diagnosis. ([ScienceDirect][3])

Do not claim:

> first rule-first agricultural advisory

Rule/expert-system approaches are old, and recent agricultural systems are again explicitly using structured/table/decision-tree knowledge. ([ScienceDirect][4])

Do not claim:

> first time-aware agricultural RAG

TARAG already exists. ([ScienceDirect][2])

Do not claim:

> zero-risk

The correct claim is:

> zero dangerous acceptance was **observed on the specified independent test suite**, with the appropriate confidence bound.

And only after the new independent holdout experiment is done.

---

# 4. What is actually new enough to build the paper around

I see four layers.

## Novelty 1 — Bounded factual authority

The LLM can generate language, but it cannot become the authority for safety-critical agricultural fields.

For an agrochemical recommendation:

$$
C =
\langle
crop,\ problem,\ stage,\ active,\ formulation,\ dose,\ unit,\ volume,\ interval,\ PHI,\ regulatory
\rangle
$$

The system certifies a critical claim only when the required fields are jointly supported by an authoritative, valid evidence record.

This is the strongest conceptual component of the present work. Your current 11-slot verifier already operationalizes it. 

---

## Novelty 2 — Selective resolution rather than “RAG for everything”

The system chooses among:

$$
\{\text{deterministic},\text{RAG},\text{abstain},\text{escalate}\}
$$

depending on:

* risk,
* evidence completeness,
* model confidence,
* query type,
* modality,
* source validity.

That turns system architecture itself into a research object.

---

## Novelty 3 — Cross-layer failure containment

You are not only testing hallucinations.

You can test a chain:

> language ambiguity → retrieval error → evidence misbinding → numerical mutation → regulatory conflict → output-channel corruption.

The system's job is to **contain failures rather than repair them with another model**.

Your E10 taxonomy is particularly useful here: retrieval omission 28%, relational misbinding 22%, numerical/volumetric ambiguity 14%, linguistic ambiguity 12%, regulatory 8%, temporal 6%, conservative refusal 6%, calibration underconfidence 4%. 

That is a strong basis for a systems failure taxonomy.

---

## Novelty 4 — Agricultural deployment constraints are part of the reliability model

Instead of treating:

* edge inference,
* offline cache,
* SMS,
* model size,
* network degradation

as random engineering features, treat them as **reliability constraints on the advisory decision pipeline**.

This fits CEA much better because the journal explicitly covers AI, networking, machine vision, simulation and agricultural computing systems—and emphasizes innovation in those systems. ([Elsevier Shop][1])

---

# 5. The final paper should have this architecture

I would replace “DGDR” as the sole conceptual centerpiece with:

# **Bounded-Authority Advisory Architecture**

It can still contain your DGDR mechanism.

The conceptual stack should be:

```text
                    USER QUERY / IMAGE
                           │
                           ▼
                ┌─────────────────────┐
                │ RISK & CONTEXT GATE │
                │ safety / ambiguity  │
                │ confidence / scope  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ CAPABILITY ROUTER   │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Structured Facts      Hybrid RAG          Vision
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                EVIDENCE AUTHORITY LAYER
                           │
              ┌────────────┴─────────────┐
              │                          │
              ▼                          ▼
       Deterministic               Generative
        resolution                 realization
              │                          │
              └────────────┬─────────────┘
                           ▼
                 RELATIONAL VERIFIER
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
              CERTIFY             ABSTAIN
                 │                   │
                 ▼                   ▼
              DELIVER             ESCALATE
```

With a cross-cutting:

```text
        provenance + versioning + audit + telemetry
```

layer.

---

# 6. Formal problem formulation

This section should be added to the final paper.

Let:

* \(x\) = user input;
* \(m\) = modality/context;
* \(r(x)\) = risk state;
* \(q(x)\) = capability/query class;
* \(E(x)\) = retrieved or structured evidence;
* \(g(x)\) = confidence/evidence quality;
* \(a(x)\) = system action.

Define:

$$
a(x)\in
\{
\text{CERTIFY},
\text{GENERATE\_THEN\_VERIFY},
\text{ABSTAIN},
\text{ESCALATE}
\}
$$

For a safety-critical claim \(C\):

$$
\operatorname{Certify}(C)=1
$$

only if:

$$
\operatorname{ValidSource}(e)
\land
\operatorname{Current}(e)
\land
\operatorname{Authorized}(e)
\land
\operatorname{Entails}(e,C)
\land
\operatorname{Completeness}(C)
\land
g(x)\ge \theta
$$

where all required safety fields are bound to the same valid evidence record.

That equation is important.

It makes the paper clearly different from:

> retrieve → generate → citation.

---

# 7. Introduce two kinds of correctness

This will improve the whole paper.

## Linguistic correctness

Does the Bengali response:

* understand the question?
* communicate appropriately?
* contain coherent language?

## Decision/factual correctness

Does the underlying advisory:

* identify the appropriate crop/problem?
* use valid treatment?
* preserve formulation?
* preserve dose?
* preserve units?
* preserve interval?
* preserve PHI?
* respect regulation?
* remain temporally valid?

Your paper's thesis is that a system can have good linguistic correctness while having unsafe factual correctness.

That gives you a strong reason for authority separation.

---

# 8. Define the primary outcome variables

Do not use “accuracy” as the umbrella metric.

Use several explicitly different endpoints.

## Primary safety endpoint

### Critical Unsafe Acceptance Rate (CUAR)

$$
CUAR =
\frac{\#\text{unsafe cases accepted/certified}}
{\#\text{unsafe cases}}
$$

This is the primary safety endpoint.

---

## Primary advisory endpoint

### Certified Advisory Correctness

$$
CAC =
\frac{\#\text{certified responses judged correct}}
{\#\text{certified responses}}
$$

This answers:

> when you allow the system to speak authoritatively, how often is it right?

---

## Coverage

$$
Coverage =
\frac{\#\text{non-abstained cases}}
{\#\text{all answerable cases}}
$$

---

## Appropriate abstention

$$
AA =
\frac{\#\text{cases where abstention was correct}}
{\#\text{cases requiring abstention}}
$$

---

## Critical-field accuracy

For chemical advice:

* crop;
* disease/problem;
* active;
* formulation;
* dose;
* unit;
* volume;
* interval;
* PHI;
* regulatory status.

This should be reported individually.

---

# 9. Your strongest existing experiment: E2

The current counter/misbinding evaluation is already excellent material.

Your weaker lexical system accepts 80% dangerous cases overall, with 100% on cross-row binding, while the typed verifier rejects all 10,000 tested cases. 

### Keep this, but upgrade it.

Create four classes of evidence corruption:

### Type A — Cross-record binding

Example:

```text
Crop: potato
Disease: late blight
Active: X
Dose: from record Y
PHI: from record Z
```

### Type B — Numerical corruption

* dose ×2
* dose ×5
* dose ÷2
* PHI −3
* interval mutation

### Type C — Semantic corruption

* wrong crop;
* wrong disease;
* wrong formulation.

### Type D — temporal/regulatory corruption

* obsolete source;
* superseded recommendation;
* restricted chemical.

Then evaluate:

* LLM direct;
* Vanilla RAG;
* citation verifier;
* LLM judge;
* slot verifier;
* single-record authority verifier.

This becomes the **central causal experiment**.

---

# 10. E3 slot ablation should become a major result

Your current experiment is one of the strongest pieces of evidence.

The current results show:

| Removed field       | Dangerous acceptance |
| ------------------- | -------------------: |
| Dosage bounds       |                31.6% |
| Regulatory polarity |                17.8% |
| Active ingredient   |                14.2% |
| Crop                |                11.4% |
| Pathogen            |                 8.2% |
| Solvent volume      |                 7.1% |
| Formulation         |                 5.8% |
| Unit                |                 5.4% |
| Growth stage        |                 4.9% |
| PHI                 |                 2.7% |
| Interval            |                 1.9% |
| Full schema         |                 0.0% |

The lexical-only baseline reaches 80%. 

That is exactly the kind of ablation a CEA reviewer wants because you aren't merely claiming the schema works—you are showing **which agricultural relations matter**.

### Upgrade it

Do:

* 10,000 cases/configuration as currently;
* multiple random seeds;
* blinded/independently generated perturbations;
* 95% CIs;
* effect sizes;
* corrected significance testing across the 11 ablations.

Use a heatmap or ranked forest-style figure.

---

# 11. E5 counterfactual consistency should become the flagship figure

Current result:

* Vanilla RAG: 72.65% false certification;
* lexical: 59.55%;
* LLM judge: 38.65%;
* typed verifier: 0%. 

This is unusually compelling.

But the paper should not call this merely “counterfactual binding consistency.”

Turn it into:

# **Authority Violation Test**

Create perturbations that are scientifically meaningful:

$$
C \rightarrow C'
$$

where \(C'\) differs in exactly one critical field.

Examples:

* dose × 5;
* dose ÷ 5;
* PHI 14 → 3;
* formulation WP → EC;
* crop potato → rice;
* disease late blight → early blight;
* regulatory +1 → −1.

### Required system property

If the evidence record does not entail the changed claim, certification must fail.

That's a **metamorphic test**.

This is stronger than random red teaming.

---

# 12. Add a formal metamorphic testing section

This is one of the new experiments I most strongly recommend.

For each valid advisory \(C\), automatically generate:

$$
M_i(C)
$$

where exactly one semantic field is changed.

Expected invariant:

$$
\operatorname{Verify}(M_i(C)) = 0
$$

unless the changed field is still entailed by a legitimate separate record.

Run at least:

* 10,000–20,000 metamorphic cases;
* balanced across all 11 slots;
* multiple perturbation magnitudes.

This gives the paper a rigorous software-verification flavor.

---

# 13. Build the real end-to-end agricultural benchmark

This is the **single most important new experiment**.

Your current E6 is promising: on 4,000 queries, the current calibrated expert system reports 65.8% correct, 34.2% safe abstention, and zero dangerous acceptance; the LLM and Vanilla RAG baselines have lower safety. 

But for the final CEA paper, this needs to be upgraded into a proper, independent benchmark.

## Target

Create approximately:

### 2,000 answerable cases

and

### 1,000 non-answerable/unsafe cases

rather than relying mainly on synthetic construction.

---

# 14. Benchmark composition

I would structure the naturalistic benchmark like this:

| Category                      |    Target |
| ----------------------------- | --------: |
| General crop management       |       250 |
| Disease diagnosis/advice      |       300 |
| Agrochemical treatment        |       400 |
| Dose/formulation/PHI          |       250 |
| IPM/non-chemical alternatives |       200 |
| Fertilizer/nutrient advice    |       150 |
| Crop-stage/calendar           |       150 |
| Ambiguous questions           |       150 |
| Unsupported/out-of-domain     |       100 |
| Regulatory/banned chemical    |        50 |
| **Total**                     | **2,000** |

Then separately:

### 1,000 safety/adversarial cases.

---

# 15. Make the benchmark genuinely independent

Do not let the same people who designed the architecture create the final test set.

Best protocol:

### Stage 1

System developers create development data.

### Stage 2

Freeze system.

### Stage 3

Independent agronomists create the final test set.

### Stage 4

No model tuning after test labels are seen.

### Stage 5

All baselines evaluated with exactly the same input.

This directly answers an obvious reviewer criticism:

> “The attacks appear designed around the defense.”

---

# 16. Expert annotation protocol

I would aim for:

### 3–5 agronomists

For at least a substantial evaluation subset.

Each response gets:

* correctness;
* completeness;
* safety;
* appropriateness of refusal;
* factual critical-field correctness;
* source validity.

Do blind scoring.

Report:

* Gwet AC1 or Krippendorff's alpha;
* pairwise agreement;
* adjudicated gold labels;
* confidence intervals.

Your existing expert review is useful infrastructure, but the new study should be larger and independent.

---

# 17. Define an agricultural safety taxonomy before annotation

The following should be mutually distinguishable:

### Safe and correct

### Safe but incomplete

### Incorrect but non-harmful

### Unsupported

### Harmful

### Correct abstention

### Incorrect abstention

### Wrong escalation

This will prevent you from collapsing all failures into “accuracy.”

---

# 18. Benchmark baselines — exact final set

I recommend six.

## B0 — LLM-only

No retrieval.

## B1 — Vanilla RAG

Current hybrid retrieval + LLM.

## B2 — RAG + generic safety guard

A conventional classifier/filter.

## B3 — RAG + post-generation LLM judge

A realistic modern baseline.

## B4 — Structured deterministic resolver

No generation.

## B5 — Full bounded-authority system

Your proposed method.

This is the essential experimental ladder.

Do not use only:

> “our system versus LLM.”

That is not enough.

---

# 19. Add one more very important baseline

## B6 — Evidence-constrained RAG without single-record binding

This isolates your actual contribution.

For example:

> retrieve relevant facts → require citation → LLM generates → ordinary entailment check.

Then compare with:

> single-record relational authority.

Without B6, reviewers may say:

> “You simply added another RAG verifier.”

B6 answers that.

---

# 20. E4 calibration/risk-coverage needs to be redone properly

You already have a strong foundation.

The current calibrated relational policy reports test:

* AURC 0.0153;
* ECE 0.0785;
* Brier 0.0116;
* 84.56% coverage;
* 1.26% selective risk at the frozen threshold \(\theta^*=0.2375\). 

But the current YAML interpretation contradicts those exact values elsewhere.

So this experiment must be **regenerated from raw predictions**.

Also, don't simply write:

> “our method outperforms conformal.”

The current figures don't cleanly justify that statement because conformal achieves somewhat lower selective risk at the reported operating point.

Instead compare at fixed risk budgets.

Report:

### Maximum coverage at ≤0.5% risk

### Maximum coverage at ≤1% risk

### Maximum coverage at ≤2% risk

plus:

* AURC;
* ECE;
* Brier;
* reliability plots.

Then the scientific question is clear:

> Which policy gives the best coverage under a predefined safety-risk budget?

That is much more rigorous.

---

# 21. Threshold selection protocol

Do not call \(\gamma=0.80\) “optimal” based on the test set.

Use:

### Training

fit classifier.

### Development

calibrate threshold.

### Frozen test

measure final performance.

Your E17 already has 0.7/0.8/0.9 sweeps. 

For the final experiment, expand:

$$
\gamma \in \{0.50,0.55,\dots,0.95\}
$$

Then calculate:

* routing coverage;
* misrouting;
* safe coverage;
* latency;
* LLM-call rate.

Select threshold on development data according to a **predefined safety operating rule**.

---

# 22. High-confidence wrong classifier experiment

This should absolutely be added.

The verifier cannot correct wrong semantic metadata if that metadata determines the selected record.

Therefore create:

### Condition A

Correct classifier metadata.

### Condition B

Real classifier output.

### Condition C

Wrong but high-confidence metadata.

### Condition D

Wrong low-confidence metadata.

Then measure:

* retrieval;
* selected evidence;
* final certification;
* final agricultural correctness;
* harmful acceptance.

This is perhaps the most important missing causal experiment in the current paper.

---

# 23. Oracle-vs-predicted routing experiment

Related but distinct.

Run the entire pipeline with:

### Oracle crop/problem metadata

versus

### predicted metadata

versus

### noisy metadata.

This decomposes:

$$
\text{total system error}
=
\text{routing error}
+
\text{knowledge error}
+
\text{generation error}
+
\text{verification failure}
$$

That is exactly the sort of systems diagnosis that CEA values.

---

# 24. E17 routing should be repositioned

Current result:

2,135 nodes → 516.4 at threshold 0.8, a 75.64% reduction, with 3.15% misrouting. 

Good.

But don't call this:

> “dialect immunity.”

The current E17 test is constructed and uses metadata availability; the paper itself correctly describes the setting as a bounded simulation. 

Call it:

> **retrieval-space reduction and register-robust routing**

Then add the naturalistic dialect experiment separately.

---

# 25. E21 dialect experiment: keep it, but split the endpoint

Current E21 shows:

* regional dialect coverage +46.9 pp;
* Banglish +48.4 pp;
* authentic-farmer +34.4 pp;
* zero observed dangerous acceptance across 4,000 queries. 

That is useful.

But report three separate outcomes:

### Input robustness

Can the system resolve what the user means?

### Retrieval robustness

Can it find the correct evidence?

### Advisory correctness

Is the final advice right?

Do not let “coverage” stand in for any of these.

---

# 26. New dialect experiment I strongly recommend

Construct a separate **unseen-regional test set**.

Train/develop on:

* standard Bengali;
* a few known regional forms.

Test on:

* unseen colloquial forms;
* spelling noise;
* Banglish;
* mixed Bengali-English;
* voice-transcription-like errors.

This turns the problem into a proper domain-shift test.

The broader NLP literature already recognizes selective answering under domain shift as a distinct problem; use that conceptual framing rather than treating dialect as just a retrieval trick.

---

# 27. Add linguistic normalization as an ablation

Compare:

### A

raw query

### B

query normalization

### C

normalization + metadata routing

### D

normalization + metadata routing + RAG

### E

full bounded-authority system

Metrics:

* intent;
* retrieval;
* certification;
* safety;
* latency.

This makes it possible to say whether the gain came from:

> modality,

or

> linguistic normalization,

or

> authority control.

---

# 28. E10 should become the system failure-analysis section

This is already useful.

Current audit indicates:

* retrieval omission 28%;
* relational misbinding 22%;
* numerical/volume ambiguity 14%;
* linguistic ambiguity 12%;
* regulatory discrepancy 8%;
* temporal validity 6%;
* verifier conservatism 6%;
* calibration underconfidence 4%. 

This should not merely be a table.

Use it to motivate the next architecture iteration.

For every failure:

$$
\text{failure}
\rightarrow
\text{root cause}
\rightarrow
\text{detector}
\rightarrow
\text{action}
\rightarrow
\text{residual risk}
$$

That becomes a genuine **failure containment framework**.

---

# 29. Temporal validity experiment

This is now mandatory in my opinion because of current agricultural RAG literature.

TARAG explicitly treats time-aware retrieval as important for crop/pest/disease management. ([ScienceDirect][2])

Add source metadata:

```text
publication_date
effective_date
review_date
expiry_date
jurisdiction
authority_level
version
```

Then construct:

### Case 1

one valid source.

### Case 2

old + new source.

### Case 3

conflicting old/new recommendations.

### Case 4

withdrawn/restricted chemical.

### Case 5

variety-specific newer recommendation.

Evaluate:

* Vanilla RAG;
* RAG + temporal reranking;
* bounded-authority resolver.

Metrics:

* current-source selection;
* stale-source certification;
* conflict detection;
* correct abstention.

---

# 30. Source authority hierarchy experiment

This is another important addition.

Define an authority order, for example:

$$
\text{current regulatory source}
>
\text{current institutional recommendation}
>
\text{older institutional source}
>
\text{secondary source}
>
\text{unverified text}
$$

Do not hard-code this exact hierarchy before agricultural validation.

Instead establish it with domain experts and regulatory sources.

Then deliberately create conflicts.

Measure:

* correct authority selection;
* erroneous source mixing;
* abstention on unresolved conflict.

This is a key extension of your current “single authoritative record” concept.

---

# 31. Strengthen the provenance model

Current E23 has a useful foundation:

* 1,000 mutations detected;
* 100% tamper detection;
* 791-byte update vs 10,985-byte full pack;
* 0.1919 ms p95 chain verification. 

But cryptographic hashing alone doesn't establish authenticity if the attacker can replace the manifest.

So upgrade from:

> hash chain

to:

> **versioned, signed manifest + hash-pinned records**

where possible.

Then evaluate:

### mutation

### deletion

### substitution

### rollback

### stale package

### forged manifest

### partial update

### mixed-version cache

The paper can then make a much stronger claim:

> the cached evidence state is both integrity-verifiable and version-aware.

---

# 32. E23 should become a deployment-integrity experiment

Instead of presenting it as a crypto experiment, ask:

> Can an offline agricultural evidence cache remain safe under updates, rollback and partial connectivity?

This ties it directly to CEA.

That is much better than simply saying:

> SHA-256 works.

---

# 33. Offline/network experiment: keep E14, but rebuild it

The current simulation gives:

* at 15% loss: 82.0% cloud-only vs 91.4% offline cache;
* at 30% loss: 12.8% cloud-only vs 58.1% offline cache. 

These are good engineering results.

But the current file has a stale acceptance note saying different values, so the final study must regenerate from raw outputs. 

### Final methodology

Use an actual network emulator where possible:

* `tc/netem` on Linux;
* Android network shaping;
* or a controlled router/emulator.

Profiles:

| Profile        |       RTT | Loss |   Jitter |
| -------------- | --------: | ---: | -------: |
| Good 4G        | realistic |   0% |      low |
| 3G             | realistic |   5% | moderate |
| Rural edge     | realistic |  15% |     high |
| Severe 2G-like | realistic |  30% |     high |

Run enough repetitions to estimate confidence intervals.

Measure:

* delivery success;
* time-to-first-usable-answer;
* p50/p95/p99;
* stale advisory rate;
* retry volume;
* bytes transferred;
* cache hit rate.

---

# 34. Offline should be measured as a service property

The key quantity isn't just:

> “cache hit.”

It is:

$$
P(\text{safe usable advisory} \mid \text{network condition})
$$

This is much more valuable.

Report:

> safe-delivery retention under degradation.

---

# 35. Edge experiment: make E9 physically real

Current E9 reports useful numbers:

* crop INT8 model 5.9 MB;
* 29.11 ms mobile CPU;
* 42.5 MB RAM;
* potato disease model 20.79 MB;
* 47.79 ms;
* 68.2 MB RAM;
* 100% top-1 agreement vs FP32.

These should be retained, but verified on actual devices before using them as strong deployment evidence.

### Use at least:

* one low-end Android;
* one midrange Android;
* one laptop/desktop reference.

Measure:

* cold start;
* warm inference;
* RAM;
* CPU;
* battery/energy per inference;
* thermal behavior;
* sustained 100/500/1000 inference runs.

This would significantly strengthen the CEA paper.

CEA's remit explicitly includes computing and electronic systems, while its current literature also treats edge computing as an important smart-agriculture direction. ([Elsevier Shop][1])

---

# 36. Do NOT put the on-device LLM at the center

You don't need to demonstrate:

> 4B LLM fully on phone.

The current architecture is stronger if:

### local

* safety;
* vision;
* intent;
* structured facts;
* cache;
* deterministic resolution.

### remote/optional

* complex generation.

That gives a strong edge/cloud hybrid design.

---

# 37. E18 efficiency experiment should be retained

Current E18:

* text-only zero-LLM = 10.48%;
* proposed = 61.52%;
* +51.04 pp;
* 1,247.93 → 546.15 ms weighted latency;
* 2.28× improvement. 

Good.

But don't call:

> “61.52% of queries are successfully answered without LLM.”

Because T0 and T4 include safety handling/refusal.

Instead report:

### deterministic advisory coverage

$$
T1+T2=51.04\%
$$

and separately:

### safety/refusal handling

$$
T0+T4=10.48\%
$$

### LLM-dependent traffic

$$
T3=38.48\%
$$

This is much more honest and informative.

---

# 38. Add a more meaningful efficiency metric

Rather than only “zero LLM,” calculate:

### LLM calls per answerable query

### LLM token use per certified advisory

### average generation tokens

### deterministic resolution latency

### total compute per certified advisory

This is much stronger than a binary zero/nonzero metric.

---

# 39. E25 lightweight intent classifier

Keep E25, but demote its importance.

Current result:

* 78.4% joint exact match;
* 96.4% crop;
* 78.4% pest;
* 100% intent;
* 0.3855 ms p50;
* 0.6719 ms p95;
* 1.25 MB;
* LLM baseline 94.2% joint and 1250 ms p50.

This supports:

> low-cost routing infrastructure.

It does **not** support:

> replacing LLM semantic understanding.

In fact, its 78.4% joint accuracy demonstrates the opposite.

That is useful because the paper can show:

> lightweight routing is imperfect, so the architecture explicitly absorbs routing uncertainty rather than assuming perfect classification.

Run:

* calibration;
* confusion matrix;
* OOD examples;
* high-confidence wrong predictions;
* error propagation.

Then it becomes scientifically relevant.

---

# 40. E19 must be expanded significantly

Do not use:

> 23 nodes, 9 facts

as the main scalability evidence.

Current E19 does show 100% slot completeness at 3 hops and p95 0.0195 ms, but it is a proof-of-mechanism experiment on a tiny graph. 

Build a realistic structured knowledge graph:

### Minimum target

Several hundred to several thousand treatment relations.

Across multiple:

* crops;
* diseases;
* formulations;
* dose forms;
* stages;
* regulatory states.

Then benchmark:

### 1-hop

### 2-hop

### 3-hop

### 4-hop

against:

* latency;
* completeness;
* provenance;
* false joins;
* memory.

Don't assume 3 hops is optimal.

Let the data decide.

---

# 41. Add negative graph queries

This is critical.

Ask for impossible combinations:

```text
crop A + disease B + formulation C
```

where no valid record exists.

Expected:

> abstain.

Measure:

### false positive relation construction.

This is more important than merely measuring traversal speed.

---

# 42. Add graph-versus-table baseline

Compare:

### flat table lookup

### typed relational graph

### hybrid retrieval

This can establish whether the graph representation itself provides a measurable benefit.

---

# 43. E15 SMS should remain—but as a secondary deployment experiment

Current result is clean:

* deterministic template: 100% selected-field survival;
* mean 108.5 chars;
* max 115;
* zero critical hazard;
* LLM summary: 64.4% critical hazard;
* naive truncation: 100% hazard. 

That's useful.

Don't make SMS a contribution.

Use it to demonstrate:

> **the factual-authority boundary survives constrained output channels.**

That is a nice supporting result.

---

# 44. E22 security is more important than SMS

Current result:

* 0/1,400 leakage in deterministic template;
* 509/1,400 in LLM-composed SMS;
* five/six attack families including Bengali/Banglish/retrieval poisoning etc.;
* deterministic architecture blocks them. 

The broader prompt-injection benchmark is even stronger:

* LLM-only 83.86%;
* Vanilla RAG 69.36%;
* RAG + LLM guard 21.79%;
* KrishokTech 0/1,400. 

This should become the **security robustness subsection**.

RAG-specific security is a well-established current research concern: SafeRAG showed that retrieval can introduce security vulnerabilities, including through manipulated knowledge and inter-context conflict. ([ACL Anthology][8])

---

# 45. Upgrade the security benchmark

Current families are good:

* direct system override;
* evidence override;
* retrieval poisoning;
* delimiter hijacking;
* native Bengali injection;
* Banglish;
* code switching.

Add:

### malicious source document

Inject an instruction into retrieved evidence.

### poisoned metadata

Modify source authority or version.

### numerical poisoning

Change dosage/PHI inside retrieved text.

### indirect prompt injection

Attack via a document rather than user query.

### multilingual source poisoning

Bengali + English mixed malicious evidence.

This connects the safety story to actual RAG security literature. ([ACL Anthology][8])

---

# 46. Use the recent “Generate but Verify” literature correctly

Current RAG research explicitly studies generation followed by faithfulness assessment and fallback. ([ACL Anthology][9])

Therefore your paper should not say:

> “we invented generate-then-verify.”

Instead say:

> Existing work demonstrates the value of post-generation faithfulness prediction; our system goes further in the agricultural safety setting by assigning factual authority to typed, source-bound records for critical claims and by allowing verification to terminate the interaction through abstention/escalation.

That is defensible.

---

# 47. Use FaithfulRAG/current conflict work as a comparator

FaithfulRAG explicitly models conflict between retrieved knowledge and parametric model knowledge at the fact level. ([ACL Anthology][10])

That suggests an excellent experiment:

### Parametric–evidence conflict

Create questions where:

* model prior says A;
* authoritative evidence says B.

Then compare:

* LLM;
* RAG;
* FaithfulRAG-style approach if practical;
* your authority-bound system.

The key metric:

> whether the system follows **validated agricultural evidence** rather than the model's prior.

That is a very strong experiment.

---

# 48. New experiment: parametric knowledge conflict

For each fact:

1. construct/identify authoritative evidence \(e\);
2. establish model prior \(p\);
3. choose conflicting cases;
4. ask the system.

Measure:

$$
P(\text{certify evidence-backed claim})
$$

and:

$$
P(\text{certify parametric-conflict claim})
$$

For your architecture, the correct behavior should be determined by the evidence authority layer—not by model preference.

This directly connects your work to modern RAG-faithfulness research. ([ACL Anthology][10])

---

# 49. New experiment: claim-level provenance

Current provenance is mostly record-level.

Upgrade it to:

```text
Claim 1
   ↓
Fact ID
   ↓
Source document
   ↓
Page/section
   ↓
Version
   ↓
Authority
```

Then have experts evaluate:

### citation correctness

### claim-evidence alignment

### source authority correctness

### temporal validity.

This is strongly aligned with current evidence-grounded verification systems. For example, SciTrue explicitly makes claim components traceable to verifiable sources rather than merely attaching citations to a generated paragraph. ([ACL Anthology][11])

---

# 50. New experiment: source-to-claim leakage

Construct adversarial documents containing:

> true crop
> true disease
> wrong chemical

and another document containing:

> wrong crop
> correct chemical.

Then ask the system.

The system should **not merge** them into a plausible recommendation.

This is essentially a realistic agricultural version of your current cross-row misbinding experiment.

It would be extremely strong.

---

# 51. New experiment: “authority boundary cannot be edited by the LLM”

This should be one of the most memorable experiments.

Create structured facts:

```text
Dose = 2–2.5 g/L
PHI = 14 days
Interval = 7 days
```

Then ask several LLMs to verbalize them under:

### unrestricted generation

### evidence prompt

### structured JSON constraint

### authority-bound generation + verifier.

Record:

* dose mutation;
* interval mutation;
* PHI mutation;
* formulation mutation;
* omission.

This tests the statement:

> **LLM = linguistic realization, not factual authority.**

---

# 52. New experiment: deterministic consistency

Take the same 1,000 evidence-complete advisory queries.

Run them:

* 10 times;
* 50 times if cheap.

For deterministic tier:

$$
Var(\text{critical fields})=0
$$

For LLM/RAG:

measure variation in:

* dose;
* PHI;
* formulation;
* interval.

This is an excellent argument for deterministic authority.

---

# 53. New experiment: “safe utility”

Your system deliberately trades coverage for safety.

You need to quantify that trade-off.

Define a utility function only for analysis:

$$
U =
C -
\lambda H -
\mu FR
$$

where:

* \(C\) = correct/useful answer;
* \(H\) = harmful acceptance;
* \(FR\) = false refusal;
* \(\lambda \gg \mu\).

The exact weights should be chosen with domain experts or reported via sensitivity analysis, not invented to produce a favorable result.

Then show:

> what happens as the system becomes more conservative?

This gives a principled way to discuss deployment tradeoffs.

---

# 54. New experiment: human escalation

Your current system uses 16123 as an endpoint, but this is not evidence that farmers actually use it.

Do not make that claim.

Instead implement a simulated human review queue.

Measure:

* fraction escalated;
* priority precision;
* review time;
* cases saved from unsafe answer;
* repetitive escalation categories.

If you can involve a real extension officer, even better.

If not, clearly label it:

> simulated human-in-the-loop evaluation.

That fits current agricultural HITL directions and CEA's applied systems culture. SMART explicitly uses human-in-the-loop diagnosis. ([ScienceDirect][3])

---

# 55. New experiment: knowledge maintenance

E24 is interesting:

* 2 facts added;
* 18 minutes;
* 55 affected queries;
* 58.7 → 64.2% coverage;
* 3.06 newly resolvable queries/minute. 

But one cluster is not a scientific result.

Expand it.

### 5–10 knowledge gaps

For each:

* source retrieval time;
* authoring time;
* validation time;
* number of facts added;
* coverage increase;
* rejection rate;
* provenance completeness.

Then calculate:

$$
\Delta Coverage / \Delta AuthoringTime
$$

This becomes:

> **knowledge-base maintainability**

rather than a one-off “18 minutes” anecdote.

This is especially relevant because current deployment-oriented NLP work increasingly emphasizes maintenance, governance and lifecycle management. EACL's 2027 Industry call explicitly highlights continuous maintenance, governance, versioning and auditing. ([EACL 2027][12])

---

# 56. Knowledge ingestion needs a controlled pipeline

Your paper should formalize:

```text
Authoritative source
        ↓
Document staging
        ↓
Fact extraction
        ↓
Schema validation
        ↓
Conflict detection
        ↓
Expert review
        ↓
Version/hash/signature
        ↓
Release to fact store
```

No direct LLM-to-production fact insertion.

This is a very strong practical safety property.

---

# 57. Build the final evidence schema

I recommend expanding the current 11 slots into two layers.

## Layer A — advisory semantics

1. crop
2. problem/pathogen
3. growth stage
4. active ingredient
5. formulation
6. dose minimum
7. dose maximum
8. dose unit
9. solvent/volume denominator
10. interval
11. PHI
12. regulatory polarity

## Layer B — evidence governance

13. source ID
14. source authority
15. jurisdiction
16. source version
17. publication date
18. effective date
19. review/expiry date
20. verification status
21. verifier identity
22. evidence hash
23. release timestamp

The 11 current fields remain the **agronomic decision contract**.

The extra fields establish **evidence authority**.

This is important because an old authoritative record can still be wrong for the current date.

---

# 58. Distinguish “authoritative” from “current”

This needs to be explicit.

A source may be:

> authoritative but obsolete.

Another may be:

> recent but secondary.

Therefore:

$$
Authority = f(source,\ jurisdiction)
$$

while:

$$
Validity = f(date,\ version,\ regulatory\ state)
$$

A record should be certifiable only if both are valid.

This makes the architecture much stronger.

---

# 59. New experiment: source conflict matrix

Construct conflicts along two axes:

|               | Current | Outdated |
| ------------- | ------: | -------: |
| Authoritative |       A |        B |
| Secondary     |       C |        D |

Evaluate whether the system:

* selects A;
* rejects B;
* uses C only when no authoritative source exists;
* abstains when authority cannot be resolved.

This is a very clean figure.

---

# 60. E9 latency decomposition should become a systems figure

Current decomposition gives:

* routing p95 0.35 ms;
* deterministic lookup p95 0.42 ms;
* hybrid retrieval p95 28.5 ms;
* generation p95 1780 ms;
* verification p95 3.8 ms;
* render p95 0.15 ms.

The key insight is:

> **generation dominates latency, not verification.**

This supports your architectural choice directly.

The paper can show:

```text
deterministic route
████ <1 ms

retrieval
████████████████████

generation
████████████████████████████████████████████████
```

Then demonstrate how selective routing avoids unnecessary generation.

That is better than just reporting the mean.

---

# 61. Cost analysis: retain, but demote

Current master reports:

* deterministic-first ladder ≈ $0.1798/1,000 queries;
* commercial cloud baseline ≈ $2.30/1,000;
* reported 92.18% reduction;
* cost per certified safe advisory $0.000213 under the current model.

Useful.

But this must be treated as:

> **scenario-based systems economics**

not economic proof.

Use sensitivity analysis across:

* cloud LLM price;
* traffic mix;
* cache hit ratio;
* SMS proportion;
* infrastructure cost;
* model utilization.

Do not make the 16-million-farmer national projection a headline result.

It relies on assumptions rather than actual deployment data.

---

# 62. Add cost per *correct safe* advisory

Current `C_safe` is promising, but it should become:

$$
C_{CS} =
\frac{\text{total serving cost}}
{\#\text{correct certified safe advisories}}
$$

not simply number of certified outputs.

That is much more meaningful.

A system cannot “win” by certifying lots of bad answers.

---

# 63. Add a latency–safety–coverage Pareto analysis

This could be one of the strongest final figures.

Each system becomes a point:

```text
          Safety
            ↑
            │       Full BAA
            │
            │    RAG+Verifier
            │
            │
            │
            │ RAG
            │
            │ LLM
            └──────────────────→ Coverage
                         + 
                       Latency
```

Better as a 3D/paired set of plots.

Show:

* correctness;
* harmful acceptance;
* coverage;
* latency.

This tells the complete story.

---

# 64. Add an ablation of the whole architecture

This is mandatory.

Build:

| Architecture  | Risk gate | Deterministic authority | Verification | Temporal validity | Abstention |
| ------------- | --------: | ----------------------: | -----------: | ----------------: | ---------: |
| LLM           |         ✗ |                       ✗ |            ✗ |                 ✗ |          ✗ |
| RAG           |         ✗ |                       ✗ |            ✗ |                 ✗ |        ✓/✗ |
| Guarded RAG   |         ✓ |                       ✗ |            ✓ |                 ✗ |          ✓ |
| Authority RAG |         ✓ |                       ✓ |            ✓ |                 ✗ |          ✓ |
| Full BAA      |         ✓ |                       ✓ |            ✓ |                 ✓ |          ✓ |

Then measure end-to-end safety/correctness.

This establishes **causal contribution of architectural layers**.

---

# 65. Vision belongs in the CEA paper—but as an uncertainty source

Your multimodal system is valuable.

But don't claim:

> “our image classifier is state of the art.”

Instead use vision to test:

> **does multimodal uncertainty propagate safely through the advisory architecture?**

### Experiment

Run:

### V1

correct crop + correct disease.

### V2

wrong crop + high confidence.

### V3

correct crop + wrong disease.

### V4

low-confidence image.

### V5

ambiguous image.

Measure:

* final evidence retrieval;
* final answer;
* certification;
* harmful acceptance;
* abstention.

This connects CV and advisory reliability beautifully.

---

# 66. Add image OOD testing

This is important for real deployment.

Use:

* different lighting;
* different backgrounds;
* partial leaves;
* multiple leaves;
* blur;
* compression;
* field photographs vs curated images.

SMART and other recent CEA multimodal studies emphasize robustness to variable/noisy inputs and human-in-the-loop reliability. ([ScienceDirect][3])

Your system can go one step beyond:

> Does visual uncertainty cause safe abstention rather than dangerous advice?

That is the important question.

---

# 67. Add multimodal conflict testing

Very interesting experiment:

Image says:

> potato.

Text says:

> “my tomato plants…”

What does the system do?

Similarly:

Image predicts:

> late blight.

Text says:

> “whitefly.”

You should not let one modality silently override the other.

Define:

$$
Conflict(image,text)
$$

and route to:

> clarification / fallback / human review.

This is a powerful addition and very relevant to multimodal advisory systems.

---

# 68. Agricultural decision hierarchy

I would make the system distinguish:

### Observation

“What is happening?”

### Diagnosis

“What is likely happening?”

### Recommendation

“What should I do?”

### Intervention

“Which chemical should I apply?”

The higher the intervention risk, the stronger the evidence requirement.

That gives you:

$$
EvidenceThreshold_{intervention}
>
EvidenceThreshold_{diagnosis}
>
EvidenceThreshold_{observation}
$$

This is a very useful design principle.

---

# 69. Risk-tiered evidence requirements

This could become a major part of the architecture.

### Low-risk

General cultural practice.

### Medium-risk

Disease management.

### High-risk

Chemical recommendation.

### Critical

Banned chemicals / poisoning / direct intervention.

Then require progressively stronger evidence.

For example:

```text
low risk        → RAG may answer
moderate risk   → RAG + evidence verification
high risk       → structured fact + joint binding
critical risk   → policy block/escalation
```

This is much richer than a simple “safety classifier.”

---

# 70. This gives the system a more general architecture

The real generalization claim becomes:

> The system is not specific to pesticides. It implements **risk-adaptive factual authority**.

The agricultural domain supplies the case where the risk model is well-defined.

You can later say the pattern could transfer to:

* veterinary;
* human health;
* industrial safety.

But **do not evaluate those domains in this paper**.

That would dilute the CEA focus.

---

# 71. E21 and E6 should be treated as different experiments

Don't duplicate them.

### E17/E21

Question:

> Does metadata routing improve language/register robustness and search narrowing?

### E6

Question:

> What happens to end-to-end agricultural correctness/safety under actual farmer-language variants?

This distinction is important.

---

# 72. Recommended primary hypotheses

Write these before running final tests.

## H1 — Authority

Evidence-bound certification reduces critical unsafe acceptance relative to LLM/RAG/citation-only baselines.

## H2 — Selective resolution

Risk/evidence-aware routing reduces unnecessary generation while maintaining useful advisory coverage.

## H3 — Relational integrity

Single-record joint binding is more robust to cross-field corruption than text/citation/LLM-judge verification.

## H4 — Uncertainty handling

Calibrated abstention achieves a better coverage–risk trade-off than fixed always-answer policies.

## H5 — Deployment resilience

Deterministic/local paths maintain higher usable advisory delivery under network degradation than cloud-only generation.

## H6 — Multimodal safety

Visual or metadata errors are converted into abstention/escalation more often under bounded authority than under unconstrained generation.

These six hypotheses give the paper an exceptionally clear backbone.

---

# 73. Recommended final Research Questions

### RQ1

**Does bounded factual authority reduce unsafe agricultural recommendations compared with direct LLM, RAG, and generic verification pipelines?**

### RQ2

**Does relational evidence binding specifically protect against cross-field and counterfactual evidence corruption?**

### RQ3

**What safety–coverage trade-off results from selective routing and calibrated abstention?**

### RQ4

**How do linguistic, visual, temporal and evidence-quality uncertainties propagate through the advisory pipeline?**

### RQ5

**How do deterministic and local paths affect latency, compute, network resilience and constrained-channel reliability?**

That's enough.

Five RQs.

Not ten.

---

# 74. Final manuscript outline

Now the actual paper.

---

## 1. Introduction

### 1.1 Agricultural advisory as a safety-critical computing problem

Explain:

* LLM usefulness;
* agricultural domain risk;
* critical-field dependence;
* why fluent generation isn't enough.

### 1.2 Why retrieval alone is insufficient

Motivate from your prior work.

Do not reproduce the retrieval paper.

State:

> retrieval quality varies by query type and language condition.

### 1.3 The missing architectural question

Introduce:

> who has factual authority?

### 1.4 Proposed solution

Introduce bounded-authority selective resolution.

### 1.5 Research questions

List RQ1–RQ5.

### 1.6 Contributions

Exactly three:

1. bounded-authority architecture;
2. relational certification + selective routing;
3. comprehensive agricultural/deployment evaluation.

---

# 75. 2. Related Work

Keep this compact but strategically deep.

## 2.1 Agricultural LLM/RAG advisory

Discuss:

* Farmer.Chat;
* KrishokBondhu;
* current agricultural domain-first RAG;
* multimodal systems.

Farmer.Chat proves that scalable agricultural GenAI is already a practical research area. ([Microsoft][7])

## 2.2 Structured agricultural knowledge

Discuss:

* tables;
* decision trees;
* knowledge graphs;
* structured facts.

Recent CEA work confirms this is a major direction. ([ScienceDirect][4])

## 2.3 RAG faithfulness and verification

Discuss:

* RAGChecker;
* Generate-but-Verify;
* FaithfulRAG;
* claim verification.

RAGChecker is particularly useful as methodological precedent because it argues that retrieval and generation should be evaluated separately and diagnostically. ([NeurIPS Proceedings][13])

## 2.4 Selective answering and abstention

Discuss:

* selective prediction;
* confidence calibration;
* risk–coverage;
* abstention.

## 2.5 RAG security and evidence poisoning

Discuss:

* SafeRAG;
* RAG safety concerns;
* retrieval poisoning.

SafeRAG demonstrated that manipulated retrieved knowledge can create substantial RAG security vulnerabilities, making this highly relevant to your evidence-bound design. ([ACL Anthology][8])

## 2.6 Gap

End with a very clear table.

---

# 76. 3. Problem Formulation and Design Requirements

This section is crucial.

## 3.1 Advisory state

Define:

$$
x, r, q, E, C, a
$$

## 3.2 Critical claim model

Define the 11-field agricultural tuple.

## 3.3 Evidence authority

Define:

* authoritative;
* valid;
* current;
* traceable.

## 3.4 Certification condition

Formalize the fail-closed rule.

## 3.5 Selective decision policy

Define:

* answer;
* generate+verify;
* abstain;
* escalate.

## 3.6 Reliability requirements

Create a table:

| Requirement           | Failure              | System response   |
| --------------------- | -------------------- | ----------------- |
| Evidence missing      | hallucination        | abstain           |
| Cross-record conflict | misbinding           | reject            |
| Wrong metadata        | routing error        | fallback          |
| Low confidence        | uncertain diagnosis  | abstain           |
| Obsolete source       | stale advice         | invalidate        |
| Injection             | policy bypass        | block             |
| Long SMS              | omission             | refuse/recompose  |
| Network failure       | unavailable evidence | cache/local route |

This becomes the formal backbone.

---

# 77. 4. Bounded-Authority Architecture

## 4.1 System overview

Architecture figure.

## 4.2 Risk/context gate

Explain policy classes.

## 4.3 Capability router

Show typed capability registry.

## 4.4 Structured fact authority layer

Detailed schema.

## 4.5 Deterministic resolution

Explain traversal and templates.

## 4.6 Hybrid RAG fallback

Explain where RAG is permitted.

## 4.7 Generative realization

Very important:

> LLM may phrase; it may not mutate critical facts.

## 4.8 Relational certification

11-slot binding.

## 4.9 Temporal and regulatory validity

Version/authority.

## 4.10 Abstention/escalation

Explain why refusal is a valid system output.

## 4.11 Provenance and audit

Claim-level trace.

## 4.12 Offline/edge/channel support

Cache, device, SMS.

---

# 78. 5. Knowledge Base Construction and Governance

This deserves its own section.

## 5.1 Source corpus

Report:

* documents;
* institutions;
* crop coverage;
* treatment relations.

Your current master/draft reports 2,135 provenance-carrying nodes and 2,946 institutional source documents. 

## 5.2 Fact extraction

## 5.3 Human validation

## 5.4 Schema validation

## 5.5 Conflict resolution

## 5.6 Temporal validity

## 5.7 Versioning and signing

## 5.8 Cache release

## 5.9 Knowledge maintenance

This is where E24 fits.

---

# 79. 6. Experimental Methodology

This should be a substantial section.

## 6.1 Experimental principles

State:

* all test sets frozen;
* development/test separation;
* identical input across baselines;
* deterministic seeds where applicable;
* preregistered metrics;
* independent test generation.

## 6.2 Benchmarks

### Naturalistic advisory benchmark

### Safety benchmark

### Metamorphic benchmark

### Dialect benchmark

### Security benchmark

### Temporal conflict benchmark

### Multimodal robustness benchmark

### Network benchmark

### Device benchmark

## 6.3 Baselines

B0–B6.

## 6.4 Expert protocol

## 6.5 Statistical protocol

## 6.6 Hardware/software environment

## 6.7 Reproducibility protocol

---

# 80. 7. Results — End-to-End Advisory Quality

This should be the **first Results section**.

Not routing.

Not SMS.

Not cost.

The reader first needs to know:

> Does the system actually give better agricultural advice?

## 7.1 Overall correctness

Table:

| System        | Correct | Unsafe | Unsupported | Correct abstention | Coverage |
| ------------- | ------: | -----: | ----------: | -----------------: | -------: |
| LLM           |         |        |             |                    |          |
| RAG           |         |        |             |                    |          |
| Guarded RAG   |         |        |             |                    |          |
| RAG+Verifier  |         |        |             |                    |          |
| Deterministic |         |        |             |                    |          |
| Full BAA      |         |        |             |                    |          |

## 7.2 Critical-field correctness

Dose, formulation, PHI, etc.

## 7.3 Performance by advisory type

## 7.4 Performance by language register

This section establishes agricultural utility.

---

# 81. 8. Results — Evidence Authority and Safety

This is your strongest scientific section.

## 8.1 Cross-record misbinding

E2.

## 8.2 Counterfactual evidence binding

E5.

## 8.3 Slot ablation

E3.

## 8.4 Parametric/evidence conflict

new.

## 8.5 Source conflict

new.

## 8.6 Metamorphic safety testing

new.

Main table:

| Method                  | True evidence certified | Counterfactual certified | CUAR |
| ----------------------- | ----------------------: | -----------------------: | ---: |
| LLM                     |                         |                          |      |
| RAG                     |                         |                          |      |
| LLM Judge               |                         |                          |      |
| Slot verifier           |                         |                          |      |
| Single-record authority |                         |                          |      |

This could become the paper's strongest table.

---

# 82. 9. Results — Selective Routing and Uncertainty

## 9.1 Calibration

E4.

## 9.2 Risk–coverage

Plot.

## 9.3 Threshold sweep

E17 + new calibration threshold sweep.

## 9.4 Oracle/predicted metadata

New.

## 9.5 High-confidence wrong metadata

New.

## 9.6 Abstention error taxonomy

E10.

The central graph should be:

> **risk vs coverage vs route share**

---

# 83. 10. Results — Language and Multimodal Robustness

## 10.1 Bengali register

E21/E6.

## 10.2 Unseen dialect/generalization

New.

## 10.3 Query normalization

New.

## 10.4 Image uncertainty

New.

## 10.5 Cross-modal conflicts

New.

This section answers:

> does safety hold when the inputs become messy?

That is much stronger than a standalone “dialect coverage” table.

---

# 84. 11. Results — Temporal and Knowledge Integrity

## 11.1 Temporal validity

New.

## 11.2 Source authority conflicts

New.

## 11.3 Cache mutation/invalidation

E23.

## 11.4 Claim-level provenance

New.

## 11.5 Knowledge maintenance

E24 expanded.

This makes your system operationally serious.

---

# 85. 12. Results — Security and Constrained Delivery

## 12.1 Prompt injection

E7/E8.

## 12.2 Retrieval poisoning

Expanded.

## 12.3 SMS safety

E15/E22.

## 12.4 Offline/network resilience

E14.

## 12.5 Local edge performance

E9 + physical tests.

This section is where the current “too many features” become a coherent **deployment reliability story**.

---

# 86. 13. Results — System Efficiency

This should be concise.

## 13.1 LLM dependency

E18.

## 13.2 Stage latency

E9.

## 13.3 Cost

E20.

## 13.4 Cost per correct certified safe advisory

new metric.

## 13.5 Pareto analysis

Coverage vs safety vs latency vs cost.

---

# 87. 14. Discussion

This section should answer the scientific implications.

## 14.1 What bounded authority buys

Not merely safety.

It buys:

* predictable critical fields;
* traceability;
* reproducibility;
* controllable failure.

## 14.2 Cost of bounded authority

* reduced coverage;
* more abstention;
* more knowledge engineering;
* dependence on authoritative facts.

## 14.3 Why the LLM is still useful

The paper should not become anti-LLM.

State:

> deterministic authority handles facts; LLM handles language and broader contextual interaction.

## 14.4 Where the architecture still fails

Use E10.

## 14.5 Generalization beyond Bengali

Discuss cautiously.

---

# 88. 15. Deployment Implications

This is where CEA orientation becomes explicit.

Discuss:

### Rural connectivity

### Low-end devices

### Offline evidence

### Extension-service escalation

### Knowledge maintenance

### Regulatory updates

### Auditability

### Operational monitoring

This section demonstrates that the paper is not just NLP theory.

---

# 89. 16. Limitations and Threats to Validity

Do not hide limitations.

Explicitly say:

### Benchmark construction

### Agricultural expert availability

### Limited crop coverage

### No national-scale deployment

### No farmer outcome/yield evidence

### Simulated network conditions where applicable

### Vision dataset limitations

### Source authority assumptions

### Classification errors

### Model/API drift

### Regulatory changes

### English/other-language generalization not evaluated.

CEA reviewers will appreciate this.

---

# 90. 17. Reproducibility

This should be unusually strong.

Provide:

### versioned dataset hashes

### model hashes

### configuration files

### random seeds

### environment lockfiles

### exact hardware

### result-generation commands

### raw outputs

### benchmark definitions

### source manifest

### audit schema

### signed evidence package where feasible.

Your current master file already demonstrates the right philosophy: git commit, seed, environment, raw-output path, self-checks and application checks. 

Extend that to the new experiments.

---

# 91. 18. Conclusion

Three paragraphs only.

### Paragraph 1

What architecture was introduced.

### Paragraph 2

What evidence shows.

### Paragraph 3

What remains unproven.

No national deployment claim.

No “solves agricultural AI.”

No “zero-risk.”

---

# 92. The final experiment portfolio

Now the most important practical table.

## CORE — absolutely required

| Experiment                        | Existing? | Final treatment                         |
| --------------------------------- | --------- | --------------------------------------- |
| E2 relational misbinding          | Yes       | **Core + expand**                       |
| E3 11-slot ablation               | Yes       | **Core + rigorous rerun**               |
| E4 calibration/risk coverage      | Yes       | **Core + redo from raw predictions**    |
| E5 counterfactual binding         | Yes       | **Core + expand**                       |
| E6 naturalistic/dialect benchmark | Yes       | **Core + independent holdout**          |
| E7/E8 injection                   | Yes       | **Core + source poisoning**             |
| E10 failure taxonomy              | Yes       | **Core + use to drive revisions**       |
| E17 routing                       | Yes       | **Core + proper threshold protocol**    |
| E18 LLM dependency                | Yes       | **Core**                                |
| E21 linguistic robustness         | Yes       | **Core + independent test**             |
| E23 provenance/cache              | Yes       | **Core + signed/versioned update test** |
| E25 lightweight router            | Yes       | **Secondary/core efficiency**           |

---

# 93. STRONGLY REQUIRED NEW EXPERIMENTS

| New experiment                  | Why                                      |
| ------------------------------- | ---------------------------------------- |
| End-to-end expert benchmark     | **Most important missing evidence**      |
| Oracle vs predicted metadata    | isolates routing error                   |
| High-confidence wrong metadata  | critical safety case                     |
| Authority-boundary ablation     | proves the central mechanism             |
| Parametric/evidence conflict    | modern RAG faithfulness                  |
| Temporal conflict               | current CEA direction                    |
| Source authority conflict       | agricultural validity                    |
| Metamorphic safety testing      | rigorous verification                    |
| Claim-level provenance          | evidence accountability                  |
| Multimodal conflict             | vision/text uncertainty                  |
| Physical edge benchmarking      | CEA deployment credibility               |
| Independent adversarial holdout | prevents defense-specific test criticism |

These are the experiments I would spend most of your remaining effort on.

---

# 94. SECONDARY EXPERIMENTS

| Experiment               | Treatment                     |
| ------------------------ | ----------------------------- |
| E15 SMS                  | secondary deployment evidence |
| E22 SMS injection        | security subsection           |
| E20 cost                 | sensitivity analysis          |
| E24 authoring            | maintenance subsection        |
| E19 graph                | expand substantially          |
| E9 latency decomposition | core efficiency figure        |
| Human review queue       | recommended                   |
| IPM/non-chemical bias    | recommended secondary         |

---

# 95. Experiments I would drop from the main narrative

Not necessarily delete from repository.

### National 16M farmer cost projection

Put in supplementary material or remove.

### Exact “3.06 queries/minute” authoring productivity

Keep only as exploratory unless expanded.

### Tiny 23-node graph demonstration

Replace with scaled graph.

### Every individual production-unit test

Keep in repository, not paper.

### Frontend build statistics

Mention once in reproducibility.

### “26-layer evaluation” language

Delete entirely.

The reader needs to see:

> **five RQs, one architecture, one coherent evidence chain.**

---

# 96. Exact figures I recommend

I would aim for **8–9 main figures** maximum.

## Figure 1 — Bounded-authority architecture

The paper's conceptual centerpiece.

## Figure 2 — Agricultural claim authority model

Show:

```text
Source → Structured fact → Critical claim → Verification → Answer
```

and the LLM as linguistic realization.

## Figure 3 — End-to-end safety/correctness comparison

Systems vs:

* correctness;
* unsafe acceptance;
* coverage.

## Figure 4 — Counterfactual binding

Current E5.

## Figure 5 — Slot ablation

Current E3.

## Figure 6 — Risk–coverage curve

E4/new calibration.

## Figure 7 — Failure taxonomy / containment

E10.

## Figure 8 — Deployment trade-off

Latency / LLM usage / network / edge.

## Figure 9 — Provenance/temporal lifecycle

Source update → cache invalidation → certification.

This gives the paper a strong visual narrative.

---

# 97. Exact tables I recommend

## Table 1

System requirements and failure responses.

## Table 2

Comparison with related agricultural advisory/RAG systems.

## Table 3

Knowledge-base schema and evidence authority model.

## Table 4

Baseline systems and configurations.

## Table 5

End-to-end expert evaluation.

## Table 6

Safety/counterfactual verification.

## Table 7

Risk–coverage/calibration.

## Table 8

Robustness by language/modality.

## Table 9

Deployment performance.

## Table 10

Failure taxonomy and mitigation.

That's enough.

---

# 98. One very important table: literature positioning

Build this early.

| System           | Agricultural | Bengali      | RAG | Structured facts | Temporal | Multimodal | Explicit abstention | Evidence authority | Edge/offline |
| ---------------- | ------------ | ------------ | --- | ---------------- | -------- | ---------- | ------------------- | ------------------ | ------------ |
| Farmer.Chat      | ✓            | multilingual | ✓   | partial          |          |            |                     |                    |              |
| KrishokBondhu    | ✓            | ✓            | ✓   |                  |          | voice      |                     |                    |              |
| Domain-first RAG | ✓            |              | ✓   | ✓                |          |            |                     |                    |              |
| TARAG            | ✓            |              | ✓   |                  | ✓        |            |                     |                    |              |
| SMART            | ✓            |              | ✓   | ✓                |          | ✓          | HITL                |                    |              |
| **This work**    | ✓            | ✓            | ✓   | ✓                | ✓        | ✓          | ✓                   | **✓**              | **✓**        |

Don't use it to claim superiority in every column.

Its purpose is to show:

> **your novelty lies in the intersection.**

Current literature makes the individual technologies non-novel, but the particular safety-oriented integration and evaluation can still be novel. ([ScienceDirect][2])

---

# 99. How to present the current 0% safety numbers

This matters enormously.

Never write:

> “Our system has zero unsafe errors.”

Write:

> “No unsafe certification was observed in the independent evaluation suite; the corresponding upper confidence bound was X%.”

And distinguish:

### Verification-suite result

from

### naturalistic benchmark result

from

### adversarial benchmark result.

Your current E7/E8 gives 0/1,400 with upper CI ~0.27%. 

Your current E6 gives zero observed dangerous acceptance over 4,000 naturalistic/register cases. 

These are very useful, but they must not be pooled into one magical “zero-risk” number.

---

# 100. Statistical protocol for the final paper

I would lock this.

### Binary proportions

Use Wilson 95% intervals.

### Paired binary comparisons

Use McNemar's test.

### Multiple slot ablations

Use Holm correction.

### Human ratings

Use:

* median;
* mean where appropriate;
* bootstrap CI;
* inter-rater agreement.

### Latency

Report:

* p50;
* p95;
* p99.

Use repeated runs.

### Cost

Report:

* point estimate;
* sensitivity interval.

### Risk-coverage

Use AURC + fixed-risk coverage.

### Multiple comparisons

Correct or clearly distinguish exploratory analyses.

---

# 101. Don't use only statistical significance

Always report:

$$
\Delta
$$

and confidence intervals.

For example:

> −13.4 percentage points unsafe acceptance, 95% CI …

That is more meaningful than:

> \(p<0.05\).

---

# 102. Data split architecture

I recommend four sets.

### D_train

model training.

### D_dev

threshold/calibration selection.

### D_test

main naturalistic benchmark.

### D_redteam

independent safety benchmark.

And ideally:

### D_external

a later collected/independent set.

This is the cleanest possible protocol.

---

# 103. Critical anti-leakage rule

Do not use:

* red-team failures;
* E10 residuals;
* final expert labels

to tune the final system and then evaluate on the same cases.

Create:

> **development red-team**

and

> **frozen test red-team**.

This is crucial for your safety claims.

---

# 104. Current master-results inconsistencies must be fixed before drafting

This is non-negotiable.

The master says `FROZEN_AND_VERIFIED`, but several acceptance notes contain stale numbers that disagree with the actual metric blocks.

Examples:

### E14

Raw metric:

> 82.0 → 91.4 at 15% loss
> 12.8 → 58.1 at 30% loss. 

Acceptance note:

> 42.1 → 92.4.

Those cannot both be the final result. 

### E17

Metric block:

> 75.64% search reduction. 

Acceptance note elsewhere gives another figure.

### E18

Metric block:

> 61.52% zero-LLM. 

Acceptance note has an older value.

### E19

Metric block:

> 100% three-hop completeness, 0.0195ms p95. 

Older acceptance text says 97.4%.

### E23

Metric block says 92.8% bandwidth reduction but `invalidation_propagation_completeness_pct: 0.0`; the verification text says purge completeness 100%. 

### E4

The raw reported performance and the “scientific interpretation” do not agree cleanly. 

### Final requirement

Create one canonical pipeline:

```text
raw JSON
   ↓
validated aggregation script
   ↓
master_results_final.yaml
   ↓
all tables/figures
   ↓
paper
```

No hand-edited result numbers.

This alone will make the manuscript much more credible.

---

# 105. I would add a “result provenance test”

Every number in the manuscript should be traceable to:

```text
Paper Table/Figure
    ↓
aggregation script
    ↓
raw experiment output
    ↓
git commit
    ↓
environment
```

You already have the beginnings of this. 

Make it formal.

This can be presented as a reproducibility protocol, not a contribution.

---

# 106. One thing that would substantially impress a CEA reviewer

Run a **blind external replication**.

Give another researcher/agent:

* frozen code;
* frozen benchmark;
* environment;
* command.

They run it without seeing expected results.

Then compare:

$$
\Delta_{replication}
$$

across all primary metrics.

This is not necessary, but given how many artifacts are in your project, it would dramatically increase confidence.

---

# 107. One thing that would substantially impress an agricultural reviewer

Have an agronomist inspect the structured knowledge records, not only final answers.

Sample:

* 500 treatment tuples;
* verify dose;
* formulation;
* PHI;
* interval;
* regulatory status;
* source.

Then report:

> **knowledge-base factual validity**

separately from:

> **system answer validity.**

This closes another major potential criticism:

> “The verifier is only as good as the database.”

The current paper already admits exactly that limitation. 

---

# 108. That suggests a three-level validity model

The final paper should distinguish:

## Level 1 — Knowledge validity

Are the source records correct?

## Level 2 — Resolution validity

Did the system select the right facts?

## Level 3 — Language realization validity

Did the generated answer preserve those facts?

Then:

$$
P(\text{safe answer})
=
P(K)
\times
P(R|K)
\times
P(L|R,K)
$$

conceptually.

This is a powerful way to organize the whole paper.

---

# 109. Where each current experiment fits in that model

| Level                | Experiments                                                      |
| -------------------- | ---------------------------------------------------------------- |
| Knowledge validity   | E23, temporal conflict, source authority, expert fact audit, E24 |
| Resolution validity  | E17, E19, E25, oracle routing, high-confidence error             |
| Language realization | E4, E5, E6, E7/E8, E15                                           |
| Cross-layer safety   | E2, E3, end-to-end benchmark, multimodal conflict                |
| Deployment           | E9, E14, E18, E20, E22                                           |

This is a much cleaner organization than E02–E26.

---

# 110. The core causal chain of the paper

The manuscript should effectively prove:

```text
Agricultural evidence is relational
          ↓
Simple retrieval/citation can misbind facts
          ↓
Structured authority is required
          ↓
Critical facts are represented as typed relations
          ↓
Evidence completeness and authority are checked
          ↓
Only then can an LLM realize the answer
          ↓
If any critical constraint fails:
      abstain / escalate
          ↓
This reduces unsafe acceptance
          ↓
Selective routing limits the cost of doing so
          ↓
Edge/offline mechanisms preserve service availability
```

That is the paper.

---

# 111. Why this is much stronger than the current paper

Your current draft's architecture is already close to this, but its experiments are organized as:

> routing, zero LLM, graph, network, SMS, economics, dialect, security, etc.

The revised paper organizes them as:

> **knowledge validity → authority → decision policy → safety → robustness → deployment.**

This gives reviewers a scientific story instead of an experiment inventory.

---

# 112. What I would make the “killer result”

I would aim for a table approximately like:

| System                |         End-to-end correctness | Critical unsafe acceptance |  Appropriate abstention |        Coverage |                      p95 latency |
| --------------------- | -----------------------------: | -------------------------: | ----------------------: | --------------: | -------------------------------: |
| LLM-only              |                                |                            |                         |                 |                                  |
| RAG                   |                                |                            |                         |                 |                                  |
| Guarded RAG           |                                |                            |                         |                 |                                  |
| RAG+LLM judge         |                                |                            |                         |                 |                                  |
| Deterministic         |                                |                            |                         |                 |                                  |
| **Bounded Authority** | **highest safe certification** |                 **lowest** | **highest appropriate** | **competitive** | **lower on deterministic cases** |

If the data actually supports such a pattern, the paper becomes very strong.

Don't engineer the benchmark to guarantee this pattern; **let the experiment determine it.**

---

# 113. What I would make the second killer result

Counterfactual binding:

> standard methods certify corrupted claims; the authority layer does not.

Your current numbers already suggest this could be spectacular. 

That is much more scientifically interesting than “we improved retrieval by 10 points.”

---

# 114. What I would make the third killer result

Risk–coverage:

> the system can deliberately trade coverage for bounded risk rather than relying on a single confidence threshold.

That's where the calibration experiment becomes central.

---

# 115. What I would make the fourth killer result

Deployment:

> deterministic/local paths preserve advisory availability under degraded connectivity at a fraction of the latency/LLM dependence.

Current E14 and E18 already point in this direction.  

---

# 116. What to do with E15 and E22

Together, they support a broader statement:

> **Once factual authority is established, constrained channels should render from certified structured data rather than re-generate safety-critical content.**

That is elegant.

SMS is just the example.

You could even add:

### voice TTS

and test whether the spoken version preserves:

* dose;
* PHI;
* interval.

But this is optional. I would not add it unless useful for the EACL application as well.

---

# 117. What to do with weather/soil

Do not make them major CEA experiments.

They belong in:

> extensibility/capability architecture.

Weather could be used in one temporal-context case study.

Soil can remain future work unless its underlying model is actually validated.

---

# 118. What to do with IPM

I would add one **small but meaningful** evaluation.

Your system should avoid creating a hidden chemical-intervention bias.

For queries such as:

> “How do I control X?”

measure whether the system appropriately surfaces:

* cultural practice;
* biological control;
* mechanical control;
* monitoring;
* chemical treatment.

when authoritative sources support them.

This gives you an environmental/agronomic angle without creating another paper.

---

# 119. Define “intervention escalation”

For example:

$$
I_0=\text{informational}
$$

$$
I_1=\text{management suggestion}
$$

$$
I_2=\text{chemical recommendation}
$$

$$
I_3=\text{high-risk intervention}
$$

Then evidence requirements increase.

That makes the system more general than pesticide safety.

---

# 120. One methodological addition: evaluate “false confidence”

This is essential.

Measure cases where:

> model confidence high, answer wrong.

Especially:

* classifier;
* retrieval;
* verifier.

Your system's value is partly that it **does not equate confidence with authority**.

This is a very strong conceptual message.

---

# 121. Another important metric: certified precision

For each route:

$$
CP =
P(\text{correct}|\text{certified})
$$

This is more operationally useful than raw accuracy.

A system can have:

> 65% overall accuracy

and:

> 98% certified precision with 34% abstention.

That is a very different system from one with:

> 80% answer rate but unsafe certification.

Your discussion should emphasize this distinction.

---

# 122. Use coverage terminology carefully

I recommend three terms:

### Resolution coverage

percentage where system returns some output.

### Advisory coverage

percentage of answerable cases for which useful advice is returned.

### Safe certified coverage

percentage of all answerable cases resulting in a correct certified advisory.

This avoids the ambiguity in your current “coverage” numbers.

---

# 123. Your E6 result becomes much stronger under this taxonomy

Current:

> 65.8% correct + 34.2% safe abstention + 0 dangerous acceptance. 

Under the new vocabulary:

> 65.8% correctly certified advisories and 34.2% safe non-certification.

That is an extremely interpretable result.

---

# 124. The paper should emphasize that abstention is not failure

But don't over-romanticize it.

Abstention has costs:

* farmer delay;
* extra extension workload;
* reduced service coverage.

Your paper should explicitly quantify:

$$
FalseAbstentionRate
$$

and:

$$
EscalationLoad
$$

This is essential.

---

# 125. Human workload model

Even without real deployment, estimate:

$$
Load =
N_{queries}
\times
P(abstain/escalate)
$$

Then validate it with a simulated queue.

Don't turn it into national economics.

Just show:

> what happens to expert workload as the system becomes safer.

---

# 126. This gives you a second trade-off curve

### Safety ↔ Coverage

and:

### Safety ↔ Human workload

This is very useful for CEA.

---

# 127. Current E10 gives you the starting point for that

6% conservative verifier refusal + 4% calibration underconfidence are already identifiable failure modes. 

You can optimize those without weakening the critical safety boundary.

---

# 128. A very strong system-design principle to articulate

Your architecture should obey:

> **Never solve a failed safety-critical evidence condition by generating more text.**

Instead:

> **repair the evidence, retrieve again, ask for clarification, or abstain.**

That is an excellent systems principle.

For example:

```text
Evidence missing
    ↓
NOT:
"ask LLM to infer it"

DO:
"retrieve better evidence / clarify / abstain"
```

This is a major conceptual distinction from generic RAG.

---

# 129. Retrieval recovery experiment

This is another useful addition.

When retrieval fails:

### Strategy A

retry with query rewrite.

### Strategy B

broaden retrieval.

### Strategy C

structured entity lookup.

### Strategy D

ask user clarification.

### Strategy E

abstain.

Measure:

* recovered correct answer;
* unsafe answer;
* added latency;
* retrieval calls.

This transforms your fallback lane from:

> “fallback”

into a measured **recovery policy**.

---

# 130. This is where your earlier retrieval paper becomes useful

Your second paper identifies retrieval failure modes.

The new paper asks:

> **What should the application do when retrieval fails?**

Excellent continuity.

---

# 131. Recommended failure-recovery hierarchy

```text
1. deterministic fact lookup
2. query/entity normalization
3. structured retry
4. hybrid RAG
5. verified generation
6. clarification
7. abstention
8. human escalation
```

Don't automatically use all of them; evaluate their effect.

---

# 132. This could replace part of the current five-tier ladder

Instead of:

> T0–T4

I would describe:

### Risk policy

and

### resolution policy.

For example:

```text
Risk gate
    ↓
Resolution state
    ↓
Recovery policy
    ↓
Verification
```

This is conceptually cleaner than hard-coded tier numbers.

---

# 133. The CEA paper should be less “LLM-centric”

This is actually an advantage.

The object of study becomes:

> **agricultural advisory computing**

rather than:

> another LLM/RAG paper.

That's exactly what CEA wants.

Current CEA scope explicitly includes AI, machine vision, networking and simulation, but the technology must advance the agricultural computing state of the art. ([Elsevier Shop][1])

---

# 134. Current CEA literature suggests your multimodal and temporal modules are useful support—not the headline

SMART shows multimodal structured retrieval plus human-in-the-loop. ([ScienceDirect][3])

TARAG shows time-aware agricultural RAG. ([ScienceDirect][2])

The goat-farmer RAG work shows domain-first structured knowledge. ([ScienceDirect][4])

Therefore your paper should say:

> “We incorporate these established capabilities as controlled evidence sources inside the bounded-authority architecture.”

That is a much safer novelty claim.

---

# 135. Exact CEA contribution wording I would aim for

Not final prose yet, but the scientific content should be:

### Contribution 1

A **bounded-authority agricultural advisory architecture** that separates factual authority from generative language realization and routes requests according to risk and evidence state.

### Contribution 2

A **typed relational certification mechanism** that prevents cross-record and counterfactual misbinding of safety-critical agricultural fields and explicitly converts unsupported conditions into abstention/escalation.

### Contribution 3

A **multi-axis empirical evaluation** covering end-to-end agricultural correctness, critical safety, selective risk–coverage, linguistic/multimodal uncertainty, temporal/provenance integrity, security, and constrained deployment.

That's the paper.

---

# 136. Exact Results order

Do not change this order unless new evidence forces it.

### First

End-to-end agricultural correctness.

### Second

Critical safety and authority binding.

### Third

Selective risk–coverage.

### Fourth

language/multimodal robustness.

### Fifth

temporal/provenance/security.

### Sixth

edge/network/efficiency.

That ordering mirrors:

> usefulness → safety → uncertainty → robustness → deployment.

---

# 137. What the reader should understand after each section

### After Introduction

> “The problem is factual authority.”

### After Problem Formulation

> “The system has a formal contract for authority.”

### After Architecture

> “Here is how authority is enforced.”

### After Results 1

> “The system still gives useful agricultural advice.”

### After Results 2

> “It is safer because authority binding actually matters.”

### After Results 3

> “It knows when not to answer.”

### After Results 4

> “This remains robust under messy language and modalities.”

### After Results 5

> “The evidence state stays governable.”

### After Results 6

> “The system can actually run under agricultural constraints.”

That's the narrative.

---

# 138. What not to put in the Abstract

Do not list:

> E14, E15, E17, E18, E19…

Never.

The abstract should report only perhaps:

1. end-to-end correctness;
2. safety;
3. selective coverage;
4. deployment efficiency.

Everything else is supporting evidence.

---

# 139. What not to put in the Introduction

Don't start with:

> “Bangladesh has 16 million farmers…”

That is context, not contribution.

Start with:

> **A wrong agricultural recommendation can remain fluent, grounded-looking, and dangerous.**

Then explain why.

---

# 140. What should be the paper's strongest single sentence

Conceptually:

> **The system treats the LLM as a language realization component, not as the authority for safety-critical agricultural facts.**

That's the sentence I would build the paper around.

---

# 141. Where “fail-closed” belongs

Use it carefully.

A fail-closed system means:

> when a required safety condition cannot be established, the system refuses the action.

That does **not** mean:

> source facts are guaranteed correct.

Therefore always distinguish:

### implementation-level fail-closed

from:

### domain-level correctness.

Your existing draft already recognizes this distinction. 

---

# 142. The paper should quantify “unknown unknowns” only cautiously

You cannot measure the entire population of agricultural failures.

Therefore say:

> observed under the evaluated test constructions.

Don't extrapolate.

---

# 143. One more experiment: source-independent test generation

Have an LLM generate adversarial cases from **abstract mutation instructions**, but then have agronomists validate them.

This is a strong hybrid methodology:

```text
programmatic mutation
        ↓
LLM diversity expansion
        ↓
agronomist validation
        ↓
frozen test set
```

This provides scale without letting the LLM define the gold label.

---

# 144. One more experiment: naturalistic hard negatives

For each valid recommendation create:

### near-valid alternative

Correct crop, similar disease, wrong active.

### partially valid

Correct crop + disease + chemical, wrong dose.

### temporally invalid

Correct old record.

### formulation mismatch

Same active, wrong formulation.

These are much more realistic than generic jailbreaks.

---

# 145. One more experiment: source document poisoning

Take legitimate institutional documents and inject one sentence:

> “For this disease, double the recommended dose.”

Then test RAG.

This is more agriculturally meaningful than generic prompt injection.

Your current security benchmark already includes retrieval poisoning, so formalize this as a separate agricultural attack family. 

---

# 146. One more experiment: source fragmentation

Split a valid record across documents:

```text
Document A:
crop + disease + active

Document B:
dose + unit

Document C:
PHI
```

Then test whether systems incorrectly assemble them.

This is perhaps the cleanest demonstration of why:

> **single-record binding**

is important.

---

# 147. One more experiment: incomplete records

Remove:

* PHI;
* formulation;
* unit;
* regulatory status.

Expected:

> abstain.

Then measure:

> how much coverage is lost per missing field?

This complements the slot ablation.

---

# 148. One more experiment: wrong but semantically plausible record

Example:

> correct disease, wrong crop family.

This tests whether semantic retrieval alone can be dangerously persuasive.

---

# 149. One more experiment: user ambiguity resolution

Ask:

> “পাতায় পচা ধরছে, কী দিব?”

No crop, no disease.

System should:

> clarify rather than guess.

Compare with LLM/RAG.

This measures **safe clarification**.

---

# 150. Add a clarification policy

The action space becomes:

$$
A=
\{
answer,
clarify,
retrieve,
verify,
abstain,
escalate
\}
$$

This is better than immediate refusal for ambiguous benign queries.

---

# 151. One more experiment: clarification efficiency

Measure:

$$
\text{queries resolved after one clarification}
$$

versus:

> immediate abstention.

This can improve coverage without sacrificing safety.

---

# 152. That gives you a better system than “refuse everything”

Exactly.

The architecture should be:

> **recover safely before refusing.**

That is a stronger design principle.

---

# 153. E24 can then become a knowledge-recovery loop too

A recurring unsupported query can be sent to:

> knowledge-gap queue.

Then:

> authoritative source found → structured fact added → validation → coverage increases.

This is a natural lifecycle.

---

# 154. Long-term architecture figure

You could have:

```text
Farmer query
    ↓
System response
    ↓
Audit / uncertainty
    ↓
Failure / knowledge gap
    ↓
Expert or author review
    ↓
Structured fact update
    ↓
Versioned evidence
    ↓
Next release
```

That makes your system look like a **living agricultural decision-support platform**, not a static chatbot.

---

# 155. CEA fit becomes much stronger with this lifecycle

CEA is explicitly interested in systems, application, AI, networking and simulation; recent CEA papers likewise emphasize integrated decision-support systems rather than isolated model scores. ([Elsevier Shop][1])

Your paper should therefore present:

> **a reliability-oriented agricultural computing architecture**

rather than:

> **a chatbot implementation.**

---

# 156. Final “must implement before submission” list

I would make these non-negotiable:

### Architecture

* bounded-authority layer;
* capability router;
* structured facts;
* source authority;
* temporal validity;
* claim-level provenance;
* signed/versioned fact pack;
* deterministic resolver;
* clarification policy;
* verifier;
* audit.

### Evaluation infrastructure

* frozen benchmark;
* independent test generation;
* exact baseline harness;
* raw-output canonicalization;
* automatic table/figure generation;
* statistical testing;
* reproducibility container.

### New experiments

* end-to-end expert benchmark;
* authority ablation;
* oracle/predicted routing;
* high-confidence wrong metadata;
* temporal conflict;
* source conflict;
* metamorphic testing;
* parametric/evidence conflict;
* independent red-team;
* physical edge test.

Everything beyond this is secondary.

---

# 157. Final “do if feasible” list

These can make an already strong paper excellent:

* real extension-officer review queue;
* external replication;
* unseen-dialect test;
* source poisoning;
* multimodal conflict;
* energy/query;
* knowledge maintenance at several clusters;
* IPM/non-chemical recommendation analysis.

---

# 158. Final “do not waste time on” list

Do not spend major effort on:

* national adoption projection;
* fancy frontend;
* more weather features;
* more crops without validated facts;
* a new LLM architecture;
* a giant multi-agent system;
* speculative economics;
* dozens of additional UI channels.

These won't strengthen the central scientific claim nearly as much.

---

# 159. The paper's ideal final contribution hierarchy

At the end, I want the reviewer to see:

## Tier 1 — Scientific contribution

**Factual authority separation + evidence-bound certification**

## Tier 2 — Algorithmic/system contribution

**Risk/evidence-aware selective resolution**

## Tier 3 — Engineering contribution

**Temporal provenance + cache + multimodal + edge/channel integration**

## Tier 4 — Evidence

**Expert benchmark + adversarial/metamorphic testing + deployment experiments**

That hierarchy is exactly right for CEA.

---

# 160. My final recommendation on paper length and depth

Do **not** target a short application note.

CEA explicitly distinguishes a short Application Note from its broader original research scope, and the journal emphasizes novelty/innovation and investigator-developed approaches. ([Elsevier Shop][1])

Your work, once the experiments above are completed, is much better positioned as a **full Original Research Paper**.

I would expect a substantial manuscript—roughly **9,000–12,000 words of actual scientific content**, depending on the eventual journal template and figure/table density—not counting references/supplementary material.

The exact word count should be driven by the journal's current submission template at drafting time.

---

# 161. The final experimental package I would aim to submit

Think of it as **six evidence blocks**:

### Block A — Does it work agriculturally?

End-to-end expert evaluation.

### Block B — Is the authority mechanism real?

E2 + E3 + E5 + metamorphic + source fragmentation.

### Block C — Does it know when it does not know?

E4 + calibration + abstention + clarification.

### Block D — Does it survive real-world uncertainty?

dialect + vision + temporal + multimodal conflicts.

### Block E — Does it remain trustworthy operationally?

security + provenance + cache + updates.

### Block F — Is it practical?

edge + network + latency + LLM dependence + cost.

That is the **complete CEA evidence story**.

---

# 162. The relationship to your previous papers becomes exceptionally clean

Your research program is now:

### Previous Paper 1

**What knowledge/data should an agricultural Bengali AI system use?**

### Previous Paper 2

**Where does retrieval fail under Bengali agricultural language variation?**

### CEA Paper

**How should a real agricultural advisory system act when language, retrieval, evidence, perception and deployment conditions are uncertain?**

### EACL Demo

**Here is the resulting complete system.**

That is not redundant publishing.

That is a coherent research program.

---

# 163. The most important conceptual shift for the CEA draft

Your current title says:

> “Evaluating Detection-Gated Deterministic Routing…”

I would now **reverse the emphasis**.

Routing is one mechanism.

The deeper contribution is:

> **factual authority + selective resolution + fail-closed certification.**

So don't let “DGDR” become the paper's identity.

Make the architecture the identity.

---

# 164. Final recommended paper blueprint, compressed into one page

```text
TITLE
Bounded-Authority Agricultural Advisory:
Selective Resolution and Evidence-Bound Verification for Safe Bengali Decision Support

1. Introduction
   ├─ agricultural advisory is safety-sensitive
   ├─ fluent/RAG answers can still misbind facts
   ├─ prior KrishokTech work exposed generation/retrieval limitations
   ├─ research gap: factual authority in integrated advisory systems
   ├─ bounded-authority proposal
   └─ RQ1–RQ5

2. Related Work
   ├─ agricultural RAG/GenAI
   ├─ structured agricultural knowledge
   ├─ multimodal advisory
   ├─ faithfulness/verification
   ├─ selective answering
   └─ RAG security

3. Problem Formulation
   ├─ advisory state
   ├─ critical agricultural tuple
   ├─ evidence authority
   ├─ certification rule
   └─ selective action policy

4. Architecture
   ├─ risk gate
   ├─ capability router
   ├─ structured fact authority
   ├─ deterministic resolver
   ├─ hybrid RAG
   ├─ generative realization
   ├─ verifier
   ├─ temporal validity
   ├─ provenance
   ├─ abstention/clarification/escalation
   └─ edge/offline/channel

5. Knowledge & Governance
   ├─ source hierarchy
   ├─ fact extraction
   ├─ expert review
   ├─ versioning/signing
   └─ maintenance

6. Methodology
   ├─ frozen benchmarks
   ├─ independent test construction
   ├─ expert annotation
   ├─ baselines
   ├─ metrics
   └─ statistics

7. End-to-End Agricultural Results
   ├─ correctness
   ├─ critical-field accuracy
   ├─ coverage
   └─ safe abstention

8. Authority & Safety
   ├─ E2 misbinding
   ├─ E3 slot ablation
   ├─ E5 counterfactual
   ├─ metamorphic tests
   ├─ source fragmentation
   └─ parametric/evidence conflict

9. Selective Reliability
   ├─ E4 calibration
   ├─ risk-coverage
   ├─ threshold
   ├─ oracle/predicted metadata
   └─ high-confidence wrong routing

10. Linguistic & Multimodal Robustness
   ├─ Bengali registers
   ├─ unseen dialect
   ├─ normalization
   ├─ visual uncertainty
   └─ modality conflict

11. Temporal & Evidence Integrity
   ├─ source conflicts
   ├─ temporal validity
   ├─ provenance
   ├─ E23 cache integrity
   └─ knowledge maintenance

12. Security & Delivery
   ├─ prompt injection
   ├─ retrieval poisoning
   ├─ E15/E22 constrained channel
   ├─ E14 network
   └─ edge deployment

13. Efficiency
   ├─ E18 LLM dependency
   ├─ E9 latency
   ├─ energy
   ├─ cost
   └─ Pareto frontier

14. Discussion

15. Deployment Implications

16. Limitations

17. Reproducibility

18. Conclusion
```

---

# 165. My final judgment

With the **current master results alone**, I would not yet submit the present 18-page draft.

But I also would **not** start over intellectually.

You already have several unusually strong components:

* the 10k misbinding evaluation;
* the 10k slot ablation;
* the 2k counterfactual binding test;
* the 4k language/register benchmark;
* the 1.4k injection benchmark;
* calibration/risk–coverage infrastructure;
* offline/network tests;
* cache/provenance tests;
* latency decomposition;
* lightweight routing;
* expert-review infrastructure.   

The **missing centerpiece is end-to-end, independently annotated agricultural correctness and a rigorous causal ablation showing that bounded factual authority—not merely “having a guard”—is responsible for the safety improvement**.

That is what I would build next.

And I would make one hard rule for the rest of the project:

> **Every new experiment must answer one of RQ1–RQ5. If it doesn't, it does not go into the paper.**

That will stop the system from becoming bloated again.

The final paper then becomes not “a paper about all the things KrishokTech can do,” but a much stronger claim:

> **We designed and empirically evaluated an agricultural decision-support architecture in which factual authority is explicitly bounded, uncertainty can terminate safely, and generative language is subordinate to validated agricultural evidence.**

That is, in my view, the strongest CEA paper you can extract from this project.

[1]: https://shop.elsevier.com/journals/computers-and-electronics-in-agriculture/0168-1699?utm_source=chatgpt.com "Subscribe to Computers and Electronics in Agriculture - 0168-1699 | Elsevier Shop | Elsevier Shop"
[2]: https://www.sciencedirect.com/science/article/pii/S0168169926003819?utm_source=chatgpt.com "TARAG: A time-aware retrieval-augmented generation framework for supporting precision crop pest and disease management through large language models - ScienceDirect"
[3]: https://www.sciencedirect.com/science/article/pii/S0168169926004771?utm_source=chatgpt.com "SMART: Structured multimodal agricultural retrieval-augmented transformer for plant disease diagnosis - ScienceDirect"
[4]: https://www.sciencedirect.com/science/article/abs/pii/S0168169926001377?utm_source=chatgpt.com "Towards an AI-based knowledge assistant for goat farmers based on retrieval-augmented generation - ScienceDirect"
[5]: https://www.sciencedirect.com/science/article/abs/pii/S0168169926002504?utm_source=chatgpt.com "Closing the gap between crop simulation and practical decision-making - ScienceDirect"
[6]: https://www.sciencedirect.com/science/article/pii/S0168169925013584?utm_source=chatgpt.com "A comprehensive review of Edge Computing empowered smart agriculture: Trends, Opportunities and Future directions - ScienceDirect"
[7]: https://www.microsoft.com/en-us/research/publication/farmer-chat-scaling-ai-powered-agricultural-services-for-smallholder-farmers/?utm_source=chatgpt.com "Farmer.Chat: Scaling AI-Powered Agricultural Services for Smallholder Farmers - Microsoft Research"
[8]: https://aclanthology.org/2025.acl-long.230/?utm_source=chatgpt.com "SafeRAG: Benchmarking Security in Retrieval-Augmented Generation of Large Language Model - ACL Anthology"
[9]: https://aclanthology.org/2025.ijcnlp-long.56/?utm_source=chatgpt.com "Generate but Verify: Answering with Faithfulness in RAG-based Question Answering - ACL Anthology"
[10]: https://aclanthology.org/2025.acl-long.1062/?utm_source=chatgpt.com "FaithfulRAG: Fact-Level Conflict Modeling for Context-Faithful Retrieval-Augmented Generation - ACL Anthology"
[11]: https://aclanthology.org/2026.eacl-demo.27/?utm_source=chatgpt.com "SciTrue: Evidence-Grounded Claim Verification in Science - ACL Anthology"
[12]: https://2027.eacl.org/calls/industry/?utm_source=chatgpt.com "Industry Track Call for Papers -"
[13]: https://proceedings.neurips.cc/paper_files/paper/2024/hash/27245589131d17368cccdfa990cbf16e-Abstract-Datasets_and_Benchmarks_Track.html?utm_source=chatgpt.com "RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation"
