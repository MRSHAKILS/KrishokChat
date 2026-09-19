Prompt:
You are acting as a senior NLP researcher and reviewer preparing a manuscript for the EACL 2027 System Demonstrations Track.

I will provide you with some or all of the following:

1. The current manuscript in text/Markdown/LaTeX form.
2. A PDF of the current manuscript, if available.
3. A ground-truth YAML describing the actual system, implementation, data, components, functionality, experiments, and other project facts.
4. Potentially additional project materials.

Your first task is NOT to rewrite the paper.

Your task is to perform a forensic audit of the current manuscript and determine what kind of paper it currently is, what kind of paper it should become for the EACL 2027 System Demonstrations Track, and where the current manuscript diverges from that target.

IMPORTANT: Do not assume what the system is about, what its main contribution is, or which functionality is most important. Infer these from the supplied ground-truth YAML and manuscript. Treat the YAML as the factual source of truth. If the manuscript claims something that is not supported by the YAML or supplied evidence, flag it rather than accepting it.

## STEP 1 — VERIFY THE CURRENT EACL 2027 REQUIREMENTS

Before analyzing the manuscript, search the current official EACL 2027 System Demonstrations Call for Papers and any other official EACL/ACL sources necessary to establish the current requirements.

Determine and explicitly record:

* maximum main-paper page limit;
* what is excluded from that page limit;
* appendix policy;
* reference policy;
* ethics/broader-impact policy;
* required demonstration video and its maximum length;
* live demo website/installable-package requirement;
* evaluation requirement;
* originality/multiple-submission requirements;
* any other requirement that could cause desk rejection;
* relevant submission and camera-ready dates.

Use the current official EACL 2027 sources whenever possible.

Do not rely on remembered or outdated EACL/ACL requirements.

## STEP 2 — STUDY REAL RECENT DEMONSTRATION PAPERS

Search the ACL Anthology and other authoritative sources for recent accepted EACL and ACL System Demonstration papers, prioritizing EACL 2026 and ACL 2025/2026.

Select a representative sample of accepted demonstrations, including systems with different types of contributions.

Study their:

* section structures;
* introduction length and style;
* treatment of related work;
* treatment of novelty;
* architecture descriptions;
* screenshots and figures;
* functionality descriptions;
* evaluation;
* comparison with existing systems;
* system availability;
* use of appendices;
* level of implementation detail;
* balance between research contribution and system demonstration.

Do NOT simply imitate any one paper.

Instead, infer recurring characteristics of successful recent System Demonstration papers.

Clearly distinguish:
A. requirements explicitly stated by the EACL CFP;
B. recurring patterns observed in accepted papers;
C. your own interpretation.

Do not claim that a pattern is an official requirement unless the CFP actually says so.

## STEP 3 — RECONSTRUCT THE CURRENT MANUSCRIPT

Create a structured inventory of the current manuscript.

For every section/subsection, identify:

* its purpose;
* the claim it is trying to establish;
* whether it describes the problem, research contribution, system, implementation, evaluation, or background;
* whether it is essential for a System Demonstration paper;
* whether it is overly detailed;
* whether it belongs in the main paper;
* whether it belongs in an appendix;
* whether it can be removed;
* whether it should be represented visually instead of explained in prose.

Do not rewrite the content.

## STEP 4 — IDENTIFY "RESEARCH PAPER DRIFT"

Specifically diagnose whether the manuscript behaves like a conventional research paper rather than a system demonstration.

Look for:

* excessive literature/background discussion;
* excessive methodological detail;
* research-question framing that is stronger than necessary;
* detailed experimental analysis that does not establish system validity;
* excessive ablations;
* implementation details that could be moved to an appendix;
* repeated explanations of the same contribution;
* too many independent contributions;
* features described as if each were a separate research contribution;
* excessive theoretical explanation;
* dataset details that do not matter to understanding the demonstrated system;
* results that are interesting scientifically but not central to demonstrating the system;
* functionality that is described but not shown;
* claims of novelty that are not sufficiently grounded in related work;
* places where a diagram or screenshot would communicate more efficiently than prose.

## STEP 5 — INVENTORY ALL SYSTEM FUNCTIONALITIES

From the YAML and manuscript, build a complete functionality inventory.

For every functionality/component, classify it as:

A. Core system functionality
B. Important supporting functionality
C. Optional/secondary functionality
D. Implementation detail
E. Research/evaluation component
F. Appendix-only material
G. Potentially removable material

Do not decide based merely on how much space the current manuscript gives something.

Instead, judge its importance to the demonstrated user-facing/system-facing contribution.

## STEP 6 — IDENTIFY THE CURRENT STORY

Describe the current paper's story in 5–10 sentences.

Then describe the story that a strong System Demonstration paper would need to communicate, without rewriting the manuscript.

Identify the mismatch.

## STEP 7 — PAGE-BUDGET DIAGNOSIS

Do NOT yet force the manuscript into six pages.

Instead, estimate how the current manuscript's content would distribute across a six-page main paper.

Identify:

* content that must remain;
* content that should be compressed;
* content that should move to figures;
* content that should move to appendices;
* content that should disappear.

The goal is not yet to achieve six pages.

The goal is to understand what the six pages should be used for.

## STEP 8 — OUTPUT

Return a rigorous audit with these sections:

1. Verified EACL 2027 Requirements
2. Evidence from Recent Accepted Demonstration Papers
3. Current Manuscript Structure
4. Research-Paper Drift
5. Complete Functionality Inventory
6. Current Story
7. Desired System-Demonstration Story
8. Main-Paper vs Appendix vs Remove Table
9. Six-Page Content Budget
10. Major Problems That Must Be Fixed
11. Information Still Needed From the Author
12. Recommended Next Stage

Do not rewrite any section of the paper yet.

Do not invent facts.

Do not invent novelty.

Do not use generic statements such as "this paper presents a novel framework" unless the supplied evidence actually supports that claim.

The goal of this stage is diagnosis, not writing.





I'll start by checking the uploaded files, then verify the official EACL 2027 requirements.# Forensic audit: KrishokTech manuscript vs. EACL 2027 System Demonstrations

## Read this first

1. **No ground-truth YAML was attached**, only `main.pdf` and `main.tex`. Every statement about what the system does is therefore "claimed by the manuscript", not verified. Section 11 lists what I need.
2. **Timing.** The paper deadline is 22 September 2026, all deadlines are 11:59 pm AoE, and there is no rebuttal stage. That is 11:59 UTC on 23 Sep, about three days from now.
3. **Three items are each a desk-reject trigger.** I checked the LaTeX source directly.
   - There is no demo URL and no video link anywhere in the source.
   - The main body is about 11½ pages against a limit of 6.
   - All 12 figures are `\placeholderbox` text boxes, not screenshots. Screenshot numbering also skips "Screenshot 6".
4. **The highest-stakes finding is the bibliography.** All four competitor citations I checked have wrong authors, titles or venues (Section 10). EACL's integrity policy names hallucinated citations as grounds for desk rejection, and authors may be barred from committing to EACL 2027 and 2028. Fix this before anything else.

---

## 1. Verified EACL 2027 requirements

Source: the official [Demo CFP](https://2027.eacl.org/calls/demos/). I cross-checked the main-conference CFP for the integrity policy.

| Item | Official requirement | Manuscript status |
|---|---|---|
| Length | Up to 6 pages; longer submissions are desk-rejected. | ≈11½ body pages (19 total): **fails** |
| Excluded from the limit | Unlimited space for an optional ethics/broader-impact statement, plus unlimited references and informative appendices. Accepted papers get one extra page. | Limitations and Conclusion are inside the 6 pages unless the chairs say otherwise (my reading) |
| Appendices | Unlimited (above) | 6 pages. The CFP does not say reviewers must read them (my interpretation) |
| Ethics | The statement is optional, but papers on sensitive tasks that do not discuss ethics will not be accepted. Flagged papers go to an ethics committee. | None. Pesticide-dosage advice to farmers is a sensitive task |
| Video | A screencast of at most 2.5 minutes. The link must be in the PDF and in the OpenReview form. | **Missing** |
| Demo / package | A live demo link or installable package is strictly enforced; no link means desk rejection. Exceptions apply only where sharing is clearly impossible, and the link goes in both the PDF and the form. | **Missing** |
| Evaluation | Comprehensive experiments are not required, but a paper with no validation evidence may be desk-rejected. Acceptable evidence includes user studies, simulations, benchmarks, expert evaluations, usage statistics, case studies and qualitative feedback. | Simulations and benchmarks only |
| Originality | The work must be original and unpublished, and cannot be in review elsewhere (ARR included). Significant overlap with other published work is not considered, and two demo submissions may not overlap by more than 25%. | Needs a check (Section 10) |
| Anonymity | Single-blind; names and affiliations are included. | OK |
| Reviewer duty | Each paper must nominate one author as a reciprocal reviewer. | Unknown (OpenReview form) |
| Format | PDF in the official EACL style; deviations in style or page limit are desk-rejected. | Uses `acl.sty`, A4, 11pt. I could not confirm the 2027 template version |
| Presentation | At least one author registers and presents a live demo with a poster. | Plan for it |
| Integrity | EACL-wide: hallucinated citations and thinly sliced contributions may be desk-rejected, with consequences for all authors. Whether the demo track applies this is my inference, since the main CFP frames it as EACL-wide. | **At risk** |
| Dates | Submission opened 18 Aug 2026; deadline 22 Sep 2026; notification 18 Dec 2026; camera-ready 6 Jan 2027; conference 9–14 March 2027. | — |

**The five reviewer questions in the CFP** are Motivation/Fit/Novelty, Related Work & Contribution, System & Demonstration Description, Evaluation/Availability/Licensing, and Presentation Quality. Reviewers are asked how clearly the architecture and the demonstration are described, how the system was validated, how it can be accessed, and under what license it is distributed. Current exposure per question:

| Reviewer question | Current risk |
|---|---|
| Motivation, fit, novelty | Medium. The novelty table is contradicted by verified sources |
| Related work | **High**. Citations do not match real records |
| System & demo description | High. There are no real screenshots; PRISM-RAG is undescribed |
| Evaluation, availability, license | **High**. No link, no license, no user or expert evidence |
| Presentation | High. Length, redundancy, placeholder figures |

---

## 2. Evidence from recent accepted demonstration papers

**Sample and limits.** EACL 2026 received 102 demo submissions and accepted 44 (43.1%). I read all 44 abstracts (the volume lists toolkits, RAG applications, interpretability tools, tutoring systems and a Bangla NLP platform). I read three papers in full: BanSuite (EACL 2026), AI for Climate Finance (EACL 2026) and My Climate CoPilot (ACL 2025). I did not sample ACL 2026 or EMNLP 2025 demos. Three full texts is a thin basis for the B-patterns below.

**A. Explicit CFP requirements.** See Section 1.

**B. Recurring patterns in the sample**
- **Access is stated up front.** Many abstracts end with a repo, live demo, package or video link and often a license. DeepPavlov cites Apache 2.0 and an online demo; AlignFix cites a live demo and Apache 2.0. BanSuite puts its YouTube link in the abstract.
- **Six pages carry the story; detail goes to appendices.** Climate Finance's main paper runs pages 492–497, followed by appendices A–K (methods, demo details, deployment case studies, dataset statistics) through page 511. BanSuite moves UI screenshots, code snippets and energy analysis to appendices.
- **Short related work.** My Climate CoPilot uses about half a page. Climate Finance uses roughly one paragraph.
- **The stack is named.** My Climate CoPilot names Rust, Elasticsearch and Claude Sonnet 3.5. Climate Finance names FastAPI, Weaviate and the OpenAI API. KrishokTech never names its generator LLM.
- **Evaluation is proportionate and comparative.** BanSuite compares against toolkits and LLMs and reports energy. Climate Finance compares against four baselines and two black-box assistants, and adds an ablation. My Climate CoPilot used over 50 domain experts, ratings and two long interviews.
- **Modest novelty framing.** Climate Finance says its components are individually established and claims only their domain-specific integration.
- **Ethics and limitations come after the main text.** My Climate CoPilot has an ethics-approval statement. Climate Finance has limitations, ethics and reproducibility statements.
- **Both diagrams and UI figures appear.** Two of the three sampled papers put their UI screenshots in the appendix. The CFP accepts screenshots or diagrams, but I would not rely on that.

**C. My interpretation**
- A demo submission is judged as a package of paper, video and live link, so the paper must be consistent with what a reviewer sees in the video.
- The main text should stand alone even if appendices go unread.
- A safety-critical domain warrants an explicit ethics/broader-impact statement, which costs no page budget.

---

## 3. Current manuscript structure

19 pages: about 11½ body, 1½ references, 6 appendix. Body prose is about 6,000 words, with 12 figures (all placeholders) and 7 tables. A six-page paper with 4–5 visuals holds roughly 3,000–3,300 words.

| § | Words | Purpose / claim | Type | Essential? | Disposition |
|---|---|---|---|---|---|
| Abstract | 190 | Four mechanisms plus three headline numbers | Summary | Yes | Compress; three overclaims (Section 10) |
| 1 Intro | 1,100 | Farmer stats, prior-study recap, image conflict, routing literature, system and evaluation preview, 4 contributions | Problem + background | Partly | Compress hard; move stats and routing literature |
| 2 (lead) | 60 | "Successive decision boundaries" | System | Yes | One sentence plus Fig. 1 |
| 2.1 | 250 | T0 precheck, T1 slots, halt outcomes, DialectSelector, token medians | System + eval | Yes | Keep core; medians to appendix |
| 2.2 | 280 | Crop-fenced BM25, router, per-crop top-1, fence simulation | System + eval | Yes | Compress; numbers to Evaluation |
| 2.3 | 260 | Untrusted LLM, verifier, badges, verifier and ASR results | System + eval | Yes | Compress; duplicates §4.3 |
| 2.4 | 360 | SMS, offline, TTS, footprint, tier mix, latency | System + eval + deployment | Partly | Compress hard |
| 3.1–3.5 | 870 | Five scenarios narrated against placeholder figures | Demonstration | **Most important** | Replace prose with a screenshot and storyboard |
| 3.6 | 190 | Restates 3.1–3.5 as a list | Demonstration | No | Cut or merge |
| 4.1–4.3 | 1,270 | Gate, fence/mismatch, safety/delivery | Evaluation | Partly | One table plus one figure |
| 5 | 600 + Table 1 | 13-feature comparison with 4 systems | Related work | Yes, but flawed | Rebuild from verified sources |
| 6.1 | 440 | Limitations | Limits | Yes | Halve |
| 6.2 | 310 | Restates abstract | Conclusion | No | 3–4 sentences |
| App. A–G | ≈2,400 + 6 tables + 4 figures | Protocol, INT8, routing probe, failures, claim-status table | Detail | Mixed | Curate (Section 8) |

---

## 4. Research-paper drift

| Symptom | Evidence |
|---|---|
| Demo is the minority of the paper | Sections 2 and 4 together are about 2,500 words; the demonstration (§3) is about 1,060 |
| The same results are retold everywhere | In the main text, 0.95% appears 7 times, "76" 6 times, and 0.3625 four times. They recur across abstract, intro, §2, §4, figures, conclusion and appendix |
| Defensive scoping | About 43 hedging or "not a claim" phrases in the main text. It reads as written to survive a research review |
| Features framed as research contributions | All four contributions begin "We introduce…". PRISM-RAG is contribution 2 but has no method subsection and no main-text evaluation |
| Over-granular evaluation | Per-mutation counts, extractor agreement, miss and false-positive rates, a McNemar p-value for a simulation, and 40+ numbers in the main text |
| Novelty argued by measurement gaps | Related work says prior systems did not report "the same operating measurements", which is not a system comparison |
| Described but not shown | Voice-transcription toggle (Fig. 2 only), DialectSelector, PRISM routes and the Evidence Agreement Gate have no visual or evidence |
| Prose where a figure would do | §2.1–2.4 walk through stages one by one; §3.6 lists six scenarios; Tables 5–7 could be one compact table |
| Ungrounded novelty | "Typed working memory", "5-level answerability routing" and "colloquial concept normalizer" are claimed as extensions over prior work with no related-work support |

---

## 5. Complete functionality inventory

Class key: **A** core, **B** important supporting, **C** optional/secondary, **D** implementation detail, **E** research/evaluation component.

| # | Functionality | Class | Shown visually? | Evidence in manuscript |
|---|---|---|---|---|
| 1 | T0 deterministic safety precheck → 16123 | A | Placeholder | 10/10 injections blocked; 0/30 off-topic refused; routing-probe refuse recall 0.493 |
| 2 | T1 slot extraction and pre-retrieval halt (clarify / cultural card / refuse) | A | Placeholder | 76/200 halted; extractor agreement 0.52, miss 0.475 |
| 3 | Quick-reply crop-chip clarification | B | Placeholder | Conformance 86/100 (seeded memory) |
| 4 | Non-chemical guidance card / partial-advice checklist | B | No | None |
| 5 | DialectSelector (6 presets) | C | No | None; mechanism unstated |
| 6 | Typed session working memory | B | Caption only | None; follow-up "untested" |
| 7 | PRISM router (5-level routing, 4 routes) | B | No | Overall conformance 0.458; document-RAG route 16/168 |
| 8 | ConceptNormalizer | B | No | Route agreement 258/458 |
| 9 | Evidence Agreement Gate + discriminative clarification | B | No | None |
| 10 | Crop-fenced BM25 retrieval | A | Placeholder | 0.3625→0.30 under gold routing; contradictory appendix arm |
| 11 | On-device ONNX crop/disease models + tri-state router | A | Placeholder | Top-1 0.90–0.96 on 4 crops; corn and chilli unmeasured |
| 12 | Text–image mismatch badge | A | Placeholder | 453/454 explicit cases; implicit conflicts uncovered |
| 13 | Grounded LLM generation (model unnamed) | B | No | 60-row review: 31.7% medium-or-better |
| 14 | Dosage verifier | A | No | Per-mutation counts; 38 clean answers |
| 15 | Provenance badges, sentence citations, drop audit | A | Placeholder | Trace order 100/100; no usability test |
| 16 | 16123 terminal referral | A | Placeholder | Referral purity 16/16 (SMS) |
| 17 | Offline PWA card + local BM25 | B | Placeholder | 0.94 hit rate (simulated loss); "0/400 cached" unexplained |
| 18 | 160-character SMS packer | C | Placeholder | ≤160 chars 299/300 and 100/100; dose survives 0/84 |
| 19 | Bengali neural TTS (+ Web Speech fallback) | C | Placeholder | None |
| 20 | Voice input toggle | C (unverified) | Fig. 2 only | None |
| 21 | INT8 quantization | D | No | Wheat neutral, rice rejected, latency worse |
| 22 | WASM inference, footprint, latency, cost model | D/E | No | 284 MB; 33.6 ms; modeled US$0.1798 per 1,000 turns |
| 23 | Evaluation harnesses (3,000-query probe, equivalence arm, live-vs-deterministic) | E | No | Dangerous acceptance 0.374 |

I ranked these by contribution to what a viewer would see, not by manuscript space. The visible core is the halt/clarify behavior, the crop fence with mismatch badge, and the verified, badged answer with terminal referral. PRISM internals are supporting components the manuscript currently presents as a headline contribution.

---

## 6. Current story

KrishokTech is a Bengali agricultural advisory system that treats the LLM as an untrusted stage inside a fixed pipeline. A deterministic precheck blocks unsafe requests. A slot gate halts treatment queries with no crop before retrieval. Crop identity from text or an on-device image model restricts BM25 retrieval. A verifier removes unsupported dosage claims before display. Answers can go out through the web, SMS, an offline card, TTS or a helpline referral. Motivation comes from Bangladesh's extension-agent shortage and the authors' earlier colloquial-retrieval study. Support is a series of operating-point measurements: 76/200 halts, a perfect-routing fence simulation (36.25%→30.0%) and a 36.19%→0.95% attack-success drop. A demonstration section narrates six scenarios against placeholder figures. Related work is a 13-feature table in which nearly every distinguishing row is checked for KrishokTech alone. The manuscript reads as an evaluation report on a control architecture with a demo section attached.

## 7. Desired system-demonstration story (described, not drafted)

A reviewer should be able to answer these from the first page, the video and the link:
- **What it is and who it serves.** A working, accessible Bengali advisory application, with a stated intended user (farmers or extension workers).
- **What the visible behaviors are.** Perhaps 4–5 behaviors, each seen in the interface, and why they matter for NLP in Bengali.
- **What it is built from.** Named components, including the LLM, and an architecture diagram.
- **Where to try it.** A live link, video and license.
- **What evidence validates it.** Enough to show the behaviors work, with honest limits.
- **What is new versus real prior systems.** Only claims that survive verification of the competitors.

**Mismatch.** The manuscript argues from operating-point statistics. The demo genre argues from what the user can see and try, and what evidence makes that trustworthy. The novelty claim needs to be rebuilt after the citations are corrected (Section 10).

---

## 8. Main paper vs appendix vs remove

| Content | Disposition | Reason |
|---|---|---|
| Problem, intended user, 3 contributions maximum | **Main**, compressed | Reviewer question 1 |
| Access links, license, video | **Main** (abstract and intro) | Mandatory |
| Architecture figure and stage descriptions | **Main** | Core |
| Real UI screenshot | **Main** | Mandatory visual aid |
| Scenario storyboard (halt, photo, mismatch, verified answer, referral) | **Main** | The demonstration |
| Compact evidence table (gate, fence, mismatch, safety, verifier) | **Main** | Validity |
| Short limitations | **Main** | Honest scope |
| Related work with corrected citations | **Main**, shortened | Reviewer question 2 |
| Farmer statistics, routing literature | Compress or cut | Background |
| PRISM description | Compress into architecture | Currently undescribed |
| DialectSelector, TTS, SMS | Compress to captions | Secondary, thinly supported |
| Per-mutation verifier counts, extractor analysis | Appendix | Detail |
| INT8, browser latency, footprint, tier mix, trace ordering | Appendix | Implementation |
| Routing probe, equivalence arm, failure ledger, Table 7 | Appendix, **reconcile first** | Currently contradict the headlines |
| Ethics and broader-impact statement | **After page 6** | Unlimited space |
| §3.6 list, repeated headline numbers, conclusion restatement, most hedges | **Remove** | Redundant |

---

## 9. Six-page content budget (diagnostic, not a draft)

| Use of the six pages | Current ≈pp (proportional estimate) | Target ≈pp |
|---|---|---|
| Abstract and title | 0.3 | 0.25 |
| Introduction and contributions | 2.1 | 0.6 |
| Related work | 1.2 | 0.4 |
| System: architecture figure and stages | 2.3 | 1.4 |
| Demonstration: screenshot, storyboard, captions | 2.0 | 1.5 |
| Evaluation: one table, one figure | 2.4 | 1.2 |
| Availability, limitations, conclusion | 1.5 | 0.5 |
| **Total** | **≈11.5** | **≈5.85** |

About two of the six pages should be figures. Ethics, references and appendices sit outside the limit. The accepted-paper extra page arrives only after acceptance, so do not design for seven.

---

## 10. Major problems that must be fixed

**P0: desk-reject or integrity risk**
1. **No live demo link, video link, license or code link.**
2. **Length:** about 11½ pages against 6.
3. **All figures are placeholders.**
4. **Reciprocal reviewer** must be nominated in the form.
5. **Citations do not match real records:**

| Manuscript says | What I found |
|---|---|
| KrishokBondhu: Ahmed, Kabir, Rahman, EMNLP 2025 System Demonstrations, pp. 142–151 | Real authors are Ameen, Islam, Aktar and Rafat; the arXiv comments say it was submitted to IEEE WIECON-ECE 2025. Your own arXiv paper cites it as Ameen et al., IEEE QPAIN 2026. |
| Farmer.Chat: Mishra, Verma, Gupta, Seth, ACM CSCW 2024 | The paper is by Namita Singh and colleagues, titled "Farmer.Chat: Scaling AI-Powered Agricultural Services for Smallholder Farmers" (arXiv 2409.08916). |
| Krishi Sathi: Sharma, Patel, Kumar, arXiv:2508.03719 | That arXiv number is "Intent Aware Context Retrieval for Multi-Turn Agricultural Question Answering" by Vijayvargia and colleagues at BharatGen. |
| My Climate CoPilot: Wadhwa et al., "inspectable expert-validated…", pp. 112–122 | The real paper is by Nguyen, Hallgren, Harkin, Prakash and Karimi, ACL 2025 System Demonstrations, pp. 62–70. |
| Agrawal, Batra, Parikh, "When visuals disagree", CVPR 2024 | I could not find it. A candidate you may have meant is Deng et al., "Words or Vision: Do VLMs Have Blind Faith in Text?", CVPR 2025 (listed in another paper's references). Confirm |
| Reza et al. 2026b, third author "Arshad Shahid" | Your arXiv paper 2608.14886 lists the third author as Omar-Ibne Shahid and the venue as EACL proceedings. Reconcile |

I did not verify the World Bank, DAE, DLEC, Bhasabodh, AIEP or FrugalGPT (venue) entries; check them all. The corrected KrishokBondhu and Farmer.Chat records already exist in your own arXiv paper.

6. **Overlap check.** Confirm that the crop-fence experiment, the 1,000-query PRISM suite and the safety evaluation do not also appear as results in your other KrishokTech-family manuscripts (the benchmark paper under review, AgriDial-NLU, and the structured-retrieval paper).

**P1: what a careful reviewer will find**
- **Comparison table contradicted.**
  - KrishokBondhu delivers spoken Bengali answers via text-to-speech. Table 1 says it has none.
  - Krishi Sathi collects missing details across turns and offers speech input and output. Table 1 marks it as lacking a pre-retrieval halt and working memory.
  - The manuscript credits Krishi Sathi with image-based diagnosis. I found no support for that in its abstract.
  - My Climate CoPilot's self-evaluation scores presentation and epistemic criteria. It is not a dosage verifier, yet Table 1 gives it a check in that row.
  - A directly relevant Bengali agricultural RAG system, Hossain et al. 2026 (arXiv:2601.02065), appears in your other paper's reference list but is missing here.
- **Motivation mismatch.** In your prior paper, dense retrieval scores 0.093 on colloquial queries and 0.970 on formal safety queries. Hybrid reaches 0.539 across all 900 queries, and BM25 scores 0.523 on colloquial farmer queries. KrishokTech deploys BM25 and says dense retrieval was not evaluated, so the colloquial gap that motivates the DialectSelector is largely a dense-retrieval phenomenon.
- **Numbers that do not reconcile.** (Wilson intervals recomputed by me.)
  - The reported intervals [0.26, 3.41] and [29.99, 42.88] match 2/210 and 76/210, so "420 calls" appears to be the total across two arms, not the guarded n.
  - The Bangla-native intervals match 10/100 and 83/100, which implies 10 guarded failures. That exceeds the roughly 2 implied for the whole guarded arm. Embedded (4/10) and roleplay (2/10) failures alone total 6.
  - The fence simulation moves 0.3625→0.30 (n=400), while Appendix A.2 reports blind 0.30 vs gated 0.30 (n=400, 0/0 discordant, p=1.0). The fence effect depends on which baseline is used.
  - Wrong-crop advice is still 30% under perfect routing, unexplained.
  - Limitations says "8–33 cases per mutation" while the appendix says 25–33.
  - Fractions are paired with percent intervals (0.1607 [8.69, 27.81]).
  - Tier terminology collides: T0–T4 stages, Tier-0..3 execution tiers, "5-tier" provenance and "5-level" routing.
- **Abstract overclaims.**
  - "76/200 ambiguous farmer queries" conflicts with §4.1, which says the halt rate is not an ambiguity estimate. The extractor's 0.475 miss rate means halts may partly reflect extraction failures. Halt precision is not reported.
  - "Perfect-gold routing" is omitted from the fence claim.
  - "Dangerous advice" is not the same metric as "attack success rate".
  - The 10% Bangla-native residual is not mentioned.
- **"LLM is not the default path" versus your own data.** The tier mix shows 92.2% of turns reach Tier-3 generation, with 7.8% zero-LLM turns and a 7.79% modeled saving.
- **Negatives buried in the appendix:** a 47.5% extractor miss rate, 45.8% overall route conformance, 9.5% on the document-RAG route, 37.4% dangerous acceptance and 49.3% refuse recall in the routing probe, 0/30 off-topic refusals, 31.7% medium-or-better on a 60-answer quality review, and dose fields surviving SMS in 0/84 cases. The Limitations section largely omits these.
- **Delivery claims.**
  - By the appendix's own figure (70 characters per UCS-2 segment), a 160-character Bengali SMS spans multiple segments.
  - TTS uses a cloud service (Microsoft Edge speech), which conflicts with the low-connectivity premise. Check the terms of use.
  - Offline results use simulated network loss, and "0/400 cached cases" is unexplained.
- **PRISM-RAG is a headline contribution with no method section and no main-text evidence.**
- **No end-to-end, user or expert evaluation, and the generator LLM is never named.**
- **Ethics gap.** There is no statement on farmer-query provenance and consent, image data, LLM data handling, single-reviewer labels, or pesticide dual-use.

**P2: presentation**
- Ambiguous tier names, cryptic phrases ("T1 base contains a 0.0% value for the 9-fact base") and inconsistent CI formatting.

---

## 11. Information still needed from the author

**Submission-critical**
1. The ground-truth YAML.
2. Is the demo deployed? Give the URL, whether it needs a login or API keys, and whether it can stay up through review. If not, is there an installable package?
3. Is a screencast of 2.5 minutes or less recorded, and where is it hosted?
4. License and repository.
5. Which author is the reciprocal reviewer?

**System facts**
6. Generator LLM: model, hosting, data-handling terms and cost.
7. How do the DialectSelector, ConceptNormalizer, PRISM routes and Evidence Agreement Gate work, and what were the four retrieval routes?
8. Is SMS a gateway integration or an export button? Is TTS online-only? Is voice input real?
9. Is 16123 confirmed as the current national helpline, and is routing users to it authorized?

**Evidence**
10. Reconcile the numbers in Section 10: 420 vs 210 per arm, the Bangla-native subset, the two 0.30 baselines, the cache 0/400 diagnostic, and the 60-row quality-review source.
11. Provenance, consent and ethics approval for the 200 farmer queries and any images.
12. Any usage data, extension-officer feedback or farmer feedback?
13. The verified bibliography (Section 10), including which paper "Reza 2026b" is.

**Decisions**
14. Primary audience: farmers or extension workers?
15. Do you want PRISM-RAG presented as a component or as a contribution, given the evidence it currently has?
16. Overlap with your sibling manuscripts (Section 10, item 6).

---

## 12. Recommended next stage

**Stage 2 is a fact lock, with no prose.** It has four parts:
- Supply the YAML.
- Build a claims ledger in which every number is tied to an artifact.
- Replace the bibliography with verified records (I can help check the remaining entries).
- Run a go/no-go check on the demo link, video, license, real screenshots and reciprocal reviewer.

Then Stage 3 is a section-level outline and figure specification against the Section 9 budget, and Stage 4 is the compressed draft.

**Feasibility with three days left.** The link and video are strictly enforced, and both require working software and a recording. If a public demo you can stand behind will not exist by the end of Sunday, I would not submit this cycle. A desk rejection plus an integrity flag costs more than a later venue.

A workable schedule: Saturday for the fact lock, Sunday for outline, screenshots and video, Monday for the draft and OpenReview form, and Tuesday (AoE) as buffer.

Send me the YAML and the demo and video status and I'll start Stage 2. You can also ask the chairs at eacl2027-sysdemo@googlegroups.com whether Limitations counts toward the six pages.