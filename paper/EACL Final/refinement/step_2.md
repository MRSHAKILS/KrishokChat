I treated this as a **real EACL 2027 Systems Demonstrations review**, not as an ACL main-track paper review. I checked the current EACL 2027 CFP, recent ACL/EACL demo proceedings and close system papers, and the current KrishokTech PDF/source. I also searched the accessible supplied files for a separate supervisor/pre-submission memo but did **not** locate one, so I have not treated any unseen supervisor advice as evidence.

## Executive reviewer assessment

**Current-form reviewer impression:** KrishokTech is clearly a legitimate and substantial systems-demonstration submission. The S1–S5 interaction is unusually coherent, the system has a real live artifact and screencast, and the evaluation is directly connected to the system's claimed control points. I would **not** reject it because it lacks a farmer user study or because it contains substantial evaluation.

However, I would **not submit the current wording unchanged**. There are several avoidable issues that could turn a good demo-system review into a skeptical review:

1. the C2 headline metric is called **“wrong-crop advice” even though its operational definition is retrieval contamination**, not answer-level advice correctness;
2. the S4 example calls **paraquat a banned pesticide**, which is not supported by the current Bangladesh DAE material I checked;
3. the manuscript claims **“first system”** on the basis of a comparison table that explicitly says “Not described” does not establish absence;
4. the paper sometimes presents the **cloud safety result more prominently than the actual deployed local model result**;
5. the appendix contains several internal/negative experiments that are not needed to establish the system and could make the paper look like a benchmark report rather than a focused demo.

Those are fixable. The underlying system/demo story does not need a redesign.

---

# 1. STEP 1 — What EACL 2027 actually requires

The current official EACL 2027 Systems Demonstrations CFP is very explicit. ([EACL 2027][1])

| Requirement                     | Current EACL 2027 rule                                            | KrishokTech status              |
| ------------------------------- | ----------------------------------------------------------------- | ------------------------------- |
| Content length                  | **Up to 6 pages**; longer submissions are desk-rejected           | **Appears compliant**           |
| References                      | Unlimited                                                         | Yes                             |
| Appendix                        | Unlimited informative appendix                                    | Yes                             |
| Ethics/broader impact           | Unlimited additional space                                        | Yes                             |
| Technical detail                | Required, including visual aids                                   | Yes                             |
| Evidence                        | Some evidence required; comprehensive evaluation **not** required | Strongly satisfied              |
| Demo video                      | **≤2.5 min**, required                                            | Link present                    |
| Live demo/package               | **Mandatory**; missing it = desk rejection                        | Link present                    |
| Video link in PDF               | Required                                                          | Present                         |
| Video link in OpenReview        | Required                                                          | Must verify manually            |
| Demo/package link in PDF        | Required                                                          | Present                         |
| Demo/package link in OpenReview | Required                                                          | Must verify manually            |
| Review model                    | Single-blind                                                      | Fine; anonymity is not required |
| Reciprocal reviewer             | One author must be nominated                                      | Administrative check            |
| Ethics                          | Sensitive tasks/data must address legitimate concerns             | Strong coverage                 |
| Accepted-paper allowance        | One additional content page after acceptance                      | Not relevant now                |

The CFP's five review dimensions are:

**Motivation, Fit & Novelty; Related Work & Contribution; System & Demonstration Description; Evaluation, Availability & Licensing; Presentation Quality.** It specifically says comprehensive experiments are not required and lists benchmarks, simulations, expert evaluations, usage statistics, case studies, and qualitative feedback as acceptable evidence. ([EACL 2027][1])

### Important distinction

**Official requirement:** six content pages, video, live demo/package, some evidence, technical/system details, availability/licensing, ethics where relevant.

**Observed accepted-paper pattern:** recent accepted demos often include substantial system figures, interaction walkthroughs, benchmarks, screenshots, and appendices. This is not a requirement.

**My reviewer inference:** KrishokTech already exceeds the evidence threshold. The submission's main optimization should therefore be **clarity and claim discipline**, not adding more experiments.

That distinction matters because some recent published demos are much longer in total PDF length. For example, LocalRQA is 16 pages, My Climate CoPilot 9, DialogGuard 10, FactSearch 7, the EACL 2026 Verification Assistant 9, and OpenGlass 11. Those are **published final artifacts**, not the current six-page EACL 2027 content allowance, and many use additional material beyond the core content. ([ACL Anthology][2])

So I would **not** use "recent papers are 9–16 pages" as a reason to expand the main paper.

---

# 2. STEP 2 — What recent accepted demos actually do

I looked at a representative set rather than one or two examples.

### LocalRQA

LocalRQA puts the system/toolkit itself first, gives an architecture figure very early, includes a compact capability comparison, then explains the system modules and deployment interfaces. It also provides a live interactive component and human evaluation functionality. 

**Lesson for KrishokTech:** system architecture + demonstrable interaction + practical deployment is entirely legitimate as the center of an EACL demo paper. You do not need to turn it into a methodological benchmark paper.

### My Climate CoPilot

This is the closest domain precedent. Its first page already visually communicates the system workflow; the system description emphasizes the actual interaction process, transparency, and expert-oriented use. It has substantial technical detail and a 50-expert evaluation. ([ACL Anthology][3])

**Lesson:** a domain-specific agricultural advisory demo is unquestionably within the demonstrated tradition of the track. A user study can strengthen such a paper, but it is not the only acceptable evidence.

### DialogGuard

DialogGuard is particularly relevant for safety. It makes the system interface, safety dimensions, system comparison, evaluation and practitioner-facing workflow all part of the contribution. It has both benchmark results and a small practitioner study. ([ACL Anthology][4])

**Lesson:** safety-focused demonstrations are accepted as systems when the actual tool and user workflow are concrete. Evaluation is there to substantiate the tool; it is not necessarily the paper's primary identity.

### FactSearch

FactSearch is a particularly useful precedent for KrishokTech. It is only 7 pages in the published version, has a clear system workflow, an inspectable web interface, local/API deployment options, and evaluation directly tied to the tool's purpose. ([ACL Anthology][5])

**Lesson:** a focused demo can make a strong contribution with a small number of well-connected experiments.

### EACL 2026 Verification Assistant

The EACL 2026 browser-based Verification Assistant is close to your multimodal/verification framing. It emphasizes an accessible interface integrating several NLP services and puts the system workflow into a figure rather than treating every backend component as a separate research contribution. ([ACL Anthology][6])

### OpenGlass

OpenGlass combines architecture, local-first deployment, privacy, latency, safety-aware abstention, logs, and real deployment evidence. The authors explicitly frame it as a **reference platform**, not a certified safety system. ([ACL Anthology][7])

**Lesson:** your own instinct to state boundaries and limitations is correct.

### RAGVUE and BanSuite

RAGVUE is a useful modern precedent for an inspectable RAG-oriented system demo, while BanSuite is especially relevant because it shows that a substantial Bangla NLP system can be presented as a software platform rather than as a narrowly defined benchmark paper. ([ACL Anthology][8])

---

# 3. STEP 3 — Track fit

## A. Is KrishokTech recognizably a SYSTEM DEMONSTRATION?

**Yes — strongly.**

The paper does not merely describe a hypothetical architecture. It has:

* a live system;
* a screencast;
* an installation package;
* a defined audience;
* a complete end-to-end interaction;
* screenshots;
* explicit system states;
* multilingual/multimodal input;
* delivery channels;
* measurable system behavior.

The S1–S5 sequence is particularly good because the demonstration is a **single farmer session** rather than a collection of unrelated feature showcases.  

### Reviewer reaction

> “I understand what I would actually see at the demo.”

That is exactly what you want.

---

## B. Does the system appear substantial enough?

**Yes.**

The architecture is not just "Bengali RAG + UI." It includes explicit safety/information/crop/verification control points, a local vision component, evidence fencing, a dosage verifier, multiple delivery modes, and human referral. 

This is more than enough system substance for the track.

---

## C. Does the paper spend too much time behaving like a main-track paper?

**Moderately, but this is a presentation issue rather than a fundamental mismatch.**

The main six pages contain three major mechanism evaluations, multiple numerical comparisons, the cloud/local safety split, vision accuracy, contradiction detection, expert evaluation, delivery constraints, and several implementation claims. 

That is not forbidden. In fact, the CFP explicitly permits benchmark and expert evidence. ([EACL 2027][1])

The problem is the **distribution of attention**.

The reader can come away thinking:

> “This is a benchmark paper with a demo attached.”

instead of:

> “This is a demonstrable agricultural advisory system whose design is validated by targeted experiments.”

That is an important distinction.

### My inference

The paper does not need fewer *credible results* so much as fewer *independent stories*.

---

## D. Is the demonstration sufficiently clear?

**Yes, with two small semantic problems.**

S1→S5 is excellent.

The only issue is that **S5 calls the interaction “DROP” even though an answer is still shown**. The system is actually dropping an unsupported claim/sentence, not necessarily dropping the whole turn. 

A reviewer could briefly wonder:

> “Why is the delivered answer in a DROP state?”

One clarifying sentence would eliminate this.

---

## E. Is the intended audience clear?

**Yes.**

You explicitly say the demonstration is for researchers and practitioners building multilingual, multimodal, or safety-critical conversational systems. 

That is better than vague "for farmers and researchers."

---

## F. Is it accessible enough?

**Probably, with a verification caveat.**

The paper gives:

* live demo;
* video;
* installable package;
* screenshots;
* translated Bengali example;
* sample-query entry points.  

So I would not call accessibility a current rejection-level problem.

But you **must personally verify the endpoints** before submission because the CFP treats missing/broken demo/video access as a serious procedural issue, and I could not certify your endpoint from this environment.

---

# 4. STEP 4 — Novelty audit

Here is how I would decompose the novelty in an actual review.

| Novelty layer                  | Reviewer assessment                     | Why                                                                                                                                        |
| ------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Domain novelty                 | **Application-specific**                | Bengali agricultural advisory is important, but agricultural conversational systems already exist                                          |
| Language/resource novelty      | **Meaningful but not sufficient alone** | Colloquial Bengali/Banglish and regional variation matter, but Bengali agricultural systems already exist                                  |
| System/architecture novelty    | **Strongest part**                      | Explicit control stages constrain what later stages may do                                                                                 |
| Safety/control novelty         | **Useful integration of known ideas**   | Deterministic gating, crop scoping, and verification are individually familiar; their enforceable combination is the stronger contribution |
| Interaction/demo novelty       | **Meaningful**                          | ASK/CONFIRM/REFER/DROP plus visible provenance/Why behavior makes the controls user-facing                                                 |
| Engineering/deployment novelty | **Useful engineering contribution**     | On-device vision, offline/SMS/read-aloud and local deployment are valuable, but shouldn't carry the main novelty claim                     |
| Evaluation novelty             | **Supporting**                          | Banglish red-teaming and paired multimodal stress testing are useful; they are not the core contribution by themselves                     |

## The SINGLE strongest distinctive contribution

A skeptical reviewer is most likely to find this:

> **KrishokTech turns uncertainty and verification into enforceable, farmer-visible control states at multiple boundaries of an agricultural conversational pipeline: before retrieval, when modalities disagree, and before a generated safety-critical claim is rendered.**

That is stronger than saying:

> "We use Bengali + agriculture + multimodal + RAG + safety."

Those are ingredients, not the central contribution.

Your own text is already close to this idea: the same architecture decides when not to retrieve and when not to render. 

### What should NOT be presented as novelty

Do not sell these as standalone contributions:

**BM25:** standard.

**ONNX crop classifier:** engineering implementation.

**LoRA fine-tuning:** standard.

**4-bit quantization:** engineering.

**SMS compression:** useful deployment functionality.

**Offline cached cards:** useful deployment functionality.

**Regional dialect presets:** meaningful localization, but not a standalone NLP-method novelty claim.

**Six-crop coverage:** scope, not novelty.

**Human referral:** important safety functionality, not novel by itself.

**Provenance badges:** a good interaction/design element; useful as part of the integrated system.

---

# 5. The biggest novelty-positioning problem: “first system”

Your paper says:

> “To our knowledge, KrishokTech is the first system…”



I would remove **“first.”**

The reason is not that your integration is uninteresting. It is that the support underneath the claim is not strong enough for a priority claim.

Table 1 itself says:

> “Not described” does not mean the system lacks the mechanism.



That creates an internal logical problem:

> You cannot use absence from a paper description as strong evidence of being the first system to implement something.

A skeptical reviewer will notice this immediately.

### Minimal fix

Claim:

> **the combination/integration**, not historical priority.

That makes the novelty defensible without weakening the system story.

---

# 6. STEP 5 — Related-work positioning

## What you already have right

The current related work covers the right conceptual neighborhoods:

* agricultural conversational systems;
* Bengali agricultural systems;
* evidence-grounded agriculture;
* multimodal contradiction;
* abstention;
* clarification;
* safety-critical dialogue.

That is a good conceptual map. 

My Climate CoPilot is correctly used as the closest evidence/transparency neighbor, and your distinction between expert-visible evidence trace and automatic claim verification is useful. ([ACL Anthology][3])

## What is missing

The missing category is **recent system-demonstration/tooling work around inspectability and verification**.

I would add, very compactly:

* **FactSearch** — interactive, inspectable claim-level verification;
* **RAGVUE** — diagnostic/inspectable RAG evaluation;
* optionally the **EACL 2026 Verification Assistant** — accessible multimodal/content verification.

These are relevant because they help you position KrishokTech as a **system with inspectable control behavior**, not just an agricultural application. ([ACL Anthology][5])

I would **not** add a new large related-work subsection. One compact paragraph is enough.

## LocalRQA

LocalRQA is useful as a **precedent**, but I would not make it one of your primary domain comparisons.

Its contribution is a reusable RQA development toolkit; KrishokTech is an application/system with safety-oriented control semantics. The connection is methodological/systemic, not domain-specific. ([ACL Anthology][2])

That distinction actually strengthens your paper.

---

# 7. Related-work claims I would narrow

This sentence is too broad:

> “Most work on retrieval safety, clarification, and prompt-injection defense is developed and evaluated on high-resource, Latin-script English…”



A reviewer could reasonably challenge that generalization.

The point you need is narrower:

> **The particular combination of safety control, clarification, multimodal contradiction handling, and agricultural verification has been much less explored in colloquial Bengali.**

That is both more defensible and more directly relevant.

Likewise, the exact prior dense-retrieval result:

> R@10 0.970 → 0.093

is not doing enough work in this paper. 

Because the demonstrated system is BM25-only and explicitly says dense retrieval was not evaluated, the exact prior benchmark result pulls the reader toward a different research story. 

I would retain the **problem motivation**, but not make that number a central part of this paper's identity.

---

# 8. STEP 6 — Demonstration-quality audit

## S1–S5 is one of the paper's strongest assets

The sequence is logically progressive:

**S1** establishes why retrieval must halt.

**S2** establishes why visual crop identification matters.

**S3** demonstrates actual cross-modal disagreement.

**S4** demonstrates terminal safety referral.

**S5** demonstrates claim-level verification.



That is excellent system-demo design because each stage introduces a failure mode that motivates the next control.

### One thing I would change

Do not make the audience infer the role of each step from the prose.

A compact sentence at the beginning of Section 4 could state:

> Each step demonstrates one control boundary; S1/S3/S4/S5 correspond directly to ASK/CONFIRM/REFER/DROP, while S2 establishes the visual context required by S3.

You already say almost this; it just needs to be maximally obvious.

---

# 9. Figure 1: current paper problem

There is a genuine consistency issue.

The manuscript repeatedly defines **five stages T0–T4**. 

But the current figure visually has **six numbered processing boxes**, including a separate delivery box. The caption still says five stages. 

### Minimal fix

Make the conceptual structure explicit as:

**T0 Safety → T1 Information → T2 Crop Fence → T3 Draft → T4 Verify → Delivery**

Then make **Delivery unnumbered**.

This is important because it resolves your control-state terminology cleanly.

### Important note about the replacement figure we just generated

**Do not insert that generated figure unchanged.**

Its visual design is clearer, but it currently combines some stage semantics differently from the manuscript—specifically, it puts “Draft & Verify” together and makes T4 “Deliver,” whereas the paper defines T3 as draft, T4 as verification, followed by delivery. That would create a new inconsistency.

The **visual style is good; the labels need to be synchronized with the paper.**

---

# 10. STEP 7 — Evaluation audit

This is where I think the most valuable editorial work remains.

## Main evaluation

| Experiment/result                             | Reviewer question answered                                             | Classification                                 | Action                               |
| --------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------ |
| 200 authentic farmer queries; 30 crop-less    | Does C1 actually stop underspecified treatment requests?               | **Essential**                                  | Keep in main                         |
| Dual annotation / κ=1.00                      | Are the C1 labels trustworthy?                                         | **Useful supporting evidence**                 | Keep briefly                         |
| LLM gate 10% vs deterministic 15%             | Is deterministic gating preferable to a live LLM decision?             | **Interesting but nonessential**               | Appendix                             |
| 4,294 held-out crop images                    | Is the visual router capable enough to support crop fencing?           | **Useful supporting evidence**                 | Keep one concise sentence/table      |
| 400-query crop-fence stress set               | Does crop conditioning reduce off-target evidence?                     | **Essential**                                  | Keep in main                         |
| 454 text-image contradictions                 | Does the mismatch control catch explicit conflicts?                    | **Essential supporting evidence**              | Keep in main                         |
| 420 cloud safety calls                        | Do controls reduce unsafe output under the benchmark threat model?     | **Essential**                                  | Keep                                 |
| 280 deployed-model calls                      | Does the actual local model behave similarly?                          | **Essential**                                  | Keep, and arguably emphasize more    |
| 118 inserted dosage errors / 38 live answers  | Can the verifier catch controlled dosage mutations?                    | **Essential**                                  | Keep                                 |
| 528-case scaled dosage benchmark              | Does the verifier generalize beyond the 38 live answers?               | **Useful supporting evidence**                 | Keep concise; appendix details       |
| 50-session / 47 guarded expert audit          | Does the delivered output look agronomically safe to human evaluators? | **Essential supporting evidence**              | Keep, but don't overclaim            |
| 100 Banglish/phonetic red-team                | Does the safety gate handle language-specific evasion?                 | **Highly useful**                              | Promote                              |
| 3,000-query routing probe                     | What is the broader routing safety envelope?                           | **Interesting, but potentially distracting**   | Appendix only                        |
| SMS 100-case comparison                       | Does deterministic compression preserve critical content?              | **Useful supporting evidence**                 | Appendix                             |
| Offline retrieval under simulated packet loss | Does offline mode remain operational under degraded network?           | **Useful supporting evidence**                 | Appendix                             |
| 400-case latency breakdown                    | Is control overhead low?                                               | **Useful supporting evidence**                 | One number in main, details appendix |
| Installation footprint                        | Is deployment lightweight?                                             | **Useful**                                     | One line or appendix                 |
| Modeled cost per 1,000 turns                  | Is the system cheaper?                                                 | **Distracting**                                | Appendix or remove                   |
| Token metering                                | How much context/token overhead is used?                               | **Nonessential**                               | Appendix                             |
| INT8 quantization details                     | Is footprint optimization practical?                                   | **Nonessential for core story**                | Appendix                             |
| 100 trace-ordering cases                      | Are event traces properly ordered?                                     | **Low submission value**                       | Appendix or remove                   |
| 1,000 PRISM conformance queries               | Does it align with PRISM?                                              | **Potentially harmful/confusing**              | Remove unless externally required    |
| Exploratory 14-row answer review, 7/14        | Does answer quality look good?                                         | **Potentially harmful and unfinished-looking** | Remove from paper                    |

The most important principle here is:

**Do not remove a weak result merely because it is weak. Remove it when it does not answer an important reviewer question.**

That distinction matters for your safety results.

For example, the local guarded ASR of **10.71%** is worse-looking than the cloud result of **0.95%**, but it is essential because it describes the actual deployed model boundary. 

By contrast, a 14-row exploratory answer review that you explicitly call descriptive and non-conclusive does not establish much. It mainly tells the reviewer that some manual scoring is unfinished. 

**That one should go.**

---

# 11. The C2 evaluation problem is genuinely important

Current wording:

> “A query yields wrong-crop advice when its top five sources include a document for another crop.”



That is not actually a definition of **wrong-crop advice**.

It is a definition of **off-target retrieval/source contamination**.

Then the paper uses:

> “wrong-crop advice 36.25% → 28.75%”

which makes the result sound like answer-level correctness. 

This is probably the **single most important technical wording issue** in the manuscript.

### Reviewer objection

> “Your metric measures whether irrelevant crop documents appear among retrieved sources, but you call it wrong-crop advice. Did you actually assess the generated answer?”

That is a completely reasonable objection.

### Minimal fix

Rename the quantity consistently as:

**off-target crop retrieval**

or

**off-target crop evidence in top-5 retrieval**

Then reserve "wrong-crop advice" for cases where the final answer itself was evaluated.

This would materially improve the paper's credibility.

---

# 12. Safety evaluation: strong, but present it as a boundary, not a certification

The strongest C3 result is impressive within its stated test condition:

* cloud: 36.19% → 0.95%;
* deployed local model: 52.5% → 10.71%;
* Bengali-native local subset: 77.0% → 19.0%. 

The paper appropriately reports residual failures and later says the controls do not eliminate unsafe output. 

So I would **not** weaken this result unnecessarily.

I would instead make one conceptual adjustment:

### The system's primary safety result should be the deployed model

The cloud result is useful because it shows the controls are not dependent on the local model alone.

But a reviewer seeing the paper's headline result may otherwise think:

> “The paper claims a 0.95% safety-failure rate for the system.”

when the deployed system actually reports 10.71%.

That distinction matters.

### Recommendation

In the main paper:

**Primary:** deployed-model 10.71% guarded ASR.

**Secondary:** cloud-model 0.95% guarded ASR.

This makes the paper more credible, not less impressive.

---

# 13. Dosage verifier: another place where precision matters

The paper is careful in some places to say the verifier handles numerical dosage statements, not unrestricted agronomic factuality. 

Keep that limitation.

Because the scaled benchmark catches only **84.6% overall mutation cases**, including substantially lower detection for unit substitutions and invented PHIs, a reviewer could reasonably ask:

> “What exactly does ‘verified’ mean?”

The answer should be very narrow:

> **numerical dosage claims are checked against evidence and permitted dose bands**

not:

> **the answer is fully agronomically verified.**

That distinction is already present in your limitations; it simply needs to remain equally sharp in the main positioning. 

---

# 14. The paraquat problem

This is the most important factual issue I found outside the paper.

Your S4 says:

> “paraquat, a banned pesticide.”



The current Bangladesh Department of Agricultural Extension material I checked does **not support that unqualified statement**. The DAE has a registered agricultural-pesticide list containing paraquat products, including a product whose active ingredient is listed as Paraquat, while the DAE separately publishes a list of cancelled pesticides. ([Department of Agricultural Extension][9])

Therefore I would **not leave the current sentence unchanged**.

### Minimal safe fix

Do not invent a new legal interpretation.

Either:

**A.** use an active ingredient/product you can verify from the DAE's cancelled list as the demonstration example, or

**B.** describe the system as **blocking a restricted/high-risk pesticide request under its safety policy**, without claiming that paraquat is legally banned.

This is exactly the kind of small factual issue that can have disproportionate impact in a safety-critical paper.

---

# 15. STEP 8 — Most plausible reviewer objections

Here is the reviewer's likely objection set.

| Objection                                                                                 | Likelihood                                     | Severity              |
| ----------------------------------------------------------------------------------------- | ---------------------------------------------- | --------------------- |
| “The C2 metric is retrieval contamination, not wrong-crop advice.”                        | **Likely**                                     | **Major but fixable** |
| “The manuscript calls paraquat banned without sufficient regulatory support.”             | **Likely**                                     | **Major but fixable** |
| “The ‘first system’ claim is stronger than the comparative evidence supports.”            | **Likely**                                     | **Major but fixable** |
| “The cloud safety result is more favorable than the actual deployed model result.”        | **Likely**                                     | **Major but fixable** |
| “The paper contains too many experiments for a system demo.”                              | **Plausible**                                  | Moderate              |
| “Why are PRISM/14-row/internal evaluation results here?”                                  | **Plausible**                                  | Moderate              |
| “The system is broad enough that its central contribution is difficult to isolate.”       | **Plausible**                                  | Moderate              |
| “No farmer user study means usefulness is not established.”                               | **Plausible**                                  | Minor–moderate        |
| “Human evaluation is small and only three raters.”                                        | **Plausible**                                  | Moderate              |
| “The system verifies dosage claims, but not general agronomic correctness.”               | **Likely**                                     | Moderate              |
| “Figure 1 says five stages but depicts six boxes.”                                        | **Likely**                                     | Minor                 |
| “DROP seems to mean the whole answer was rejected, but an answer is still displayed.”     | **Plausible**                                  | Minor                 |
| “Licensing for derived BARI/BRRI/DAE content needs clearer provenance.”                   | **Plausible**                                  | Moderate              |
| “A non-Bengali reviewer may struggle to judge the actual linguistic content of the demo.” | **Possible**                                   | Minor                 |
| “Why isn't dense retrieval evaluated?”                                                    | **Unlikely as a rejection issue**              | Minor                 |
| “Why no field study?”                                                                     | **Plausible**, but not necessarily problematic | Minor–moderate        |

### The important one that I would NOT fear

> “There is no farmer user study.”

The current CFP explicitly says user studies are only one acceptable form of evidence and lists benchmarks, simulations, expert evaluation, usage statistics, case studies, and qualitative feedback as alternatives. ([EACL 2027][1])

Your paper has several of those.

So I would **not** launch a rushed farmer study now.

---

# 16. Scope/breadth risk

The paper currently presents all of these:

Bengali + colloquial/dialectal input + Banglish + crop vision + multimodal conflict + RAG + deterministic gate + dosage verification + safety red-teaming + local LLM + cloud LLM + SMS + offline + read-aloud + provenance + human referral.

That is substantial.

It can be read in two ways.

### Positive reading

> “This is a real deployed agricultural advisory system with multiple carefully designed safety boundaries.”

### Negative reading

> “This is a feature collection containing several individually modest engineering modules.”

Your job is to make the first reading unavoidable.

The way to do it is **not** by adding more technical detail.

It is by repeatedly organizing the paper around one sentence:

> **Every component exists to control what evidence or action the system is allowed to take under uncertainty.**

That is the system identity.

---

# 17. STEP 9 — Practical submission risk

| Risk                                  | Level             | Reviewer reasoning                                                                                                                                                    |
| ------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Track-fit risk**                    | **LOW**           | This is very clearly an actual system demonstration; the CFP explicitly welcomes application systems, reusable components, and systems without LLMs. ([EACL 2027][1]) |
| **Novelty-positioning risk**          | **MODERATE–HIGH** | Core integration is defensible, but “first” and the feature-comparison table overstate what has been established                                                      |
| **Technical-validity risk**           | **MODERATE–HIGH** | C2 metric semantics and regulatory wording need correction                                                                                                            |
| **Evaluation risk**                   | **MODERATE**      | Evidence is plentiful; the problem is fragmentation and a few potentially distracting results                                                                         |
| **Demonstration risk**                | **LOW–MODERATE**  | S1–S5 is strong; stage semantics and S4 wording need cleanup                                                                                                          |
| **Presentation risk**                 | **MODERATE**      | Main paper is dense and slightly research-report-like, but figures/screenshots are useful                                                                             |
| **Availability/reproducibility risk** | **MODERATE**      | Required links are present, but endpoint/package functionality and release/licensing must be checked manually                                                         |
| **Ethics/safety risk**                | **MODERATE–HIGH** | High-stakes agricultural advice raises the bar; fortunately the paper already documents consent, de-identification, residual failures, privacy and human referral.    |

## The 5 issues that could realistically prevent acceptance if left unchanged

### 1. C2 “wrong-crop advice” terminology

This is the clearest technical claim/evidence mismatch.

### 2. Paraquat/regulatory wording

A safety-critical paper should not contain a questionable regulatory fact in its central demonstration scenario.

### 3. Overclaiming novelty

The “first system” sentence plus “Not described” table creates unnecessary skepticism.

### 4. The paper looks partly like a benchmark report

Especially because of the large appendix ledger, internal experiment IDs, PRISM conformance, exploratory 14-row result, cost model, token accounting, and multiple deployment micro-benchmarks.

### 5. Artifact/license verification

EACL 2027 makes the live demo/package mandatory. ([EACL 2027][1])
If the actual demo, screencast, or package does not work for a reviewer, that is dramatically more serious than any prose issue.

---

# 18. Source/PDF consistency problem

I found one very concrete submission-hygiene issue.

The submitted PDF title is:

> **KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory** 

The current `main.tex` source instead contains:

> **KrishokTech: A Safe, Multimodal System Demonstration for Bengali Agricultural Advisory** 

That needs to be synchronized before submission.

This is not an argument about which title is better. It is a **version-control problem**.

The same source also contains comments about restoring a public repository URL for camera-ready, while the current EACL track is single-blind and does not require author anonymity.  ([EACL 2027][1])

The essential issue is simpler:

> **The PDF, source, demo, and repository must all describe the same revision.**

---

# 19. Availability and licensing

The manuscript does several good things:

* live demo;
* screencast;
* source/package;
* Apache-2.0 code;
* model and knowledge-node release information;
* local deployment information. 

But I would check one thing carefully:

> **Does every released agricultural knowledge artifact actually have the license you claim for it?**

The source says the `krishokchat-4b` model and 2,135 extension nodes are on Hugging Face under CC-BY-4.0, while the code/container is Apache-2.0. 

A reviewer may reasonably ask whether:

* the license covers your **derived nodes**;
* it covers the original BARI/BRRI/DAE material;
* the package redistributes source text or only derived representations.

You do not need a long legal discussion. You do need an unambiguous release boundary.

---

# 20. Ethics and safety: this is actually a strength

I would not cut the ethics section.

You have unusually useful details:

* farmer queries are de-identified;
* names/phones/locations removed;
* ethics review and consent reported;
* images remain on-device;
* cloud calls do not receive farmer images;
* residual safety failures are openly reported;
* human referral is part of the system boundary. 

This is exactly the kind of documentation the current CFP asks authors working with sensitive tasks/data to provide. ([EACL 2027][1])

I would, however, remove the exact 16123 operating hours unless you have a current authoritative source for those hours. They are operational information that can change, and I did not find a sufficiently current official source in this check to certify that exact schedule.

---

# 21. What I would KEEP

**Keep the control-state architecture.** This is the paper's identity.

**Keep S1–S5.** It is the strongest demonstration narrative.

**Keep the 200 authentic farmer-query gate evaluation.** It directly validates ASK behavior. 

**Keep the crop-fencing stress evaluation.** Rename the metric precisely. 

**Keep the deployed-model safety result.** It is essential evidence for the actual system. 

**Keep the dosage verifier evaluation.** It directly tests one of the system's central claims. 

**Keep the Banglish/phonetic safety test.** This is one of the strongest pieces of evidence connecting the system design to the Bengali user context. 

**Keep the human expert audit.** Small, but useful as independent validation. 

**Keep the limitations.** The paper's explicit statement that it has no field study and that safety controls do not eliminate risk is credibility-positive. 

**Keep the ethics/privacy section.**

---

# 22. What I would REMOVE or DE-EMPHASIZE

### Remove from the main paper

The **“first system”** claim.

The **Table 1 “Not described” feature-comparison table**, or replace it with a short prose positioning paragraph.

The exact prior dense-retrieval number in the Introduction.

The **14-row exploratory answer review**.

The **PRISM conformance numbers** unless PRISM is actually important to the system story.

### Keep only in appendix

Token metering.

Modeled cost.

Detailed INT8 results.

Full SMS comparison.

Detailed offline packet-loss experiments.

Trace-ordering tests.

The LLM-vs-deterministic gating micro-comparison.

Full 3,000-query safety-envelope analysis.

Internal identifiers such as **N14, E50, N05c** unless they serve a real reproducibility purpose.

### Why?

Not because these results are bad.

Because they answer increasingly narrow engineering questions after the central system has already been convincingly established. That makes the manuscript look more like an **evaluation dossier** than a demo paper.

---

# 23. What I would PROMOTE

### 1. Promote the integrated control architecture

This should become the unmistakable center of the paper.

Not:

> “three safety techniques.”

But:

> **an enforceable sequence of control states that bounds retrieval, modality agreement, generation, and rendering.**

### 2. Promote the actual deployed model result

Do not let the paper's best cloud number become its perceived safety guarantee.

### 3. Promote Banglish robustness

This is unusually well connected to your stated Bengali deployment context.

### 4. Promote the live interaction

The paper should make the reader think:

> “I know exactly what I am going to see at the demo.”

### 5. Promote inspectability

The provenance badge + Why panel is an unusually useful bridge between backend verification and user-facing behavior. Your paper has something concrete here that pure benchmark papers do not.

---

# 24. What the paper is currently trying to be

**Right now it is simultaneously trying to be:**

1. a Bengali agricultural advisory application;
2. a safety/control architecture paper;
3. a multimodal RAG paper;
4. a verification paper;
5. a deployment/edge-computing report;
6. a safety benchmark paper;
7. a systems demonstration.

All seven descriptions are technically defensible.

But the combination creates the biggest presentation risk.

---

# 25. What it should most clearly be perceived as

The reviewer should leave with:

> **“KrishokTech is a deployable Bengali agricultural advisory system whose key design contribution is an explicit, enforceable control pipeline that makes uncertainty visible and prevents unsafe or unsupported evidence from silently becoming advice.”**

Everything else should support that sentence.

The domain is the setting.

The Bengali/colloquial issue is the deployment constraint.

The multimodal component is one control boundary.

The verifier is another control boundary.

The SMS/offline/local pieces establish practical deployability.

The experiments validate those boundaries.

That is a much cleaner systems-demo identity.

---

# 26. Minimum revision set before submission

I would stop editing once these are done:

### A. Fix the C2 metric terminology

**Submission-critical.**

Replace “wrong-crop advice” with the actual measured quantity unless you have an answer-level annotation behind it.

### B. Fix the regulatory example

**Submission-critical.**

Do not call paraquat legally banned unless you have authoritative current evidence supporting exactly that claim.

### C. Remove “first system”

**Submission-critical.**

Frame novelty as the integration/enforcement of the controls.

### D. Make the cloud/local boundary explicit

**Submission-critical.**

The deployed model result should be visibly distinct from the cloud benchmark.

### E. Fix Figure 1 semantics

**Submission-critical.**

Five T0–T4 stages, then delivery.

### F. Move Figure 1 earlier if feasible

**High-value, contained.**

Recent demos often make the core system workflow visible very early; LocalRQA and My Climate CoPilot are strong examples. 

Removing/reducing Table 1 would make this easy without increasing page count.

### G. Remove the 14-row exploratory result and PRISM block

**High-value, contained.**

They contribute little to the core demo story and create unnecessary reviewer questions.

### H. Add one compact sentence positioning against FactSearch/RAGVUE/Verification Assistant

**High-value, contained.**

No new subsection.

### I. Verify the live demo, screencast, package and OpenReview entries externally

**Submission-critical.**

The CFP explicitly makes the live artifact and video mandatory. ([EACL 2027][1])

### J. Synchronize PDF/source/title/assets/license claims

**Submission-critical.**

---

# Final decision table

| Issue                                                | Location                  |           Severity | Why it matters to a demo reviewer                               | Evidence                                                          | Fix before submission? | Minimal fix                                                                   |
| ---------------------------------------------------- | ------------------------- | -----------------: | --------------------------------------------------------------- | ----------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------- |
| C2 calls retrieval contamination “wrong-crop advice” | §5.2, Table 2, Appendix B |           **High** | Claim exceeds measurement                                       |                                                                   | **Yes**                | Rename metric to off-target retrieval/evidence                                |
| Paraquat called “banned”                             | S4, §3.1, ethics          |           **High** | Central safety example may be factually/regulatorily inaccurate |  ; DAE list ([Department of Agricultural Extension][9])           | **Yes**                | Use verified cancelled example or neutral “blocked high-risk request” wording |
| “First system” novelty claim                         | Related Work              |           **High** | Evidence cannot establish priority                              |                                                                   | **Yes**                | Claim integrated combination, not “first”                                     |
| “Not described” comparison table                     | Table 1                   |  **Moderate–High** | Invites fairness/absence objections                             |                                                                   | **Yes**                | Replace with prose positioning                                                |
| Cloud result dominates perceived safety claim        | Abstract/§5.3             |           **High** | Cloud ≠ deployed demo                                           |                                                                   | **Yes**                | Lead with deployed result, cloud as secondary benchmark                       |
| Five stages vs six boxes                             | Figure 1                  |       **Moderate** | Internal architecture inconsistency                             |                                                                   | **Yes**                | T0–T4 + unnumbered delivery                                                   |
| DROP semantics unclear                               | S5                        |   **Low–Moderate** | User-visible behavior may be misunderstood                      |                                                                   | Preferably             | State that unsupported claims are dropped, not necessarily the whole answer   |
| Main paper feels benchmark-heavy                     | §§5–6                     |       **Moderate** | Dilutes demo identity                                           |                                                                   | **Yes, contained**     | Move/remove secondary experiments                                             |
| 14-row exploratory review                            | Appendix A                |       **Moderate** | Looks unfinished; low evidentiary value                         | Appendix inspection                                               | **Yes**                | Remove                                                                        |
| PRISM conformance block                              | Appendix A                |       **Moderate** | Confusing and contains weak scores unrelated to main story      | Appendix inspection                                               | **Yes**                | Remove unless genuinely central                                               |
| Missing recent system-demo neighbors                 | Related Work              |       **Moderate** | Weakens system-demo positioning                                 | FactSearch/RAGVUE/Verification Assistant ([ACL Anthology][5])     | Yes                    | One compact positioning sentence                                              |
| No farmer user study                                 | Evaluation                |   **Low–Moderate** | Usefulness is not field-validated                               | Current limitations ; CFP accepts other evidence ([EACL 2027][1]) | **No**                 | Keep limitation                                                               |
| Small expert audit                                   | §5.3                      |       **Moderate** | Limits generalization                                           |                                                                   | No major change        | Keep as bounded evidence                                                      |
| License provenance of knowledge nodes                | Availability/source       |       **Moderate** | Reviewer may question redistribution rights                     |                                                                   | **Yes**                | State exact code/data/model release boundaries                                |
| PDF/source title mismatch                            | PDF vs `main.tex`         |       **Moderate** | Version-control/submission hygiene                              |                                                                   | **Yes**                | Synchronize and recompile                                                     |
| Demo/video/package endpoints                         | PDF/OpenReview            | **High if broken** | Mandatory under CFP                                             | ([EACL 2027][1])                                                  | **Yes**                | Test externally and duplicate exact URLs in OpenReview                        |

---

# Bottom line

### KEEP

The **five-control architecture**, S1–S5 narrative, provenance/Why behavior, deployed safety result, C1/C2/C3 core validation, Banglish red-teaming, human audit, limitations, ethics, and live artifacts.

### REMOVE / DE-EMPHASIZE

“First system,” the “Not described” table, exact dense-retrieval motivation number, 14-row exploratory evaluation, PRISM conformance, modeled cost, token metering, trace-ordering, most INT8/SMS micro-results, and internal experiment IDs.

### PROMOTE

The **integrated control-state architecture**, the fact that the system is actually deployed locally, the user-visible ASK/CONFIRM/REFER/DROP behavior, the Bengali/Banglish safety context, and the inspectable provenance/verification experience.

### Minimum gap to close

You do **not** need an architectural redesign, a new dataset, or a rushed farmer study.

You need to make the current artifact say exactly what it demonstrates:

**a real, inspectable, deployable Bengali agricultural advisory system with explicit control boundaries—not a benchmark paper that happens to have a demo.**

That is the strongest reading of the existing artifact, and the current EACL 2027 CFP supports that positioning directly. ([EACL 2027][1])

[1]: https://2027.eacl.org/calls/demos/?utm_source=chatgpt.com "Call for System Demonstrations -"
[2]: https://aclanthology.org/2024.acl-demos.14/?utm_source=chatgpt.com "LocalRQA: From Generating Data to Locally Training, Testing, and Deploying Retrieval-Augmented QA Systems - ACL Anthology"
[3]: https://aclanthology.org/2025.acl-demo.7/?utm_source=chatgpt.com "My Climate CoPilot: A Question Answering System for Climate Adaptation in Agriculture - ACL Anthology"
[4]: https://aclanthology.org/2026.acl-demo.19/?utm_source=chatgpt.com "DialogGuard: Multi-Agent Psychosocial Safety Evaluation Interface of Sensitive LLM Responses - ACL Anthology"
[5]: https://aclanthology.org/2026.acl-demo.36/?utm_source=chatgpt.com "FactSearch: An Interactive Agentic Fact Search System for Verifying Large Language Model Outputs - ACL Anthology"
[6]: https://aclanthology.org/2026.eacl-demo.12/?utm_source=chatgpt.com "A Browser-based Open Source Assistant for Multimodal Content Verification - ACL Anthology"
[7]: https://aclanthology.org/2026.acl-demo.82/?utm_source=chatgpt.com "OpenGlass: A Sensing-Computing Split Architecture for Local MLLM-Driven Real-Time Visual Assistance - ACL Anthology"
[8]: https://aclanthology.org/2026.eacl-demo.35/?utm_source=chatgpt.com "RAGVUE: A Diagnostic View for Explainable and Automated Evaluation of Retrieval-Augmented Generation - ACL Anthology"
[9]: https://dae.gov.bd/sites/default/files/files/dae.portal.gov.bd/page/8a812db0_3544_4105_b066_df78074d3efb/Registered%20Agricultural%20PesticidesList%20%286%29.pdf?utm_source=chatgpt.com "List of Registered Agricultural Pesticides, Bio Pesticides and Public Health Pesticides in Bangladesh                                                                                                 Approved"
