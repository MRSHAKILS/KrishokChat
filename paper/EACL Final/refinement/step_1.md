I reviewed the manuscript as a **system-demonstration artifact**, not as a generic NLP research paper. I also checked the current EACL 2027 Demo CFP, the EACL 2026/ACL 2026/2025/2024 demo proceedings, and the closest comparison systems including **My Climate CoPilot, LocalRQA, DialogGuard, FactSearch, and OpenGlass**.

My main conclusion is operational: **do not add another major experiment or redesign the architecture before submission.** The highest-value work now is to fix a small number of credibility/consistency issues and tighten the paper around the system itself.

## 1. What the current EACL 2027 track actually asks for

The current official CFP is very favorable to what you are building, but it also gives you a very clear submission target:

* maximum **6 content pages**; extra space is available for ethics/broader impact, references, and informative appendices;
* a **live demo website or downloadable installation package is mandatory** this year;
* a **≤2.5-minute screencast** is required, with the link in both the PDF and OpenReview;
* at least one author must present the live demo and poster;
* one author must be nominated as a reciprocal reviewer;
* comprehensive experimentation is explicitly **not required**, but the paper must contain some evidence of prototype usefulness/quality; the CFP explicitly lists benchmarks, simulations, expert evaluation, usage statistics, case studies, and qualitative feedback as acceptable forms of evidence;
* the review criteria explicitly cover system/demonstration description, evaluation/availability/licensing, and presentation quality. ([EACL 2027][1])

The deadline is **22 September 2026, 11:59 pm UTC−12**, so this is genuinely a final-refinement situation rather than an opportunity for a new research cycle. ([EACL 2027][1])

### What recent accepted demos suggest — observed pattern, not a rule

Across the recent EACL/ACL demo volumes, there is **no single accepted-paper template**. The 2026 EACL and 2026/2025/2024 ACL volumes contain everything from research toolkits to domain applications, safety interfaces, multimodal systems, and deployment platforms. ([ACL Anthology][2])

Some particularly relevant examples:

* **My Climate CoPilot** is very close in application domain: evidence-grounded agricultural QA, transparency, privacy, and system-level interaction, with evaluation involving 50 domain experts. ([ACL Anthology][3])
* **LocalRQA** is useful as a system-paper precedent for treating training/testing/deployment infrastructure itself as the contribution rather than trying to turn every component into a separate research contribution. ([ACL Anthology][4])
* **DialogGuard** combines an actual usable interface, explicit safety auditing, explanatory output, evaluation, and a practitioner study. ([ACL Anthology][5])
* **OpenGlass** similarly makes system architecture, privacy, deployment constraints, measured latency, safety-aware behavior, and released artifacts part of the system story. ([ACL Anthology][6])
* **FactSearch** emphasizes configurability, transparent inspection, and a practical interactive interface rather than presenting the system as a collection of isolated algorithms. ([ACL Anthology][7])

So I would **not** try to make KrishokTech look like a 15-page research paper just because some older demo papers are long. The current EACL 2027 page limit is the controlling rule.

---

# 2. What the manuscript already does well

There is quite a lot here that I would deliberately preserve.

### A. The system has an actual demonstration narrative

The S1→S5 sequence is unusually coherent for a system paper. It demonstrates:

**ASK → crop-scoped evidence → CONFIRM → REFER → DROP**

rather than showing five unrelated features. The paper explicitly says the screencast follows the same sequence, and the examples cover all four farmer-visible states. 

That is exactly the sort of thing a demo reviewer can understand quickly.

### B. The control points are concrete and user-visible

The paper does not merely say "we add safety." It describes explicit points before retrieval, before generation, before rendering, and exposes their consequences to the user. 

The crop-mismatch behavior and Why panel are especially good demo material. The paper also gives a real public interface and screencast. 

### C. The evaluation is mapped to system failures

This is one of the strongest structural choices. C1, C2, C3 each has a corresponding failure mode and corresponding test rather than one generic "overall performance" table. The paper has evidence on gating, crop conflict, adversarial safety, dosage checking, and constrained delivery.  

### D. The limitations section is appropriately explicit

The manuscript openly says there is no field study, most contradiction cases are synthetic, the verifier covers numerical dosage claims rather than all agronomic facts, and the local model still has residual attack failures. 

That is good evidence discipline, and I would **keep it**.

### E. Ethics/privacy is not an afterthought

The paper documents de-identification, consent/ethics review, on-device image processing, and the cloud/local-model boundary. 

This is especially valuable for this track because the CFP explicitly says sensitive-data or sensitive-task papers need to address legitimate ethical concerns. ([EACL 2027][1])

---

# 3. A — Submission-critical: fix these before submitting

## A1. Synchronize `main.tex` and `main(2).pdf`

This is the first thing I would fix.

Your compiled PDF currently says:

> **KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory** 

But the uploaded `main.tex` contains:

> **KrishokTech: A Safe, Multimodal System Demonstration for Bengali Agricultural Advisory**

Those are clearly different title versions.

This is not merely cosmetic. It means the source and the submitted artifact are not demonstrably the same revision.

**Action:** decide which current title is intended, update the source, recompile, and inspect the newly generated PDF. Do not submit a PDF generated from one revision with a source repository containing another.

There is a second source-level warning: your TeX explicitly falls back to a **“Screenshot to be added”** placeholder if `s5_why_panel.png` is absent. 

The current PDF does contain the S5 image, so the PDF itself is fine; this is a **source-bundle integrity check**. Make sure the real screenshot and all figure assets are present in whatever repository/package you point reviewers to.

**Priority: A1 / highest.**

---

## A2. Correct the “banned pesticide / paraquat” claim

This is the most important factual correction I found outside the manuscript itself.

The paper currently describes paraquat as a **“banned pesticide”** and uses that as the S4 referral example. 

I could **not verify that paraquat is currently banned in Bangladesh**. More importantly, the Department of Agricultural Extension's published registered-pesticide list includes multiple paraquat products. ([Department of Agricultural Extension][8]) A July 2026 Bangladesh report also describes calls to ban paraquat, which is inconsistent with treating the chemical as already comprehensively banned. ([BSS][9])

So this should not be fixed merely by changing one adjective.

### What to do

Choose one of these two evidence-consistent paths:

**Path 1 — use a genuinely cancelled/prohibited active ingredient.**
Replace the demo example, screenshot text, attack cases, and relevant evaluation labels with an ingredient you can verify in the current DAE cancellation/regulatory records.

**Path 2 — keep paraquat as a system-blocked high-risk chemical, but stop calling it legally banned.**
Then explain that KrishokTech's **safety policy blocks the request irrespective of whether the active ingredient is legally registered**, and make that policy explicit.

I would not leave the current wording as-is.

This affects:

* Section 3.1;
* S4 in Section 4;
* Appendix C safety taxonomy;
* the safety benchmark terminology;
* any screenshot containing “banned”;
* the 16123 referral description.

**Priority: A2.**

---

## A3. Fix the “five stages” versus “six boxes” inconsistency

Your text repeatedly says there are **five pipeline stages, T0–T4**. 

But Figure 1 visually contains **six numbered boxes**: Safety Check, Information Gate, Crop Fence, Draft, Verify, and Deliver.

The sixth box is clearly delivery rather than another control stage.

That is actually easy to fix.

### Recommended formulation

Make the conceptual structure:

> **Five control stages (T0–T4), followed by delivery.**

Then visually make **Deliver** an unnumbered downstream output, or label the figure as:

> **Five control stages + delivery**

The current caption still says “Each of the five stages…” while the graphic visibly numbers six. 

This is exactly the kind of small inconsistency a reviewer can notice within seconds.

**Priority: A3.**

---

## A4. Fix the C2 metric terminology

This is the most important methodological wording issue in the evaluation.

The manuscript says:

> “A query yields wrong-crop advice when its top five sources include a document for another crop.”

But that definition is **not advice**. It is a retrieval/source-contamination condition.

The paper later reports:

> “Wrong-crop advice 36.25% → 28.75%”

even though the stated operational criterion is whether an off-target document appears in the top five. 

Unless you actually generated the answer and independently judged that answer as wrong-crop advice, the terminology is too strong.

### Change it everywhere

Use something like:

> **off-target retrieval**
> or
> **off-target crop evidence in top-5 retrieval**

Then Table 2 becomes:

> **Off-target retrieval: 36.25% → 28.75%**

And the abstract should no longer say that crop fencing reduced “wrong-crop advice” unless that is genuinely what was measured. 

This is not cosmetic. It aligns the claim with the actual measurement unit.

**Priority: A4.**

---

## A5. Balance the abstract's safety result

The abstract currently headlines the cloud result:

> 36.19% → 0.95% attack success

but the deployed local model reaches **10.71% guarded ASR**, with **19.0% on the Bengali-native subset**. 

The main paper does disclose the local result, so this is not hidden. But because the abstract is where reviewers form their first mental model of a safety system, reporting only the more favorable cloud result can create an avoidable impression.

### I would change only one sentence

Something along the lines of:

> “Across 420 cloud-model calls, guarded ASR fell from 36.19% to 0.95%; on the deployed local model, it fell from 52.5% to 10.71%.”

You do not need all the Bengali-subset detail in the abstract.

This also fits your own limitations section, which correctly acknowledges the local model boundary. 

**Priority: A5.**

---

## A6. Manually verify all three artifact links before submission

The CFP makes the demo website/package link a **strict desk-rejection requirement**, and the screencast link must be present in both the PDF and OpenReview. ([EACL 2027][1])

Your paper contains:

* live demo;
* screencast;
* anonymous source/install link. 

I attempted to validate those endpoints from my environment, but the network path here could not resolve them. **That does not mean the links are broken**; it means I cannot honestly certify them from this environment.

So before pressing Submit, personally test:

`krishoktech-one.vercel.app`

`krishoktech-one.vercel.app/screencast`

and the installation/package URL.

Do that from a browser/network outside this environment, preferably while logged out/incognito.

Also test the demo in the exact state shown in the screencast.

**Priority: A6.**

---

## A7. Do the reciprocal-reviewer and OpenReview checks

The current CFP explicitly requires one author to be nominated as a reviewer. ([EACL 2027][1])

Also make sure the **same demo URL, video URL, and package URL** appear in both:

1. the paper PDF, and
2. the OpenReview submission form.

This is administrative rather than scientific, but it is precisely the sort of thing that can cause an otherwise valid submission to fail before content review.

**Priority: A7.**

---

## A8. Make the boundary from your earlier KrishokChat/retrieval papers explicit

Your Related Work and Introduction cite your own 2026 papers on retrieval and safety. The current CFP has an explicit significant-overlap policy. ([EACL 2027][1])

The paper already has a distinct system story, but I would add **one sentence** making that boundary explicit:

> This paper is about the deployed advisory system and its enforceable control pipeline; the earlier works provide the retrieval/safety datasets and benchmark evidence rather than constituting the system contribution described here.

Only use that wording if it accurately reflects the actual prior papers.

The purpose is not to defend yourself preemptively; it is to make the **novelty boundary legible** to a reviewer who sees the same authors and related artifacts.

**Priority: A8.**

---

# 4. B — High-value but contained

## B1. Replace Table 1 with positive positioning

I would seriously reconsider the large comparison table on page 4.

The problem is not that comparisons are bad. The problem is that the table says things like:

> “Not described”

for competing systems while simultaneously adding the caveat that “Not described” does not mean the system lacks the mechanism. 

That leaves the table with an awkward evidentiary position:

* it looks like a capability comparison;
* but it explicitly says it is not independently tested;
* and some entries are based on what the cited papers did or did not describe.

That is unnecessary reviewer surface area.

### Better use of the same space

Turn the section into a short positive-positioning paragraph:

* Farmer.Chat / KrishokBondhu / Krishi Sathi establish localized agricultural conversational access;
* My Climate CoPilot establishes evidence-grounded agricultural QA and transparency;
* KrishokTech's distinction is that **crop omission, cross-modal disagreement, and unsupported dosage claims are explicit terminal control states in one pipeline**.

That is stronger because you are explaining **what your system does**, rather than implicitly making claims about what other systems don't do.

This is also closer to how My Climate CoPilot positions itself: it identifies closely related work and explains the particular system-level distinctions rather than relying only on a feature matrix. ([ACL Anthology][3])

**Priority: B1.**

---

## B2. Remove the “first system” superlative

This sentence:

> “To our knowledge, KrishokTech is the first system to combine…”

is vulnerable because the space is large and changing rapidly, while your comparison table is itself explicitly based on what prior papers describe. 

You do not need the word **first** to establish novelty.

Use a narrower contribution statement such as:

> “KrishokTech combines pre-retrieval halting, crop-conditioned evidence fencing, and pre-render dosage verification in one enforceable pipeline for colloquial Bengali agricultural advisory.”

That claims exactly what your paper demonstrates.

**Priority: B2.**

---

## B3. Shorten the C1 LLM comparison in the main paper

This is the paragraph where you report:

* deterministic gate = 15%;
* unconstrained LLM = 10%;
* 91% agreement;
* 4.2s latency.

The strongest result is actually much simpler: **the deterministic gate agrees with the human crop-presence labels while avoiding an LLM call, and all 30 crop-less treatment queries are stopped before retrieval.** 

The live-LLM comparison is not doing much for the system-demo story and invites questions about prompting, model selection, and why 10% vs 15% should matter.

Keep it in Appendix A.

In the 6-page paper, I would use those lines to reinforce the system behavior rather than introduce another miniature benchmark.

**Priority: B3.**

---

## B4. Trim the SMS/offline measurement paragraph

The main paper currently includes:

* 399/400 SMS messages within 160 chars;
* dose preservation 23/89/92;
* local-vs-remote retrieval under packet loss;
* 33.6 ms non-LLM overhead. 

Those are individually useful, but collectively they begin to turn the system demo into a deployment-engineering report.

The CFP does value accessibility and deployment, but the **demo itself already shows web, SMS, offline, and read-aloud delivery**. 

### Main-paper version

Keep perhaps:

> “Verified responses can also be delivered through SMS and an offline cached card; detailed delivery measurements are in Appendix D.”

Then leave the numerical delivery analysis in the appendix.

**Priority: B4.**

---

## B5. Separate “cloud evaluation” from “deployed demo” more explicitly

Section 3.3 currently says the deployed model is `krishokchat-4b` and that Gemini is used as the cloud benchmark throughout evaluation. 

That is technically understandable, but a reviewer can still ask:

> **“When I open the demo, which model am I actually interacting with?”**

Add one short sentence in either Section 3.3 or the Demonstration section that answers exactly that.

Do not add any model claim beyond what your actual deployment does; just make the boundary explicit.

This matters because the cloud model's 0.95% and the deployed model's 10.71% are materially different results.

**Priority: B5.**

---

## B6. Remove the implication that DialectSelector was shown to improve retrieval

The main text says:

> “A DialectSelector covers six regional presets to narrow the colloquial-to-formal retrieval gap…”

But the current system paper does not present a direct evaluation demonstrating that the selector itself narrowed that gap. 

Your previous retrieval work motivates the problem, but the current paper's evaluation does not establish an improvement attributable to DialectSelector.

Change this to a capability description:

> “A DialectSelector provides six regional presets for localized synonym expansion…”

That preserves the feature without implying an unmeasured effect.

**Priority: B6.**

---

## B7. Move the dense-retrieval result out of the center of the Introduction

The Introduction currently opens with the exact prior-paper result:

> R@10 0.970 on formal queries → 0.093 on colloquial queries. 

That is interesting, but your current deployed retrieval is BM25 and the limitations explicitly say dense retrieval was **not evaluated** in this system. 

So the exact numeric result creates an unnecessary conceptual fork:

> “Why is the paper emphasizing dense retrieval if the demonstrated system doesn't actually evaluate it?”

I would replace the number with:

> “Prior evaluation shows that retrieval can degrade substantially on colloquial farmer queries…”

Then let this paper focus on what KrishokTech does about the downstream uncertainty.

The exact R@10 values can remain in the cited prior paper.

**Priority: B7.**

---

# 5. C — Optional polish

These are not reasons to delay submission.

### C1. Reduce generic connective prose

A few lines sound more generic than the rest of the paper, especially phrases like:

> “Together, these systems establish…”

and

> “The underlying risk is not specific to agriculture…”

The system-specific writing is much stronger elsewhere.

Do not try to “humanize” the whole paper. Just replace a few broad transitions with concrete positioning.

This is polish, not a substantive concern.

### C2. Slightly increase Figure 2's visual emphasis if trivial

The three screenshots are useful and the captions do most of the explanatory work. The page is already readable, so I would **not** redesign the figure.

A tiny crop/scale improvement to make the critical UI element—the mismatch badge and Why panel—easier to see at normal PDF zoom would help, but only if it takes minutes.

### C3. Keep the appendix evidence ledger

Do **not** cut the appendix simply because there are many measurements.

It is doing a useful credibility job by distinguishing measured, simulated, pilot, and modeled components. The main paper explicitly points reviewers there. 

That is much better than cramming every detail into six pages.

### C4. Bibliography hygiene

I checked the citation keys in the TeX source: all cited keys resolve to entries in the `.bib`; there are five unused bibliography entries. That is not a submission problem, but deleting unused entries is harmless cleanup.

---

# 6. D — Do **not** attempt these now

This is important.

### Do not add a field study

The CFP explicitly says comprehensive evaluation is unnecessary, and it accepts benchmark results, simulations, expert evaluation, qualitative feedback, etc. as evidence. ([EACL 2027][1])

You already have:

* authentic farmer queries;
* controlled benchmarks;
* multimodal stress testing;
* adversarial testing;
* dosage mutation testing;
* human agronomic audit;
* deployment measurements;
* a live demonstration.

A rushed farmer study would add methodological risk rather than necessarily improving the demo paper.

The paper itself already says there was no field study and that adoption/yield effects remain unmeasured. 

Keep that limitation.

### Do not add dense retrieval experiments

Not before this submission. It would create a new research story around retrieval architecture and consume space that the demo paper needs for its actual system.

### Do not add another vision ablation

The existing 4,294-image evaluation and crop-fence stress test already establish why the visual component is there. 

### Do not add another safety benchmark just to increase numbers

The C3 section is already extensive. The main issue is **presentation and claim calibration**, not lack of measurements.

### Do not redesign the architecture

The five-control-stage concept plus explicit interaction states is already a coherent system identity.

---

# 7. My recommended final six-page structure

I would keep the current broad structure rather than rebuild the manuscript:

**Page 1:** Abstract + Introduction
**Page 2:** compact Related Work/Positioning + start System Design
**Page 3:** architecture + System Design
**Page 4:** Demonstration + screenshots
**Page 5:** C1/C2 evaluation
**Page 6:** C3 + limitations + availability/conclusion
**Page 7 onward:** ethics, references, appendices

That already fits the current CFP's 6-page rule, and your current PDF does appear to put the ethics statement after the six content pages.  

I would **not** spend the remaining space expanding Related Work or adding another experimental table.

---

# 8. The exact editing order I would use tonight

**First:** synchronize `main.tex` and the PDF.

**Second:** fix the paraquat/regulatory wording and the 16123 referral text. The current manuscript states fixed helpline hours, but the current official Agricultural Information Service page gives different operating information; because these details are operational and can change, the safest paper-level choice is to omit exact hours and keep the referral itself. ([Ais][10]) The manuscript currently states specific hours in the ethics section. 

**Third:** fix “five stages” versus the six-box Figure 1.

**Fourth:** rename the C2 metric everywhere from “wrong-crop advice” to the exact retrieval quantity you actually measured.

**Fifth:** rebalance the abstract so the cloud and deployed safety results are both represented.

**Sixth:** remove or compress Table 1 and the C1 LLM comparison.

**Seventh:** make the demo-model/cloud-benchmark boundary explicit.

**Eighth:** manually test the demo, screencast, and package links from an external browser, then enter the same URLs into OpenReview.

**Ninth:** nominate the reciprocal reviewer.

**Tenth:** final PDF visual pass: check the first six pages only for figure placement, orphan headings, link wrapping, title consistency, and any residual placeholder.

---

## The most important distinction

I would **not** describe the needed revision as “make the paper more rigorous by adding more experiments.”

The paper already has more experimental machinery than this track requires. The higher-value revision is:

> **make every prominent claim correspond exactly to what the system and evaluation actually establish, while making the live demonstration the center of the paper.**

That is why the paraquat issue, C2 terminology, cloud/local distinction, and Figure 1 stage count matter more right now than another 300-query benchmark.

Your strongest material is already there: the continuous farmer interaction, explicit control states, visible mismatch/referral/verification behavior, real artifact availability, and evaluation tied directly to those controls. 

I can generate a publication-ready replacement for **Figure 1** right now—which style should I use: **ACL-minimal flowchart, compact safety-pipeline, or polished systems-architecture**?

[1]: https://2027.eacl.org/calls/demos/?utm_source=chatgpt.com "Call for System Demonstrations -"
[2]: https://aclanthology.org/volumes/2026.eacl-demo/?utm_source=chatgpt.com "Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 3: System Demonstrations) - ACL Anthology"
[3]: https://aclanthology.org/2025.acl-demo.7/?utm_source=chatgpt.com "My Climate CoPilot: A Question Answering System for Climate Adaptation in Agriculture - ACL Anthology"
[4]: https://aclanthology.org/2024.acl-demos.14/?utm_source=chatgpt.com "LocalRQA: From Generating Data to Locally Training, Testing, and Deploying Retrieval-Augmented QA Systems - ACL Anthology"
[5]: https://aclanthology.org/2026.acl-demo.19/?utm_source=chatgpt.com "DialogGuard: Multi-Agent Psychosocial Safety Evaluation Interface of Sensitive LLM Responses - ACL Anthology"
[6]: https://aclanthology.org/2026.acl-demo.82/?utm_source=chatgpt.com "OpenGlass: A Sensing-Computing Split Architecture for Local MLLM-Driven Real-Time Visual Assistance - ACL Anthology"
[7]: https://aclanthology.org/2026.acl-demo.36/?utm_source=chatgpt.com "FactSearch: An Interactive Agentic Fact Search System for Verifying Large Language Model Outputs - ACL Anthology"
[8]: https://dae.gov.bd/sites/default/files/files/dae.portal.gov.bd/page/8a812db0_3544_4105_b066_df78074d3efb/Registered%20Agricultural%20PesticidesList%20%286%29.pdf?utm_source=chatgpt.com "List of Registered Agricultural Pesticides, Bio Pesticides and Public Health Pesticides in Bangladesh                                                                                                 Approved"
[9]: https://www.bssnews.net/district/409351?utm_source=chatgpt.com "Ban on hazardous pesticides demanded to ensure safe food, biodiversity | District"
[10]: https://ais.gov.bd/site/page/d9147061-2995-416f-b355-d7feb0d9f9a1/%E0%A6%95%E0%A7%83%E0%A6%B7%E0%A6%BF-%E0%A6%95%E0%A6%B2-%E0%A6%B8%E0%A7%87%E0%A6%A8%E0%A7%8D%E0%A6%9F%E0%A6%BE%E0%A6%B0?utm_source=chatgpt.com "কৃষি কল সেন্টার | পাতা | কৃষি তথ্য সার্ভিস (এআইএস)"
