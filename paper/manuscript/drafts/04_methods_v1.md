# 4. Methods

> **Status:** DRAFT v1 (2026-08-22) — methods specification only; contains no experimental results or outcome language. Written under `CLAIM_LEDGER_FREEZE.md` (trace map at end of file); no external citations per brief. The arXiv v1 identifier banned by `docs/PAPER_POLICY.md` appears nowhere.

Section 3 closed by promising four specifications: the claim schema, the structured candidate that performs relation-aware verification, the calibration step behind selective certification, and the paired protocol under which dialect normalization becomes a measured axis rather than silent preprocessing. This section delivers all four. Every endpoint, threshold rule, parser, dictionary, and hypothesis specified below was frozen before test access. It states design decisions and freeze rules only; no experimental outcome appears here.

## 4.1 Safety router and deterministic pre-check

Section 3 described the deployed router, so we record here only the properties that evaluation relies on. The six-category taxonomy stands unchanged. Deterministic keyword and rule families, including the corpus-coverage gate, precede structured LLM classification on every request. When classifier output cannot be parsed or its provider fails, the query maps to `low_confidence`; the stage thus fails closed under infrastructure faults. Retrieval starts only after a `safe_agri` decision, and each routing decision appends one audit record. Multi-turn context handling and adversarial red-teaming remain engineering lanes outside this paper's claims.

## 4.2 Retrieval

The adjudicated runtime retrieves with BM25 over the precomputed index, whose file is pinned by hash. Cache keys carry the corpus-generation tag, so answers computed against an older corpus cannot re-enter after a rebuild. No live web scraping or index construction occurs at request time. Retrieval failures degrade to empty result sets plus a controlled referral.

Production also offers hybrid reciprocal-rank fusion of BM25 and dense rankings as its default path. Because fused score magnitudes cannot gate abstention (Section 3), the confirmatory evaluation fixes BM25-only operation as the thesis runtime. A prespecified ablation compares BM25, dense, and hybrid retrieval at k = 5 under otherwise identical downstream components.

## 4.3 Verifier: ClaimSafe-BN schema and structured matcher

The schema, named ClaimSafe-BN, anchors this subsection; the paragraphs that follow specify its fields, its missing-value conventions, its relation labels, its safety-criticality criterion, the extractor that populates it, and the decision procedure that consumes it.

A claim instance records `claim_id`; crop; disease/pest; action; chemical/intervention; formulation; amount; unit; denominator; interval/frequency; PHI/safety condition; `source_id`; an evidence span; polarity; an applicability predicate; uncertainty; relation; and a `safety_critical` flag. Each evidence span stores character offsets, the span text itself, and the hash of the cited source, identified by stable `source_id` rather than by list position. Polarity takes exactly one of four values: affirmed, negated, conditional, or prohibited.

We state the missing-value rule exactly, because annotation and parsing both depend on it. Null denotes true absence or non-applicability; unknown denotes a value present in the source but unresolved during extraction. Neither state is ever encoded as zero or as an empty string. Original and normalized text are preserved side by side, and Bengali numerals convert to ASCII digits for comparison only.

Relation-aware verification assigns each claim one label from a frozen enum: `supported`, `contradicted`, `partially_supported`, `unsupported`, `ambiguous`, or `not_applicable`. Matching runs against every candidate span attached to the answer, never against a single best match. When authoritative spans conflict on a material field, such as amount, formulation, or interval, the verdict is `ambiguous` and the answer abstains.

An error is safety-critical if it could change chemical identity, banned status, formulation, dose, denominator, or mixture arithmetic. The same holds for errors touching interval or PHI guidance, protective-equipment, weather, water, livestock, or human-exposure instructions, applicability, polarity, or the poisoning-response path. A safety-critical claim certifies only when its relation is `supported` and every required field is resolved.

Schema population is fully deterministic. A parser recognizes Bengali and English numeral patterns, units, denominators, interval expressions, PHI phrases, polarity markers, and applicability structures. The parser runs offline alongside a normalizer and a relation matcher, and together these modules form the structured candidate that Section 5 evaluates against the deployed matcher. That deployed matcher remains untouched in the serving path and serves as the lexical baseline.

Verdict assignment is deterministic-first under fail-closed gating. Hard gates force abstention whenever the `source_id` or evidence span is missing, a required field is unresolved, dimensions mismatch, a contradiction stands, or a source conflict remains unresolved. An optional natural-language-inference (NLI) component may act only as a bounded secondary resolver for relations left ambiguous after deterministic matching; it can never override a hard gate. An LLM judge likewise never supplies gold labels; expert annotators do. Per-claim verdicts aggregate into an answer-level action: `certify`, `abstain`, `blocked`, or `out_of_scope`.

Three artifacts freeze this specification as versioned files: the machine-readable schema, a label manual operationalizing each relation, and a risk taxonomy defining safety criticality. The confirmatory evaluation consumes these pinned versions; later amendments require new version identifiers.

## 4.4 Selective certification

Selective certification turns per-claim verdicts into an answer-level decision to certify or withhold. The abstention score is built from explicit extraction and matching features; raw model probabilities alone never determine it. Only prespecified calibration families are compared, and only on development data. Where sample size permits, grouped cross-validation within the development set estimates each family's stability.

The threshold freezes through a constrained objective fixed in advance: either risk at a frozen coverage target, or minimum risk subject to a coverage floor. The cost ratio between error types enters this objective only after expert review fixes its value. We report coverage(t), the share of answers certified at threshold t, and selective risk(t), the number of dangerous certification errors divided by the number of certified answers. False abstentions and dangerous non-abstentions are reported separately rather than collapsed into one error rate. Area under the risk–coverage curve, expected calibration error, and Brier score act as secondary diagnostics.

Two administrative rules protect the policy. Any threshold, parser, dictionary, or prompt change informed by test access invalidates the confirmatory run outright. Per-stage latency is recorded at p50/p95, and a candidate exceeding the latency budget stays offline regardless of its accuracy.

## 4.5 Normalization: paired dialect protocol

Dialect normalization is evaluated on paired inputs. One `intent_id` links a standard-Bangla query to native-reviewed regional and romanized forms judged intent-equivalent to that query. All variants of one intent stay in the same split, grouped by source, intent, and transformation lineage, so no variant can leak across splits. Native review gates authenticity and equivalence before any variant enters the dataset.

Eleven slots freeze before any transformation runs: crop, target organism, chemical/intervention, formulation, amount, unit, denominator, interval/frequency, PHI/safety condition, polarity, and harmful intent. Together they define what a normalization condition must not silently alter.

Normalization climbs a fixed ladder of conditions. Raw input first passes Unicode grapheme normalization, then dictionary normalization, which adds reviewed lexical mappings on top of Unicode handling while risk-term protection guards safety-bearing strings. A learned normalizer may join only after clearing a development gate; nothing beyond the dictionary level enters confirmatory scope automatically.

Our threat model is explicit: normalization can itself corrupt negation, chemical identity, dosage slots, or harmful intent. Retrieval-only reporting is therefore insufficient, and retrieval benefit and safety preservation are measured jointly. The primary retrieval endpoint is Recall@10, evaluated subject to non-inferiority on harmful-to-benign safety flips. Verifier condition and normalization condition form a factorial pair whose interaction we analyze separately rather than fold into a main effect.

One derived resource requires exact framing. The reviewed dictionary evaluated here is a 16-pair map derived deterministically from the frozen reviewed splits, with no LLM anywhere in its construction loop. On the dialect population from which it was derived, the map raised expansion hit rate from 0.03% to 33.49%. We report those figures as characterizations of the map on its own derivation population and do not compare them with the benchmark-population figure in Section 3. Romanized Banglish input remains outside the dictionary's coverage.

Governance operates at the level of individual mappings. Every mapping records provenance, canonical form, target variety, reviewer, version, example contexts, a safety flag, and its allowed context of use. Mappings touching ambiguous or safety-bearing terms apply only under exact-context rules or do nothing at all. Unknown inputs pass through unchanged.

## 4.6 Vision routing with evidence grounding

Vision input passes two classification stages: a general crop classifier routes the image, and a crop-specific disease classifier labels the observed condition. Both models ship as ONNX exports, perform classification only, and emit no bounding boxes. Localization metrics stay out of scope until a verified detection artifact exists.

Treatment advice behind a vision route cannot bypass verification. Such text enters the shared QA pathway through a vision-advisory channel and must meet the same verifier or return an explicitly uncertified outcome. The repaired fallback adds one structural guarantee: source-empty treatment advice can never be marked verified, whatever the classifiers conclude.

## 4.7 Telemetry and audit

Each request extends the additive audit schema with per-stage timings, token counts, provider identifier, request id, cache-hit marker, safety category, retrieval-hit flag, and verifier verdicts. The `cost_estimate` field stays null because we claim no price table. Storage remains local-only under retention and redaction controls, and the system emits no external telemetry. Distributed-tracing export was considered and deferred; it contributes nothing to this paper's claims.

## Confirmatory hypotheses

Five hypotheses govern the evaluation, and all five are confirmatory. Their endpoints, multiplicity control, and minimum sample support froze before test access. Section 5 operationalizes them; each appears here in one sentence.

1. **H1.** Structured relation matching reduces dangerous non-abstention relative to the lexical baseline on expert-labeled safety-critical claims.
2. **H2.** Development-calibrated abstention lowers selective risk as coverage decreases and meets a frozen high-risk constraint on test.
3. **H3.** The full relation schema outperforms prespecified field-removal ablations for safety-critical certification.
4. **H4.** Reviewed dictionary normalization improves BM25 recall for paired dialect queries without increasing harmful-to-benign safety flips (non-inferiority).
5. **H5.** Relation-aware certification benefits from normalization only when normalization preserves safety-critical slots (factorial interaction).

One interpretation limit applies to everything that follows. Failure to reject a null does not establish equivalence unless a margin was specified and powered in advance. This study makes no farmer-outcome, agronomic-effectiveness, or deployment-causality hypothesis of any kind. Section 5 presents the experiment matrix that instantiates the methods specified here.

---

<!--
Trace map (paper/manuscript/CLAIM_LEDGER_FREEZE.md):
- Opening: freeze-before-test framing per 04_HYPOTHESES.md interpretation limit
- 4.1: S03 (pre-retrieval order; parse/provider failure -> low_confidence; fail-closed; audit per decision), S17 (corpus-coverage gate within deterministic pre-check families)
- 4.2: S01 (BM25-only adjudicated thesis runtime; hash-pinned index), S11 (hybrid RRF production default; k=5 ablation), P0-7 (corpus-generation tag in cache keys)
- 4.3: T07 (schema fields, missing-value rule, relation enum, source-conflict policy, safety-criticality criteria, label manual, risk taxonomy, versioned artifacts), T15 (deterministic parser + normalizer + relation matcher offline as structured candidate; hard-gate list), S02+F02 (deployed lexical matcher untouched as lexical baseline; not semantic/relation-aware/calibrated), F10 (LLM judge never gold)
- 4.4: T07 (cost ratio fixed after expert review; latency budget), E2/G5 framing (development-only calibration, grouped CV, invalidation rule)
- 4.5: T11/T13 (paired intent_id construction; native authenticity/equivalence gates; grouped splits), T09 (frozen reviewed splits feeding derivation), F17 stated exactly (16-pair deterministic map, no LLM; 0.03% -> 33.49% on derivation population; no comparison with benchmark-population figure; Banglish uncovered), F09 honored (retrieval benefit and safety preservation measured jointly; factorial analyzed separately, never assumed)
- 4.6: S05 (classification-only artifacts; no boxes), F04+F07 honored via T06+T21 repair (source-empty treatment advice never marked verified)
- 4.7: T0-01/T0-02/T0-05 (additive audit fields; local JSONL+SQLite storage; stage timings), OTel deferral noted as non-contributing
- Constraints honored throughout: safe anchors S01/S02/S03/S05/S11/S17; artifacts T07/T11/T13/T15; prohibitions F02/F07/F09/F10/F12/F17; zero results language; H1-H5 compressed verbatim-in-meaning from 04_HYPOTHESES.md
-->

*End of draft v1.*
