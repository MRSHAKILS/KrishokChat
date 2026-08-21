# 5. Experiments

> **Status:** DRAFT v1 (2026-08-22) â€” evaluation protocol only; contains no experimental results or outcome language. Written under `CLAIM_LEDGER_FREEZE.md` (trace map at end of file); no external citations per brief.

We evaluate the methods of Section 4 under three commitments. First, design precedes access: every experiment below was specified, with its identifier and priority frozen, before any test data was touched. Second, wherever automatic scores are insufficient, expert and native-speaker human judgment supplies the verdict. Third, reproducibility is manifest-governed: every run records its inputs, code, configuration, and outputs by hash, so any reported number traces back to artifacts. Freezing also fixed how results may be read, because the interpretation limits closing this section were agreed before outcomes existed. Nine experiments instantiate hypotheses H1â€“H5 under these rules.

## 5.1 Benchmark and annotation protocol

**Annotation protocol v1.** All labeling follows annotation protocol v1. Two annotators work independently on every item, and a lead adjudicator resolves their disagreements under a versioned manual. Adjudication appends its decision to the lineage rather than erasing the disagreement. Labeling proceeds to full scale only after a pilot clears an agreement gate of Krippendorff's Î± â‰¥ 0.70. Raw labels are retained permanently, each carrying its annotator identifier, guideline version, timestamp, and adjudication lineage. Consensus labels support analysis, but consensus never replaces the raw layer as the record of what was actually marked.

**Pilot calibration.** A pilot of 24 development-only items calibrates the manual before the main labeling effort begins. Pilot items come from the development side only. If pilot agreement falls short of the gate, we revise the manual and rerun the pilot. The rerun is mandatory; the protocol does not allow skipping it to protect a schedule.

**Grouped splits.** We assign items to grouped train, development, and test splits in a 60/20/20 proportion using split seed 20260813. The grouping key combines source, intent, and transformation lineage, which keeps every regional, romanized, adversarial, and normalized form of one intent inside a single split. Counterpart variants therefore share a split, so the paired comparisons of Section 5.2 stay well defined. We report a leakage check alongside the published splits, and the split manifests record artifact hashes. A dry-run reproduction must succeed before the splits freeze.

**Reproduced baselines.** Comparison anchors are reproduced rather than repaired. The deployed lexical dosage matcher runs offline at its captured revision, with fixture parity against recorded behavior and no silent fixes applied. The structured candidate enters comparisons only after passing its fail-closed suite of 26 tests. A quietly improved baseline would inflate apparent gains, so fixture parity is a precondition of comparison rather than a courtesy.

**Composition reporting.** Dataset counts enter this paper exclusively through artifact manifests. Each qualifying manifest states the file path, the counting method, and the content hash, so an independent reader can recompute every published figure. Historical totals derived from PDFs stay excluded until reconciliation at assembly time. Until reconciliation completes, the dataset-composition table reserves a placeholder slot where the verified totals will appear.

## 5.2 Experiment matrix

On this shared foundation, we prespecify nine experiments: four essential, three strong-supporting, and two optional. Questions and priorities were frozen together. Essential rows carry the confirmatory weight; omitting one would break the paper's argument. Strong-supporting rows explain why effects arise, how they vary across subgroups, or whether system integrity holds. Optional rows extend coverage when resources allow. Every row fixes its primary metric and test in advance, so post hoc metric selection is out of contract.

**Prespecified experiment matrix (questions and priorities frozen before test access; table numbering assigned at assembly).**

| ID | Priority | Question | Baselines and comparators | Primary metric and analysis |
|---|---|---|---|---|
| E1 | ESSENTIAL | Does relation-aware verification catch what the lexical baseline misses? | Lexical baseline; fixed LLM judge included only as a clearly labeled secondary comparator | Dangerous non-abstention rate among safety-critical unsupported or contradicted claims; paired McNemar with bootstrap confidence interval |
| E2 | ESSENTIAL | What riskâ€“coverage tradeoff does calibrated abstention expose? | Uncalibrated structured decision; always-certify and always-abstain bounds | Selective risk at the frozen coverage target; stratified paired bootstrap for selective risk and area under the riskâ€“coverage curve (AURC) |
| E3 | STRONG | Which schema fields drive the safety gains? | Full ClaimSafe-BN schema versus field-removal ablations removing denominator, interval, PHI, applicability, polarity, or source-conflict | Change in dangerous non-abstention per removal; paired McNemar with Holm correction |
| E4 | ESSENTIAL | Does reviewed-dictionary dialect normalization improve retrieval without safety cost? | Raw input; Unicode-only ladder step; reviewed dictionary (learned normalizer admitted only through the gated E9 route) | Recall@10 subject to non-inferiority on harmful-to-benign safety flips; paired bootstrap plus exact flip tests |
| E5 | ESSENTIAL | Does the verification benefit survive dialect normalization? (verifier Ã— normalization factorial) | Factorial cells lexical/raw, lexical/dictionary, structured/raw, structured/dictionary, paired by intent | Interaction contrast on dangerous non-abstention; paired clustered bootstrap |
| E6 | STRONG | Is behavior uneven across standard, regional, and romanized varieties? | Paired comparison cells frozen before testing | Worst-group dangerous non-abstention and false-safe rate; stratified bootstrap; descriptive treatment below the sample gate |
| E7 | STRONG | Does the vision fallback stay evidence-safe end to end? | Repaired source-linked path versus captured defective fixture | Count of source-empty verified outcomes required to equal zero; exact assertion suite |
| E8 | OPTIONAL | Does bounded NLI resolution earn its latency? | Deterministic matcher with and without NLI tie-breaking on ambiguous relations | Macro-F1 on ambiguous and partially supported relations within the latency budget; paired analyses |
| E9 | OPTIONAL | Would a learned normalizer beat the reviewed dictionary? | Reviewed dictionary baseline; learned candidate admitted only after passing its development gate | Recall@10 improvement subject to all safety and slot gates |

E1, E2, E4, and E5 carry the thesis. They ask whether relation-aware verification catches what the lexical baseline misses, whether selective certification exposes a defensible riskâ€“coverage tradeoff, and whether dialect normalization improves retrieval without safety cost, alone and in factorial combination. E3 supplies the mechanism behind those effects, E6 reports subgroup behavior honestly across varieties, and E7 certifies end-to-end integrity of the deployed pipeline. E8 and E9 are exploratory extensions, and either may be omitted without weakening the confirmatory contract.

## 5.3 Human evaluation

Automatic metrics cannot certify everything the system promises, so human judgment enters at three layers. Gold labels make automatic scoring auditable, expert review covers integration failures, and native review protects linguistic validity.

**Expert gold labels.** Expert annotators build the gold reference set under the same two-annotator-plus-adjudicator protocol as Section 5.1. Agreement is reported separately at span, field, and relation level, alongside the adjudication rate. These reference labels anchor every automatic score used elsewhere in the evaluation.

**Blinded end-to-end review.** A second layer applies blinded expert review to integrated system outputs rather than isolated components. Reviewers record both error directions: dangerous pass-through, where an unsupported unsafe claim reaches the user, and false abstention, where a safe query is refused. Pass-through and false abstention carry asymmetric risks, so neither is collapsed into the other.

**Native dialect review.** Native speakers of the affected varieties review every normalization mapping and every paired variant. For each item they judge authenticity and decide whether source and normalized queries remain intent-equivalent. Rejection rates and missingness are reported alongside the judgments themselves.

**Scope.** No farmer study appears in this paper. Claims about farmer-facing outcomes would require their own protocol, institutional review, and publication. This paper therefore makes no usability, trust, or adoption claims.

## 5.4 Statistics and reproducibility

Inference proceeds at Î± = 0.05 throughout. Multiplicity control follows each experiment's prespecified plan, with Holm correction applied wherever multiple comparisons accumulate. Wherever the design permits pairing, we pair observations, since paired analyses remove between-item variance that unpaired tests would mistake for signal. Resampling respects clustering by intent and source. Seeds, split-lineage checks, and near-duplicate reporting apply to every analysis, and judgments collected in Section 5.3 follow these same rules.

Every run emits a manifest recording input and output hashes, split identifiers, the code revision with a dirty-tree flag, configuration, model and provider versions, prompt hashes where applicable, hardware, and failures encountered during execution. Manifests turn Section 6 into an audit trail, because every primary claim there will cite the run identifier that produced it. A pinned golden replay regression runs offline in continuous integration as an engineering invariant, separate from the scientific experiments. Numbers without manifests do not exist in this paper.

**Interpretation limits (STOP conditions).** Interpretation was constrained in advance, not negotiated afterward. Four STOP conditions bind every claim in Section 6 regardless of how the numbers fall.

1. If E1 shows no reduction in dangerous non-abstention, no superiority claim appears anywhere in this paper.
2. If calibration thresholds move after test access, all selective-certification claims are withdrawn.
3. Below the frozen minimum cell size, subgroup analyses remain descriptive only.
4. A learned normalizer never defines the normalization contribution; the reviewed dictionary holds that role regardless of E9's outcome.

Section 6 presents results only for runs that satisfy these constraints, and every result arrives attached to a run identifier.

---

*End of draft v1.*

<!--
Trace map (Â§5 sources; see paper/manuscript/CLAIM_LEDGER_FREEZE.md):
- 5.1 annotation protocol: T07 (protocol v1), T08 (pilot, 24 dev-only items)
- 5.1 grouped splits: T09 (seed 20260813, leakage check, split manifests + artifact hashes, dry-run reproduction)
- 5.1 baseline reproduction: T12 (captured lexical matcher offline, fixture parity), T15 (structured candidate, fail-closed suite of 26 tests)
- 5.2 experiment matrix and statistics: 05_MINIMUM_EXPERIMENT_MATRIX.md + 07_ABSTENTION_AND_DIALECT_PROTOCOL.md
- 5.3 human evaluation: T10 (gold labels), T23 (blinded end-to-end review), T11 + T13 (native dialect review)
- STOP conditions: 03_THESIS_DECISION.md
-->
