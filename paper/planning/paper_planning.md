I went deeper, including the repository’s **production-oriented planning/architecture material**, the exact EACL 2027 calls, recent EACL system/industry papers, your two existing papers, and the fast-moving 2025–2026 agricultural-LLM/CEA literature. The result is much more concrete now.

The key correction is this:

**I would not make your two papers “application vs. theory.”**
I would make them:

1. **EACL System Demonstration:** the *engineering-integrated artifact* — what KrishokTech is, how the complete system works, why the integration matters, and evidence that it is usable.
2. **CEA:** the *scientific architectural paper* — a generalizable **bounded-authority / fail-closed advisory architecture**, rigorously evaluated as a decision-support system.

And I would build the software further specifically to make those two papers unusually strong.

Your current repository supports that strategy better than I initially thought. It already has separate architecture/ports/infrastructure, vision, retrieval, audit, tests, deployment-oriented organization, and a future plan explicitly centered around a resolution ladder and structured fact layer. ([GitHub][1])

---

# The most important finding

Your current application has a **much stronger scientific spine** than “Bengali agricultural chatbot.”

Your own production architecture notes identify the key transition:

> today: safety → retrieve → generate → verify

versus the proposed:

> **T0 deterministic safety → T1 structured resolver → T2 deterministic/template advisory → T3 grounded generation → T4 honest refusal**

where the LLM becomes a fallback rather than the default. ([GitHub][2])

And the intended invariant is excellent:

> **“Answer deterministically when we can prove the answer. Use the LLM only to phrase, disambiguate, or when nothing deterministic applies.”** ([GitHub][2])

That is the idea I would build the CEA paper around.

But—and this is important—it is **not enough to call that novel by itself**.

The current literature already contains:

* agricultural systems separating factual knowledge from conversational delivery;
* expert/golden-fact grounding;
* policy-grounded agricultural LLM architectures;
* rule-first agricultural advisory systems;
* time-aware RAG;
* multimodal agricultural decision systems. ([arXiv][3])

So our novelty must be **the particular combination and experimentally demonstrated behavior**, not “we use rules before LLMs.”

That distinction will make or break the CEA paper.

---

# 1. The two papers I recommend

## PAPER 1 — EACL 2027 System Demonstration

### Working title

**KrishokTech: A Safety-Aware Multimodal Bengali Agricultural Advisory System**

Alternative:

**KrishokTech: Evidence-Grounded and Safety-Aware Agricultural Advisory for Bengali Farmers**

I prefer the first one for the demo track.

### What this paper answers

> **What does KrishokTech provide as an integrated, usable NLP system, and how are its components connected to support Bengali agricultural advisory?**

This is an **artifact paper**.

It does not need to prove a new general algorithm.

It needs to demonstrate:

* system originality;
* technical quality;
* meaningful NLP use;
* usable interaction;
* integration;
* reproducibility/accessibility;
* evidence that the system works.

That is exactly what EACL 2027 asks for. The Demo CFP explicitly welcomes application systems, open-source systems, software for evaluation, multimodal systems, and systems ranging from prototypes to production-ready systems. It also requires a live demo/installable package and a ≤2.5-minute screencast. ([EACL 2027][4])

And the recent EACL Demo literature confirms that these can be serious systems papers: for example, the 2026 EACL demo *AI for Climate Finance* combined agentic RAG, structured extraction, benchmarking, expert annotations, public deployment and open-source plans into a 20-page-style system paper; another demo presented a browser-based multimodal verification platform integrated into an established real-world tool. ([ACL Anthology][5])

---

# 2. What the EACL paper should NOT attempt

Do **not** make EACL Demo:

> “We invented DGDR and proved safety.”

That belongs in CEA.

Do not make it:

> “Here are all 24 routes in the frontend.”

Do not make it:

> “Here are all of our retrieval experiments.”

Do not reproduce the dataset paper.

Do not reproduce your retrieval paper.

Do not spend half the paper on agricultural background.

The demo paper should be a polished **system story**.

---

# 3. Exact EACL paper structure

For the 6-page limit, I would use:

## 1. Introduction — ~0.6 page

Establish the practical problem:

* Bengali farmer queries;
* domain-specific evidence;
* safety sensitivity;
* heterogeneous modalities;
* current agricultural AI tends to separate these components.

Then state:

> KrishokTech integrates Bengali RAG, safety routing, evidence verification, image-based disease advisory, and deployable service interfaces into one open research system.

Your existing prior papers provide the knowledge/retrieval foundation; this paper is about integration.

---

## 2. System Design — ~1.5 pages

One major architecture figure.

I want this exact visual:

```text
                         Farmer
                           │
              ┌────────────┴─────────────┐
              │                          │
          Bengali text                 Image
              │                          │
              ▼                          ▼
       Safety / Intent Router       Crop Classifier
              │                          │
              │                    Crop-specific
              │                    disease model
              │                          │
              └────────────┬─────────────┘
                           ▼
                  Capability / Resolver
                           │
             ┌─────────────┼──────────────┐
             ▼             ▼              ▼
        Structured      Retrieval       Refusal
          facts          + LLM
             │             │
             └──────┬──────┘
                    ▼
              Evidence verifier
                    │
                    ▼
             Typed response
                    │
                    ▼
         UI / audit / escalation
```

This is better than your current diagram because it makes the application itself comprehensible immediately.

---

# 4. The EACL paper's strongest application-level differentiator

The system should visibly expose:

> **what the system decided to do, and why.**

Your current API already returns:

* source entries,
* confidence state,
* `agent_trace`,
* verifier flags,
* model information,

and the frontend renders the trace as:

> Checking safety → Retrieving sources → Generating answer → Verifying. ([GitHub][1])

That is excellent demo material.

Make this central.

A farmer/reviewer doesn't merely see:

> “Here is an answer.”

They see:

> “This request was screened → these sources were retrieved → this advisory was generated → this evidence check passed.”

That makes the system **auditable**, which is much more interesting than a prettier chatbot.

---

# 5. EACL section 3 — Interaction modes

~1 page.

Show exactly four scenarios:

### Scenario A — Ordinary Bengali advisory

Farmer asks:

> “ধানের পাতায় বাদামী দাগ হয়েছে, কী করব?”

Show:

query → route → evidence → answer → provenance.

### Scenario B — Chemical safety

Farmer asks for a prohibited/restricted chemical.

Show:

query → safety classifier → immediate block → official escalation.

### Scenario C — Image advisory

Show:

image → crop → crop-specific disease → treatment knowledge → advisory.

### Scenario D — Uncertain query

Show:

uncertainty → no unsafe hallucination → fallback/refusal.

This fourth scenario is critical.

The **refusal behavior** is part of what makes the system distinctive.

---

# 6. EACL evaluation section

~1.3 pages.

Don't attempt 15 metrics.

Use 4 groups:

### A. Functional validation

* unit/integration tests;
* API contract checks;
* model loading;
* route coverage.

### B. NLP quality

Use your **existing retrieval results** only briefly, and identify them explicitly as prior work.

Then test the actual integrated system on a held-out set.

### C. Safety

Use the system's held-out safety benchmark.

### D. Performance

Measure:

* p50/p95 latency,
* retrieval time,
* model time,
* memory,
* local vs remote generation if applicable.

Because you have time and local agents, we can make these measurements much better than what exists now.

---

# 7. EACL paper's “system contribution” statement

The key sentence should approximately become:

> **KrishokTech contributes an openly accessible Bengali agricultural advisory system that integrates safety screening, evidence-grounded retrieval, multimodal disease diagnosis, response verification, provenance tracing, and deployable service interfaces into a single auditable interaction workflow.**

Notice what isn't claimed:

* no “first Bengali RAG”;
* no “best model”;
* no “new classifier”;
* no universal safety theorem.

That matches the EACL demo category very well.

---

# 8. Now PAPER 2 — CEA

This one should be much more serious.

## Working title

**Bounded-Authority Agricultural Advisory: Fail-Closed Routing and Evidence-Bound Verification for Bengali Decision Support**

I like this considerably more than the current title.

Why “bounded authority”?

Because that is the real design philosophy:

> **The LLM is not allowed to own the agricultural decision.**

It can:

* interpret,
* phrase,
* summarize,
* disambiguate.

But critical facts must originate from validated structured evidence.

That's a scientifically meaningful systems principle.

---

# 9. CEA's central research hypothesis

I would make the paper test this:

> **In safety-sensitive agricultural advisory, separating factual authority from linguistic generation—using deterministic structured resolution for supported cases and fail-closed verification/fallback for unsupported cases—can reduce unsafe recommendations while retaining useful coverage and improving operational efficiency.**

That is substantially stronger than:

> “our chatbot has a safety classifier.”

---

# 10. The architectural contribution

This should become your **main new architecture**.

I would implement a formal **Resolution and Authority Layer**.

Something like:

```text
                    QUERY
                      │
                      ▼
              Safety / Risk Gate
                      │
             ┌────────┴────────┐
             │                 │
          unsafe             safe
             │                 │
          STOP/T4              ▼
                   Capability Router
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Structured       Retrieval      Vision/
        Facts            RAG             Context
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  Evidence Authority
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
      Deterministic                  Generative
      answer path                    answer path
           │                               │
           └──────────────┬────────────────┘
                          ▼
                   Certification
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
              ACCEPT            ABSTAIN
                                   │
                                   ▼
                              ESCALATE
```

And every answer carries:

```text
resolution_tier
evidence_ids
evidence_version
authority_type
verification_status
confidence
risk_class
timestamp
```

Your production plan already points toward exactly this kind of contract: structured facts, provenance, `resolution_tier`, corpus version, capability registration and extensibility seams. ([GitHub][2])

---

# 11. But here is the key upgrade I want over the current proposal

Do not make the CEA contribution merely:

> T0/T1/T2/T3/T4.

Make the deeper concept:

# **Authority separation**

Every answer should have two logically separate dimensions:

### Linguistic authority

Who/what can phrase the response?

### Factual authority

Who/what is allowed to determine the agricultural claim?

This is where the LLM becomes a **realization layer** rather than the factual authority.

For example:

```text
Structured fact:
Tomato + late blight
→ active ingredient X
→ dose Y
→ interval Z
→ PHI N

LLM:
Can explain this in Bengali.

LLM:
Cannot alter X/Y/Z/N.
```

That is much more powerful conceptually.

---

# 12. This also differentiates you from current agricultural GenAI literature

The recent agricultural literature is moving rapidly toward:

* GOLDEN FACTS/fact decoupling;
* policy-grounded LLMs;
* time-aware RAG;
* structured knowledge graphs;
* multimodal RAG;
* agentic agricultural decision systems. ([arXiv][3])

So your paper should **not pretend these directions don't exist**.

Instead:

### Use them as baselines or ingredients.

That is exactly what you asked for.

---

# 13. The “use current literature to make the system stronger” strategy

I agree with you completely here.

We should incorporate modern techniques **without allowing them to hijack the paper's identity**.

The CEA system can include:

### 1. Hybrid retrieval

Already present.

BM25 + dense + RRF.

Good.

### 2. Query rewriting

Add a Bengali normalization/rewriting stage, but only as a retrieval aid.

### 3. Structured fact extraction

Convert trusted documents into:

```text
crop
problem
stage
treatment
active ingredient
formulation
dose
unit
volume
interval
PHI
regulatory status
source
validity
```

Your current production plan already specifies almost exactly this structure. ([GitHub][2])

### 4. Temporal validity

This is particularly important because current CEA work is explicitly moving toward time-aware agricultural RAG. ([ScienceDirect][6])

Add:

```text
valid_from
valid_until
source_date
review_date
version
```

### 5. Evidence graph / relation constraints

Don't need a giant KG.

A typed relational layer is enough.

### 6. Confidence calibration

Calibrate:

* safety classifier,
* disease classifier,
* retrieval confidence.

### 7. Selective prediction

Use risk–coverage analysis.

### 8. Human-in-the-loop escalation

This connects directly to contemporary policy-grounded agricultural systems such as Pezego-HITL. ([arXiv][7])

### 9. Multimodal uncertainty

Do not assume image diagnosis is correct.

Pass its uncertainty into advisory routing.

### 10. Audit/event trace

Already built—make it experimentally useful.

---

# 14. The CEA paper should have a **risk-aware query routing policy**

This is the piece I would formalize mathematically.

Not every query deserves the same pathway.

Define a risk score:

$$
R(x)=f(
\text{chemical},
\text{dose},
\text{regulatory},
\text{diagnosis uncertainty},
\text{missing context},
\text{evidence quality}
)
$$

Then use:

$$
\text{route}(x)=
\begin{cases}
\text{block/escalate} & R(x)>r_h\\
\text{deterministic} & R(x)\le r_h \land \text{facts complete}\\
\text{RAG+verification} & \text{evidence exists but facts incomplete}\\
\text{abstain} & \text{unsupported}
\end{cases}
$$

The exact formulation can evolve after experiments.

But this would turn the architecture from an ad hoc collection of rules into a **decision policy**.

---

# 15. CEA Experiment 1 — The central ablation

This is the most important experiment.

Create these systems:

### S0 — LLM only

No retrieval.

### S1 — Standard RAG

Retrieve → LLM.

### S2 — Safety-gated RAG

Safety → retrieve → LLM.

### S3 — RAG + post-hoc verifier

Safety → RAG → LLM → verifier.

### S4 — Structured deterministic resolver

Safety → structured facts → deterministic answer.

### S5 — Full bounded-authority architecture

Safety → resolver → RAG fallback → verifier → abstention/escalation.

Then evaluate all five on the same benchmark.

This one experiment can carry half the paper.

---

# 16. CEA Experiment 2 — Factual correctness

Build a **golden agricultural benchmark** specifically for this paper.

Not another retrieval benchmark.

Use:

* realistic Bengali farmer questions;
* ambiguous questions;
* chemical questions;
* dosage questions;
* disease questions;
* management questions;
* missing-context questions;
* unsupported questions.

Get agricultural experts to create the gold answers.

Then score:

### Atomic fact precision

### Atomic fact recall

### Contradiction rate

### Critical-field accuracy

### Complete advice rate

### Appropriate abstention

This directly responds to the weakness we identified in the first review.

---

# 17. CEA Experiment 3 — Safety attack suite

Create a frozen adversarial benchmark.

Attack dimensions:

### Evidence attacks

* mixed source records;
* outdated source;
* irrelevant high-score retrieval;
* contradictory sources.

### Schema attacks

* wrong crop;
* wrong disease;
* wrong formulation;
* missing dose;
* wrong unit;
* wrong PHI;
* wrong interval.

### Model attacks

* hallucinated chemical;
* plausible fake dose;
* prompt injection;
* instruction override.

### Perception attacks

* wrong crop;
* wrong disease;
* high-confidence misclassification.

### User attacks

* incomplete question;
* colloquial ambiguity;
* adversarial phrasing.

The key metric:

$$
DAR=\frac{\text{unsafe cases accepted}}{\text{unsafe cases}}
$$

with 95% confidence intervals.

But also:

$$
FAR=\frac{\text{safe cases incorrectly refused}}{\text{safe cases}}
$$

Because a safety system that refuses everything is useless.

---

# 18. CEA Experiment 4 — Authority-boundary ablation

This is the experiment I think could make the paper genuinely distinctive.

Create:

### A. Free LLM composition

LLM can produce anything.

### B. Retrieved-context constrained generation

LLM only receives retrieved evidence.

### C. Slot-constrained generation

LLM must fill the schema.

### D. Single-record authority binding

All critical slots must come from the same record.

### E. Full authority-controlled architecture

Structured facts + deterministic resolution + LLM fallback + verifier.

Then measure:

* wrong dosage;
* formulation mismatch;
* PHI errors;
* source mixing;
* unsupported claims.

This tests your **actual architectural hypothesis**.

---

# 19. CEA Experiment 5 — Risk/coverage curve

Vary thresholds.

For example:

$$
\gamma \in \{0.50,0.60,0.70,0.80,0.85,0.90,0.95\}
$$

Measure:

* coverage;
* unsafe acceptance;
* appropriate refusal;
* latency;
* deterministic-route percentage.

Produce a risk–coverage plot.

This is much more scientifically meaningful than saying:

> “γ = 0.8 worked.”

---

# 20. CEA Experiment 6 — Oracle versus predicted routing

This is mandatory.

Run:

### Oracle metadata

Perfect crop/problem metadata.

### Real predicted metadata

Actual model.

### Corrupted metadata

Intentionally introduce wrong but confident labels.

This tells you:

> Is the architecture robust because of verification, or only because the inputs are accurate?

That distinction is critical.

---

# 21. CEA Experiment 7 — Temporal knowledge robustness

This is where I would deliberately borrow an idea from recent agricultural RAG work.

Take a subset of recommendations and create:

* current source;
* outdated source;
* conflicting source;
* revised dose;
* withdrawn/restricted recommendation.

Then compare:

### Standard RAG

versus

### time-aware authority layer.

Measure whether the system:

* selects current evidence;
* detects conflict;
* refuses when validity is unresolved.

This is scientifically useful and directly aligned with current CEA direction. ([ScienceDirect][6])

It also gives your system a **future-facing characteristic** without claiming that temporal RAG itself is your invention.

---

# 22. CEA Experiment 8 — Edge/deployment evaluation

Here we should improve dramatically over your current manuscript.

Use real devices.

At least two:

### Low-end Android

2–4 GB RAM.

### Mid-range Android

6–8 GB RAM.

Measure:

* safety classifier latency;
* image classifier latency;
* retrieval latency;
* network transfer;
* peak memory;
* cold start;
* warm inference;
* energy/query if possible.

Then compare:

### cloud-first

vs

### hybrid local safety/detection + cloud generation

This is where your production architecture becomes valuable.

And this is exactly the kind of agricultural computing evidence CEA cares about.

---

# 23. CEA Experiment 9 — Low connectivity

Now your GSM/offline work has a clear place.

Evaluate:

* 0%;
* 10%;
* 20%;
* 30%;
* maybe 50% packet loss.

Compare:

### cloud-only

### cache-first

### hybrid local safety + cache + cloud

Metrics:

* completion;
* time to usable response;
* stale-answer rate;
* unsafe-delivery rate.

Don't make “SMS” the research paper.

Make:

> **service reliability under constrained connectivity**

the research question.

That is much more defensible.

---

# 24. CEA Experiment 10 — deterministic answer authority

This is one of my favorite experiments for your system.

Take questions where a structured answer exists.

For example:

> crop + disease + stage + treatment

Run the same query repeatedly.

Compare:

### LLM

### RAG+LLM

### deterministic resolver

Measure:

* output variance;
* numeric consistency;
* dosage consistency;
* PHI consistency;
* latency.

Your proposed system has a potentially beautiful result:

> deterministic advisory answers are invariant when evidence is unchanged.

That is more scientifically meaningful than merely saying:

> “deterministic lookup is faster.”

---

# 25. How I would structure the CEA manuscript

## 1. Introduction

Problem:

Agricultural GenAI is promising, but high-stakes recommendations require more than fluent generation.

Gap:

Existing agricultural systems increasingly use RAG, expert facts, structured knowledge and human supervision, but the **authority relationship between deterministic agricultural facts and generative language remains insufficiently formalized/evaluated**.

Contribution:

A bounded-authority advisory architecture.

---

## 2. Related Work

Only four clusters:

### Agricultural advisory systems

Farmer.Chat, KrishokBondhu, AIEP.

### Agricultural GenAI/RAG

GOLDEN FACTS, Pezego-HITL, TARAG.

### Multimodal agricultural decision support

Recent CEA systems.

### Selective/fail-closed AI

Selective prediction, abstention, verification.

Don't spend 4 pages reviewing generic RAG.

---

## 3. Problem Formulation

Formalize:

$$
x \rightarrow (r,e,a)
$$

where:

* \(r\) = risk state;
* \(e\) = evidence state;
* \(a\) = action.

Define acceptable actions:

$$
A=\{\text{answer},\text{fallback},\text{abstain},\text{escalate}\}
$$

Then define authority constraints.

This section makes the paper research-like rather than application-like.

---

## 4. Bounded-Authority Architecture

### 4.1 Risk gate

### 4.2 Capability routing

### 4.3 Structured fact layer

### 4.4 Deterministic resolution

### 4.5 RAG fallback

### 4.6 Evidence authority

### 4.7 Verification

### 4.8 Abstention

### 4.9 Audit/provenance

### 4.10 Edge/cache path

---

# 26. The key architectural diagram for CEA

I would make the paper's primary figure:

```text
                         USER QUERY / IMAGE
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │  RISK & CONTEXT GATE    │
                    │ safety / confidence /   │
                    │ missing-context checks  │
                    └────────────┬────────────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
                   BLOCK                   ACCEPT
                     │                       │
                     ▼                       ▼
                 ESCALATE              CAPABILITY ROUTER
                                               │
                         ┌─────────────────────┼────────────────────┐
                         │                     │                    │
                         ▼                     ▼                    ▼
                    FACT TABLE             HYBRID RAG           VISION
                         │                     │                    │
                         └─────────────────────┼────────────────────┘
                                               ▼
                                    EVIDENCE AUTHORITY LAYER
                                               │
                                  ┌────────────┴─────────────┐
                                  │                          │
                             DETERMINISTIC             GENERATIVE
                               ANSWER                   FALLBACK
                                  │                          │
                                  └────────────┬─────────────┘
                                               ▼
                                    RELATIONAL VERIFIER
                                               │
                             ┌─────────────────┴─────────────────┐
                             │                                   │
                          CERTIFY                             ABSTAIN
                             │                                   │
                             ▼                                   ▼
                         DELIVER                             ESCALATE
```

This is a paper figure, not an app architecture diagram.

---

# 27. The CEA paper's main claim

I would ultimately want the abstract to be able to say something like:

> We show that treating verified agricultural facts as an explicit authority layer—rather than allowing the generator to determine safety-critical values—reduces critical factual errors while preserving useful coverage through selective deterministic and generative routing.

That is the paper.

Everything else supports that.

---

# 28. Now: what to build in the system before submission

Because you have time and agents, I would **actively redesign the codebase**.

The production folder already anticipates this. The current architecture plan says the goal is to let architecture, rather than model choice, be the contribution; it also proposes versioned fact artifacts, typed capabilities and resolution tiers. ([GitHub][2])

I would implement the following.

## Layer 1 — Safety Gateway

Input:

```json
{
  "query": ...,
  "image": ...,
  "context": ...
}
```

Output:

```json
{
  "risk_class": "...",
  "risk_score": 0.93,
  "action": "block|continue",
  "evidence_required": true
}
```

---

# 29. Layer 2 — Capability Registry

Your production plan already has the right idea:

```python
Capability(
    id="disease_advisory",
    can_handle=...,
    resolve=...,
    requires=...,
    available=...
)
```

([GitHub][2])

Make this real.

Capabilities could include:

* general_agri_qa
* disease_advisory
* pesticide_advisory
* crop_calendar
* weather_advisory
* soil
* escalation

This gives the platform an actual **extensibility architecture**.

This is useful for the demo and strengthens the CEA system model.

---

# 30. Layer 3 — Typed Agricultural Fact Store

I would make this the heart of the reliability layer.

Example:

```text
FactID
Crop
Problem
ProblemType
GrowthStage
ActiveIngredient
Formulation
DoseMin
DoseMax
DoseUnit
Volume
Interval
PHI
RegulatoryStatus
IPMAlternatives
SourceID
SourceVersion
EffectiveDate
ExpiryDate
VerifiedBy
VerifiedAt
```

Your current production planning already proposes nearly exactly this structured layer. ([GitHub][2])

---

# 31. Layer 4 — Deterministic Resolver

Input:

```text
crop + problem + stage + intent
```

Output:

```text
fact_id
answer_template
evidence
```

No LLM.

This is crucial.

---

# 32. Layer 5 — LLM realization

The LLM receives the **resolved facts**, not authority over the facts.

For example:

```text
FACTS:
Dose: ...
Unit: ...
PHI: ...
Interval: ...

USER:
...

INSTRUCTION:
You may explain these facts in Bengali.
You must not alter numerical or regulatory fields.
```

Then the verifier checks the output.

This creates a clean separation:

> **knowledge authority → language realization**

---

# 33. Layer 6 — Verification

Move beyond your current verifier.

Add:

### schema validation

### numerical consistency

### unit consistency

### temporal validity

### source binding

### banned/restricted check

### crop/problem compatibility

### formulation compatibility

And return a typed decision:

```text
CERTIFIED
CERTIFIED_WITH_WARNING
ABSTAIN
ESCALATE
```

This can be one of the strongest pieces of the CEA paper.

---

# 34. Layer 7 — Provenance

The current system already exposes source IDs and provenance fields. ([GitHub][1])

Go further:

Every final critical claim should be traceable to:

```text
answer claim
→ structured fact
→ source node
→ source document
→ document version/date
```

This creates a provenance graph.

And **the demo UI should display it elegantly**.

---

# 35. Layer 8 — Audit

You already have a local audit trail.

Use it scientifically.

Every interaction logs:

```text
query
risk class
route
resolution tier
retrieved sources
evidence version
model
verification
final action
latency
```

Then the paper can evaluate:

> how much of the system's behavior is explainable/auditable.

---

# 36. What I would add from current literature—but only as supporting mechanisms

This part matters because you specifically asked about leveraging other research.

### Temporal RAG

Use the idea from TARAG to enforce source validity. ([ScienceDirect][6])

### Golden-fact style evaluation

Use atomic agricultural facts and expert validation from the recent Farmer.Chat/GOLDEN FACTS direction, but **don't duplicate their contribution**. ([arXiv][3])

### Policy-grounded HITL

Use Pezego-HITL's notion of policy compliance and expert escalation as inspiration for your escalation protocol. ([arXiv][7])

### Structured knowledge graph

Use a lightweight relation layer inspired by current agricultural KG work, but don't make KG construction the paper. Recent CEA work is already exploring LLM-driven agricultural knowledge graphs. ([ScienceDirect][8])

### Multimodal evidence

Use crop/disease image input as another evidence source—not as an isolated CV contribution. Recent CEA work already treats vision + language + knowledge graphs as an agricultural diagnosis paradigm. ([ScienceDirect][9])

### Selective prediction

Use calibrated confidence and risk–coverage curves from the broader ML literature.

That combination makes your system feel **current** without turning the paper into a buzzword collection.

---

# 37. One thing I would NOT add

### Multi-agent “agents” for the sake of being modern.

You don't need five LLM agents debating each other.

That would actually damage the core contribution.

Your system's selling point should be:

> **less unnecessary autonomy, more bounded authority.**

That is much more defensible.

Recent agricultural systems are already exploring multi-agent RAG and simulation-grounded reasoning. ([ArXCompass][10])

You don't need to compete there.

---

# 38. What makes your approach different from Farmer.Chat / KrishokBondhu / GOLDEN FACTS?

This needs to be explicit.

### Farmer.Chat

Strong in:

* real deployment;
* multilingual advisory;
* broad agricultural service;
* scale.

Your differentiation:

> **Bengali safety-critical authority/control architecture.**

Farmer.Chat's scale is much larger, so don't compete on scale. Recent technical reporting places Farmer.Chat at very substantial farmer/query volumes. ([ResearchGate][11])

### KrishokBondhu

Strong in:

* Bengali;
* voice;
* call center;
* RAG.

Your differentiation:

> **structured safety, evidence authority, multimodal routing, auditability.**

KrishokBondhu already demonstrates 72.7% high-quality responses in its evaluation, so don't claim that Bengali RAG itself is novel. ([SciRate][12])

### GOLDEN FACTS / Farmer.Chat evaluation

Strong in:

* atomic facts;
* expert evaluation;
* separating facts from delivery.

Your differentiation:

> **architectural enforcement of factual authority and selective route control across deterministic, generative, multimodal and refusal pathways.**

That is where the CEA contribution should live.

---

# 39. The CEA paper should probably NOT claim “first”

Very important.

Your internal novelty document currently proposes several “first Bengali agri assistant…” claims. ([GitHub][13])

I would remove nearly all “first” language.

The literature is moving too quickly.

Instead:

> “To our knowledge, we are the first to evaluate X under Y benchmark…”

only after we conduct an actual systematic search.

But otherwise say:

> **We introduce…**
>
> **We formulate…**
>
> **We evaluate…**
>
> **We demonstrate…**

That's stronger academically.

---

# 40. What the two papers share

They can share the **same software**.

They can share:

* knowledge base;
* models;
* API;
* UI;
* benchmark infrastructure.

But the papers should answer different questions.

### EACL:

> **What is this system and what can users do with it?**

### CEA:

> **Does bounded factual authority and selective routing improve safety/reliability/efficiency of agricultural advisory?**

That's the non-overlap boundary.

---

# 41. What the EACL paper should cite from your prior work

Very explicitly:

> “The Bengali agricultural corpus and retrieval benchmark underlying KrishokTech were developed in prior work [X,Y]. This paper focuses on their integration into a safety-aware multimodal advisory system.”

Then EACL doesn't duplicate your old papers.

---

# 42. What the CEA paper should cite from your prior work

Much more deeply:

Your earlier work provides empirical motivation:

### Paper 1:

parametric generation struggles with exact agricultural treatment facts. ([arXiv][14])

### Paper 2:

retrieval behavior differs strongly by Bengali query type and linguistic condition; no retrieval method is universally best. ([arXiv][15])

Then CEA says:

> therefore, an agricultural advisory system should not assume either generation or retrieval is universally reliable.

That is a **beautiful continuity**.

---

# 43. This gives you a very strong three-paper scientific arc

You already have:

### P1

**Knowledge and benchmark**

### P2

**Retrieval uncertainty**

### P3

**Decision/authority architecture**

And EACL adds:

### P4

**System artifact**

This looks like a research program, not publication slicing.

---

# 44. Exact experimental matrix for the CEA paper

I recommend this as the master table.

| Experiment | Main purpose              | Models/systems                          | Primary metrics                 |
| ---------- | ------------------------- | --------------------------------------- | ------------------------------- |
| E1         | Architecture ablation     | LLM / RAG / gated RAG / verifier / full | unsafe rate, correctness        |
| E2         | Agronomic correctness     | all systems                             | expert correctness/completeness |
| E3         | Safety attacks            | baseline vs full                        | dangerous acceptance            |
| E4         | Authority binding         | free / context / slot / single-record   | critical-field errors           |
| E5         | Selective routing         | multiple thresholds                     | risk–coverage                   |
| E6         | Perception propagation    | oracle / predicted / corrupted          | routing + final safety          |
| E7         | Temporal validity         | standard / time-aware                   | stale acceptance                |
| E8         | Edge deployment           | cloud / hybrid / local                  | latency, RAM, energy            |
| E9         | Network resilience        | cloud/cache/hybrid                      | success, stale, latency         |
| E10        | Deterministic consistency | deterministic vs LLM                    | variance + numeric consistency  |

Ten experiments sounds like a lot, but these are **one experimental program**, not ten disconnected experiments.

And importantly:

**You do not need to report every single one in the main text.**

Some can become appendix/supplementary evidence.

---

# 45. What I would make the headline results

Not:

> 26 evaluations completed.

Not:

> 2,135 nodes.

Not:

> 61.52% zero-LLM.

Instead:

### Result 1

**Critical agronomic errors decrease substantially under authority-bound verification.**

### Result 2

**Deterministic resolution provides exact/invariant handling for evidence-complete queries.**

### Result 3

**Selective routing retains useful coverage while reducing unnecessary generation.**

### Result 4

**The system remains usable under constrained connectivity/edge conditions.**

Those are CEA results.

---

# 46. The EACL paper's headline results

Different:

### Result 1

Integrated Bengali conversational advisory.

### Result 2

Integrated image-to-advisory workflow.

### Result 3

Traceable evidence and verification UI.

### Result 4

Open/reproducible software.

### Result 5

Representative quality/safety/performance validation.

That's a compelling demo paper.

---

# 47. Why I now prefer EACL Demo over Industry Track

After checking the actual current calls, I prefer **Demo** for this particular paper.

The 2027 Demo call explicitly says demonstrations can range from prototypes to mature production systems and gives “application systems using language technology” as a target category. ([EACL 2027][4])

Your system fits naturally.

The Industry Track is also genuinely relevant—it explicitly invites citizen-facing systems, multilingual constraints, application descriptions, system constraints, robustness and reliability in production. ([EACL 2027][16])

But it asks for stronger evidence around real-world implementation/deployment. I would rather make the EACL submission a **killer demo** than stretch the current evidence into an “industry deployment” story.

The fact that your repository has a production-oriented architecture and roadmap helps, but I would call that:

> **production-oriented engineering**

rather than claim:

> **production deployment**

unless you actually deploy it.

---

# 48. And your production-folder correction matters

You were right to correct me.

The top-level README currently describes the repository conservatively as a capstone/demo prototype, but the repository has a separate `production/` planning area, an explicit architecture refinement plan, deployment plans, typed ports/adapters, ML asset separation, testing infrastructure, and future capability/scale plans. ([GitHub][1])

So for the papers, I would characterize it as:

> **research prototype engineered around production-oriented modularity and deployment constraints**

unless actual production deployment exists.

That is a strong and honest formulation.

---

# 49. What I would do with the “production” architecture

I would actually **finish a subset of it before submitting**.

Specifically:

### Must build

* capability registry;
* structured fact layer;
* deterministic resolver;
* authority metadata;
* temporal validity;
* verifier;
* risk-aware routing;
* audit event schema;
* resolution tier in API;
* proper evaluation harness.

### Nice to build

* admin review queue;
* operator dashboard;
* source version management;
* feedback loop;
* cache updates.

### Do not prioritize for the papers

* elaborate monetization;
* dozens of frontend routes;
* generalized marketplace;
* every future module.

Your existing planning document itself makes this distinction: the future scope is broad, but the strongest “one thing” is the safety-aware advisory spine. ([GitHub][17])

---

# 50. The “one crop solved deeply” idea

Your production scope analysis makes an important observation: instead of adding many half-supported crops, select one valuable agricultural problem and make it work end to end. ([GitHub][17])

I agree, but I would modify it slightly for the paper.

Don't restrict the **whole application** to one crop.

Instead:

### For CEA:

Use **2–4 high-risk crop/use-case families** with rich structured facts and expert validation.

For example:

* rice;
* potato;
* chili;
* brinjal.

That gives sufficient diversity.

### For the demo:

show more of the available crop/vision system.

This makes the CEA science focused while the EACL application remains broad.

---

# 51. One particularly strong addition: “evidence completeness”

I would introduce:

$$
EC(x)=
\frac{\#\text{required safety fields supported}}
{\#\text{required safety fields}}
$$

But don't stop there.

Define:

$$
JEC(x)=1
$$

only if **all critical fields are jointly supported by one valid record/version**.

That allows you to experimentally distinguish:

> “I found all the words somewhere”

from:

> “I can legitimately certify the recommendation.”

That is precisely where your current relational verification idea becomes scientifically meaningful. 

---

# 52. Another strong idea: claim-level provenance

Instead of:

> answer → 3 sources

do:

```text
Claim 1 → Fact F21 → Source S8
Claim 2 → Fact F21 → Source S8
Claim 3 → Fact F22 → Source S9
```

Then test:

> **citation correctness vs claim provenance**

This is more sophisticated than generic RAG citation.

For safety-critical fields, however, require:

> **same authoritative record**

rather than merely “has citation.”

That should be one of the core differences between ordinary grounded generation and your system.

---

# 53. Another experiment worth adding: source conflict

This is very important.

Construct:

```text
Source A:
Crop X / disease Y / chemical Z / dose 1

Source B:
Crop X / disease Y / chemical Z / dose 2
```

with different dates/authority.

Then test:

### baseline RAG

Does it merge them?

### verifier

Does it detect conflict?

### temporal/authority resolver

Does it choose correctly or abstain?

This is a very CEA-friendly evaluation because agriculture is temporally and regulatorily dynamic.

---

# 54. Another experiment: “LLM can paraphrase but cannot mutate”

This could become a beautiful small test.

Generate 500 deterministic fact records.

Ask several LLMs to verbalize them in Bengali.

Check:

* numerical mutations;
* omitted fields;
* unit changes;
* PHI changes;
* crop substitutions;
* formulation substitutions.

Then compare:

### unconstrained prompting

vs

### schema-locked prompting

vs

### post-verification.

This directly tests the **bounded authority** principle.

---

# 55. Another experiment: “unsupported question”

Ask questions where the knowledge base contains no reliable answer.

Examples:

* crop not covered;
* disease not in corpus;
* treatment missing;
* formulation missing;
* ambiguous image;
* out-of-date record.

Measure:

> does the system invent something?

This is where abstention matters more than accuracy.

---

# 56. One metric I would introduce: “safe utility”

Rather than reporting accuracy alone, define something like:

$$
SU = C - \lambda H - \mu F
$$

where:

* \(C\) = useful correct responses,
* \(H\) = harmful accepted responses,
* \(F\) = unnecessary refusals,
* \(\lambda \gg \mu\).

You don't have to make this the main metric, but a cost-sensitive utility analysis can formalize why a small coverage reduction may be acceptable if it eliminates high-risk errors.

This fits the selective/policy-grounded literature nicely. ([arXiv][7])

---

# 57. What would “success” look like for CEA?

I am not going to invent target values.

But structurally, the result we want is:

```text
                   Safety-critical errors
                         ↓↓↓↓↓

LLM ─────────────── highest
RAG ─────────────── lower
RAG+Verifier ────── lower
Authority DGDR ──── lowest

                        while

Useful coverage:
LLM ─────────────── high
RAG ─────────────── high
RAG+Verifier ───── moderate/high
Authority DGDR ─── high enough

and

latency:
deterministic < RAG < multi-step generation
```

That pattern would make the paper extremely compelling.

---

# 58. What would make me say “this is genuinely novel”?

After the additional experiments, something like:

> **The contribution is not a new language model or retrieval method. It is an empirically validated architecture that separates factual authority from linguistic generation, assigns queries to deterministic/generative/refusal paths based on risk and evidence completeness, and evaluates the resulting safety–coverage–latency frontier in Bengali agricultural advisory.**

Now we have a real contribution.

---

# 59. What the EACL paper can then say

The demo paper doesn't need to pretend this architecture is a theorem.

It can say:

> “KrishokTech operationalizes the bounded-authority design in a complete farmer-facing application.”

Then show it.

This is clean division.

---

# 60. Simultaneous submission: yes, but manage overlap aggressively

Submitting the CEA journal manuscript and EACL Demo manuscript around the same time is **conceptually possible**, but you must maintain the distinction in content and results.

For EACL, the Demo policy explicitly prohibits significant overlap and says submissions cannot be simultaneously under review elsewhere; it also says multiple demo submissions from the same authors must avoid >25% overlap in content/results. ([EACL 2027][4])

So I would keep a **publication overlap ledger**:

| Material                    |           EACL Demo |                          CEA |
| --------------------------- | ------------------: | ---------------------------: |
| System architecture         |                   ✓ | ✓, but different abstraction |
| UI/screenshots              |                   ✓ |                      minimal |
| API                         |                   ✓ |                   supporting |
| Vision workflow             |                   ✓ |                as experiment |
| Bengali retrieval benchmark | prior work citation |          prior work citation |
| Resolution ladder           |               brief |                      central |
| Authority model             |               brief |                      central |
| Safety benchmark            |      representative |                         full |
| Agronomic expert study      |               small |                      central |
| Risk–coverage               |      maybe 1 figure |                      central |
| Edge performance            |             summary |                         full |
| User interaction            |             central |                      limited |
| Architecture ablations      |                  no |                      central |

That makes the two papers clearly distinct.

---

# 61. I would actually make the CEA paper the “parent research paper”

This means:

### EACL

```text
KrishokTech
   ↓
integrated application
   ↓
system demonstration
```

### CEA

```text
KrishokTech
   ↓
experimental platform
   ↓
scientific hypothesis
   ↓
controlled evaluation
   ↓
generalizable architecture
```

This distinction is extremely important.

---

# 62. The EACL paper should not mention every CEA experiment

For example, don't put:

> “We conducted a factorial study of 12,000 adversarial samples…”

in the demo paper unless needed.

Just say:

> “The system incorporates the fail-closed verification architecture evaluated separately in our companion study.”

But because simultaneous submissions cannot be cited as published papers, be careful. We can phrase the Demo paper so it stands alone without relying on unpublished CEA findings.

---

# 63. The CEA paper should not depend on the EACL paper either

It should stand completely independently.

The repository and system exist as the experimental platform.

---

# 64. Exact work order

Since you said you have time and local agents, this is how I would execute it.

## Phase 1 — Freeze the research identity

Do **not** add random features.

Freeze the core:

> **bounded authority + selective routing + evidence verification**

This is the CEA hypothesis.

---

## Phase 2 — Re-architect the application

Build:

1. structured fact store;
2. capability registry;
3. resolution tiers;
4. risk-aware routing;
5. temporal source validity;
6. deterministic resolver;
7. authority-bound LLM realization;
8. verifier;
9. audit trail.

---

## Phase 3 — Build the benchmark

Create:

### 3–5k realistic Bengali queries

with labels:

* safe/unsafe;
* answerable/unanswerable;
* fact requirements;
* risk;
* gold agricultural answer;
* acceptable abstention;
* source authority.

And a separate:

### 1–2k adversarial cases.

Do not evaluate on data used to engineer the rules.

Freeze this test set **before final tuning**.

---

# 65. Phase 4 — Expert annotation

This is important.

Have at least **3 agronomists** independently annotate a substantial subset.

Measure:

* agreement;
* difficult-case rate;
* correctness;
* safety;
* completeness.

You already used three agronomists in the current work, with Gwet's AC1 reported as 0.862. 

That is useful infrastructure. We can scale the protocol rather than throw it away.

---

# 66. Phase 5 — Controlled evaluation

Run all ablations under the same:

* model;
* retrieval corpus;
* prompts;
* query set;
* hardware;
* seeds;
* decoding settings.

Then produce one canonical results ledger.

Your current paper's E14/E20/E25 inconsistencies should **not** survive into the next version. The existing manuscript itself says those artifacts conflict. 

We should make this new evaluation reproducible from one command.

---

# 67. Phase 6 — Physical deployment test

Use:

### phone

### laptop / low-end PC

### server/cloud

and measure:

* RAM;
* inference;
* network;
* energy where possible.

This supports both:

* CEA deployment claims;
* EACL system quality.

---

# 68. Phase 7 — Build the EACL demo

The final demo should have a **single magical interaction**.

Example:

### User enters:

> “আমার আলু গাছে দেরিতে পচা রোগ হয়েছে, কী ওষুধ দেব?”

System visually shows:

```text
✓ Safety checked
✓ Agricultural intent recognized
✓ Structured evidence available
✓ Deterministic resolution selected
✓ Source verified
✓ Dose verified
```

Then:

> Bengali answer.

Then click:

> **Why this answer?**

and show:

> fact → source → date → verifier.

That is a memorable demo.

---

# 69. Second demo interaction

Upload a diseased leaf.

Show:

```text
Image quality
      ↓
Crop prediction
      ↓
Disease prediction
      ↓
Confidence
      ↓
Agricultural evidence
      ↓
Advice
      ↓
Safety verification
```

Again, this is a very strong integrated NLP + multimodal demo.

---

# 70. Third demo interaction

Ask a banned/restricted treatment.

Show:

```text
⚠ High-risk query
→ generation not invoked
→ advisory blocked
→ escalation route
→ audit event
```

This is probably the most visually convincing part of the system.

---

# 71. The EACL paper's contribution list should be only three items

### C1 — Integrated Bengali agricultural advisory system

### C2 — Multimodal image-to-advisory workflow integrated with evidence-grounded NLP

### C3 — User-visible safety/provenance/verification trace for an open, reproducible system

That's enough.

Don't list 12 “contributions.”

---

# 72. The CEA contribution list should also be only three

### C1

**Bounded-authority architecture** separating factual authority from language generation.

### C2

**Risk/evidence-aware selective routing** across deterministic, generative and abstention paths.

### C3

**Comprehensive agricultural validation** of the safety–coverage–latency trade-off under Bengali, multimodal and constrained-deployment conditions.

Now the two papers are unmistakably different.

---

# 73. What I would call the architecture

I'm not convinced “DGDR” is the best final name.

It sounds like primarily a routing mechanism.

The deeper idea is authority.

Potential names:

### BAC — Bounded Authority for Agricultural Copilots

### BAA — Bounded-Authority Advisory Architecture

### SAFE-RAG

**Safety-Aware Fact-Entailment RAG**

### FARM-GUARD

**Fact-Authority Routing and Mitigated Generation for Guided Agricultural User Recommendations and Decisions**

I actually prefer something simpler:

## **BAA — Bounded-Authority Advisory**

Then the system could be:

> **BAA-KrishokTech**

But this is something we should settle only after formalizing the method.

---

# 74. One major warning

Don't create an acronym soup.

The current manuscript has:

> DGDR, E02–E26, T0–T4, E17, E21, E25, etc.

For the CEA paper, this is too project-management-like.

We should have:

* **one architecture name**
* **four or five components**
* **four research questions**
* **a handful of experiments**

That's it.

---

# 75. My exact recommended CEA RQs

## RQ1 — Reliability

**Does separating factual authority from language generation reduce critical agricultural factual errors relative to LLM-only and RAG baselines?**

## RQ2 — Selective routing

**Can risk/evidence-aware routing reduce unnecessary generation while retaining useful advisory coverage?**

## RQ3 — Robustness

**How does the architecture behave under evidence corruption, temporal conflict, classifier error and adversarial input?**

## RQ4 — Deployment

**What are the latency, memory, energy and connectivity trade-offs of deterministic, generative and hybrid advisory paths?**

That is a coherent journal paper.

---

# 76. Exact EACL sections

## 1. Introduction

## 2. System Overview

## 3. Architecture and Components

### 3.1 Safety router

### 3.2 Bengali RAG

### 3.3 Multimodal diagnosis

### 3.4 Verification and provenance

### 3.5 Interaction/audit UI

## 4. Demonstration Scenarios

## 5. Evaluation

### 5.1 Functional validation

### 5.2 Quality/safety evidence

### 5.3 Performance

## 6. Availability and Reproducibility

## 7. Ethics / Limitations

That's all.

---

# 77. Exact CEA sections

## 1. Introduction

## 2. Related Work

## 3. Problem Formulation

## 4. Bounded-Authority Advisory Architecture

### 4.1 Risk gate

### 4.2 Capability routing

### 4.3 Structured fact authority

### 4.4 Deterministic resolution

### 4.5 Generative realization

### 4.6 Evidence certification

### 4.7 Abstention/escalation

### 4.8 Temporal/provenance controls

## 5. Experimental Design

### 5.1 Benchmark

### 5.2 Baselines

### 5.3 Expert annotation

### 5.4 Safety attack suite

### 5.5 Deployment environments

## 6. Results

### 6.1 End-to-end correctness

### 6.2 Critical safety

### 6.3 Risk–coverage

### 6.4 Classifier error propagation

### 6.5 Temporal/conflicting evidence

### 6.6 Edge/network performance

## 7. Discussion

## 8. Limitations

## 9. Reproducibility

## 10. Conclusions

That is a real CEA paper.

---

# 78. Where the existing manuscript material goes

| Current material            | Destination                                        |
| --------------------------- | -------------------------------------------------- |
| DGDR                        | **CEA core**                                       |
| 11-slot tuple               | **CEA core**                                       |
| fail-closed verifier        | **CEA core**                                       |
| safety stress tests         | **CEA core**                                       |
| classifier error            | **CEA core**                                       |
| zero-LLM ladder             | **CEA core, redesigned**                           |
| Bengali retrieval benchmark | **prior work / small EACL mention**                |
| vision system               | **EACL core; CEA robustness experiment**           |
| SMS                         | **CEA deployment subsection**                      |
| cache                       | **CEA deployment subsection**                      |
| national economics          | **remove**                                         |
| authoring rate              | **remove**                                         |
| E26 exploratory fallback    | **remove unless it becomes scientifically useful** |
| 23-node graph demo          | **replace with larger-scale evaluation**           |
| project ledger/status       | **remove from paper**                              |
| current figures             | **redesign**                                       |
| 26 experiment taxonomy      | **replace with 4 RQs / 8–10 controlled tests**     |

This is the surgery I would perform.

---

# 79. Your “application paper” intuition was only half wrong

You were right that:

> “I developed a complete system, therefore I should have a system paper.”

Absolutely.

The mistake was thinking:

> “A system paper must describe the entire system.”

No.

A system paper describes:

> **the system's identity, architecture, functionality, audience, originality, evidence, and availability.**

An application paper is still a scientific argument.

The codebase can be enormous.

The paper can be six pages.

The CEA manuscript can be much deeper because its object is the **architectural principle and experimental evidence**, not the complete product.

EACL 2027's Demo criteria make exactly this distinction: design, novelty, architecture, functionality, validation, accessibility and usability matter, while a comprehensive experimental evaluation is not required. ([EACL 2027][4])

---

# 80. The best final positioning

I would position the whole project like this:

> **KrishokTech is an open Bengali agricultural advisory platform developed around a research program on trustworthy agricultural language technology. Earlier work established the knowledge and retrieval foundations; the current system integrates multimodal diagnosis, retrieval, safety routing, evidence verification and deployment-oriented interfaces. This work then studies bounded factual authority as the reliability layer connecting those components.**

That's clean.

Your CV then tells a story:

**Dataset → Retrieval → Integrated System → Reliability Architecture**

---

# 81. My final decision: two papers, specifically these two

## PAPER 1 — EACL 2027 Demo

**KrishokTech: A Safety-Aware Multimodal Bengali Agricultural Advisory System**

**Identity:** software/system artifact.

**Primary contribution:** complete, open, auditable Bengali agricultural NLP application.

**Primary evidence:** system validation + live demonstration + representative safety/quality/performance evaluation.

**Target length:** 6 pages + references/appendix.

**Deadline:** 22 September 2026. ([EACL 2027][4])

---

## PAPER 2 — CEA

**Bounded-Authority Agricultural Advisory: Fail-Closed Routing and Evidence-Bound Verification for Bengali Decision Support**

**Identity:** scientific agricultural computing paper.

**Primary contribution:** bounded-authority architecture + selective resolution + evidence certification.

**Primary evidence:** expert-annotated end-to-end benchmark + ablations + adversarial safety + risk–coverage + perception propagation + temporal conflict + edge/network evaluation.

**Target:** substantially more rigorous than the current manuscript.

---

# 82. And the key point about doing the experiments “from scratch”

**Yes.**

Given what you told me, I would actually prefer a clean re-run.

Your current results are useful as exploratory evidence, but the next CEA study should have:

> **a frozen benchmark → frozen baselines → frozen protocol → clean run → one canonical result set.**

Your existing results tell us **what to test**, not necessarily what must appear as final evidence.

That is especially important because your current manuscript itself acknowledges unresolved conflicts in E14/E20/E25. 

---

# 83. The one thing I would lock now

Before writing a single paragraph of either paper, I would lock this boundary:

### EACL asks:

> **Can we demonstrate a complete, useful, credible Bengali agricultural AI system?**

### CEA asks:

> **Can bounded factual authority and selective routing make agricultural AI advisory more reliable under safety and deployment constraints?**

Everything you build afterward should map to one of those two questions.

That is the clean separation you were looking for.

And importantly, it means **you can still make the system much more impressive before submission**—temporal evidence, calibrated routing, structured facts, human review, stronger vision uncertainty, offline reliability, provenance graphs, local inference, etc.—without turning either manuscript into a feature dump. The recent agricultural literature actually gives us several mature mechanisms to borrow in exactly that way. ([ScienceDirect][6])

The next step should be to turn these into **two frozen research protocols**: exact datasets, exact baselines, exact ablations, exact metrics, annotation protocol, statistical tests, figures/tables, software changes, and an explicit **EACL-vs-CEA overlap matrix** before we start implementation.

[1]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System "GitHub - RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
[2]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System/blob/main/production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md "KrishokTech-Agricultural-Advisory-System/production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md at main · RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
[3]: https://arxiv.org/abs/2603.03294?utm_source=chatgpt.com "Fine-Tuning and Evaluating Conversational AI for Agricultural Advisory"
[4]: https://2027.eacl.org/calls/demos/?utm_source=chatgpt.com "Call for System Demonstrations -"
[5]: https://aclanthology.org/2026.eacl-demo.34/?utm_source=chatgpt.com "AI for Climate Finance: Agentic Retrieval and Multi-Step Reasoning for Early Warning System Investments - ACL Anthology"
[6]: https://www.sciencedirect.com/science/article/pii/S0168169926003819?utm_source=chatgpt.com "TARAG: A time-aware retrieval-augmented generation framework for supporting precision crop pest and disease management through large language models - ScienceDirect"
[7]: https://arxiv.org/abs/2607.13934?utm_source=chatgpt.com "Pezego-HITL: A policy-grounded large language model architecture for agricultural extension in Ghana"
[8]: https://www.sciencedirect.com/science/article/pii/S016816992600565X?utm_source=chatgpt.com "Autonomous construction of crop pest and disease knowledge graphs at scale via LLM-driven expert modeling - ScienceDirect"
[9]: https://www.sciencedirect.com/science/article/pii/S0168169926000797?utm_source=chatgpt.com "From identification to prevention: a kiwi disease diagnosis system integrating vision and large language models - ScienceDirect"
[10]: https://arxcompass.github.io/papers/llm/2026_07/papers_9.html?utm_source=chatgpt.com "llm - 2026_07 | ArXCompass"
[11]: https://www.researchgate.net/publication/399930197_Building_AI-based_advisory_services_for_smallholder_farmers_Technical_learnings_from_the_AIEP_Initiative?utm_source=chatgpt.com "(PDF) Building AI-based advisory services for smallholder farmers: Technical learnings from the AIEP Initiative"
[12]: https://scirate.com/?date=2025-10-28&page=106&range=7&utm_source=chatgpt.com "Top arXiv papers"
[13]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System/blob/main/production/future_plan/06_PAPER_NOVELTY.md "KrishokTech-Agricultural-Advisory-System/production/future_plan/06_PAPER_NOVELTY.md at main · RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
[14]: https://arxiv.org/abs/2606.29243?utm_source=chatgpt.com "KrishokTech: A Citation-Grounded Dataset and Benchmark for Bengali Agricultural Advisory"
[15]: https://arxiv.org/abs/2608.14886?utm_source=chatgpt.com "Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory"
[16]: https://2027.eacl.org/calls/industry/?utm_source=chatgpt.com "Industry Track Call for Papers -"
[17]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System/blob/main/production/future_plan/00_SCOPE_OUTLINE.md "KrishokTech-Agricultural-Advisory-System/production/future_plan/00_SCOPE_OUTLINE.md at main · RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
