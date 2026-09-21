I treated this as a **content-selection pass before rewriting**: the question is not “how do we make every section better?” but “what deserves to exist in a six-page EACL Systems Demonstration paper at all?”

I also cross-checked the current EACL 2027 CFP and a recent sample of accepted demos, including **EACL 2026 Verification Assistant/RAGVUE, ACL 2026 FactSearch/OpenGlass, ACL 2025 My Climate CoPilot/SpatialWebAgent/FlexRAG, and ACL 2024 LocalRQA**. The CFP explicitly emphasizes system design, demonstration clarity, evidence, availability/licensing, and visual aids, while saying comprehensive experiments are not required. ([EACL 2027][1])

One note: I did not find a separate, retrievable supervisor/pre-submission memo among the supplied files, so I have not treated any unseen supervisor recommendation as evidence.

---

# 1. DEFINE THE CORE STORY

## One sentence

> **KrishokTech is a deployable Bengali agricultural advisory system that makes uncertainty and safety explicit by controlling what the pipeline may retrieve, generate, verify, and render, with those controls exposed through a continuous farmer interaction.**

That is the story I would submit.

## Three sentences

> Farmers may ask underspecified treatment questions or provide text and images that disagree, while generated dosage claims can exceed the supporting evidence. KrishokTech addresses these failure modes with three enforceable control points: it halts missing-crop treatment requests before retrieval, fences evidence to the identified crop and confirms text–image conflicts, and verifies dosage-bearing claims before rendering them. The system is demonstrated through a continuous ASK→CONFIRM→REFER→DROP interaction and supported by targeted validation on authentic farmer queries, multimodal stress cases, adversarial inputs, and dosage mutations.

## One paragraph

> Bengali agricultural advisory requires more than conversational access: farmers may omit the crop in a treatment request, use colloquial or Banglish forms, attach an image that conflicts with their text, or receive a generated dosage claim that is not supported by the retrieved evidence. KrishokTech treats these uncertainties as explicit control states rather than relying on the language model to resolve them implicitly. Its pipeline halts underspecified treatment requests before retrieval, constrains retrieval to an identified crop and requires confirmation when modalities disagree, and checks dosage-bearing claims against retrieved evidence and permitted dose ranges before display. The live demonstration follows one farmer interaction through clarification, crop scoping, multimodal conflict, safety referral, and claim filtering, while targeted evaluations validate the individual controls and a bounded human audit checks delivered outputs.   

---

# 2. WHAT THE CURRENT MANUSCRIPT IS ACTUALLY TELLING

The current paper starts close to the intended story, but then branches into several secondary stories.

### Story A — the one you want

**Explicit control points for uncertainty and safety in Bengali agricultural advisory.**

This is already clearly present in the third and fourth Introduction paragraphs and in the System Design section.  

### Story B — currently too prominent

**Bengali agricultural retrieval is difficult.**

The exact dense-retrieval R@10 0.970→0.093 result is inherited from your earlier retrieval work. 

This is useful motivation, but it is not the core story of this system.

### Story C — currently too prominent

**KrishokTech is a broad multi-channel deployment platform.**

Web + SMS + offline + read-aloud + local inference + ONNX + browser/WASM + installation footprint + network resilience become a second system story. 

These are useful deployment properties, but they should support the primary story rather than compete with it.

### Story D — currently too prominent

**KrishokTech is an extensive safety benchmark.**

The Appendix contains separate routing probes, PRISM conformance, token metering, cloud and local attack suites, mutation categories, SMS experiments, packet-loss simulation, cost modeling, trace ordering, etc.  

That makes the artifact look increasingly like an empirical safety paper with a demonstration attached.

### Story E — the risky one

**KrishokTech is the first system combining these mechanisms.**

That is stronger than the actual evidence supports. 

---

# 3. WHERE THE MANUSCRIPT STARTS TELLING A DIFFERENT STORY

| Location              | Current story                                          | Desired action                                          |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------- |
| Abstract              | Core controls + delivery + several headline benchmarks | Keep controls/demo/evidence; compress delivery          |
| Intro ¶1              | Digital agricultural access                            | Keep, shorter                                           |
| Intro ¶2              | Bengali retrieval failure + VLM conflict + LLM safety  | Keep motivation, remove exact dense R@10 centerpiece    |
| Intro ¶3–4            | Explicit control-state architecture                    | **This is the core; promote**                           |
| Intro final paragraph | Links + availability                                   | Keep, but separate from narrative                       |
| Related Work ¶1       | Agricultural advisory ecosystem                        | Keep, but shorter                                       |
| Related Work ¶2       | Safety/verification/abstention ecosystem               | Keep, but make KrishokTech's integration clearer        |
| Related Work ¶3       | Low-resource/Bengali + “first system”                  | Narrow and remove “first”                               |
| Table 1               | Comparative novelty argument                           | Remove from main paper                                  |
| System Design         | Control architecture                                   | **Central**                                             |
| Delivery details      | Platform/channel breadth                               | Mention, don't center                                   |
| Demonstration         | Continuous farmer workflow                             | **Central**                                             |
| §5.1 C1               | Gate validation                                        | **Central**                                             |
| §5.2 C2               | Retrieval + contradiction                              | **Central, with metric correction**                     |
| §5.3 C3               | Huge collection of safety/deployment results           | Keep core safety/verifier evidence; compress the rest   |
| §5.4                  | Extensive qualification                                | Keep, but much shorter                                  |
| §6                    | Limitations + availability + conclusion                | Keep; tighten                                           |
| Appendix              | Full evidence dossier                                  | Keep useful audit details; remove low-value diagnostics |

---

# 4. CONTENT TRIAGE

## A. Abstract

| Component                                          | Decision                                                  |
| -------------------------------------------------- | --------------------------------------------------------- |
| Problem: unsafe/underspecified agricultural advice | **KEEP AS CENTRAL**                                       |
| Three controls                                     | **PROMOTE MORE STRONGLY**                                 |
| ASK/CONFIRM/REFER/DROP interaction                 | **KEEP AS CENTRAL**                                       |
| Web/SMS/offline delivery                           | **MENTION ONLY**                                          |
| 200-query C1 result                                | **KEEP AS CENTRAL**                                       |
| C2 result                                          | **KEEP AS CENTRAL**, but rename metric                    |
| Cloud ASR result                                   | **KEEP**, but do not let it represent the deployed system |
| “These results show…” final sentence               | **KEEP BUT SHORTEN**                                      |

The abstract should answer only:

**What problem? What system idea? What is distinctive? What does the attendee see? What evidence validates it?**

---

## B. Introduction

### Paragraph 1 — agricultural-access motivation

**KEEP BUT SHORTEN.**

Current function: establishes why digital agricultural advisory matters. 

Desired role: approximately 3–4 sentences.

Do not spend a substantial fraction of page 1 proving the general importance of agricultural extension.

---

### Paragraph 2 — failure modes

**KEEP BUT SHORTEN.**

Keep:

* missing crop;
* text/image conflict;
* unsupported dosage;
* colloquial/Banglish challenge.

De-emphasize:

* exact 0.970→0.093 prior retrieval result.

The prior retrieval work should establish *why uncertainty matters*, not become the opening claim of the new system paper. 

---

### Paragraph 3 — system idea

**KEEP AS CENTRAL / PROMOTE.**

This is arguably the most important paragraph in the Introduction:

> “making uncertainty and safety decisions explicit rather than leaving them to the language model.”



This should become the conceptual anchor.

---

### Paragraph 4 — three controls

**KEEP AS CENTRAL / PROMOTE.**

This is the paper's contribution map:

C1, C2, C3. 

Keep it.

---

### Paragraph 5 — demo links

**MENTION ONLY.**

Keep the actual URLs because the CFP requires them, but the links need not occupy narrative attention. The current CFP explicitly requires both the screencast and live demo/package link in the PDF and OpenReview. ([EACL 2027][1])

---

# 5. RELATED WORK TRIAGE

## Agricultural systems paragraph

Current references:

* Farmer.Chat
* KrishokBondhu
* Krishi Sathi
* Bengali RAG system

**KEEP BUT SHORTEN.**

Purpose:

> establish that localized agricultural conversation, retrieval, multimodality, and clarification already exist.

Then immediately identify your distinction.

Do not enumerate the whole agricultural ecosystem.

---

## Safety/verification paragraph

Current references:

* My Climate CoPilot
* AgroLLM
* VLM conflict
* clinical dialogue
* abstention
* clarification

**KEEP BUT SHORTEN.**

This is the more important related-work paragraph because it establishes the intellectual neighborhood around your control architecture.

My Climate CoPilot is especially relevant because it is itself an accepted agricultural system demo emphasizing evidence, transparency, privacy, and expert validation. ([ACL Anthology][2])

---

## Bengali/low-resource paragraph

**KEEP BUT SHORTEN.**

The point should be:

> colloquial Bengali/Banglish creates a deployment-specific safety problem.

Do not spend several sentences proving that Bengali NLP is low-resource in general.

---

## “First system”

**REMOVE.**

The current:

> “To our knowledge, KrishokTech is the first system…”

should not survive. 

Replace the idea with:

**“KrishokTech combines these controls into one enforceable, farmer-visible pipeline.”**

That is enough.

---

## Table 1

**REMOVE FROM MAIN PAPER.**

The table's fundamental weakness is epistemic:

> “Not described” does not mean the system lacks the mechanism.



That caveat effectively neutralizes the table as evidence.

Recent demos do use comparison tables, but they generally compare clearly documented toolkit/system capabilities rather than relying on absence from another paper as evidence; LocalRQA is a good example. ([ACL Anthology][3])

Use prose positioning instead.

---

# 6. SYSTEM DESIGN TRIAGE

## T0 Safety Check

**KEEP AS CENTRAL.**

Necessary because it establishes the first control boundary.

The exact 0.32 ms timing is:

**KEEP BUT SHORTEN / MENTION ONLY.**

The system behavior matters more than the sub-millisecond number.

---

## T1 Information Gate

**KEEP AS CENTRAL.**

The key system idea is:

> do not retrieve on a missing safety-critical crop.

The detailed five-slot extractor belongs in the appendix.

---

## DialectSelector

**MENTION ONLY IN MAIN.**

The current paper says it “narrows the colloquial-to-formal retrieval gap.” 

That effect is not directly established in this system evaluation.

So:

* capability = mention;
* causal improvement claim = remove;
* six presets and tokenizer behavior = appendix.

---

## T2 crop fencing

**KEEP AS CENTRAL.**

This is one of the three central controls.

Keep:

* crop identification;
* crop-conditioned evidence;
* unreachable off-target passages;
* explicit text/image disagreement;
* confirmation before chemical advice.

The exact confidence thresholds belong in the appendix.

---

## Tri-state visual router

**KEEP BUT SHORTEN.**

The behavior is important:

**confident → route; ambiguous → ask; OOD → stop/re-capture.**

The exact `p1 ≥ 0.90`, margin 0.20, and OOD 0.40 thresholds are appendix-level implementation detail. 

---

## T3/T4 generation + verification

**KEEP AS CENTRAL.**

This is the other major distinctive component.

The key conceptual phrase is:

> the generated answer is an **unverified draft** until the verifier accepts it. 

Keep.

---

## Provenance badges

**KEEP BUT SHORTEN.**

The user-visible provenance and Why panel are important because they turn backend verification into demonstrable interface behavior.

But the detailed five-badge taxonomy belongs in the appendix.

---

## Delivery channels

Current:

* web;
* SMS;
* offline card;
* Bengali read-aloud.

**MENTION ONLY.**

These make the system more usable and help demonstrate accessibility, but they should not become four mini-contributions.

---

# 7. DEMONSTRATION TRIAGE

## Section 4 opening

**KEEP AS CENTRAL.**

The audience definition is appropriate:

> researchers/practitioners working on multilingual, multimodal, safety-critical conversational systems. 

The current demo is also unusually coherent relative to many system papers.

---

## S1 Missing crop

**KEEP AS CENTRAL.**

Essential because it demonstrates the pre-retrieval decision.

---

## S2 Photograph scopes evidence

**KEEP AS CENTRAL.**

Essential because it supplies the visual condition required for S3.

---

## S3 Photograph/text mismatch

**KEEP AS CENTRAL / PROMOTE.**

This is probably the most visually distinctive step.

Recent system demos often use the first few pages to show the actual system workflow rather than bury it behind extensive setup. My Climate CoPilot puts its main system workflow figure on page 1; the Verification Assistant does similarly with architecture and workflow material immediately after the introduction. 

---

## S4 safety referral

**KEEP AS CENTRAL**, but revise the underlying regulatory example before rewriting.

The *behavior*—hard stop + human referral—is central.

The specific paraquat classification should not determine the paper architecture.

---

## S5 verification/drop

**KEEP AS CENTRAL.**

One semantic clarification is necessary:

The system drops **an unsupported claim/sentence**, not necessarily the whole answer.

That distinction should be built into the final content plan.

---

## Figure 2

**KEEP AS CENTRAL.**

The three screenshots are valuable.

The rest of the screenshots belong in the appendix.

---

# 8. EVALUATION TRIAGE

The main paper should have **four evidence questions**, not fifteen.

## Evidence Question 1

> Does the system stop treatment requests that lack the crop?

**Essential.**

Use:

* 200 authentic queries;
* 30 missing crop;
* 30/30 halted before retrieval.

The annotator agreement can be a brief support statement.



---

## Evidence Question 2

> Does crop conditioning reduce off-target evidence and does the system catch explicit text–image conflicts?

**Essential.**

Use:

* 400-query stress set;
* 36.25% → 28.75%;
* 453/454 explicit conflicts detected.

But the metric must be renamed.

The current definition measures **off-target retrieved evidence**, not “wrong-crop advice.” 

This correction is part of the **content architecture**, not merely wording.

---

## Evidence Question 3

> Does the guard reduce unsafe outputs on both the deployed model and the cloud benchmark?

**Essential.**

Primary system result:

**52.5% → 10.71% on deployed model.**

Secondary benchmark:

**36.19% → 0.95% on cloud model.**

Both matter because the first tells the reviewer about the actual system while the second provides a useful controlled reference.



---

## Evidence Question 4

> Does the dosage verifier catch deliberately corrupted dosage claims?

**Essential.**

Use:

* 114/118 live mutation cases;
* 296/350 scaled benchmark if space permits;
* explicitly state that the verifier covers numerical dosage claims, not all agricultural factuality.



---

## Human audit

**KEEP AS SUPPORTING EVIDENCE.**

This is valuable because it answers a different reviewer question:

> “Do the delivered outputs actually look safe/actionable to humans?”

The 46/47 Grade-1 result and κ≈0.82 are useful. 

But the detailed rubric belongs in the appendix.

---

## Banglish red-teaming

**PROMOTE STRONGLY, but into the appendix unless space permits.**

This is unusually well connected to the stated Bengali deployment problem.

The 85/85 interception result directly supports the claim that formal-script-only safety checks are insufficient for your target interaction environment. 

If you have room for only one secondary safety result, this is the one I would preserve.

---

# 9. MAIN-TRACK BLOAT: EXACT CASES

## 1. “Evaluation Units”

Current appendix formally distinguishes:

* query;
* case;
* mutation case;
* system case.



### Why this is bloat

It establishes an experiment vocabulary rather than helping a reviewer understand the system.

### Current function

Methodological bookkeeping.

### Do instead

Use ordinary terminology directly in each experiment.

**MOVE TO APPENDIX** or **REMOVE.**

---

## 2. Text-gate pass-through experiment

Current appendix reports a 400-case paired pass-through experiment with McNemar's test and several secondary statistics. 

### Why this is bloat

It is an interesting robustness check for C1, but the main claim already has a direct 200-authentic-query validation.

### Do instead

Keep it in the appendix as evidence that the gate does not unnecessarily halt valid crop-specified requests.

**MOVE TO APPENDIX.**

---

## 3. PRISM conformance

The current appendix reports an overall conformance of **0.478** and a conversational-follow-up result of **0/100 because the D tier is absent**. 

### Why this is bloat

A reviewer can reasonably ask:

> “Why are you telling me your system got 0/100 on conversational follow-up?”

when the reason is simply that the benchmark's conversational tier was unavailable.

That does not improve understanding of KrishokTech.

### Do instead

**REMOVE FROM SUBMISSION.**

Keep the internal result in the evaluation repository if desired.

---

## 4. Token metering

Current appendix measures 89-token clarification versus 2,146-token retrieval context. 

### Why this is bloat

It does not answer an EACL demo-review question.

### Do instead

**REMOVE or keep only in internal experiment artifacts.**

---

## 5. Exploratory 14-row answer review

Current appendix explicitly says the result is descriptive and does not establish quality superiority, with manual rubric scoring pending. 

### Why this is harmful

It communicates incompleteness without contributing meaningful evidence.

### Do instead

**REMOVE ENTIRELY.**

This is one of the clearest self-inflicted reviewer concerns.

---

## 6. INT8 analysis

The appendix contains detailed storage, latency, McNemar tests, degradation thresholds, and a rejected rice INT8 model. 

### Why this is bloat

Your contribution is not quantization.

### Current function

Shows implementation optimization.

### Do instead

One sentence such as:

> “The deployed crop models are small enough for client-side inference.”

Exact quantization experiments belong in the artifact documentation.

**MOVE TO APPENDIX.**

---

## 7. Detailed SMS comparison

The current appendix contains a full three-arm comparison, mutation conditions, seed, slot-survival details, chemical-name retention, and invented-dosage behavior. 

### Why this is bloat

It creates a second research story:

> “We have invented a safe SMS compression algorithm.”

That is not your core paper.

### Do instead

Say that verified responses can be exported to SMS and offline formats; put the measurements in the appendix.

**MOVE TO APPENDIX.**

---

## 8. Offline packet-loss experiments

Useful, but simulated. 

### Do instead

**APPENDIX.**

The fact that an offline card exists is a system capability. The network simulation is supporting evidence.

---

## 9. Modeled cost

The system reports both modeled and token-meter-derived costs. 

### Why this is bloat

No reviewer needs the paper to establish a cost-saving contribution.

**MOVE TO APPENDIX or REMOVE.**

---

## 10. Trace ordering

100/100 traces preserve event order.

### Why this is bloat

This is implementation correctness rather than a substantive user/system contribution.

**REMOVE FROM SUBMISSION.**

---

# 10. “AI HONESTY” OVEREXPOSURE

This requires care because some of your transparency is genuinely good.

## A. Important scientific limitation

**Keep.**

Examples:

* no field study;
* crop-fence stress benchmark not live farmer sessions;
* synthetic contradiction cases;
* verifier covers numerical dosage claims;
* local model has non-zero residual ASR.

These materially define what the results mean. 

---

## B. Required qualification

**Keep.**

Examples:

* cloud vs local model distinction;
* simulated packet-loss condition;
* expert audit sample size;
* bounded scope of verifier.

These prevent overclaiming.

---

## C. Harmless implementation detail

**Appendix.**

Examples:

* exact classifier thresholds;
* model footprint;
* detailed SMS character survival;
* exact latency decomposition.

---

## D. Unnecessary self-inflicted reviewer concern

### 1. PRISM 0.478

Remove.

### 2. Conversational follow-up 0/100 because benchmark tier unavailable

Remove.

### 3. 14-row “pending” review

Remove.

### 4. Safety-envelope dangerous acceptance 0.374

The appendix currently reports:

> dangerous acceptance = 0.3740

on an offline stub generation probe. 

This is the type of number that invites a reviewer to conclude:

> “Why is the alleged safety system accepting dangerous cases 37.4% of the time?”

even though the setup is a specific offline routing probe rather than the deployed advisory pipeline.

Unless this result is directly necessary for a claim you retain, **remove it from the paper**. Keep it in your internal evaluation registry.

### 5. SMS chemical-name retention 34/100

This is honest, but it distracts from the actual certified claim.

The main paper does not need to announce that its SMS channel preserved chemical names only 34% of the time.

**Appendix only.**

---

# 11. CLAIM–EVIDENCE BALANCE

| Major claim                                             |                         Evidence strength | Assessment                                   | Action                                               |
| ------------------------------------------------------- | ----------------------------------------: | -------------------------------------------- | ---------------------------------------------------- |
| Explicit control states improve handling of uncertainty |                                    Strong | Well supported by architecture + demo        | **Central**                                          |
| C1 prevents retrieval on crop-less treatment queries    |              Strong within 200-query test | Good                                         | **Central**                                          |
| C2 reduces wrong-crop advice                            |       **Too strong as currently defined** | Metric is retrieval contamination            | Rename to off-target retrieval                       |
| Mismatch badge handles explicit text/image conflicts    |                  Strong within tested set | 453/454                                      | **Central**                                          |
| C3 lowers attack success                                | Strong under defined benchmark conditions | Good                                         | **Central**, lead with deployed model                |
| System is safe                                          |                                 Too broad | Residual 10.71% local ASR                    | Use “reduces unsafe outputs under tested conditions” |
| Dosage claims are verified                              |             Moderately strong but bounded | Strong for tested numerical mutation classes | Say “numerical dosage claims”                        |
| DialectSelector narrows retrieval gap                   |                        Weak in this paper | No direct causal evaluation                  | Remove improvement claim                             |
| System is first                                         |                               Unsupported | Literature comparison cannot establish this  | Remove                                               |
| System works offline                                    |                      Strong as capability | Performance under network loss is simulated  | State capability; simulation in appendix             |
| Six crops                                               |                           Strong as scope | Not novelty                                  | Mention as scope                                     |
| Web/SMS/read-aloud                                      |                   Strong as functionality | Not novelty                                  | Mention only                                         |
| Supports extension officers                             |                             Design intent | Not validated by field study                 | Keep as intended-use framing                         |

---

# 12. NOVELTY FOCUS

## The novel system idea

Not:

* Bengali;
* agriculture;
* RAG;
* multimodal;
* citations;
* speech;
* SMS;
* ONNX;
* local LLM.

Those are components/settings.

### The actual distinctive idea is:

> **The advisory system enforces explicit decision boundaries before retrieval, during multimodal evidence selection, and before rendering safety-critical generated claims.**

This is the system-level contribution.

---

## The three ideas that deserve repeated emphasis

### 1. Explicit control states

**ASK / CONFIRM / REFER / DROP**

This is the most user-visible formulation.

### 2. Evidence is constrained before generation

**Crop-conditioned retrieval + text/image conflict confirmation.**

This differentiates the system from a generic multimodal RAG assistant.

### 3. Generated safety-critical claims are untrusted until checked

**Dosage verification before rendering.**

This differentiates your system from a generic evidence-trace interface such as My Climate CoPilot, which emphasizes exposing information and self-evaluation, whereas KrishokTech's system architecture makes verification a release gate. ([ACL Anthology][2])

---

# 13. WHERE THOSE IDEAS SHOULD APPEAR

| Part              | Idea to emphasize                                   |
| ----------------- | --------------------------------------------------- |
| **Title**         | Deterministic/evidence-bounded control architecture |
| **Abstract**      | Three controls + continuous interaction             |
| **Introduction**  | Uncertainty becomes explicit system state           |
| **Related Work**  | Integration/enforcement distinction                 |
| **Architecture**  | T0–T4 control boundaries                            |
| **Demonstration** | ASK → CONFIRM → REFER → DROP                        |
| **Evaluation**    | One validation per control                          |
| **Conclusion**    | Model output does not automatically become advice   |

The title should **not** primarily sell “safe,” “multimodal,” or “system demonstration” because those descriptors are generic. The title should communicate the architectural idea.

---

# 14. FINAL SECTION-BY-SECTION CONTENT BLUEPRINT

## Title

### Purpose

Tell the reviewer immediately what system idea is being demonstrated.

### MUST contain

* KrishokTech;
* Bengali agricultural advisory;
* explicit deterministic/evidence-bounded control concept.

### SHOULD emphasize

Architecture/control idea.

### SHOULD remove

Generic words such as “A Safe, Multimodal System Demonstration…” as the main title concept.

### Maximum detail

One architectural descriptor + one domain descriptor.

---

# Abstract

### Purpose

One-minute mental model.

### MUST contain

Problem → three controls → demonstrated interaction → 2–4 headline evidence facts.

### SHOULD emphasize

* explicit control states;
* pre-retrieval halt;
* crop-fenced/conflict handling;
* dosage verification;
* deployed-system validation.

### Compress

* channel list.

### Remove

Detailed implementation attributes.

---

# Introduction

### Purpose

Explain why this system design exists.

### MUST contain

1. agricultural advisory risk;
2. concrete uncertainty/failure modes;
3. KrishokTech's design principle;
4. three controls;
5. transition to demonstration.

### SHOULD emphasize

The conceptual sentence:

> uncertainty/safety decisions are explicit system states rather than model behavior.

### Remove/compress

* exact prior retrieval benchmark;
* long general agricultural-access motivation;
* broad claims about all low-resource NLP.

### Maximum detail

~4–5 compact paragraphs.

---

# Related Work

### Purpose

Position the system against the correct neighbors.

### MUST contain

* agricultural advisory systems;
* evidence/verification systems;
* multimodal/conflict systems;
* Bengali/low-resource context.

### SHOULD emphasize

Why your combination is distinctive.

### Compress

individual paper summaries.

### Remove

feature table based on “Not described.”

### Maximum detail

~2–3 compact paragraphs.

Recent accepted demos support this concise positioning style: My Climate CoPilot has a focused related-work section, Verification Assistant combines introduction and related work compactly, and FactSearch is only seven published pages while still giving a clear positioning argument and evaluation. 

---

# System Design

### Purpose

Explain the system well enough that the reviewer can reconstruct the workflow.

### MUST contain

* T0–T4 architecture;
* control semantics;
* retrieval fence;
* text/image conflict handling;
* generation-verification boundary;
* user-visible states.

### SHOULD emphasize

Each stage constrains what the next stage is allowed to do.

### Compress

* exact thresholds;
* exact model formats;
* exact tokenizer rules;
* deployment micro-details.

### Move to appendix

Tri-state thresholds, five-slot extractor schema, dialect presets.

### Maximum detail

Three conceptual subsections, one per control family.

---

# Demonstration

### Purpose

Prove this is a system demonstration rather than an architecture proposal.

### MUST contain

S1–S5.

### SHOULD emphasize

The causal progression:

**underspecified → scoped → contradictory → unsafe → verified**

### Keep

Three main screenshots.

### Move to appendix

remaining gallery screenshots.

### Maximum detail

Enough for a reviewer to mentally simulate the interaction.

Recent accepted demos consistently make this interaction/system workflow concrete. My Climate CoPilot uses a clear five-step workflow; Verification Assistant describes the workflow immediately after its architecture; OpenGlass similarly ties its evaluation and system description to concrete interaction patterns. 

---

# Evaluation

### Purpose

Validate that the system actually performs the promised control behaviors.

### MUST contain

**C1:** 200 queries / 30 missing crop / all halted.

**C2:** 400 stress cases / off-target evidence reduction / 453 of 454 explicit contradictions.

**C3:** deployed and cloud ASR comparison.

**Verifier:** controlled dosage mutation detection.

### SHOULD contain

One concise human audit result.

### Should be compressed

* detailed statistical machinery;
* secondary channel evaluations;
* micro-latencies.

### Maximum detail

~1.5–2 pages.

The CFP explicitly does **not** require comprehensive experimentation; it only requires evidence validating usefulness/quality, and explicitly accepts benchmark, simulation, expert evaluation, usage statistics, case study and qualitative evidence. ([EACL 2027][1])

---

# Availability / Licensing

### Purpose

Satisfy a core EACL 2027 systems criterion.

### MUST contain

* live demo URL;
* screencast URL;
* installation/source URL;
* code/data/model licensing.

### SHOULD emphasize

What a reviewer can actually access.

### Compress

hardware/configuration details.

The current CFP specifically requires the video and live demo/package links in both the PDF and OpenReview. ([EACL 2027][1])

---

# Ethics

### Purpose

Handle the fact that this is safety-sensitive agricultural advice.

### MUST contain

* provenance of farmer queries;
* de-identification/consent;
* privacy handling;
* human referral;
* residual safety risk;
* bounded claims.

### SHOULD emphasize

The system is an advisory aid, not a replacement for extension officers.

### Compress

operational helpline-hour details that can change.

The CFP says sensitive-task/data papers that do not address legitimate ethical concerns will not be accepted, and specifically allows extra ethics/broader-impact space outside the six content pages. ([EACL 2027][1])

---

# Appendix

### Purpose

Provide reproducibility and reviewer-verifiable depth without polluting the six-page story.

### KEEP

* exact T0 safety taxonomy/matching method;
* tri-state visual thresholds;
* extractor slot definitions;
* dialect presets;
* per-crop model measurements;
* detailed crop-fence benchmark;
* detailed safety attack families;
* deployed-model safety table;
* dosage mutation table;
* human-evaluation rubric;
* Banglish red-team benchmark;
* SMS/offline measurements if the artifact release supports them;
* evidence ledger, but only after removing unnecessary diagnostics.

### REMOVE

* PRISM 0.478;
* 0/100 conversational follow-up;
* pending 14-row answer review;
* trace-ordering;
* modeled cost unless you need it for artifact documentation;
* token metering;
* detailed INT8 development history.

The current accepted-demo ecosystem supports extensive appendices and technical detail when useful; LocalRQA, My Climate CoPilot, RAGVUE and OpenGlass all devote significant space to implementation/evaluation beyond the core story. 

---

# 15. THE SIX-PAGE SURVIVAL SET

If I had to physically lock the main paper today, this is the set I would allow through:

### Page 1

**Abstract + Introduction**

### Page 2

**Related Work + architecture figure**

### Page 3

**System Design**

### Page 4

**Demonstration + three screenshots**

### Page 5

**C1 + C2 Evaluation**

### Page 6

**C3 + compact limitations + availability/conclusion**

Everything else goes into appendix, references, or ethics space.

That structure is much closer to the observable shape of successful system demos: a clear problem/system identity very early, an immediately understandable system workflow, then focused validation. My Climate CoPilot's first page is a particularly strong example of putting the system workflow alongside the abstract rather than making readers wait for it. 

---

# 16. FINAL EDITING QUEUE

## P0 — MUST FIX BEFORE SUBMISSION

### P0.1 — Central metric definition

**Location:** §5.2, Table 2, Appendix B.

Change the conceptual metric from **“wrong-crop advice”** to the actual measured retrieval quantity.

Reason: this is the clearest claim/evidence mismatch.

---

### P0.2 — Regulatory example

**Location:** §3.1, S4, Ethics, Appendix C.

Resolve the current **paraquat/banned** wording before rewriting the surrounding content.

The safety behavior can stay; the legal characterization needs evidence.

---

### P0.3 — Novelty claim

**Location:** Related Work final paragraph.

Remove the “first system” priority claim.

---

### P0.4 — Cloud/local safety framing

**Location:** Abstract, §5.3, Table 2.

Make the **deployed local model** the primary system result; present cloud evaluation as controlled secondary evidence.

---

### P0.5 — Figure 1 semantics

**Location:** Figure 1 + §3 opening.

Make it unmistakable that there are **T0–T4 control stages followed by delivery**, rather than six T-stages.

---

### P0.6 — PDF/source consistency

**Location:** submission artifact/source.

The current PDF title is:

> “KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory”

while the current source contains:

> “KrishokTech: A Safe, Multimodal System Demonstration for Bengali Agricultural Advisory.”

That source/PDF mismatch needs to be resolved before submission.  

---

### P0.7 — Required artifacts

**Location:** Availability + OpenReview.

Verify externally that:

* live demo works;
* package works;
* screencast works;
* same URLs are in PDF and OpenReview.

These are explicitly mandatory under the current CFP. ([EACL 2027][1])

---

# P1 — HIGH VALUE

### P1.1

Remove Table 1 and replace it with a compact positioning paragraph.

**Location:** §2, Table 1. 

### P1.2

Move Figure 1 earlier so the system architecture is visible by page 2.

**Location:** Figure 1 / §2–3 boundary.

### P1.3

Remove the exact prior retrieval R@10 0.970→0.093 from the central Introduction narrative.

**Location:** Introduction ¶2. 

### P1.4

Remove the 14-row exploratory answer review.

**Location:** Appendix A. 

### P1.5

Remove PRISM conformance from the submission.

**Location:** Appendix A. 

### P1.6

Move token metering, INT8 details, SMS comparison, offline packet-loss analysis and modeled cost to appendix/artifact documentation.

### P1.7

Make the Why panel/provenance behavior explicitly part of the demonstration contribution.

**Location:** §3.3 + §4 S5.  

### P1.8

Add a very compact related-work bridge to **FactSearch/RAGVUE/Verification Assistant** as systems for transparent verification/inspection, not as feature competitors.

Their existence as recent accepted system demonstrations makes them useful positioning neighbors. ([ACL Anthology][4])

---

# P2 — NICE TO HAVE

### P2.1

Move exact visual-router thresholds into a cleaner appendix subsection.

### P2.2

Move detailed badge taxonomy into appendix.

### P2.3

Reduce appendix experiment identifiers such as N14/E50/N05c unless they materially help artifact reproducibility.

### P2.4

Clean unused bibliography candidates rather than adding references merely to look more comprehensive. The current `.bib` contains several unused candidates such as FrugalGPT, RouteLLM, AIEP, and others.

---

# P3 — DO NOT TOUCH NOW

Do not:

* redesign the architecture;
* collect a new farmer dataset;
* run a new field study;
* add dense retrieval experiments;
* build a new multimodal model;
* add more attack families merely to increase N;
* add another ablation;
* create a new benchmark solely for publication value.

None of those is necessary to define the six-page system-demo story.

---

# 17. THE FINAL KEEP / REMOVE / PROMOTE MAP

## KEEP AS CENTRAL

**System concept:** explicit control states.

**C1:** pre-retrieval halt.

**C2:** crop fencing + text/image confirmation.

**C3:** pre-render dosage verification.

**S1–S5:** continuous farmer workflow.

**Three screenshots.**

**Deployed-model safety evidence.**

**Dosage verifier evidence.**

**Human audit.**

**Ethics/privacy.**

**Live demo/video/package availability.**

---

## REMOVE / DE-EMPHASIZE

**“First system.”**

**Feature-comparison Table 1.**

**Exact prior dense-retrieval headline.**

**PRISM conformance.**

**14-row exploratory review.**

**Trace-ordering test.**

**Token metering.**

**Modeled cost.**

**Detailed INT8 development story.**

**Detailed SMS research comparison in the main paper.**

**Detailed packet-loss results in the main paper.**

**3,000-query dangerous-acceptance diagnostic**, unless there is a specific retained claim that requires it.

---

## PROMOTE MORE STRONGLY

**“Uncertainty becomes an explicit system state.”**

**“Evidence is fenced before generation.”**

**“Generated safety-critical claims are untrusted until verified.”**

**ASK → CONFIRM → REFER → DROP.**

**The actual deployed model boundary.**

**Banglish/colloquial safety handling.**

**The user-visible Why/provenance behavior.**

---

# 18. THE MOST IMPORTANT STRATEGIC DECISION

Your current paper is trying to be:

> **an agricultural application + Bengali NLP paper + multimodal RAG paper + safety benchmark + deployment report + system demo.**

The final paper should be perceived as:

> **a system demonstration of an evidence-bounded Bengali agricultural advisor whose distinctive design is the enforcement of explicit control states before retrieval, across conflicting evidence, and before safety-critical output is rendered.**

That is narrower.

It is also stronger.

It uses almost everything genuinely valuable in the current artifact while removing the parts that make a reviewer work too hard to figure out **what the system actually contributes**.

The resulting paper does not try to look more impressive. It makes the evidence you already have work harder.

[1]: https://2027.eacl.org/calls/demos/ "Call for System Demonstrations -"
[2]: https://aclanthology.org/2025.acl-demo.7/ "My Climate CoPilot: A Question Answering System for Climate Adaptation in Agriculture - ACL Anthology"
[3]: https://aclanthology.org/2024.acl-demos.14/?utm_source=chatgpt.com "LocalRQA: From Generating Data to Locally Training, Testing, and Deploying Retrieval-Augmented QA Systems - ACL Anthology"
[4]: https://aclanthology.org/2026.eacl-demo.35/?utm_source=chatgpt.com "RAGVUE: A Diagnostic View for Explainable and Automated Evaluation of Retrieval-Augmented Generation - ACL Anthology"
