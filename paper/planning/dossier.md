You were right to stop me. **The supporting artifact should be one serious PDF dossier, authored in LaTeX, not another PPT.** The 7–8 slide PPT is the mandatory screening deck; the optional “Supporting File / Document Related to the Current Status” is where we should put the deeper evidence package. The official form confirms the main presentation is strictly PPT/PPTX, while the supporting-document field is separate and has no public format restriction shown on the form. ([Innovation Fair][1])

And I corrected the most important research mistake you flagged: **KrishokTech v2 is not the old 145,500-instance story.** The authoritative v2 paper is the 26-page paper, *“KrishokTech: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory,”* with **85,979 core benchmark instances across four tracks + a 1,000-query Real-World Farmer Benchmark**, built from **284 government publications, 13 institutions, six Bengali dialects, and 2,946 semantic knowledge units**. Its released tracks are 28,993 General QA, 11,224 Treatment QA, 20,112 Safety Refusal/Re-query, and 25,650 Table QA. ([arXiv][2])

The current Hugging Face repository has a larger row count because the released dataset representation contains additional/configured rows; that is **not** what I will use as the headline v2 benchmark count. The paper's 85,979 core-instance figure is the correct number for the research story. ([Hugging Face][3])

So below is the **reset, final execution specification for the supporting PDF only**.

---

# 1. What this PDF actually is

This is **not**:

* a second presentation;
* a compressed version of the CEA paper;
* a collection of certificates;
* a publication list;
* a technical manual;
* a 100-page dump of every experiment.

It is:

# **The KrishokTech Innovation Due-Diligence Dossier**

Its job is to answer, in order:

> **Where did this come from?**
> **What did you discover?**
> **What did you actually build?**
> **Why is the architecture different?**
> **What evidence supports it?**
> **Can it operate outside a lab?**
> **Who can use it?**
> **How can it be commercialized?**
> **What would funding unlock?**

The official Fair says its mission is explicitly to move innovations from **research and experimentation into practical application, enterprise and market**, connecting innovators with industry, investors, government, universities and financial institutions. That means this supporting PDF should be written like **technical due diligence for a promising national innovation**, not like an academic appendix. ([Innovation Fair][4])

---

# 2. The PDF's narrative spine

The entire document should follow exactly this causal chain:

```text
FIELD EXPERIENCE
      ↓
A REAL BANGLADESH PROBLEM
      ↓
WE INVESTIGATED THE PROBLEM
      ↓
OUR FIRST RESEARCH REVEALED THE KNOWLEDGE GAP
      ↓
OUR SECOND RESEARCH REVEALED THE RETRIEVAL GAP
      ↓
THOSE FAILURES DETERMINED THE SYSTEM ARCHITECTURE
      ↓
KRISHOKCHAT BECAME AN INTEGRATED ADVISORY PLATFORM
      ↓
WE TESTED ITS SAFETY / RELIABILITY / DEPLOYABILITY
      ↓
WE ENGINEERED IT TOWARD PRODUCTION
      ↓
THE NEXT STEP IS FIELD VALIDATION + INSTITUTIONAL SCALE
```

Every section must answer the previous section's unresolved question.

That is the single most important writing rule.

---

# 3. Final PDF length

My recommendation:

## **24–30 pages**

Not because “more pages is better.”

Because this is enough room to tell the entire story **without making every page dense**.

A good target is:

* 2 cover/opening pages
* 4 origin/research pages
* 5 system pages
* 8 evidence pages
* 4 deployment/business pages
* 2 roadmap/closing pages
* optional appendix

So approximately **27 pages**.

That is a serious supporting dossier.

---

# 4. Final PDF title

Use:

# **KRISHOKCHAT**

## **From Field Problem to Deployable Agricultural Intelligence**

Subtitle:

> **Current Status, Research Evidence, System Architecture and Deployment Pathway**

Do not put:

> “Funding Proposal”

in the title.

Do not put:

> “Technical Report”

either.

“Current Status, Research Evidence and Deployment Pathway” communicates exactly what the document is.

---

# 5. Page 1 — Cover

## Exact text

# KRISHOKCHAT

## From Field Problem to Deployable Agricultural Intelligence

**Current Status, Research Evidence, System Architecture and Deployment Pathway**

A Bengali-first agricultural advisory platform designed for farmers and the institutions that support them.

**Research → Evidence → Engineering → Validation → Deployment**

Bangladesh · 2026

### Visual

Do **not** generate the whole page with GPT.

Use:

* one actual field photograph;
* one actual KrishokTech UI crop/screenshot;
* subtle agricultural background;
* clean typography.

The cover should immediately communicate:

> real field + real software + research depth.

---

# 6. Page 2 — Executive Overview

## Title

# **What KrishokTech is today**

This page should be almost entirely visual.

### Left

A concise paragraph.

### Right

Six capability cards.

## Exact body text

KrishokTech is a Bengali-first agricultural intelligence platform built to help farmers obtain useful agricultural guidance without requiring specialist terminology, constant access to an expert, or uninterrupted connectivity.

The platform brings together conversational agricultural question answering, evidence-grounded retrieval, crop and disease image analysis, safety screening, response verification, provenance, auditability and constrained-delivery pathways in one system. The engineering direction is deliberately broader than a chatbot: KrishokTech is being developed as a reusable advisory platform that can support farmers directly and, through the same infrastructure, extension officers, NGOs, agribusinesses and public agricultural services.

### Six cards

**Bengali interaction**

**Agricultural evidence**

**Crop & disease vision**

**Safety & verification**

**Low-connectivity support**

**Production-oriented infrastructure**

Bottom line:

> **The product is already built; the next stage is field validation and institutional deployment.**

---

# 7. Page 3 — Why the project started

## Title

# **The project started with a field problem, not a model**

This is your human-origin page.

Use the real field photographs you mentioned.

### Exact copy

Our starting point was practical. We went to farmers, listened to the questions they were already trying to solve, and observed the conditions under which agricultural decisions are actually made. The problems did not arrive one at a time. Language, disease recognition, treatment decisions, irrigation and soil questions, access to expertise and network availability were often part of the same situation.

That changed the design objective.

We were not trying to build another agricultural chatbot. We were trying to build an agricultural advisory system that could remain useful when the farmer's language was informal, the information was incomplete, the decision was safety-sensitive, and the connection was unreliable.

### Pull quote

# **“The farmer's real problem is not simply lack of information. It is getting the right information, in the right form, at the moment a decision has to be made.”**

---

# 8. Page 4 — The problem we chose to solve

## Title

# **Why ordinary digital advice is not enough**

Create one large visual:

```text
FARMER
  │
  ├── speaks colloquially
  ├── may use Banglish / dialect
  ├── may not know disease name
  ├── may only have a photo
  ├── may ask an incomplete question
  └── may have weak connectivity
          ↓
    ADVISORY SYSTEM
          ↓
  MUST STILL PRODUCE
  A SAFE, USEFUL RESPONSE
```

Then three short subsections.

### Language

> Official agricultural documents are usually written differently from how farmers ask questions.

### Knowledge

> A plausible agricultural answer can still be wrong when chemical identity, formulation, dose, timing or crop applicability is misbound.

### Delivery

> A correct answer is not useful if it cannot reach the farmer under the available connectivity conditions.

The CEA manuscript already makes this distinction explicitly: treatment advice can become unsafe through wrong chemical identity, formulation, dose, interval, PHI or crop applicability; network and message constraints are distinct last-mile failure surfaces. 

---

# 9. Page 5 — The first research foundation

## Title

# **Before building the advisor, we built the evidence foundation**

This is the v2 paper.

### Exact copy

Our first major research contribution was a provenance-traceable Bengali agricultural benchmark designed specifically for agricultural knowledge, treatment advice, safety behavior and structured reasoning.

The released KrishokTech v2 benchmark contains 85,979 core instances across four tracks: General Knowledge QA, Treatment QA, Safety Refusal and Re-query, and Table QA. The resource is built from 284 government agricultural publications across 13 institutions and six Bengali dialects, with every benchmark instance linked back to its originating semantic knowledge unit and source publication.

The benchmark was deliberately designed to separate what is often collapsed into a single “agricultural QA” score: ordinary agricultural knowledge, safety-critical treatment advice, refusal/clarification behavior, and reasoning over structured agricultural tables.

### Metrics visual

**284 publications**

**13 institutions**

**6 Bengali dialects**

**2,946 semantic knowledge units**

**85,979 core benchmark instances**

**1,000 real-world farmer queries**

These numbers are directly supported by v2. ([arXiv][2])

---

# 10. Page 6 — What v2 taught us

## Title

# **The first lesson: better language behavior does not automatically produce safe agricultural advice**

This is the crucial transition.

Use a simple chart:

```text
MODEL SCALE
    ↑
    │
    │        ─── no reliable guarantee of treatment correctness
    │
    └────────────────────────────→
```

Then show actual findings.

### Closed-book

Gemini-2.5-FL Treatment Correct: **43.64%**

Gemma-4-26B: **38.73%**

LLaMA-3.1-8B: **12.43%**

Qwen-2.5-7B: **13.29%**

GPT-OSS-120B: **32.92%**

### Oracle evidence

Treatment hallucination remains **4.05–7.00%** across the evaluated systems.

These are from v2. ([arXiv][2])

### Exact conclusion

> **Evidence helps. But evidence supplied to a generator is not the same thing as evidence enforced by the system.**

That sentence should be large.

---

# 11. Page 7 — Real farmer language changed the problem

## Title

# **The second lesson: the farmer does not speak in benchmark language**

Explain v2's Farmer Benchmark.

### Exact copy

The benchmark's controlled tracks were not enough. We therefore kept a separate Real-World Farmer Benchmark to test whether research behavior transfers to actual advisory-style questions.

The 1,000-query benchmark was collected independently of benchmark construction. Three hundred queries came from structured field interviews with smallholder farmers in Rajshahi and Natore; the remaining queries came from agricultural Facebook communities and a farmer question-and-answer portal. The evaluation split contains 350 queries.

These questions are shorter, more colloquial and often less complete than benchmark-generated questions. That difference matters because a system can perform well on a clean agricultural question and still fail when the farmer does not name the crop, describes a symptom indirectly, or uses local terminology.

The v2 paper explicitly describes this independent collection and the 300 field-interview queries. ([arXiv][2])

---

# 12. Page 8 — The retrieval paper

## Title

# **Then we asked a different question: where does retrieval fail?**

Use the actual second paper title:

> **Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory**

Then exact copy:

Our second research study treated retrieval failure as its own problem rather than hiding it behind an end-to-end chatbot score.

Across 1,000 evaluation queries and 2,882 knowledge nodes extracted from 284 official Bangladeshi agricultural publications, we compared five retrieval architectures and six embedding models under different language conditions.

The result was not that one retriever always wins. The stronger finding was that retrieval behavior changes with the form of the question. Colloquial farmer language, formal Bengali, and other language conditions create different failure patterns, and therefore an agricultural advisory system should not assume that text retrieval is equally reliable for every farmer query.

The published arXiv abstract gives the exact study design and headline finding: Hybrid RRF reaches overall R@10 0.539, while dense retrieval falls sharply on colloquial farmer queries; BM25 is strong for native Bengali and degrades heavily on English-to-Bengali retrieval. ([arXiv][5])

---

# 13. Page 9 — The turning point

## Title

# **The research changed our architecture**

This page is incredibly important.

Create a left/right visual.

### LEFT

**What we initially had**

```text
Question
   ↓
Retrieve
   ↓
Generate
   ↓
Answer
```

### RIGHT

**What the evidence demanded**

```text
Question / Image
      ↓
Understand context
      ↓
Assess safety and uncertainty
      ↓
Route to the appropriate capability
      ↓
Use structured evidence where possible
      ↓
Generate only where necessary
      ↓
Verify before delivery
      ↓
Answer / Clarify / Refuse / Escalate
```

### Exact bridge text

> **The system architecture is therefore not a collection of features added around a chatbot. It is the engineering response to the failure modes identified by the research program.**

This sentence connects your papers to the product naturally.

---

# 14. Page 10 — The complete KrishokTech architecture

## Title

# **One platform, one advisory case, multiple evidence paths**

This is the largest diagram in the document.

Use:

```text
                    FARMER
          ┌─────────┼──────────┐
          │         │          │
         TEXT      IMAGE      VOICE*
          │         │          │
          └─────────┼──────────┘
                    ↓
            CONTEXT & SAFETY
                    ↓
              CASE STATE
                    ↓
            CAPABILITY ROUTER
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       STRUCTURED  RAG       VISION
        FACTS               MODELS
          │         │         │
          └─────────┼─────────┘
                    ↓
          AGRICULTURAL EVIDENCE
                    ↓
            RESPONSE ENGINE
             ┌──────┴──────┐
             ↓             ↓
       DETERMINISTIC    LLM REALIZATION
             │             │
             └──────┬──────┘
                    ↓
               VERIFICATION
                    ↓
       ┌────────────┼────────────┐
       ↓            ↓            ↓
     ANSWER      CLARIFY      ESCALATE
                    │
                    ↓
        WEB / LOCAL / CACHE / SMS
```

`*` only show voice if it is actually deployed by the time the PDF is finalized.

---

# 15. Page 11 — The farmer journey

## Title

# **The system is designed around a real advisory interaction**

Show four screenshots.

### Step 1

Ask in Bengali.

### Step 2

Add a crop image.

### Step 3

Inspect evidence.

### Step 4

Receive advice or clarification.

Use short labels:

> **Ask**

> **Understand**

> **Verify**

> **Act**

### Text

KrishokTech treats a farmer interaction as a case rather than a single prompt. The system can carry the farmer's question, available crop context, image evidence, retrieved agricultural sources, verification status and subsequent follow-up within the same advisory flow.

This allows different capabilities to contribute to the same decision instead of forcing the farmer to understand which technical tool should be used first.

---

# 16. Page 12 — Bengali and farmer-language layer

## Title

# **Built for the language farmers actually use**

Show examples:

```text
Formal Bengali
“আলুর লেট ব্লাইট রোগের ব্যবস্থাপনা কী?”

Farmer-style Bengali
“আলুর পাতায় কালা দাগ পড়ছে কি করুম?”

Banglish
“alu te pata kalo hoye jacche ki korbo?”
```

Then a conceptual normalization flow:

```text
Farmer expression
      ↓
Language normalization / interpretation
      ↓
Agricultural entity
      ↓
Evidence retrieval
```

### Important wording

Don't say:

> “we understand every Bengali dialect.”

Say:

> **“The system is designed and evaluated for multiple Bengali registers and dialect conditions.”**

Your current evaluation reports detection-gated coverage gains from 42.9% to 89.8% for regional dialects and 41.6% to 90.0% for Romanized Banglish in the specified evaluation. 

---

# 17. Page 13 — Multimodal diagnosis

## Title

# **A crop image becomes evidence for the same advisory case**

Diagram:

```text
PHOTO
 ↓
Crop classification
 ↓
Crop-specific disease model
 ↓
Confidence
 ↓
Agricultural knowledge
 ↓
Advisory
```

Then a real UI screenshot.

### Exact paragraph

The vision workflow is deliberately integrated with the advisory layer. A photograph is not treated as an isolated classification task. The predicted crop and disease become structured context for downstream agricultural retrieval and advice.

This separation also allows uncertainty to propagate. A low-confidence or contradictory visual prediction does not have to become a confident agricultural recommendation; it can instead trigger clarification or another evidence path.

The existing system documentation describes crop classification followed by per-crop disease routing, while the CEA work explicitly treats the vision output as routing metadata rather than claiming a new detector. ([github.com](https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System)) 

---

# 18. Page 14 — The important new multimodal feature

## Title

# **When evidence disagrees, KrishokTech asks before it acts**

This is one of the features I would absolutely build before final PDF generation.

Show:

```text
TEXT: Tomato
IMAGE: Potato (0.91)

       ⚠ CONFLICT

“Your message and image suggest different crops.
Please confirm before I continue.”
```

### Exact explanation

> **A multimodal system should not silently choose whichever signal is more convenient. Conflicting evidence is itself a system state.**

Then perhaps:

> Confirm text

> Use image

> Upload another image

This is simultaneously:

* a good product feature;
* a good safety feature;
* a good system-demonstration feature;
* strong material for the CEA evaluation.

Your current E31 already has a cross-modal-conflict experiment reporting 100% clarification triggering and 0% CUAR in the evaluated BAA configuration. 

---

# 19. Page 15 — The system's safety boundary

## Title

# **Safety is a system state, not a disclaimer**

Large visual:

```text
                 USER INPUT
                      ↓
                 SAFETY GATE
              ┌───────┼────────┐
              ↓       ↓        ↓
            SAFE    UNCLEAR   UNSAFE
              ↓       ↓        ↓
            ROUTE   CLARIFY   BLOCK
```

Then:

> **Unsafe → no normal generation path**

### Exact copy

KrishokTech treats safety-sensitive agricultural requests differently from ordinary information requests. The safety layer can terminate a request before retrieval or generation, while evidence and verification layers provide a second boundary for responses that reach the advisory path.

This creates multiple opportunities to stop a harmful recommendation: before retrieval, during evidence resolution, after generation, and before constrained delivery.

The current application implements six safety categories and terminal handling before retrieval, with a local audit trail. ([github.com](https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System))

---

# 20. Page 16 — Why the structured treatment contract matters

## Title

# **An agricultural treatment is not a sentence. It is a set of linked facts.**

Use a visually elegant 11-field record:

```text
Crop
Problem
Growth stage
Active ingredient
Formulation
Dose min
Dose max
Unit
Volume
Application interval
PHI
Regulatory status
```

You can call it:

# **Agricultural Treatment Record**

Don't overwhelm the reader with the algorithm.

### Exact paragraph

For safety-critical treatment advice, correctness depends on relationships among fields rather than the presence of individual words.

A recommendation can contain the right chemical name and still be unsafe if the dosage belongs to another crop, the formulation is different, the pre-harvest interval is unsupported, or the recommendation comes from an obsolete or conflicting source. KrishokTech therefore represents critical treatment information as a typed relational record and requires the necessary fields to remain jointly supportable before certification.

This reflects the existing CEA contract and its 11-slot relational verification design. 

---

# 21. Page 17 — The strongest evidence-binding result

## Title

# **The verifier is not just checking whether words appear. It checks whether the facts belong together.**

This should be one of the most visually impressive evidence pages.

Create a table:

| Method                        | Correct evidence certified | Counterfactual evidence certified |
| ----------------------------- | -------------------------: | --------------------------------: |
| Vanilla RAG                   |                     100.0% |                            72.65% |
| Lexical matcher               |                     100.0% |                            59.55% |
| LLM judge                     |                      95.7% |                            38.65% |
| **Typed relational verifier** |                 **100.0%** |                          **0.0%** |

Then:

# **CBC = 1.000**

### Exact explanatory text

We tested the verification boundary by deliberately changing evidence that should change a recommendation—for example, scaling the dose, shortening the pre-harvest interval, or substituting incompatible evidence.

A system that merely searches for matching words can still certify the corrupted answer. The typed relational verifier instead checks whether the complete recommendation remains supported by a valid record.

In the current 2,000-pair counterfactual benchmark, the typed verifier certified 0.0% of corrupted cases, while Vanilla RAG certified 72.65%.



---

# 22. Page 18 — Why each safety field matters

## Title

# **The safety schema changes behavior**

Use a ranked horizontal bar chart.

Exact values from your current 10,000-case slot-ablation study:

| Removed constraint    | Dangerous acceptance increase |
| --------------------- | ----------------------------: |
| Dosage bounds         |                      +31.6 pp |
| Regulatory polarity   |                      +17.8 pp |
| Active ingredient     |                      +14.2 pp |
| Host crop             |                      +11.4 pp |
| Target pathogen       |                       +8.2 pp |
| Volume denominator    |                       +7.1 pp |
| Formulation           |                       +5.8 pp |
| Unit                  |                       +5.4 pp |
| Growth stage          |                       +4.9 pp |
| PHI                   |                       +2.7 pp |
| Interval              |                       +1.9 pp |
| All typed constraints |                  80.0% hazard |

The full tested configuration had zero observed dangerous acceptance. 

### Exact interpretation

> **The schema is not administrative metadata. Removing different fields creates measurably different safety failures, with dosage, regulatory status and active ingredient producing the largest individual effects in the evaluated attack suite.**

This is excellent evidence.

---

# 23. Page 19 — Retrieval failure and safe degradation

## Title

# **When retrieval gets worse, the system degrades by refusing—not by inventing**

This is another killer page.

Show four states:

```text
Gold evidence
↓
Noise
↓
Contradictory evidence
↓
No evidence
```

Current results:

| Evidence condition | Vanilla RAG hazard | KrishokTech hazard |
| ------------------ | -----------------: | -----------------: |
| Gold               |              10.0% |               0.0% |
| Noisy              |              19.2% |               0.0% |
| Contradictory      |              33.2% |               0.0% |
| Omitted            |              23.2% |               0.0% |

Current KrishokTech safe-abstention rates increase as evidence quality deteriorates. 

### Exact paragraph

This is one of the most important design decisions in the system.

Retrieval failure should reduce confidence in the answer, not increase the model's freedom to improvise. We therefore evaluate degradation as a first-class operating condition. As authoritative evidence disappears or is replaced by contradictory material, the system is allowed to lose coverage through abstention rather than preserving a superficially high answer rate by guessing.

---

# 24. Page 20 — Multiple generators, one safety boundary

## Title

# **The safety layer is intended to outlive the model**

Use three models:

* Gemma-4
* Llama-3
* Qwen-2.5

Current result:

| Model       | Raw RAG hazard | Verified hazard |
| ----------- | -------------: | --------------: |
| Gemma-4     |          7.40% |           0.00% |
| Llama-3-8B  |         11.80% |           0.00% |
| Qwen-2.5-7B |         13.60% |           0.00% |

Coverage differs, but the tested safety boundary remains unchanged. 

### Exact statement

> **The application does not need one perfect language model to become operationally trustworthy. It needs a model-independent boundary around the claims the system is willing to certify.**

That's a very strong innovation-fair statement.

---

# 25. Page 21 — Bengali robustness

## Title

# **Local language variation should not force unsafe behavior**

Show:

### Standard Bengali

> text-first → lower
> gated → higher

### Farmer language

> text-first → lower
> gated → higher

### Regional dialect

> 42.9% → 89.8% coverage

### Banglish

> 41.6% → 90.0% coverage

Current E21 gives these coverage values and zero observed dangerous acceptance over 4,000 queries. 

### Exact text

The goal is not to claim that Bengali language variation has been solved. The practical goal is narrower and more useful: when language becomes difficult for retrieval, the system should have alternative evidence paths and safe fallback behavior rather than converting linguistic uncertainty into unsupported agricultural advice.

---

# 26. Page 22 — Expert validation

## Title

# **The system was reviewed by agricultural experts, not only by software tests**

Use huge numbers:

# **200**

responses

# **3**

agronomists

# **4.82 / 5**

mean correctness

# **100%**

chemical safety pass

# **98.5%**

evidence traceability

# **96.5%**

deployment approval

# **0.862**

Gwet's AC1 on safety

These values are from the current uploaded results. 

### Exact paragraph

Automated testing is necessary but not sufficient for agricultural deployment. We therefore included a double-blind expert review of 200 representative advisory outputs by three certified agronomists.

KrishokTech received a mean correctness score of 4.82/5, a 100% chemical-safety pass rate in the evaluated sample, 98.5% evidence traceability, and 96.5% deployment approval. The resulting safety agreement was Gwet's AC1 = 0.862.

These results do not replace field validation, but they provide a second form of evidence: the structured safety behavior was evaluated by agricultural specialists rather than judged only by the system itself.

---

# 27. Page 23 — Multimodal uncertainty

## Title

# **When vision is uncertain, uncertainty is passed forward**

Show:

```text
Image
 ↓
Crop prediction
 ↓
Disease prediction
 ↓
Confidence
 ↓
Conflict / uncertainty?
 ├── NO → evidence
 └── YES → clarification
```

Current E31 reports:

> 100% clarification triggering under its cross-modal BAA test, with 0% CUAR and no chemical-cocktail delivery in the 100 tested cases. 

### Exact text

> **A prediction is an input to the advisory system, not permission to act.**

That sentence should be highlighted.

---

# 28. Page 24 — Offline and last-mile delivery

## Title

# **A correct recommendation still fails if it cannot reach the farmer**

Visual:

```text
ONLINE
   ↓
Remote advisory

LIMITED CONNECTION
   ↓
Cached / local evidence

OFFLINE
   ↓
Verified local pathways

CONSTRAINED CHANNEL
   ↓
Deterministic SMS
```

Use the current network results carefully.

### At 15% packet loss

Cloud-only: **82.0%**

Offline-first cache: **91.4%**

### At 30% packet loss

Cloud-only: **12.8%**

Offline-first cache: **58.1%**

These are simulation results, not carrier measurements. 

### Exact text

> **The design treats connectivity as part of the advisory system, not as an external assumption.**

Then explicitly:

> **Controlled network simulation; carrier-level performance remains a deployment validation task.**

This is the right tone.

---

# 29. Page 25 — Constrained channels

## Title

# **The same safety contract survives the last mile**

Show SMS template.

Current E15:

* deterministic template: 102–115 chars;
* selected dosage / interval / PHI fields preserved;
* LLM-composed control: 64.4% critical-hazard rate under the test definition. 

Current E22:

* deterministic template: 0/1,400 injection leakage;
* LLM-generated SMS: 509/1,400 leakage. 

### Exact statement

> **When a message must be compressed, we do not ask the language model to decide which safety fields can disappear. The certified structured record is rendered through a deterministic delivery format.**

Excellent engineering story.

---

# 30. Page 26 — LLM dependency and efficiency

## Title

# **Use generation where it adds value; do not pay for it when the answer is already known**

Show:

```text
5,000-query workload

T0 Safety             6.40%
T1 Detection→Facts   32.22%
T2 Templated facts   18.82%
T3 LLM               38.48%
T4 Refusal            4.08%
```

Then:

# **51.04%**

of the workload takes deterministic advisory paths.

# **61.52%**

reaches a zero-LLM terminal path when safety/refusal are included.

Current weighted latency:

> 546.15 ms vs 1,247.93 ms

The current evidence reports these values. 

### Exact language

> **The point is not to eliminate LLMs. The point is to stop using a generative model as the default authority for every agricultural question.**

---

# 31. Page 27 — Production orientation

## Title

# **The software architecture was designed to evolve into a service**

Show the real repository structure:

```text
frontend/
backend/
capstone/
dataset_release/
demo-assets/
deploy/
docs/
paper/
production/future_plan/
research_artifacts/
scripts/
tools/
```

The current GitHub repository explicitly contains these areas and 193 commits. ([GitHub][6])

Then show:

### Modular backend

### Model-provider abstraction

### Health/readiness

### Audit trail

### Deployment scripts

### Research/replay infrastructure

### Versioned evidence assets

### Automated tests

Current result baseline:

**558 backend tests passed**

**8 skipped**

**0 failed**

**50/50 golden replay**

**frontend build green** 

### Exact paragraph

KrishokTech is not tied to one model provider, one retrieval implementation, or one frontend workflow. The codebase separates application logic from infrastructure adapters, keeps research artifacts separate from runtime assets, and provides explicit deployment, audit and testing layers.

This matters commercially because the agricultural knowledge, models and external services will change over time. The platform therefore has to accommodate new models, new evidence packs, new crops and new delivery channels without forcing a complete rebuild.

---

# 32. Page 28 — Knowledge can grow without rebuilding the product

## Title

# **The long-term asset is not only the model—it is the governed agricultural knowledge layer**

This is where E24 belongs.

Current observation:

* 2 BARI-verified facts added;
* 18 minutes;
* 55-query cluster;
* coverage 58.7% → 64.2%. 

Do not claim:

> general authoring speed.

Write:

> **A targeted knowledge intervention in one chili-anthracnose cluster increased coverage from 58.7% to 64.2% in the evaluated sample.**

Then visual:

```text
Authoritative source
      ↓
Fact extraction
      ↓
Validation
      ↓
Versioned knowledge pack
      ↓
Advisory system
```

### Big strategic statement

> **Knowledge improvement becomes an update to the platform, not a rebuild of the application.**

---

# 33. Page 29 — Governance and provenance

## Title

# **Every important agricultural claim should remain traceable after deployment**

Show a provenance chain:

```text
Source publication
      ↓
Semantic unit
      ↓
Structured fact
      ↓
Advisory claim
      ↓
Verification
      ↓
Delivered response
```

Then current E23:

* 1,000 mutation tests;
* 1,000/1,000 detected;
* hash-chained evidence pack;
* ~791-byte delta vs 10,985-byte full pack;
* 0.1919ms p95 verification in the tested client workflow. 

### Exact text

> **The objective is not merely to cite a source. It is to preserve the path from the source to the specific agricultural fact that the system was willing to certify.**

---

# 34. Page 30 — Operational resilience

## Title

# **When something fails, the system should degrade deliberately**

Create a failure matrix:

| Failure                     | Preferred behavior                  |
| --------------------------- | ----------------------------------- |
| Unsafe query                | Block                               |
| Missing context             | Clarify                             |
| Unsupported fact            | Abstain                             |
| Evidence conflict           | Reject / escalate                   |
| Stale source                | Invalidate                          |
| Vision/text conflict        | Clarify                             |
| Remote LLM unavailable      | Local/deterministic path            |
| Dense retrieval unavailable | Alternate retrieval                 |
| Network unavailable         | Cached/local path                   |
| SMS too long                | Deterministic refusal/recomposition |

This page should make the project look **operational**, not merely intelligent.

---

# 35. Page 31 — The complete research-validation matrix

## Title

# **What has been tested**

This is where we finally allow density.

Use a structured matrix, not prose.

### Safety

* relational misbinding;
* slot ablation;
* counterfactual evidence;
* prompt injection;
* retrieval poisoning;
* stale evidence;
* source fragmentation;
* model variation.

### Language

* standard Bengali;
* farmer language;
* regional dialect;
* Banglish;
* normalization.

### Multimodal

* crop classification;
* disease classification;
* cross-modal conflict;
* confidence uncertainty.

### Deployment

* latency;
* local inference;
* cache;
* degraded networks;
* GSM composition;
* provenance updates;
* knowledge maintenance.

### Human

* expert correctness;
* safety;
* evidence traceability;
* deployment approval.

Bottom:

> **The evaluation program is broader than any single benchmark because the system has multiple failure surfaces.**

---

# 36. Page 32 — What the evidence says

## Title

# **Five conclusions we can support today**

This is a very important synthesis page.

### 01

> **Agricultural generation cannot be treated as a purely linguistic problem.**

Supported by v2.

### 02

> **Retrieval quality changes with farmer language and query condition.**

Supported by your retrieval study. ([arXiv][5])

### 03

> **Evidence binding must respect agricultural relationships, not only lexical overlap.**

Supported by counterfactual + slot ablation.  

### 04

> **The system can trade answer coverage for safer behavior instead of guessing.**

Supported by retrieval degradation / selective behavior. 

### 05

> **The application has a viable engineering path from research prototype toward deployment.**

Supported by codebase, deployment layers and test infrastructure—not by field adoption.

Then a final line:

# **These findings led us to build KrishokTech as a platform, not a chatbot.**

---

# 37. Page 33 — Commercial model

## Title

# **Designed as shared advisory infrastructure**

Do not make this a generic startup slide.

Use:

```text
                 KRISHOKCHAT
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       FARMERS      NGOs       GOVERNMENT
                      │
                AGRIBUSINESS
                      │
               EXTENSION NETWORK
```

Then:

### Farmer-facing layer

> free/basic access

### Institutional layer

> dashboards, APIs, knowledge packs, deployment support

### Public-service layer

> extension integration, escalation, broadcast advisory

### Exact paragraph

The most realistic commercialization path is not to assume that individual smallholder farmers will finance the entire service directly. KrishokTech is better positioned as shared advisory infrastructure: the farmer is the beneficiary, while institutions can finance deployment, support, knowledge integration and operational services.

Potential deployment customers include agricultural programmes, NGOs, agribusinesses, extension networks and public agricultural services. The same core platform can therefore support multiple channels without creating separate products for each organization.

Your production planning already identifies institutional/B2B/B2G deployment as the more durable path. ([github.com](https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System/blob/main/production/future_plan/00_SCOPE_OUTLINE.md))

---

# 38. Page 34 — Market need

## Title

# **The demand already exists; the missing layer is intelligent delivery**

Use existing Bangladesh advisory infrastructure as the starting point.

You have:

* BAMIS;
* 16123;
* extension services.

BAMIS publishes agricultural advisory information, and 16123 is the national agricultural call center. ([GitHub][6])

### Exact text

Bangladesh does not need to invent demand for agricultural advice. Farmers already seek support through extension officers, agricultural call centres, weather and advisory services, local experts and informal information networks.

The opportunity for KrishokTech is to add a digital intelligence layer to that existing ecosystem: understanding farmer-language questions, combining text and image evidence, grounding responses in agricultural knowledge, enforcing safety checks, and routing unresolved cases toward human or institutional support.

This is much stronger than pretending KrishokTech replaces existing extension institutions.

---

# 39. Page 35 — Social inclusion

## Title

# **Access should not depend on English, perfect spelling or reliable broadband**

Use five cards:

### Bengali-first

### Dialect-aware

### Banglish-tolerant

### Low-connectivity pathways

### Voice-ready design

### Exact text

> **Inclusion is implemented as product behavior rather than a statement of intent.**

Then explain:

* large touch targets;
* plain Bengali;
* image-based input;
* progressive clarification;
* offline/cache;
* future voice input.

Your repository's frontend roadmap explicitly considers WCAG-oriented touch targets, Bengali font optimization, PWA/offline UX, on-device diagnosis and voice affordances. ([github.com](https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System/tree/main/production/future_plan))

---

# 40. Page 36 — Environment and responsible agriculture

## Title

# **Better information can also mean more responsible intervention**

Do not claim:

> KrishokTech reduces pesticide usage nationally.

Instead state:

> **The system is designed to make treatment recommendations conditional on evidence and to support IPM/non-chemical alternatives where authoritative guidance exists.**

Then mention:

* dosage verification;
* PHI;
* regulatory state;
* IPM;
* alternative management.

This is where you connect ethics to actual architecture.

---

# 41. Page 37 — SDGs

## Title

# **The innovation contributes directly to four development priorities**

Use four large circles:

### SDG 2

**Zero Hunger**

> agricultural knowledge, extension, resilience.

### SDG 9

**Industry, Innovation and Infrastructure**

> local digital infrastructure.

### SDG 12

**Responsible Consumption and Production**

> evidence-bound intervention and safer chemical guidance.

### SDG 13

**Climate Action**

> weather-aware/proactive advisory pathways.

Don't use 8–10 SDGs.

The UN's SDG 2 targets explicitly include smallholder productivity/income, sustainable agriculture, resilience, extension and technological development. ([Innovation Fair][4])

Bangladesh's own SDG commitment also connects digital agriculture to productivity, food security and empowerment of rural farmers. ([Innovation Fair][4])

---

# 42. Page 38 — Leadership

## Title

# **The innovation was developed as a continuous research-to-engineering cycle**

Use a horizontal timeline:

```text
Field visit
   ↓
Problem identification
   ↓
Dataset / benchmark
   ↓
Retrieval analysis
   ↓
System development
   ↓
Safety research
   ↓
Production hardening
   ↓
Field deployment target
```

Then team responsibility:

### Research

### ML

### Backend

### Frontend

### Infrastructure

### Field coordination

### Validation

Keep this factual.

Do not use inflated titles.

---

# 43. Page 39 — Why the project is different from a typical prototype

## Title

# **What separates KrishokTech from a feature demo**

This page should be a direct comparison:

| Typical prototype           | KrishokTech                               |
| --------------------------- | ----------------------------------------- |
| Model-first                 | Problem-first                             |
| One model                   | Multiple controlled capabilities          |
| Answer-only                 | Answer + evidence + verification          |
| Online assumed              | Degraded connectivity considered          |
| Static data                 | Governed evidence layer                   |
| No audit                    | Audit trail                               |
| No structured failure state | Clarify / refuse / escalate               |
| One provider                | Replaceable model providers               |
| Demo code                   | Modular deployment-oriented architecture  |
| Evaluation = accuracy       | Safety + coverage + latency + reliability |

This should be one of the strongest funding-facing pages.

---

# 44. Page 40 — Deployment roadmap

## Title

# **The next step is not another prototype. It is a field deployment cycle.**

Use:

```text
CURRENT
Validated system
      ↓
PHASE 1
Controlled pilot
      ↓
PHASE 2
Farmer + extension evaluation
      ↓
PHASE 3
Institutional deployment
      ↓
PHASE 4
Regional scale
      ↓
PHASE 5
National service layer
```

### Phase 1

> Deploy to a controlled farmer cohort.

### Phase 2

> Measure expert agreement, useful coverage, safety, referral and user behavior.

### Phase 3

> Integrate with institutional workflows.

### Phase 4

> Expand crop/knowledge/service coverage.

### Phase 5

> Scale through public and private agricultural channels.

---

# 45. Page 41 — What funding unlocks

## Title

# **What support changes**

This is the actual funding page.

Four large blocks:

### FIELD VALIDATION

> farmer pilots, extension evaluation, outcome measurement.

### KNOWLEDGE SCALE

> expert-reviewed agricultural knowledge packs, regulatory updates.

### DEPLOYMENT

> hosting, edge/offline, monitoring, service reliability.

### ECOSYSTEM

> institutional integration, extension workflow, partnership development.

### Exact text

The core system does not need to be invented from scratch. The next investment is in reducing the gap between controlled validation and field operation.

Funding would support expert-reviewed knowledge expansion, farmer and extension pilots, production infrastructure, multimodal and offline deployment, operational monitoring, and institutional integration. The objective is to measure real-world value under real conditions and build the evidence required for responsible scale.

---

# 46. Page 42 — What success will mean

## Title

# **We will measure deployment by outcomes, not downloads**

This is important.

Use five metrics:

### Safe advisory rate

### Correct advisory rate

### Appropriate abstention

### Farmer task completion

### Extension referral resolution

Then later:

### crop-loss / yield outcomes

### chemical-use outcomes

### user trust

### retention

### cost per successfully resolved case

This makes the project look mature.

---

# 47. Page 43 — Current evidence / future evidence

## Title

# **What we know now, and what deployment must still prove**

Two columns.

### ESTABLISHED TODAY

* benchmark resources;
* retrieval findings;
* system architecture;
* safety tests;
* expert review;
* software verification;
* network simulation;
* local model path;
* production structure.

### NEXT VALIDATION

* field outcomes;
* carrier-level delivery;
* farmer adoption;
* extension workload;
* real referral follow-through;
* long-term trust;
* yield/chemical-use impact.

This is a powerful credibility page because it says:

> **we know exactly where the evidence currently ends.**

Your CEA manuscript itself makes these distinctions clearly. 

---

# 48. Page 44 — Research portfolio

## Title

# **The innovation is backed by a continuous research programme**

Four cards.

### Research 01

**KrishokTech: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory**

**Contribution:** knowledge/evaluation foundation.

### Research 02

**Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory**

**Contribution:** retrieval failure analysis.

### Research 03

**Bounded-Authority Agricultural Advisory / CEA manuscript**

**Contribution:** system reliability, routing, verification, deployment architecture.

### Research 04

**KrishokTech System Demonstration / EACL submission**

**Contribution:** integrated public system.

Be very careful with status labels:

> Published/preprint / Submitted / In preparation

depending on the actual state.

The v2 paper is definitely arXiv v2 and current. ([arXiv][2]) The retrieval paper is on arXiv as 2608.14886. ([arXiv][5])

---

# 49. Page 45 — Links and access

## Title

# **Explore the work**

Four large QR codes, maximum.

### LIVE SYSTEM

> Try KrishokTech

### SOURCE CODE

> GitHub repository

### RESEARCH

> KrishokTech v2

### RETRIEVAL STUDY

> Where Does Retrieval Fail?

Then small:

> **Primary repository:** github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System

The repository is public and currently exposes backend, frontend, deployment, research artifacts, production plans and experiment-related materials. ([GitHub][6])

---

# 50. Page 46 — Closing

## Title

# **From field problem to trusted agricultural service**

Very little text.

Use the full system image.

Exact copy:

KrishokTech began with a practical question from the field:

**How can agricultural technology become genuinely useful to a farmer when language, evidence, uncertainty and connectivity all matter at the same time?**

We answered that question by building the research foundation, measuring where current AI fails, redesigning the advisory architecture around those failures, and engineering the result into a working platform.

The next step is to take that system into the field, measure its real value, and build the institutional pathway for responsible scale.

Bottom:

# **Research → Evidence → System → Field**

Then QR code.

---

# 51. Optional appendix after Page 46

This is where we can include the rest.

I recommend **not numbering these as part of the main narrative**.

Use:

## Appendix A — Full system architecture

## Appendix B — Experiment catalogue

## Appendix C — Safety attack matrix

## Appendix D — Full expert-evaluation table

## Appendix E — Full deployment benchmark

## Appendix F — Research-paper details

## Appendix G — Repository / production architecture

## Appendix H — Detailed references

This lets a very technical judge dig deeper without harming the core story.

---

# 52. The appendix's experiment catalogue should include all 36 completed CEA layers

But **group them by question**, not by chronological experiment number.

Use this structure:

## A. Knowledge & evidence

* E19 graph traversal
* E23 provenance/cache
* E24 knowledge growth
* E30 temporal validity
* E36 source fragmentation

## B. Routing & retrieval

* E17 detection gating
* E25 compact router
* E32 oracle routing
* E33 wrong high-confidence routing
* E35 normalization
* E12 retrieval degradation

## C. Safety & verification

* E02 misbinding
* E03 slot ablation
* E04 calibration
* E05 counterfactual
* E07/E08 security
* E10 failure taxonomy
* E11 generator robustness
* E12 poisoning
* E22 SMS injection

## D. Language & multimodality

* E06 dialect
* E21 dialect hazard
* E31 multimodal uncertainty
* E37 clarification

## E. Delivery & deployment

* E09 runtime
* E14 network
* E15 GSM
* E18 LLM dependency
* E20 cost
* E38 escalation
* E39 IPM

This is how the “lots of experiments” become a **coherent validation programme**.

---

# 53. Very important: don't show the experiment IDs in the main story

Do not write:

> E02, E03, E05, E21...

everywhere.

A funding judge should never have to decode experiment IDs.

In the appendix:

> **Safety Test S3 — Counterfactual Evidence Binding**

and then small:

> Internal experiment: E05

That's enough.

---

# 54. LaTeX implementation specification

Now the actual build instructions for your agents.

## Document type

Use:

```latex
\documentclass[11pt,a4paper]{article}
```

I would use A4, not letter.

---

# 55. Packages

Use approximately:

```latex
\usepackage[margin=18mm]{geometry}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{multirow}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{tcolorbox}
\usepackage{fontspec}
\usepackage{polyglossia}
\usepackage{hyperref}
\usepackage{bookmark}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{longtable}
\usepackage{adjustbox}
\usepackage{qrcode}
\usepackage{fontawesome5}
```

For Bengali:

```latex
\setmainfont{Aptos}
\newfontfamily\bengalifont[Script=Bengali]{Noto Sans Bengali}
```

Use a proper installed Bengali font, but **do not distribute font files with the submission**.

---

# 56. Visual theme

Use:

### Primary

Deep agricultural green.

### Secondary

Warm earth.

### Accent

Technology blue.

### Background

Off-white.

### Text

Very dark charcoal.

No gradients.

No glowing AI motifs.

No stock “robot farmer” visual clichés.

---

# 57. Page layout rule

Every page needs this structure:

```text
TITLE
1-line takeaway
--------------------
main visual
--------------------
supporting explanation
--------------------
source / evidence footer
```

A page should never have:

> title → giant paragraph → giant paragraph → tiny citation.

---

# 58. Typography hierarchy

### H1

24–28 pt

### H2

16–18 pt

### body

10.5–11.5 pt

### captions

8.5–9 pt

### large numbers

32–46 pt

### quote

16–20 pt

This should feel like a premium technical report, not a thesis.

---

# 59. Diagram rule

For every diagram, the agent should ask:

> “Can I remove one node without losing meaning?”

If yes, remove it.

The PDF should not reproduce your internal software architecture in microscopic detail.

---

# 60. Graphical style

All system diagrams should use the same vocabulary:

### Blue

Input/context.

### Green

Verified agricultural evidence.

### Purple

AI/generation.

### Red

Safety stop.

### Amber

Uncertainty/clarification.

### Grey

Infrastructure.

This is enough for a coherent visual language.

---

# 61. Chart rule

All charts must use **real data only**.

No AI-generated numerical charts.

Use:

* matplotlib/PGFPlots;
* exact source YAML;
* exact raw results.

Every chart gets:

> **Source: KrishokTech evaluation artifact, [experiment name].**

For simulated experiments:

> **Source: software/network simulation; not carrier-level measurement.**

---

# 62. Screenshot rule

Screenshots are always real.

Needed screenshots:

1. landing page;
2. Bengali conversation;
3. trace;
4. evidence;
5. image diagnosis;
6. safety block;
7. expert/research view;
8. offline/local state;
9. analytics/health;
10. SMS export.

Don't fabricate screenshots.

---

# 63. Image-generation rule

Use GPT image generation for **conceptual illustrations only**.

Good uses:

* field-origin image;
* ecosystem diagram backgrounds;
* abstract agriculture + technology visual.

Bad uses:

* benchmark charts;
* UI;
* numerical tables;
* architecture with small technical labels;
* citation pages.

For generated visuals, use one consistent prompt prefix:

```text
Premium editorial illustration for a Bangladesh national innovation dossier, A4-oriented composition with a clear widescreen-safe center area, authentic Bangladeshi agricultural environment, restrained deep agricultural green and warm earth palette, realistic human proportions, documentary rather than futuristic, clean negative space, no logos, no watermark, no fake statistics, no decorative text.
```

---

# 64. Source/citation rule

This is extremely important.

The PDF should distinguish:

### [Research]

Your papers.

### [System]

Your GitHub.

### [Experiment]

Your uploaded results files.

### [Government]

DAE/BAMIS/BARC/etc.

### [External literature]

Current research.

Do not put citations in every sentence.

But every **factual external claim** must have a source.

---

# 65. The PDF should have three evidence labels

I strongly recommend little badges:

### **MEASURED**

real experimental measurement.

### **SIMULATED**

software/network simulation.

### **PROJECTED**

scenario/model assumption.

This will enormously increase credibility.

For example:

> **Offline delivery retention — SIMULATED**

> **Expert evaluation — MEASURED**

> **National deployment cost — PROJECTED**

That prevents accidental overclaiming.

---

# 66. This also resolves a problem in the current CEA material

The CEA manuscript itself distinguishes measured production facts from research-layer, simulation and projection evidence. 

The supporting PDF should use this same evidence discipline.

---

# 67. What to do with the conflicting experiment numbers

Before the PDF is generated:

## Agent task

Create:

```text
innovation_fair_supporting_doc/data/canonical_fair_numbers.yaml
```

Only approved numbers can appear in the PDF.

Each number must have:

```yaml
metric:
value:
unit:
source:
experiment:
status:
notes:
```

Example:

```yaml
evidence_nodes:
  value: 2946
  source: KrishokTech_v2
  status: measured
```

This avoids the current E14/E18/E19 stale-note problem.

The current CEA artifact still contains contradictory historical values in some experiment acceptance notes, so we should never manually copy those numbers into the PDF. 

---

# 68. The PDF should not repeat the CEA manuscript's uncertainty caveats everywhere

Instead, have one dedicated page:

# **Evidence status and boundaries**

Then use tiny badges.

This is cleaner.

---

# 69. The exact “evidence status” page

Use:

| Evidence                    | Status      | Meaning              |
| --------------------------- | ----------- | -------------------- |
| v2 benchmark                | Established | arXiv resource       |
| Retrieval study             | Established | arXiv study          |
| Expert review               | Measured    | 200 outputs          |
| Safety attack suite         | Measured    | specified benchmark  |
| Counterfactual verification | Measured    | 2,000 pairs          |
| Network resilience          | Simulated   | emulator             |
| GSM composition             | Tested      | software composition |
| Carrier delivery            | Future      | not measured         |
| Farmer outcome              | Future      | field study needed   |
| National impact             | Future      | not yet demonstrated |

This one page saves us from overclaiming elsewhere.

---

# 70. One writing principle for the whole PDF

Avoid academic hedging such as:

> “It may be hypothesized that…”

But also avoid startup hype such as:

> “revolutionary, game-changing, disruptive…”

Use:

> **“We built…”**

> **“We measured…”**

> **“We found…”**

> **“This changed the design…”**

> **“The next deployment stage will measure…”**

That will sound natural.

---

# 71. Another crucial writing rule

Whenever a result is impressive, immediately explain **why it matters**.

Bad:

> “0/2,000.”

Good:

> **“0/2,000 counterfactual certifications: the verifier rejected corrupted treatment combinations rather than following the model's prior.”**

Every number must answer:

> **So what?**

---

# 72. Another writing rule

Never make one number carry three different meanings.

For example:

> 61.52% zero-LLM

should never simultaneously be described as:

> “61.52% answered deterministically.”

It isn't.

The current workload explicitly contains T0 safety and T4 refusal in that number. 

Use:

> **51.04% deterministic advisory paths**

and:

> **61.52% zero-LLM terminal handling**

Correct.

---

# 73. How to connect the first paper to the system

Use this transition exactly:

> **The benchmark showed that agricultural language modeling needs grounded evidence. The product therefore began with evidence, not generation.**

Excellent.

---

# 74. How to connect the second paper

Use:

> **The retrieval study then showed that evidence is not equally reachable from every farmer query. The system therefore needed more than one route to the same agricultural knowledge.**

That leads naturally to routing.

---

# 75. How to connect the safety research

Use:

> **Once retrieval became part of the decision path, the next problem was evidence integrity: retrieving a relevant passage does not guarantee that its fields can be safely combined.**

Then:

> **That led to typed relational verification.**

Beautiful causal chain.

---

# 76. How to connect multimodality

Use:

> **The same logic applies to images. A visual prediction is useful context, but it should not automatically become permission to recommend an intervention.**

Then cross-modal conflict.

---

# 77. How to connect deployment

Use:

> **Finally, correctness is only useful if the advisory can reach the farmer. Connectivity and delivery therefore became part of the system boundary.**

Then offline/cache/SMS.

---

# 78. This gives the PDF one continuous story

```text
We observed the problem.
        ↓
We built the knowledge resource.
        ↓
We measured model limitations.
        ↓
We measured retrieval limitations.
        ↓
We built multiple evidence paths.
        ↓
We created a safety boundary.
        ↓
We integrated vision.
        ↓
We built last-mile resilience.
        ↓
We made the platform operational.
        ↓
We are ready for field validation.
```

That is the PDF.

---

# 79. The final document should not say “we solve all agriculture”

It should say:

> **“We are building a reusable platform whose first validated domain is Bengali agricultural advisory in Bangladesh.”**

That makes scaling plausible.

---

# 80. The “national platform” phrase must be used carefully

Good:

> **potential national advisory infrastructure**

Better:

> **architecture intended to support institutional and national-scale deployment**

Do not say:

> already a national platform.

Not yet.

---

# 81. The project-photo requirement

The Fair's form has an optional project photo. ([Innovation Fair][1])

Use:

### Best photo

Founder/team in the field with farmer + crop context.

### Second-best

Farmer using the system.

### Third-best

System on phone beside crop.

Do not use:

* headshot;
* lab-only computer photo;
* logo.

---

# 82. The supporting PDF should have no “Thank you” page

The final page is not:

> Thank you.

It is:

# **The next experiment is in the field.**

That is much stronger.

---

# 83. One final page that I now think is worth adding

## Title

# **From answer generation to agricultural decision support**

Use a spectrum:

```text
CHATBOT
   ↓
RAG ASSISTANT
   ↓
GROUNDED ADVISOR
   ↓
VERIFIED ADVISOR
   ↓
DECISION-SUPPORT PLATFORM
```

Place:

# **KRISHOKCHAT**

at the last stage.

Then:

> **The long-term product is not the generated answer. It is the decision-support infrastructure behind the answer.**

This is the cleanest conceptual statement for the entire project.

---

# 84. Final page-count recommendation

I would now lock the structure at:

### Main narrative

**46 pages**

### Appendix

**8–15 optional pages**

That gives:

> **~46 pages of curated due-diligence content, expandable to ~55–60 pages with appendices.**

That sounds large, but this is not a 46-page essay. A large fraction are:

* full-width diagrams;
* screenshots;
* tables;
* benchmark cards;
* evidence matrices.

That is appropriate for a supporting technical dossier.

---

# 85. What the 46 pages are actually doing

### Pages 1–4

**Why the problem exists**

### Pages 5–9

**Why you had to build this**

### Pages 10–14

**What exactly you built**

### Pages 15–21

**Why its safety architecture matters**

### Pages 22–30

**What the evidence says**

### Pages 31–36

**Why it can become a service**

### Pages 37–42

**Why it matters nationally**

### Pages 43–46

**What happens next**

That is a coherent document.

---

# 86. The PDF should be much denser than the 8-slide deck—but not academically dense

The difference is:

### PPT

> **“Here is the idea.”**

### PDF

> **“Here is the idea, the evidence, the architecture, the research lineage, the current status, and the path to deployment.”**

That's exactly what the supporting field is for.

---

# 87. What gets removed completely

Do not put these into the main PDF narrative:

* every individual code test;
* every model package version;
* all 36 experiment IDs;
* the old 145,500 v1 headline;
* project-management status notes;
* internal acceptance/ledger language;
* “done/pending/blocked” experiment workflow terminology;
* speculative national cost savings;
* unsupported partnership claims;
* claims of farmer outcome.

They can appear in appendices only where useful.

---

# 88. What gets promoted

These deserve unusually strong visual treatment:

### v2's 85,979 benchmark / 1,000 farmer benchmark

### retrieval-failure finding

### 2,946 semantic knowledge units

### 0/2,000 counterfactual certifications

### 0/1,400 injection certifications

### slot-ablation hazard hierarchy

### 200 expert evaluations

### 4.82/5 expert correctness

### 96.5% deployment approval

### 51.04% deterministic advisory workload

### network/cache resilience

### production architecture

These are the **proof points**.

---

# 89. One correction to the wording from my previous response

I previously described the first dataset as:

> “145,500 supervised QA examples.”

That was indeed based on the **v1** abstract, not your current v2. That was wrong for the current research story.

The correct v2 framing is:

> **85,979 core benchmark instances + 1,000 real-world farmer queries, with 2,946 semantic units and 284 official publications from 13 institutions across six Bengali dialects.** ([arXiv][2])

And the v2 results are substantially more interesting than the old v1 story anyway: the paper shows closed-book insufficiency, a persistent chemical hallucination floor even with oracle context, improved General QA from fine-tuning, and the failure of answer-only fine-tuning to preserve safety behavior. ([arXiv][2])

So the correction actually makes our innovation narrative **stronger**, because the product now emerges naturally from the demonstrated research gaps.

---

# 90. The exact master storyline agents should follow

Give every writing/layout agent this instruction:

> **Never introduce a technology before the problem it solves has appeared. Never show a result without explaining what design decision it validates. Never introduce a future capability as though it were already deployed. Never use a research-paper statistic as a product statistic unless the endpoint genuinely matches. Every section must create the question that the next section answers.**

Then the writing sequence becomes:

### Field

“Why did we start?”

### Research

“What did we discover?”

### Architecture

“What did we change?”

### Product

“How does the farmer experience it?”

### Evidence

“Why should anyone trust it?”

### Operations

“Can it survive real constraints?”

### Market

“Who can deploy it?”

### Roadmap

“What does support unlock?”

This is the story.

---

# 91. The final emotional arc

The PDF should begin:

> **We went to the field.**

Then:

> **We discovered the problem was harder than it looked.**

Then:

> **We measured why.**

Then:

> **We built around those failures.**

Then:

> **We tested the system where it matters.**

Then:

> **We are now ready for the next level of validation.**

That is not “chapabazi.”

That is a credible innovation story.

---

# 92. And the key final sentence

I would end the whole supporting PDF with:

> **KrishokTech is no longer only a question of whether an AI model can answer an agricultural question. The project is now about whether Bangladesh can build a locally grounded, evidence-aware, safe and deployable intelligence layer for agricultural decision support.**

That is the level at which I would pitch the innovation.

---

# 93. The actual final deliverables for your agents

They should produce exactly:

```text
innovation_fair_supporting_doc/
│
├── main.tex
├── references.bib
├── data/
│   └── canonical_fair_numbers.yaml
├── figures/
│   ├── field_origin.*
│   ├── research_timeline.*
│   ├── system_architecture.*
│   ├── safety_flow.*
│   ├── treatment_record.*
│   ├── counterfactual_binding.*
│   ├── slot_ablation.*
│   ├── retrieval_degradation.*
│   ├── dialect.*
│   ├── multimodal.*
│   ├── network.*
│   ├── efficiency.*
│   └── roadmap.*
├── screenshots/
│   ├── farmer_home.*
│   ├── bengali_chat.*
│   ├── evidence.*
│   ├── vision.*
│   ├── safety.*
│   ├── offline.*
│   └── admin.*
├── sources/
│   ├── krishoktech_v2.pdf
│   ├── retrieval_paper.pdf
│   ├── cea_paper.pdf
│   └── results.yaml
└── build/
    └── KrishokTech_Innovation_Fair_Supporting_Dossier.pdf
```

And the build pipeline must be:

```text
raw experiment files
       ↓
canonical numbers
       ↓
charts/tables
       ↓
LaTeX
       ↓
PDF
       ↓
visual audit
       ↓
claim audit
       ↓
final PDF
```

No manual number editing after the canonical data file is frozen.

---

# 94. Final recommendation on this supporting PDF

**Yes: use the optional supporting-file slot for this PDF.**

And **yes: build it in LaTeX.**

Do not upload the 26-page v2 paper, the CEA manuscript, and the retrieval paper separately as if the judges are expected to read them.

Instead:

> **this PDF tells the story and extracts the proof from those works.**

The actual papers remain linked as primary research artifacts.

The distinction is:

### Paper

**What did we publish scientifically?**

### Supporting dossier

**Why does the entire body of work constitute a credible innovation worth supporting?**

That is the object you were asking for.

The official Fair's mission makes this especially appropriate because it is explicitly trying to connect research with practical application, enterprise, market and national innovation infrastructure. ([Innovation Fair][4])

---

# 95. The single sentence that should govern every page

# **Every page must either explain why KrishokTech exists, show what was built, prove that an important property was tested, or explain how the tested system becomes deployable.**

If a page does none of those four things:

**delete it.**

That is the discipline I would use for the final PDF.

[1]: https://innovationfairbd.org/innovator-application-form "Innovation Fair"
[2]: https://arxiv.org/html/2606.29243v2 "KrishokTech: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory"
[3]: https://huggingface.co/datasets/RaiyanKhaan/KrishokTech?utm_source=chatgpt.com "RaiyanKhaan/KrishokTech · Datasets at Hugging Face"
[4]: https://innovationfairbd.org/about "Innovation Fair"
[5]: https://arxiv.org/abs/2608.14886?utm_source=chatgpt.com "Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory"
[6]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System "GitHub - RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
