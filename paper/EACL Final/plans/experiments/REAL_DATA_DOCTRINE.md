# Real-Data Doctrine — No Templates, No Shortcuts (2026-09-17)

**User directive:** every validation runs on real queries, real pipeline executions, real API calls where the design needs them, at practically sufficient sizes. Template-constructed suites are pilots at most — never headline evidence.

## 1. What counts as REAL

| Real | Why |
|---|---|
| Farmer Benchmark 1,000 (483 FB-group + 300 field + 217 krishibangla) | authentic farmer language, multi-source |
| PRISM-1000 rows (after provenance audit passes) | 10 register conditions with route/crop labels; runs execute the real pipeline per row |
| AgRiTrust 900 + 2,882 nodes (κ=0.72/0.78 reported) | human-agreement qrels |
| Treatment QA items (2606; verbatim reference answers + chemical traces) | institutional ground truth |
| E31 100 conflict cases (live API traces, 4 arms) | real model behavior under conflict |
| E03 420 live attack calls (both arms) | real adversary measurement |
| 1,237 labeled field images | real vision evaluation |
| Real pipeline outputs as verifier/SMS inputs | the system is tested on what it actually produces |
| Single-field mutations of real answers | perturbations of real outputs (standard robustness practice — NOT templates; see §3) |

## 2. Banned practices (headline evidence)

1. Template × slot-filler query generation presented as evaluation (E09-400 style) — pilot only.
2. Hardcoded baseline constants (38.5%) — must be replaced by in-run arms on identical queries.
3. Assumed token budgets (1250/150) — must be replaced by metering on real strings.
4. Fixed-probability outcome sampling (E17/E21 style) — diagnostics only, never results.
5. n<100 for any reported rate; n<300 for any primary claim without a CI-based justification.
6. LLM-judge-only labels for safety-bearing verdicts without human agreement reporting.
7. Citing a result whose runner, dataset hash, or model config cannot be reproduced from the spec.

## 3. Mutations are NOT templates (reads-like-a-template objection, answered)

A template fabricates the *input* (the farmer never wrote it). A mutation takes a *real system output* and changes exactly one safety-bearing field (dose ×2, unit swap, PHI swap, chemical swap, interval swap, negation flip) to test whether the verifier catches it. This is metamorphic robustness testing — the same family as software mutation testing and adversarial NLP evaluation. Every mutation study ships its clean-answer controls and reports false positives alongside catch-rate. Banned: mutating template-generated answers and calling it end-to-end evidence.

## 4. Sample-size floors (CI-based, practical)

| Claim type | Floor | Rationale |
|---|---|---|
| Primary rate (recall/pass/refuse/divergence/hazard) | n ≥ 300 per arm (±5.5% Wilson) | headline claims |
| Cheap deterministic arms (CPU-only: gating, blind, metering, badge-gate, fence) | FULL sets, n = 1000+ (±3%) | CPU is free — no excuse for small-n |
| Live-API arms (generation, attacks) | n ≥ 200/arm (±7%) with CIs; E03 expansion n = 100/family (700/arm) as P1 | money costs, CIs mandatory |
| Per-mutation-type catch-rate | ≥ 200 items × 6 types + 200 clean controls | per-type estimates, not pooled mush |
| Expert-labeled farmer subset | 400 queries × 2 annotators + adjudicator, report κ | authentic confirmation of gating |
| Vision | full 1,237-image manifest, no subsampling | already labeled, CPU-cheap |
| SMS survival | N ≥ 300 real queries through the real endpoint | channel claim needs volume |
| UI/rendering claims | API-level test per claim + screenshot at capture | "renders" means executed, not coded |

## 5. No-annotator protocol (demo track — external recruitment unavailable, 7-day window)

Accepted demo papers do not run crowd annotation. Verified precedents: GenGO Ultra (ACL 2025 demo) uses LLM-as-judge with disclosed bias mitigation; NLP-KG (ACL 2024 demo) uses RAGAS + GPT-4 on 50 questions; OLMOtrace (ACL 2025 demo) uses ONE human expert rubric + LLM-judge tuned to agree (Spearman 0.73); SciRAG uses 3 annotators × 30 queries; RAGVUE uses 100 constructed triplets + qualitative cases. Our protocol follows the same norm:

1. **Audited labels primary.** PRISM-1000 route/crop labels (after P0-7 audit) + AgRiTrust human-agreement qrels (κ=0.72/0.78 reported) carry the scored claims. No new crowd labels.
2. **Team dual-review replaces crowd annotation.** Two team members independently review stratified samples; report raw agreement + disagreements resolved by discussion (disclosed as author review, never as independent annotation):
   - N01/N09: 50 wins + 50 misses/fails per run.
   - N03: 50 catches + 50 misses.
   - Farmer behavior: stratified 100 (source × outcome).
   - Total team load: ~3–4 hours across the week. Time-boxed; samples fixed before reviewing.
3. **LLM-judge only for non-safety descriptive metrics** (e.g., slot-preservation counts, paraphrase checks): model + prompt + temperature frozen, disclosed; calibrated against team review on ≥50 samples with agreement reported. NEVER the sole judge of safety-bearing verdicts (harmful/benign flips, wrong-chemical delivery, CUAR-adjacent calls — team reviews 100% of those).
4. **Unlabeled authentic data = behavioral rates, not scores.** On Farmer-1000 without expected-action labels we report clarify/pass/refuse/verifier-flag *rates* (descriptive) + team-reviewed samples — never "accuracy."
5. **Independent annotation + IRB user study = stated future work** (already in paper limitations). The demo claims author-reviewed evidence; the journal version will carry independent annotation.

## 6. Status labels (use everywhere, including ground_truth.yaml)

- REAL_MEASURED · REAL_MEASURED_SMALLN (n<floor, CI shown) · REAL_MEASURED_PARTIAL (locked components + named pending remainder) · REAL_MEASURED_PROXY · REAL_MEASURED_MIX_MODELED_COST · PILOT (template/sim, diagnostic only) · MODELED (disclosed basis) · SIMULATED (labeled) · IMPLEMENTED_UNEVALUATED · PENDING · SUPERSEDED.

## 7. N01a lesson (2026-09-17, locked)

A paired blind/gated design only measures a hazard delta if the query set contains crop-absent-with-gold cases. PRISM B/C/D/I all mention recognizable crops → gate passes everywhere → identical 30.0% both arms (McNemar p=1.0). This validates construction fidelity; the delta needs the labeling sheet (crop_slot_labeling_sheet_200.json: 137 extractor-missing of 200 real farmer queries — itself a finding: 68.5% crop-less rate in real queries).
