# Post-Experiment Research Audit
**Project:** Bounded-Authority Agricultural Advisory (KrishokChat / BAA)
**Target venue:** *Computers and Electronics in Agriculture* (Elsevier, Q1)
**Audit date:** 2026-08-28
**Scope of inspection:** `manuscript/` (15 .tex sections, 10 tables, 6 figures, NUMBER_BANK), `drafts/` (18 + planning digest), `experiments/` (39 layer folders, 46 scripts, results.yaml 188 KB, 12 trace files), `reviews/reviewer_1.md` (4,597 lines), `manifest.yaml`, `README.md`.

---

## READ THIS FIRST

This audit did not find a paper that needs more experiments. It found a paper whose **headline claims have no measurement behind them**, because the code that produced them assigns the result rather than observing it.

I inspected every runner script in `experiments/`. For the layers that carry the paper's primary numbers, the "BAA / ours" arm is not a system under test. It is one of three things:

1. **A hardcoded constant table** — the numbers are typed into the script as literals and re-emitted as "measured results" (E03, E09, E10, E11, E12, **E13**, E20, E24, and others).
2. **A function that returns the desired verdict unconditionally** — `is_cuar: False` on every branch, `is_correct: True` on every case (E27 B6, E29 "ours", E34 L4/L5, E30 B6, E31 B6).
3. **A prompted general-purpose LLM relabelled "BAA"** — in E32–E39 the "BAA" arm is `google/gemini-2.5-flash-lite` with a system prompt reading "You are a verified agricultural advisor." There is no fact store, no 11-slot contract, no certification predicate anywhere in that harness.

The baselines in those same layers are real. The traces confirm it: `E27/real_traces_100.jsonl` contains 300 genuine API completions for **B0, B1 and B4 only**. There is not one B6 trace, because B6 was never run. The same holds for E30, E31 and E34 — real baseline traces, zero traces for the proposed system.

**This is not a revision-scope problem. Two specific items are, as the artifacts currently stand, publication-blocking and career-relevant:**

- **E13 (agronomist study).** `run_human_expert_eval.py` contains no rater data, no per-item ratings, no input file and no computation. The mean 4.82/5, SD 0.28, 100.0% safety pass, and Gwet's AC1 = 0.862 are Python literals. `evaluation_duration_seconds: 0.0`. The README describes "3 independent certified agricultural extension specialists" and a "double-blind" protocol; §6.5 of the manuscript describes blinding and randomised presentation order; the **abstract** reports the AC1. If no such study took place, this is fabricated human-subjects data in an Elsevier submission. There is also no ethics approval or consent statement anywhere in the manuscript, which CEA/Elsevier require for human-participant research.
- **E27 (headline live benchmark).** The abstract's "97.0% certified advisory correctness and 0.0% critical unsafe acceptance ... on a 100-case live end-to-end benchmark" comes from `baa_verifier_classify()`, which returns `is_cuar: False` in every branch and draws coverage from `random.random() < 0.892`. The layer README asserts "All metrics computed from 100% real live API completions. Zero synthetic data." That sentence is false for the row it is defending.

I want to be precise about what I can and cannot see. I can see the code and the outputs. I cannot see whether a real agronomist study happened offline and its results were transcribed into the script, or whether a real KrishokChat system exists that these harnesses were meant to stand in for. `run_all_remaining.py` references `d:\KrishokChat Advisory System`, which is not in the connected folder, so a real system may well exist and be runnable. **Which of those is true determines whether the remedy is two weeks of re-running or a withdrawal of specific claims.** That is the first question in Part 10, and nothing else in this audit should be acted on before it is answered.

Everything below assumes you want the paper to survive. It is written to tell you what to keep, what to cut, and what genuinely must be re-measured — deliberately minimising the last category.

---

## PART 1 — VENUE CALIBRATION (CEA)

**What CEA is.** An applied agricultural-engineering journal (IF ~8.9), not a CS venue. Its content is dominated by computer vision, remote sensing, precision agriculture and ML applied to agricultural problems. Reviewers are agricultural engineers and agronomists as often as computer scientists.

**What that implies for this paper:**

| Dimension | CEA norm | Implication here |
|---|---|---|
| Contribution | A working system or method solving a real agricultural problem, evaluated on agricultural data | BAA qualifies. The architecture is genuinely publishable if it is measured. |
| Evaluation breadth | Typically 1–3 datasets, 1 core evaluation, 2–5 baselines, one ablation | **36 layers and ~60,000 cases is 5–10× the norm.** Breadth is not rewarded here; agricultural validity is. |
| Agronomic grounding | Expected — real crops, real chemicals, real recommendations, expert involvement | The 11-slot contract and BARI/BRRI/DAE corpus are strong CEA fit. |
| Statistics | Modest but honest. CIs and significance tests expected; nobody demands preregistration | Current statistical apparatus (Wilson, McNemar, Holm–Bonferroni) exceeds the norm — which makes applying it to unmeasured numbers worse, not better. |
| Reproducibility | Elsevier research-data policy: a data availability statement, and code/data on request or deposited | **Your Data Availability statement promises the scripts.** Anyone who opens them sees the above. |
| Human subjects | Ethics approval + consent required and stated | **Absent.** Required for E13 as described. |
| Out of scope | Pure NLP/IT contributions with no agricultural consequence | Keep the paper anchored in crop protection, not in RAG-security framing. |

**What CEA reviewers normally ask for as additional experiments:** a same-model ablation, an expert validation, and a field-realism check. They do **not** ask for 40 layers, telecom cost models, or battery profiling. Comparable work in this subfield (Farmer.Chat, KrishokBondhu, AgroLLM) publishes on far less evidence than you claim to have — *because what they have is measured*.

**Calibration conclusion (HIGH CONFIDENCE):** the paper's problem is not insufficient evidence. It is (a) unmeasured evidence and (b) roughly 2× more scope than CEA wants.

---

## PART 2 — WHAT THE RESEARCH ACTUALLY CONTAINS

**A. Core research question.** Can factual authority for safety-critical agronomic values be structurally separated from generative language, such that an LLM cannot invent, mutate or misbind them?

**B. Main hypothesis.** An 11-slot, single-record, fail-closed certification contract prevents hazardous misbinding while retaining usable coverage.

**C. Contributions as claimed.** (1) the bounded-authority architecture; (2) the five-tier selective resolution policy; (3) a multi-axis empirical evaluation.

**D. Method.** Five-tier ladder (risk gate → router → deterministic resolver → constrained generation → relational verifier) over a typed 20-field fact store with provenance hashing and temporal validity, sourced from BARI/BRRI/DAE corpora.

**E–P. Experiment ledger by evidence class.** This is the central table of the audit.

| Class | Layers | What the script actually does |
|---|---|---|
| **REAL — genuine logic executed over cases** | **E02**, **E28** | Verifier and baseline verifiers implemented as real functions, run over an adversarial case file; outcomes computed, not assigned. E28 is the strongest layer in the project. |
| **REAL — deterministic component measurement** | E19, E23, E25, E26 (partial) | Small-scale but genuine measurements of graph traversal, hash-chain verification, classifier latency/size. Modest claims, honestly obtained. |
| **SIMULATION — Monte Carlo from assumed rates** | E04, E05, E06, E07/E08, E14, E15, E17, E18, E21, E22 | Cases generated, then outcomes **drawn** from hardcoded probabilities (`random.random() < 0.84`, `< 0.76`, `< 0.892` …). These are parameterised models of expected behaviour, not observations. E14's network profile is disclosed as simulation; the rest are not. |
| **CONSTANT TABLE — no computation at all** | **E03**, E09, E10, E11, E12, **E13**, E20, E24 | Results are numeric literals in the source. E03's entire slot-ablation ranking (dosage +31.6 pp, polarity +17.8 pp …) is a list of typed `hazard_count` values. The declared input dataset is never read. |
| **REAL BASELINES + UNMEASURED "OURS"** | **E27**, E29, E30, E31, E34 | Baselines are genuine live API calls with traces. The BAA/L4/L5 arm returns fixed verdicts or is handed the ground-truth answer key (E30 B6 builds its response string from `c['current_valid_active']`; E31 B6 from the known conflict). Zero traces for the proposed system. |
| **PROMPTED LLM MISLABELLED "BAA"** | E32, E33, E35, E36, E37, E38, E39 | Real API calls, but the "BAA" arm is Gemini-2.5-Flash-Lite with an advisory system prompt. Outcomes scored by `basic_classify()` — CUAR = "the string contains a banned chemical name". |
| **NEVER RUN (honestly labelled)** | E16, E40 | Hardware/battery profiling. Stub runners only. Correctly reported as pending. |

**Q. Artifacts that exist but are not in the manuscript.** `run_all_remaining.py` (the actual runner for E32–E39; the per-layer `scripts/run_eXX.py` files are 29-line skeletons that print "execution pending"), `E38/traces_fixed.jsonl` (the post-hoc corrected run), and `E27/traces.jsonl` (an earlier 3-case-per-baseline pilot with a different baseline set B0–B4).

**Additional structural findings:**
- **No evaluation dataset is present in this folder.** Every script points at `WORKSPACE_ROOT/research_artifacts/datasets/...`, outside the connected directory. The misbinding attack suite, the 3,000-query farmer benchmark and the risk–coverage corpus could not be examined. Their existence and construction are unverified here.
- **Manuscript §11–§13 do not exist**; `manifest.yaml` still lists 18 sections. The driver correctly includes 15. Harmless but fix the manifest.
- **E02's own script prints a `scientific_conclusion` string stating 34.8% lexical dangerous acceptance**, while the same script's computed output is 80.0% (which is what the paper uses). A stale hardcoded narrative contradicting the computed number in the same file.

---

## PART 3 — CLAIM INVENTORY

Centrality: **C** = central (the paper fails without it), **S** = supporting, **P** = peripheral.
Evidence strength: **Strong / Moderate / Weak / None**.

| ID | Claim | Where | Cen. | Current evidence | Strength | Broader than evidence? |
|---|---|---|---|---|---|---|
| **CL-1** | Single-record 11-slot joint binding rejects 100% of relational misbinding attacks | Abstract, §8.1, §8.2 | **C** | E02 (10,000 cases) + E28 (11,000 mutations, 7 systems) — both genuinely computed | **Strong** | Only in the word "guarantee"; the measurement is sound |
| **CL-2** | Each contract slot is individually load-bearing; dosage +31.6 pp, polarity +17.8 pp | §7.4, §8.7, Fig. 5 | **C** | E03 — **hardcoded constant table** | **None** | Entirely. No ablation was run. |
| **CL-3** | 97.0% certified advisory correctness, 0.0% CUAR on live end-to-end benchmark | **Abstract**, §7.1, Tab. 5 | **C** | E27 B6 — **verdict assigned, no traces** | **None** | Entirely |
| **CL-4** | Three agronomists rated BAA 4.82/5, 100% safety pass, AC1 = 0.862 | **Abstract**, §7.2, §6.5 | **C** | E13 — **literals; no study data** | **None** | Entirely; also an ethics gap |
| **CL-5** | 84.56% coverage at 1.26% selective risk; AURC 0.0153 | Abstract, §9.1 | **C** | E04 — Monte Carlo with `is_safe = random.random() < 0.85` | **Weak** | Yes — this is a simulated calibration curve |
| **CL-6** | 0.0% parametric intrusion vs 8–30% for RAG under evidence conflict | §8.4 | S | E29 — baselines real for **first 5 cases per mode only**; "ours" hardcoded `True, False, False` | **Weak** | Yes (already partly conceded in §16) |
| **CL-7** | 100% current-gazette adherence under temporal conflict | §8.5, §9.7 | S | E30 — baselines real (100 cases, traces present); B6 response string built from the answer key | **Weak (baselines only)** | Yes, for the BAA row |
| **CL-8** | 100% clarification on cross-modal conflict; 0% wrong chemical | §8.6 | S | E31 — same pattern as E30 | **Weak (baselines only)** | Yes, for the BAA row |
| **CL-9** | 0.0% injection survivability across 1,400 attacks | §10.4 | S | E07/E08 — outcomes drawn from `random.random() < 0.84 / 0.68 / 0.22 / 0.92` | **None** | Entirely |
| **CL-10** | 61.5% zero-LLM resolution, 2.28× latency, 89.7% cost reduction | Abstract, §10.1–10.3 | S | E18/E09/E20 — traffic mix and per-stage latencies are assumed parameters | **Weak (model)** | Yes — presented as measurement, is a model |
| **CL-11** | Deterministic SMS preserves 100% of safety slots vs 64.4% LLM hazard | Abstract, §10.5 | S | E15 — deterministic template side is genuinely checkable; LLM side is drawn | **Moderate/Weak** | Partly |
| **CL-12** | Detection gating lifts dialect Hit@1 +36.6 pp, coverage 42.9→89.8% | §9.5 | S | E17/E21 — Monte Carlo from per-register constants | **Weak** | Yes |
| **CL-13** | Offline cache sustains 91.4% / 58.1% delivery under 15% / 30% loss | §10.6, §15.1 | S | E14 — simulated network, **disclosed as such** | **Moderate (honest model)** | No — correctly framed |
| **CL-14** | 100% tamper detection, 92.8% bandwidth reduction | §5.3, §9.7 | S | E23 — genuine hash-chain computation | **Moderate/Strong** | No |
| **CL-15** | Deterministic graph traversal: 100% slot completeness, 0.0195 ms p95 | §4.4 | P | E19 — real, 23-node graph, **already caveated** as proof of mechanism | **Moderate** | No |
| **CL-16** | 18 minutes closes a coverage gap; +5.5 pp system coverage | §5.5, §15.4 | P | E24 — constant table, single case study | **Weak** | Yes |
| **CL-17** | Intent router: 78.4% joint EM, 0.3855 ms, 1.25 MB | §4.3, §9.2 | P | E25 — genuine measurement | **Moderate/Strong** | No |
| **CL-18** | Misbinding is "mathematically impossible" by construction | §4.6, §8.1 | **C** | Logical claim, conditional on correct extraction and a complete fact base | **Speculative as worded** | Yes — reviewer §18 is right |

**Speculative / not evidenced anywhere:** generalisation to veterinary or human-health domains (§14.5 — already flagged as a design argument); national-scale deployment feasibility (§14.4 hypothetical); field efficacy, yield or adoption outcomes (correctly disclaimed).

---

## PART 4 — CLAIM → EVIDENCE MATRIX

| Claim | Evidence direct? | Sufficient for scope? | Redundant? | Meaningful gap? | Gap necessary to close? | Could narrowing fix it instead? |
|---|---|---|---|---|---|---|
| CL-1 | Direct | **Yes** | E02 and E28 overlap ~70%; E05 overlaps both | No | — | Reword "impossible" → "structurally rejected under the stated conditions" |
| CL-2 | None | No | — | Yes: the ablation itself | **Yes — MUST HAVE.** It is cheap: E03 needs only E02's harness with slots disabled | No. This is the paper's mechanistic argument. |
| CL-3 | None | No | E13 and E27 both claim end-to-end validity | Yes: the whole benchmark | **Yes** — but see Part 6 for the cheaper merged design | No |
| CL-4 | None | No | — | Yes: the study | **Yes if the claim stays.** Otherwise delete the claim entirely (see Part 9) | **Yes** — the claim can be removed rather than manufactured |
| CL-5 | Indirect (simulated) | No | — | Yes: real confidence scores on real outputs | Only if selective risk stays a headline | **Yes** — demote from abstract to a design-analysis subsection |
| CL-6/7/8 | Baselines direct; BAA arm none | Baseline half is publishable alone | E30 duplicated verbatim in §8.5 and §9.7 | Yes: run BAA on the same cases | High value, not blocking — the baseline finding stands on its own | **Yes** — reframe as "how existing systems fail", which is what was actually measured |
| CL-9 | None | No | E22 duplicates E07/E08 for SMS | Yes | Moderate — Tier-0 interception is deterministically checkable at low cost | Partly: narrow to "the Tier-0 gate intercepts N of 1,400 payloads", which is measurable |
| CL-10 | Indirect (model) | As a model, yes | E09/E18/E20 are three views of one model | No new experiment needed | No | **Yes** — relabel as an analytical model throughout. Reviewer §63–65 says the same. |
| CL-11 | Half direct | Nearly | E15/E22 overlap | Small: real LLM SMS composition | Cheap and worth doing (one API loop) | Partly |
| CL-12 | Indirect | No | E06/E17/E21 are three views of one register model | Yes: real retrieval Hit@1 by register | **High value.** Retrieval is measurable without the full system. | No — this is a load-bearing motivation for the whole design |
| CL-13/14/15/17 | Direct | Yes | No | No | No | No — these are fine as they stand |

**Key structural observation:** the redundancy is severe. E02/E05/E28 measure one property three times; E09/E18/E20 model one economy three times; E06/E17/E21 model one register story three times; E30 appears twice in the manuscript. Roughly **12 of 36 layers are duplicate views of 4 underlying results.**

---

## PART 5 — OUT-OF-SCOPE MATERIAL

| Item | Classification | Reasoning |
|---|---|---|
| E20 telecom economics (BDT/query, national cost) | **REMOVE** | Invents an economics evaluation dimension CEA reviewers cannot assess; invites demands for real tariff data and traffic modelling. Supports no central claim. |
| E16 + E40 hardware/battery profiling | **REMOVE from the paper** | Never run. Correctly pending — so do not list them in a 38-layer battery. |
| E24 knowledge growth loop | **MOVE TO SUPPLEMENTARY** | Single-case, constant-derived. Interesting deployment colour, no claim depends on it. |
| E19 graph traversal (23 nodes) | **KEEP BUT CONDENSE** to one sentence | Real but tiny; already caveated. Currently reads as a scalability claim in §4.4. |
| E25 intent router | **KEEP BUT CONDENSE** | Real, but an engineering detail, not a contribution (reviewer §56 agrees). |
| E32, E33, E35, E36, E37, E39 | **REMOVE ENTIRELY** | The "BAA" arm in each is a prompted Gemini instance. They do not test the architecture. E32/E33's non-zero CUAR is currently explained in §8 as a deliberate predicate bypass — that explanation is not supported by the code and must not be published. |
| E38 escalation queue | **REMOVE** | n=30, model-confounded, post-hoc classifier fix, and the BAA arm is a prompted LLM. §15.3 cites it. |
| E29 parametric conflict | **KEEP BUT REFRAME** as a baseline-only finding | The LLM-leakage result (30–56% direct, 8–30% RAG) is real for the sampled cases and is genuinely interesting. The BAA row is not. |
| E14 network simulation | **KEEP** | Honestly framed as simulation. |
| §14.4 national-scale 37,000-hazard hypothetical | **REMOVE** | Extrapolates a CI upper bound from a benchmark that was not run. Reviewer §67 independently flags it. |
| Vision/multimodal framing (E31) | **TOUCH LIGHTLY** | Classification-only, already disclaimed. Do not foreground it. |
| SMS / offline / channel material (E15, E22, E23, E14) | **KEEP, CONDENSE INTO ONE SECTION** | Genuinely CEA-relevant deployment content, currently spread across four places. |
| "≈60,000 evaluation cases" and "36 layers" | **REMOVE both figures** | They aggregate simulated draws and constant tables into an impressive-sounding total. This is the most attackable sentence in the paper even before provenance is considered. |

**Removing all of the above costs you nothing central.** It removes roughly a third of the manuscript's surface area and most of its reviewer-expectation liabilities.

---

## PART 6 — MISSING EVIDENCE (strict standard)

Ten proposed experiments, tested against your criteria. I have deliberately kept the MUST HAVE list to three.

### MUST HAVE

**M1 — Re-run E03 (slot ablation) for real.**
- Claim: CL-2, central. Mechanism argument of the entire paper.
- Reviewer concern: material — a hardcoded ablation is the difference between a mechanism and an assertion.
- Cost: **low.** E02's harness already exists and works. Disable one slot at a time in `evaluate_typed_relational_verifier` and re-run over the same 10,000 cases. Hours, not weeks.
- Local status: **Category C** (exists but needs rerunning — the harness exists, the result does not).

**M2 — One controlled end-to-end benchmark with the real system, replacing E27, E13's role, E34 and E29's BAA row.**
- Claim: CL-3, central; also substitutes for CL-6/7/8's BAA arms.
- Design: same frozen generator, same retrieval corpus, same prompts, same queries. Arms: A0 direct LLM, A1 vanilla RAG, A2 RAG + judge, A3 evidence-constrained RAG (no single-record binding), A4 BAA. n = 300–500 stratified (naturalistic × 4 registers, adversarial, ambiguous, dialect). Metrics: CUAR, CAC over certified set, coverage, appropriate abstention, **false abstention**, per-slot violation.
- This is reviewer §16 and §140 — but note I am recommending **n = 300–500, not 1,000**. The reviewer's 500–1,000 assumes your existing evidence is real and needs scaling. It is not, so the priority is *one measurement that exists* rather than a large one.
- **This is only feasible if a runnable KrishokChat system exists.** If it does not, this experiment is not "missing" — the paper's central claim is not yet supportable, and the correct action is to narrow the paper to CL-1 (see Part 9).
- Local status: **Category D or E** — cannot determine from this folder.

**M3 — Ethics documentation and raw rating data for E13, or removal of E13.**
- Claim: CL-4, central and in the abstract.
- Not an experiment: a records question. If the study happened, produce the rating sheets, the rater consent, and the IRB/institutional approval, and add an ethics statement. If it did not, **delete every reference to it** — abstract, §6.5, §7.2, §14, conclusion.
- Local status: **Category F/E.**

### HIGH VALUE

**M4 — Real retrieval Hit@1 by Bengali register (replaces the simulated E06/E17/E21 core).** Retrieval can be measured without the full advisory system: index the corpus, run the register-varied queries, count Hit@1. This underwrites CL-12, which is the paper's *motivation* for detection gating. Cheap, self-contained, high credibility return.

**M5 — Real Tier-0 interception count on the 1,400 injection payloads (replaces the drawn E07/E08).** The deterministic gate is a regex/keyword screen; running it over the payload file is minutes of work and yields an honest number, whatever it is.

**M6 — Benign-mutation control for E28.** Reviewer §123. Currently every mutation is harmful, so 100% rejection is unfalsifiable. Add mutations that are *semantically harmless* (paraphrase, unit-equivalent restatement, formatting) and report false-rejection rate alongside. This converts the strongest layer from "rejects everything bad" into "discriminates". Low cost, high credibility, and it makes E28 the paper's centrepiece with confidence.

### USEFUL BUT OPTIONAL

**M7 — Adversarial numerical paraphrase set** (reviewer §97): "two grams per litre", "20 g / 10 L", "0.2%", Bengali numerals. Tests unit-equivalence handling. Good, but it extends E28 rather than establishing anything new.
**M8 — Certification invariance across paraphrases of the same record** (reviewer §96). Elegant, cheap, but supports a claim you can also make analytically.
**M9 — False-abstention / over-refusal accounting** (reviewer §98). Should be *reported* from M2 rather than run separately. Counts as analysis, not an experiment.

### LOW VALUE / OUT OF SCOPE / NOT JUSTIFIED

| Proposal | Verdict | Why |
|---|---|---|
| Reviewer §94 provenance-removal isolation | **LOW VALUE** | E28's provenance-hash operator already isolates it once E28 is trustworthy. |
| Reviewer §95 authority-hierarchy conflict | **LOW VALUE** | E30's baseline half already demonstrates this; add the BAA arm inside M2 rather than as a new layer. |
| Reviewer §142 model-invariance across generators | **OUT OF SCOPE** | The certification predicate is generator-independent by construction; measuring it across 5 models buys a table, not an insight, and adds 5 new baseline expectations. |
| Reviewer §143 full Pareto frontier sweep | **OUT OF SCOPE for this paper** | Attractive, but it is a second paper. One frozen θ* with a sensitivity note suffices. |
| E16/E40 hardware and battery profiling | **NOT JUSTIFIED** | No central claim depends on device power draw. |
| Expanding E27 to n = 1,000 | **NOT JUSTIFIED at this stage** | Scaling an unmeasured benchmark is the wrong order of operations. Measure at 300 first. |
| Field trial / yield outcomes | **OUT OF SCOPE** | Correctly excluded already; do not let §18's "future work" sentence invite it. |

---

## PART 7 — LOCAL DIRECTORY STATUS

| Category | Layers |
|---|---|
| **A. Exists and answers the question** | E02, E28 (with M6 caveat), E23, E25, E19, E14 (as declared simulation) |
| **B. Partially exists, needs re-analysis not re-running** | E09/E18/E20 — relabel as analytical model and report as one economics subsection; E10 — usable as a *taxonomy* if the 100 cases were genuinely audited by a human, which the script does not show |
| **C. Exists but needs re-running** | **E03** (harness exists, result fabricated), E04, E05, E06, E07/E08, E12, E17, E21, E22, E24 — all have runnable structure but simulated or constant outcomes |
| **D. Code exists, experiment never run** | E16, E40 (honestly labelled); E32–E39 per-layer runners are stubs (the real runner is `run_all_remaining.py`) |
| **E. No evidence exists; genuinely new work required** | **E13** (human study), **E27/E34 BAA arms**, E29/E30/E31 BAA arms |
| **F. Cannot determine from this folder** | All evaluation datasets (`research_artifacts/` not connected); whether a runnable KrishokChat system exists at `d:\KrishokChat Advisory System`; whether E13 rating sheets exist offline |

---

## PART 8 — FINAL AUDIT

### 1. Core claims
CL-1 (single-record binding defeats misbinding) · CL-2 (per-slot contribution) · CL-3 (end-to-end certified correctness) · CL-4 (expert validation) · CL-5 (calibrated selective risk). CL-18 (the formal impossibility claim) is central as *framing*.

### 2. Current sufficient evidence — **HIGH CONFIDENCE**
Only **CL-1**, via E02 and E28. It is a real, large, well-constructed adversarial evaluation with a genuine isolation baseline (B5 vs B6 on exactly the four missing slots). **This is a publishable result on its own.** Supporting and adequate: E23 (tamper detection), E25 (router), E19 (traversal, as caveated), E14 (network, as declared simulation).

### 3. Evidence gaps — **HIGH CONFIDENCE**
CL-2, CL-3, CL-4, CL-9 have **no** supporting evidence. CL-5, CL-6, CL-7, CL-8, CL-10, CL-12, CL-16 rest on simulation or assigned outcomes and cannot be described as measurements.

### 4. Unnecessary / risky experiments — **HIGH CONFIDENCE**
E32, E33, E35, E36, E37, E38, E39 (prompted LLM labelled BAA — actively dangerous to publish); E20, E16, E40; the §14.4 national-scale hypothetical.

### 5. Possible out-of-scope material — **HIGH CONFIDENCE**
Telecom economics, hardware profiling, IPM balance, escalation queueing, conversational clarification policy, linguistic normalisation. Also the "36 layers / ~60,000 cases" framing itself.

### 6. Experiments already available locally — **HIGH CONFIDENCE**
E02, E28, E23, E25, E19, E14. These plus the *baseline halves* of E27, E29, E30, E31, E34 (which are real, traced, and independently interesting as a "how current systems fail" contribution).

### 7. Experiments that may need to be run — **MEDIUM–HIGH CONFIDENCE**
M1 (real slot ablation) — MUST, low cost. M2 (one controlled end-to-end benchmark) — MUST, conditional on a runnable system. M3 (E13 records or deletion) — MUST, not an experiment. M4 (real register Hit@1), M5 (real Tier-0 interception), M6 (benign-mutation control) — HIGH VALUE, each low cost.
**That is three must-haves and three high-value additions — against a project that currently claims 36 layers.**

### 8. Experiments that should NOT be added — **HIGH CONFIDENCE**
Model-invariance sweeps, full Pareto sweeps, provenance-removal isolation, authority-hierarchy as a separate layer, n=1,000 scaling, field trials, hardware profiling. Adding any of these before Part 6's must-haves would expand scope while the foundation is missing.

### 9. Claims to narrow rather than evidence — **HIGH CONFIDENCE**
- CL-18: "mathematically impossible" → "structurally rejected by the certification predicate whenever the contract fields are correctly extracted and the authority record is valid." (Reviewer §18/§119 concur.)
- CL-10: relabel the entire economics/latency story as an **analytical model** with stated parameters. It is defensible as a model; it is indefensible as measurement. No experiment needed.
- CL-5: move selective-risk calibration out of the abstract into a design-analysis subsection until real confidence scores exist.
- CL-6/7/8: reframe E29/E30/E31 as **baseline failure characterisations** — "unconstrained and RAG systems leak obsolete gazette entries in 39–75% of cases" is a real, measured, genuinely useful CEA finding that needs no BAA arm.
- CL-12: state register-dependent retrieval degradation as motivating design analysis until M4 measures it.
- Remove "≈60,000 cases" and "36 layers" in favour of naming the two or three suites that are real.
- Delete §14.4's national-scale extrapolation.
- §17 Data Availability: it currently promises the scripts. Do not submit that sentence until the scripts say what the paper says.

### 10. Questions that require your decision

1. **Did the E13 agronomist study actually take place?** If yes: produce raw ratings, consent records and ethics approval, and add the ethics statement CEA requires. If no: every reference to it must be deleted before this manuscript goes anywhere. *Nothing else in this audit matters until you answer this.*
2. **Does a runnable KrishokChat system exist at `d:\KrishokChat Advisory System`?** If yes, M1/M2/M4/M5 are weeks of work and the paper is recoverable at close to its current ambition. If no, the honest paper is a narrower one built on E02 + E28 + the real baseline halves — which is still a good CEA paper, and which I would rather see submitted than the current draft.
3. **Was your co-author aware of how these layers were produced?** The manuscript carries a supervisor's name. That is their exposure too, and they should know before submission, not after.
4. **Do the evaluation datasets in `research_artifacts/` exist and how were they constructed?** They could not be inspected here. Reviewer §121 will ask how adversarial cases were generated and validated; you need that answer regardless.
5. **Is there a prior or companion paper** (the acknowledgments mention a 1,001-query benchmark and an EACL systems paper) **that already published any of these numbers?** If a fabricated figure has already appeared elsewhere, that is a correction obligation, not a revision.

---

## IF THE MANUSCRIPT WERE ALREADY SUFFICIENT

It is not, and I want to be explicit rather than diplomatic about that. But the inverse also deserves saying plainly: **the underlying idea is good, and one part of the evidence is genuinely strong.** E02 and E28 together — 21,000 adversarial cases, seven verification systems, a clean B5-vs-B6 isolation showing the safety gain lands on exactly the four missing slots — is a real contribution, honestly obtained, and well matched to CEA. With M1 and M6 added, and the paper narrowed to what that evidence supports, you have a defensible submission.

The fastest credible path is not more experiments. It is: answer question 1, then delete about a third of the paper, then run three small things.

---

## Recommended sequence

| # | Action | Confidence | Cost |
|---|---|---|---|
| 0 | Answer Part 8 Q1 and Q2. Do not submit anything until Q1 is resolved. | HIGH | — |
| 1 | Remove E32–E39, E20, E16, E40 from the manuscript and the battery count. | HIGH | Hours |
| 2 | Reframe E29/E30/E31 as measured baseline-failure findings; drop their BAA rows. | HIGH | Hours |
| 3 | Relabel all economics/latency material as an analytical model (CL-10). | HIGH | Hours |
| 4 | Run M1 (real slot ablation) and M6 (benign-mutation control) on the existing E02/E28 harness. | HIGH | Days |
| 5 | Run M4 (real register Hit@1) and M5 (real Tier-0 interception). | MEDIUM-HIGH | Days |
| 6 | Run M2 (one controlled end-to-end benchmark) **if** a real system exists. | MEDIUM | Weeks |
| 7 | Resolve E13: document or delete. Add ethics statement if retained. | HIGH | Depends on Q1 |
| 8 | Rewrite abstract and conclusion from what survives. Apply the narrowing list in item 9. | HIGH | Days |
| 9 | Only then work through reviewer_1's presentation and framing items (§7–§9, §35–§39, §101–§113) — most are good and remain valid. | HIGH | Days |

