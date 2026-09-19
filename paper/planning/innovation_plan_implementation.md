I’ve now gone through the **current repository, production structure, the 36 completed CEA experiment layers, the separate EACL system-test matrix, and the new results files you uploaded**, and I also checked the actual Innovation Fair application fields plus recent EACL demonstration papers.

There is enough material here to make the application substantially stronger than a normal “student AI project” pitch. The important thing is **selection discipline**: the application must sell one innovation, while the supporting document proves the depth underneath it.

The Fair itself explicitly frames its purpose as moving local innovation from **research and experimentation → practical application → enterprise → market**, and the application requires exactly the elements you listed: a ≤250-word description, technical details, 7–8 slides addressing the nine judging dimensions, and an optional current-status supporting document. ([innovationfairbd.org](https://innovationfairbd.org/about)) ([innovationfairbd.org](https://innovationfairbd.org/innovator-application-form))

For EACL, the same philosophy also fits: the 2027 Demo CFP explicitly welcomes application systems, open systems, research tools, multimodal systems and mature production-oriented systems; it evaluates motivation/fit/novelty, system description, evaluation, availability/licensing and presentation quality. ([2027.eacl.org](https://2027.eacl.org/calls/demos/)) Recent accepted demos such as *AI for Climate Finance*, *RAGVUE*, *SmartMatch*, *PromptLab*, and the browser-based multimodal verification assistant all succeed by making the **system workflow** clear and then backing it with targeted evidence rather than turning the paper into a catalogue of technologies. ([ACL Anthology][1])

So here is the **final execution specification**.

---

# PART I — The non-negotiable positioning

## Project name

# **KrishokTech**

### **Bengali Agricultural Intelligence for Farmers, Extension and Rural Communities**

Do not call it:

* “an AI chatbot”
* “a RAG application”
* “a disease detection app”
* “an LLM agricultural assistant”

Those are components.

The product is:

> **A Bengali-first agricultural intelligence and advisory platform.**

The innovation is:

> **bringing farmer language, crop imagery, agricultural knowledge, safety verification and constrained-connectivity delivery into one operational advisory workflow.**

And the strongest differentiator is:

> **The system is designed around the places where agricultural AI fails—not only around where AI performs well.**

That should guide almost every sentence.

Your repository genuinely supports this broader system description: it currently has Bengali hybrid RAG, a six-way safety classifier, terminal safety outcomes, audit logging, streaming trace events, crop-to-crop-specific disease routing, weather/helpline functions, replaceable LLM backends, a layered backend, and separate deployment infrastructure. ([GitHub][2])

---

# PART II — THE 250-WORD DESCRIPTION

This must sound like a founder/researcher describing something they actually built, not like a grant abstract.

### Final version

KrishokTech is a Bengali-first agricultural intelligence platform developed from field observations and direct engagement with farmers in Bangladesh. Farmers often face a combination of problems at once: difficulty communicating in standard language, limited access to agricultural experts, uncertainty about crop diseases and treatments, and unreliable connectivity. KrishokTech is designed around these real constraints rather than assuming that a generic AI assistant is sufficient.

The platform combines Bengali conversational advisory, crop-image analysis, agricultural knowledge retrieval, safety screening, evidence verification, audit trails and low-connectivity delivery in one system. A farmer can describe a problem in Bengali or Banglish, upload a crop image, receive crop- and disease-specific guidance, inspect the supporting evidence, and obtain a response through the available connectivity path. For safety-critical recommendations, the system verifies agricultural facts before delivery and can ask for clarification, refuse unsupported advice or route a case for human assistance.

The system is supported by our earlier research on Bengali agricultural knowledge and retrieval, followed by a large-scale reliability evaluation of the integrated architecture. Our current evaluation includes independent agronomist review, adversarial safety testing, evidence-binding tests, multilingual and dialect conditions, multimodal conflict cases, network-degradation tests and deployment benchmarks. In one 100-case live-model expert benchmark, KrishokTech achieved 97% certified correctness with no observed critical unsafe acceptance; separate 11,000-case metamorphic testing also found no observed invalid certification.

KrishokTech is now moving from research validation toward field deployment, with a longer-term goal of supporting farmers, extension services, NGOs, agribusinesses and public agricultural services through a locally grounded and scalable technology platform.

### Important

This is about **230–240 words**, not padded to 250.

Do not add claims such as:

> “first in Bangladesh,”
> “hallucination-free,”
> “100% safe,”
> “already nationally deployed”

unless you have independent evidence for those statements.

The current experimental database supports the underlying numbers and validation statements above. The expert benchmark reports 97% certified correctness and 0% observed CUAR over 100 live-model cases, while the metamorphic study reports 11,000/11,000 rejected mutations.   

---

# PART III — TECHNICAL DETAILS FIELD

The form specifically asks for:

> key components, design, programming languages, materials and equipment/tools.

So this field should be technical but readable.

### Final version

KrishokTech is implemented as a modular web-based agricultural advisory platform with a Next.js/React/TypeScript frontend and a FastAPI/Python backend. The system is organized into application, domain, port/protocol and infrastructure layers so that models and external service providers can be replaced without changing the core advisory logic.

The NLP layer uses Bengali Unicode normalization, BM25 sparse retrieval and FAISS dense retrieval with precomputed agricultural knowledge indexes. A safety and routing layer screens requests before retrieval and supports terminal handling of unsafe, off-topic, prompt-injection and low-confidence cases. Generative responses can be produced through configurable remote or local LLM backends, including Ollama-based local inference. A verification layer checks grounded responses and safety-critical agricultural fields against structured evidence.

The multimodal pipeline accepts crop images, identifies the crop family, routes the image to a crop-specific disease classifier, and connects the resulting diagnosis to Bengali agricultural knowledge and treatment guidance. The system also supports contextual services such as weather information, audit logging, streaming responses and constrained SMS delivery.

For deployment, KrishokTech uses precomputed local assets, configurable model providers, health/readiness checks, containerized services and offline-oriented knowledge caching. The development process includes automated backend/frontend tests, reproducible experiment scripts, model verification, audit traces and versioned research artifacts.

The current platform has been engineered so that additional crops, agricultural knowledge packs, advisory capabilities and deployment channels can be introduced without rebuilding the farmer-facing application.

The technology details are grounded in the actual repository architecture: Next.js 16/React 19/TypeScript, FastAPI, BM25 + FAISS, mE5 embeddings, Ollama/OpenRouter/Gemini adapters, Ultralytics/ONNX vision, audit infrastructure, streaming, and the layered application/domain/ports/infrastructure structure. ([GitHub][2])

---

# PART IV — THE 8-SLIDE INNOVATION FAIR DECK

## Important rule

**Do not build eight academic slides.**

Build eight **decision slides**.

The judge should understand the entire proposition after 3 minutes.

The sequence is:

> **FIELD → PROBLEM → DISCOVERY → INNOVATION → PROOF → IMPACT/MARKET → RESPONSIBILITY → FUNDING/DEPLOYMENT**

---

# SLIDE 1 — FIELD ORIGIN

## Title

# **We started with farmers, not with a model.**

## Main text

> In Bangladesh, agricultural decisions are often made with incomplete information, unfamiliar terminology, limited access to experts and unreliable connectivity.

Then three very short labels:

### **FIELD**

Farmer interactions and local problem discovery

### **LANGUAGE**

Questions are asked in the language farmers actually use

### **ACCESS**

Advice must remain useful beyond reliable broadband

Bottom:

> **The question was not “How do we add AI to agriculture?”
> It was “How can technology become genuinely useful to a farmer?”**

## Visual

Use your **actual field photographs** here.

Do not generate these.

Use:

* farmer interaction;
* soil/irrigation photograph;
* crop photograph;
* perhaps a notebook/field observation image.

### Layout

Left 55%:

large field photo.

Right 45%:

three stacked problem cards.

Bottom:

one sentence.

---

## Optional visual prompt

Don't generate the field photograph. Generate only a subtle background/transition visual if needed.

### GPT image prompt

```text
Create a premium editorial illustration for a Bangladesh national innovation presentation, 16:9 widescreen. Depict a realistic Bangladeshi smallholder farmer standing beside a crop field while using a smartphone to seek agricultural advice. Include subtle visual cues of a rural agricultural setting, crop leaves, weak mobile connectivity, and an agricultural extension context. The mood should feel authentic, practical, hopeful and documentary-like, not futuristic or science-fiction. Use a restrained professional palette based on deep agricultural green, warm earth tones and off-white. Leave substantial negative space on the right side for presentation text. No logos, no fake UI, no decorative typography, no English text inside the generated image.
```

---

# SLIDE 2 — THE GAP

## Title

# **The problem is not a lack of AI. It is a lack of accountable agricultural AI.**

## Main visual

Four boxes:

```text
Generic AI
↓
Fluent answer
↓
May misunderstand farmer language
May rely on outdated knowledge
May invent unsupported treatment
```

Then:

```text
Typical RAG
↓
Better grounding
↓
Still sensitive to retrieval failure,
language variation and evidence conflicts
```

Then:

```text
Vision-only tools
↓
Good at diagnosis
↓
Do not solve the full advisory problem
```

Right/bottom:

# **KrishokTech**

> Language + Vision + Evidence + Safety + Delivery

## Small footer

> Our earlier research tested these failure modes before the integrated system was designed.

This connects naturally to the two papers.

## Visual prompt

```text
Create a clean high-end editorial infographic, 16:9 widescreen, showing the evolution of agricultural digital advice. Three fragmented approaches on the left: generic AI chatbot, text-only retrieval, and image-only diagnosis. Each should be represented visually with simple professional icons and a short conceptual label, while showing their limitations through subtle broken links. On the right, show one integrated agricultural advisory platform combining LANGUAGE, VISION, EVIDENCE, SAFETY, and DELIVERY into a single coherent workflow. Bangladesh-focused visual identity, professional government innovation presentation style, deep agricultural green, muted earth tones, white background, generous whitespace. Avoid dense text. No fake statistics.
```

---

# SLIDE 3 — WHY KRISHOKCHAT EXISTS

## Title

# **We learned from failure before we built the product.**

This is your research credibility slide.

Use a horizontal story:

```text
FIELD PROBLEM
      ↓
BENGALI AGRICULTURAL DATA
      ↓
RETRIEVAL RESEARCH
      ↓
FAILURE DISCOVERY
      ↓
SYSTEM DESIGN
      ↓
VALIDATION
```

### Three evidence cards

#### 01 — Knowledge

> We built a citation-grounded Bengali agricultural knowledge and evaluation foundation.

#### 02 — Retrieval

> We measured how farmer language, dialect and Banglish change retrieval behavior.

#### 03 — Reliability

> We redesigned the system around those observed failure modes.

Then the killer sentence:

# **Research findings became engineering decisions.**

This is one of the most important slides in the whole deck.

---

# SLIDE 4 — THE INNOVATION

## Title

# **One advisory system, built around the farmer's real workflow.**

This must be the most visually impressive slide.

Use a central pipeline:

```text
              FARMER
      Text • Image • Voice*
               │
               ▼
        UNDERSTAND + SCREEN
               │
               ▼
         SAFETY / CONTEXT
               │
        ┌──────┼───────┐
        ▼      ▼       ▼
      VISION  FACTS    RAG
        │      │       │
        └──────┼───────┘
               ▼
       AGRICULTURAL ADVISOR
               │
          ┌────┴─────┐
          ▼          ▼
       VERIFY     CLARIFY /
                   ESCALATE
          │
          ▼
  WEB • LOCAL • OFFLINE • SMS
```

* Remove Voice if it is not actually live by the submission date.

Center badge:

# **No evidence → no unsafe advice.**

Bottom text:

> KrishokTech is not a single model. It is a coordinated agricultural intelligence system.

---

# SLIDE 5 — PROOF

## Title

# **This is already more than a prototype.**

This slide must be visually simple.

Use four large numbers.

### **2,946**

institutional source documents

### **2,135**

knowledge nodes

### **97%**

certified correctness on a 100-case live-model expert benchmark

### **0 observed**

critical unsafe acceptance in that benchmark

Then a thin bottom row:

> **11,000** metamorphic authority tests
> **1,400** adversarial injection cases
> **200** expert-reviewed outputs
> **558** backend tests passing
> **50/50** golden replay

The exact numbers are supported by the current database: 2,135/2,946 source infrastructure, 97% on the independent live benchmark, the 11,000 metamorphic test suite, and the current software verification baseline.    

### Very important

Do **not** put:

> “100% safe”

on this slide.

Put:

> **0 observed critical unsafe acceptance in the evaluated benchmark.**

That sounds much more credible.

---

# SLIDE 6 — IMPACT + MARKET

## Title

# **Built for farmers. Scalable through institutions.**

Three columns.

### FARMERS

> Bengali-first advice
> Crop-image support
> Clarification when information is missing
> Low-connectivity pathways

### INSTITUTIONS

> Extension support
> Knowledge distribution
> Case escalation
> Agricultural program deployment

### INDUSTRY

> API/service integration
> Agribusiness advisory
> Institutional knowledge packs
> Analytics and operational support

Then bottom:

```text
Farmer
  ↓
KrishokTech
  ↓
Extension / NGO / Agribusiness
  ↓
Public Agricultural Services
```

## Bottom sentence

> **The farmer is the beneficiary; institutions provide the path to sustainable scale.**

That commercialization model is much more believable than pretending every farmer will pay a subscription.

Your own production-scope analysis supports this institutional/B2B/B2G path. ([GitHub][3])

---

# SLIDE 7 — SAFETY, INCLUSION, SDG

## Title

# **Useful AI must also be responsible AI.**

Four quadrants.

### SAFETY

> Unsafe requests can be stopped before generation.

### INCLUSION

> Bengali, dialect-aware routing, Banglish, low-connectivity access and future voice interaction reduce barriers to participation.

### ENVIRONMENT

> Evidence-based treatment and IPM-oriented recommendations can reduce unnecessary chemical use.

Your current IPM experiment reports 77.14% non-chemical alternative recommendations under the BAA/IPM-balanced resolver versus 2.86% for a chemical-first baseline.

Don't put the exact statistic on the main slide unless we have the final source line; the concept is enough.

### SDGs

**SDG 2 — Zero Hunger**

**SDG 9 — Industry, Innovation & Infrastructure**

**SDG 12 — Responsible Consumption & Production**

**SDG 13 — Climate Action**

The UN's SDG 2 targets explicitly include smallholder productivity/income, sustainable agriculture, resilience, agricultural extension, research and technology. ([sdgs.un.org](https://sdgs.un.org/goals/goal2?utm_source=chatgpt.com))

Bangladesh's national SDG commitments also explicitly connect digital agricultural transformation with productivity, food security and empowering rural farmers. ([bangladesh.un.org](https://bangladesh.un.org/sites/default/files/2023-09/Bangladesh_SDG%20Summit%202023_National%20Statement%20of%20Commitment_v2.pdf?utm_source=chatgpt.com))

---

# SLIDE 8 — THE ASK

## Title

# **The technology exists. The next step is field deployment.**

Left:

## TODAY

> Working integrated platform
> Research foundation
> Safety and reliability evaluation
> Multimodal advisory
> Production-oriented architecture
> Public demonstration

Right:

## NEXT

> Farmer pilot
> Expert/extension workflow
> Broader agricultural knowledge coverage
> Voice + edge/offline expansion
> Institutional integration
> Measured field impact

Bottom:

# **Support the transition from validated research system to field-deployed agricultural service.**

And the final three links:

**LIVE DEMO** | **GITHUB** | **RESEARCH**

QR code to live demo.

This is the only slide where you should explicitly make the funding transition.

---

# PART V — EXACT SLIDE FOOTERS

Every slide should use a tiny footer:

> **KrishokTech | Bengali-first agricultural intelligence for Bangladesh**

And Slide 5 onward can use:

> **Research evidence and system status available in supporting dossier.**

Don't clutter with citations.

---

# PART VI — WHAT THE SUPPORTING DOCUMENT SHOULD BE

Do not upload the three papers separately.

Create one:

# **KrishokTech — Current Status, Research Evidence & Deployment Roadmap**

**Recommended format:** PDF.

The application page identifies the supporting upload separately but does not specify its format in the public form; the main presentation explicitly requires PPT/PPTX. A PDF dossier is therefore the safer supporting artifact unless the actual portal upload control states otherwise. ([innovationfairbd.org](https://innovationfairbd.org/innovator-application-form))

Target:

# **20 slides/pages**

Not 40.

Not 50.

Not the 26-page research manuscript.

This is a **due-diligence dossier**, not an academic paper archive.

---

# PART VII — SUPPORTING PDF: EXACT STRUCTURE

## COVER

# **KrishokTech**

### From Field Problem to Deployable Agricultural Intelligence

Subline:

> Research foundation · Integrated system · Reliability validation · Deployment pathway

Visual:

Actual farmer field photograph blended with actual product screenshot.

---

# PAGE 2 — AT A GLANCE

### Header

# **What exists today**

Use a status matrix:

| Capability                       | Status         |
| -------------------------------- | -------------- |
| Bengali advisory                 | LIVE           |
| Hybrid RAG                       | LIVE           |
| Safety screening                 | LIVE           |
| Multimodal crop/disease workflow | LIVE           |
| Evidence verification            | LIVE/VALIDATED |
| Local LLM                        | AVAILABLE      |
| Audit/trace                      | LIVE           |
| Offline-oriented knowledge cache | IMPLEMENTED    |
| SMS pathway                      | IMPLEMENTED    |
| Production architecture          | IMPLEMENTED    |
| Soil/irrigation expansion        | INTEGRATION    |
| Voice                            | NEXT PHASE     |
| Institutional dashboard          | NEXT PHASE     |

Do not label anything “LIVE” unless your hosted version actually works at submission time.

---

# PAGE 3 — FIELD ORIGIN

### Header

# **The project began with a field problem.**

Three actual photos:

1. farmer interaction;
2. soil/irrigation issue;
3. crop/problem observation.

Text:

> We began by listening to farmers and observing the practical constraints around agricultural decisions. Language, access to expertise, disease identification, irrigation/soil questions and connectivity repeatedly appeared together rather than as isolated problems.

Then:

# **That became the design brief.**

---

# PAGE 4 — THE RESEARCH PROGRAM

Use the four-stage timeline:

```text
FIELD OBSERVATION
        ↓
KNOWLEDGE FOUNDATION
        ↓
RETRIEVAL FAILURE ANALYSIS
        ↓
INTEGRATED ADVISORY SYSTEM
        ↓
RELIABILITY VALIDATION
        ↓
DEPLOYMENT
```

Bottom:

> The application is the result of a research-development cycle, not a standalone software build.

---

# PAGE 5 — RESEARCH PAPER 1

## Header

# **Research Foundation: Bengali Agricultural Knowledge**

Place actual paper title, venue/link, QR.

Then three boxes:

### We built

> Citation-grounded Bengali agricultural knowledge and evaluation resources.

### We tested

> Instruction tuning, grounding, safety and farmer-oriented evaluation.

### We learned

> Better language behavior does not guarantee exact treatment facts; grounded knowledge remains essential.

Use 3–4 key numbers only.

Your earlier benchmark reports 129 manuals, 290 hierarchical nodes, 139,200 instruction-tuning pairs, 5,300 chemical-safety examples, 1,000 adversarial examples, 145,500 total QA instances, and a 1,001-query Farmer Benchmark. ([arxiv.org](https://arxiv.org/abs/2606.29243?utm_source=chatgpt.com))

---

# PAGE 6 — RESEARCH PAPER 2

## Header

# **Failure Analysis: Where Bengali Agricultural Retrieval Breaks**

Visual:

```text
Standard Bengali
       ↓
stronger retrieval

Farmer language
       ↓
degradation

Regional dialect
       ↓
larger degradation

Banglish
       ↓
largest degradation
```

Then:

> We did not treat this as a linguistic inconvenience. We treated it as an architectural problem.

That's the bridge.

---

# PAGE 7 — WHAT THE RESEARCH CHANGED

Header:

# **The product architecture came from the evidence.**

Table:

| Research finding                                        | Product response           |
| ------------------------------------------------------- | -------------------------- |
| Exact agricultural facts need grounding                 | Structured evidence        |
| Retrieval varies by farmer language                     | Metadata-guided routing    |
| LLMs can misbind related fields                         | Relational verification    |
| Evidence can become stale                               | Versioned/temporal sources |
| Connectivity can fail                                   | Local/cache pathways       |
| Image predictions can conflict with text                | Clarification              |
| Unsafe generation cannot be repaired reliably afterward | Pre-generation safety gate |

This is one of the strongest supporting slides.

---

# PAGE 8 — FULL SYSTEM

Header:

# **KrishokTech in one view**

Use the full architecture diagram.

At bottom:

> One system, multiple modalities, one advisory case.

---

# PAGE 9 — FARMER WORKFLOW

Screenshot sequence:

```text
Ask
 ↓
Understand
 ↓
Upload image
 ↓
Retrieve evidence
 ↓
Verify
 ↓
Answer
 ↓
Follow up
```

Show the actual UI.

Use annotations with 1–2 words:

> Bengali input
> Image
> Evidence
> Verification
> Next step

---

# PAGE 10 — SAFETY

Header:

# **Safety is part of the workflow, not a disclaimer at the end.**

Visual:

```text
USER INPUT
   ↓
SAFETY GATE
   ├── SAFE → continue
   ├── HIGH RISK → stop
   ├── INJECTION → stop
   └── UNCERTAIN → clarify
```

Then one big number:

# **0 / 1,400**

observed unsafe certification in the current adversarial benchmark.

Below small comparison:

> LLM direct: 83.86% unsafe certification
> Vanilla RAG: 69.36%
> LLM judge: 21.79%
> KrishokTech: 0.00%

These numbers are directly in the current results file. 

---

# PAGE 11 — EVIDENCE BINDING

Header:

# **Retrieval is not enough. The system must bind the right facts together.**

Use the current counterfactual experiment.

Visual:

```text
Valid record
Crop ✓
Disease ✓
Active ✓
Dose ✓
PHI ✓
       ↓
CERTIFY
```

Then corrupted:

```text
Crop ✓
Disease ✓
Active from another record ✗
Dose mutated ✗
PHI mutated ✗
       ↓
REJECT
```

Then result:

# **0% false certification**

for the typed verifier under the current 2,000-pair counterfactual test.

Vanilla RAG reports 72.65% certification on the counterfactual evidence. 

---

# PAGE 12 — 11-SLOT SAFETY CONTRACT

Visualize the 11 fields.

Then:

> Removing the dosage-bound constraint produced the largest single hazard increase (+31.6 percentage points), followed by regulatory polarity (+17.8 pp) and active ingredient (+14.2 pp).

Then:

# **80% hazard when typed constraints are removed**

against:

# **0% in the full tested configuration**

This is excellent proof that the structured schema isn't decorative. 

---

# PAGE 13 — MULTIMODAL

Header:

# **The image is not a separate feature. It becomes part of the advisory case.**

Use three screenshots:

### Image

crop identification.

### Disease

crop-specific disease model.

### Advisory

Bengali evidence-grounded answer.

Then show the cross-modal conflict behavior:

> “Text says tomato. Image predicts potato. The system asks before acting.”

Your recent multimodal benchmark reports 100% conflict-triggering in the tested 100-case cross-modal set for the BAA pathway, with 0 observed CUAR.

---

# PAGE 14 — BANGLA / FARMER LANGUAGE

Header:

# **We design for how farmers actually communicate.**

Visual:

| Input style      | Text-first | Detection-gated |
| ---------------- | ---------: | --------------: |
| Standard Bengali |    ~70–73% |            ~93% |
| Farmer benchmark |    ~58–60% |            ~93% |
| Regional dialect |    ~43–45% |            ~90% |
| Banglish         |       ~42% |            ~90% |

Use the final exact values from the canonical results table when typesetting; the current evaluation has roughly these ranges and reports gains of 34–48 percentage points depending on register. 

Bottom:

> **The objective is not perfect language understanding. It is useful and safe agricultural interaction despite language variation.**

---

# PAGE 15 — EXPERT VALIDATION

Header:

# **Agricultural experts evaluated the system—not only developers.**

Use:

### 3

certified agricultural extension specialists/agronomists

### 200

evaluated outputs

### 4.82 / 5

mean correctness rating

### 100%

chemical safety pass rate

### 96.5%

deployment approval

### 0.862

Gwet's AC1 on safety

The current human-validation study reports exactly these values.

Then compare:

> LLM Direct: 38% deployment approval
> Vanilla RAG: 52.5%
> RAG + LLM Judge: 71%
> KrishokTech: 96.5%

This is one of the strongest funding slides.

---

# PAGE 16 — RELIABILITY / RISK

Header:

# **The system is designed to fail safely.**

Use your current risk/coverage graph.

Show:

> deterministic answer
> grounded generation
> clarification
> refusal
> escalation

Then briefly explain:

> As evidence quality decreases, certification coverage is allowed to fall rather than forcing the system to continue generating.

Your retrieval-degradation experiment explicitly reports this behavior: as retrieval recall falls from 1 to 0, certification coverage falls while chemical hazard remains at 0% across the tested 8,000 cases.

---

# PAGE 17 — LOW-CONNECTIVITY

Header:

# **Built for the network conditions that shape rural access.**

Show the current degradation chart:

### Rural edge — 15% packet loss

Cloud only: **82.0%**

Offline cache: **91.4%**

### Severe 2G-like — 30% packet loss

Cloud only: **12.8%**

Offline cache: **58.1%**

Then:

> Controlled network simulation; physical field validation is the next deployment stage.

The values come from the current network stress test. 

---

# PAGE 18 — EFFICIENCY + LOCAL AI

Header:

# **Use the expensive model only when it is needed.**

Show:

```text
Safety / deterministic / structured
          ↓
        < 1 ms class

Generative route
          ↓
       ~1.4 s class
```

Then:

# **61.52%**

zero-LLM terminal handling in the current workload model

and:

# **2.28×**

reported weighted latency improvement in that model

But add a footnote:

> Includes safety/refusal terminal paths; deterministic advisory routes specifically account for the structured-resolution tiers.

This avoids misleading interpretation. 

---

# PAGE 19 — PRODUCTION READINESS

Header:

# **Engineered for deployment, not only demonstration.**

Show the actual repository structure:

```text
frontend
backend
application
domain
ports
infrastructure
ML assets
deployment
tests
audit
research artifacts
```

Then:

### Current verified software baseline

**558 backend tests passed**

**8 skipped**

**0 failed**

**50/50 golden replay**

**frontend build green**

These are in your latest canonical master results. 

Then:

> Production-oriented architecture separates application logic, infrastructure adapters, models, retrieval and audit so the system can evolve without rebuilding the entire product.

The repository itself documents this architecture. ([GitHub][2])

---

# PAGE 20 — ROADMAP + FUNDING

Header:

# **What support unlocks**

Four stages:

### 1. FIELD PILOT

100–1,000 farmer validation

### 2. KNOWLEDGE SCALE

Expert-reviewed agricultural knowledge packs

### 3. SERVICE INTEGRATION

Extension / NGO / agribusiness deployment

### 4. NATIONAL SCALE

Multi-channel advisory infrastructure

Bottom:

# **Research has established the foundation. Deployment is the next experiment.**

Then links:

**GitHub**

**Live demo**

**Research papers**

---

# PART VIII — THE SPECIAL “RESEARCH EVIDENCE” APPENDIX

Because you have enormous experimental material, add **optional appendix pages** after Page 20 if the upload size allows.

These do not need to be read sequentially.

Create:

### Appendix A

CEA experiment map

### Appendix B

Full baseline table

### Appendix C

Safety attack families

### Appendix D

Metamorphic operators

### Appendix E

Temporal/source-conflict tests

### Appendix F

Multimodal tests

### Appendix G

Network/edge benchmark

### Appendix H

Research papers

This is where the 36 experiments can finally breathe.

---

# PART IX — WHICH RESULTS TO PUT WHERE

Your 36-layer database is much richer than the Fair deck should show. Here is the final allocation.

| Experiment                 | Main 8 slides | Supporting dossier | Appendix |
| -------------------------- | ------------: | -----------------: | -------: |
| E02 relational misbinding  |             ✓ |                  ✓ |        ✓ |
| E03 slot ablation          |               |                  ✓ |        ✓ |
| E04 calibration            |               |                  ✓ |        ✓ |
| E05 counterfactual         |               |                  ✓ |        ✓ |
| E06 dialect                |             ✓ |                  ✓ |        ✓ |
| E07/E08 injection          |             ✓ |                  ✓ |        ✓ |
| E09 latency                |               |                  ✓ |        ✓ |
| E10 failure taxonomy       |               |                  ✓ |        ✓ |
| E11 multi-generator        |               |                  ✓ |        ✓ |
| E12 retrieval degradation  |               |                  ✓ |        ✓ |
| E13 expert validation      |             ✓ |                  ✓ |        ✓ |
| E14 network                |               |                  ✓ |        ✓ |
| E15 SMS                    |               |                  ✓ |          |
| E17 routing                |               |                  ✓ |        ✓ |
| E18 LLM dependency         |             ✓ |                  ✓ |        ✓ |
| E19 graph                  |               |                  ✓ |        ✓ |
| E20 telecom economics      |               |                  ✓ |        ✓ |
| E21 dialect hazard         |               |                  ✓ |        ✓ |
| E22 SMS security           |               |                  ✓ |          |
| E23 provenance             |               |                  ✓ |        ✓ |
| E24 knowledge growth       |               |                  ✓ |        ✓ |
| E25 lightweight classifier |               |                  ✓ |          |
| E26 chunk fallback         |               |                  ✓ |        ✓ |
| E28 metamorphic            |               |                  ✓ |        ✓ |
| E29 parametric conflict    |               |                  ✓ |        ✓ |
| E27 expert benchmark       |             ✓ |                  ✓ |        ✓ |
| E30 temporal conflict      |               |                  ✓ |        ✓ |
| E31 multimodal uncertainty |             ✓ |                  ✓ |        ✓ |
| E34 full ablation          |               |                  ✓ |        ✓ |
| E32 oracle routing         |               |                  ✓ |        ✓ |
| E33 wrong routing          |               |                  ✓ |        ✓ |
| E35 normalization          |               |                  ✓ |          |
| E36 source fragmentation   |               |                  ✓ |        ✓ |
| E37 clarification          |               |                  ✓ |        ✓ |
| E38 escalation             |               |                  ✓ |        ✓ |
| E39 IPM                    |     ✓/concept |                  ✓ |        ✓ |

This keeps the main deck clean while still using the enormous research base.

---

# PART X — DO NOT PUT THESE RESULTS IN THE MAIN DECK

There are several current results I would **not use publicly until they are re-audited**, even though they exist in the experiment database.

### E32

The current result shows:

> Oracle 70% correctness / BAA 64% / CUAR values that don't support the clean “routing solves everything” story.

Do not hide it from the research paper. But don't make it a funding-pitch number.

### E33

Similarly, the “wrong high-confidence metadata” result isn't strong enough for a headline.

### E37

The current key metric says:

> BAA clarification gate 5.41% CUAR vs direct answer 0%.

That is obviously not a result we should present as a benefit without auditing the evaluation definition.

### E36

Current source fragmentation still leaves nonzero CUAR.

Again: research weakness, not funding-pitch evidence.

### E35

“100% to 100%” tells us little.

### E19

The 23-node graph is useful proof-of-mechanism but weak as a scale claim.

This is exactly what an expert reviewer would do: **not suppress inconvenient results, but also not confuse every experiment with evidence of product superiority.**

---

# PART XI — EXACT VISUAL DESIGN SPECIFICATION

## Slide size

# 16:9 widescreen

Use:

**1920 × 1080**

for all generated raster assets.

---

## Main visual language

### Background

Near-white.

### Primary

Deep agricultural green.

### Secondary

Warm earth / muted sand.

### Accent

One restrained technology blue.

### Text

Very dark charcoal.

Do not use:

* neon gradients;
* cyberpunk aesthetics;
* glowing AI brains;
* robots;
* generic futuristic agriculture imagery;
* excessive green leaves around everything.

This is Bangladesh national innovation, not a crypto startup.

---

# PART XII — GPT IMAGE GENERATION RULE

For generated conceptual graphics, use this suffix in every prompt:

```text
16:9 widescreen presentation graphic, premium government innovation showcase style, realistic but polished, Bangladesh-specific agricultural context, restrained agricultural green and warm earth palette, clean white negative space, crisp visual hierarchy, minimal text, no logos, no watermark, no decorative typography, no fake statistics, no futuristic holograms, no generic Silicon Valley imagery.
```

For charts, **do not use GPT image generation**.

Generate charts from actual data.

For screenshots, **never use GPT image generation**.

Use real UI.

For the architecture diagram, I prefer programmatic/vector construction rather than image generation because textual fidelity matters.

---

# PART XIII — WHAT THE MAIN DECK SHOULD LOOK LIKE VISUALLY

The rhythm should be:

### Slide 1

**real photograph**

### Slide 2

**conceptual comparison graphic**

### Slide 3

**research timeline**

### Slide 4

**hero architecture**

### Slide 5

**numbers + evidence**

### Slide 6

**market ecosystem**

### Slide 7

**impact/inclusion/SDG**

### Slide 8

**roadmap + QR/demo**

That gives:

> human → problem → credibility → technology → proof → business → responsibility → ask.

Excellent pitch structure.

---

# PART XIV — ACTUAL UI SCREENS YOU NEED TO BUILD BEFORE SUBMISSION

These are more important than adding another model.

## Screen 1 — Farmer home

Must show:

> Ask a question
> Upload crop photo
> Optional context

---

## Screen 2 — Answer screen

Must show:

> answer

> verification status

> source

> next action

---

## Screen 3 — Why this answer?

Must show:

> evidence

> source

> confidence

> verification

> model/route

This is very close in spirit to RAGVUE and SmartMatch's emphasis on interactive inspection. ([ACL Anthology][4])

---

## Screen 4 — Image workflow

Show:

> image → crop → disease → advisory

---

## Screen 5 — Conflict workflow

Show:

> text says Tomato
> image predicts Potato

Then:

> **Please confirm before continuing.**

---

## Screen 6 — Unsafe request

Show:

> Request blocked.

Then:

> Why?

Then:

> official support / extension contact.

---

## Screen 7 — Offline mode

Show:

> Connected / Limited / Offline

And which capabilities remain active.

---

## Screen 8 — Expert mode

Show:

> case ID

> evidence

> source version

> verification state

> review actions.

---

# PART XV — THE ONE “WOW” FEATURE I WANT YOUR AGENTS TO BUILD

This is worth prioritizing.

## **Explainable Advisory Trace**

For every response, user can click:

# **Why did KrishokTech answer this way?**

Then an animated vertical trace:

```text
1. Farmer input
      ↓
2. Language interpreted
      ↓
3. Safety checked
      ↓
4. Agricultural context identified
      ↓
5. Evidence selected
      ↓
6. Advisory generated
      ↓
7. Critical facts verified
      ↓
8. Final response delivered
```

Each node opens one compact detail panel.

This will make the Fair demo and later EACL demo dramatically better.

The current repository already returns trace events through its SSE/agent-trace workflow. ([GitHub][2])

---

# PART XVI — THE SECOND “WOW” FEATURE

# **Try to Break the Advice**

Build a demo mode.

Start from one validated treatment record.

Buttons:

> Change crop
> Change disease
> Change dosage
> Change formulation
> Change PHI
> Use outdated source
> Add malicious instruction

Then run:

### Unrestricted baseline

vs

### KrishokTech

Show:

```text
Baseline
✗ accepts corrupted evidence

KrishokTech
✓ detects mismatch
✓ rejects certification
✓ explains failure
```

This turns your CEA work into a **live interactive demonstration**.

The current counterfactual and metamorphic results make this especially well justified.  

---

# PART XVII — THE THIRD “WOW” FEATURE

# **Ask Like a Farmer**

Create a small set of real-style queries.

Examples:

> “আলুতে পচা ধরছে কী দিব?”

> “morich e kala dag hoise ki korbo”

> “ধানের পাতা পুড়ে যাইতেছে”

The app shows:

> **How KrishokTech interpreted your question**

Then:

> evidence.

This turns your second paper into a product capability.

---

# PART XVIII — 250-WORD DESCRIPTION SUPPORTING EVIDENCE

When a judge reads the description, they should be able to find the corresponding evidence instantly:

| Description claim | Evidence                   |
| ----------------- | -------------------------- |
| field-driven      | field photographs + Page 3 |
| Bengali-first     | Paper 1/2 + Page 14        |
| multimodal        | Page 13                    |
| safety            | Pages 10–12                |
| research-backed   | Pages 5–7                  |
| deployment        | Pages 17–19                |
| scalable          | Page 20                    |

This is exactly how we avoid “AI-generated pitch” vibes.

Everything has a trace.

---

# PART XIX — THE TECHNICAL DETAILS MUST NOT SOUND LIKE A CV

Avoid this:

> “We use Python, FastAPI, Next.js, FAISS, BM25, YOLO, Gemini…”

That is an inventory.

Instead explain:

> **what each technical choice enables.**

For example:

> “Precomputed retrieval indexes allow the system to serve evidence locally without rebuilding the corpus during a request.”

Much stronger.

The repository explicitly uses precomputed indexes loaded at startup and separates model/infrastructure adapters from application logic. ([GitHub][2])

---

# PART XX — HOW TO HANDLE THE PAPERS

You were right that the papers matter.

But the visual treatment should be:

# **Evidence of technical maturity**

Not:

# **Our publications**

Use four cards:

### Research Foundation

KrishokTech benchmark

### Retrieval Research

Where Retrieval Fails

### Reliability Research

CEA manuscript

### System Demonstration

EACL Demo

Each card gets:

* paper title;
* one-sentence finding;
* QR/link.

That is enough.

---

# PART XXI — THE RESEARCH TIMELINE WORDING

Use exactly:

> **We followed the problem from field observation to evidence, from evidence to failure analysis, and from failure analysis to system design.**

Then:

> **The product is the engineering outcome of that research loop.**

This is natural and strong.

---

# PART XXII — THE COMMERCIALIZATION WORDING

Use:

> **KrishokTech is designed as shared advisory infrastructure rather than a single-purpose consumer app.**

Then:

> Farmers benefit from the service; institutions provide sustainable deployment, integration and scale.

This is a much more mature business proposition.

---

# PART XXIII — THE MARKET DEMAND WORDING

Use:

> Agricultural advisory demand already exists through Bangladesh's extension ecosystem, weather/advisory services and formal agricultural support channels. KrishokTech is designed as a digital intelligence layer that can complement these channels rather than replace them.

Bangladesh already has formal agricultural advisory infrastructure, including BAMIS services and the 16123 agricultural call center. ([bamis.gov.bd](https://www.bamis.gov.bd/en/advisory/?utm_source=chatgpt.com)) ([ais.gov.bd](https://ais.gov.bd/site/page/d9147061-2995-416f-b355-d7feb0d9f9a1/%5Bfront%5D?utm_source=chatgpt.com))

This is very strong because you're not inventing a fictional market.

---

# PART XXIV — THE FUNDING STORY

Never say:

> “We need funding to finish development.”

That makes it sound incomplete.

Use:

> **The core platform has already been built. Funding is needed to move from controlled validation to field validation, institutional integration and broader deployment.**

That is the exact transition the Fair says it wants to support. ([innovationfairbd.org](https://innovationfairbd.org/about))

---

# PART XXV — WHAT TO BUILD IN THE NEXT 48 HOURS

Since your deadline is immediate, priority is **presentation readiness**, not another 25 experiments.

## Absolute priority

### 1.

Polished live demo.

### 2.

Unified farmer workflow.

### 3.

Why-this-answer evidence view.

### 4.

Image continuation.

### 5.

Safety refusal.

### 6.

Demo mode.

### 7.

Production-health page.

### 8.

Supporting dossier.

### 9.

Main 8-slide deck.

### 10.

250-word + technical-details final proofreading.

---

# PART XXVI — WHAT TO BUILD AFTER SUBMISSION

Then continue:

### 1

Temporal source governance.

### 2

Voice input.

### 3

Expert handoff.

### 4

Knowledge editor.

### 5

Institution dashboard.

### 6

Physical edge/energy.

### 7

Farmer pilot.

### 8

Soil/irrigation validated integration.

Those are valuable for the CEA/EACL trajectory.

---

# PART XXVII — THE FULL EACL/CURRENT RESEARCH STORY SHOULD SIT BEHIND THE FAIR

Your final intellectual architecture is:

```text
FIELD
 │
 ▼
BENGALI AGRICULTURAL KNOWLEDGE
 │
 ▼
RETRIEVAL FAILURE RESEARCH
 │
 ▼
INTEGRATED KRISHOKCHAT
 │
 ├─────────────┐
 ▼             ▼
APPLICATION   RELIABILITY
 │             │
 ▼             ▼
EACL DEMO     CEA
 │             │
 └──────┬──────┘
        ▼
 FIELD DEPLOYMENT
```

This is excellent.

It avoids three separate-looking projects.

---

# PART XXVIII — THE EXACT FINAL “MASTER MESSAGE”

Everything should converge toward this:

> **KrishokTech is a Bangladesh-focused agricultural intelligence platform built from real farmer problems, strengthened by research, and engineered for safe deployment. It combines Bengali language interaction, crop-image understanding, agricultural evidence, safety verification and low-connectivity pathways so that the system can answer when it has evidence, ask when it needs context, and refuse when it cannot justify the advice.**

That is the innovation.

Not:

> RAG.

Not:

> LLM.

Not:

> vision.

Not:

> chatbot.

---

# PART XXIX — FINAL AGENT EXECUTION SPEC

Give your implementation agents these rules verbatim.

## Product

> Treat KrishokTech as a unified agricultural advisory platform, not a collection of features.

## UX

> Every farmer interaction should become a structured advisory case that can carry text, image, context, evidence, verification and follow-up.

## Trust

> Every high-risk response must expose evidence status and verification state.

## Safety

> Never present unsupported chemical advice as a normal answer.

## Multimodal

> Text and image signals must be reconciled explicitly; contradictions must trigger clarification.

## Offline

> The application must visibly distinguish online, limited and offline operating states.

## Research

> Every benchmark/demo case must be replayable.

## Demo

> Build one-click Demo Mode with prevalidated scenarios.

## Evidence

> No number enters the Fair deck unless it exists in the canonical results source.

## Visuals

> Use real screenshots and field photos for evidence; use generated images only for conceptual visuals.

## Writing

> Use concrete, plain language. Avoid phrases such as “revolutionary,” “game-changing,” “cutting-edge,” “AI-powered solution,” “seamlessly,” “leveraging state-of-the-art,” unless a sentence genuinely requires them.

## Claims

> Never say “first,” “100% safe,” “hallucination-free,” “production deployed,” or “nationally validated” unless independently supported.

## Main deck

> Eight slides only. One dominant idea per slide. Do not turn the deck into a condensed research paper.

---

# PART XXX — FINAL QA BEFORE UPLOAD

Before submitting the Innovation Fair application, run this exact checklist.

### Administrative

* Applicant type correct.
* Category selected as **Agriculture & Food Technology** unless the form circumstances require otherwise.
* 250-word field ≤250.
* Technical-details field complete.
* PPT exactly **8 slides**.
* Supporting file opens correctly.
* Project photo included.
* Government/private commercialization fields answered truthfully.
* Live demo URL works.
* GitHub URL works. ([Innovation Fair][5])

### Main deck

* No slide has more than one major idea.
* No slide is text-heavy.
* All numbers match canonical results.
* All screenshots are real.
* All QR codes work.
* No unsupported partnership claims.
* No unsupported national-deployment claims.
* Final slide clearly says what funding unlocks.

### Supporting dossier

* Every major claim points to evidence.
* Papers are linked, not dumped.
* Current status is clearly separated from future roadmap.
* Simulated results are labeled as simulated.
* No contradictory old numbers remain.
* E32/E33/E36/E37 do not appear as positive headline evidence until audited.
* CEA/EACL submission statuses are updated only after actual submission.

### Live system

* Demo mode works without credentials.
* At least five safe reproducible cases work.
* One unsafe case works.
* One ambiguous case works.
* One image case works.
* Evidence panel works.
* Offline/local mode works or is honestly labeled.
* No API key appears in frontend.
* Health endpoint works.
* Error state is graceful.

---

# The single biggest thing I want you to remember

**Do not try to convince the judges that KrishokTech contains the most technology.**

Convince them that:

> **you found a real Bangladesh problem, investigated it scientifically, built around the actual failure modes, created a functioning system, tested it seriously, and now have a credible path from research to field deployment and institutional scale.**

That is much harder for another project to imitate.

And your current evidence really does support that story: the repository shows a substantive modular system and production-oriented structure; the expert evaluation reports 4.82/5 mean correctness, 100% chemical-safety pass and 96.5% deployment approval; the adversarial benchmark reports 0/1,400 unsafe certifications; and the structured/counterfactual tests provide unusually strong evidence that the verification layer is doing something materially different from ordinary retrieval. ([GitHub][2])   

The right **next execution order** is therefore: **freeze the wording → build the 8-slide deck → build the 20-page evidence dossier → polish the live demo around the three “wow” workflows → audit every number once more → submit.**

[1]: https://aclanthology.org/2026.eacl-demo.34/?utm_source=chatgpt.com "AI for Climate Finance: Agentic Retrieval and Multi-Step Reasoning for Early Warning System Investments - ACL Anthology"
[2]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System "GitHub - RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
[3]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System/blob/main/production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md "KrishokTech-Agricultural-Advisory-System/production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md at main · RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
[4]: https://aclanthology.org/2025.acl-demo.0/?utm_source=chatgpt.com "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations) - ACL Anthology"
[5]: https://innovationfairbd.org/innovator-application-form "Innovation Fair"
