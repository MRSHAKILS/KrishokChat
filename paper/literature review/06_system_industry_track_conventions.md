# Cluster 6 — System/Application/Industry-Track Publication Conventions (META-ANGLE): Findings (2025–2026)

**Generated:** 2026-08-12 · **Scout:** 6 · **Status:** official CFP pages and proceedings front matter fetched & verified

---

## 1. Track-by-track requirements

### ACL System Demonstrations (2025 Vienna; 2026 San Diego) — primary candidate
- **Format (both years):** up to 6 pages + 2-page appendix, unlimited references/ethics; +1 page camera-ready; ACL style. Desk rejection for over-length, missing evaluation, or missing live-demo artifact.
- **Mandatory artifacts (2025–2026):** a ≤2.5-minute screencast; a live demo URL or installable package — "submissions that do not provide links will be desk rejected."
- **Evaluation is mandatory:** ACL 2026 CFP states "submissions that fail to provide any form of evaluation may be desk rejected" ([2026 CFP](https://2026.aclweb.org/calls/system_demonstration/)).
- **Numbers:** 2025: 187 submitted, 178 valid, 64 accepted (34.22%); 2026: 227 submitted, 215 valid, 85 accepted (37.45%). Best Demo 2026: olmOCR.
- **2026 accepted-demo profile:** an explicit "LLM safety tooling" cluster — DialogGuard (multi-agent psychosocial safety evaluation), RiskLab, Fast-MIA membership inference — plus agent instrumentation (PROTEA) and domain QA (GovScape, ClinQueryAgent).
- **Closest accepted analogue:** *My Climate CoPilot: A Question Answering System for Climate Adaptation in Agriculture* ([2025.acl-demo.7](https://aclanthology.org/2025.acl-demo.7/)) — evidence-grounded RAG QA for farmer advisors, evaluated by 50 domain experts, with automatic evaluation built in. **This is the template for KrishokChat.**

### ACL / NAACL / EMNLP Industry Tracks
- **Format:** 6 pages; references, limitations, ethics unlimited. EMNLP 2025: mandatory "Limitations" section, desk-reject without it ([EMNLP 2025 CFP](https://2025.emnlp.org/calls/industry_track/)). ACL 2026 industry does not use ARR — direct OpenReview, deadline Feb 14, 2026 ([ACL 2026 CFP](https://2026.aclweb.org/calls/industry_track/)).
- **Self-declared category:** every submission must self-identify as **Deployed / Emerging / Discovery**. "Emerging" explicitly permits non-deployed work with evidence of a path to real-world deployment.
- **Review criteria:** novelty, technical quality, potential impact, clarity, with explicit attention to "evaluation methodologies (human vs. automated)" and repeatable experiments.
- **Numbers:** EMNLP 2025: 193 accepted at 42%; ACL 2026: 532 submissions, 153 accepted (34.16%). ACL 2026 chair clustering: RAG/enterprise knowledge AI, agentic systems, model adaptation, evaluation/benchmarking, **safety/trustworthiness/RAI**, multimodal.
- **Accepted examples:** *SAGE: A Generic Framework for LLM Safety Evaluation* (EMNLP 2025); *Is Agentic RAG worth it? An experimental comparison of RAG approaches* and *Towards Faithful Industrial RAG* (ACL 2026) — RAG-pipeline evaluation papers clear the bar only with comparative experiments.

### AAAI-IAAI (application tracks) and AAAI Demos
- **IAAI-26 Deployed Highly Innovative Applications:** 8 pages, single-blind; deployed = "in production and used by end-users, with meaningful data collected"; every accepted paper receives the "Innovative Application" Certificate ([IAAI-26 call](https://aaai.org/conference/aaai/aaai-26/iaai-26-call/)). **Emerging Applications of AI:** 6 pages, for not-yet-deployed work with a deployment path; "the Emerging Track is more selective than the Deployed Track."
- **AAAI-26 Demonstration Program:** 2-page paper + ≤5-minute video; judged on clarity, significance, relevance, audience engagement; open-sourcing encouraged ([demo call](https://aaai.org/conference/aaai/aaai-26/demonstration-call/)).
- **IJCAI 2025 Demo Track:** 3-page paper + 2 reference pages, ≤10-minute video, no rebuttal; "applicability and potential impact" are the stated criteria ([IJCAI 2025 CFP](https://2025.ijcai.org/call-for-papers-demonstrations/)).

### KDD Applied Data Science (2025 Toronto, 2026 Jeju)
- **Hard gate:** "Submissions must include a quantification of the post-launch performance… Submissions that do not provide this quantification will be desk-rejected without review." Offline-only systems and repo-only releases are explicitly desk-rejected ([KDD 2026 CFP](https://kdd2026.kdd.org/applied-data-science-ads-track-call-for-papers/)).
- **9 pages, ACM sigconf; acceptance ~20%.**
- **Novelty definition:** "Novelty… will not generally focus on novel research contributions, but may instead lie in the choice of application domain, engineering design, usability approach, or business use case." Claude-level algorithms explicitly not required.

### CIKM 2025 Applied Research
- 7 pages, single-blind. Must "clearly outline how the work has been deployed or released and for how long, or how the work is planned to be deployed or released"; online/offline evaluation in scope ([CIKM 2025 CFP](https://cikm2025.org/calls/applied-research-papers)).

### NeurIPS 2025 Datasets & Benchmarks
- **Track-specific requirements:** (1) single-blind allowed; (2) mandatory code submission; (3) dataset hosting on Dataverse/Kaggle/HF/OpenML with a **mandatory Croissant metadata file** — invalid Croissant or inaccessible data may be desk-rejected; public release by camera-ready ([D&B CFP](https://neurips.cc/Conferences/2025/CallForDatasetsBenchmarks)).
- Scope explicitly includes benchmarks with **contamination-mitigation design**, dataset audits, curatorial methodology. 1,995 submissions in 2025.

### WACV 2026 — marginal fit
Applications track judged on systems-level innovation, novelty of domain, comparative assessment ([area chair guidelines](https://wacv.thecvf.com/Conferences/2026/AreaChairGuidelines)). The 35-class crop-disease classifier is neither a new task nor a new domain — vision alone cannot carry a WACV paper.

## 2. Evaluation expectations

**Mandatory (desk-reject thresholds):** any form of evaluation for ACL demos; post-launch quantification for KDD ADS; Limitations section for EMNLP industry; live link + video for ACL demos; Croissant + hosted data + executable code for NeurIPS D&B; accurate responsible-NLP checklist (EMNLP 2025 onward; misleading answers are desk-reject material per ARR announcement).

**Expected in practice:** human evaluation/user studies (ACL demo CFP explicitly asks "Were user studies/human evaluation experiments conducted?"; My Climate CoPilot's 50-expert precedent); human-vs-automated methodology justification in industry tracks; ablations isolating pipeline components; error analysis; cost/latency reporting.

**Nice-to-have:** open-source release ("of special interest" in both ACL demo years), publicly deployed demo, shielded online A/B data, expert-in-the-loop evaluation, LLM-judge calibration against human ratings.

## 3. Novelty-defense playbook

The "just another LLM wrapper" critique is documented reviewer behavior: the 2026 study *Reporting and Reviewing LLM-Integrated Systems in HCI* ([arXiv 2602.05128](https://arxiv.org/html/2602.05128v1)) interviewed 18 authors/reviewers and found: chatbot-shaped UIs, unpositioned work, and unjustified LLM use trigger the label; acceptance now requires component-level evals on 30–100 representative inputs. Authors who survive reviewers (a) de-emphasize LLM framing when the system is the contribution, (b) center a niche domain, (c) report exact model names/versions and an "engineering methodology," (d) position against pre-LLM literature. Track CFPs encode the same norm: KDD ADS and WACV relocate novelty to "application domain, engineering design, usability"; ACL demo novelty is judged on "the approach/technology on which this system is based." ACL 2026 industry confirms the base RAG pipeline is a commodity — accepted papers differentiate on evaluation design and deployment realities.

## 4. Concrete gaps KrishokChat can exploit

1. **No Bengali agricultural-safety dataset at tier-1 venues.** The ACL 2025 demo volume contains one agriculture-QA system (My Climate CoPilot, English, expert-facing); the nearest Bengali system (KrishokBondhu) has no safety layer and no dialect coverage. A 20,112-record, 6-dialect safety refusal/re-query dataset is unmatched in any 2025–2026 demo/industry volume.
2. **Safety-evaluation tooling is a recognized category, but only for English/enterprise.** EMNLP 2025 accepted SAGE; ACL 2026 demos accepted DialogGuard and RiskLab. None addresses low-resource agri-advisory refusal behavior or chemical/self-harm escalation routing.
3. **NeurIPS D&B explicitly solicits contamination-mitigation methodology.** The T3/T4 generation pipeline (real farmer queries → slot-based expansion → dialect rewriting) is contamination-avoidance-by-construction; the D&B CFP lists "approaches to mitigate LLM contamination" as in-scope.
4. **The deployment-evidence ladder is empty.** All candidates are demo-stage. KDD ADS desk-rejects offline-only prototypes; IAAI-26's Emerging track is the designated venue for "trajectory to deployment" work. The audit-trail logging is exactly the "measurable performance data" both IAAI tracks and KDD require once a pilot runs.

## 5. Track fit recommendation

1. **ACL 2027 System Demonstrations — primary target.** Verified precedent (My Climate CoPilot), mandatory-but-flexible evaluation, 6 pages; next cycle follows the Jan–Feb pattern ([ACL 2026 demo page](https://2026.aclweb.org/calls/system_demonstration/)).
2. **IAAI-27 Emerging Applications — second target.** 6 pages, single-blind, built for not-yet-deployed systems with a deployment path.
3. **AAAI-27 Demonstration Program — cheap supplementary play.** 2 pages + video; matches the live-demo strength of the agent-trace visualization.
4. **EMNLP 2027 Industry Track — fallback.** File under "Emerging"; mandatory Limitations; emphasize human-vs-automated evaluation of the safety router and verifier.
5. **NeurIPS 2027 Datasets & Benchmarks — for the dataset alone.** Requires HF hosting + Croissant metadata + executable generation code.
6. **Avoid KDD ADS and CIKM Applied in current form** — both demand post-launch performance evidence and desk-reject offline-only prototypes; revisit after a live farmer pilot produces post-launch metrics.