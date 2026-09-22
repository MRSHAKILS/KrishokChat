The paper’s strongest material is already concrete: a missing crop stops retrieval, conflicting crop evidence requires confirmation, and dosage claims face a separate release check. The repair should bring those actions forward and reduce repeated abstract framing.

Below follows the four-part editorial plan. **No manuscript text or system behavior has been changed.** Locations refer to the original LaTeX source.

## 1. Exact writing problems by section

### Title — line 53

> “KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory”

The title accurately identifies the system, language, domain, and design emphasis. Its weakness is the pair of unfamiliar modifiers before readers know what they mean.

**Recommendation:** retain it provisionally. Define “deterministic-first” and “evidence-bounded” through concrete actions immediately in the abstract. A title change is lower priority than repairing those explanations.

### Abstract — line 69

- **“Safety-critical agricultural advice creates a deployment tension”** starts with an abstract characterization. The missing-crop or conflicting-evidence problem would establish the need more directly.
- **“uncertain or actionable advice”** groups different properties: advice can be actionable without being uncertain. Identify the problematic condition—unsupported treatment or dosage.
- **“bounded generator rather than an authority”** states the principle but does not yet explain the decisions withheld from the generator.
- The six-item pipeline inventory is followed by five numerical findings. This makes the abstract read as a compressed component catalogue.
- **“453 of 454 explicit contradictions”** obscures the synthetic/farmer split and conflicts with the description of an implicit-reference miss.
- **“without rejecting any unmodified response”** needs its denominator: 38 original answers.
- The abstract says little about what the attendee can inspect.

**Repair:** organize around the concrete problem, authorization decisions, visible demonstration, and a small selection of correctly scoped results. Retain other useful results in the evaluation rather than forcing every result into the abstract.

### Introduction — lines 85–95

The opening farmer example is strong. Most repair is needed in the middle paragraphs.

- **“The system asks how much authority the model needs”** makes the system sound as though it poses a research question. The authors specify which decisions the generator cannot make.
- **“an update surface outside the model”** is unnecessarily abstract; the concrete object is an external agricultural evidence index.
- Paragraphs beginning **“KrishokTech makes these decisions explicit”** and **“The model is deliberately not the authority”** explain essentially the same principle twice.
- Edge deployment, privacy, regional guidance, normalization, and authorization arrive before their relationships are fully established.
- Farmers and extension officers should be identified as intended users before the introduction turns to the conference demonstration.
- The final paragraph’s **“one continuous farmer session”** depends on repairing the demonstration’s crop transitions.
- The license statement should be centralized in Availability and corrected using the release information identified in Prompt 1.

**Repair:** keep the opening example, explain the missing decisions, introduce the controls, then explain how normalization and external evidence support them.

### Contribution paragraph — line 93

> “Our contributions are threefold…”

The listed contributions—deterministic control, knowledge-centric deployment, and Bengali/Banglish control—do not match the immediately preceding C1–C3 organization.

**“knowledge-centric edge deployment”** is also a broad noun phrase that obscures the implemented behavior.

**Repair:** describe one integrated system with three control responsibilities:

1. Request admission and policy referral.
2. Crop-specific evidence binding and conflict confirmation.
3. Dosage-claim release.

Treat normalization, updateable knowledge, and local deployment as properties supporting that integration. Keep the existing statement that dialect understanding and field effectiveness have not been established.

### Related work and positioning — lines 105–109

- **“KrishokTech instead focuses…”** can imply that prior advisors do not clarify, constrain, or refuse. The cited discussion does not establish such a categorical distinction.
- **“an unresolved safety condition rather than an incomplete conversational turn”** offers a rhetorical contrast between descriptions that can both be true.
- The long citation group on claim checking combines different mechanisms without explaining their particular relationship to this system.
- **“script-agnostic deterministic checks”** is broader than normalization for tested Bengali/Banglish variants.
- The authors’ prior benchmark and retrieval work are cited elsewhere but not explicitly distinguished from this demonstration.

**Repair:** compare mechanisms and inherited resources. Identify what is reused, then state what the present runtime integration adds. Avoid implying that deterministic checks, clarification, or external retrieval are individually unprecedented.

### System design — lines 114–145

The stage descriptions contain some of the manuscript’s best prose. The problems concern precision and placement.

- Lines 114–116 repeat the authorization principle before explaining the checks.
- **“Those permissions belong to deterministic stages”** needs to distinguish deterministic enforcement from fallible inputs, including learned vision predictions and the separately reported classification branch.
- **“identifies the crop”** can imply certainty. For the vision model, “predicts” is the more precise verb.
- **“This prevents evidence for an unrelated crop from reaching generation”** is stronger than the unresolved retrieval results permit.
- Confidence thresholds are promised in an appendix that does not currently supply them.
- The explanation of why sparse retrieval is defensible interrupts the operational description. One concise design rationale is enough.
- The generation paragraph mixes control flow, training, quantization, serving software, latency, and deployment audience.
- “DROP” needs a consistent meaning: removing a claim may permit the remaining response to be delivered; it does not necessarily terminate the whole turn.

**Repair:** describe each stage through its input, decision, and consequence. Keep implementation details when they explain that decision; relocate other deployment details. Preserve the narrow description of T4.

### Demonstration — lines 180–195

- The introduction names the attendee audience but should quickly establish what attendees can change and inspect.
- S1 binds potato. S2 introduces rice and silently changes the session’s crop. That transition bypasses the conflict behavior being demonstrated.
- S3 does not describe the farmer’s confirmation or the resulting state.
- S5 does not explain how the prior conflict and referral have been resolved.
- **“verified residue”** is awkward and can imply that every remaining statement has been verified. The verifier checks only specified dosage claims.
- The text must distinguish a deliberately injected dosage error from an error produced spontaneously during a live run.
- Claims of matching the screencast’s order need reconciliation.

**Repair:** use an action → visible response → next permitted action pattern. Describe actual confirmation or reset steps; do not invent them to make the narrative flow.

### Evaluation — lines 200–248

The three-question structure should stay, but the evidence needs clearer grouping.

- **“wrong-crop advice”** names a generated-output outcome although the measurement concerns retrieved sources.
- Q2 begins with disease-classifier accuracy before defining the retrieval test. This encourages readers to confuse disease accuracy with crop-routing accuracy.
- The conflict paragraph pools farmer and synthetic cases before explaining their different origins.
- **“only 20%”** adds rhetorical emphasis to a baseline measured on a separate set.
- Q3 begins with full-pipeline attacks and Banglish interception, although its heading concerns dosage release.
- Line 239 mixes models, suites, languages, failure categories, and an unsupported explanation involving four-bit quantization.
- Line 241 combines the output audit and two verifier experiments in one paragraph.
- **“Constrained delivery preserves the dose”** overstates a result with observed losses.
- **“Appendix … ledgers every result”** is unnatural phrasing and currently stronger than the appendix’s coverage.

**Repair:** give each experiment a compact sequence: question, sample and unit, comparison, result, interpretation. Keep full-pipeline ASR distinct from evidence attributable to an individual control. Unresolved counts must remain editorial queries until reconciled.

### Limitations — line 259

The paragraph contains substantive limitations but packs unrelated issues into four long numbered clauses.

- **“Four limitations qualify the three questions”** foregrounds document organization rather than practical limits.
- Knowledge updating and support for entirely new crops are treated too similarly.
- The unreconciled cloud/local comparison reappears as if it were settled.
- Coverage, implicit references, attack residuals, SMS information loss, and local latency deserve clearly separated explanations.

**Repair:** group limitations by what users may encounter: incomplete evidence coverage, unresolved language/image ambiguity, residual unsafe output, and delivery/deployment constraints.

### Availability — line 263

This section needs factual correction before stylistic polishing.

- **“Code, models, and container scripts are licensed under Apache-2.0”** applies one license across different artifacts.
- The next sentence assigns another license to a model without clearly distinguishing the asset.
- Repository-level links do not identify the exact language-model and evidence releases claimed.
- The withheld T0 resources are described without clearly stating their effect on reproducing the public package.

**Repair:** identify each artifact, version, access route, and applicable license. Separate hosted functionality from what can be reproduced using the released package.

### Conclusion — line 267

The conclusion is largely strong.

- The first two sentences repeat the same point, but the second makes it concrete and deserves priority.
- The normalization/evidence sentence carries two supporting mechanisms and a limitation in one sentence.
- The closing limitation is appropriate and should remain.

**Repair:** retain the draft/control distinction, state what the demonstration makes observable, and finish with the bounded evidence and remaining farmer evaluation. Do not introduce a broader framework claim.

### Ethics and broader impact — lines 276–288

- Annotation-agreement statistics interrupt the data-governance discussion; they belong primarily in evaluation methods.
- **“The chemical-advice pathway fails closed”** is insufficiently qualified given reported misses.
- **“ensuring life-safety emergencies are never delayed”** claims an external assistance outcome that displaying a referral cannot establish.
- **“Cloud calls were limited to offline benchmark evaluation”** conflicts with the connected live mode described in System Design.
- **“Unresolved or unsafe cases end in a referral”** overlooks ASK and CONFIRM.
- Absolute image-handling and retention statements need configuration-specific support.
- The sandbox statement **“without giving any chemical advice”** needs a clear scope: blocked toxic-chemical requests or every chemical-related interaction.

**Repair:** organize around data handling, recognized-risk behavior, remaining failures, referral limits, and deployment-specific processing. Preserve direct admissions of residual risk.

## 2. Recommended narrative changes

Use the requested opening–middle–ending pattern as a guide to paragraph function, without forcing every short section into three paragraphs.


| Section       | Opening: why it matters                                                        | Middle: what happens                                                                             | Ending: what the reader understands                               |
| ------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| Abstract      | A treatment question can lack the information needed to proceed.               | Controls govern admission, crop evidence, confirmation, referral, and dosage release.            | What the demo exposes and what bounded results support.           |
| Introduction  | Concrete farmer question and consequence of a wrong crop/dose.                 | Authorization principle, intended users, and C1–C3.                                              | The integrated contribution and attendee experience.              |
| Related work  | Existing advisors provide useful conversational and retrieval capabilities.    | Compare clarification, evidence checking, multimodal conflict, and the authors’ prior resources. | The specific runtime integration contributed here.                |
| System design | Draft quality alone does not determine whether a request or claim may proceed. | T0–T4 inputs, decisions, transitions, and delivery.                                              | Where authorization resides and what remains fallible.            |
| Demonstration | Attendees need to inspect decisions, not just final answers.                   | Five scenarios with explicit state changes and user actions.                                     | How a blocked or questioned request resumes, or ends in referral. |
| Evaluation    | Each control requires an observable test.                                      | Admission, evidence binding, dosage release, then clearly labeled system-level evidence.         | Which behaviors are supported and which outcomes remain untested. |
| Limitations   | Errors can enter through inputs, evidence, generation, and delivery.           | Specific residuals and operating constraints.                                                    | The supported scope of use.                                       |
| Availability  | Readers need access to the demonstrated configuration.                         | Exact artifacts, versions, licenses, modes, and restrictions.                                    | What can be tried and reproduced.                                 |
| Conclusion    | Return briefly to the authorization problem.                                   | Summarize the demonstrated separation of drafting and control.                                   | Bounded prototype evidence and remaining farmer evaluation.       |
| Ethics        | Incorrect treatment advice can cause harm.                                     | Data governance, processing modes, policy-triggered actions, and residual risks.                 | What the system can do and what still requires human assistance.  |


The contribution paragraph should bridge the introduction to this structure. It does not need a separate miniature introduction and conclusion.

## 3. Concrete rewrite plan

1. **Fix the vocabulary before editing paragraphs.**  
Use consistent meanings for *request*, *turn*, *draft*, *retrieved passage*, *dosage claim*, and *delivered response*. Distinguish predicted crop, user-confirmed crop, and the crop bound to retrieval. Define ASK, CONFIRM, and REFER as interaction outcomes and clarify whether DROP is a claim-level action.
2. **Align the contribution statement with C1–C3.**  
Keep one system story throughout the introduction, architecture, evaluation, and conclusion. Explain normalization, external evidence, and local deployment where they support those controls.
3. **Repair the introduction and related work first.**  
Preserve the farmer example. Consolidate the repeated authority discussion. Replace abstract terms such as “update surface” with the actual component. Add a concise comparison with the authors’ prior resources and benchmark work.
4. **Rewrite stage descriptions around observable operations.**  
For each stage, specify what it reads, what rule or prediction it uses, what it permits or blocks, and what the user sees. Keep model training and hardware details out of the control-flow explanation unless necessary to understand a deployment mode.
5. **Repair the demonstration using verified transitions.**  
Resolve potato→rice context changes, confirmation, and continuation after referral. Identify any injected draft. Align captions, scenario text, and recording. Replace “verified residue” with language accurately describing the remaining response and the verifier’s limited scope.
6. **Restructure evaluation without adding claims.**  
Put Banglish precheck evidence with admission controls. Define retrieval contamination before reporting it. Separate farmer and synthetic conflicts. Give the output audit and verifier tests separate paragraphs. Label full-pipeline ASR accordingly rather than attributing it to T4 alone.
7. **Resolve factual dependencies before finalizing affected sentences.**  
The cloud counts, multi-turn membership, hard-fence residuals, execution modes, privacy statements, and artifact licenses cannot be repaired through confident wording. Track these as author queries. Where records remain unavailable, remove or narrow the disputed claim without substituting an invented value or behavior.
8. **Revise limitations, availability, and ethics together.**  
These sections must describe the same release and execution modes. Keep residual risk explicit; replace outcome guarantees with the action actually performed. Move annotation statistics to methods while retaining collection and consent information in ethics.
9. **Write the abstract last and check two-column readability.**  
Select representative results only after their interpretation is settled. Preserve useful technical nuance; split sentences when they combine different experiments or actors. Use recovered space to clarify transitions and improve figure readability, not merely to make the paper shorter.

## 4. Sentences that should stay

These sentences are already strong. Quotations retain the wording while omitting LaTeX commands and citation markup. Their surrounding context and factual support should remain intact.

**Introduction, line 85**

> “When yellow spots appear on potato leaves, a farmer often needs advice before an extension officer can visit.”

A concrete actor, problem, and practical constraint.

**Introduction, line 87**

> “A farmer may ask ‘which pesticide should I spray?’ without naming the crop.”

Directly establishes why a fluent answer is not the first required action.

**System design, line 121**

> “The first decision is whether a request should reach retrieval at all.”

A clear opening for the admission subsection.

**System design, line 125**

> “The pipeline halts before BM25 retrieval runs (sources_retrieved = 0) and enters ASK.”

Connects the internal operation to its visible state.

**System design, line 130**

> “Requests that pass the information gate enter T2, where crop identity determines what evidence retrieval is allowed to access.”

Precisely states the purpose of crop binding.

**System design, line 123**

> “The boundary follows the system’s safety policy; it does not attempt to reproduce the full regulatory status of every chemical.”

An important distinction that prevents policy behavior from being mistaken for regulatory classification.

**System design, line 143**

> “This verifier is intentionally narrow: it checks dosage-bearing numerical claims and does not establish the factual correctness of every agronomic statement in the response.”

One of the paper’s strongest scope statements.

**System design, line 145**

> “The badge exposes the retrieved source and verification path; it does not by itself establish that every citation was causally used by the generator.”

Preserves a technically important distinction about provenance.

**Evaluation, line 224**

> “The gate halted all 30 crop-less queries before retrieval and passed the other 170 to fenced search without a false halt.”

A strong result when retained beside the description of the 200-query cohort.

**Evaluation, line 241**

> “For the dosage verifier, we inserted controlled errors into verified answers.”

Clearly identifies the experimental intervention. Do not let later summaries obscure that these were inserted errors.

**Conclusion, line 267**

> “The model drafts, while deterministic controls decide access, confirmation, referral, and dosage release.”

The clearest existing expression of the requested central story.

**Conclusion, line 267**

> “No claim of field effectiveness is made; evaluation with farmers remains to be done.”

A concise and appropriate boundary on the demonstrated contribution.

**Ethics, line 282**

> “We report these residuals and do not claim that the system prevents all unsafe output.”

Keep this adjacent to the concrete residual results.