Yes. I’ve treated **`main(10).tex` as the current manuscript/source**, `main(10).pdf` as the current compiled artifact, and **Step 1–3 as the already-approved editorial/content decisions**. I am not going to rewrite the prose yet. This pass is the **full section-by-section rewriting blueprint** that the subsequent prose-writing turns should follow.

The central editorial decision is the one already established in Step 3: the paper should read as **a system demonstration of an evidence-bounded Bengali agricultural advisor**, not as a retrieval paper, safety benchmark, deployment report, and demo paper simultaneously. :chatgpt-content-reference{index="0"}

---

# 0. GLOBAL REWRITING RULES

Before touching individual sections, every later rewrite should obey these rules.

### Core narrative

The manuscript should consistently communicate:

> **KrishokTech makes uncertainty and safety explicit system states, controlling what can be retrieved, what evidence can reach generation, and which generated safety-critical claims can reach the user.**

The three control families remain:

1. **C1 — pre-retrieval halting**
2. **C2 — crop-fenced evidence + text/image confirmation**
3. **C3 — pre-render dosage verification**

And the user-facing demonstration remains:

> **ASK → CONFIRM → REFER → DROP**

These are already the strongest structural elements of the manuscript. :chatgpt-content-reference{index="1"}

### Writing style

The prose should:

- start paragraphs with concrete situations or decisions;
- use active, precise verbs;
- avoid repeatedly announcing what a paragraph is about;
- avoid turning every mechanism into a “contribution”;
- avoid excessive “This demonstrates... / This highlights... / Taken together...” conclusions;
- avoid promotional language;
- avoid explaining standard technologies at textbook length;
- let figures and examples carry some of the explanation.

### Claim discipline

Every later sentence should pass:

> **Is this exactly what the experiment/system actually establishes?**

Especially:

- “wrong-crop advice” → **off-target retrieval/evidence**, unless answer-level correctness was actually evaluated;
- “first system” → **remove**;
- paraquat “banned” → **must be resolved before prose rewrite**;
- cloud safety result → do not let it implicitly represent the deployed local system;
- “DROP” → make clear that the unsupported **claim** is dropped, not necessarily the whole response.

These are not stylistic preferences; they are the major claim/evidence corrections identified in the supplied review material. :chatgpt-content-reference{index="2"}

---

# 1. TITLE

## Current role

The current source title is:

> *KrishokTech: A Safe, Multimodal System Demonstration for Bengali Agricultural Advisory*

while the reviewed PDF reportedly contains a different title. The source/PDF mismatch must be resolved first. :chatgpt-content-reference{index="3"}

## Rewriting objective

The title should tell a reviewer **what the system idea is**, not merely that it is “safe” and “multimodal.”

### Desired conceptual structure

**KrishokTech + control/evidence concept + Bengali agricultural advisory**

The approved plan specifically favors an architectural descriptor over generic “A Safe, Multimodal System Demonstration...” wording. :chatgpt-content-reference{index="4"}

### Proposed editorial direction

I would retain the exact intended title decision for the actual writing pass only after resolving the source/PDF mismatch. The title family should be closer to:

> **KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory**

if that is indeed the intended approved title.

### What to remove

Avoid stacking:

- safe,
- multimodal,
- system,
- demonstration,
- Bengali,
- agricultural,
- advisory

as generic descriptors.

### Why this improves the demo paper

It tells the reviewer **what design principle they should notice**, rather than merely identifying the paper as a demo.

### Claim-strength flag

**No stronger claim should be introduced in the title.** “Evidence-bounded” is acceptable only insofar as it accurately describes the actual verification/fencing pipeline.

---

# 2. ABSTRACT

## Current function

The current abstract already has the correct ingredients:

- agricultural advisory setting;
- explicit uncertainty/safety states;
- three controls;
- continuous interaction;
- C1 result;
- C2 result;
- safety result. :chatgpt-content-reference{index="5"}

The problem is primarily **emphasis and terminology**, not missing content.

## Rewrite structure

Use exactly this progression:

### Sentence 1 — setting/problem

Introduce the concrete risk:

> Bengali agricultural advisory requires more than fluent conversational generation because treatment requests may be incomplete and evidence may conflict.

Do **not** spend several sentences establishing the importance of agricultural extension.

### Sentence 2 — design principle

Introduce the central idea:

> KrishokTech treats uncertainty and safety as explicit interaction/control states.

This should become the abstract's conceptual anchor.

### Sentence 3 — C1

State:

- missing crop;
- treatment request;
- halted before retrieval.

### Sentence 4 — C2

State:

- crop-conditioned evidence;
- text/image disagreement;
- confirmation.

Do **not** call the metric “wrong-crop advice” if the benchmark measures retrieval contamination.

### Sentence 5 — C3

State:

- generated dosage-bearing claims are drafts;
- claims are checked against evidence and permitted ranges;
- unsupported claims are removed before rendering.

### Sentence 6 — demonstration

Mention that the system is demonstrated through the continuous:

> ASK → CONFIRM → REFER → DROP

sequence.

### Evidence

Keep only approximately **2–4 headline facts**.

Priority:

1. 30/30 missing-crop cases halted;
2. C2 off-target evidence result;
3. deployed-model safety result;
4. dosage verification result if space permits.

The current content blueprint explicitly says the abstract should contain problem → three controls → demonstrated interaction → 2–4 evidence facts. :chatgpt-content-reference{index="6"}

## Compress/remove

Compress:

- web/SMS/offline channel enumeration;
- model implementation details;
- latency details.

## Important correction

The abstract currently gives:

> cloud attack success 36.19% → 0.95%

while the deployed local model has a materially different result. The approved editorial direction is to make the **deployed model the primary system evidence** and cloud evaluation secondary. :chatgpt-content-reference{index="7"}

### Why this improves the demo paper

The abstract will describe **the system reviewers can actually interact with**, rather than allowing one benchmark configuration to define the system's perceived safety.

### Claim-strength flag

Do not write anything equivalent to “the system prevents unsafe outputs.” The evidence supports **reduction/detection/blocking under the evaluated conditions**, not universal safety.

---

# 3. INTRODUCTION

## Target length

Approximately **4–5 compact paragraphs**, rather than expanding the motivation. :chatgpt-content-reference{index="8"}

The introduction should follow the exact six-step logic requested in your prompt:

> **concrete user/problem → existing difficulty → specific failure mode → system idea → distinctive aspect → demonstration/evidence**

---

## Paragraph 1 — concrete farmer setting

### Purpose

Put the reviewer immediately in the actual interaction context.

Use:

- farmer needs advice when symptoms/pests appear;
- extension access may not be immediate;
- digital advisory is useful.

### Keep

The existing Bangladesh agricultural-access framing and citations.

### Compress

The current broader discussion of why digital agriculture matters.

### Do not do

Do not make this paragraph sound like a general digital-agriculture survey.

### Why

A demo paper benefits from making the **interaction problem concrete immediately**, rather than spending page space establishing a broad societal motivation.

---

## Paragraph 2 — concrete failure modes

This paragraph should introduce the actual reasons a generic conversational advisor can fail.

Keep four failure modes:

1. treatment request without crop;
2. colloquial/regional/Banglish phrasing;
3. image/text disagreement;
4. generated dosage unsupported by evidence.

The current manuscript already establishes these well. :chatgpt-content-reference{index="9"}

### Treatment of prior retrieval work

The exact:

> R@10 0.970 → 0.093

result should **not be the centerpiece** of this paragraph.

It may remain as supporting evidence that colloquial agricultural retrieval is difficult, but the introduction should not pivot into:

> “our previous retrieval paper showed...”

because that makes the new manuscript look like an extension of the retrieval paper.

The approved blueprint explicitly calls for removing the exact prior benchmark from the central narrative. :chatgpt-content-reference{index="10"}

### Why

The reviewer needs to understand **why explicit control is necessary**, not learn the full history of your retrieval benchmark.

---

## Paragraph 3 — central design principle

This becomes the conceptual heart of the Introduction.

Core idea:

> KrishokTech does not ask the language model to resolve every uncertainty implicitly.

Instead:

> uncertainty and safety decisions are represented as explicit system states.

Then briefly explain that these decisions happen **before retrieval, during evidence reconciliation, and before rendering**.

This idea is already present in the current manuscript. :chatgpt-content-reference{index="11"}

### Why

This sentence provides the intellectual identity of the paper.

Without it, the paper risks reading as a list of safety features.

---

## Paragraph 4 — three controls

This is the compact contribution/system map.

### C1

> underspecified treatment request → halt before retrieval → ASK/referral.

### C2

> identified crop → retrieval fence → conflicting modalities → CONFIRM.

### C3

> generated dosage claim → evidence/range check → render or DROP.

Keep the existing C1/C2/C3 labels because they provide a clean organizational spine for the Evaluation.

### Why

The entire manuscript can now map cleanly:

> **Introduction claim → System mechanism → Demonstration behavior → Evaluation evidence**

That is exactly the structure a system-demonstration paper needs.

---

## Paragraph 5 — demonstration transition

End by telling the reader what they will actually see.

Not:

> “We evaluate three mechanisms extensively.”

Instead:

> the demonstration follows one continuous farmer interaction through clarification, crop scoping, multimodal disagreement, referral, and verified delivery.

Mention:

- live system;
- screencast;
- artifact availability.

The links themselves can remain compact.

### Why

The Introduction should make the reader expect a **demo**, not another benchmark section.

---

# 4. RELATED WORK AND POSITIONING

## Target

Approximately **2–3 compact paragraphs**. :chatgpt-content-reference{index="12"}

The current Related Work has the correct literature neighborhoods but should become explicitly comparative rather than paper-by-paper.

---

## Paragraph 1 — agricultural conversational systems

Group:

- Farmer.Chat;
- KrishokBondhu;
- Krishi Sathi;
- Bengali agricultural RAG.

Do not summarize each paper independently.

Instead establish:

> localized agricultural conversation, retrieval, multimodal input, and clarification are established system ingredients.

Then pivot immediately:

> KrishokTech focuses on **when those components should be allowed to proceed**.

### Why

This prevents the section from becoming a bibliography and gives the reader a meaningful comparison dimension.

---

## Paragraph 2 — grounding, verification, abstention, conflict

Group:

- My Climate CoPilot;
- AgroLLM;
- VLM contradiction work;
- abstention;
- clarification;
- relevant safety-critical dialogue.

Then explain:

> These works motivate evidence inspection, bounded generation, abstention, and clarification; KrishokTech integrates those decisions as enforceable pipeline boundaries in an agricultural advisory workflow.

The existing manuscript already makes the useful observation that the same architecture decides both when not to retrieve and when not to render. :chatgpt-content-reference{index="13"}

### Why

This turns the literature review into a **comparison of design responsibilities**, rather than a sequence of citations.

---

## Paragraph 3 — Bengali/low-resource and system-tooling context

Briefly establish:

- colloquial Bengali/Banglish creates an additional deployment constraint;
- existing resources skew toward formal text;
- recent inspectable verification/demo systems such as FactSearch/RAGVUE/Verification Assistant provide relevant system precedents.

The latter should be positioned as **system/inspection neighbors**, not direct agricultural competitors.

The approved blueprint specifically calls for this compact bridge. :chatgpt-content-reference{index="14"}

---

## Remove “first system”

Delete:

> “To our knowledge, KrishokTech is the first system...”

Replace the underlying idea with:

> **KrishokTech combines pre-retrieval halting, crop-conditioned evidence fencing, and pre-render dosage verification in one enforceable, farmer-visible pipeline.**

The distinction is **integration**, not historical priority.

### Why

The current comparison table cannot support a priority claim because “Not described” cannot establish that another system lacks a capability. :chatgpt-content-reference{index="15"}

### Claim-strength flag

**Do not replace “first” with another implicit superlative** such as “unique,” “unprecedented,” or “the only.”

---

# 5. REMOVE TABLE 1 FROM THE MAIN NARRATIVE

This deserves its own editorial decision.

## Current role

Table 1 compares control mechanisms across systems.

## Decision

**Remove from main paper.**

Do not spend prose trying to defend the table.

### Why

The table's evidentiary basis is:

> “Not described.”

while simultaneously acknowledging:

> “Not described” does not mean the system lacks the mechanism.

That makes it weak evidence for comparative novelty. :chatgpt-content-reference{index="16"}

### Replacement

Use one concise positioning paragraph.

### Appendix?

Only retain a comparative table if it is genuinely useful for artifact/reviewer context and can be grounded in documented capabilities. Otherwise remove it completely.

---

# 6. SYSTEM DESIGN

## Overall purpose

The System Design section should answer:

> **What enters the system, what decision happens next, what is allowed through, what can be blocked, and what reaches the farmer?**

The approved structure is exactly **three conceptual subsections**, corresponding to the control families. :chatgpt-content-reference{index="17"}

---

# 6.1 Subsection 1 — Halting Before Retrieval

This remains C1.

## Opening

Start with the control boundary, not implementation details:

> The first decision is whether the request should be allowed to reach retrieval at all.

Then explain T0/T1.

### T0

Keep:

- deterministic safety precheck;
- dangerous/unsafe request handling;
- human referral;
- zero LLM invocation where applicable.

### T1

Then:

- extract crop/symptom/treatment intent;
- if treatment request lacks resolvable crop;
- halt;
- no BM25 retrieval;
- ASK/referral.

The current source describes exactly this sequence. :chatgpt-content-reference{index="18"}

### Human-readable system logic

The prose should make this visually reconstructible:

> **unsafe request → REFER**  
> **missing safety-critical crop → ASK**  
> **otherwise → retrieval**

### Move out

Appendix:

- exact matching patterns;
- slot schema;
- detailed timing;
- dialect preset mechanics;
- tokenizer details.

### Regulatory wording

The current “banned pesticide / paraquat” example **must be resolved before this section is rewritten**.

The control behavior can remain unchanged, but the legal characterization cannot be casually rewritten. The supplied review explicitly flags this as a submission-critical issue. :chatgpt-content-reference{index="19"}

### Why this improves the demo

It makes C1 understandable as a **decision boundary**, rather than as a collection of filters.

---

# 6.2 Subsection 2 — Crop-Fenced Retrieval and Mismatch Badge

This remains C2 and should probably be one of the strongest technical sections.

## Opening

Explain:

> Once retrieval is permitted, evidence is still constrained by crop identity.

Then:

1. crop must be bound;
2. BM25 searches the curated agricultural evidence;
3. crop fence makes other-crop passages unreachable;
4. image classifier can provide crop identity;
5. ambiguity triggers disambiguation;
6. text/image mismatch triggers CONFIRM;
7. conflicting evidence within a crop can also trigger clarification.

The current manuscript has all of these behaviors. :chatgpt-content-reference{index="20"}

## Key conceptual distinction

Emphasize:

> The fence does not merely lower the rank of irrelevant evidence; it prevents it from entering the candidate evidence set.

That is an important system-design distinction.

## Visual router

Describe behaviorally:

> **confident → route**  
> **ambiguous → disambiguate**  
> **out-of-scope → recapture**

Do not put exact numerical thresholds in the main prose.

### Appendix

Move:

- confidence threshold;
- margin threshold;
- OOD threshold;
- model-by-crop measurements.

The approved blueprint explicitly recommends this. :chatgpt-content-reference{index="21"}

## Terminology correction

Never write:

> “wrong-crop advice”

for the C2 retrieval benchmark unless answer-level advice correctness was independently evaluated.

Use:

> **off-target retrieval**

or:

> **off-target crop evidence in top-k retrieval**

This is one of the most important rewriting changes.

### Why

The original operational definition measures whether an off-target document appears among retrieved sources, not whether the generated answer is actually wrong. :chatgpt-content-reference{index="22"}

---

# 6.3 Subsection 3 — Untrusted Generation, Verification, and Delivery

This is C3.

## Opening concept

The first sentence should establish:

> Retrieval-grounded generation is still treated as a draft.

Then explain:

> T3 generates → T4 verifies → only accepted claims are rendered.

This is one of the strongest conceptual phrases in the current manuscript:

> **the draft is treated as unverified text, not a final answer.**

The current source explicitly establishes this boundary. :chatgpt-content-reference{index="23"}

## Verification

Keep:

- numerical/dosage claim extraction;
- retrieved passage grounding;
- permitted BARI/BRRI range;
- unsupported/out-of-range claim → dropped/annotated.

Do **not** imply that all agricultural factuality is verified.

### Important qualification

The verifier is for:

> **numerical dosage-bearing claims**

not all agronomic facts.

That limitation needs to remain visible.

## Provenance / Why panel

Promote slightly.

This is not merely UI decoration. It makes the backend control behavior **observable to the user**, which matters specifically in a demo.

Keep:

- provenance badge;
- Why explanation;
- source relationship.

Move detailed five-badge taxonomy to appendix.

## Delivery

Mention:

- web;
- SMS;
- offline card;
- Bengali read-aloud.

But only as a compact closing sentence.

### Why

Delivery channels establish deployment relevance without creating four additional contributions.

---

# 7. FIGURE 1 — ARCHITECTURE

## Required semantic correction

The paper currently describes:

> five stages T0–T4

but the visual includes six boxes because “Deliver” is downstream.

The final prose should explicitly define:

> **five control stages (T0–T4), followed by delivery.**

The supplied blueprint treats this as P0.5. :chatgpt-content-reference{index="24"}

## Figure narrative

The caption should communicate:

> each control stage can terminate or alter the interaction through ASK, CONFIRM, REFER, or DROP.

The delivery box should not visually imply a sixth T-stage.

### Why

The architecture becomes immediately reconstructible without making the reader reconcile numbering.

---

# 8. DEMONSTRATION

This should be the **centerpiece** of the paper.

The current S1–S5 sequence is already one of the strongest assets. :chatgpt-content-reference{index="25"}

## Opening paragraph

Very short.

Establish:

- intended audience;
- live system;
- one continuous farmer interaction;
- S1–S5 follows same order as screencast.

Then immediately begin S1.

---

# 8.1 S1 — Missing Crop / ASK

Use the actual farmer query.

Structure every step explicitly as:

> **USER ACTION → SYSTEM DECISION → VISIBLE RESPONSE → WHY IT MATTERS**

### User action

Colloquial crop-less pesticide-treatment question.

### System decision

T1 detects missing crop and stops before retrieval.

### Visible response

Crop chips / clarification.

### User action

Farmer selects potato.

### Visible response

Potato-grounded answer with citations.

### Why it matters

The system refuses to search on an incomplete safety-critical premise.

The existing manuscript provides this sequence clearly. :chatgpt-content-reference{index="26"}

---

# 8.2 S2 — Photograph Scopes Evidence

This step exists to make S3 possible.

### User action

Upload photograph.

### System decision

On-device classifier identifies crop.

### Visible response

Rice context is established.

### Retrieval effect

T2 fence limits evidence to rice.

### Privacy point

Photograph remains on-device.

### Why it matters

The image does not merely enrich the answer; it changes **which evidence is reachable**.

That is the key sentence.

---

# 8.3 S3 — Text/Image Mismatch / CONFIRM

This should receive the strongest narrative emphasis.

### User action

Provide text naming one crop while image indicates another.

### System decision

System refuses to silently choose one modality.

### Visible response

Crop Mismatch badge + confirmation.

### Why it matters

The system makes cross-modal uncertainty visible rather than silently resolving it.

This is probably the most distinctive demo moment.

### Figure

Use the strongest screenshot here.

---

# 8.4 S4 — Safety Referral / REFER

Keep the hard-stop behavior.

### User action

Unsafe request.

### System decision

Terminal safety/referral state.

### Visible response

Human assistance / helpline path.

### Why it matters

The system has a path where **generation is deliberately not attempted**.

### Regulatory caveat

Do not rewrite the exact chemical example until the paraquat issue is resolved.

---

# 8.5 S5 — Verification / DROP

This needs one semantic correction.

The system should not appear to “drop the answer” if it actually drops an unsupported claim.

### User action

Ask a dosage-bearing question.

### System decision

Generator produces a draft.

Verifier checks numerical claim.

### Visible response

Unsupported/out-of-range claim is removed or flagged; remaining grounded content is shown.

### Why it matters

Generation is not the terminal authority.

The terminal authority is the verification boundary.

### Why panel

Explicitly show the user-facing explanation/provenance.

---

# 9. FIGURE 2 / DEMO SCREENSHOTS

## Main paper

Keep the three strongest screenshots.

They should collectively show:

1. ASK;
2. CONFIRM;
3. verification/Why behavior.

The exact selection can be optimized visually later, but the content should represent the **control states**, not generic UI.

## Appendix

Move:

- remaining gallery screenshots;
- secondary delivery views;
- less important UI states.

### Why

The main paper should make the reviewer understand the interaction without spending half a page on interface inventory.

---

# 10. EVALUATION — NEW INTERNAL LOGIC

The Evaluation section should stop being organized as:

> “Here are all experiments we performed.”

Instead organize it around:

> **What reviewer doubt does each result resolve?**

The approved blueprint reduces the main evaluation to four evidence questions. :chatgpt-content-reference{index="27"}

---

# 10.1 C1 — Does the system stop treatment requests lacking a crop?

## Main result

- 200 farmer queries;
- 30 crop-less treatment requests;
- 30/30 halted before retrieval.

## Main interpretation

The gate enforces the intended information requirement without allowing retrieval to operate on an incomplete safety-critical premise.

## Keep

Human annotation/agreement only as a compact supporting fact.

## Move

Detailed:

- LLM comparison;
- latency;
- PRISM;
- token accounting

to appendix or remove.

The review material specifically identifies the LLM comparison as unnecessary main-paper complexity. :chatgpt-content-reference{index="28"}

### Reviewer doubt resolved

> “Is the pre-retrieval gate actually doing what the system says it does?”

---

# 10.2 C2 — Does crop fencing reduce off-target evidence and catch multimodal disagreement?

## Main result

- 400-query stress benchmark;
- off-target retrieval metric;
- 36.25% → 28.75%;
- 453/454 explicit conflicts detected.

## Terminology

Replace “wrong-crop advice” everywhere.

### Reviewer doubt resolved

> “Does the crop context actually constrain evidence, and does the system notice explicit modality conflicts?”

## Important distinction

Do not claim:

> “the system reduced wrong advice”

unless the answer itself was evaluated.

Claim:

> “crop fencing reduced off-target retrieved evidence.”

This is a central claim-evidence correction. :chatgpt-content-reference{index="29"}

---

# 10.3 C3 — Does safety guarding reduce unsafe outputs on the deployed system?

This should be reframed.

## Primary result

**Deployed local model**

> 52.5% → 10.71% guarded ASR

## Secondary result

**Cloud benchmark**

> 36.19% → 0.95%

The exact values should be checked against the current source/table during the actual prose pass, but the approved content plan clearly establishes the **local result as primary**. :chatgpt-content-reference{index="30"}

## Interpretation

The guard reduces attack success on the actual deployed configuration, while the cloud model provides a controlled secondary reference.

Do not make the cloud model appear to be the deployed system.

### Reviewer doubt resolved

> “Does the safety control matter on the system people actually interact with?”

---

# 10.4 Dosage verifier

## Main result

Keep the controlled mutation test:

- 114/118 live mutation cases;
- 296/350 scaled benchmark if space allows.

## Main interpretation

The verifier detects deliberate numerical perturbations that would otherwise alter safety-critical dosage claims.

## Qualification

Immediately state:

> This mechanism verifies numerical dosage claims against retrieved evidence and permitted ranges; it does not establish general agricultural factuality.

### Reviewer doubt resolved

> “Does the pre-render verifier actually detect unsupported dosage changes?”

---

# 10.5 Human audit

Keep one compact result.

The 46/47 Grade-1 result and κ≈0.82 are useful because they address a different question:

> “Do the delivered outputs remain usable/actionable to human reviewers?”

The rubric itself should go to the appendix.

### Why

This adds human-facing evidence without turning the paper into a user study.

---

# 10.6 Banglish / colloquial safety

The content plan says this is important because the system's deployment context is not just standard Bengali.

However, it should **not become another major evaluation narrative**.

### Main paper

One compact statement establishing that safety behavior was tested under colloquial/Banglish inputs.

### Appendix

Keep:

- red-team categories;
- phonetic variations;
- detailed results;
- attack families.

### Why

This strengthens the Bengali-specific system story without creating a second benchmark paper.

---

# 11. REMOVE/COMPRESS THE CURRENT “MAIN-TRACK BLOAT”

The following material should **not be allowed to compete with the core six-page narrative**.

The approved plan explicitly identifies these as secondary. :chatgpt-content-reference{index="31"}

---

## 11.1 Evaluation Units

### Action

Remove from main paper.

### Reason

Implementation bookkeeping rather than system behavior.

### Destination

Appendix only if necessary for reproducibility.

---

## 11.2 Text-gate pass-through experiment

### Action

Remove from main narrative.

### Reason

Does not answer a central demo-track question.

---

## 11.3 PRISM conformance

### Action

Remove.

### Reason

The PRISM result creates more questions than it resolves for this paper.

---

## 11.4 Token metering

### Action

Remove.

### Reason

Not relevant to the central user-facing system claim.

---

## 11.5 14-row exploratory answer review

### Action

Remove.

### Reason

Especially risky because an incomplete/pending exploratory analysis invites reviewer concern without strengthening the central evidence.

---

## 11.6 INT8 development history

### Action

Appendix/artifact documentation only.

### Reason

Useful implementation detail, not core system contribution.

---

## 11.7 Detailed SMS comparison

### Action

Main paper: one sentence.

Appendix: detailed numbers if artifact documentation benefits.

### Reason

SMS is a delivery mode, not a second research contribution.

---

## 11.8 Offline packet-loss experiments

### Action

Appendix.

### Reason

Deployment robustness is useful, but it should not displace the central control-state story.

---

## 11.9 Modeled cost

### Action

Remove unless needed specifically for artifact/deployment documentation.

### Reason

It is not necessary to validate the three central controls.

---

## 11.10 Trace ordering

### Action

Remove.

### Reason

Insufficient value relative to the space and cognitive overhead.

---

# 12. LIMITATIONS

This section should remain.

That is important because the manuscript's limitations are unusually useful for establishing scientific discipline.

The current material acknowledges:

- no field study;
- synthetic contradiction cases;
- verifier scope;
- residual local-model attack failures.

These should remain. :chatgpt-content-reference{index="32"}

## Structure

### Limitation 1 — no field deployment/user study

State directly.

Do not apologize.

### Limitation 2 — contradiction benchmark

State that most multimodal contradiction cases are constructed stress cases.

### Limitation 3 — verifier scope

Numerical dosage claims only.

### Limitation 4 — residual safety failures

The guard reduces but does not eliminate attacks on the deployed model.

### Limitation 5 — coverage

Current deployment covers six staple crops.

## Tone

Use factual boundaries:

> “The current evaluation does not establish...”

rather than:

> “Unfortunately, we were unable to...”

### Why

This sounds like a mature systems paper rather than a defensive paper.

---

# 13. AVAILABILITY AND LICENSING

This needs to be **short and explicit**.

## Must contain

- live demo;
- screencast;
- source/install package;
- license;
- relevant model/data licensing.

The current source already contains the live demo, screencast, and anonymous source/install URL. :chatgpt-content-reference{index="33"}

## Writing structure

One short paragraph or compact artifact block:

> Reviewers can interact with the live system at X, view the ≤2.5-minute screencast at Y, and obtain the source/installable package at Z. The released components are distributed under the stated licenses...

Do not spend prose on:

- hardware;
- directory structure;
- deployment micro-details.

### Why

For this track, availability is part of evaluation, but it should be **easy to verify rather than narratively elaborate**.

---

# 14. ETHICS / BROADER IMPACT

The current manuscript's ethics/privacy material should remain but become concise and concrete.

## Must cover

### Data provenance

Where farmer queries came from.

### Consent/de-identification

Retain the actual documented procedure.

### Image privacy

Important:

> crop images processed on-device / do not leave device

if that remains exactly supported by the system.

### Human referral

Explain that unsafe cases are routed to human assistance rather than generated through.

### Advisory boundary

Explicitly state:

> KrishokTech is an advisory aid and is not a replacement for agricultural extension professionals.

### Residual risk

Connect to the evaluation:

> safeguards reduce measured failures but do not establish complete safety.

### Why

This is especially important because the system operates in a safety-sensitive domain, and the supplied EACL guidance identifies ethics as an explicit review concern. :chatgpt-content-reference{index="34"}

---

# 15. CONCLUSION

The conclusion should be **short**.

## Do not repeat the entire paper.

Use three moves:

### 1. Restate the system idea

> KrishokTech makes uncertainty and safety explicit control states in Bengali agricultural advisory.

### 2. Restate the three boundaries

- before retrieval;
- across conflicting evidence;
- before rendering safety-critical claims.

### 3. End with what the demo establishes

The system provides a concrete, inspectable workflow in which:

> ASK → CONFIRM → REFER → DROP

are observable consequences of those controls.

Then one sentence on evidence:

> targeted evaluations validate the intended control behaviors, while the stated limitations define what remains unestablished.

### Why

The conclusion should reinforce the **system identity**, not introduce another result.

---

# 16. APPENDIX ARCHITECTURE

The appendix should become a **technical evidence repository**, not a second paper.

The approved plan says to preserve depth that helps reproducibility/reviewer verification. :chatgpt-content-reference{index="35"}

---

## Appendix A — Architecture and decision logic

Keep:

- exact T0 taxonomy;
- matching method;
- T1 slot definitions;
- tri-state visual thresholds;
- dialect presets;
- provenance badge taxonomy.

This is where implementation-specific information belongs.

---

## Appendix B — Evaluation protocols

Keep:

- evaluation unit definitions;
- detailed C1 protocol;
- detailed C2 stress benchmark;
- contradiction construction;
- dosage mutation protocol;
- detailed safety evaluation methodology;
- statistical details where necessary.

This protects the main paper from methodological clutter.

---

## Appendix C — Safety

Keep:

- detailed attack families;
- deployed-model table;
- Banglish/phonetic red-team benchmark;
- regulatory/policy details once verified.

### Critical

Do not carry an unresolved “paraquat = banned” statement into the appendix.

---

## Appendix D — Vision/crop models

Keep:

- per-crop model results;
- exact thresholds;
- OOD behavior;
- detailed crop-fence evaluation.

---

## Appendix E — Human evaluation

Keep:

- rubric;
- annotation protocol;
- agreement;
- full examples if useful.

---

## Appendix F — Delivery/deployment

Optional, if supported by the released artifact:

- SMS measurements;
- offline measurements;
- installation footprint;
- deployment configuration.

Do **not** turn this into a separate optimization paper.

---

# 17. SIX-PAGE MAIN-PAPER ORDER

The approved page architecture should remain the target.

## Page 1

### Abstract

Then:

### Introduction

End with the three-control map and demo transition.

---

## Page 2

### Related Work

Then architecture figure / beginning of system overview.

This is deliberately earlier than the current structure.

### Why

The reviewer should see the system identity very early.

---

## Page 3

### System Design

Three conceptual subsections:

1. C1 — Halting Before Retrieval
2. C2 — Crop-Fenced Retrieval
3. C3 — Untrusted Generation + Verification

---

## Page 4

### Demonstration

S1–S5.

Three strongest screenshots.

This is the **visual center of the paper**.

---

## Page 5

### Evaluation

C1 + C2.

Focused tables/results.

No auxiliary benchmark stories.

---

## Page 6

### Evaluation

C3 + dosage verification + compact human audit/limitations.

Then:

### Availability / Licensing

### Conclusion

Ethics can use the appropriate additional space if the submission format permits it.

This page architecture is explicitly established in the supplied blueprint. :chatgpt-content-reference{index="36"}

---

# 18. SECTION-TO-SECTION TRANSITION LOGIC

This is important for the eventual prose because the current manuscript sometimes reads as a collection of sections.

The new transitions should follow this chain:

### Introduction → Related Work

> Existing systems provide the ingredients; KrishokTech focuses on enforcing decisions about when those ingredients are allowed to operate.

### Related Work → System Design

> This motivates the three control boundaries.

### System Design → Demonstration

> The controls are not only backend mechanisms; they produce observable interaction states.

### Demonstration → Evaluation

> The evaluation tests whether each demonstrated control behaves as intended.

### Evaluation → Limitations

> These results validate the targeted behaviors but do not establish field-level safety/generalization.

### Limitations → Availability/Conclusion

> The released artifact makes those behaviors inspectable and reproducible within the stated scope.

This gives the paper one continuous argumentative movement.

---

# 19. WHAT SHOULD BE REPEATED THROUGHOUT THE PAPER

Only three conceptual ideas deserve deliberate repetition.

## 1. Uncertainty becomes an explicit system state

Use this in:

- Introduction;
- System Design;
- Demonstration;
- Conclusion.

---

## 2. Evidence is fenced before generation

Use this in:

- Introduction;
- C2;
- S2/S3;
- Evaluation.

---

## 3. Generated safety-critical claims remain untrusted until verified

Use this in:

- Introduction;
- C3;
- S5;
- dosage evaluation;
- Conclusion.

The supplied editorial blueprint identifies exactly these three as the concepts that deserve repeated emphasis. :chatgpt-content-reference{index="37"}

Do **not** repeatedly restate:

- BM25;
- LoRA;
- ONNX;
- 4-bit quantization;
- SMS;
- offline mode.

Those are implementation details, not the paper's conceptual refrain.

---

# 20. WHAT SHOULD NEVER BECOME A NEW CLAIM DURING REWRITING

This is the **claim firewall** for the subsequent prose-writing turns.

### Do not upgrade:

**Off-target retrieval**  
→ “wrong advice”

unless answer-level correctness was measured.

**Attack reduction**  
→ “safe”

unless safety is explicitly defined and supported.

**Dosage verification**  
→ “factuality verification”

because the verifier is bounded to numerical dosage claims.

**Integration**  
→ “first”

because the literature evidence does not establish priority.

**Current deployment**  
→ “general agricultural advisor”

because coverage is bounded.

**Cloud benchmark**  
→ “deployed system”

because the local model is the deployment boundary.

**Constructed multimodal stress cases**  
→ “real-world multimodal failures”

unless the data actually support that.

**Human audit**  
→ “farmer usability”

because the audit is not necessarily a farmer user study.

**Live demo**  
→ “field deployment”

because those are different claims.

---

# 21. FINAL KEEP / REMOVE / PROMOTE MAP

## KEEP AS CENTRAL

- system concept: explicit control states;
- C1 pre-retrieval halt;
- C2 crop fencing + text/image confirmation;
- C3 pre-render dosage verification;
- S1–S5 continuous interaction;
- three main screenshots;
- deployed-model safety evidence;
- dosage-verifier evidence;
- compact human audit;
- ethics/privacy;
- live demo/video/package availability.

This is the final approved central set. :chatgpt-content-reference{index="38"}

## REMOVE / DE-EMPHASIZE

- “first system”;
- feature-comparison Table 1;
- exact prior dense-retrieval headline;
- PRISM conformance;
- 14-row exploratory review;
- trace-ordering;
- token metering;
- modeled cost;
- detailed INT8 development history;
- detailed SMS comparison in main paper;
- detailed packet-loss results in main paper;
- large dangerous-acceptance diagnostic unless needed for a retained claim.

:chatgpt-content-reference{index="39"}

## PROMOTE

- “uncertainty becomes an explicit system state”;
- “evidence is fenced before generation”;
- “generated safety-critical claims are untrusted until verified”;
- ASK → CONFIRM → REFER → DROP;
- actual deployed-model boundary;
- colloquial/Banglish handling;
- Why/provenance behavior.

:chatgpt-content-reference{index="40"}

---

# 22. THE EXACT REWRITING ORDER I RECOMMEND

To avoid the quality degradation you mentioned from rewriting the entire paper in one pass, I would **not** write it sequentially from page 1 to page 6.

The controlled sequence should be:

### Pass 1 — Structural anchor
1. Title
2. Abstract
3. Introduction

### Pass 2 — Intellectual positioning
4. Related Work
5. remove Table 1 / replace with positioning paragraph

### Pass 3 — Technical explanation
6. System Design §3.1
7. System Design §3.2
8. System Design §3.3
9. Figure 1 caption/semantic wording

### Pass 4 — Demo prose
10. Demonstration opening
11. S1
12. S2
13. S3
14. S4
15. S5
16. Figure 2 caption

### Pass 5 — Evidence
17. Evaluation opening
18. C1
19. C2
20. C3
21. dosage verifier
22. human audit

### Pass 6 — Boundaries
23. Limitations
24. Availability/Licensing
25. Ethics
26. Conclusion

### Pass 7 — Appendix
27. Architecture/decision appendix
28. evaluation protocols
29. safety appendix
30. vision appendix
31. human evaluation
32. deployment appendix

### Pass 8 — Final consistency edit

Only after all prose exists:

- terminology consistency;
- C1/C2/C3 labels;
- ASK/CONFIRM/REFER/DROP consistency;
- “off-target retrieval” terminology;
- local/cloud distinction;
- dosage-verifier scope;
- figure references;
- citation preservation;
- title/PDF/source consistency.

---

## The final editorial target

The rewritten paper should leave a reviewer with one very clear mental model:

> **KrishokTech is an actual Bengali agricultural advisory system in which uncertainty and safety are not left entirely to the language model. The pipeline explicitly decides when to ask before retrieving, when to constrain or reconcile evidence, when to refer instead of generate, and when to remove a generated safety-critical claim before it reaches the user. The demonstration makes those decisions visible, and the evaluation validates the corresponding control behaviors.**

Everything else should support that sentence—or move out of the six-page story.

That is the full section-by-section plan I would use for the subsequent prose-writing passes, without redesigning the system or introducing new experimental claims.