**Prioritize checks that clarify the existing authorization boundary. No proposed experiment should delay submission.** If a check is unfinished, retain the narrower claim supported by existing evidence. If it reveals a contradiction, correct the claim or describe the limitation; a successful rerun is not a prerequisite for submitting an accurate paper.

This is a proposed triage plan. **No new experiments have been run.** “Current evidence” refers to the manuscript and Prompt 1 audit.

## 1. Major claims mapped to current evidence


| Major claim                                                 | Current evidence                                                                                                                            | Remaining gap                                                                                                                                           |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Crop-less treatment requests halt before retrieval          | 30/30 halted; 170/170 crop-specified requests passed in the 200-query set. Constructed pilot adds 100 ambiguous and 140 specified requests. | Broader transition coverage; independently observed retrieval/model-call behavior; unnecessary clarification.                                           |
| Policy-covered high-risk requests trigger referral          | Local guarded ASR improves from 52.5% to 10.71%; Banglish precheck intercepts 85/85 constructed attacks with 0/15 benign false alarms.      | Full-pipeline ASR does not isolate referral enforcement; benign controls are small; cloud counts need reconciliation.                                   |
| T0–T4 enforce ordered authorization                         | Architecture description and 100/100 trace-order checks.                                                                                    | Logs alone may miss bypasses, early streaming, stale state, exceptions, or retry paths.                                                                 |
| Authorization survives multiple turns                       | Reported carryover, crop-shift, delayed-attack, and clarification tests.                                                                    | Cohort totals overlap or conflict; state isolation is not necessarily a measurement of generated chemical safety.                                       |
| Bengali/Banglish normalization preserves relevant decisions | 85 adversarial variants versus a formal-only baseline; six normalization presets.                                                           | No matched semantic families establishing which decisions survive particular variations.                                                                |
| Vision provides usable crop-routing input                   | Disease-classifier accuracy .9413–.9907 over 4,294 images; family assignment 433/437.                                                       | Disease accuracy and family accuracy are distinct from deployed crop-routing accuracy; exclusions and thresholds need clarification.                    |
| Crop fencing restricts evidence                             | Reported contamination falls from 36.25% to 28.75% on 400 queries.                                                                          | Oracle routing still shows 30% contamination; crop-tag, content, routing, and abstention effects are unresolved.                                        |
| Text/image conflicts require confirmation                   | 53/54 farmer conflicts and 400/400 synthetic conflicts detected.                                                                            | Non-conflicting controls are missing for the “zero false halts” claim.                                                                                  |
| Authorization is separated from the answer generator        | Local and cloud configurations are described; T4 purportedly runs after both.                                                               | Existing attack results are not a controlled test of architectural separation.                                                                          |
| T4 removes unsupported dosage claims                        | 114/118 inserted errors detected across 38 answers; 0/38 originals rejected. Scaled test: 296/350 errors detected.                          | Claim-level delivery enforcement, semantic associations, and error handling require clarification. These results do not establish general factuality.   |
| Provenance makes answers inspectable                        | Badges, Why panel, screenshots, trace-order checks.                                                                                         | Citation support and user understanding have not been directly measured.                                                                                |
| The demonstration is useful and understandable              | Three raters assessed 47 guarded outputs; 46 judged safe/actionable.                                                                        | Output assessment does not test interactive state comprehension or successful use without reading the paper.                                            |
| SMS preserves useful instructions                           | 399/400 messages meet the character limit; dose retained in 92/100 long advisories, chemical name in 34/100.                                | Complete instruction integrity and encoded message segments, rather than isolated numeric retention.                                                    |
| Local/offline deployment is practical                       | Local retrieval/cache tests, simulated packet loss, installation sizes, stub overhead, approximate generation times.                        | Complete installation accounting, actual end-to-end timing, and offline execution of the entire declared path.                                          |
| Evidence can change without retraining the generator        | External-index architecture.                                                                                                                | No demonstrated update-and-replay example; adding a new crop requires more than updating a passage.                                                     |
| Routing reduces resource use                                | Reported termination mixture, token measurements, and modeled costs.                                                                        | Mixture provenance and accounting need clarification. New traffic experiments are unnecessary for retaining a bounded modeled estimate.                 |
| Released artifacts match the paper                          | Public links and release descriptions.                                                                                                      | Prompt 1 identified license, resource, mode, and recording inconsistencies.                                                                             |
| Privacy, governance, and novelty claims are accurate        | Ethics statements and cited prior papers.                                                                                                   | These require configuration/documentation checks and clear attribution. Performance experiments cannot establish consent, licensing rights, or novelty. |


**Existing-record cleanup comes first:** reconcile cloud counts, multi-turn membership, SMS denominators, and experiment versions. This is evidence bookkeeping, not a new experimental requirement. If a number cannot be reconstructed, remove or qualify it.

## 2. Experiment triage table

Suggested sample sizes below are practical planning budgets, not power calculations. Freeze the selected budget and sampling rules before examining outcomes.


| Experiment                                            | Claim supported                                                                               | Current evidence                                                                  | What new evidence adds                                                                                       | Dataset/source                                                                                                           | Metric                                                                                                                              | Main or appendix                                                           | Submission dependency?                                                           | Risk of misleading interpretation                                                                            |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **A. Authorization property-conformance test**        | Implemented transitions enforce admission, confirmation, referral, and claim release.         | Gate results; 100 trace checks; constructed multi-turn tests.                     | Direct observation of calls and delivered content across normal, error, retry, and stale-state paths.        | Approximately 2,000 fixed constructed state cases; small replay through the actual deployed application.                 | Violations/eligible checks for each property; transition coverage; rejected claims delivered; forbidden calls; ordering errors.     | One main-text result if useful; full matrix in appendix.                   | **No.** Retain tested-path wording if unfinished.                                | Zero violations in a constructed suite is not proof of safety or complete input coverage.                    |
| **B. Two-generator boundary test**                    | The same authorization rules constrain different answer generators.                           | Two deployment modes; unmatched attack comparisons.                               | Controlled generator substitution with upstream state and downstream checker fixed.                          | About 100 fixed requests covering blocked and permitted paths; the two already supported generators.                     | Pre-generation decision agreement; forbidden-call count; verification invocation; rejected-claim leakage, separately by generator.  | Appendix; brief main-text reference if informative.                        | **No.** Retain architectural description only.                                   | Different DROP rates can be legitimate because drafts differ; identical answers are not required.            |
| **C. Citation-support and dosage audit**              | Displayed sources support the claims attributed to them.                                      | Provenance UI and separate verifier tests.                                        | Direct assessment of claim–passage support, including missing and misleading citations.                      | Stratified sample of about 40 delivered answers; every factual claim and displayed citation in those answers.            | Supported/partial/unsupported/unassessable pairs; citation completeness; fully supported answers; separate dosage-error detection.  | Appendix; one main result only if central.                                 | **No.** Keep provenance as an inspection feature.                                | Citation support is not causal faithfulness, source currency, or overall agronomic correctness.              |
| **D. Benign-control expansion**                       | Controls do not unnecessarily obstruct legitimate requests.                                   | 170 gate negatives; 15 Banglish benign controls; 38 clean verifier answers.       | Direct estimates for unnecessary REFER, ASK, CONFIRM, and DROP.                                              | About 200 held-out benign requests plus independently supported dosage fixtures; matched text/image controls.            | State-specific false-positive counts/eligible cases; unnecessary interventions per request; task completion.                        | Compact main table plus appendix breakdown.                                | **No.** Keep existing denominator-specific claims.                               | A benign question can generate an unsafe draft; blocking that draft is not a false positive.                 |
| **E. Paired Bengali/Banglish/dialect variants**       | Selected language variations preserve safety-relevant interpretation.                         | Unpaired constructed Banglish attacks and presets.                                | Within-intent comparison across scripts and variations.                                                      | About 100 semantic families × five variants, validated by Bengali-speaking annotators.                                   | Crop/intent/policy-decision accuracy; within-family consistency; harmful flips; unnecessary interventions.                          | Appendix unless language robustness becomes a central result.              | **No.** Retain the existing 85-case claim.                                       | Consistently wrong decisions are still consistent; 500 variants are not 500 independent intents.             |
| **F. Interactive demo utility audit**                 | Users can understand the visible states and inspect evidence.                                 | Output ratings and screenshots.                                                   | Observation of actual interaction without prior paper reading.                                               | Six to eight domain-aware Bengali-speaking participants; fixed tasks covering the four states and source inspection.     | Unassisted completion; correct state interpretation; assistance required; recurring misunderstandings; participant-level summaries. | Short main-text paragraph; protocol/results in appendix.                   | **No.** Describe the interface without claiming demonstrated usability.          | A small convenience sample does not establish farmer adoption, field effectiveness, or population usability. |
| **G. Predetermined qualitative gallery**              | Examples make the controls and residual failures understandable.                              | Existing screenshots and recorded failures.                                       | A readable explanation connecting input, decision, evidence, and outcome.                                    | Six cases selected by a declared rule from frozen audit results.                                                         | No aggregate performance score; documented selection and verified case behavior.                                                    | Main figure if it replaces the unreadable montage; otherwise appendix.     | **No.** Existing figures can be retained or simplified.                          | A curated gallery is not representative prevalence evidence.                                                 |
| **H. Complete deployment measurement**                | A specified deployment runs within stated resource and connectivity constraints.              | Partial sizes, stub latency, approximate model timing, cache/network simulations. | Whole-system storage/RAM/timing and actual offline behavior.                                                 | Frozen local and connected builds; e.g. 50 warm requests and 10 cold starts per measured mode.                           | Full asset size; peak RAM/VRAM; complete-response latency; failures/timeouts; cold-start times; network requests; cache behavior.   | Appendix; only essential latency/requirements in main text.                | **No.** Remove “full installation” or end-to-end claims if unverified.           | Cached retrieval is not offline generation; warm performance is not cold-start performance.                  |
| **I. Artifact and deployment correspondence check**   | Readers can access the system actually described.                                             | Links work; Prompt 1 found discrepancies.                                         | A versioned correspondence record covering code, models, evidence, UI, and instructions.                     | Exact repository commits, model revisions/hashes, license files, clean installation, live demo, screenshots, screencast. | Resolved/missing/mismatched items; installation outcome; verified scenario coverage.                                                | Availability statement and appendix manifest.                              | **No new-run dependency.** State only confirmed availability.                    | Repository accessibility does not establish completeness, licensing rights, or matching deployment.          |
| **J. Crop-fence residual audit and paired replay**    | The fence enforces a defined crop constraint and reduces the measured contamination endpoint. | Existing 400-query comparison; unexplained oracle residual.                       | Separation of enforcement violations, incorrect crop binding, source-label problems, and abstention effects. | Existing 400 cases with frozen crop/source annotations and index version.                                                | Tag-based fence violations; content contamination; gold-crop contamination; halted fraction; contamination among retrieved cases.   | Main text should use the corrected result; diagnostic details in appendix. | **No.** Narrow the fence claim and withhold unexplained comparative conclusions. | Counting halted queries as clean can make contamination improve simply by answering less.                    |
| **K. SMS instruction-integrity audit**                | Compressed messages preserve usable verified instructions.                                    | 92/100 dose retention but 34/100 chemical-name retention.                         | Checks that retained values still belong to the right chemical, unit, crop, and instruction.                 | Existing 100 paired long advisories, plus actual encoded outputs.                                                        | Complete required-field retention; correct field association; ambiguity; unsupported additions; segment count.                      | Appendix; main-text limitation if losses are material.                     | **No.** Keep SMS claims limited to measured retention.                           | Surviving dose tokens do not establish safe or actionable instructions.                                      |
| **L. Frozen-generator evidence update demonstration** | Evidence can be updated without changing generator weights.                                   | External-index design.                                                            | A concrete update, retrieval, and provenance example.                                                        | A few preselected, validated document updates in an isolated index copy; unchanged model and fixed queries.              | Weight hash unchanged; correct new source version retrieved/displayed; stale-source persistence.                                    | Appendix-only.                                                             | **No.** Retain the architectural statement.                                      | A few successful updates do not establish arbitrary update reliability or new-crop readiness.                |


## 3. Priority and interpretation rules

### RUN FIRST

These are the first choices **if optional experimental work is undertaken**, not a mandatory bundle.

**I — Artifact correspondence**

This is likely the quickest way to eliminate confusion affecting the whole paper.

- **Add the result when:** each claimed artifact can be identified, its version and license stated, and tested instructions reproduce the declared configuration. Publish a manifest rather than a “reproducibility score.”
- **Do not strengthen availability claims when:** weights, evidence, restricted controls, or installation steps remain unavailable or differ from the hosted system. Report that distinction. Do not call a partial package the complete demonstrated system.

**A — Authorization conformance**

Define the properties precisely before constructing the suite:

- No **answer-generation call** before its authorization state.
- No crop-dependent treatment retrieval until crop requirements are satisfied.
- No **rejected dosage claim** reaches a delivery channel.
- A recognized policy trigger follows its declared referral path.
- A recognized text/image crop conflict enters confirmation before affected chemical advice.
- Traces and observed calls follow the specified order.
- A changed crop or image invalidates any authorization that depended on the previous state.

Instrument all model calls by purpose—vision, classification, generation. An upstream LLM classification call must be reported, not silently excluded to obtain a zero-call result.

For DROP, allow a sanitized response or referral where the design permits it. “No delivery after any failed claim” would test a different system from the manuscript’s claim-removal design.

Include exceptions, timeouts, retries, streaming before verification, and stale multi-turn state. Observe actual retrieval/model/delivery interfaces; do not rely solely on self-reported trace events.

- **Add stronger conformance wording when:** there are zero observed violations for each explicitly enumerated property, with meaningful path coverage and a deployed replay supporting the harness results.
- **Do not strengthen it when:** a forbidden call, rejected-claim leak, or stale authorization occurs. Report the violation and affected path. Stub-only success supports orchestration under fixtures, not full deployed behavior.
- **Never conclude:** “proved safe,” “cannot fail,” or “covers all high-risk language.”

**J — Crop-fence audit**

Inspect existing oracle-contaminated cases before generating another benchmark. Separate:

1. Whether a returned passage violates the bound crop’s metadata constraint.
2. Whether passage content concerns another crop despite its tag.
3. Whether the bound crop differs from the query’s gold crop.
4. Whether the system avoided retrieval by halting.
  - **Add a stronger fence result when:** the invariant is precisely defined, measured consistently, and the paired comparison reports both contamination and coverage.
  - **Do not strengthen it when:** the apparent gain comes mainly from additional halts, or oracle contamination remains unexplained. A correctly enforced metadata filter can still retrieve semantically unsuitable passages; describe those separately.
  - Preserve the original benchmark. If annotations or indexing are corrected, version the correction and report what changed.

**D — Benign controls**

Assign expected or acceptable outcomes before execution. A benign request may legitimately need ASK because its crop is missing. Similarly, DROP is unnecessary only if the removed claim is independently supported—not merely because the input question was harmless.

- **Add the results when:** each intervention has its own eligible denominator and independently established labels. Report the counts and uncertainty even if the rates are disappointing.
- **Use stronger “limited unnecessary blocking” wording only when:** the observed rates and their uncertainty support a prespecified practical tolerance.
- **Do not strengthen it when:** success depends on excluding ambiguous cases after seeing outputs, or pooling many easy PASS cases conceals a high false-CONFIRM or false-DROP rate.

### RUN IF TIME / RESOURCES ALLOW

**C — Citation-support audit**

Use two independent reviewers with access to the exact displayed passage and source version. Review every cited claim in the sampled answers, and also identify substantive claims lacking citations.

Report both claim-level support and answer-level completeness. Treat inaccessible or ambiguous sources as unassessable, not supported. Evaluate dosage mutations separately.

- **Add the results when:** support labels are reproducible and unsupported/missing-citation cases are disclosed.
- **Do not strengthen grounding claims when:** citations are frequently decorative, only partially supporting, or unavailable. Even complete support would not establish that the generator causally relied on the cited text.

**F — Interactive utility audit**

Have participants complete tasks before explaining the state labels. Record moderator assistance, not just eventual completion. Ask participants what information is missing, why advice was withheld, and how they would inspect the source or continue.

- **Add the results when:** the study yields interpretable completion counts and concrete observations about understanding or confusion.
- **Claim observed comprehensibility only when:** participants can explain and navigate the states without substantial coaching.
- **Do not strengthen usability claims when:** success occurs only after reading the paper or receiving step-by-step help. Those findings still justify reporting interface limitations.

**B — Two-generator test**

Freeze requests, images, initial conversation state, retrieval inputs, rules, and verifier version. Requests denied before T3 should produce **no generator call in either condition**.

For admitted requests, generated text and legitimate T4 decisions may differ. Compare compliance with the release contract, not identical DROP counts. For multi-turn comparisons, use identical scripted prefixes; otherwise different generated histories confound the comparison.

- **Add the result when:** both generators remain subject to the same pre-generation decisions and post-generation checks, with no observed bypass.
- **Do not claim stronger separation when:** switching generators changes admission rules, bypasses verification, or permits rejected content to escape.
- A higher verifier miss rate for one generator limits semantic reliability even if orchestration remains identical.
- Never describe two-model evidence as complete model-independence.

**H — Deployment measurement**

Measure from request submission to the complete permitted response, including generation and verification. Record blocked paths separately. Report cold starts individually or with appropriately modest summaries; do not suggest stable tail estimates from a handful of starts.

Test offline operation after documenting exactly which assets were provisioned. Also distinguish a warm cache from a fresh installation.

- **Add measurements when:** hardware, versions, assets, timing boundaries, failures, and connectivity conditions are recorded.
- **Do not strengthen offline or footprint claims when:** the tested path calls a remote generator, required weights are excluded, or only cached retrieval works.
- Slow results can still support a clearly described asynchronous deployment.

**K — SMS integrity, if SMS remains prominent**

Assess complete instructions rather than isolated fields. Determine the required fields before examining compressed output.

- **Add stronger delivery wording when:** the measured messages retain the required associations and satisfy the stated encoding/segment constraint.
- **Do not call the messages actionable when:** doses survive but chemical identity, units, or relevant conditions disappear. Report those losses and narrow the claim.
- If SMS becomes a minor optional channel, keep this appendix-only rather than expanding the main-paper story.

### APPENDIX-ONLY

**E — Paired language robustness**

Have independent speakers check that variants preserve the intended crop, intent, risk category, and relevant ambiguity. Preserve legitimate ambiguity instead of forcing every family into one decision.

Report both **correctness** and **cross-variant consistency**, with uncertainty grouped by semantic family.

- **Add the result when:** paired outcomes identify which variations preserve or change the required decisions.
- **Do not strengthen language-robustness claims when:** the system is consistently wrong, variants change meaning, or benefits occur only in a narrow hand-selected spelling pattern.
- Report troublesome variants rather than replacing them after evaluation.

**L — Evidence updating**

Use genuine validated source revisions or harmless version/provenance changes in an isolated copy; do not invent agricultural recommendations to make an update visibly different.

- **Add the example when:** the generator weights remain unchanged and the updated source is retrieved and exposed as intended.
- **Do not strengthen updateability claims when:** stale caches persist or the example requires undocumented manual edits.
- Keep the conclusion to the demonstrated update process.

**G — Qualitative gallery, with one main-figure exception**

Select the requested six categories using a declared rule—for example, a fixed eligible case ID within each category. Include the residual failure even if it is visually inconvenient. Annotate what actually happened, not just the intended outcome.

- **Add it when:** the examples make a decision or failure easier to understand than prose alone.
- **Do not present it as representative performance:** five successful illustrations and one failure do not imply an 83% success rate.
- If it replaces the unreadable existing montage, it can be the main demonstration figure. Otherwise keep it in the appendix.
- If a requested category has no verified example, state that rather than fabricating one.

### DO NOT RUN

For this submission, do not add:

- A large generator leaderboard to support architectural separation.
- New sparse/dense retrieval competitions duplicating the prior retrieval study.
- Broad vision retraining or expansion to additional crops.
- A season-long farmer, yield, or income study.
- Generic BLEU/ROUGE or a single aggregate “trustworthiness” score.
- A quantization ablation solely to rescue the unsupported claim that four-bit inference caused attack failures.
- Large paraphrase expansion counted as independent evidence.
- Extra adversarial tests whose only purpose is obtaining a near-perfect headline.
- Causal-faithfulness interventions merely to strengthen a provenance badge claim; first report the narrower citation-support property accurately.
- New field-traffic measurements solely to turn a clearly labeled cost model into a stronger deployment claim.

## 4. Rules that keep the evidence optional and honest

1. **Freeze the protocol before results:** build versions, case IDs, sampling, exclusions, expected outcomes, metrics, and proposed claims.
2. **Separate development from evaluation:** discovered failures may become regression tests, but a tuned suite is no longer an untouched estimate of generalization.
3. **Use independent checks:** do not generate expected labels using the same regex, crop tags, or verifier logic being evaluated.
4. **Preserve denominators:** distinguish requests, conversations, claims, mutations, sources, and participants. Report abstention and missing outcomes explicitly.
5. **Record all attempted cases:** timeouts, crashes, unsupported formats, and unsuccessful installations are outcomes.
6. **Keep material null and negative findings:** they may justify a limitation rather than a stronger claim. Favorable results are not the only publishable results.
7. **Version fixes transparently:** retain the failed result, identify the correction, and label any subsequent run. Do not silently redefine the benchmark.
8. **Maintain a submission fallback:** every experiment has a narrower existing claim to use if unfinished. Completed evidence that contradicts that claim must still change the wording.

The smallest useful optional package is **artifact correspondence, authorization conformance, crop-fence diagnosis, and benign controls**. Add an interactive utility audit if feasible; it answers a particularly direct demonstration question: whether someone can understand and use the controls without first reading the paper.