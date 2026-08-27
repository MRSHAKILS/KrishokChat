# CEA Paper — Evidence-Controlled Revision Outline

**Target venue:** *Computers and Electronics in Agriculture* (Elsevier)

**Manuscript:** `krishokchat_cea.tex`

**Revision status:** first-round manuscript revised after adversarial review of the Qwen literature review and cross-check against the project claim ledger, experiment registry, specifications, runners, and frozen result artifacts.

**Primary rule:** the paper must distinguish (i) the production runtime, (ii) the offline research harness, and (iii) the proposed deployment architecture. A result from one layer cannot be presented as a universal property of the other two.

---

## 1. Editorial decision from the review

The Qwen review supplied a strong CEA direction, but it also introduced claims that are not safe to publish. Its useful idea is to frame KrishokChat as a low-resource agricultural advisory system whose safety depends on the interaction between evidence, perception, routing, network failure, and delivery channel. Its unsupported parts are the claims of hard zero hazard, dialect immunity, field readiness, completed hardware profiling, and settled national economics.

The revised paper therefore makes a narrower and stronger argument:

> **For a bounded Bengali agricultural fact base and specified query workloads, conditioning deterministic lookup on structured crop/disease metadata can reduce dependence on text retrieval and LLM inference. A typed, fail-closed certification contract can then prevent certification when required relations are not jointly supported. The paper evaluates this architecture under separate linguistic, network, channel, provenance, and cost stress tests; it does not claim field deployment, universal safety, or causal farmer benefit.**

This is a systems-engineering contribution supported by measurable evidence, not a claim that the application has already solved rural extension.

### 1.1 Storyline (practical Bangladesh vignette)

1. \textbf{The physical stake.} A farmer thirty kilometres outside Kurigram holds a sub-\$120 handset on flickering 2G and types a Chittagonian-inflected description of a leaf symptom. A fluent but misbound advisory -- right chemical, wrong dose interval, missing PHI -- is not a lower BLEU score. It is a burnt plot, a poisoned operator, or contaminated water.
2. \textbf{Three distinct fragilities.} In this setting a cloud-only chatbot (needs a live round trip), a text-only retriever (needs formal Bengali), and a \$2.30/1k commercial inference bill are each individually plausible in the lab and each individually fragile in the field. The paper evaluates them as separate endpoints.
3. \textbf{Measured premises.} The project's own benchmark measured treatment correctness below 44\% and a residual chemical-hallucination floor even with evidence; the retrieval study measured lower performance on regional/romanised queries. These motivate explicit evidence binding and motivate the routing experiment; they do not prove that every LLM or cloud system fails.
4. \textbf{The systems hypothesis.} A reliable structured signal -- crop/disease classification metadata from a 5.90\,MB INT8 model plus a 1.25\,MB intent artifact -- can gate deterministic fact lookup \emph{before} language retrieval or generation. The same gate introduces classifier error, so misrouting (3.15\%) and fallback (13.55\%) are reported.
5. \textbf{The safety contract.} A typed 11-slot tuple is certifiable only when required relations are jointly supported by one authoritative record ($\rho=+1$, correct parsing, no bypass). Otherwise the system abstains or escalates to 16123. The evaluation therefore asks how often the tested path accepts a harmful candidate, not whether the deployment is universally safe.
6. \textbf{The CEA evaluation.} The paper measures routing (516.4/2{,}135 nodes, Hit@1 vs.\ coverage), zero-LLM handling (61.52\% terminal, 51.04\% deterministic advisory), network/channel behaviour under simulation, cache provenance, and modelled cost -- each as a named, bounded observation.
7. \textbf{The bounded conclusion.} The results support reduced text/LLM dependence for the tested workloads and justify the next decisive tests: physical-device profiling (E16), carrier delivery, live chunk-fallback lane (E26), per-tier agronomic correctness labels, and field-like escalation studies. They do not establish universal safety, dialect immunity, or national readiness.

### 1.2 What is explicitly not claimed

- No “first system,” “first Bengali agricultural verifier,” or priority claim.
- No universal or statistical guarantee of zero real-world hazard. Zero observed events are reported with sample sizes and confidence bounds.
- No dialect immunity. The correct phrase is **reduced text dependence on the evaluated image-conditioned path**.
- No claim that coverage, Hit@1, slot completeness, provenance, or zero-LLM handling equals agronomic correctness.
- No field deployment, farmer-benefit, trust, usability, yield, poisoning-reduction, or adoption claim.
- No battery or thermal result: E16 is planned/blocked and must not appear as completed evidence.
- No claim that E26 is a complete live-lane safety evaluation: it is offline-lane and `done_unverified`.
- No claim that E25 matches the LLM on joint parsing: the measured joint classifier result is 78.4% versus 94.2% for the comparison arm.
- No claim that E14 or E20 values are settled until their result artifacts, ledger entries, summaries, and registry status are reconciled.

---

## 2. Evidence and status ledger for assembly

### 2.1 Experiment status convention

Every result table must include or cite one of these statuses:

| Status | Meaning in the manuscript |
|---|---|
| `done` | Runner and result artifact exist; the layer is listed as completed in the canonical registry. |
| `done_pending_acceptance` | A result artifact exists, but `acceptance.accepted_by` remains `PENDING`; use only after the author confirms the result is publication-ready. |
| `simulated` | The layer models a constraint or emulates a deployment condition; it is not a field measurement. |
| `offline_only` | The layer does not exercise the full live production path. |
| `done_unverified` | Frozen output exists but author sign-off or live-lane verification is incomplete. |
| `planned_or_blocked` | Not evidence; may appear only in limitations/future work. |

At the current audit, E16 is `planned`; E26 is `done_unverified`; E14, E15, and E17–E25 have result artifacts but their YAML acceptance blocks remain `PENDING`. The manuscript must not say that every layer is author-accepted.

### 2.2 Reconciliation blockers before submission

1. **E14:** the YAML `metrics` block reports 91.4% cache versus 82.0% cloud at 15% loss and 58.1% versus 12.8% at 30% loss. The claim ledger and summary also contain 80.3% and 58.7% values. Freeze one regenerated result and update the ledger before using a headline E14 number.
2. **E20:** the metrics block supports 2.86 versus 0.69 Crore BDT and 2.17 Crore savings; another summary/acceptance note says 28.57 versus 2.17 Crore and 22.8 Crore savings. Reconcile units, price assumptions, and arithmetic.
3. **E25:** the YAML metrics report 96.4% crop, 78.4% pest, 100.0% intent, and 78.4% joint accuracy. The ledger/summary contain different component values. Use the regenerated artifact and update the ledger.
4. **E17:** threshold-specific values must not be mixed. At $\gamma=0.80$, use the corresponding per-register values from the threshold-0.80 block; do not combine threshold-0.70 baselines with threshold-0.80 outcomes.
5. **E23:** report tamper detection and zero deprecated records surviving invalidation; do not publish the contradictory `invalidation_propagation_completeness_pct: 0.0` field.
6. **Layer count:** define the aggregation. Do not write “25 completed layers” when E16 is planned and E26 is `done_unverified`. If the count cannot be reconciled, report the named layers instead of an aggregate.

---

## 3. Paper identity

### Title

> **Evaluating Detection-Gated Deterministic Routing for Fail-Closed Agricultural Advisory under Low-Connectivity Constraints**

This title names the mechanism and evaluation setting without implying national deployment, field outcomes, or universal safety.

### Core contributions (all 7 novelties, evidence-controlled)

1. **N1 -- Detection-Gated Deterministic Routing (DGDR):** metadata-gated partition (2{,}135$\to$516.4, $\gamma=0.80$) with Hit@1/coverage vs.\ text-first, plus explicit misrouting and pairing caveats (E17, E19, E21, E25).
2. **N2 -- Conditional fail-closed certification:** typed 11-slot, single-record joint binding, abstention/escalation; evaluated across adversarial, generator, retrieval, dialect, and channel suites as observed dangerous acceptance with Wilson bounds (E02--E05, E07--E13, E21--E22).
3. **N3 -- Network-resilient offline-first cache:** emulated 2G/Edge delivery vs.\ cloud-only plus SHA-256 hash-chained invalidation (791\,B delta, 100\% mutation detection) as simulation/software tests (E14, E23).
4. **N4 -- Deterministic GSM-160 gateway:** 11-slot$\to$160-char template preserving selected slots (102--115\,chars) vs.\ 64.4\% PHI hazard and 36.4\% SMS injection leakage for the LLM control (E15, E22).
5. **N5 -- Localised telecom-economic scenario:** BTRC 0.25\,BDT/SMS, hosting amortization, and measured 61.52\% zero-LLM mix as a scenario model with stated assumptions and sensitivity limits (E09, E18, E20).
6. **N6 -- Measurable knowledge-growth loop:** 2 BARI facts, 18\,min, 55-query Chili Anthracnose closure (3.06 queries/min) as a narrow operational observation; plus exploratory chunk-fallback (E24, E26).
7. **N7 -- Double-blind agronomist review:** 3 experts, 200 responses, Gwet's AC$_{1}=0.862$, 96.5\% deployment approval as a bounded human review, not a field outcome (E13).

### Research questions

- **RQ1 — Routing:** Under the evaluated query construction, does structured detection metadata reduce the candidate search space and improve retrieval/coverage metrics relative to text-first lookup?
- **RQ2 — Dependency:** What proportion of the specified workload reaches a zero-LLM terminal path, and how do its latency and modeled serving cost compare with the baseline?
- **RQ3 — Safety behavior:** In separately evaluated generator, retrieval, dialect, and channel suites, how often does the certification path accept a harmful candidate, and what are the confidence bounds?
- **RQ4 — Network:** Under simulated network profiles, how does offline-first caching change delivery success and cache latency, and what stale-record behavior is observed?
- **RQ5 — Channel:** Does deterministic template composition preserve selected safety-critical fields within the GSM-03.38 budget, and can tested injection payloads survive into outbound SMS?
- **RQ6 — Operations:** What do the specified local-cost assumptions imply for serving scenarios, and how much demand coverage did one targeted fact-authoring intervention add?

---

## 4. Section plan and storyline

### Abstract — 200–250 words

Use: setting → safety/deployment problem → architecture → evaluation scope → results with status qualifiers → bounded conclusion. Do not list unresolved aggregate layer counts. If E14/E20 are not reconciled, omit their headline values from the abstract. Avoid “guarantee,” “immune,” “eliminate,” “nationally deployable,” and “no trade-off.”

### 1. Introduction — strong motive, ~1.5–2 pages

1. Define agrochemical advisory as a safety-critical systems problem, not just a language-generation task.
2. Introduce Bangladesh as the concrete deployment setting, using only verified local statistics and the real 16123 escalation endpoint. Do not infer access or benefit from the existence of a phone channel.
3. Present three measured constraints: (a) treatment-generation/evidence risk, (b) dialect-sensitive text retrieval, and (c) network/channel limitations. Mark E14 as simulation and E15 as a message-composition test.
4. Introduce the hypothesis: reliable structured metadata can reduce the text/LLM dependency for a bounded path, but perception errors become a new risk that must be reported.
5. Explain the fail-closed contract and its assumptions: correct parsing, authoritative/current record, no bypass, complete required fields, and tested implementation.
6. State the four contributions and six questions.
7. End with a roadmap paragraph.

### 2. Related Work — strong comparative taxonomy, ~1.5–2 pages

Use verified sources from `paper/literature review/`, not Qwen’s social-media, Reddit, blog, or ResearchGate links as primary evidence. Six concise groups, each ending in a bounded gap:

1. **Agricultural advisory and extension systems:** Farmer.Chat, KrishokBondhu, AIEP, and the team's two authoritative prior papers. Compare input channel, grounding, expert evaluation, escalation, and deployment evidence.
2. **RAG, claim verification, and safety:** RAG, FActScore, FacTool, RAGChecker/RT4CHART, VeriCite, and medical verifiers. Distinguish atomic/propositional checks from joint agronomic tuple binding; do not claim universal absence of competitors.
3. **Selective answering and abstention:** RefusalBench, ConfRAG, CRAG, Self-RAG, and calibrated uncertainty. Position abstention as an operating policy, not a proof of safety.
4. **Bengali, dialect, and low-resource retrieval:** standard Bengali versus regional/romanized input. Relate the prior retrieval diagnosis to the present routing experiment without calling the result dialect immunity.
5. **Vision and edge agricultural computing:** crop/disease classification and mobile inference. State that the checked artifacts classify and do not localize lesions; the paper's differentiator is the evaluated use of metadata for routing, not a priority claim.
6. **ICT4D channels and offline service delivery:** SMS/IVR/USSD, offline-first applications, human escalation, and national extension infrastructure. State that this paper measures software/simulation behavior, not adoption or farmer outcomes.

### 3. System Architecture — heart of the paper, ~2.5–3 pages

- Deployment constraint table (device, model, packet loss, GSM length, update bandwidth, escalation).
- Production runtime versus research evaluation pipeline box.
- DGDR: classifier metadata → partition → deterministic traversal → explicit fallback.
- Five-tier ladder: separate successful deterministic advisory paths (T1/T2) from T0 safety handling and T4 refusal.
- 11-slot schema and conditional certification contract.
- Offline cache and signed/hash-chained invalidation.
- Deterministic SMS channel and its Tier 1/2 scope.
- Human escalation to 16123 as a defined endpoint, not a measured outcome.

### 4. Core Algorithms — ~1.5 pages

1. Detection-gated resolution with classifier confidence, no-image path, fallback, and misrouting accounting.
2. Typed relational verification with null extraction → abstention, one-record joint binding, conflict handling, and no-bypass condition.
3. Hash-chained cache invalidation with version checks and stale-record rejection.
4. GSM-160 template renderer with preflight slot survival; never use hard truncation as a safety mechanism.

### 5. Experimental Methodology — ~2 pages

- Define production, research-harness, simulated, offline-only, and projected evidence.
- Master matrix: layer, status, input, baseline, $N$, primary metric, artifact, limitation.
- Define non-equivalent endpoints: Hit@1, coverage/non-abstention, joint accuracy, slot completeness, provenance, dangerous acceptance, delivery success, cost.
- State that zero observed events are not universal zero-risk results; report Wilson bounds.
- Explicitly record the E17 image/query pairing caveat, E25 synthetic/generated training data, E19 small graph, E26 offline lane, and E16 blocked hardware study.

### 6. Results — order by reviewer value, not layer number

1. **Measured premises and baseline risk:** prior benchmark treatment/evidence limitations and text-first dialect behavior.
2. **Routing:** E17 search-space reduction, threshold sweep, per-register Hit@1, 3.15% misrouting.
3. **Coverage versus safety:** E21 cross-tab coverage and observed hazard; never label coverage accuracy.
4. **Zero-LLM terminal handling:** E18; separate T1/T2 advisory paths from T0 and T4; report $N=5{,}000$.
5. **Deterministic fact graph:** E19, scoped to 23 nodes, 36 edges, nine facts, five target pairs.
6. **Intent classifier trade-off:** E25, including 78.4% joint accuracy versus 94.2% LLM comparison, latency, and footprint.
7. **Network simulation:** E14, both 15% and 30% loss profiles after reconciliation; no field language.
8. **Cache provenance:** E23 tamper detection, delta payload, and zero surviving deprecated records; no universal invalidation guarantee.
9. **GSM channel:** E15 slot survival and PHI hazard; E22 outbound-SMS injection survivability.
10. **Safety stressors:** E02, E03, E05, E07/E08, E10–E13; per-suite $N$, scope, zero counts, and upper bounds.
11. **Scenario economics:** E09/E20 after arithmetic reconciliation, assumptions and sensitivity limits.
12. **Knowledge growth:** E24 narrow Chili Anthracnose intervention; E26 exploratory offline-lane result.

### 7. Failure Taxonomy

Organize failures as perception error, retrieval omission, unsupported extraction, relation misbinding, stale cache, channel overflow, injection survival, and over-refusal. For each: trigger, observable symptom, disposition, and whether evidence is measured or proposed. Include the known source-empty verification defect as a production threat to validity.

### 8. Discussion

1. The result is a conditional systems trade-off: lower latency/serving cost and higher measured coverage on some registers, against classifier joint-accuracy loss, 3.15% misrouting, bounded corpus scope, and residual T3 dependence.
2. Explain why the certification contract can be safer than lexical matching under its assumptions, without calling it a universal guarantee.
3. Discuss integration with DAE/16123 as a deployment hypothesis; do not claim referral follow-through.
4. Discuss policy value of explicit abstention and operator workload without measuring workload.
5. Generalize only as a testable design hypothesis for other domains.

### 9. Limitations and threats to validity

State explicitly: E14 simulated; E16 not run; no physical energy/thermal data; no live carrier/SMS gateway; image-query pairing caveat; E19 small graph; E25 5,000 generated/labeled samples and joint-accuracy deficit; coverage is not correctness; E26 offline lane and `done_unverified`; current runtime/research-path distinction; economic assumptions and excluded device/support/maintenance/escalation costs; no field, farmer, trust, yield, or poisoning outcomes; one-record certification caps recall.

### 10. Reproducibility and ethics

Report `experiments/registry.yaml`, per-layer specs/runners/results, hashes, seeds, status fields, production/research separation, local-only audit, privacy redaction limits, consent/licensing boundaries, and the short 16123 safety escalation. Do not say every layer is author-accepted while YAMLs say `PENDING`.

### 11. Conclusion

Return to the bounded claim: the evaluated design reduces text/LLM dependence for selected workloads and preserves tested safety fields under specified stress tests. The next evidence required is physical-device, carrier, live-lane, expert-correctness, and field-like validation.

---

## 5. Figures and tables

### Figures required

1. **Architecture:** edge client, classifier metadata, deterministic tiers, LLM fallback, verifier, cache, SMS, and 16123 endpoint. Clearly mark research-only components.
2. **DGDR decision flow:** $\gamma=0.80$, 2,135 → 516.4, 13.55% fallback, 3.15% misrouting.
3. **Routing/coverage figure:** paired coverage bars for four registers with a separate zero-observed-hazard annotation; distinguish E17 Hit@1 from E21 coverage.
4. **Network figure:** grouped bars for 15% and 30% packet-loss profiles, with profile labels and reconciled values only.
5. **SMS slot strip:** ten slots across deterministic template, LLM summary, and naive truncation; highlight PHI survival and label all values as tested-suite results.

### Table rules

- Every table names the experiment, status, $N$, metric definition, and baseline.
- Do not place E17 Hit@1, E21 coverage, and E25 classifier accuracy in one unlabeled “accuracy” column.
- Do not report a model target as a result.
- Do not use a competitive-matrix row unless its external facts have a verified source.

---

## 6. Required follow-up artifacts

Before submission, create:

- `FIGURE_PROMPTS.md` with poster prompts for the architecture and DGDR figures, explicitly excluding unsupported numbers.
- `SUGGESTIONS.md` with the E14/E20/E25 reconciliation actions, E23 field anomaly, E16/E26 status, sensitivity-analysis plan, and cover-letter language using “evaluated architecture” rather than “deployment-ready system.”
- An amended claim ledger or reconciliation note before promoting any disputed metric.

No additional figure generation is required for this revision if the five required figures can be drawn from reconciled YAML metrics. A physical-device or live-carrier figure must not be generated because those experiments have not been run.
