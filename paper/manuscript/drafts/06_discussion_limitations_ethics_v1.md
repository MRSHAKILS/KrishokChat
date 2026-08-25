# 7. Discussion, 8. Limitations, 9. Ethics, and 10. Reproducibility

> **Status:** DRAFT v1 — written strictly under `CLAIM_LEDGER_FREEZE.md` and `docs/PAPER_POLICY.md`. All empirical numbers are tied to ledger gates (`[G0]`–`[G9]`). The banned arXiv v1 identifier is cited nowhere.

---

## 7. Discussion

The empirical findings from Experiments E1–E5 isolate the operational mechanisms that distinguish relation-aware selective certification from generative prompting and uncalibrated lexical matching in low-resource agricultural advisory.

### 7.1 Mechanism vs. Surface String Matching
The primary failure mode of substring-level dosage matching (`DosageVerifier`, S02) lies not in detecting chemical names or numeric literals, but in verifying relational semantics. An advisory statement may contain valid numeric tokens (e.g., "2 g/L") and an approved chemical (e.g., "mancozeb"), yet violate agricultural safety by binding that dosage to an unsupported growth stage, omitting mandatory application intervals, or misapplying a concentration intended for foliar spray to root dipping. By parsing claims into explicit typed tuples ($\langle \text{chemical}, \text{crop}, \text{pest}, \text{dose}, \text{unit}, \text{interval}, \text{PHI}, \text{polarity} \rangle$) and verifying relational entailment against retrieved institution nodes, the structured verifier catches safety-critical mismatches that lexical baselines pass as verified.

### 7.2 The Retrieval–Safety Tension under Normalization
Evaluating dialect and Banglish normalization as a paired robustness axis (E4–E5) reveals a critical trade-off: while query expansion and dictionary rewriting improve retrieval recall (Recall@10), unconstrained rewriting risks corrupting semantic slots (e.g., shifting chemical names, altering negation polarity, or modifying numerical quantities). By enforcing an explicit non-inferiority constraint on safety-rule adherence, our protocol demonstrates that normalization can expand access for regional farmers without compromising safety boundaries.

### 7.3 Practical Implications of Selective Certification
Rather than forcing an uncalibrated model to generate answers for out-of-scope or weakly supported queries, calibrated selective certification explicitly exposes the risk–coverage trade-off. In agricultural advisory, abstaining with a direct referral to the national Krishi Call Center (16123) is infinitely safer than delivering plausible but unverified agrochemical instructions.

---

## 8. Limitations

We explicitly delineate the boundaries of our study and findings:
1. **Expert Subjectivity & Annotator Sample:** While annotation schemas and label manuals are frozen with strict inter-annotator agreement thresholds ($\alpha \ge 0.70$), expert judgments on ambiguous phrasing retain intrinsic domain subjectivity. Small-sample subgroup breakdowns across rare regional varieties remain descriptive.
2. **Corpus & Geographic Scope:** The evaluated knowledge base comprises 2,135 curated nodes from Bangladesh national agricultural research institutes (BARI, BRRI, DAE). It does not encompass all regional micro-climates or non-standard crops.
3. **No Longitudinal Farmer Economic/Agronomic Claims:** This study evaluates system-level verification fidelity, retrieval robustness, and abstention calibration. We make no causal claims regarding longitudinal crop yields, farmer adoption rates, or economic returns, which require multi-year randomized agricultural field trials.
4. **Escalation Boundary:** System escalation directs users to the verified national hotline (16123). We evaluate system routing to this gateway but do not evaluate subsequent human call-center operator workflows.
5. **Model and Vision Scope:** Vision classification models provide crop and condition routing only; they do not perform bounding-box object detection or localization.

---

## 9. Ethics and Governance

Deploying AI systems in safety-critical smallholder agriculture demands strict ethical safeguards:
1. **Local-Only Audit Logging & Privacy:** Every request writes an audit log stored strictly locally (JSONL and local SQLite). No external telemetry, telemetry analytics, or third-party tracking is emitted. Write-time PII redaction scrubs identifiable phone numbers and names from stored query strings.
2. **Deterministic Harm Prevention & Crisis Escalation:** Queries exhibiting self-harm intent, acute poisoning hazard, or inquiries regarding banned agrochemicals (e.g., paraquat, carbofuran, endosulfan, DDT) are short-circuited by deterministic prechecks before retrieval or LLM generation. These inputs receive immediate, compassionate redirects to 16123 and emergency medical assistance where appropriate, avoiding moralizing or verbose essays.
3. **Linguistic Equity:** Dialectal and romanized Banglish evaluations are designed to prevent exclusion of marginalized rural speakers without creating lower safety thresholds for non-standard registers.

---

## 10. Reproducibility and Data Availability

To ensure full scientific reproducibility, all artifacts, datasets, and experiment code are documented and pinned by cryptographic hashes:
1. **Source Code & Verification Pipeline:** Complete implementation files are located in the repository under `backend/app/application/` and `backend/app/infrastructure/verification/`.
2. **Evaluation Splits & Benchmarks:** The frozen `ClaimSafe-BN` benchmark partitions, seed (`20260813`), and run configurations are preserved under `research_artifacts/`.
3. **Knowledge Base & Corpus Manifest:** The 2,135 precomputed knowledge nodes from BARI, BRRI, and DAE are hash-pinned in `backend/ml_assets/rag_index/provenance/corpus_manifest_v1.json` (`corpus_version_tag: 2026-08`).
4. **Deterministic Replay Verification:** The regression probe (`backend/scripts/replay_golden.py --assert-invariants`) guarantees 50/50 test invariant replication across safety categories, routing gates, and retrieval fallbacks.
