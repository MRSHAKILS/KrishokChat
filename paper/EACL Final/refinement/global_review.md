# KrishokTech: EACL 2027 demonstration and narrative audit

**Diagnostic only — no manuscript rewrite.** Reviewed 22 September 2026.

## Overall assessment

This is a serious demonstration paper with a coherent system contribution and substantial prototype evidence. Its strongest contribution is already present: explicit control over whether generation may proceed, which crop-specific evidence it may access, when the user must resolve a conflict, and which dosage claims may be displayed. The concrete opening example, ASK/CONFIRM/REFER/DROP states, three evaluation questions, narrow description of dosage verification, and explicit absence of field-effectiveness claims should be retained.

The manuscript does **not** need a new research story or a much larger experimental program. It does need several consequential corrections before submission. The most serious are internally inconsistent evidence counts, a retrieval metric described as generated advice, an unexplained conflict between hard fencing and residual contamination under oracle routing, inconsistent deployment/privacy statements, and availability claims that differ from the linked public artifacts. These are concentrated problems, not evidence that the entire paper is unsound. I would not assign a percentage of the paper that is “broken”; that would conceal the unequal importance of the findings.

### Scope and evidence standard

I read the supplied 13-page PDF, its complete LaTeX source and bibliography, the official CFP, the substantive full texts and appendices of the five comparison demonstrations, and the two cited prior KrishokChat papers. I visually inspected all manuscript pages and selected architecture/interface pages from the comparison papers. I also checked the public website, screencast metadata, repository license/README, and linked model repository.

The experiment logs, evaluation scripts, dataset manifests, ethics documentation, and deployed implementation were not supplied as audit inputs. Therefore, **“measured” below means reported as measured in the manuscript**, not independently replicated here. The audit independently checks arithmetic, internal consistency, what the described measurement can establish, visual presentation, and selected public metadata. It does not certify production behavior, legal permissions, model accuracy, or research approval. I did not submit farmer data or exercise the live advice workflow.

Locations use the supplied PDF page numbers and `main.tex` line numbers. Repeated claims in the abstract, tables, conclusion, and ethics statement are grouped with their underlying experiment rather than counted as independent evidence. Originals were preserved.

## 1. Prioritized diagnostic

### Critical before submission

**C1. Correct the retrieval endpoint and resolve the hard-fence inconsistency.** In §5.2, line 232, “wrong-crop advice” means that at least one of the top five retrieved sources belongs to another crop. No generated-advice outcome is measured by this definition. Call it a retrieval contamination rate everywhere, including the ledger. More fundamentally, §3.2 says other-crop passages cannot enter the candidate set, but the ledger reports 30% contamination even with oracle crop routing. That requires a concrete explanation: crop-tag versus passage-content disagreement, mixed-crop passages, a different experimental implementation, a different reference crop, or another documented cause. These are possibilities, not findings. Publish the actual invariant and explain the residual. Also separate contamination among answered queries from the effect of halting queries entirely.

**C2. Reconcile the cloud attack counts before using them as headline evidence.** The cloud ledger reports 210 calls per arm and 0.95% guarded ASR, implying 2 successful attacks. It also calls the Bengali-native set a subset of 100 with 10% guarded ASR, implying 10 successes. Ten successes cannot be contained in two. The possibility of distinct suites must be verified from logs and explicitly labeled, not assumed. The deployed model uses 280 calls per arm, whereas the cloud row uses 420 total; the table mixes per-arm and combined denominators. Embedded/roleplay failure counts also appear under different models in prose and ledger. See ledger items E21–E24 below.

**C3. Reconcile the multi-turn suite membership.** The five rows total 275 dialogues and 575 turns if disjoint, while the reported total is 200/425. The difference is exactly the 75-dialogue, 150-turn crop-topic-shift row, suggesting that “Cross-Crop Hazard” may be a second outcome on that same cohort. If so, say four dialogue cohorts and five checks, and mark the shared rows. Do not sum them twice or call an undefined aggregate “100% robustness.” Clarify whether chemical leakage was assessed in generated advice or inferred from cleared memory slots.

**C4. State the actual execution modes consistently.** Line 139 says the connected live website uses cloud generation; line 286 says cloud calls were limited to offline benchmark evaluation. These cannot both describe the same release without qualification. Add a compact mode specification identifying browser/local/server components, model, what text leaves the device, what happens to images, and which controls run in each mode. Retain absolute privacy or zero-retention claims only for the configuration and agreement actually verified. Account for the LLM classification branch in the off-topic audit and the T2 fact-lookup bypass in the cost analysis.

**C5. Correct the release and license descriptions against a frozen artifact manifest.** The public code repository’s current LICENSE is MIT, while the paper says Apache-2.0. The linked Hugging Face repository is labeled Apache-2.0 and lists vision/soil assets; its file listing did not identify the claimed 4B language-model checkpoint or 2,135-node evidence release. The paper also assigns CC-BY-4.0 to that model and dataset. Provide distinct, exact links and licenses for code, vision models, language-model weights/adapters, and derived evidence. Specify inherited restrictions rather than assigning one blanket license. Public checks support a mismatch, not a conclusion that the missing artifacts do not exist elsewhere. [Code license]([https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System/blob/main/LICENSE](https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System/blob/main/LICENSE)); [model files]([https://huggingface.co/RaiyanKhaan/KrishokTech-Models/tree/main](https://huggingface.co/RaiyanKhaan/KrishokTech-Models/tree/main)).

**C6. Repair promised but missing methods.** Appendix A currently promises decision rules, thresholds, interfaces, extractor evaluation, and a provenance badge taxonomy; it supplies almost none of those details. It contains a one-sentence badge description and the Banglish table. The vision confidence/margin thresholds explicitly referenced from §3.2 are absent. Restore a concise specification of crop binding, confidence/ambiguity decisions, conflict precedence, resumption after ASK/CONFIRM/REFER, and verifier matching. Report extractor accuracy separately from annotation agreement. Withholding exact T0 patterns does not prevent publishing these interfaces and decision rules.

**C7. Make the demonstration state transitions credible and the screenshots readable.** S1 binds potato; S2 introduces a rice photo and silently scopes the session to rice; S3 then demonstrates a rice/potato conflict. Explain the crop change or explicit reset between S1 and S2. Show how S3 is resolved and what permits S5 to resume after referral. If the displayed 10× overdose is a deliberately injected draft, label that intervention; do not imply a spontaneous live model error is reliably reproducible. Figure 2 is too small to read the evidence for the claimed states. This is a demonstration-track issue, not merely cosmetic.

**C8. Narrow the delivery and footprint claims.** “Full installation” at 339.6 MB cannot include approximately four billion parameters stored at four bits each: weights alone are roughly 2 GB before overhead. State which assets are counted. SMS length in characters is not enough to establish one-message delivery in Bengali: the common limits are 160 GSM-7 characters or 70 UCS-2 characters for one segment, with lower per-segment limits for concatenation. State the output encoding and measure segments. A retained dosage with the chemical name missing is not established as safe actionable advice. [SMS encoding documentation]([https://www.twilio.com/docs/glossary/what-sms-character-limit](https://www.twilio.com/docs/glossary/what-sms-character-limit)).

### Strongly recommended

1. **Position the contribution directly against the authors’ two prior papers.** Identify reused data, checkpoint, normalization, and retrieval resources, then state the added runtime controls and inspectable interaction. This avoids an unnecessary “repackaged benchmark” impression without alleging overlap.
2. **Keep one contribution hierarchy.** C1 admission/referral, C2 evidence binding/conflict handling, and C3 dosage release already organize the paper. The introduction’s different three-item list—controls, edge knowledge, multilingual normalization—competes with that structure. Treat normalization, external knowledge, and deployment as enabling properties of the same integrated system.
3. **Move attack interception evidence to the control that performs it.** The headline table labels the attack guard C3, while the paper attributes pre-generation interception to T0/C1. Separate precheck interception, full-pipeline ASR, and post-generation verification. Their causal contributions are not interchangeable.
4. **Separate positive conflict detection from false-positive measurement.** The 454 conflict cases cannot establish zero false halts on non-conflicting inputs. Supply the negative-set denominator if it already exists; otherwise remove that claim pending a small benign-control check.
5. **Use a release/version crosswalk.** The manuscript reports 2,135 nodes and BM25-only evaluation; the public README reports 2,120 nodes and a hybrid retrieval/classification flow. Freeze a commit and dataset version so these are identifiable releases rather than apparent contradictions. [Public repository]([https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System](https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System)).
6. **Resolve data provenance and ethics cohort identity.** Map the 200 gate queries and 54 farmer conflict cases to collection source, identifiers, reuse status, consent, and approval coverage. Do not generalize the approval for one collection to another. The earlier benchmark’s collection description differs; this may simply be a different cohort. See §3 below.
7. **Define operating conditions for latency.** Distinguish the 4.2-second gate classifier, 1.8-second cloud answer generation, approximately 24-second local generation, and 33.565-millisecond stub-LLM overhead. Add hardware, input/output length, sample counts, and warm/cold conditions where available.
8. **Reconcile the recorded demo with the written demo.** The screencast page’s schedule begins with REFER and extends to 2:30, whereas §4 claims the same ASK-first S1–S5 order. The video element reports about 48.7 seconds. That duration is within the limit; the issue is inconsistent descriptions, not an overlong video. I checked metadata, not complete audiovisual coverage. [Screencast page]([https://krishoktech-one.vercel.app/screencast](https://krishoktech-one.vercel.app/screencast)).
9. **Correct verified bibliographic metadata errors.** Five concrete examples appear in §8. These are targeted primary-record checks, not a claim that every bibliography field has been validated.
10. **Restore ordinary template layout and rebalance space.** The source uses multiple `enlargethispage` adjustments, including a large one before §6. Check the result against the official template rather than assuming compliance. Page 6 leaves substantial space in its right column; Appendix page 12 is sparse while page 13 squeezes the evidence ledger. Improve readability before shrinking more text.

### Optional polish

- Shorten the citation stack in the opening motivation; retain the concrete farmer question.
- Replace “six staple crops” with “six supported crop groups” if that better matches brassica and the implementation’s labels.
- Standardize “Banglish,” “Bengali-native,” “farmer cases,” “queries,” “calls,” “outputs,” and “mutations.” These are different units.
- Reduce repetition of the authority-boundary statement in the abstract, introduction, design principle, and conclusion; each should add information.
- Clean unused or duplicate BibTeX entries after correcting cited records. Duplicate unused POPE entries are a cleanup issue, not a scientific blocker.
- Retain useful qualifications already present, especially the narrow verifier scope, the statement that a provenance badge does not prove causal citation use, and the absence of field-effectiveness claims.

## 2. Track fit and accepted demonstration conventions

### Official requirements and current fit

The 2027 CFP allows six content pages, with optional ethics and unlimited references/appendices. It requires a paper, a video of at most 2.5 minutes, and a live system or installable package; demo/package and video links belong in both the PDF and submission form. Review is single-blind. Prototype evidence can be limited in scale; a comprehensive experimental campaign is not required. Availability and licensing should be explicit. [Official EACL 2027 demonstration CFP]([https://2027.eacl.org/calls/demos/](https://2027.eacl.org/calls/demos/)).

The supplied PDF places its main text on pages 1–6, ethics/references on pages 7–9, and appendices on pages 10–13. Both public links responded during this audit. I did not inspect the OpenReview submission or test a fresh installation, so those requirements remain checks for the authors, not certified completed items.

| Review question | Diagnosis | Proportionate action |

|---|---|---|

| Concrete problem | Clear: underspecified, conflicting, or risky Bengali agricultural questions can receive fluent but unsuitable advice. | Keep the concrete example; lead with the missing decision, not general agricultural transformation. |

| Relevance to NLP | Clear but disperses across capabilities: colloquial language normalization, information-state extraction, multimodal contradiction, evidence-conditioned generation, and constrained release. | Connect each language capability to an admission, evidence, or release decision. |

| System novelty | Plausible integration contribution; generic deterministic checks, RAG, and local models are not individually new. | Specify the implemented ordering, state transitions, and crop/dosage semantics; position against prior work. |

| Intended users | Farmers and extension officers are implicit; the demonstration audience is explicitly researchers/practitioners. | Distinguish end users from conference attendees and explain officer-assisted/offline use briefly. |

| Attendee experience | Five concrete steps exist, but their continuity is not yet consistent. | Repair state transitions, identify editable inputs, and show successful continuation after a halt. |

| Visible functionality | Architecture is visible; UI evidence is too small. | Enlarge decisive input/state/source/Why-panel areas and give short English glosses for Bengali text. |

| Evidence of prototype quality | More than enough kinds of evidence; some reported outcomes are not interpretable until reconciled. | Correct counts and endpoint semantics before adding volume. |

| Availability/licensing | Working links are a strength; exact artifacts, versions, licenses, and modes are unclear. | Publish one accurate release manifest and match the manuscript to it. |

### What the accepted papers actually suggest

These papers inform conventions, not a mandatory template or a standard of agricultural safety. I read their full substantive content rather than relying on abstracts.

| Paper | Relevant observed convention | What KrishokTech should take from it |

|---|---|---|

| **My Climate CoPilot**, ACL 2025 | Identifies agricultural advisors and their tasks early; connects a staged architecture to a large, legible interface with data/literature views. Evaluation includes expert/user feedback and query analysis. It explicitly was not publicly available at publication (§5.5). | Make the target actor and evidence-inspection action concrete. Do not treat a 2025 paper’s access exception as permission to ignore the 2027 CFP. [Full paper]([https://aclanthology.org/2025.acl-demo.7.pdf](https://aclanthology.org/2025.acl-demo.7.pdf)). |

| **RAGVUE**, EACL 2026 | Organizes around diagnostic retrieval/answer/faithfulness questions, supplies API/CLI/UI entry points, and uses 100 constructed QCA triplets plus qualitative analysis. Larger interface examples appear in the appendix. Code is Apache-2.0. | A focused constructed evaluation can establish prototype behavior if its unit and limitations are explicit. Judge agreement is not automatically correctness. [Full paper]([https://aclanthology.org/2026.eacl-demo.35.pdf](https://aclanthology.org/2026.eacl-demo.35.pdf)). |

| **FactSearch**, ACL 2026 | Exposes prompt/response input, verification controls, and expanded claims with supporting sources. A dedicated demonstration narrative and a 50-question-pair evaluation keep the contribution tied to an inspectable workflow. | Show the attendee’s action and the system’s visible consequence. A compact evaluation can suffice. Availability links should not be mistaken for an explicit license statement. [Full paper]([https://aclanthology.org/2026.acl-demo.36.pdf](https://aclanthology.org/2026.acl-demo.36.pdf)). |

| **The AI Committee**, EACL 2026 | Specifies input schema, configuration, staged validation, status, and export. Its design includes a deterministic Arbiter after upstream judgments. Evaluation covers three datasets and ablations; code is Apache-2.0. | Do not present “deterministic authority after LLM output” as unprecedented by itself. The agricultural crop-binding and release workflow must carry the specific contribution. [Full paper]([https://aclanthology.org/2026.eacl-demo.41.pdf](https://aclanthology.org/2026.eacl-demo.41.pdf)). |

| **MED-COPILOT**, ACL 2026 | Identifies clinicians/trainees, connects recommendations to guidelines and similar cases, and exposes evidence controls in the interface. It reports benchmark evaluation while explicitly lacking clinical validation/user study. | Prototype utility and domain effectiveness are distinct. KrishokTech can make a useful demo claim without pretending to have farmer-field validation. [Full paper]([https://aclanthology.org/2026.acl-demo.49.pdf](https://aclanthology.org/2026.acl-demo.49.pdf)). |

Across these examples, effective concision comes from concrete actors, inputs, outputs, and limitations—not a universal section order or uniformly tiny evaluations. KrishokTech already has enough technical substance to follow those conventions in its own form.

## 3. Strongest existing story and self-comparison

### Recommended paper thesis

KrishokTech is a Bengali agricultural advisory prototype that places explicit controls around a language model. Before an answer is drafted, it checks whether a treatment request identifies a crop, binds retrieval to that crop, and asks the farmer to resolve conflicting text and image evidence; policy-covered high-risk requests are referred to a human service. After generation, a separate verifier withholds unsupported dosage claims. The demonstration makes these decisions visible through ASK, CONFIRM, REFER, and DROP, with source traces and connected or local delivery options. Its contribution is this integrated, inspectable workflow; the evaluation supports particular control behaviors on bounded test sets, while leaving residual failures and field usefulness unresolved.

### Assessment of the proposed framings

| Framing | Judgment |

|---|---|

| Deterministic authorization around a probabilistic generator | Strong organizing principle, conditional on an accurately described implementation. Deterministic enforcement still receives fallible extracted slots, crop predictions, and source metadata. It is not an oracle of safety. |

| Bengali/Banglish-aware control | Supported for specified normalization and the constructed 85-attack/15-benign test. Not evidence of complete dialect or script coverage. |

| Multimodal evidence binding | Strong demonstration mechanism: attach a photo, bind a crop, expose conflict, require confirmation. Separate crop routing from disease classification. |

| Crop-fenced retrieval | Central and useful, but its claimed invariant and measured contamination must agree. |

| Independently updateable evidence | Credible architectural property of an external index. Avoid calling external RAG knowledge a new invention; document versioning and the limits of adding new crop support. |

| Edge deployment and explicit referral/release | Valuable supporting property. Define what runs locally, account for the language model’s size/latency, and distinguish a displayed referral from successful human assistance. |

| Inspectable ASK/CONFIRM/REFER/DROP | The strongest demo-facing expression of the contribution. It needs legible screenshots and a consistent session. These states should organize the attendee experience, not become four extra grand contributions. |

### What is prior and what this demonstration adds

The prior **KrishokChat** benchmark already contributes Bengali agricultural data, provenance, chemical-advice/safety tasks, dialect coverage, and a fine-tuned checkpoint. Its current title is *KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory*. The present contribution should be the runtime integration and demonstrated enforcement, not the invention of those resources. Its collection/permission descriptions also warrant a cohort and license crosswalk: the earlier field-interview account lacks formal IRB review, whereas this manuscript describes institutionally reviewed extension logs; these may be different collections. The earlier release describes a more restrictive noncommercial/share-alike data license. Resolve reuse and permissions without assuming either misconduct or that a new blanket license overrides inherited terms. [Prior benchmark, full text]([https://arxiv.org/pdf/2606.29243](https://arxiv.org/pdf/2606.29243)).

The prior **Where Does Retrieval Fail?** paper evaluates retrieval architectures and language conditions over an existing agricultural corpus. Its image-linked resources are not an evaluated multimodal advisory interaction. Treat retrieval benchmarking and corpus construction as prior; crop authorization, interactive conflict resolution, and release enforcement are the new demonstration’s intended additions. Provide a corpus-version crosswalk, including why its 2,882-node resource differs from the present 2,135 nodes. A different number does not itself establish new data or problematic overlap. [Prior retrieval study, full text]([https://arxiv.org/pdf/2608.14886](https://arxiv.org/pdf/2608.14886)).

A short explicit comparison in Related Work is sufficient. The manuscript currently cites these papers but leaves reviewers to reconstruct the boundary. I found no basis in this audit to accuse the submission of impermissible overlap; novelty attribution needs clarification.

## 4. Section-by-section narrative map

| Section | Preserve | Change or relocate | Purpose in the story |

|---|---|---|---|

| Title and abstract | System identity, Bengali setting, admission/evidence/release principle. | Use corrected metrics; distinguish farmer and synthetic conflicts; avoid an inventory of every subsystem and result. | Say what the system controls and what the demonstration establishes. |

| Introduction | The yellow-leaf/pesticide example and ASK/CONFIRM/REFER/DROP. | Align the contribution list with C1–C3; identify farmers/officers; use one sentence for updateable knowledge and deployment. | Concrete failure → design principle → contribution. |

| Related Work | Localized advisors, clarification, verification, script variation. | Add explicit self-positioning; compare mechanisms rather than accumulate names. Do not claim other systems never clarify/refuse or use deterministic checks. | Explain what this particular integration adds. |

| System Design | T0–T4 ordering, gate before retrieval, untrusted draft, narrow T4 scope. | Distinguish learned inputs from deterministic rules; disclose additional classifier/bypass paths; define crop authority and reset behavior. Move model training/storage minutiae to deployment details. | Establish the operational boundary before measurements. |

| Architecture figure | Ordered flow and outcomes. | Make every actual path visible, including no-generation termination and delivery after verification. | Let a reader predict system behavior. |

| Demonstration | Five actionable scenarios and free/preset inputs. | Repair continuity; show confirmation and resumption; reconcile recording order; label injected draft errors. | Demonstrate the boundary through user actions. |

| Interface figure | Real screenshots and source/Why views. | Crop irrelevant browser whitespace, enlarge decisive content, add English glosses; prioritize visible state transitions over miniature full screens. | Supply visual evidence of inspectability. |

| Evaluation | Q1/Q2/Q3 and paired/control experiments. | Rename retrieval endpoint; repair counts; place attack blocking under the right control; keep dose-check coverage and residuals explicit. | Test each design decision using its actual outcome. |

| Evaluation scope | Constructed/synthetic/network and non-field limitations. | Keep a concise summary; avoid repeating it verbatim in §6 and ethics. | Prevent proxy-to-outcome overreach. |

| Limitations/availability/conclusion | Residual failures, six-crop coverage, slow local generation, support for officers. | Correct release/mode details; distinguish updating evidence from adding a complete new crop pipeline. End with the demonstrated contribution, not a new claim. | State practical boundaries and how to access the prototype. |

| Ethics | Data minimization, human oversight, policy rather than regulatory classification. | Resolve approval cohorts, live-cloud statement, image handling, and absolute emergency/fail-closed wording. | Match governance statements to actual modes and data. |

| Appendix A | Space for reproducible decision logic. | Fill the missing thresholds, badge definitions, interfaces, extraction metrics, and gate methods. | Make the main design auditable. |

| Appendix B | Separate deployment and constrained-delivery tests. | Clarify SMS encoding/semantics, footprint exclusions, stub latency, and cost assumptions. | Support deployment claims without expanding the headline contribution. |

| Appendix C | Full gallery. | Enlarge readable views; include the alternate delivery channels promised by the cross-reference, or correct that reference. | Show what the attendee can inspect. |

| Appendix D | Constructed state-transition checks. | Declare overlapping cohorts and distinguish state integrity from generated chemical safety. | Bound the multi-turn claim. |

| Evidence ledger | Explicit status and scope is a valuable feature. | Use one unit per denominator; allow mixed statuses; include omitted results such as trace ordering; improve page layout. | Make every numerical claim traceable. |

The introduction is not excessively dominated by generic agricultural motivation. The larger ordering problem is repeated framing plus a dense collection of subsystem results whose relationship to C1–C3 is not always explicit. Do not replace the introduction wholesale.

## 5. Complete claim–evidence ledger

**Status notation:** M = reported direct measurement; P = controlled pilot; S = simulated condition; D = derived/modelled quantity; A = architectural, policy, or availability assertion without a corresponding measurement supplied. “Constructed” describes the sample and can coexist with M; it is not the opposite of measured. A measurement under simulated noise needs both labels. Counts inferred arithmetically below are consistency checks, not recovered raw observations.

### Admission, annotations, and gate comparisons

| ID / source | Claim, denominator, and actual endpoint | Status and required scope/action |

|---|---|---|

| E01 — §5.1, L224; headline L210; ledger L496; abstract | 30/30 crop-less treatment queries halt; 170/170 crop-specified queries pass, in 200 authentic queries. The 15% is the cohort’s halt prevalence, not a general detection rate. | M. Strong bounded result. State the selection process and crop-presence gold labels. “No false halts” is supported on these 170 negatives, not all farmer questions. |

| E02 — §5.1 L224; ethics L278 | Crop-presence agreement 100%, κ=1; normalized 37-crop taxonomy agreement 99.5%, κ=.9945; intent agreement 93.5%, κ=.8958. Apparently the same 200 queries, but make that explicit. | M, annotation reliability. None is extractor accuracy. Report system-versus-gold results if claiming extraction accuracy; identify adjudication and any evaluation/tuning separation. |

| E03 — §5.1 L226; ledger L500 | LLM halt rate 10% versus gate 15%; agreement 91%; median gate-decision latency 4,218.6 ms on 200 queries. | M. Halt frequency is not detection quality. If all three percentages are exact on the same set, they imply LLM TP=16, FN=14, FP=4, TN=166. Verify and publish the actual confusion matrix rather than leave readers to infer it. Specify model/prompt and timing conditions. |

| E04 — ledger L500 | Fourteen reviewed answers, 7/14 “medium or better.” | P/descriptive despite row’s M label. Define rating categories and selection; no population quality or coverage claim. Keep out of the headline. |

| E05 — ledger L498 | 100/100 constructed ambiguous requests halt; 114/140 specified requests pass directly; 26/140 require bounded clarification. Total 240. | P. Valid conformance evidence. The 26 clarifications do not automatically contradict E01: cohorts and slot requirements may differ. Explain the distinction; do not describe all specified requests as universally passed. |

| E06 — ledger L499 | Median 89 clarification tokens versus 2,146 retrieval-context tokens over a 200-query set. | M, different quantities. Not a measured total-token saving from paired complete executions. Existing “separate medians” qualification is good. Give tokenizer and counted spans. |

| E07 — §3.1 L125 | Missing-crop treatment requests stop before retrieval with `sources_retrieved=0`; six regional normalization presets. | A supported in part by E01. Define treatment intent, unknown/implicit crop handling, and session carryover. Six implemented presets do not establish six-dialect accuracy. |

| E08 — Appendix A, L326–331; §5.3 L239; ledger L526 | 85 constructed attacks: 35 phonetic chemicals, 25 crises, 25 sabotage. Formal-only baseline catches 1/85; normalized precheck 85/85; both pass 15 benign controls. | M on a constructed stress suite. Retain 85/85 and 0/15 with scope; no universal evasion resistance. Table columns switch meaning from “blocked” to “passed” on the benign row: label the outcomes. Split crisis referral destinations according to the stated emergency policy. |

### Vision, retrieval boundaries, and conflict handling

| ID / source | Claim, denominator, and actual endpoint | Status and required scope/action |

|---|---|---|

| E09 — §5.2 L232; ledger L503 | Top-1 .9413–.9907 across six crop-specific disease classifiers; 4,294 test images. | M. Disease classification conditional on crop is not crop-identification accuracy. Give per-model test sizes, source/split provenance, and label sets. No inference of field-image performance. |

| E10 — ledger L503 | 100% ONNX/PyTorch prediction agreement. | M, equivalence check. State number of paired inputs, preprocessing, model versions, and whether this means labels or full scores. The row’s 4,294 may be the intended denominator; it is not explicitly assigned to this check. |

| E11 — ledger L504 | Wheat INT8: 5.92→1.61 MB, 3.68× smaller, 0 percentage-point accuracy change on 400 images. Potato .09-point drop, n=1,170; brassica 0-point drop, n=443. | M. Keep as storage/accuracy trade-off, not evidence of improved diagnosis or faster execution. The row-wide n=400 applies only to wheat. |

| E12 — ledger L504 | INT8 latency is 1.5–2× higher on non-VNNI x86; rice loses 2.5 points, exceeds a 2-point release threshold, and was not deployed. | M plus A release decision. Specify devices, repetitions, and affected models; retain the non-speedup caveat. Identify the deployed rice artifact and the threshold’s provenance. |

| E13 — ledger L505 | Family assignment 433/437, approximately 99.08%; wheat-800 excluded. | M. Define family labels, errors, exclusion reason, and whether this covers every route used in the demo. It does not validate open-world crop identification. Do not substitute disease accuracy or this family accuracy for an unexplained ~5% routing-noise parameter. |

| E14 — §5.2 L232; ledger L506; headline L211; abstract | Top-five cross-crop-source rate: 36.25% open, 31.25% routed, 28.75% routed+gated; oracle 30%, all n=400. Equivalent rates are 145, 125, 115, 120 queries if all share the denominator. | M; add S if routing errors were sampled to imitate empirical noise. Name it retrieval contamination. Report crop reference, passage labeling, routing mechanism, halt count, attempted retrieval count, and answer coverage. Explain oracle residual under a claimed hard exclusion. A gate that answers less can reduce total-query contamination without improving retrieval on answered queries. |

| E15 — ledger L506 | Oracle/open comparison has 25/0 discordant pairs, exact McNemar p≈5.96×10⁻⁸. | D from paired outcomes. The stated p-value is arithmetically compatible with those counts. It supports that comparison only—not the noisy+gate endpoint or generated-advice correctness. Preserve paired identifiers. |

| E16 — ledger L497 | Text-only gate comparison 30.25%→28.75% on 400 queries; 6/0 discordant pairs; p=.03125. | M/D. Rates imply 121→115 contaminated queries. The p-value fits the given discordances. Keep distinct from E14: sharing the 28.75% endpoint does not make the experiments interchangeable. “Without penalty” needs its own defined pass/coverage outcome. |

| E17 — §5.2 L234; ledger L507; abstract/headline | Conflict detection 53/54 farmer cases and 400/400 synthetic PRISM cases, combined 453/454. One miss involves an implicit crop reference. | M on two different sources. Foreground the stratified counts. Do not call the whole suite “explicit contradictions” while describing an implicit miss; define eligibility and recognized conflict type. Constructed success does not establish real-world conflict robustness. |

| E18 — same sources | “No false halts” for the mismatch badge. | No negative denominator supplied. All 454 are described as conflict positives. Identify the non-conflicting cohort and count; otherwise remove the false-positive claim. Do not borrow the gate’s 170 negatives, which test another mechanism. |

| E19 — §5.2 L234 | On a separate 300-conflict set, prompted LLM clarification 20%, naive multimodal RAG 13%. | M; exact counts and baseline configuration missing. If percentages are exact, they imply 60 and 39 cases. These are not a matched comparison to 453/454. Evaluate/describe the same cases if retaining a direct superiority claim; otherwise present separately. |

| E20 — §3.2 L132–134 | Three-way vision routing; deterministic crop fence; within-crop diagnostic clarification. | A. Confidence/margin thresholds are absent from the promised appendix. Specify binding and precedence. E17 tests cross-crop mismatch, not all contradictory diagnoses within a crop. No dedicated within-crop diagnostic-conflict result is supplied. |

### Attack success, advice audit, and dosage release

| ID / source | Claim, denominator, and actual endpoint | Status and required scope/action |

|---|---|---|

| E21 — §5.3 L239; ledger L525; abstract/headline | Local ASR 52.5%→10.71%, 280 calls **per arm**. Rates imply 147→30 successful attacks out of 280. | M. Useful full-pipeline comparison under the reported attack set/judge. State prompt pairing, model/release, judge rubric, and which controls differ. It does not isolate T4 or prove overall safety. Total model calls are 560 if one call per prompt per arm. |

| E22 — same sources | Local Bengali-native ASR 77%→19% on 100 attacks. | M. Plausible subset of E21, but identify suite membership. Keep visible as an important residual. It does not prove Bengali is intrinsically harder without matched-language analysis. |

| E23 — §5.3 L239; ledger L524; headline | Cloud ASR 36.19%→.95%, 420 calls **total**, 210 per arm; implied counts 76→2. Bengali-native 83%→10%, n=100. | M, internally inconsistent if the latter is a subset of the former. Resolve suite IDs, arms, denominator, and relationship before quoting combined results. Do not silently “correct” either rate. |

| E24 — §5.3 L239 versus ledger L524–525 | Residual embedded attacks 4/10 and roleplay 2/10; same-design/prompts/judge comparison across local and cloud. | M but attribution unclear. Main text associates failure variants with local results; ledger associates them with cloud. Identify model, arm, and suite. Unequal 280/210 per-arm samples do not establish identical prompt coverage. Remove the causal attribution to 4-bit quantization unless independently tested. |

| E25 — §3.3 L141; introduction/conclusion | Independent checking across local and cloud generators. | A architectural property, illustrated using two models. It is defensible to say the same checker runs after both. It does not establish generator-invariant error rates, universal compatibility, or equal safety. |

| E26 — §5.3 L241; ledger L527 | Three blinded evaluators rate 47 guarded outputs: 46 safe/actionable, one vague/harmless, zero dangerous; three unguarded controls all dangerous; Fleiss κ=.8217. | M, small output audit. Identify the two students and extension officer by role, selection/blinding/rating process, and output sampling. Not 47 experts, not a farmer trial, and not a balanced paired causal comparison with the three controls. “Expert audit” should not hide the evaluator composition. |

| E27 — §5.3 L241; ledger L529; abstract | 114/118 inserted errors detected in 38 live-source answers, 96.61%; 0/38 unmodified answers rejected. | M, constructed mutations of live answers. Unit is injected error, clustered within 38 answers—not 118 naturally occurring independent failures. Keep clean-answer specificity separate. This tests the defined checker, not general factuality. |

| E28 — same sources | Scaled benchmark: 528 cases from 88 passages; 350 inserted errors, 296 caught, 84.57%, 54 missed. | M on constructed cases. Describe the remaining 178 cases and their results; arithmetic alone does not establish they are all clean controls. Do not extend the 0/38 live rejection result to the whole scaled benchmark. Row-wide n=528 should not conceal the separate live set. |

| E29 — §5.3 L241; ledger L529 | Overdose 76/76 and underdose 67/67 detected; chemical substitutions 85%, unit substitutions 73%, invented PHI 65%. | M. Publish counts for the last three types and whether categories overlap. These residuals delimit what “dosage verification” means. No claim that all chemical identities, units, or safe-use relations are checked successfully. |

| E30 — §3.3 L143; ethics L282 | Unsupported/out-of-range dosage claims are dropped; chemical pathway “fails closed.” | A plus E27–29. State matched chemical/formulation/crop/unit relations, failure handling, and deletion granularity. Recognized conditions can fail closed while unrecognized unsafe content still passes. Avoid a blanket fail-closed guarantee given measured misses. Verify that surviving prose remains interpretable after deletion. |

| E31 — ledger L528 | 10/10 injections blocked; 0/30 off-topic inputs refused by T0, 25/30 by an LLM classifier; five weather queries deliberately allowed. | M on two sets. The row’s n=30 omits the 10-injection set. Separate safety refusal from relevance routing and explain intended labels. Document where this additional LLM branch occurs and whether it can authorize a request. |

### SMS, offline operation, footprint, latency, and cost

| ID / source | Claim, denominator, and actual endpoint | Status and required scope/action |

|---|---|---|

| E32 — §5.3 L243; Appendix B L343; ledger L533 | 299/300 offline-ready and 100/100 live-ready messages satisfy ≤160 characters; 399/400 overall. | M, string-length conformance. Define “ready,” output script, encoding, and actual SMS segment count. Not evidence of network delivery, receipt, or semantic safety. |

| E33 — Appendix B L343; ledger L533 | Referral purity 8/8. | P/M small check. Define purity: correct destination, no chemical content, no extraneous text, or another criterion. Eight examples cannot establish all referral behavior. |

| E34 — same sources | Naive truncation keeps dose patterns in 12/92; compressor preserves 65/66 live gold dosage claims, 98.5%. | M, different denominators. State inclusion/exclusion and overlap; not a paired 92-versus-66 treatment effect. Pattern retention is narrower than correct complete instructions. |

| E35 — same sources | Dose, application interval, and PHI survive in 1,000/1,000 certified tuples, 102–115 GSM characters, no >160 violations. | M, constructed input-constrained conformance. Replace general “guarantees” with this supported domain unless a formal invariant is specified and proved. Explain what certified means and the literal encoding. An implementation that copies fields can still omit or misbind their meaning. |

| E36 — Appendix B L343–359; ledger L534; §5.3 L243 | On 100 paired long advisories: dose survives 23/100 naive, 89/100 LLM, 92/100 compressor; chemical names 20/100, 56/100, 34/100. | M, constructed/selected paired set using frozen detectors. Dose retention is not complete advice retention. The compressor loses the chemical name in 66/100 outputs by this metric; require dose–chemical–unit association before calling the output actionable. Report manual or tuple-level checks if available. |

| E37 — same sources | Length conformance 100/100, 98/100, 100/100; invented dosage 0, 1 plus one borderline, 0; seed 42. | M. Define borderline and detector/manual adjudication. Zero observed invention is useful but does not prove absence of all incorrect output. “Copies verified slots” is an architectural assertion, not evidence that extraction and association cannot fail. |

| E38 — ledger L533 | SMS aggregate n=1,416. | Unreconciled aggregation. The stated 400 length checks, 1,000 tuples, and eight purity checks alone total 1,408; other sets overlap or measure different units. Do not derive a combined success rate. Replace the single n with separate experiment IDs/counts and a membership map. |

| E39 — Appendix B L364; ledger L535 | BM25 hit rate .94 and 0/400 service-worker cache misses. | M. Define hit@k, relevance gold, query set and warm/cold cache conditions. The ledger associates n=400, but explicitly assign it to each metric. Retrieval availability is not complete offline language-model operation. |

| E40 — same sources | Under 15% and 30% simulated packet loss, local hit rate stays .94; remote loses 13.25 and 30 percentage points. | M/S. Specify loss injection/retries/timeouts and baseline. “Rural edge”/“severe 2G” are scenario labels, not measured representative rural networks. No field connectivity claim. |

| E41 — Appendix B L367–381; ledger L537 | 95.64 MB ONNX assets, 284 MB minimal install, 339.6 MB full install. | M, artifact sizing; inventory/version/unit missing. Exclude or include model weights and dependencies explicitly. Current “full” label is misleading for a 4B 4-bit local generator. Disk footprint also is not peak RAM. |

| E42 — §3.3 L139; limitations L259; ledger L536 | Approximately 24 seconds/local CPU generation call; 1.8 seconds/cloud answer. | Timing claims with unspecified samples/conditions. Name CPU/RAM/runtime/model/quantization, token lengths and statistic; give cloud timing definition. Do not claim interactive end-to-end latency from either alone. |

| E43 — Appendix B L386–402; ledger L536 | n=400 with stub LLM: total median 33.565 ms, p95 67.833; safety .321/.705, retrieval 26.831/61.248, verifier 4.815/11.220 ms median/p95. | M, non-generation overhead. Existing caption is appropriately explicit. Keep “non-LLM” in every reuse. Component medians need not sum to the total median; that is not an error. The ledger’s 4.2-second “live latency” belongs to a gate decision, not this whole pipeline. |

| E44 — ledger L526; Appendix D L478 | Regex matching median .016 ms; full T0 .321 ms; delayed-attack precheck .20 ms. | M, different code paths/test sets. Identify timing boundaries, hardware, and sample count for each. These values are not necessarily inconsistent and are not whole-answer response times. |

| E45 — Appendix B L407; ledger L538 | n=1,000 termination mixture: 5.7% T0, 0% T1 guidance, 2.2% T2 lookup, 92.1% generation; 7.9% zero-LLM turns. | Mixture provenance unclear; ledger labels row D. Say whether observed, sampled, or assumed, and define “turn.” Do not generalize to farmer traffic. Explain the lookup branch and whether ASK counts; a 15% halt prevalence in another cohort is not automatically contradictory. |

| E46 — same sources | $0.1682/1,000 modelled versus $0.1950 baseline, 13.7% saving; metered-token calculation $0.1720. | D, even when token counts were measured. Arithmetic is consistent: the second estimate implies about 11.8% saving against the same baseline. State price date, input/output rates, tokens, mode, and exclusions. Not actual bills or whole local-deployment operating cost. |

| E47 — Appendix B L410 | 100/100 traces preserve event ordering, median nine events. | M, sampled trace conformance; missing from “every result” ledger. Define event ordering and sampled paths. Good inspectability evidence, not proof every citation caused the draft or every execution is correct. |

### Multi-turn behavior and remaining deployment assertions

| ID / source | Claim, denominator, and actual endpoint | Status and required scope/action |

|---|---|---|

| E48 — Appendix D L455–478; ledger L530 | Stated 200 dialogues/425 turns across five regimes; row sums 275/575 if disjoint; ledger says four regimes. | M on constructed suite, membership unresolved. Mark shared cohorts explicitly. Do not retain an undefined “100% robustness” total. |

| E49 — same sources | Anaphora: 75 dialogues, 175 turns, 100/100 follow-up slot retention; ledger says 75/75. | M. Both could be true with dialogue-level versus turn-level success. Report both units explicitly; no inference to unrestricted farmer conversations. |

| E50 — same sources | Crop-topic shift: 75/75 shifts detected and old disease slots flushed; cross-crop chemical leakage 0%. | M, endpoint uncertain. Slot flushing does not itself measure toxic advice. Define checked generated outputs or narrow to state isolation. Show whether the “hazard” row is a second measure on the same 75 dialogues. |

| E51 — same sources | Delayed attacks: 30 dialogues/60 turns, 30/30 second-turn interceptions and referral. | M on specified two-turn patterns. Not extended-dialogue jailbreak resistance or successful human intervention. Distinguish agronomic and emergency referral rules. |

| E52 — same sources | Clarification: 20 dialogues/40 turns, 20/20 ASK then crop-binding resolutions. | M on constructed interactions, not a user study. Add to ledger; retain as direct state-transition evidence. |

| E53 — §3.3 L145; Appendix A L316 | Exactly one visible provenance badge per response; sources and Why-panel traces; web, SMS, offline card, read-aloud. | A, partially illustrated. List badge meanings and channel availability; distinguish implemented/tested features from paths merely described. Appendix C does not establish every promised alternative channel. Preserve the caveat that a badge is not causal citation faithfulness. |

| E54 — design L114–116; ledger L528, L538 | Only T3 uses the generating model; authorization independent of it; deterministic stages. | A. Distinguish “does not invoke the answer generator,” “invokes no LLM,” and “deterministic.” Learned vision and the reported LLM classification branch require an exact boundary description. Explicitly state whether probabilistic classification can influence admission. |

| E55 — limitations L259; conclusion L267 | Evidence can be updated independently of generator training; coverage expansion primarily knowledge maintenance. | A, plausible for index updates. Updating a passage differs from adding a crop that needs a router, classifier, aliases, policy, and evaluation. Do not imply new-crop readiness is guaranteed by adding documents. |

| E56 — availability L263 | Six-crop deployed system, 4B local generator, 2,135 released nodes, licenses and access. | A/public metadata mismatch. Provide versions and exact resource links; distinguish the hosted full system from the restricted/reproducible package. The withheld T0 dictionary should be an explicit reproducibility limit. |

| E57 — ethics L278–280, L286 | Approved/consented de-identified query data; public-image licenses; photos never uploaded/stored remotely; local deployment makes no external calls; enterprise zero retention. | A, not validated by performance tables. Provide collection/approval and dataset manifests; resolve live cloud use; scope privacy guarantees to tested modes. A model label or open download alone does not establish redistribution rights. |

| E58 — ethics L284, L288 | Referral ensures emergencies are never delayed; all unresolved/unsafe cases end in human referral. | A overstated outcome. The system can display a destination immediately; it cannot establish connection time or access to care from the reported tests. ASK and CONFIRM can end a turn without referral. State the actual branch behavior and cite current service details. |

### Evidence-status and uncertainty cleanup

The reported Wilson intervals for the clearly identified binomial counts and the two stated exact McNemar tests are broadly consistent with the given counts. This does not resolve sample selection, shared-source clustering, evaluator judgment, or suite membership. For example, 118 mutations from 38 answers are not automatically 118 independent natural errors. The first repair is a manifest of experiment ID, source cohort, generated artifact, model/configuration, unit, positive/negative counts, and overlap—not additional confidence intervals on ambiguous denominators.

There are also several methods and outcomes mentioned only in the appendix ledger. A ledger is valuable, but it cannot replace a short reproducible explanation of how labels, errors, and successes were determined.

## 6. Natural writing: targeted changes, not a stylistic overhaul

The manuscript already contains concrete, technically competent prose. Its main language problems are repeated framing and occasionally stronger outcome nouns than the measurements justify. No detector-oriented rewriting is warranted.

| Passage / location | Diagnosis | Recommended editorial action |

|---|---|---|

| Abstract’s subsystem and metric inventory | Too many mechanisms and denominators compete with the main point. | Keep the control principle, visible interaction, and a small set of corrected representative results. |

| Repeated generation/authority contrast, introduction, L116, L267 | Useful once; repeated formulations spend space without advancing the explanation. | Define the principle early, then use concrete stage actions. |

| Introduction’s three contributions versus C1–C3 | Two taxonomies create conceptual work for the reader. | Align the list and let deployment/normalization support those controls. |

| “Those permissions belong to deterministic stages,” L116 | Abstract actor and potentially inaccurate scope. | Name the check and decision; distinguish learned signals from enforcement rules. |

| “This prevents evidence for an unrelated crop from reaching generation,” L134 | Absolute claim conflicts with the reported oracle result. | State the verified exclusion rule and separately report residual contamination. |

| “wrong-crop advice,” L232 and ledger | Changes a retrieval observation into a generated-output claim. | Use the actual retrieval endpoint consistently. |

| “all explicit contradictions” with an “implicit” miss, L234 | Eligibility and failure description conflict. | Define the full conflict suite, then distinguish explicit from implicit cases. |

| “reflecting the operational bounds of a 4-bit local model,” L239 | Unmeasured causal explanation. | Describe observed failure categories; omit quantization attribution. |

| “Constrained delivery preserves the dose,” L243 | Broad, binary conclusion from 92/100 long advisories. | State the bounded retention result and lossy behavior. |

| “guarantees 100.0% critical slot survival,” L343 | General guarantee derived from certified test inputs. | Identify the certified input domain and observed count. |

| “cannot invent values,” L343 | Copying may prevent novel strings but does not prove correct binding or extraction. | Describe copying behavior and observed invention metric without implying semantic infallibility. |

| “Real-world deployment requires maintaining agronomic coherence across extended farmer dialogues without hallucinatory context drift or safety degradation,” L455 | Generic, abstract introduction to short constructed tests. | Open with the concrete state transitions being tested. |

| “completely eliminating cross-crop pesticide leakage,” L478 | Absolute and possibly substitutes memory state for generated advice. | Name the actual checked state/output and bounded denominator. |

| “ensuring life-safety emergencies are never delayed,” L284 | Claims an external service outcome from a UI action. | Describe immediate display/routing without claiming assistance timing. |

| “Unresolved or unsafe cases end in a referral,” L288 | Hides the ASK/CONFIRM paths. | State the actual termination and continuation rules. |

| Long ASR paragraph, L239 | Mixes models, suites, scripts, residuals, and causal interpretation. | Split by experiment once the suite identities are repaired. |

Semicolons and technical nouns are not inherently unnatural. The material problem is packing multiple experiments or qualifications into one sentence. Prefer one actor, action, and supported outcome per sentence where this improves interpretation. Retain necessary terms such as “crop fence” after defining them; do not replace precision with conversational vagueness.

## 7. Claims that deserve stronger emphasis

These are already present and can be emphasized without inventing a new contribution. All numerical results remain subject to the manuscript’s reported experimental provenance.

1. **Admission before retrieval:** the gate stops all 30 crop-less treatment requests and passes the 170 crop-specified requests in the authentic 200-query set. The meaningful behavior is that an unresolved crop prevents retrieval, not merely that the system asks a question.
2. **Human confirmation is part of evidence binding:** the UI exposes an explicit text/image crop conflict and withholds chemical advice pending resolution. Pair this with the separate 53/54 farmer and 400/400 synthetic results rather than only the pooled near-perfect number.
3. **Language variation affects control behavior:** on the defined constructed set, normalization changes interception from 1/85 to 85/85, with 0/15 benign false alarms. That is a concrete Bengali/Banglish system result, provided the scope remains visible.
4. **Generated text is checked after drafting:** 114/118 injected errors are caught while all 38 original answers pass. This is a useful sensitivity/specificity pairing for a bounded verifier, not a general truthfulness claim.
5. **The larger verifier test exposes the boundary honestly:** 296/350 caught, with complete detection of the tested over/underdoses and weaker chemical/unit/PHI handling. Reporting the 54 misses gives the narrow release mechanism credibility.
6. **Local guarding reduces observed ASR while leaving substantial residual risk:** the reported 52.5%→10.71% result is meaningful. Keep the 19% Bengali-native residual nearby; do not use the unresolved cloud comparison to imply near-total protection.
7. **The interface explains why a turn stopped or a claim disappeared:** the visible state, retrieved source, and Why-panel are stronger demonstration assets than another broad safety slogan. The 100/100 trace-order checks support sampled execution ordering.
8. **The generator is replaceable within an explicitly defined interface:** show that the same post-check runs for local and cloud drafts. Claim architectural separation, not equal performance or universality.
9. **The paper already discloses useful deployment trade-offs:** quantization can reduce storage while slowing execution on the tested CPU, local generation takes about 24 seconds, SMS compression loses information, and offline network tests are simulated. Preserve these candid distinctions.
10. **The small blinded audit supports a limited usefulness claim:** 46 of 47 guarded outputs were judged safe and actionable by the specified three raters. Use that result with its sampling and rater limitations; do not upgrade it to farmer validation.

The retrieval improvement should become a headline again only after its endpoint and oracle-fence inconsistency are resolved. Independently updateable knowledge is worth a concise architectural statement, but not a separate claim of new retrieval science.

## 8. Bibliography corrections verified against primary records

| BibTeX entry | Finding and action |

|---|---|

| `our_agricultural_safety` | The current arXiv title is **KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory**, not the title in the supplied entry. Cite the actual version used and its correct title. [Primary record]([https://arxiv.org/abs/2606.29243](https://arxiv.org/abs/2606.29243)). |

| `farmerchat2024` | The supplied author list is substantially incorrect after the first two names. Replace it from the primary record rather than patching isolated initials. [Farmer.Chat record]([https://arxiv.org/abs/2409.08916](https://arxiv.org/abs/2409.08916)). |

| `hossain2026` | The title should be **Cost-Efficient Cross-Lingual Retrieval-Augmented Generation for Low-Resource Languages: A Case Study in Bengali Agricultural Advisory**. [Primary record]([https://arxiv.org/abs/2601.02065](https://arxiv.org/abs/2601.02065)). |

| `vijayvargia2025` | The first author is **Abhay Vijayvargia**, not Rohit Vijayvargia. Verify the whole imported record. [Primary record]([https://arxiv.org/abs/2508.03719](https://arxiv.org/abs/2508.03719)). |

| `bangla_low_resource` | The cited Kakwani et al. paper is **IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages**, pages **4948–4961**. The supplied title, some author details, and ending page differ. Import the ACL record. [Primary record]([https://aclanthology.org/2020.findings-emnlp.445/](https://aclanthology.org/2020.findings-emnlp.445/)). |

Also check the role each citation plays. General multilingual-resource work does not directly establish the effectiveness of this system’s Banglish safety matching; its own bounded test does. Bibliography comments claiming verification are not substitutes for primary-record checks.

## 9. Experiments that should NOT be added for this submission

- A season-long yield, income, or randomized farmer-impact trial. The paper explicitly does not claim field effectiveness; these are future research, not a prerequisite for this prototype demonstration.
- A large user study merely to imitate another accepted demo’s sample size.
- A leaderboard across many new language models. Two implemented execution modes can illustrate the interface; repair the existing comparisons first.
- Another broad sparse-versus-dense or multilingual retrieval benchmark duplicating the prior retrieval paper. The present question is evidence authorization and contamination under the demonstrated controls.
- Retraining every vision model, adding many crops, or evaluating every Bengali dialect. These expand scope rather than resolve the current claims.
- Generic BLEU/ROUGE scores or another large LLM-judge quality score disconnected from the gate, crop, and dose decisions.
- A full-precision versus quantized-model ablation solely to rescue the sentence attributing residual attacks to 4-bit quantization. Removing that unsupported explanation is the proportionate action.
- Exhaustive adversarial testing intended to justify an absolute safety guarantee. Keep the actual bounded guarantee, residuals, and referral limitations explicit.
- New experiments for arithmetic, version, license, or cohort contradictions. These need record reconciliation and accurate writing, not more data.

## 10. Small supporting checks that address real gaps

**Start with existing records.** Reconcile attack-suite IDs, multi-turn membership, verifier error categories, and SMS counts; supply the missing thresholds; freeze artifact versions. These corrections are more urgent than collecting new measurements.

| Priority | Small check | Minimum useful design and endpoint | Claim it could support |

|---|---|---|---|

| High | Integrated demonstration replay | Run the five scenarios on one identified build. Log crop state, attached image, explicit user confirmation/reset, retrieval count, generator invocation, referral, and verifier output. Cover resumption after ASK/CONFIRM/REFER and label any injected draft. | The actual visible workflow and stage ordering. |

| High | Crop-fence residual audit | Inspect the existing oracle-contaminated cases first. Compare bound crop, gold crop, passage tags/content, candidate set, and final top five; report halted versus answered cases. | What the fence actually enforces, and why contamination remains. Usually analysis of existing logs, not a new benchmark. |

| High if retaining zero-false-halt wording | Benign conflict controls | A modest, explicit set of matched text/image pairs, different symptoms within the same crop, absent photos, and ambiguous photos. Report CONFIRM/ASK/pass by intended behavior and denominator. | False-positive behavior of the mismatch mechanism. |

| High if advertising safe SMS advice | Complete instruction and encoding check | Review a small set of long chemical advisories after verification and compression. Check chemical/formulation, dose, unit, crop, interval/PHI as linked fields, plus encoded segment count. Include known name-loss examples from the existing 100-case set. | Whether retained numbers still express usable instructions and fit the promised delivery channel. |

| Medium | Verifier boundary cases | Extend existing controlled mutations only where unclear: same number/wrong unit, wrong chemical with plausible dose, missing formulation, and deletion leaving ambiguous instructions. Include untouched counterparts. | Precise behavior of T4 and its failure handling—not general agronomic factuality. |

| Medium if emphasizing offline deployment | Local execution and mode check | One identified local build: disable network access, execute representative admission/retrieval/generation/verification paths, record required assets and timed stages. Observe image/text network requests in connected mode separately. | That the packaged mode runs locally and its stated data flow matches implementation. |

| Optional | Frozen-generator knowledge update | Change one versioned source passage, rebuild the relevant index, and replay a query with unchanged weights. Record source version and retrieved evidence. | A concrete illustration of independent knowledge maintenance, without pretending it proves all update quality. |

| Optional | Small observed usability session | A few intended users or extension officers attempt missing-crop clarification, conflict confirmation, and source inspection. Report task completion and specific misunderstandings. Follow the applicable research approval process. | Understandability of the visible controls; not field effectiveness. |

| Conditional only | Matched two-model subset | If retaining a quantitative model-comparison claim, evaluate both on the same existing prompt subset with identical guard configuration and scoring. | A controlled two-model comparison. Unnecessary for the narrower architectural statement. |

Do not run all of these automatically. After record reconciliation, prioritize the integrated demo, the unexplained fence residuals, and SMS semantics if those claims remain prominent. The other checks are conditional on the claims the authors choose to retain.

## Submission-focused decision

Preserve the current problem, system, and C1–C3 story. Correct the evidence semantics and contradictions, expose the missing decision rules, make the demonstrated state transitions readable and reproducible, and align the public artifacts with the availability/privacy statements. The paper already has sufficient breadth of prototype evidence; the immediate need is trustworthy interpretation and a convincing demonstration, not a new research program.