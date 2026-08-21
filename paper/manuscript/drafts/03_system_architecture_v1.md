# 3. System Architecture

> **Status:** DRAFT v1 (2026-08-22) — factual description of the evaluated runtime only; no results or performance figures. Written under `CLAIM_LEDGER_FREEZE.md` (trace map at end of file); single external citation per brief. The arXiv v1 identifier banned by `docs/PAPER_POLICY.md` is cited nowhere.

This section describes the KrishokChat runtime exactly as deployed and evaluated; it contains no results, and all performance figures are deferred to Section 6. Three commitments organize every component presented here: safety decisions precede retrieval, answers are grounded in retrieved evidence before display, and every request leaves one complete local audit record. We use the staged vocabulary of agentic retrieval-augmented pipelines (Singh et al., 2025) to describe this flow. Figure 1 summarizes the stages; Sections 3.1 through 3.7 state what each stage guarantees and what it leaves to later sections.

**Figure 1. KrishokChat pipeline as evaluated.** Each user query meets pre-retrieval safety routing first; only queries classified `safe_agri` proceed to BM25 retrieval, generation, and verification, while terminal safety outcomes exit before retrieval and fail closed to a canned referral. Every completed request terminates in either a response or a referral and writes exactly one local audit record. Rendering of the diagram is produced programmatically at assembly time.

```
User query → [1] Safety/Router → [2] Retrieval (BM25) → [3] Generation → [4] Verifier → Response/Audit
```

## 3.1 Pre-retrieval safety routing

Pre-retrieval safety routing is the first stage of the pipeline and runs before any corpus access. The router assigns every incoming query to exactly one of six categories: `safe_agri`, `banned_or_restricted_chemical`, `self_harm_or_poisoning_risk`, `off_topic`, `prompt_injection`, and `low_confidence`. Only `safe_agri` queries continue to retrieval. Every other category terminates immediately with a canned response and an audit entry. No query in a terminal category reaches the index or the generator.

Classification proceeds in two layers. A deterministic pre-check applies keyword and rule families first, and structured LLM classification handles the remaining cases. If the classifier output cannot be parsed or its provider fails, the query maps to `low_confidence`; the stage is fail-closed under infrastructure faults. The two harm-related terminal categories receive short referrals rather than generated advice: both name Krishi Call Center 16123, the national agricultural helpline, and the self-harm referral adds a note to seek in-person medical help when the situation is an emergency.

Routing also extends to the boundary of the collection through a deterministic corpus-coverage gate. Six keyword families route likely out-of-corpus requests to `low_confidence`, where they receive the standard referral instead of an attempted answer. In a pinned 50-item golden replay probe, unanswerable queries were refused 12/12, off-topic 2/2, and answerable queries were refused 0/32 by the gate — keyword-scoped, not semantic. We accordingly treat the gate as a bounded guard over known out-of-corpus patterns; coverage of unseen out-of-corpus intents remains unmeasured.

## 3.2 Retrieval

Retrieval is intentionally conservative. The retriever is BM25 over a precomputed index of 2,135 knowledge nodes drawn from national agricultural institutions, and the index file is pinned by hash so the exact evaluated artifact can be re-verified at any time. Cache keys carry a corpus-generation tag, which makes cached answers computed against an older index unreachable after any rebuild. Retrieval failures degrade to empty result sets and a controlled referral rather than to partially filled contexts.

The production default also offers hybrid retrieval, which fuses BM25 with dense rankings through reciprocal-rank fusion; this paper's confirmatory evaluation nevertheless runs on BM25 alone as the thesis runtime and treats hybrid retrieval as an ablation comparator (Section 5). A structural property of fused rankings motivates the design that follows: reciprocal-rank fusion quantizes top-1 scores by construction, so score magnitude alone cannot gate abstention. Unsupported-content control therefore belongs to the verification stage downstream of generation, not to any threshold on retrieval scores.

## 3.3 Generation

Generation runs through one shared QA pipeline regardless of transport: JSON and streaming endpoints invoke the same use case, so both expose identical safety, retrieval, and verification behavior. Generation itself draws on a small open-weight generator class reached through a provider failover chain, which keeps answering available when a single provider fails. The safety classifier stays outside this chain and retains its direct client, because routing decisions must not depend on generation-provider health. A local CPU inference lane provides a further fallback behind a concurrency semaphore, so queued requests wait rather than overload the model process. A locally fine-tuned checkpoint artifact exists within this setup with recorded hashes; we make no performance claim for it in this paper.

## 3.4 Verification

Verification is the last processing stage before a response is released. The deployed verifier is a normalized lexical dosage matcher, and we refer to it throughout as the lexical baseline. It first canonicalizes Bengali and English numerals, units, denominators, and interval expressions into comparable forms, then matches the normalized dosage strings against retrieved sources by substring lookup. Its reach is narrow by design: the mechanism is not semantic, it is not relation-aware, and it is not calibrated. That limitation defines precisely the upgrade target that Section 4 develops into relation-aware verification.

Flagging follows an annotate-and-drop policy. When the lexical baseline finds an unsupported numeric claim, it attaches a flag to the answer instead of suppressing the response, and flagged answers remain displayed with that annotation. Alongside the deployed matcher, a structured candidate exists offline: a deterministic claim parser, a normalizer, and a relation matcher built for relation-aware verification. This candidate is not wired into the serving path; Section 4 specifies it, and Section 5 evaluates it against the lexical baseline.

## 3.5 Vision routing

Uploaded photographs follow a two-stage vision route before any advice is produced. A crop classifier identifies the crop, and a crop-specific disease classifier then labels the observed condition. Both artifacts perform classification only; they emit no bounding boxes, and we claim no localization capability. Treatment text requested behind a vision route enters the shared QA pathway under a vision-advisory channel, so it falls under the same verifier or receives an explicitly uncertified outcome. A repaired fallback closes the residual gap: source-empty treatment advice can never be marked verified, even when both classifiers succeed.

## 3.6 Benchmark endpoint and audit trail

The service surface closes with two supporting mechanisms. First, a benchmark endpoint serves statistics computed entirely offline from stored artifacts; it computes nothing at request time, so live load stays independent of evaluation bookkeeping. Second, every request produces exactly one local audit record, written as JSONL and mirrored into SQLite. Each record carries the assigned safety category, the action taken, retrieval hit and passage counts, verifier verdicts, per-stage timings, token counts, the serving provider, and a request identifier. Audit storage is local-only with retention limits and redaction controls applied at write time, and the system emits no external telemetry.

## 3.7 Problem formulation

We close with the problem formulation that the remainder of the paper instantiates. Given a query, a generated answer, and retrieved passages where each passage carries a stable source identifier and an exact evidence span, certification asks which of the answer's claims hold against those spans. Claims are parsed into a schema over the fields crop, disease/pest, action, chemical/intervention, formulation, amount, unit, denominator, interval/frequency, PHI/safety condition, polarity (affirmed, negated, conditional, prohibited), an applicability predicate, uncertainty, and source conflict. Certification is then a function of parsed evidence relations rather than of surface similarity, and deciding when to certify at all becomes an instance of selective certification.

Under this formulation, hypotheses H1–H5 are tested under expert gold labels on frozen grouped splits (Section 5). Section 4 specifies the claim schema, the structured candidate that performs relation-aware verification, and the calibration step that turns per-claim verdicts into selective certification. It likewise fixes the paired protocol under which dialect normalization is treated as a safety-constrained robustness axis rather than as silent preprocessing. In offline sampling of 1,000 real farmer queries, dialect-expansion triggered on 0.6% of requests, so expansion alone cannot carry dialect coverage; Section 4 treats normalization as a measured protocol instead. Section 5 presents the experiment matrix under which these components are measured.

---

<!--
Trace map (paper/manuscript/CLAIM_LEDGER_FREEZE.md):
- Opening + Figure 1: S01 (BM25-only runtime), S03 (safety precedes retrieval; fail-closed terminal outcomes)
- 3.1: S03 (six categories; terminal canned referral; fail-closed mapping), S17 (coverage gate: six keyword families; pinned golden probe 12/12, 2/2, 0/32; keyword-scoped-not-semantic scope note); 16123 referral wording per AGENTS §4 and skeleton §9 Ethics
- 3.2: S01 (BM25 as thesis runtime), S11 (2,135 nodes; hybrid RRF as production default; expansion hit rate 0.6%/1,000), S15 (quantized fused top-1; score magnitude cannot gate abstention), P0-7 (corpus-generation tag in cache keys)
- 3.3: S04 (shared QA pipeline across JSON/SSE), T0-06 (provider failover chain; safety classifier direct client), S08+F06 (checkpoint artifact with hashes; no performance claim)
- 3.4: S02 (normalized lexical dosage matcher), F02 (prohibition honored: not semantic/relation-aware/calibrated), S14 (annotate-and-drop), T15 (offline structured candidate)
- 3.5: S05 (classification-only artifacts; empty boxes), T06+T21/G8 (repaired fallback; source-empty never verified)
- 3.6: S12 (benchmark endpoint serves precomputed stats), T0-01/T0-02/T0-04/T0-05 (one audit record per request; JSONL+SQLite; field set), skeleton §9 Ethics (retention, redaction, no external telemetry)
- 3.7: 03_THESIS_DECISION.md (frozen formulation), 04_HYPOTHESES.md (H1-H5), T09 (frozen grouped splits)
-->

*Provisional reference (assembly: G0 re-verification required): Singh et al. (2025). Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. arXiv:2501.09136.*

*End of draft v1.*
