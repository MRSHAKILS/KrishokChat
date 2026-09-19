Prompt:
You are now acting as a senior EACL System Demonstration reviewer and research editor.

I am preparing an EACL 2027 System Demonstrations submission.

You have access to:

* the ground-truth YAML;
* the current manuscript;
* the PDF, if supplied;
* and potentially the forensic audit from a previous analysis.

If a previous analysis is supplied, use it as evidence, but independently verify important claims against the original YAML/manuscript.

Your task is NOT to rewrite the paper yet.

Your task is to determine exactly what the six-page EACL System Demonstration paper should emphasize.

## 1. RESEARCH BEFORE JUDGING

Search current and recent authoritative sources.

At minimum, examine:

* the official EACL 2027 System Demonstrations CFP;
* recent EACL System Demonstration papers, especially EACL 2026;
* recent ACL System Demonstration papers;
* closely related systems/tools in the same problem area;
* relevant recent research papers needed to establish novelty and positioning.

Prioritize actual accepted demonstration papers and primary sources.

Do not infer "what reviewers like" from generic blogs or advice pages.

Do not claim to know hidden reviewer preferences.

Instead distinguish:

* explicit CFP requirements;
* recurring patterns in accepted papers;
* evidence-based positioning against related systems;
* your own editorial judgment.

## 2. DETERMINE THE CENTRAL SYSTEM CONTRIBUTION

Using the actual project evidence, answer:

What is the system primarily demonstrating?

Do not automatically treat every implemented feature as a contribution.

Find the smallest coherent set of system capabilities that makes the system meaningfully distinct and useful.

Then identify:

* central contribution;
* supporting contributions;
* secondary functionality;
* implementation details;
* evaluation-only components.

If multiple plausible central stories exist, present them as alternatives and explain what evidence distinguishes them.

Do not choose a story merely because it sounds more impressive.

## 3. FEATURE SELECTION

For every major functionality, score it qualitatively using the following dimensions:

* relevance to the central user problem;
* distinctiveness compared with existing systems;
* importance to the system's identity;
* demonstrability in a live demo;
* evidence that the functionality works;
* usefulness to the intended audience;
* need for explanation in the main paper;
* suitability for appendix-only treatment.

Do NOT produce a numerical ranking or arbitrary score.

Instead classify each functionality as:

MAIN PAPER
SUPPORTING MAIN PAPER
FIGURE/SCREENSHOT ONLY
APPENDIX
REMOVE

Explain the evidence for each classification.

## 4. NOVELTY AUDIT

For every claimed contribution, search for existing systems or papers that perform similar functions.

Build a table with:

* our functionality/contribution;
* closest prior systems/papers;
* what those systems already do;
* what our system actually adds;
* whether the difference is architectural, functional, data/resource-based, interaction-based, evaluation-based, or merely implementation;
* whether the difference is strong enough to describe as novel;
* whether the wording should be softened.

Be conservative.

If something is not genuinely novel, do not manufacture novelty language.

If the contribution is primarily integration, accessibility, usability, resource creation, or a new application, say so explicitly rather than pretending it is a new algorithm.

## 5. DEMONSTRATION VALUE

Analyze what can actually be shown in a 2.5-minute demonstration video and a live demo.

Determine:

* the ideal user journey;
* the most informative interaction sequence;
* which functionality should appear in the demo;
* which functionality is unnecessary to demonstrate;
* which screenshot(s) would communicate the system most effectively;
* which architectural diagram is necessary;
* which functionality can be mentioned in one sentence rather than explained.

The paper and video should reinforce each other rather than duplicate each other unnecessarily.

## 6. MAIN PAPER VS APPENDIX

Construct a detailed content allocation.

MAIN PAPER should contain only material necessary to establish:

* practical problem;
* importance;
* system contribution;
* relevant novelty;
* system architecture;
* key functionality;
* intended users;
* evidence of validity/usefulness;
* comparison/positioning;
* availability/licensing.

APPENDIX may contain supporting material such as:

* extended architecture;
* additional functionality;
* detailed implementation;
* complete prompts;
* additional screenshots;
* extensive examples;
* additional experimental results;
* ablations;
* detailed dataset/resource information;
* secondary evaluations;
* edge cases;
* full benchmark tables;
* supplementary qualitative examples.

However, do not automatically move important evidence to the appendix simply to save space.

For every proposed appendix item, explain why a reviewer can understand and evaluate the main contribution without it.

## 7. FIND THE PAPER'S "ONE SENTENCE"

Produce several candidate one-sentence descriptions of the system's central contribution.

They must be factual and evidence-grounded.

Avoid generic phrases such as:

"an innovative end-to-end framework"
"cutting-edge architecture"
"comprehensive solution"
"novel AI-powered platform"

unless those claims are specifically justified.

The sentence should answer:

"What does this system allow someone to do that was previously difficult, fragmented, unavailable, or substantially less practical?"

## 8. OUTPUT

Return:

1. Evidence-based contribution diagnosis
2. Novelty audit
3. Functionality classification
4. Demonstration/video story
5. Main-paper content
6. Appendix content
7. Removable content
8. Necessary figures/screenshots
9. Proposed six-page section architecture
10. Claims that should be strengthened
11. Claims that should be weakened
12. Claims that should be removed
13. Research gaps or missing evidence that must be fixed before rewriting

Do not rewrite the manuscript yet.

Do not compress prose yet.

Do not optimize wording yet.

This stage is about deciding WHAT the paper should contain.





# Stage 2: what the six-page paper should emphasize

## Scope and status

- **No ground-truth YAML has arrived.** The uploads folder still holds only `main.pdf` and `main.tex`. Every "evidence" reference below means evidence inside the manuscript, not verified system facts.
- **Re-verified against `main.tex`:**
  - There is no demo, video or license link.
  - All 12 figures are placeholders.
  - PRISM-RAG has no method description.
  - The generator LLM is never named.
  - The knowledge base is never described (size, sources, license).
  - The provenance of the "200 authentic farmer queries" is never stated.
- **Two additions to the first audit.**
  - The mismatch-badge headline (453/454) pools 54 farmer cases with 400 "PRISM" cases, which appear to be constructed.
  - I read arXiv 2606.29243 v1, the benchmark paper. It lists two authors (Reza and Shahid) and a different title from both records in circulation. It contains no dosage verifier and no oracle-evidence experiment, and it recommends retrieval as future work (the paper lists the Knowledge Nodes, chemical whitelist and glossary as released under CC-BY-4.0, with MIT-licensed code). Check what the demo cites "Reza et al. 2026b" for.
- **Research coverage.**
  - I re-read the official CFP.
  - I sampled EACL 2026 demos by abstract, plus two full papers.
  - I read one ACL 2025 demo in full.
  - I searched for closely related agricultural and safety systems.
  - Track sizes: EACL 2026 received 102 demo submissions and accepted 44, and ACL 2026 received 227 submissions, counted 215 as valid with all required materials, and accepted 85.
  - I did not search EMNLP 2025 demos exhaustively. "Not novel" below means novel relative to what I found.

---

## 1. Evidence-based contribution diagnosis

**What the system primarily demonstrates.** A Bengali agricultural advisory app built so that risky situations end in a visible non-generative outcome instead of a fluent answer. The four outcomes are ask (missing crop), confirm (photo and text disagree), drop (dosage claim cannot be supported) and refer (unsafe or out of scope, to 16123). Each outcome is a distinct screen, and each answer is labelled by how it was produced.

**Smallest coherent set (the identity of the system)**
1. A crop-slot gate that blocks retrieval until a crop is known, with quick-reply chips and resume.
2. Retrieval scoped to the crop, taken from text or an on-device photo, with a confirmation state when the two disagree.
3. A dosage-claim check before display, with a per-answer origin badge and a visible drop audit.
4. A terminal referral path.

**Tiering**

| Tier | Items |
|---|---|
| Central | The four capabilities above, presented as one control-flow story |
| Supporting | Working memory (resume after clarification); on-device ONNX crop identification; grounded generation (name the LLM); T0 precheck (as the mechanism behind referral); offline PWA card |
| Secondary | SMS export, TTS, DialectSelector, non-chemical guidance card, evidence-conflict clarification (ConceptNormalizer plus Agreement Gate) |
| Implementation | INT8, WASM/SIMD, footprint, latency, service worker, tier accounting |
| Evaluation-only | 3,000-query routing probe, equivalence arm, 240-prompt pilot, trace ordering, live-vs-deterministic comparison, mutation harness, cost model |

**Alternative central stories**

| Story | Evidence for | Evidence against | What would change the ranking |
|---|---|---|---|
| **A. Visible control outcomes** (recommended) | Every outcome has a measured behavior: 76/200 halts; pilot 100/100 and 140/140; 53/54 real plus 400 constructed contradiction cases; mutation detection 33/33, 30/31, 22/25, 29/29; referral purity 16/16. Each is demonstrable | Each mechanism is simple and has prior art alone; evidence is operating-point and small-n; numbers need reconciling | A case study showing reviewers or users understand the states |
| **B. Fail-closed dosage verification** | Highest stakes; concrete mechanism; 0 false positives on 38 clean answers; guarded 2/210 vs unguarded 76/210 (my inference from the reported intervals) | Mutations are synthetic; ASR measures attack prompts, not everyday dosage error; Bangla-native residual is 10/100; SMS drops doses (0/84); dose-band source is undescribed | Verifier results on natural outputs of the deployed LLM, with dose-band coverage documented |
| **C. Deployable in low connectivity** | Local ONNX for 4 crops, PWA cache, 284 MB minimal install, 33.6 ms non-LLM overhead | 92.2% of turns still reach remote generation; TTS uses a cloud speech service; network loss is simulated; 160 Bengali characters exceed one SMS segment; offline diagnosis already exists | An end-to-end offline test with a local generator or cached-answer fallback |
| **D. Colloquial and dialect handling** | Prior retrieval study; DialectSelector; ConceptNormalizer | No evaluation of either; BM25 (the deployed retriever) scored 0.523 on colloquial queries in your prior paper, against 0.093 for dense; a prior Bengali agricultural system already injects colloquial-to-scientific keywords | An evaluation of both components on farmer queries |
| **E. "LLM only when needed"** | Halt path avoids retrieval | 7.8% zero-LLM turns and a 7.79% modeled saving; token medians are not comparable across paths | A tier mix where most turns avoid the LLM |

**Recommendation.** Use Story A, with B as its technically strongest component. Stories C, D and E fail on the manuscript's own numbers, not on ambition. If the YAML shows the verifier evaluated on natural outputs at scale, B could become the lead and A the setting.

**Candidate one-sentence descriptions (factual, evidence-bounded)**
1. *Story A:* "KrishokTech is a Bengali agricultural advisory web app that, for treatment questions, asks for a missing crop before searching, asks the farmer to confirm when a photo and the text name different crops, removes dosage claims it cannot tie to a source passage and permitted range, and refers unsafe requests to the 16123 helpline, labelling each answer by how it was produced."
2. *Story B:* "A pre-display check for Bengali agricultural advice that binds each generated dosage claim to a retrieved passage and a permitted range and drops what fails, with the drop shown to the user."
3. *Scoping variant:* "A Bengali agricultural advisory app whose answers are restricted to the crop the farmer or their photo identifies, and which stops and asks when the crop is unknown or contested."
4. *Contingent on new evidence (D):* "…maps colloquial or dialectal Bengali questions to standard forms and agronomic concepts before retrieval." I would not use this without an evaluation.

---

## 2. Novelty audit

| Our contribution | Closest prior | What prior already does | What we add | Difference type | Novel? | Wording |
|---|---|---|---|---|---|---|
| Crop-slot gate with clarification | Krishi Sathi; CLAM, Tree of Clarifications, RAC | Krishi Sathi collects missing details across turns before generating. Selective clarification is an established line of work (CLAM, Tree of Clarifications, RAC). A 2026 study finds LLMs recognize ambiguity but rarely ask clarifying questions | A rule-based crop check that blocks retrieval entirely, with Bengali chips | Interaction/functional | No for clarification; modest for the zero-retrieval crop gate | Soften to "we implement" |
| Crop-scoped retrieval | AgriRegion | Restricts the knowledge base and enforces geospatial constraints during retrieval | Crop as the constraint, sourced from text or photo | Functional | No | Soften |
| On-device photo → crop → retrieval scope | PlantVillage Nuru; Farmer.Chat | Nuru diagnoses offline on a phone and links to management information. Farmer.Chat accepts image, audio and video | Photo used as a retrieval scope; four measured crop models | Integration | No | Describe as a component |
| Text–photo mismatch confirmation | Deng et al. (CVPR 2025); CLASH | VLMs disproportionately trust text when it conflicts with the image. CLASH is a benchmark for cross-modal contradiction detection | A confirm-before-chemical-advice state; a deterministic check on crop labels | Interaction | Possibly distinctive as a design; cannot claim "first" | Do not present as solving VLM text bias (no VLM is used) |
| Dosage-claim verifier | AgroLLM; My Climate CoPilot; Digital Green evaluation | AgroLLM uses agronomic thresholds to guide retrieval and validate outputs. MyCC uses LLM self-evaluation on presentational and epistemic criteria. Digital Green treats dosage and banned-pesticide errors as acute risks | Passage binding plus dose-band check on generated sentences, with drop and audit | Functional/architectural at component level | Strongest candidate, still "we implement" | Verify AgroLLM's details before contrasting |
| Origin/provenance badges | SciTrue, ClinicalTrialsHub, Climate Finance, MyCC | Attribution and evidence traceability are recurring themes in the 2026 demos. MyCC shows the data and steps behind each answer | An answer-origin label that includes non-AI paths | Interaction | No | Small design feature |
| PRISM-RAG (memory, normalizer, routes, gate) | Krishi Sathi; Hossain et al. | Intent-slot flows; domain keyword injection to align colloquial farmer terms with scientific nomenclature | Not described | Unknown | Cannot be assessed | Drop novelty language |
| Deterministic-first routing to save LLM calls | FrugalGPT, RouteLLM (already cited) | Cost/quality routing | Conditional halts | Implementation | No; own data contradicts | Remove |
| SMS, offline, TTS | KrishokBondhu, Krishi Sathi, Nuru | KrishokBondhu delivers spoken Bengali answers through STT and TTS. Krishi Sathi adds speech input and output. Nuru works offline | Length-limited SMS packer; cached PWA card | Implementation | No | Captions only |
| Bengali system integrating these behaviors | KrishokBondhu; Hossain et al. | Hossain et al. translate to English, retrieve, and translate back; it is text-only, with about 15.6 s latency | Control and verification behaviors, photo input, local retrieval | Application + integration (+ resource if released) | Honest claim: an open Bengali system with these behaviors | Claim only after release is confirmed |

**Overall.** The contribution is application, integration and interaction design, with a stronger component in the verifier. It is not a new algorithm.

---

## 3. Functionality classification

| Functionality | Class | Evidence and rationale |
|---|---|---|
| Crop-slot gate + chips + resume | **MAIN PAPER** | Central; demonstrable; operating-point evidence; distinct only in combination |
| Crop-scoped retrieval | **MAIN PAPER** | Central; simulation only (gold routing); baseline discrepancy to fix |
| Text–photo mismatch confirmation | **MAIN PAPER** | Central; 53/54 real, 400 constructed; only comparative baselines exist in Appendix B.4 |
| Dosage verifier | **MAIN PAPER** | Central; strongest safety relevance; small synthetic evidence |
| Terminal referral + T0 | **MAIN PAPER** (as one outcome) | Demonstrable; T0 evidence is weak (refuse recall 0.493; off-topic 0/30) |
| On-device ONNX crop ID | SUPPORTING MAIN | Source of crop identity; 4 crops; small n (potato n=30) |
| Origin badges + drop audit | SUPPORTING MAIN | The UI of the verifier; needed for demonstrability |
| Grounded generation | SUPPORTING MAIN | Must name the LLM |
| Working memory | SUPPORTING MAIN | One sentence; enables resume |
| Offline PWA card | SUPPORTING MAIN | One sentence with caveat (simulated loss; cache diagnostic unclear) |
| Guidance card / partial-advice checklist | FIGURE/SCREENSHOT ONLY | Demonstrable; no evidence |
| SMS export | FIGURE/SCREENSHOT ONLY | Doses survive 0/84; multi-segment issue |
| TTS read-aloud | FIGURE/SCREENSHOT ONLY | No evaluation; cloud dependency |
| Evidence-conflict clarification | FIGURE/SCREENSHOT ONLY | Show only if it works live; no evidence |
| DialectSelector | FIGURE/SCREENSHOT ONLY | No mechanism or evidence |
| PRISM router internals, conformance | APPENDIX | 0.458 overall; 9.5% on document-RAG route |
| INT8, WASM, latency, footprint, ONNX parity | APPENDIX | Implementation; rice rejected, INT8 slower |
| Extractor analysis, equivalence arm, live-vs-deterministic | APPENDIX | Needed for honesty; reconcile first |
| 3,000-query routing probe | APPENDIX | Dangerous acceptance 0.374 (report plainly) |
| Tier mix, cost model, trace ordering | APPENDIX | Does not support the "LLM not default" claim |
| Voice input toggle | REMOVE | Appears only in a placeholder caption |
| "5-level answerability routing" as a contribution | REMOVE | Undescribed |
| Token comparison (89 vs 2,146) as savings | REMOVE | Different paths, not comparable |
| Modeled cost saving | REMOVE | 7.79% and modeled |

---

## 4. Demonstration / video story

**Ideal journey: one farmer, one sick crop, escalating uncertainty (about 2.5 minutes).**

| Time | Beat | Shows |
|---|---|---|
| 0:00–0:15 | Problem and what you are about to see | UI, one-line premise |
| 0:15–0:50 | Colloquial Bengali treatment question, no crop | Halt, zero sources, chips, choose crop, resume with cited sources |
| 0:50–1:25 | Rice photo, text says potato | On-device prediction, mismatch badge, chemical advice held, confirm |
| 1:25–2:00 | Fully specified question | Answer with origin badges; one dosage claim dropped with the audit line |
| 2:00–2:20 | Banned or unsafe request | Deterministic guard, 16123 referral |
| 2:20–2:30 | Access | URL, license, 3-second SMS/offline montage |

**Paper and video should divide the work.** The video carries interaction; the paper carries architecture, the evidence table, positioning, limits and access.

**One sentence or less in the paper:** TTS, SMS, offline card, working memory.

**Do not demonstrate:** INT8, WASM, DialectSelector (unless evidence exists), voice toggle, tier mix.

**Live-demo needs.**
- A no-login mode.
- Scripted "try this" inputs for each beat.
- A reliable way to trigger a drop live.
- An answer to what happens if the LLM key or quota is unavailable during review.

---

## 5. Main-paper content

Organised by the CFP's review questions.
- **Motivation, fit, novelty.**
  - Problem: Bangladesh's extension-agent ratio, and the risk of chemical advice.
  - Intended user.
  - The four outcomes, with an honest novelty statement.
- **Related work.** Verified systems only: KrishokBondhu, Farmer.Chat, Krishi Sathi, My Climate CoPilot, Hossain et al., AgroLLM, AgriRegion, Nuru. Add the clarification and text-bias literature in one sentence each.
- **System and demonstration.**
  - Architecture with the four outcomes marked.
  - Stack, including the named LLM and the knowledge base.
  - The demo scenarios.
- **Evaluation.**
  - One compact table for gate, fence, mismatch, verifier and safety.
  - The mismatch baselines from Appendix B.4.
  - Limits stated once.
- **Availability and licensing.** Demo URL, video link, repository, license, data provenance, hardware and API requirements.
- **Not needed in the main paper** (Section 6 lists where it goes): anything in the appendix table below.

---

## 6. Appendix content

| Item | Why a reviewer can judge the contribution without it | What main must still say |
|---|---|---|
| PRISM conformance table | Not a claimed contribution once reframed | One line: routes exist and are unevaluated |
| INT8, WASM, footprint, ONNX parity | Not part of the identity | Footprint number if offline is mentioned |
| Extractor agreement/miss, equivalence arm, live-vs-deterministic | Supports gate honesty, not the demo | A sentence flagging single-reviewer labels |
| Routing probe (3,000) | Offline stub, not the live system | Refuse-recall caveat |
| Per-mutation verifier counts | Summary suffices | Aggregate range and the small-n caveat |
| Tier mix, cost, trace ordering | Do not support a headline | Nothing, or one honest line |
| Additional UI states, prompts, failure ledger | Extra views | Pointer |
| Scripted "try this" inputs | Helps reviewers use the live demo | Mention that they exist |

---

## 7. Removable content

- Voice-input toggle (unless verified).
- The "5-level answerability routing" and "typed working memory" novelty claims.
- The 89 vs 2,146 token comparison as a saving.
- Modeled cost as a benefit.
- The CVPR "When visuals disagree" citation.
- Farmer statistics beyond one or two verified ones.
- §3.6 (it restates 3.1–3.5) and the conclusion's restatement of results.
- Roughly 40 of the 43 defensive hedges.

---

## 8. Necessary figures and screenshots

1. **F1 architecture:** the pipeline with the four outcomes as coloured exits.
2. **F2 real annotated screenshot,** ideally one session, showing chips, mismatch badge, origin badge and dropped-claim audit.
3. **F3 storyboard,** maybe as F2's panels: the halt-and-resume and photo-mismatch sequences.
4. **T1 rebuilt comparison table** on verified sources, fewer rows, with cells that can be defended.
5. **T2 compact evidence table.**

No results chart is required. Two of the six pages should be visuals.

---

## 9. Proposed six-page section architecture

| Section | ≈Pages | Establishes | CFP question |
|---|---|---|---|
| Abstract | 0.25 | Four outcomes, access link, one scoped result | Motivation/fit/novelty |
| 1 Introduction | 0.6 | Problem, users, contributions (≤3), links | Motivation/fit/novelty |
| 2 Related work | 0.4 | Verified positioning | Related work |
| 3 System | 1.3 | Architecture (F1), stack, knowledge base, four outcomes | System and demo |
| 4 Demonstration | 1.5 | UI (F2), storyboard (F3), scenarios | System and demo |
| 5 Evaluation | 1.2 | T2, baselines, honest limits | Evaluation |
| 6 Availability, limitations, conclusion | 0.55 | URL, license, data, scope | Availability/licensing |

Ethics/broader-impact goes after page 6 at no page cost. Cover farmer data and consent, pesticide safety, human oversight, LLM provider data handling, and single-reviewer labels. If the field-survey queries come from your benchmark, its paper describes an IRB protocol you could reuse. Confirm before citing it.

---

## 10. Claims that should be strengthened

- **Mismatch handling.** Bring the Appendix B.4 baseline results into the main text. Note that a prompted LLM judge reached 0.0% cross-crop advice at about 1.5 s, so the honest advantage is latency, determinism and cost, not safety.
- **Verifier.** Support it with results on natural outputs of the deployed LLM, not only mutations.
- **Gate.** Report precision and recall of the halt decision against gold "should halt" labels, with a second annotator.
- **Provenance.** Even a small expert or team feedback round on the scenarios would qualify as a case study.
- **Availability.** Add the license and release facts.

## 11. Claims that should be weakened

- "Halted 76/200 **ambiguous** queries" → halts, not ambiguity.
- Fence result → "under gold-routing simulation; wrong-crop advice remains 30%".
- "0.95% dangerous advice" → "attack success, n=210 per arm; Bangla-native 10/100" (after reconciliation).
- Offline → "local retrieval and cached card; loss simulated".
- SMS → "160-character export; doses not preserved".
- TTS → "cloud speech service; not evaluated".
- Off-topic scope handling → do not claim it (0/30), and note that Hossain et al. report robust out-of-domain rejection.
- Table 1 "only ours" rows → limit to differences you can defend.

## 12. Claims that should be removed

- "We introduce PRISM-RAG" as a novelty contribution.
- "The LLM is not the default path" (92.2% reach generation).
- Any "first" or "novel" language not backed by the Section 2 audit.
- The "MC ✓†" cell.
- Unverified competitor cells (KrishokBondhu TTS, Krishi Sathi image diagnosis).

---

## 13. Research gaps to fix before rewriting

**Blocking**
1. YAML.
2. Demo URL, video and license.
3. Generator LLM identity, hosting and quota behavior during review.
4. Knowledge-base description (sources, size, license, whether it is the benchmark release).
5. Dose-band source and coverage (crops and chemicals).
6. Reconcile the numbers from the first audit: n per arm, Bangla-native 10/100 vs 2/210, the two 0.30 baselines, the offline "0/400" diagnostic, and the source of the 60-row quality review.
7. Provenance of the 200 farmer queries and the 400 "PRISM" cases.

**Evidence that scoping can cover, if there is no time for new experiments**
8. Case-study logs of the scenarios (the CFP accepts case studies and qualitative feedback).
9. A plain-RAG baseline on the same queries, if one exists.
10. Real (not held-out dataset) photo results. Nuru's in-field accuracy was 65%, against 40–58% for extension agents, which shows field numbers differ from benchmark numbers.

**Facts to confirm**
11. That 16123 is the current helpline, and that routing users there is authorized.
12. Overlap with your sibling manuscripts.
13. What "Reza et al. 2026b" is cited for, given that v1 lacks the verifier.

**Clock.** The deadline is 22 Sep, 11:59 pm AoE. If the live link, video and real screenshots cannot exist by Sunday, the submission is not viable this cycle regardless of how good the plan is.

Send me the YAML and the demo status first. I will lock the facts against them before any drafting.