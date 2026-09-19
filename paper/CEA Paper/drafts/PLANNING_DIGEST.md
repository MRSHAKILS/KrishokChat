# PLANNING_DIGEST.md

Extraction digest of three planning sources for the CEA manuscript
"Bounded-Authority Agricultural Advisory: Selective Resolution and Evidence-Bound
Verification for Safe Bengali Decision Support".

Sources read (in full):
1. `paper/planning/innovation_plan.md` — 3,714 lines
2. `paper/planning/paper_planning.md` — 2,932 lines
3. `paper/planning/paper_eacl.md` — 3,957 lines

**Scope note on the comparison request.** Section 1 asks for "anything present here
that is NOT already in the CEA design brief `paper_cea.md`". The task instructions
explicitly forbade opening any file other than the three above, so `paper_cea.md`
was **not read** and no line-by-line diff against it was possible. The
"not-in-a-standard-CEA-brief" sub-section below therefore lists material that is
atypical of a journal design brief on structural grounds (funding-pitch framing,
commercialisation, deck design, submission logistics), flagged as *unverified
against paper_cea.md*.

---

## 1. innovation_plan.md — what it contributes

### 1.0 What this document actually is

Not a paper plan. It is a **Bangladesh Innovation Fair 2026 funding-selection
submission strategy** (8-slide pitch deck + ~20-slide supporting dossier + ≤250-word
description + technical-details field + live demo plan). It is framed as
"a **funding-selection pitch**, not as a paper presentation" (line 1). It contains
the project's own consolidated claim inventory and evidence numbers, which is why it
is relevant to the CEA manuscript.

Fair logistics stated: "Innovate to Market" theme; categories include Agriculture &
Food Technology and AI/Automation/Robotics; requires "a ≤250-word description,
technical details, a 7–8 slide deck covering nine evaluation dimensions, and
optionally a current-status supporting document"; registration deadline stated as
**30 August 2026**, internal deadline treated as **28–29 August**.

### 1.1 Novelty claims and how they are framed

Quoted verbatim from the source:

1. **Core mechanism claim (§6):**
   > deterministic answer when the system can prove the answer; LLM only for phrasing, disambiguation, or unsupported cases.

   Framed with the headline slogan:
   > # **"The AI does not get to invent the agricultural fact."**

   and: "The system retrieves/derives the authoritative agricultural information
   first, and the language model becomes a bounded explanation layer."

2. **Integration-not-components claim (§Slide 4, line 416):**
   > **Our innovation is the integration and orchestration: language, vision, evidence, safety, verification and delivery operate as one accountable advisory system.**

   Explicitly guarded: "Don't claim that each element is new."

3. **Evidence-gating claim (§Slide 4, line 404):**
   > # **"No evidence → no unsafe advice."**

4. **Failure-driven-architecture claim (§3, line 78):**
   > **evidence that your architectural decisions came from observed failures, not from assembling trendy technologies.**

   and (§Slide 3, line 357): "**We did not start with a chatbot. We started with the
   failure modes of agricultural AI.**"

5. **Retrieval-fragility claim (§4, line 98):**
   > **Farmer language is not the same as standardized Bengali, and retrieval performance changes dramatically with dialect, colloquial wording and Romanized Banglish.**

   Explicitly *not* to be framed as "LLMs don't understand Bengali" ("That's too crude").

6. **Discovered failure-mode list (§Slide 5, line 450):**
   > **Our research uncovered real failure modes—including retrieval omission, relational misbinding, numerical ambiguity and linguistic ambiguity—and those findings directly changed the architecture.**

7. **Justified-answers principle (§44, line 1560):**
   > **Agricultural AI should not maximize the number of answers; it should maximize the number of answers that are justified.**

8. **Strongest originality framing (§73, line 2350):**
   > **KrishokTech does not treat agricultural AI as a chatbot problem; it treats it as an evidence, decision, safety and delivery problem—and integrates those layers into one Bengali-first system.**

9. **Safety-behaviour claim (§77, line 2380):**
   > **When the system cannot establish the evidence required for a high-risk recommendation, it does not complete the recommendation—it asks, refuses, or escalates.**

10. **Contrast-with-general-LLM claim (§125, line 3297):**
    > **"ChatGPT can generate an answer. KrishokTech is designed to decide whether an agricultural answer is justified before it is delivered."**

11. **Biggest-innovation answer (§124, line 3289):**
    > **"Our innovation is that the agricultural decision is not delegated blindly to a generative model. We built a system where farmer language, vision, agricultural evidence and safety controls work together, and the system can deliberately answer, clarify, refuse or escalate depending on what it can establish."**

12. **Extensibility claim (§32, line 1211):**
    > **The architecture is intentionally modular so that new crops, knowledge packs, models, regulatory data sources and advisory capabilities can be added without redesigning the farmer-facing application.**

13. **Layer-separation claim (§76, line 2374):**
    > **The platform already separates application logic, models, retrieval, verification, audit and deployment infrastructure, allowing new knowledge and capabilities to be added without rebuilding the farmer-facing product.**

14. **Data-operation scaling claim (§60, line 2033):** the production plan "explicitly
    says one design goal is that adding 10× knowledge should be a **data operation
    rather than a code rewrite**, with versioned/hash-pinned artifacts and expert review."

### 1.2 Conceptual frameworks, named mechanisms, acronyms, formalisms (exact names)

- **"route, verify, abstain, escalate"** (§17, line 820) — the named four-action
  architectural response to insufficient language/retrieval confidence. Introduced as
  the answer to: "**What should a real system do when its language/retrieval
  confidence is insufficient?**" and described as "the bridge from research to product."

- **Four-branch decision policy (§44, lines 1564–1580), verbatim block:**
  ```text
  Unsafe
     ↓
  STOP

  Insufficient evidence
     ↓
  CLARIFY / REFUSE

  Verified evidence
     ↓
  ANSWER

  Complex but supported
     ↓
  GENERATE + VERIFY
  ```

- **Full advisory pipeline (§Slide 4, lines 371–400), verbatim:**
  ```text
                FARMER
            text / image / voice
                      │
                      ▼
             UNDERSTAND CONTEXT
                      │
                      ▼
              SAFETY SCREEN
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        VISION       FACTS        RAG
          │           │           │
          └───────────┼───────────┘
                      ▼
              AGRICULTURAL
            EVIDENCE ENGINE
                      │
                      ▼
           VERIFY BEFORE DELIVERY
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
         ADVISE             CLARIFY/
                             ESCALATE
                      │
                      ▼
            WEB / MOBILE / SMS
  ```

- **"11-slot formal equation"** (§11, line 681) / **"Why 11 fields matter"** (§21,
  line 896) — the typed agricultural treatment record with 11 fields. Named fields
  appearing in the ablation: **dosage**, **regulatory status**, **active ingredient**,
  and "all typed constraints". The document says to "Visualize the agricultural
  treatment record" then show the ablation. No full enumeration of all 11 fields is
  given in this file.

- **Typed verifier** — named as a method row in the counterfactual comparison table
  (§20). **"typed relational misbinding evaluation"** — named as the 10,000-case
  evaluation suite (§Slide 5, line 438).

- **Detection-gated routing** (§4, line 103) / **metadata-guided routing** (§22,
  line 931) — the mechanism that raises dialect and Banglish coverage. Labelling
  instruction: "explicitly label: > **Improved advisory coverage through
  metadata-guided routing.**"

- **Six-way safety classification** + **pre-generation terminal blocking** (§5, §31).

- **Crop→disease model routing** (§5, line 121) — crop classifier then crop-specific
  disease classifier.

- **Zero-LLM terminal handling** vs **deterministic advisory routing** — two distinct
  metrics that the document insists must not be conflated (§23, line 949: "The exact
  interpretation must distinguish safety/refusal from deterministic advisory.").

- **Vocabulary mandated for safety claims** (§107): "**evidence-constrained**",
  "**fail-closed**", "**verified**", "**unsafe cases are blocked in tested scenarios**".

- **Innovation definition (§7, line 159):**
  > **A Bangladesh-first, Bengali, multimodal agricultural decision-support platform that combines farmer-language AI, crop/disease vision, authoritative agricultural knowledge, safety verification, and low-connectivity delivery into one deployable advisory system.**

- **Positioning one-liner (§145, line 3631):**
  > # **From farmer language to verified agricultural action.**

### 1.3 Metrics and numbers (exact, as written)

Headline set (§33):
- **2,135** provenance-carrying knowledge nodes
- **2,946** institutional source documents
- **145,500** benchmark/supervised QA examples from the research foundation
- **1,001** authentic farmer queries in the Farmer Benchmark
- **10,000** relational safety cases
- **1,400** adversarial security cases
- **61.5%** zero-LLM terminal handling in the current workload model
- **0 observed** dangerous certification in the typed-verification evaluation

Efficiency / workload (§Slide 5 line 442, §23, §108, §137):
- "**61.5%** of the current modeled workload reaches zero-LLM terminal handling,
  including safety/refusal; **51.0%** is deterministic advisory routing specifically."
- "61.52% zero-LLM terminal handling; 51.04% deterministic advisory paths;
  2.28× modeled latency improvement"
- "51.04% of the workload in the reported model is deterministic advisory, while
  38.48% reaches generation."

Security benchmark, 1,400 injection cases (§19, line 870):

| Pipeline        | Unsafe certification |
| --------------- | -------------------: |
| LLM direct      |               83.86% |
| Vanilla RAG     |               69.36% |
| RAG + LLM guard |               21.79% |
| KrishokTech     |      **0% observed** |

Evidence-binding / counterfactual result (§20, line 885):

| Method         | False certification under corrupted evidence |
| -------------- | -------------------------------------------: |
| Vanilla RAG    |                                       72.65% |
| Lexical        |                                       59.55% |
| LLM Judge      |                                       38.65% |
| Typed verifier |                                       **0%** |

Typed-field ablation (§21, lines 902–908), verbatim:
> removing dosage → +31.6 pp hazard
> removing regulatory status → +17.8 pp
> removing active ingredient → +14.2 pp
> removing all typed constraints → 80% hazard.

Language/dialect coverage (§4, §22):
- "regional dialect text-first coverage is around 43%; detection-gated routing raises
  it to around 90%; Banglish similarly rises from around 42% to around 90%; the system
  maintains zero observed dangerous acceptance in that evaluated set."
- Exact form (§22): `Regional dialect 42.9% → 89.8%`, `Banglish 41.6% → 90.0%`,
  `Authentic farmer language ...` (left incomplete in source)

Offline / low-connectivity simulation (§24, line 959):
- "91.4% vs 82.0% at 15% loss and 58.1% vs 12.8% at 30% loss" (offline-first vs
  cloud-only). Must be labelled "**Controlled network simulation**", "not real field
  connectivity."

Software invariants (§25):
- **558 tests passing**, **50/50 golden replay**, frontend build green, modular
  architecture, local + remote LLM, health/readiness endpoints, audit trail,
  deployment structure.

Prior-paper (Paper 1) dataset numbers (§14, lines 746–752):
- 290 hierarchical knowledge nodes; 129 manuals; 139,200 instruction-tuning pairs;
  5,300 chemical safety; 1,000 adversarial; 145,500 total QA pairs; 1,001 farmer benchmark.

Numbers explicitly deprioritised (§34, lines 1261–1265) — "Don't headline":
- 0.0195ms graph traversal; 0.3855ms classifier latency; 92.8% cache bandwidth
  reduction; $0.000213 per answer; 75.64% search reduction.
  ("These are excellent **supporting evidence** but weak innovation-fair headlines.")

### 1.4 Positioning-vs-prior-work arguments

- **Plantix** (§Slide 2, line 291; §126): "Do **not** insult Plantix or existing
  services. Instead compare categories." Answer script if asked how it differs from
  Plantix: "Don't say: > 'Plantix is bad.' Say: > **'We are not competing only on
  image diagnosis. Our system combines Bengali conversational interaction, local
  agricultural evidence, safety-critical verification, multimodal follow-up and
  Bangladesh-oriented deployment channels.'**"

- **Category reframing (§35):** existing mental model "**Agricultural AI =
  chatbot/diagnosis app**" vs. proposed "**Agricultural AI = national decision-support
  infrastructure**"; "Then compare **architecture**, not features."

- **BAMIS and the 16123 Agricultural Call Center (§39, §90):** treated as existing
  national advisory infrastructure that establishes demand rather than as competitors.
  "the advisory demand already exists; we are modernizing its delivery layer." And:
  "KrishokTech provides an AI-native, Bengali, multimodal layer that can complement
  these channels rather than pretending to replace them."

- **National-significance framing (§91):** "Not: > 'AI will feed Bangladesh.'
  Instead: > **'Bangladesh has already built agricultural advisory institutions.
  KrishokTech can provide a new digital intelligence layer that makes those services
  more accessible, personalized, multimodal and scalable.'**"

- **Comparison categories used instead of named products (§Slide 2 matrix and §36
  matrix):** "Generic AI / RAG only / Vision only / KrishokTech" and
  "Generic AI / Typical agri app / Generic RAG / KrishokTech". Instruction: "Don't
  claim that all competitors have zeros. Use: > 'typical' and: > 'selected
  alternatives.'"

- **Fine-tuning insufficiency (§15):** "**Fine-tuning improved structure—but exact
  agricultural facts still required grounded knowledge.**" Sourced to the team's own
  benchmark paper, which "explicitly finds that fine-tuning alone still struggles with
  exact chemical-dose generalization."

- **Field trend (§142):** "Current agricultural GenAI literature supports the broader
  trend toward integrated RAG, structured knowledge, multimodality and human oversight."
  (cited to ACL Anthology 2026.eacl-demo.34)

### 1.5 Material atypical of a journal design brief (unverified against paper_cea.md)

Flagged as structurally non-journal content, i.e. likely absent from a CEA design brief:

1. **The entire funding/commercialisation layer**: three-layer business model
   (Layer 1 public farmer service, Layer 2 institutional service, Layer 3 government
   infrastructure); "**The farmer is the beneficiary; the scalable business is the
   advisory infrastructure for institutions, extension networks, NGOs, agribusiness
   and government.**"; five funding workstreams A–E (Knowledge, Field pilot,
   Multimodal, Deployment, Institutional integration).
2. **The capability status matrix (§117)** — a per-capability readiness ledger
   (LIVE / VALIDATED / AVAILABLE / IMPLEMENTED / IMPLEMENTED-PILOT / INTEGRATION /
   ROADMAP / DEVELOPMENT). This is a claim-scoping tool: it is the file's most precise
   statement of what may and may not be asserted as existing.
3. **The soil/irrigation field-origin story** and its explicit claim limit (§61, §119):
   soil is "replay-only in the architecture plan", so "**Field-driven expansion:
   soil/irrigation advisory under active integration.**" is the permitted wording.
4. **The four-artifact research portfolio framing (§53)** — Paper 1 "Research
   Foundation", Paper 2 "Failure Analysis", CEA "**Reliability Science**" /
   "fail-closed, evidence-bound safety architecture", EACL Demo "**Integrated System**"
   / "complete farmer-facing platform". This is the clearest statement in any of the
   three files of the intended division of labour between CEA and EACL.
5. **Deployment-language discipline (§79, §109)** — the distinction between
   "production-oriented and deployment-ready architecture" and "production deployed",
   and between "offline AI" and "offline-first pathways for verified knowledge and
   selected local capabilities".
6. Submission logistics, slide-count/word-budget allocations, QR-code strategy,
   AI-image-generation strategy, judge-persona simulation, SDG mapping
   (SDG 2 primary; SDG 9 primary; SDG 12 primary/secondary; SDG 13 secondary;
   SDG 5 conditional), demo-page features (`/showcase`, `/innovation`,
   "Compare with ordinary AI", "Funded by Bangladesh, built for Bangladesh" mode),
   30-second verbal pitch, InnovationFair/ folder layout.
7. **Nine-criterion → slide mapping table** (Originality, Practical Impact,
   Commercialization, Technical Capability, SDGs, Innovative Leadership,
   Social Inclusion, Ethics & Safety, Market Demand).
8. **Concrete social-inclusion mechanisms (§43)**: Bengali-first, dialect-tolerant,
   large touch targets, voice input (future), low-connectivity mode, free/basic farmer
   access, extension handoff. Presented as design mechanisms rather than generic claims.

---

## 2. paper_planning.md — what it contributes

### 2.0 What this document is

The **two-paper strategy document**: it defines the EACL Demo paper and the CEA journal
paper as separate artifacts, and is the origin of the CEA paper's title, hypothesis,
architecture name, RQs, section plan, experiment matrix, and overlap ledger. It states
the framing correction up front (lines 3–10):

> **I would not make your two papers "application vs. theory."**
> I would make them:
> 1. **EACL System Demonstration:** the *engineering-integrated artifact* — what KrishokTech is, how the complete system works, why the integration matters, and evidence that it is usable.
> 2. **CEA:** the *scientific architectural paper* — a generalizable **bounded-authority / fail-closed advisory architecture**, rigorously evaluated as a decision-support system.

### 2.1 Titles proposed

- **CEA working title (line 321):** "**Bounded-Authority Agricultural Advisory:
  Fail-Closed Routing and Evidence-Bound Verification for Bengali Decision Support**"
  (note: the actual manuscript title uses "Selective Resolution" in place of
  "Fail-Closed Routing", and adds "Safe").
- **EACL working title (line 60):** "**KrishokTech: A Safety-Aware Multimodal Bengali
  Agricultural Advisory System**"; alternative (line 64): "**KrishokTech:
  Evidence-Grounded and Safety-Aware Agricultural Advisory for Bengali Farmers**".

### 2.2 Named framework, mechanisms, acronyms, formalisms (exact)

**Resolution ladder (line 27)** — the transition being proposed, verbatim:
> today: safety → retrieve → generate → verify
>
> versus the proposed:
>
> **T0 deterministic safety → T1 structured resolver → T2 deterministic/template advisory → T3 grounded generation → T4 honest refusal**

with the invariant (line 33):
> **"Answer deterministically when we can prove the answer. Use the LLM only to phrase, disambiguate, or when nothing deterministic applies."**

**Authority separation (§11, lines 428–457)** — declared the deeper concept that must
supersede a bare T0–T4 story. Two logically separate dimensions per answer:
- **Linguistic authority** — "Who/what can phrase the response?"
- **Factual authority** — "Who/what is allowed to determine the agricultural claim?"

The LLM becomes a **realization layer** rather than the factual authority. Verbatim
illustration:
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
Summarised as: "> **knowledge authority → language realization**" (line 1288).

**Named architecture candidates (§73, lines 2349–2367):**
- **BAC** — Bounded Authority for Agricultural Copilots
- **BAA** — Bounded-Authority Advisory Architecture
- **SAFE-RAG** — **Safety-Aware Fact-Entailment RAG**
- **FARM-GUARD** — **Fact-Authority Routing and Mitigated Generation for Guided
  Agricultural User Recommendations and Decisions**
- Preferred: "## **BAA — Bounded-Authority Advisory**"; system name "**BAA-KrishokTech**"
- Explicit dissatisfaction with the incumbent name: "I'm not convinced 'DGDR' is the
  best final name. It sounds like primarily a routing mechanism. The deeper idea is
  authority."

**Answer metadata contract (§10, lines 405–414), verbatim:**
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

**Typed decision output of the verifier (§33, lines 1316–1321), verbatim:**
```text
CERTIFIED
CERTIFIED_WITH_WARNING
ABSTAIN
ESCALATE
```

**Verifier check list (§33):** schema validation; numerical consistency; unit
consistency; temporal validity; source binding; banned/restricted check;
crop/problem compatibility; formulation compatibility.

**Capability registry (§29, lines 1177–1199)** — verbatim contract:
```python
Capability(
    id="disease_advisory",
    can_handle=...,
    resolve=...,
    requires=...,
    available=...
)
```
Capability list proposed: `general_agri_qa`, `disease_advisory`, `pesticide_advisory`,
`crop_calendar`, `weather_advisory`, `soil`, `escalation`.

**Safety Gateway I/O (§28, lines 1152–1169)** — verbatim:
```json
{
  "query": ...,
  "image": ...,
  "context": ...
}
```
```json
{
  "risk_class": "...",
  "risk_score": 0.93,
  "action": "block|continue",
  "evidence_required": true
}
```

**Typed Agricultural Fact Store schema (§30, lines 1213–1235)** — 20 fields, verbatim:
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

**Structured fact extraction target schema (§13.3, lines 508–522)** — a shorter
13-field variant, verbatim:
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

**Temporal validity fields (§13.4, lines 533–538)** — verbatim:
```text
valid_from
valid_until
source_date
review_date
version
```

**Deterministic Resolver contract (§31, lines 1245–1255):** input
`crop + problem + stage + intent` → output `fact_id`, `answer_template`, `evidence`.
"No LLM. This is crucial."

**LLM realization prompt contract (§32, lines 1269–1282), verbatim:**
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

**Provenance chain (§34, lines 1336–1341), verbatim:**
```text
answer claim
→ structured fact
→ source node
→ source document
→ document version/date
```

**Audit event schema (§35, lines 1358–1368), verbatim:**
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

**Claim-level provenance (§52, lines 1832–1836), verbatim:**
```text
Claim 1 → Fact F21 → Source S8
Claim 2 → Fact F21 → Source S8
Claim 3 → Fact F22 → Source S9
```
with the requirement, for safety-critical fields, of "> **same authoritative record**
rather than merely 'has citation.'"

### 2.3 Formulas and metric definitions (verbatim, never paraphrased)

**Risk score (§14):**
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

**Routing policy (§14):**
$$
\text{route}(x)=
\begin{cases}
\text{block/escalate} & R(x)>r_h\\
\text{deterministic} & R(x)\le r_h \land \text{facts complete}\\
\text{RAG+verification} & \text{evidence exists but facts incomplete}\\
\text{abstain} & \text{unsupported}
\end{cases}
$$
Noted: "The exact formulation can evolve after experiments."

**Problem formulation (§25.3):**
$$
x \rightarrow (r,e,a)
$$
where "\(r\) = risk state; \(e\) = evidence state; \(a\) = action", and the action set:
$$
A=\{\text{answer},\text{fallback},\text{abstain},\text{escalate}\}
$$

**DAR — dangerous acceptance rate (§17):**
$$
DAR=\frac{\text{unsafe cases accepted}}{\text{unsafe cases}}
$$
"with 95% confidence intervals."

**FAR — false abstention/refusal rate (§17):**
$$
FAR=\frac{\text{safe cases incorrectly refused}}{\text{safe cases}}
$$
Rationale: "Because a safety system that refuses everything is useless."

**EC — evidence completeness (§51):**
$$
EC(x)=
\frac{\#\text{required safety fields supported}}
{\#\text{required safety fields}}
$$

**JEC — joint evidence completeness (§51):**
$$
JEC(x)=1
$$
"only if **all critical fields are jointly supported by one valid record/version**."
Purpose: to distinguish "> 'I found all the words somewhere'" from
"> 'I can legitimately certify the recommendation.'"

**SU — safe utility (§56):**
$$
SU = C - \lambda H - \mu F
$$
where "\(C\) = useful correct responses, \(H\) = harmful accepted responses,
\(F\) = unnecessary refusals, \(\lambda \gg \mu\)."

**Selective-routing threshold sweep (§19):**
$$
\gamma \in \{0.50,0.60,0.70,0.80,0.85,0.90,0.95\}
$$

**Other named metrics (§16 golden-benchmark scoring):** Atomic fact precision;
Atomic fact recall; Contradiction rate; Critical-field accuracy; Complete advice rate;
Appropriate abstention.

**Inter-annotator agreement already in hand (§65, line 2176):** "You already used
three agronomists in the current work, with Gwet's AC1 reported as 0.862."

### 2.4 Central hypothesis, contributions, RQs

**CEA central research hypothesis (§9, line 348), verbatim:**
> **In safety-sensitive agricultural advisory, separating factual authority from linguistic generation—using deterministic structured resolution for supported cases and fail-closed verification/fallback for unsupported cases—can reduce unsafe recommendations while retaining useful coverage and improving operational efficiency.**

**CEA main claim for the abstract (§27, line 1132), verbatim:**
> We show that treating verified agricultural facts as an explicit authority layer—rather than allowing the generator to determine safety-critical values—reduces critical factual errors while preserving useful coverage through selective deterministic and generative routing.

**CEA novelty statement (§58, line 2000), verbatim:**
> **The contribution is not a new language model or retrieval method. It is an empirically validated architecture that separates factual authority from linguistic generation, assigns queries to deterministic/generative/refusal paths based on risk and evidence completeness, and evaluates the resulting safety–coverage–latency frontier in Bengali agricultural advisory.**

**CEA contribution list — exactly three (§72):**
- **C1 — Bounded-authority architecture** separating factual authority from language generation.
- **C2 — Risk/evidence-aware selective routing** across deterministic, generative and abstention paths.
- **C3 — Comprehensive agricultural validation** of the safety–coverage–latency trade-off under Bengali, multimodal and constrained-deployment conditions.

**CEA research questions (§75), verbatim:**
- **RQ1 — Reliability:** "**Does separating factual authority from language generation reduce critical agricultural factual errors relative to LLM-only and RAG baselines?**"
- **RQ2 — Selective routing:** "**Can risk/evidence-aware routing reduce unnecessary generation while retaining useful advisory coverage?**"
- **RQ3 — Robustness:** "**How does the architecture behave under evidence corruption, temporal conflict, classifier error and adversarial input?**"
- **RQ4 — Deployment:** "**What are the latency, memory, energy and connectivity trade-offs of deterministic, generative and hybrid advisory paths?**"

**Gap statement (§25.1, line 995), verbatim:**
> Existing agricultural systems increasingly use RAG, expert facts, structured knowledge and human supervision, but the **authority relationship between deterministic agricultural facts and generative language remains insufficiently formalized/evaluated**.

**EACL contribution list — exactly three (§71):**
- C1 — Integrated Bengali agricultural advisory system
- C2 — Multimodal image-to-advisory workflow integrated with evidence-grounded NLP
- C3 — User-visible safety/provenance/verification trace for an open, reproducible system

**EACL system-contribution sentence (§7, line 302), verbatim:**
> **KrishokTech contributes an openly accessible Bengali agricultural advisory system that integrates safety screening, evidence-grounded retrieval, multimodal disease diagnosis, response verification, provenance tracing, and deployable service interfaces into a single auditable interaction workflow.**

**Overall project positioning (§80, line 2576), verbatim:**
> **KrishokTech is an open Bengali agricultural advisory platform developed around a research program on trustworthy agricultural language technology. Earlier work established the knowledge and retrieval foundations; the current system integrates multimodal diagnosis, retrieval, safety routing, evidence verification and deployment-oriented interfaces. This work then studies bounded factual authority as the reliability layer connecting those components.**

Four-paper arc (§43): **P1** Knowledge and benchmark → **P2** Retrieval uncertainty →
**P3** Decision/authority architecture (CEA) → **P4** System artifact (EACL).
"This looks like a research program, not publication slicing."

### 2.5 CEA section plan (§77), verbatim structure

```
1. Introduction
2. Related Work
3. Problem Formulation
4. Bounded-Authority Advisory Architecture
   4.1 Risk gate
   4.2 Capability routing
   4.3 Structured fact authority
   4.4 Deterministic resolution
   4.5 Generative realization
   4.6 Evidence certification
   4.7 Abstention/escalation
   4.8 Temporal/provenance controls
5. Experimental Design
   5.1 Benchmark
   5.2 Baselines
   5.3 Expert annotation
   5.4 Safety attack suite
   5.5 Deployment environments
6. Results
   6.1 End-to-end correctness
   6.2 Critical safety
   6.3 Risk–coverage
   6.4 Classifier error propagation
   6.5 Temporal/conflicting evidence
   6.6 Edge/network performance
7. Discussion
8. Limitations
9. Reproducibility
10. Conclusions
```

An earlier variant (§25) lists Section 4 as a 10-subsection architecture:
4.1 Risk gate; 4.2 Capability routing; 4.3 Structured fact layer; 4.4 Deterministic
resolution; 4.5 RAG fallback; 4.6 Evidence authority; 4.7 Verification; 4.8 Abstention;
4.9 Audit/provenance; 4.10 Edge/cache path.

**Related Work — only four clusters (§25.2):**
- Agricultural advisory systems: Farmer.Chat, KrishokBondhu, AIEP
- Agricultural GenAI/RAG: GOLDEN FACTS, Pezego-HITL, TARAG
- Multimodal agricultural decision support: recent CEA systems
- Selective/fail-closed AI: selective prediction, abstention, verification

"Don't spend 4 pages reviewing generic RAG."

**EACL section plan (§76):** 1. Introduction; 2. System Overview; 3. Architecture and
Components (3.1 Safety router, 3.2 Bengali RAG, 3.3 Multimodal diagnosis,
3.4 Verification and provenance, 3.5 Interaction/audit UI); 4. Demonstration Scenarios;
5. Evaluation (5.1 Functional validation, 5.2 Quality/safety evidence,
5.3 Performance); 6. Availability and Reproducibility; 7. Ethics / Limitations.
EACL page budgets given: Introduction ~0.6 page; System Design ~1.5 pages;
Interaction modes ~1 page; Evaluation ~1.3 pages; 6 pages total.

### 2.6 Experiment plan — the master matrix (§44), verbatim

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

Note: these E-numbers are the *planning* numbering in this file and are distinct from
the repository's `experiments/registry.yaml` E02–E26 numbering.

**E1 system ladder (§15), verbatim labels:**
- **S0 — LLM only** (no retrieval)
- **S1 — Standard RAG** (retrieve → LLM)
- **S2 — Safety-gated RAG** (safety → retrieve → LLM)
- **S3 — RAG + post-hoc verifier** (safety → RAG → LLM → verifier)
- **S4 — Structured deterministic resolver** (safety → structured facts → deterministic answer)
- **S5 — Full bounded-authority architecture** (safety → resolver → RAG fallback → verifier → abstention/escalation)

"This one experiment can carry half the paper."

**E4 authority-boundary ablation arms (§18), verbatim labels:**
- A. Free LLM composition
- B. Retrieved-context constrained generation
- C. Slot-constrained generation
- D. Single-record authority binding ("All critical slots must come from the same record.")
- E. Full authority-controlled architecture

Measured: wrong dosage; formulation mismatch; PHI errors; source mixing;
unsupported claims.

**E3 attack taxonomy (§17), verbatim five families:**
- **Evidence attacks:** mixed source records; outdated source; irrelevant high-score retrieval; contradictory sources
- **Schema attacks:** wrong crop; wrong disease; wrong formulation; missing dose; wrong unit; wrong PHI; wrong interval
- **Model attacks:** hallucinated chemical; plausible fake dose; prompt injection; instruction override
- **Perception attacks:** wrong crop; wrong disease; high-confidence misclassification
- **User attacks:** incomplete question; colloquial ambiguity; adversarial phrasing

**E6 oracle-vs-predicted routing (§20):** three metadata conditions — Oracle metadata
(perfect crop/problem metadata); Real predicted metadata; Corrupted metadata
("Intentionally introduce wrong but confident labels"). Declared "mandatory". Purpose:
"> Is the architecture robust because of verification, or only because the inputs are
accurate?"

**E7 temporal robustness (§21):** variants — current source; outdated source;
conflicting source; revised dose; withdrawn/restricted recommendation. Compare
Standard RAG vs time-aware authority layer. Measure whether the system selects current
evidence, detects conflict, refuses when validity is unresolved.

**E8 edge deployment (§22):** at least two real devices — **Low-end Android** 2–4 GB
RAM, **Mid-range Android** 6–8 GB RAM. Measure safety classifier latency; image
classifier latency; retrieval latency; network transfer; peak memory; cold start;
warm inference; energy/query if possible. Compare cloud-first vs hybrid local
safety/detection + cloud generation.

**E9 low connectivity (§23):** packet loss at "0%; 10%; 20%; 30%; maybe 50%". Compare
cloud-only / cache-first / hybrid local safety + cache + cloud. Metrics: completion;
time to usable response; stale-answer rate; unsafe-delivery rate. Framing instruction:
"Don't make 'SMS' the research paper. Make: > **service reliability under constrained
connectivity** the research question."

**E10 deterministic answer authority (§24):** repeat same query; compare LLM /
RAG+LLM / deterministic resolver; measure output variance; numeric consistency;
dosage consistency; PHI consistency; latency. Target result: "> deterministic advisory
answers are invariant when evidence is unchanged."

**Additional experiments proposed beyond the matrix:**
- **Source conflict (§53):** two sources with same crop/disease/chemical but
  `dose 1` vs `dose 2` and different dates/authority; test whether baseline RAG merges
  them, whether verifier detects conflict, whether temporal/authority resolver chooses
  correctly or abstains.
- **"LLM can paraphrase but cannot mutate" (§54):** generate 500 deterministic fact
  records, have several LLMs verbalize them in Bengali, check numerical mutations;
  omitted fields; unit changes; PHI changes; crop substitutions; formulation
  substitutions. Compare unconstrained prompting vs schema-locked prompting vs
  post-verification.
- **Unsupported question (§55):** crop not covered; disease not in corpus; treatment
  missing; formulation missing; ambiguous image; out-of-date record. "Measure: > does
  the system invent something?"

**Benchmark construction plan (§64 Phase 3):** "### 3–5k realistic Bengali queries"
labelled with safe/unsafe; answerable/unanswerable; fact requirements; risk; gold
agricultural answer; acceptable abstention; source authority. Plus "### 1–2k
adversarial cases." Rules: "Do not evaluate on data used to engineer the rules.
Freeze this test set **before final tuning**."

**Expert annotation (§65 Phase 4):** "at least **3 agronomists** independently annotate
a substantial subset"; measure agreement; difficult-case rate; correctness; safety;
completeness.

**Controlled-evaluation protocol (§66 Phase 5):** all ablations under the same model;
retrieval corpus; prompts; query set; hardware; seeds; decoding settings → "one
canonical results ledger", "reproducible from one command".

**Crop scope (§50):** for CEA use "**2–4 high-risk crop/use-case families** with rich
structured facts and expert validation", e.g. rice; potato; chili; brinjal. For the
demo, "show more of the available crop/vision system."

### 2.7 Target headline results

**CEA headline results (§45), verbatim — and what must NOT be headlined:**
Not "26 evaluations completed", not "2,135 nodes", not "61.52% zero-LLM". Instead:
- **Result 1 — Critical agronomic errors decrease substantially under authority-bound verification.**
- **Result 2 — Deterministic resolution provides exact/invariant handling for evidence-complete queries.**
- **Result 3 — Selective routing retains useful coverage while reducing unnecessary generation.**
- **Result 4 — The system remains usable under constrained connectivity/edge conditions.**

**Desired qualitative result shape (§57), verbatim — explicitly not target values
("I am not going to invent target values"):**
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

**EACL headline results (§46):** Result 1 Integrated Bengali conversational advisory;
Result 2 Integrated image-to-advisory workflow; Result 3 Traceable evidence and
verification UI; Result 4 Open/reproducible software; Result 5 Representative
quality/safety/performance validation.

### 2.8 Material-relocation table (§78), verbatim

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

"This is the surgery I would perform."

### 2.9 Build/implementation plan tied to the papers

**Must build (§49):** capability registry; structured fact layer; deterministic
resolver; authority metadata; temporal validity; verifier; risk-aware routing;
audit event schema; resolution tier in API; proper evaluation harness.
**Nice to build:** admin review queue; operator dashboard; source version management;
feedback loop; cache updates.
**Do not prioritize for the papers:** elaborate monetization; dozens of frontend
routes; generalized marketplace; every future module.

**Eight-layer implementation stack (§28–§35):** Layer 1 Safety Gateway; Layer 2
Capability Registry; Layer 3 Typed Agricultural Fact Store; Layer 4 Deterministic
Resolver; Layer 5 LLM realization; Layer 6 Verification; Layer 7 Provenance;
Layer 8 Audit.

**Seven-phase work order (§64–§68):** Phase 1 Freeze the research identity
("bounded authority + selective routing + evidence verification"); Phase 2
Re-architect the application (9 numbered components); Phase 3 Build the benchmark;
Phase 4 Expert annotation; Phase 5 Controlled evaluation; Phase 6 Physical deployment
test (phone / laptop or low-end PC / server-cloud, measuring RAM, inference, network,
energy); Phase 7 Build the EACL demo.

**Mechanisms to borrow from current literature but not claim (§13, §36):**
1. Hybrid retrieval (BM25 + dense + RRF) — already present
2. Query rewriting — "Bengali normalization/rewriting stage, but only as a retrieval aid"
3. Structured fact extraction
4. Temporal validity — from TARAG
5. Evidence graph / relation constraints — "Don't need a giant KG. A typed relational layer is enough."
6. Confidence calibration — safety classifier, disease classifier, retrieval confidence
7. Selective prediction — risk–coverage analysis
8. Human-in-the-loop escalation — from Pezego-HITL
9. Multimodal uncertainty — "Do not assume image diagnosis is correct. Pass its uncertainty into advisory routing."
10. Audit/event trace — "Already built—make it experimentally useful."

### 2.10 EACL demo interactions specified here

- **Interaction 1 (§68):** Bengali query "আমার আলু গাছে দেরিতে পচা রোগ হয়েছে, কী ওষুধ দেব?"
  → visible trace, verbatim:
  ```text
  ✓ Safety checked
  ✓ Agricultural intent recognized
  ✓ Structured evidence available
  ✓ Deterministic resolution selected
  ✓ Source verified
  ✓ Dose verified
  ```
  then Bengali answer, then a "**Why this answer?**" click showing
  "fact → source → date → verifier."
- **Interaction 2 (§69):** leaf image → Image quality → Crop prediction →
  Disease prediction → Confidence → Agricultural evidence → Advice →
  Safety verification.
- **Interaction 3 (§70):** banned/restricted treatment request →
  ```text
  ⚠ High-risk query
  → generation not invoked
  → advisory blocked
  → escalation route
  → audit event
  ```
- **Four scenario set (§5):** Scenario A Ordinary Bengali advisory (query
  "ধানের পাতায় বাদামী দাগ হয়েছে, কী করব?"); Scenario B Chemical safety;
  Scenario C Image advisory; Scenario D Uncertain query. "This fourth scenario is
  critical. The **refusal behavior** is part of what makes the system distinctive."
- Existing API/UI trace already returns source entries, confidence state,
  `agent_trace`, verifier flags, model information; frontend renders
  "Checking safety → Retrieving sources → Generating answer → Verifying."
