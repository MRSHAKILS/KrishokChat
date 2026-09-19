I went back through the **whole integrated project**, not just the current CEA manuscript: the GitHub repository structure and implementation, the production-oriented deployment layer, the current experiment registry/results, the earlier KrishokTech research line, and the actual EACL System Demonstrations call plus recent accepted EACL/ACL demos.

My conclusion is stronger than before:

**KrishokTech is a very good EACL Demo candidate, but the winning paper should not be “an agricultural chatbot with many features.”** The EACL paper should present KrishokTech as an **open, production-oriented, safety-aware Bengali AI advisory platform whose distinguishing property is that multiple NLP/vision/retrieval capabilities are integrated into a transparent, user-observable decision workflow**.

The CEA paper should carry the deeper scientific reliability experiments. The EACL paper should carry the **system experience, integration, usability, deployment-readiness, and reproducibility story**.

The official EACL 2027 Demo CFP explicitly welcomes application systems, reusable components, tools, and systems that may range from prototypes to mature production-ready systems. It requires three things: a ≤6-page paper, a ≤2.5-minute screencast, and either a live demo website or installable package; missing any of those causes desk rejection. It also explicitly asks reviewers to assess motivation/novelty, related work/contribution, system and demo description, evaluation/availability/licensing, and presentation quality. ([EACL 2027][1])

And your repo is much more substantial than the word “prototype” in the top-level README suggests: it has a layered FastAPI/Next.js architecture, port/adapter separation, provider-switchable LLM infrastructure, audit logging, SSE traces, image routing, deployment controls, readiness/liveness, versioning, security headers, concurrency limits, production build scripts, and a public repository. ([GitHub][2]) ([GitHub][2]) ([GitHub][2])

So I would build the EACL paper around **that actual system**, while carefully avoiding claims that belong to the CEA paper.

---

# 1. The exact EACL identity I recommend

## Working title

### **KrishokTech: A Safety-Aware Multimodal Bengali Agricultural Advisory Platform**

This is the title I would use unless we discover a stronger system-level novelty during implementation.

Two alternatives:

**KrishokTech: An Auditable Multimodal Bengali Agricultural Advisory System**

**KrishokTech: Production-Oriented Bengali Agricultural Advisory with Retrieval, Vision, and Safety-Aware Routing**

I prefer the first because it is clear, broad, and immediately tells an EACL reviewer what the artifact is.

---

# 2. The one-sentence system pitch

The paper should be reducible to:

> **KrishokTech is an open Bengali agricultural advisory platform that integrates safety screening, hybrid retrieval, grounded generation, multimodal crop-disease diagnosis, evidence/provenance inspection, and deployment-oriented safeguards into an observable end-to-end workflow.**

That is enough to explain why this is a **system demonstration** rather than another standalone RAG experiment.

The repository already supports the bulk of these capabilities: hybrid BM25+dense retrieval, a four-stage safety→retrieval→generation→verification pipeline, six-way safety classification, audit logs, streaming traces, crop/disease image routing, replaceable LLM adapters, weather/helpline support, and structured API responses. ([GitHub][2]) ([GitHub][2])

---

# 3. What EACL Demo reviewers are actually rewarding

The official call is unusually explicit.

They want to know:

### Motivation, fit, novelty

Why this system matters to NLP and what is novel compared with existing systems.

### System and demonstration

How it works, who uses it, what users can do, whether the UI is actually usable.

### Evaluation

Some evidence that the thing is useful/quality-controlled.

### Availability/licensing

Can reviewers actually access it?

### Presentation

Can the architecture and workflow be understood quickly? ([EACL 2027][1])

Recent accepted demos strongly reinforce this pattern.

---

# 4. What recent accepted demos teach us

## A. AI for Climate Finance

This is probably the **closest paper archetype** for KrishokTech.

It does not pretend that hybrid retrieval, agents, structured extraction, and reasoning are individually novel. It explicitly says the contribution is their **integration into a domain-specific workflow**. It then gives:

* a concrete task;
* a multi-stage system;
* annotated data;
* comparative evaluation;
* expert evaluation;
* a public deployment;
* demonstration scenarios;
* detailed appendices. ([ACL Anthology][3]) 

That is almost exactly the model we should follow.

### Lesson for KrishokTech

We should say:

> the component technologies are established; the contribution is the integrated Bengali agricultural advisory workflow and its operationalization.

---

## B. Browser-based multimodal verification assistant

This paper emphasizes:

* an existing real-world user problem;
* integration of multiple NLP services;
* unified UI;
* actionable signals;
* real-world usage context.

It specifically says it showcases the architecture, integration of services, and real-world application. ([ACL Anthology][4])

### Lesson

Your paper should not merely enumerate models.

It should show:

> **one farmer task → multiple backend capabilities → unified user-facing result.**

---

## C. RAGVUE

RAGVUE is especially interesting because it has a **system interface built around inspecting model behavior**. It exposes a Python API, CLI, and UI, and its demo shows both summary and individual-case diagnostic views. ([ACL Anthology][5]) 

### Lesson

Your existing agent-trace UI is not decoration.

It should become a major selling point:

> **the system lets the user see what happened, not just what the model said.**

---

## D. SmartMatch

SmartMatch exposes backend choices, retrieved items, similarity scores, qualitative cues, and latency through its interface. ([ACL Anthology][6])

### Lesson

Add **inspectability** to KrishokTech.

Don't merely show the answer.

Let the user/reviewer inspect:

* route;
* evidence;
* confidence;
* model;
* latency;
* verification;
* source.

---

## E. FlexRAG

FlexRAG's value is integration and accessibility: text, multimodal, network-based RAG, lifecycle support, asynchronous processing, caching, and public source code. ([ACL Anthology][7])

### Lesson

Your production-oriented modularity is useful **if surfaced as a capability**, not as software-engineering trivia.

---

# 5. The biggest strategic decision

I would turn KrishokTech from:

> **chat + image diagnosis + weather + safety + research dashboard**

into a **unified agricultural assistance workspace**.

The conceptual unit should be:

# **One advisory session**

A session may include:

* text;
* image;
* context;
* evidence;
* history;
* safety state;
* recommendation;
* provenance;
* escalation.

This is much stronger than disconnected pages.

---

# 6. What I want the finished application to look like

The landing point should be a single farmer-oriented workspace.

Something like:

```text
                    KRISHOKCHAT
            Bengali Agricultural Assistant

  ┌────────────────────────────────────────────────────┐
  │ What is happening to your crop?                    │
  │                                                    │
  │ "আমার আলু গাছে পাতায় কালো দাগ পড়েছে..."           │
  │                                                    │
  │ [🎤 Voice] [📷 Photo] [🌾 Crop] [📍 District]     │
  └───────────────────────┬────────────────────────────┘
                          ▼
                 Understanding request
                          │
         ┌────────────────┼──────────────────┐
         ▼                ▼                  ▼
      Safety          Crop/Disease        Context
      check             evidence        information
         │                │                  │
         └────────────────┼──────────────────┘
                          ▼
                    Advisory engine
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
         Facts/RAG      Vision      Clarification
             │            │            │
             └────────────┼────────────┘
                          ▼
                    Verification
                          │
                          ▼
                     Advice card
                          │
       ┌──────────────────┼───────────────────┐
       ▼                  ▼                   ▼
    Bengali           Evidence             Next step
    advice             source             / escalation
```

The important concept is:

> **every capability contributes to the same advisory object.**

---

# 7. New flagship feature #1 — “Why this advice?”

This is the first feature I would definitely add.

Every answer should have an expandable panel:

### Why this answer?

```text
Decision
✓ Crop: Potato
✓ Problem: Late blight

Evidence
✓ BARI source
✓ DAE source
✓ Source version
✓ Retrieved evidence

Safety
✓ No restricted chemical conflict
✓ Dose field verified
✓ PHI verified

Generation
✓ LLM used for Bengali explanation

Verification
✓ Passed
```

Then:

> **View source**

opens the exact relevant evidence.

This is a direct application of the inspectability pattern seen in RAGVUE/SmartMatch-style demonstrations, but tailored to the agricultural context.  ([ACL Anthology][6])

For EACL, this is gold.

---

# 8. New flagship feature #2 — “Answer status”

Do not make all responses look identical.

Show a visible system status:

### VERIFIED

Evidence-complete and verified.

### GROUNDED

RAG-generated and evidence-supported.

### NEEDS CLARIFICATION

The query is underspecified.

### LIMITED

Knowledge available but insufficient for certification.

### BLOCKED

Safety policy prevents response.

### ESCALATED

Requires human/official assistance.

This gives the application a **real decision-support UX**.

---

# 9. New flagship feature #3 — “Evidence timeline”

Since the CEA research is going to add temporal/versioned evidence, surface a simplified version in the application.

Example:

```text
Recommendation
│
├── Source: BARI
├── Published: 2024
├── Verified: 2026-08-20
├── Knowledge pack: v1.7
└── Current regulatory status: valid
```

This makes the system visibly different from generic ChatGPT-style chat.

---

# 10. New flagship feature #4 — “Ask safely”

Give the user an interaction mode specifically for uncertain problems.

Example:

> “পাতায় দাগ হয়েছে।”

The system doesn't hallucinate.

It says:

```text
I need 2 more details:

1. Which crop?
2. Can you upload a photo?
```

Then the UI offers:

**Upload photo**

**Choose crop**

**Describe symptom**

This is very important because it demonstrates intelligent interaction rather than mere refusal.

---

# 11. New flagship feature #5 — multimodal case continuation

This would make the vision module much more powerful.

Current repo:

> image → crop classifier → crop-specific disease model → Bengali diagnosis/treatment advice. ([GitHub][2])

Don't leave it as a separate `/detect` page.

Instead:

### User starts with text

> “আমার গাছের পাতায় দাগ হয়েছে।”

Then attaches image.

System continues the same session:

> “The image is consistent with potato late blight. I found three relevant verified sources…”

This is a much more impressive NLP demo because the modalities **interact** rather than merely coexist.

---

# 12. New flagship feature #6 — cross-modal contradiction handling

This is one of the best new features we can add.

Example:

Text:

> “আমার টমেটো গাছে…”

Image classifier:

> potato.

System:

```text
⚠ The text and image provide conflicting crop signals.

Text: Tomato
Image: Potato (0.91)

Would you like to:
[Confirm tomato]
[Use image result]
[Upload another photo]
```

This is excellent for:

* multimodal reliability;
* user interaction;
* demonstration;
* research credibility.

And it complements the CEA paper's multimodal uncertainty experiments without making the EACL paper about the same scientific experiment.

---

# 13. New flagship feature #7 — “Safe action card”

Do not present chemical advice as ordinary prose.

Present a structured card:

```text
RECOMMENDATION

Crop
Potato

Problem
Late blight

Treatment
[active ingredient]
[formulation]

Dose
...

Interval
...

PHI
...

Evidence
BARI / DAE

Status
✓ Verified
```

The prose explanation can sit below.

This visually demonstrates the distinction between:

> **structured agricultural fact**

and:

> **LLM explanation**.

That also aligns beautifully with the CEA architecture.

---

# 14. New flagship feature #8 — structured advice rather than chat-only

Modern system demos increasingly make structured outputs visible.

AI for Climate Finance turns document evidence into structured pillar/budget results with clickable evidence. 

Your equivalent should be:

> farmer question → structured advisory record.

The user should be able to switch between:

### Farmer view

Simple Bengali.

### Expert view

Structured evidence/metadata.

### Trace view

Pipeline details.

This is excellent for both recruiters and researchers.

---

# 15. New flagship feature #9 — farmer/expert view toggle

This one is very practical.

## Farmer mode

Minimal:

> “What should I do?”

## Extension/agronomist mode

Shows:

* diagnosis confidence;
* source;
* evidence;
* treatment relation;
* verification;
* history;
* unresolved issues.

This helps establish KrishokTech as a **dual-audience system**:

> farmer-facing advisory + expert oversight.

That makes the system more serious than a consumer chatbot.

---

# 16. New flagship feature #10 — “case handoff”

This is potentially excellent.

When the system cannot safely resolve a case:

### Generate a case summary

```text
CASE ID: KC-2026-00451

Crop: Potato
Suspected problem: Late blight
Image confidence: 0.71
Text evidence: incomplete
Safety status: unresolved

Evidence inspected:
3 sources

Reason for escalation:
No jointly supported treatment relation.

Attachments:
1 image
2 farmer messages
```

Then:

**Download case**

or

**Share with extension officer**

or

**Call official support**

This turns “I don't know” into a productive system behavior.

For EACL reviewers, that's a very compelling human-AI interaction feature.

---

# 17. New flagship feature #11 — intervention ladder

I would visibly classify the request:

```text
Informational
      ↓
Management
      ↓
Treatment
      ↓
Chemical intervention
      ↓
High-risk / prohibited
```

And the system becomes increasingly conservative.

This is a UX representation of the CEA paper's authority model.

It also makes the system understandable to a nontechnical reviewer.

---

# 18. New flagship feature #12 — “compare options”

For some agricultural questions, instead of returning one opaque answer:

```text
Option A
Chemical treatment
Evidence: high
PHI: 14 days

Option B
Cultural control
Evidence: high

Option C
IPM combination
Evidence: moderate
```

This is valuable for agriculture and makes the system feel more like a **decision-support assistant** rather than a chatbot.

The caveat is that options must come from supported agricultural knowledge, not free-form generation.

---

# 19. New flagship feature #13 — weather contextualization

You already have Bengali weather + agricultural tip. ([GitHub][2])

Don't make `/weather` a random extra.

Integrate it:

> “Should I spray today?”

System can present:

* current weather;
* forecast;
* relevant advisory condition;
* evidence;
* uncertainty.

This should be framed as:

> **context-aware advisory**

not a weather chatbot.

But only use live weather data if the production environment can reliably provide it.

---

# 20. New flagship feature #14 — “knowledge freshness” indicator

The application should show:

> Knowledge updated: 2 days ago

and maybe:

> 12/13 institutional sources current.

This is a very strong trust feature.

The recent agricultural literature's move toward temporal RAG makes this especially timely. Current TARAG work explicitly addresses time-aware agricultural knowledge retrieval. ([ACL Anthology][8])

---

# 21. New flagship feature #15 — offline mode indicator

Don't simply claim “offline capable.”

Show the operating state:

```text
🟢 Online
🟡 Limited connectivity
🔵 Offline mode

Available offline:
✓ Safety
✓ Crop diagnosis
✓ Verified facts
✓ Cached advisories

Unavailable:
○ Live weather
○ Remote LLM
```

This is a genuine systems feature.

---

# 22. New flagship feature #16 — local LLM fallback

The repo already supports:

* Gemini online;
* local KrishokTech-4B via Ollama. ([GitHub][2])

Make model availability explicit:

```text
Generation:
● Online Gemini
○ Local KrishokTech-4B
```

And if the local model is unavailable, the system already fails closed. ([GitHub][2])

That is an excellent demonstration feature.

---

# 23. New flagship feature #17 — graceful degradation

This is one of the strongest system-level features you can build.

Create an actual **degradation controller**.

When remote LLM fails:

```text
Remote unavailable
       ↓
Local evidence lookup
       ↓
Structured advisory
       ↓
No safe fact found?
       ↓
Clarification / escalation
```

When dense retrieval fails:

```text
dense unavailable
       ↓
BM25
       ↓
structured lookup
```

When image model fails:

```text
vision unavailable
       ↓
text advisory
```

This demonstrates **service continuity**, which is very appropriate for an operational system.

---

# 24. New flagship feature #18 — live system health panel

For the reviewer/developer:

```text
SYSTEM STATUS

Safety model          ✓
Dense index            ✓
Fact store             ✓
Vision models          ✓
LLM provider           ✓
Knowledge version      v1.7
Cache                  ✓
Last verification      14:02
```

The repository already has `/health` and `/readyz` plus deployment controls. ([GitHub][2])

Expose a **non-sensitive public health dashboard**.

This strengthens the production-oriented story.

---

# 25. New flagship feature #19 — audit explorer

Current system already records safety events locally and exposes metrics. ([GitHub][2])

Turn `/analytics` into something much more impressive:

```text
Last 24 hours

Total requests
Safety blocks
Clarifications
Verified advisories
Abstentions
Escalations

Top failure reasons
```

And a sample case:

> Request → route → evidence → decision.

The EACL reviewer can understand system behavior without reading your code.

---

# 26. New flagship feature #20 — “research mode”

You already have research/benchmark pages in the frontend. ([GitHub][2])

Keep them, but change the meaning.

Not:

> “Here are numbers from my previous papers.”

Instead:

### Research Mode

> Inspect KrishokTech's decision process.

Features:

* switch retriever;
* toggle generation provider;
* inspect retrieved evidence;
* view verifier status;
* compare model outputs;
* inspect latency.

This makes the system useful to researchers, which is very suitable for an NLP demo.

RAGVUE and SmartMatch are good precedents for exposing internal evaluation/selection behavior through a UI.  ([ACL Anthology][6])

---

# 27. New flagship feature #21 — A/B comparison mode

This could be fantastic for the demo.

Let the reviewer choose:

### Vanilla RAG

vs

### KrishokTech Safety-Aware

Then show:

```text
Retrieved sources
Answer
Safety status
Critical fields
Verification
Latency
```

For a demonstration track, this is much more powerful than merely stating:

> “our method is safer.”

The application **demonstrates the difference interactively**.

---

# 28. New flagship feature #22 — evidence corruption sandbox

Since the CEA paper contains the sophisticated verification experiments, make a lightweight public research tool:

```text
Choose a verified fact

[Corrupt dosage]
[Swap formulation]
[Change PHI]
[Swap crop]
[Use old source]
```

Then:

### Vanilla RAG

> may still answer.

### KrishokTech verifier

> rejects.

This is almost certainly the **single best research demonstration feature** we could add.

The current E2/E3/E5 results already show why it matters. The current typed verifier rejects all tested counterfactual certifications while Vanilla RAG accepts large proportions of corrupted cases. 

For the EACL demo, this turns an abstract security/safety result into something a reviewer can play with.

---

# 29. New flagship feature #23 — evidence provenance graph

Click:

> “Dose 2–2.5 g/L”

and display:

```text
Claim
 ↓
Structured fact
 ↓
Source node
 ↓
Institution
 ↓
Document
 ↓
Version/date
```

This is a very strong research-tool feature.

It borrows the spirit of the evidence-span presentation in the accepted AI for Climate Finance demo. That paper lets users click evidence spans back to source PDF passages. 

---

# 30. New flagship feature #24 — voice input

This would make the system substantially more compelling for Bengali agricultural NLP.

The repository is text/image oriented today, but a practical farmer system could accept:

> Bengali speech → ASR → safety → advisory.

However:

**do not add speech merely because it looks impressive.**

Add it only if we can demonstrate:

* robust Bengali ASR;
* noisy rural-style speech;
* dialect;
* code switching;
* transcription errors;
* safe handling of uncertain transcription.

This would align particularly well with the broader Bengali agricultural voice-advisory literature and your earlier work.

---

# 31. Best voice design

Don't simply do:

> voice → text → answer.

Do:

```text
Voice input
   ↓
ASR
   ↓
Transcript shown to farmer
   ↓
"Did I understand you correctly?"
   ↓
Safety / advisory pipeline
   ↓
Text + optional audio answer
```

That is better UX and safer.

---

# 32. New flagship feature #25 — “farmer language normalization”

Your previous research already studies Bengali retrieval failures.

Expose this capability:

```text
Farmer input:
"আলুতে পঁচা ধরছে"

Normalized:
Potato disease / rot-like symptom
```

Then show:

> “I interpreted your expression as…”

This would connect your **three-paper research lineage** inside the application without duplicating the research papers.

---

# 33. New flagship feature #26 — dialect-aware query explanation

For regional terms:

> “What does this word mean?”

The system can show:

```text
Input term: "pora rosh"

Interpreted as:
[Candidate pathology term]

Confidence:
0.67

Need confirmation?
[Yes] [No]
```

This is significantly more responsible than silently normalizing a dialect term.

---

# 34. New flagship feature #27 — multilingual source transparency

If a source is Bengali:

> source in Bengali.

If a source is English:

> original source + Bengali explanation.

Do not translate evidence silently.

This makes provenance more trustworthy.

---

# 35. New flagship feature #28 — “safe export”

Allow the user to export a case as:

### PDF / printable advisory

or

### SMS

or

### extension-officer case summary.

The important thing is:

> export from the **certified structured object**, not from a fresh LLM summarization.

That reuses your E15/E22 work elegantly.

---

# 36. New flagship feature #29 — SMS simulation

Your UI could have:

> **Send as SMS**

and show:

```text
Characters: 113 / 160
Safety fields preserved: 5 / 5
Source: verified
```

This would make the low-connectivity contribution visible in the demo.

Your current experiment already reports deterministic GSM template preservation and no length violations on the tested tuples. 

---

# 37. New flagship feature #30 — deployment profiles

Offer:

### Cloud

### Hybrid

### Offline

and show which capabilities are active.

Example:

```text
HYBRID MODE

Local:
✓ safety
✓ vision
✓ structured facts
✓ cache

Remote:
✓ complex generation
```

This is both useful for deployment and highly demonstrable.

---

# 38. New flagship feature #31 — “model independence”

Your LLM port abstraction is a real engineering strength. The repository allows OpenRouter/Gemini/Ollama/stub switching without changing application logic. ([GitHub][2])

Make it visible:

> **KrishokTech is model-provider agnostic.**

But don't oversell this as research novelty.

It is a system-quality feature.

---

# 39. New flagship feature #32 — no external-data mode

A powerful reproducibility option:

> **Research reproducibility mode**

runs entirely from:

* frozen corpus;
* local models;
* deterministic pipeline.

This is ideal for reviewers.

It also protects your demo from API outages.

---

# 40. New flagship feature #33 — “replay this case”

Every research/demo example should have:

> **Replay**

which reproduces:

* same query;
* same evidence version;
* same model;
* same verification;
* same final answer.

Your master-results infrastructure already uses deterministic replays extensively. 

Turn that into a visible capability.

---

# 41. New flagship feature #34 — “case provenance ID”

Every response gets:

> `KC-CAS-8F31A2`

Clicking it shows:

* timestamp;
* route;
* evidence version;
* model;
* verification.

This creates a clean audit identity.

---

# 42. New flagship feature #35 — capability routing visibly demonstrated

Your current architecture already has a clear four-stage QA pipeline and separate vision pipeline. ([GitHub][2])

For the demo, show:

```text
Query type:
Pesticide question

Selected capability:
Treatment Advisory

Resolution:
Structured fact

Generation:
Not required

Verification:
Passed
```

Then another:

```text
Query type:
Ambiguous disease

Selected capability:
Clarification

Resolution:
No safe fact

Generation:
Skipped
```

This makes the internal system logic visible.

---

# 43. New flagship feature #36 — “LLM called?” badge

This can be surprisingly effective.

Every answer:

```text
LLM CALLS: 0
```

or:

```text
LLM CALLS: 1
Reason: language realization
```

That connects your CEA efficiency research to the product without becoming the main EACL contribution.

---

# 44. New flagship feature #37 — response diff

For research mode:

> Compare answer before and after verification.

Example:

```text
Generated:
Use X at 2–5 g/L, PHI 7 days.

Verifier:
✗ PHI unsupported

Certified:
No treatment advice delivered.
```

This is extremely compelling.

It visibly demonstrates the value of verification.

---

# 45. New flagship feature #38 — “what went wrong?” panel

For refused cases:

> **Why didn't I answer?**

Then:

```text
Cause:
No jointly supported dose + formulation + PHI relation.

What you can do:
Upload a clearer photo
or provide crop/stage
or contact extension support
```

This turns rejection into an explainable UX.

---

# 46. New flagship feature #39 — “knowledge gap” workflow

If the system fails repeatedly:

> **Knowledge gap detected**

The expert view can say:

```text
50 similar queries were unresolved.

Likely missing knowledge cluster:
Chili / Anthracnose

[Review candidate source]
[Add structured fact]
```

This connects to your E24 knowledge-maintenance experiment.

The accepted EACL ecosystem clearly values tools that support iterative human workflows, as seen in PromptLab and RAG-oriented systems. ([ACL Anthology][9])

---

# 47. New flagship feature #40 — admin knowledge editor

This would be a production-oriented addition:

### Source ingestion

### Fact extraction

### conflict checking

### expert review

### publish

### rollback

This is more ambitious, but very valuable.

It turns:

> “a static knowledge base”

into:

> **a governed knowledge service**.

For a production-minded system, that is a major upgrade.

---

# 48. The EACL system should then have three distinct audiences

## Farmer

> Ask → understand → act.

## Expert/extension officer

> inspect → verify → correct → escalate.

## Researcher/developer

> replay → compare → diagnose → benchmark.

That is extremely strong for a system demo.

It also mirrors what accepted NLP tools often do well: an accessible user interface layered over research infrastructure. RAGVUE, SmartMatch, PromptLab, and the multimodal verification assistant all follow variants of this pattern.  ([ACL Anthology][6]) ([ACL Anthology][9]) ([ACL Anthology][4])

---

# 49. The application architecture I recommend

The final EACL system should be presented as:

```text
┌──────────────────────────────────────────────────────────┐
│                     KRISHOKCHAT                          │
├──────────────────────────────────────────────────────────┤
│                    Interaction Layer                     │
│  Text • Voice • Image • Context • Case History          │
├──────────────────────────────────────────────────────────┤
│                Interpretation & Safety                   │
│  Language normalization • Risk • Clarification           │
├──────────────────────────────────────────────────────────┤
│                  Capability Router                       │
│  QA • Disease • Treatment • Weather • Escalation        │
├──────────────────────────────────────────────────────────┤
│                 Evidence & Intelligence                  │
│  Structured facts • Hybrid RAG • Vision • LLM           │
├──────────────────────────────────────────────────────────┤
│               Verification & Provenance                  │
│  Fact checks • source links • validity • audit           │
├──────────────────────────────────────────────────────────┤
│                    Delivery Layer                        │
│  Web • offline cache • local model • SMS • case handoff │
└──────────────────────────────────────────────────────────┘
```

This is much better than the current simplistic:

> safety → retrieval → generation → verification.

That old diagram describes a single execution path.

The new diagram describes **the actual integrated platform**.

---

# 50. What should be the EACL paper's core novelty?

Not:

> “we have many features.”

Not:

> “we use RAG + YOLO + LLM.”

Instead:

### **Integration novelty**

> KrishokTech operationalizes Bengali agricultural NLP, multimodal disease diagnosis, safety gating, evidence-grounded response generation, verification, and constrained delivery as one auditable advisory workflow.

This is exactly the kind of contribution recent successful system demos use. AI for Climate Finance explicitly positions its integration of established technologies into a specialized workflow as its contribution. ([ACL Anthology][3])

---

# 51. What should be explicitly secondary

The following are **capabilities**, not paper-level contributions:

* BM25;
* FAISS;
* mE5;
* YOLO classification;
* Gemini;
* Ollama;
* FastAPI;
* Next.js;
* SSE;
* Tailwind;
* caching;
* weather;
* SMS;
* analytics.

These should appear in the architecture.

They should not each be sold as novelty.

---

# 52. EACL paper outline: exact final structure

Because the EACL Demo paper has a strict **6-page maximum**, we need to write it as a compact systems paper, not like the 18-page CEA manuscript. The call explicitly says 6 pages and allows unlimited references, appendices and ethics/broader-impact material. ([EACL 2027][1])

I recommend:

---

## 1. Introduction — 0.6–0.7 page

### 1.1 Problem

Bengali farmers need:

* natural language;
* multimodal input;
* localized knowledge;
* safety;
* low-connectivity access.

### 1.2 System gap

Most systems provide one or two components.

KrishokTech integrates:

> interaction + evidence + diagnosis + safety + delivery.

### 1.3 Contributions

Exactly three.

**C1.** An integrated Bengali agricultural advisory platform.

**C2.** A multimodal and safety-aware workflow with visible provenance/verification.

**C3.** An open, reproducible, production-oriented software artifact with representative empirical validation.

End with public GitHub/demo link.

---

# 53. 2. System Overview — 0.7 page

### 2.1 Design goals

* Bengali-first;
* evidence grounded;
* safety aware;
* multimodal;
* low-connectivity tolerant;
* inspectable;
* deployable.

### 2.2 Architecture figure

One large figure.

### 2.3 Interaction flow

Brief.

---

# 54. 3. Advisory Workflow — 1.1 pages

This is the core section.

### 3.1 Query understanding and safety

Six-way safety policy.

### 3.2 Retrieval and grounded generation

Hybrid BM25+dense.

### 3.3 Evidence verification

How source/evidence status appears.

### 3.4 Multimodal diagnosis

Image → crop → disease → knowledge → advisory.

### 3.5 Resolution and fallback

Clarify / structured fact / RAG / refusal / escalation.

---

# 55. 4. User-Facing System — 1.0 page

This should contain screenshots.

### 4.1 Farmer workspace

### 4.2 Evidence/trace view

### 4.3 Vision continuation

### 4.4 Expert/research mode

### 4.5 Case handoff / offline channel

This is where the paper should resemble the best system demos.

Stakeholder Suite ends its paper with explicit interface figures and explains what each page supports. 

AI for Climate Finance likewise has a dedicated system-demonstration section describing the UI and concrete user flow. 

Follow this structure.

---

# 56. 5. Validation — 1.0–1.2 pages

Do not reproduce the CEA paper.

Instead report **system-level validation**.

### 5.1 Advisory quality

Small held-out benchmark.

### 5.2 Safety

Representative dangerous-query evaluation.

### 5.3 Multimodal

Vision workflow performance.

### 5.4 Performance

Latency/model availability/local mode.

### 5.5 Reliability

Backend tests / replay / deployment checks.

Your current repository already has 558 passing backend tests and 50/50 golden replay in the master results artifact, while the application itself reports health/readiness and production runtime controls.  ([GitHub][2])

---

# 57. 6. Availability, Reproducibility and Limitations — 0.5–0.7 page

### Availability

GitHub.

### Deployment

Live demo or installable package.

### Models

Open/local where possible.

### Licensing

Explicit.

### Limitations

* no national field deployment yet;
* no claim of agronomic omniscience;
* image artifacts are classification models;
* external services may be unavailable;
* safety claims are bounded.

The repository already documents the local model setup and checked-in model metadata. ([GitHub][2]) ([GitHub][2])

---

# 58. 7. Conclusion — 2–3 paragraphs

One sentence:

> KrishokTech demonstrates how Bengali NLP, agricultural evidence, multimodal diagnosis, safety control, and deployability can be integrated into one inspectable advisory system.

Then:

> public availability.

Then:

> future real-world validation.

Done.

---

# 59. What not to put in the EACL main paper

Move to appendix or omit:

* all E02–E26 experiment definitions;
* complete safety taxonomy;
* full 11-slot formal derivation;
* every statistical CI;
* every network simulation;
* national economics;
* long related-work review;
* detailed code architecture rules;
* all source institutions;
* every model class.

The CEA paper owns those.

---

# 60. EACL paper's key figure set

Because only 6 pages are available, I recommend **5 figures/tables total**.

## Figure 1

Integrated system architecture.

## Figure 2

Farmer workspace screenshot.

## Figure 3

Evidence + trace + verification screenshot.

## Figure 4

Multimodal case screenshot.

## Figure 5

Research/expert console or comparative safety workflow.

### Table 1

System capabilities + implementation/evidence status.

### Table 2

Representative validation results.

You may not need both tables if the layout becomes crowded.

---

# 61. The strongest screenshot

This should be:

```text
USER:
আলুর পাতায় কালো দাগ হয়েছে। কী করব?

--------------------------------------------------

KRISHOKCHAT

✓ Safety checked
✓ Crop context: Potato
✓ Relevant evidence found
✓ Advisory generated
✓ Evidence verified

RECOMMENDATION
...

WHY?
Crop:
Disease:
Active ingredient:
Dose:
PHI:
Source:
Version:

[View evidence] [Show trace] [Export]
```

This one screenshot communicates almost the entire system.

---

# 62. The strongest interactive demo scenario

This is the one I would prioritize for the live demo:

### Stage 1

User enters ambiguous Bengali text.

### Stage 2

System asks a clarification question.

### Stage 3

User uploads a photo.

### Stage 4

System identifies crop and disease.

### Stage 5

Evidence is retrieved.

### Stage 6

The interface shows a structured advisory.

### Stage 7

User clicks:

> **Why this advice?**

### Stage 8

Exact evidence appears.

### Stage 9

User clicks:

> **Export as SMS**

### Stage 10

The system shows:

> 118/160 characters; safety fields preserved.

This is a phenomenal 2.5-minute story.

---

# 63. The 2.5-minute video: exact storyboard

The video is mandatory and is part of evaluation; the call explicitly recommends a screencast with audio and says production-quality editing is not a priority. ([EACL 2027][1])

We should use the entire 150 seconds strategically.

## 0:00–0:10 — Hook

Show:

> **KrishokTech**
>
> Bengali multimodal agricultural advisory.

Voice:

> “KrishokTech helps Bengali farmers ask questions, share crop images, receive evidence-grounded guidance, and understand why the system gives—or refuses—an answer.”

No logo animation longer than 2 seconds.

---

# 64. 0:10–0:30 — Farmer text interaction

Type a realistic Bengali farmer query.

Show:

```text
Safety ✓
Evidence ✓
Advice ✓
```

Then expand the trace.

Narration:

> “The request is screened before retrieval, then grounded in agricultural evidence, and finally verified before delivery.”

Do not explain implementation details yet.

---

# 65. 0:30–0:55 — Ask safely / clarification

Give an incomplete query.

System asks:

> Which crop?

and:

> Can you upload a photo?

Narration:

> “When the system does not have enough information, it asks for clarification rather than fabricating an answer.”

This is a very strong behavioral demonstration.

---

# 66. 0:55–1:20 — Image continuation

Upload the photo.

Show:

```text
Crop → Potato
Disease → Late Blight
Confidence → ...
```

Then advisory.

Narration:

> “Text and image inputs become part of the same advisory case. The crop classifier routes the image to the appropriate disease model, and the resulting diagnosis is connected to the agricultural knowledge layer.”

The repo already supports this crop→specific-disease model path. ([GitHub][2])

---

# 67. 1:20–1:40 — Evidence inspection

Click:

> **Why this advice?**

Show source/version/fields.

Narration:

> “The system exposes the evidence and verification state behind its recommendation instead of presenting an opaque answer.”

This is the strongest research-facing part.

---

# 68. 1:40–1:55 — Unsafe/refusal scenario

Enter a restricted/prompt-injection query.

Show:

```text
BLOCKED
LLM not called
Reason:
unsafe request
```

Narration:

> “High-risk requests can terminate before retrieval or generation, and unsupported recommendations are refused rather than invented.”

Your repository already implements terminal safety categories before retrieval/generation. ([GitHub][2])

---

# 69. 1:55–2:10 — Offline/local/SMS

Switch to local mode or offline profile.

Show:

```text
Local safety ✓
Local vision ✓
Structured facts ✓
Remote generation unavailable
```

Then export to SMS.

Narration:

> “The platform also supports local components and constrained delivery paths for low-connectivity settings.”

---

# 70. 2:10–2:25 — Research/ops console

Show:

* audit;
* replay;
* evidence;
* model selector.

Narration:

> “Researchers and operators can inspect system traces, replay cases, and examine evidence and runtime status.”

This is exactly the kind of practical tool capability accepted demos emphasize. 

---

# 71. 2:25–2:30 — Close

Show:

> GitHub
> Demo URL
> “Open, reproducible Bengali agricultural advisory.”

No long conclusion.

---

# 72. Video production rules

The video should:

### Be one continuous screencast

No cinematic transitions.

### Zoom intelligently

Crop the browser window where necessary.

### Use large browser text.

### Never make the reviewer search the interface.

### Use precomputed/deterministic demo cases

Do not risk a live model outage.

### Keep one backup local deployment.

### Avoid terminal windows except perhaps a 1-second glimpse.

### Use Bengali queries, English narration.

That makes the demo accessible to EACL reviewers while showcasing Bengali NLP.

---

# 73. The three “must-show” demo moments

If the video gets compressed and we can only guarantee three moments:

### 1. Evidence-backed answer

### 2. Image → disease → advisory

### 3. Safe refusal / verification

These establish:

> NLP + multimodal + responsible AI.

---

# 74. What should be live at submission time

The call is strict: missing the live website or installable package link results in desk rejection. ([EACL 2027][1])

Therefore we need:

## Public demo

Preferably:

> `krishoktech...`

with no login for core demo.

## Backup install package

Docker or one-command local launch.

## Repository

Public.

## Demo dataset

Preloaded safe cases.

## Rate limiting

Protect live demo.

## Remote API fallback

If Gemini/OpenRouter fails, use local model or deterministic canned benchmark mode.

---

# 75. I strongly recommend a “Demo Mode”

This is especially important.

Create:

```text
/demo
```

which has:

### 5–8 curated scenarios

A reviewer can click:

* Bengali advisory;
* ambiguous query;
* image diagnosis;
* unsafe request;
* evidence inspection;
* offline mode;
* SMS export.

This prevents the reviewer from getting stuck.

The accepted AI for Climate Finance demo makes the public system accessible without installation and documents exactly how users interact with it. 

---

# 76. But Demo Mode must be honest

Don't fake live inference.

Label:

> “Demo case — reproducible frozen input”

if that is what it is.

A precomputed case is acceptable.

The current repository already distinguishes live application functionality from precomputed benchmark statistics. ([GitHub][2])

Keep that transparency.

---

# 77. Production-oriented hardening I want before EACL

Your existing production work is already a major advantage.

The repository has:

* liveness/readiness;
* strict readiness mode;
* hidden API docs;
* SSE heartbeat;
* uniform error envelopes;
* local concurrency controls;
* corpus-version cache invalidation;
* security headers;
* dependency audit;
* log retention policy. ([GitHub][2])

This is excellent.

I would add:

### structured request IDs

### rate limiting

### request timeout

### circuit breakers for remote LLM

### fallback provider

### safe default model

### health check for every dependency

### model version displayed in response

### evidence-pack version displayed in response

### audit log rotation

### PII minimization

### data deletion capability

### public demo data isolation

These make the deployment story substantially stronger.

---

# 78. New production feature: failover matrix

This would be extremely impressive.

Create a matrix:

| Failure               | Primary     | Fallback           |
| --------------------- | ----------- | ------------------ |
| Remote LLM down       | remote      | local              |
| Dense retriever down  | dense       | BM25               |
| Vision model down     | vision      | text clarification |
| Cache stale           | cache       | revalidation       |
| Evidence missing      | RAG         | abstain            |
| Unsafe classification | normal path | block              |
| Network down          | cloud       | local/cached       |

Then show it in the system.

This is a true **resilient AI application** feature.

---

# 79. New production feature: graceful degradation score

For internal evaluation, compute:

> what fraction of core user tasks remain available when individual dependencies fail?

Test:

* LLM unavailable;
* dense index unavailable;
* network unavailable;
* vision unavailable;
* stale cache;
* provider timeout.

This is a valuable system-quality metric.

---

# 80. New production feature: disaster mode / read-only mode

If the evidence store cannot be validated:

> system enters read-only safe mode.

It can provide:

* cached verified facts;
* static safety guidance.

It cannot:

* ingest new facts;
* certify new uncertain answers.

This is excellent production safety design.

---

# 81. New production feature: “knowledge release”

Build a simple release artifact:

```text
Knowledge Pack
v1.7
Source count: 2946
Validated facts: ...
Published: ...
Hash: ...
```

Reviewer can inspect.

This pairs very nicely with the repository's existing provenance/versioning work. ([GitHub][2])

---

# 82. New production feature: model registry

Create:

```text
Safety model v2.1
Crop model v1.4
Potato disease model v1.2
KrishokTech-4B v0.9
Knowledge v1.7
```

Every answer references those versions.

This is excellent for reproducibility and operational credibility.

---

# 83. New production feature: case replay

Every demo scenario can be replayed from an immutable case bundle:

```text
case/
  request.json
  image.jpg
  knowledge_version
  model_versions
  expected_trace.json
```

Then:

> **Replay**

should reproduce the behavior.

This is one of the easiest ways to turn the system into something that feels research-grade.

---

# 84. New production feature: observability

Instrument:

* route;
* model;
* latency;
* retrieval count;
* verifier outcome;
* refusal;
* fallback;
* error.

Do not expose sensitive logs publicly.

But aggregate statistics can show:

```text
Requests
Safety blocks
LLM calls
Verified answers
Abstentions
Average latency
```

This is useful in demo and funding contexts.

---

# 85. The EACL evaluation plan

Here I would deliberately **not** duplicate the CEA paper.

Use four evidence categories.

## E1. System availability

* public demo;
* GitHub;
* installable package.

## E2. Functional coverage

Test:

* QA;
* safety;
* vision;
* offline;
* export.

## E3. Quality snapshot

A held-out representative benchmark.

## E4. Operational reliability

* integration tests;
* replay;
* dependency failover;
* latency.

That is enough for a system demo.

The official call says a comprehensive evaluation isn't necessary, but **some evidence is mandatory**. ([EACL 2027][1])

---

# 86. EACL benchmark design

Use around:

### 300–500 representative real-style Bengali queries

covering:

* general farming;
* disease;
* treatment;
* ambiguous;
* unsafe;
* Banglish;
* regional dialect;
* out-of-domain.

No need for 5,000 here.

That huge evidence package belongs in CEA.

---

# 87. EACL expert evaluation

Have:

### 3 agronomists

review perhaps 100 representative cases.

Rate:

* helpfulness;
* correctness;
* safety;
* evidence relevance;
* clarity.

This is perfect for a demo paper because the call explicitly accepts expert evaluations and case studies as evidence. ([EACL 2027][1])

You can reuse the infrastructure from the CEA study, but the test sample and framing should remain distinct.

---

# 88. EACL system performance table

Report:

| Mode            | p50 | p95 | LLM calls | Status   |
| --------------- | --: | --: | --------: | -------- |
| Structured fact |     |     |         0 | Verified |
| RAG             |     |     |         1 | Grounded |
| Image advisory  |     |     |       0/1 | Verified |
| Local model     |     |     |         1 | Local    |
| Offline cache   |     |     |         0 | Cached   |

This is exactly the sort of deployment-oriented evidence that makes a demo feel real.

---

# 89. EACL system availability table

Maybe:

| Component     | Public     | Reproducible | Local |
| ------------- | ---------- | ------------ | ----- |
| Backend       | ✓          | ✓            | ✓     |
| Frontend      | ✓          | ✓            | ✓     |
| RAG assets    | ✓/licensed | ✓            | ✓     |
| Vision assets | ✓/licensed | ✓            | ✓     |
| Local LLM     | ✓          | ✓            | ✓     |
| Demo mode     | ✓          | ✓            | ✓     |

This helps reviewers immediately understand the artifact.

---

# 90. EACL literature positioning

I would explicitly compare against these archetypes:

### Farmer.Chat

Multilingual agricultural GenAI at scale. The system is already a mature agricultural advisory benchmark for “what a deployed assistant looks like,” so don't compete on scale. ([microsoft.com](https://www.microsoft.com/en-us/research/publication/farmer-chat-scaling-ai-powered-agricultural-services-for-smallholder-farmers/?utm_source=chatgpt.com))

### KrishokBondhu

Bengali voice/RAG agricultural advisory. Again, don't claim Bengali RAG is yours.

### AI for Climate Finance

Domain-specific integration of established components + public deployment + expert validation. ([ACL Anthology][3])

### Multimodal Verification Assistant

Unified interface over multiple backend analysis tools. ([ACL Anthology][4])

### RAGVUE

Inspectable RAG workflows. ([ACL Anthology][5])

### SmartMatch

Interactive retrieval inspection and latency-aware UI. ([ACL Anthology][6])

### FlexRAG

Open modular RAG infrastructure. ([ACL Anthology][7])

Your differentiator:

> **farmer-facing, Bengali, agricultural, multimodal, safety-aware, evidence-inspectable, low-connectivity-oriented integration.**

---

# 91. One thing I would add from the recent ACL demo ecosystem: evaluator-facing affordances

A lot of strong demos are not just “use the tool.”

They let the reviewer **inspect**.

Therefore add:

### `Inspect evidence`

### `Compare retrieval`

### `Replay case`

### `See route`

### `See verification`

### `See latency`

These should be one-click controls.

That makes the demo much more compelling to a technical NLP audience.

---

# 92. One feature I would deliberately NOT add: autonomous multi-agent farming

Don't add:

> planner agent → critic agent → farmer agent → weather agent → market agent.

That would make the application look trendy but not necessarily better.

The strongest system identity is:

> **controlled integration and observable behavior.**

Not “agentic for its own sake.”

The AI for Climate Finance paper demonstrates that agentic reasoning can be useful, but its value is tied to a clearly defined domain workflow and structured output. 

---

# 93. Another feature I would avoid: generic chatbot memory

Don't build long-term conversational memory unless it provides agricultural value.

Better:

> **case memory**

Store:

* crop;
* stage;
* disease;
* previous advice;
* unresolved questions;
* evidence version.

This is more useful and safer.

---

# 94. Add “conversation state as a structured case”

Instead of:

> long chat transcript

maintain:

```text
CASE

Crop: Potato
Stage: Vegetative
Problem: Late blight?
Symptoms: dark lesions
Image: attached
Location: Rajshahi
Weather: rainy
Evidence: 3 sources
Status: clarification required
```

This is a strong product feature.

---

# 95. Add “farmer context”

The system can ask:

* crop;
* growth stage;
* district;
* cultivation type;
* harvest timing.

But ask only when needed.

Use:

> **progressive clarification**

rather than a long questionnaire.

This is better UX and also demonstrates intelligent NLP interaction.

---

# 96. Add structured Bengali answer templates

For critical responses:

```text
কার জন্য
কী সমস্যা
কি করবেন
কতটা ব্যবহার করবেন
কতদিন পর আবার
ফসল তোলার আগে কতদিন অপেক্ষা
উৎস
```

The exact agricultural content must come from the verified fact layer.

This gives a beautiful farmer-facing representation.

---

# 97. Voice response is optional, but could be a major differentiator

I would rank it:

### Priority A

Text + image + evidence.

### Priority B

voice input.

### Priority C

voice response.

The first two already give you a strong system demo.

---

# 98. Exact EACL acceptance strategy

To maximize acceptance, I want the reviewer to be able to answer:

### “What is it?”

Immediately.

### “Why is it useful?”

Immediately.

### “What is new?”

Integration + inspectability + safety-aware workflow.

### “Does it work?”

Yes, with representative validation.

### “Can I use it?”

Yes.

### “Can I understand it?”

Yes, through trace/evidence UI.

### “Is it more than a toy?”

Yes, via deployment-oriented engineering and reproducible tests.

### “Can I demo it?”

Yes.

That is the target.

---

# 99. Final EACL contribution claims

I would use exactly these three.

### C1 — Integrated system

> KrishokTech integrates Bengali conversational retrieval, multimodal crop-disease advisory, safety-aware routing, evidence verification, and constrained delivery into a unified agricultural assistance workflow.

### C2 — Interactive transparency

> The system exposes route, evidence, confidence, verification status, and case provenance through a user-facing trace and expert inspection interface.

### C3 — Open/deployable artifact

> The platform is publicly released with modular backend interfaces, local/remote model support, reproducible assets, deployment controls, and representative validation.

This is enough.

---

# 100. What counts as “system novelty” versus “engineering detail”

This distinction should govern the entire paper.

### System-level novelty

* integrated advisory workflow;
* multimodal continuation;
* safety-aware routing;
* evidence inspection;
* case handoff;
* graceful degradation;
* structured case state.

### Valuable engineering

* provider abstraction;
* production health;
* caching;
* concurrency;
* security headers;
* logging;
* deployment scripts.

### implementation detail

* Tailwind;
* React version;
* Python package version;
* exact API path.

Only the first category needs persuasive prose.

---

# 101. The final application should have four modes

## Mode 1 — Ask

Bengali text/voice.

## Mode 2 — Diagnose

Image.

## Mode 3 — Inspect

Evidence/trace.

## Mode 4 — Operate

Analytics/cases/deployment.

This is a much better product architecture for the demo than a collection of frontend routes.

---

# 102. Final EACL demo workflow

```text
HOME
  ↓
Ask / Photo
  ↓
Unified Case
  ↓
Safety + Context
  ↓
Capability Router
  ↓
Evidence / Vision / Weather
  ↓
Resolution
  ↓
Verification
  ↓
Advisory
  ↓
Why?
  ↓
Evidence / Provenance
  ↓
Export / Follow-up / Escalate
```

Every system component contributes to one user journey.

---

# 103. How the EACL paper and CEA paper divide the system

This is critical.

## EACL paper discusses

**the complete platform**

but focuses on:

* integration;
* user interaction;
* multimodal behavior;
* inspectability;
* availability;
* deployment readiness.

## CEA paper discusses

**the reliability architecture**

and evaluates:

* authority;
* safety;
* verification;
* risk–coverage;
* failure propagation;
* temporal validity;
* edge/network behavior.

The same software can support both.

---

# 104. What I would build first

### Sprint 1 — Core UX

* unified advisory case;
* evidence view;
* status badge;
* clarify workflow;
* image continuation.

### Sprint 2 — Research/ops

* replay;
* A/B comparison;
* evidence corruption sandbox;
* audit explorer;
* expert mode.

### Sprint 3 — Deployment

* failover;
* local/offline profiles;
* readiness;
* model registry;
* knowledge version display;
* demo mode.

### Sprint 4 — Optional differentiators

* voice;
* case handoff;
* signed knowledge release;
* temporal source timeline;
* SMS export.

---

# 105. My priority ranking of new features

## Tier S — must have

1. unified case/session;
2. “Why this advice?” evidence panel;
3. visible verification/status;
4. image→chat continuation;
5. safe clarification flow;
6. replayable demo cases;
7. demo mode;
8. public reproducible deployment;
9. expert/research inspection view.

## Tier A — high impact

10. multimodal contradiction handling;
11. evidence provenance graph;
12. A/B baseline comparison;
13. graceful degradation/failover;
14. offline/local mode;
15. structured safe action cards;
16. knowledge version/freshness;
17. case handoff.

## Tier B — strong additions

18. SMS export;
19. weather-context integration;
20. knowledge-gap workflow;
21. admin fact governance;
22. voice input;
23. case memory;
24. deployment health dashboard.

## Tier C — only after all of the above

25. voice output;
26. broader crops;
27. additional external data sources;
28. extra AI agents.

---

# 106. The feature I think could make the demo memorable

I want the reviewer to be able to intentionally break the system.

### “Try to fool the advisor”

Button.

It opens:

> Evidence conflict

Then:

> Change dosage

or:

> Swap crop

or:

> Add malicious instruction.

The UI runs:

### baseline RAG

and

### KrishokTech.

Then:

```text
Baseline:
✗ produces recommendation

KrishokTech:
✓ detects mismatch
✓ refuses certification
✓ explains why
```

This is much more memorable than a standard chat response.

It also leverages the real CEA research without turning EACL into that paper.

---

# 107. The second memorable interaction

### “Ask in farmer language”

Preloaded examples:

* colloquial Bengali;
* regional dialect;
* Banglish;
* typo-heavy query.

Then show:

> interpreted intent.

This directly demonstrates the relevance of your previous research line.

---

# 108. The third memorable interaction

### “Upload a crop photo”

Then:

> crop → disease → evidence → action.

This demonstrates multimodality.

---

# 109. The fourth memorable interaction

### “Turn this into an SMS”

Show:

> 118 / 160 characters

and:

> critical fields preserved.

That demonstrates constrained delivery.

---

# 110. Put all four into the 2.5 minutes

The video isn't merely a recording of the paper.

It should be a **miniature guided tour of the entire research/application philosophy**:

> understand → diagnose → verify → deliver.

---

# 111. What the paper itself should say about production

Do **not** write:

> “production-ready.”

Unless you actually deploy it.

Write:

> **production-oriented architecture**

or:

> **deployment-oriented system with explicit operational safeguards**

The repository supports that description very well: single-box deployment scripts, liveness/readiness, bounded concurrency, cache versioning, error handling, security headers, audit/log policies, and a replaceable LLM backend. ([GitHub][2])

When you actually have a real hosted deployment with monitoring and user traffic, then we can upgrade the wording.

---

# 112. The README should be changed before submission

The current README first calls KrishokTech:

> “a research capstone demo prototype, not a production service.” ([GitHub][2])

For EACL, that wording is unnecessarily weak and somewhat inconsistent with the actual repository.

I would change it to something like:

> **An open, production-oriented research platform for safety-aware Bengali agricultural advisory.**

Then:

> “The repository contains a deployable integrated system, research artifacts, reproducible evaluation infrastructure, and experimental/demo components. Field-scale deployment has not yet been conducted.”

That is accurate and much stronger.

---

# 113. The repository structure actually supports the EACL story

The current repo has explicit separation of:

* backend;
* frontend;
* datasets;
* models;
* deployment;
* demo assets;
* production/future plan;
* research artifacts;
* scripts. ([GitHub][2])

This is exactly what an open system demo should look like.

Use a README structure like:

```text
What KrishokTech is
Why it exists
5-minute quickstart
Live demo
Demo scenarios
Architecture
Research evidence
Deployment
Models/data
Reproducibility
License
```

---

# 114. Make the public demo reviewer-proof

A reviewer should be able to:

1. open URL;
2. click “Demo Mode”;
3. choose scenario;
4. get result;
5. inspect evidence;
6. replay.

No API key.

No sign-in.

No setup.

No external dataset download.

No waiting 5 minutes for a model.

If live generation needs a provider, use cached deterministic examples for the demo surface, with a clearly labeled live mode.

---

# 115. Licensing needs attention

The EACL call explicitly asks reviewers to consider availability and licensing. ([EACL 2027][1])

You need to ensure:

* code license;
* model license;
* dataset license;
* source-document redistribution rights;
* external model/API terms.

Especially because your corpus includes institutional source documents.

If full source redistribution isn't legally possible, distribute:

* metadata;
* IDs;
* extracted derived facts where permitted;
* build scripts;
* retrieval indices only where legally allowed.

And explain the limitation.

---

# 116. Ethics section

Because this is agricultural advice, the ethics/broader-impact component should be explicit even though the EACL call says an ethics section isn't always mandatory. It specifically warns that sensitive tasks without discussion of legitimate ethical issues may be rejected. ([EACL 2027][1])

Cover:

### Safety

Incorrect chemical advice.

### Language fairness

Regional/dialect variation.

### Access

Poor connectivity.

### Transparency

Evidence/provenance.

### Human escalation

When automation is insufficient.

### Data privacy

Farmer photos and logs.

### Model limitations

No universal agronomic guarantee.

That is enough.

---

# 117. Very important: don't hide the limitations

EACL reviewers are likely to respect this.

Say:

* vision models are classification, not lesion localization;
* not a field trial yet;
* weather availability depends on external service;
* expert escalation isn't yet a measured farmer outcome;
* the system is domain-bounded;
* some components are experimental.

The repository already honestly distinguishes the locked soil analyzer from active functionality and states that image models are classification only. ([GitHub][2]) ([GitHub][2])

Keep that honesty.

---

# 118. One possible high-impact addition: “agronomist review mode”

When expert mode is enabled:

```text
SYSTEM ANSWER
...

Review

[Approve]
[Reject]
[Edit fact]
[Flag source]
[Request clarification]
```

The correction becomes part of an audit trail.

Even if the paper does not evaluate active learning, the system demonstrates a realistic human oversight loop.

This is very compatible with current applied NLP system design.

---

# 119. One possible high-impact addition: feedback is structured

Don't just have a 👍.

Use:

> Was this useful?

and if no:

> Problem type:
>
> * wrong diagnosis
> * wrong treatment
> * too vague
> * missing context
> * unsafe
> * language issue

That gives future deployment data.

Do not silently train on it.

---

# 120. One possible high-impact addition: “report unsafe advice”

This is a production safety control.

A user/expert can flag:

> unsafe

and the system records the case.

Again, not necessarily a paper contribution, but very useful operationally.

---

# 121. One possible high-impact addition: evidence disagreement

If two authorities disagree, expose:

```text
⚠ Sources disagree

Source A — 2025
Source B — 2026

System status:
Not certified

Reason:
conflicting authoritative recommendations
```

This is a very mature behavior.

The CEA paper can investigate it scientifically.

The EACL demo can simply demonstrate it.

---

# 122. One possible high-impact addition: source freshness chip

Every source card:

> BARI — 2025 — Verified

or:

> DAE — 2026 — Current

Again, very useful.

---

# 123. One possible high-impact addition: “no source, no chemical”

Make this an explicit UI principle:

> **No verified source → no chemical recommendation.**

This is an extremely memorable system rule.

It captures the whole CEA idea in one product phrase.

---

# 124. EACL paper abstract structure

The abstract should contain:

### Problem

Bengali agricultural advisory requires combining language, evidence, multimodality and safety.

### System

KrishokTech.

### Unique integration

Safety-aware routing + hybrid RAG + image-to-advisory + verification + provenance.

### Evidence

Representative benchmark/expert/performance validation.

### Availability

Open-source / live demo.

No giant metric dump.

---

# 125. EACL related work structure

Only three paragraphs.

### Agricultural conversational systems

Farmer.Chat, KrishokBondhu, etc.

### System/interactive RAG demonstrations

AI for Climate Finance, RAGVUE, SmartMatch, FlexRAG.

### Gap

Existing systems demonstrate pieces or different application domains; KrishokTech integrates multilingual agricultural advisory, multimodality, safety and inspectability in one Bengali-facing platform.

That's enough.

---

# 126. How I would phrase novelty carefully

Something like:

> “The individual components—retrieval, vision classification, LLM generation, and safety filtering—are established. Our contribution is their integration into an auditable Bengali agricultural advisory workflow in which heterogeneous inputs share a common advisory case and users can inspect routing, evidence, and verification outcomes.”

That is honest and strong.

---

# 127. Why this is better than claiming an algorithmic novelty

Because EACL Demo explicitly accepts systems whose contribution lies in applications and integration. ([EACL 2027][1])

And recent accepted demos validate that pattern: AI for Climate Finance explicitly says its components are individually established and contribution lies in their integration into the domain workflow. ([ACL Anthology][3])

So we are not weakening the paper by doing this.

We are matching the venue.

---

# 128. The final EACL paper “evidence triangle”

The paper should establish three things:

### Scientific quality

Some measured validation.

### System quality

Architecture, integration, usability.

### Artifact quality

Open demo, code, reproducibility.

The call is explicitly structured around these dimensions. ([EACL 2027][1])

---

# 129. What would make this EACL demo unusually strong

If the final system can do this:

> **A Bengali farmer submits a vague text query → system asks an intelligent clarification → farmer adds an image → crop/disease routing occurs → evidence is retrieved → advisory is produced → user inspects source/provenance → asks a follow-up → system preserves the case context → unsafe modification is blocked → result can be exported for SMS/extension handoff.**

That is a **complete language technology interaction**.

It is much stronger than:

> “Here is our chatbot.”

---

# 130. Final EACL architecture after proposed additions

```text
                         FARMER
                            │
             ┌──────────────┼──────────────┐
             │              │              │
            Text          Voice           Image
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                 LANGUAGE / CONTEXT LAYER
                            │
                ┌───────────┴──────────┐
                │                      │
             clarify                safety
                │                      │
                └───────────┬──────────┘
                            ▼
                    ADVISORY CASE
                            │
                            ▼
                    CAPABILITY ROUTER
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
       ▼                    ▼                    ▼
  Structured facts       Hybrid RAG            Vision
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
                     EVIDENCE LAYER
                            │
                  ┌─────────┴─────────┐
                  │                   │
              deterministic       generative
                  │                   │
                  └─────────┬─────────┘
                            ▼
                       VERIFIER
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
              CERTIFY               ABSTAIN
                 │                     │
                 ▼                     ▼
             ADVISORY             CLARIFY/ESCALATE
                 │
       ┌─────────┼─────────┬───────────────┐
       ▼         ▼         ▼               ▼
    Farmer     Evidence   Expert         SMS/
     view       view       view          Offline
```

That's the platform I would submit.

---

# 131. Final feature-to-paper mapping

| Feature                 | EACL demo       | CEA                            |
| ----------------------- | --------------- | ------------------------------ |
| Bengali chat            | **central**     | evaluation input               |
| Hybrid RAG              | central         | baseline/component             |
| Safety gate             | central         | **scientific core**            |
| Structured facts        | visible         | **scientific core**            |
| Relational verifier     | visible         | **scientific core**            |
| Vision                  | **central**     | uncertainty experiment         |
| Evidence UI             | **central**     | provenance                     |
| Expert mode             | central         | HITL experiment                |
| Replay                  | central         | reproducibility                |
| Audit                   | central         | supporting evidence            |
| Local LLM               | central         | deployment                     |
| Offline cache           | central         | deployment                     |
| SMS                     | demo feature    | constrained-channel evaluation |
| Weather                 | optional        | minor/contextual               |
| Soil                    | optional future | not core                       |
| Cost dashboard          | optional        | supporting                     |
| Knowledge editor        | valuable        | maintenance                    |
| Knowledge version       | central         | temporal validity              |
| Multimodal conflict     | **strong demo** | **strong experiment**          |
| A/B baseline            | **strong demo** | methodology                    |
| Evidence attack sandbox | **killer demo** | **core safety research**       |

---

# 132. My final recommendation on what to build

Do **not** attempt every feature simultaneously.

The high-value build target is:

### Core EACL product

**Unified case + safety + multimodal continuation + evidence inspection + expert view + replay/demo mode + production hardening.**

### CEA research engine behind it

**authority + verification + calibration + adversarial/temporal/multimodal testing.**

That creates two papers from one platform without overlap.

---

# 133. The final 2.5-minute story in one sentence

The video should communicate:

> **“KrishokTech understands the farmer, gathers the right evidence, uses images when needed, refuses when it cannot justify an answer, shows why it answered, and remains usable under constrained deployment.”**

That's the EACL story.

---

# 134. Final judgment

After reviewing the actual current codebase, the production-oriented repository, the current results, and successful EACL/ACL demonstration papers, I would **strongly pursue EACL Demo**, not Industry Track, for this artifact.

The official Demo CFP is almost tailor-made for the system you have: application system using NLP, potentially multimodal, openly available, demonstrable through a website/package, and evaluable with benchmarks, expert studies, simulations, usage evidence and case studies. ([EACL 2027][1])

And your repository already gives you a real foundation: it has 2,120 knowledge nodes across 2,946 source documents, multiple agricultural institutions, hybrid retrieval, safety routing, streamed trace events, image-based crop/disease workflows, model-provider abstraction, reproducible tests, and production-oriented runtime controls. ([GitHub][2]) ([GitHub][2]) ([GitHub][2])

The **best EACL version of KrishokTech is therefore not “more AI.”**

It is:

> **more coherent interaction, more inspectability, more multimodal continuity, more graceful failure, more reproducibility, and a genuinely usable public demo.**

That is what I would build.

And because we now have the CEA paper scoped separately, we can safely make the EACL system **much richer** without turning its six-page paper into the same scientific manuscript: the EACL paper can demonstrate the complete platform, while the CEA paper proves the reliability principles underneath it.

One final operational constraint: EACL 2027's Demo deadline is **22 September 2026**, the submission is capped at **6 pages**, and the paper, video, and live-demo/package links are all mandatory. ([EACL 2027][1])

[1]: https://2027.eacl.org/calls/demos/?utm_source=chatgpt.com "Call for System Demonstrations -"
[2]: https://github.com/RaiyaanReza/KrishokTech-Agricultural-Advisory-System "GitHub - RaiyaanReza/KrishokTech-Agricultural-Advisory-System · GitHub"
[3]: https://aclanthology.org/2026.eacl-demo.34/ "AI for Climate Finance: Agentic Retrieval and Multi-Step Reasoning for Early Warning System Investments - ACL Anthology"
[4]: https://aclanthology.org/2026.eacl-demo.12/ "A Browser-based Open Source Assistant for Multimodal Content Verification - ACL Anthology"
[5]: https://aclanthology.org/2026.eacl-demo.35/ "RAGVUE: A Diagnostic View for Explainable and Automated Evaluation of Retrieval-Augmented Generation - ACL Anthology"
[6]: https://aclanthology.org/2026.eacl-demo.36/?utm_source=chatgpt.com "SmartMatch: Real-Time Semantic Retrieval for Translation Memory Systems - ACL Anthology"
[7]: https://aclanthology.org/2025.acl-demo.60/ "FlexRAG: A Flexible and Comprehensive Framework for Retrieval-Augmented Generation - ACL Anthology"
[8]: https://aclanthology.org/volumes/2026.eacl-demo/?utm_source=chatgpt.com "Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 3: System Demonstrations) - ACL Anthology"
[9]: https://aclanthology.org/2026.eacl-demo.18/?utm_source=chatgpt.com "PromptLab: A Collaborative Platform for Prompt Engineering and Dataset Curation - ACL Anthology"
