# Landscape, Gaps, and Competitive Position

## Manageable literature taxonomy

The nine review clusters reduce to five evidence groups. Detailed paper notes remain in `paper/literature review/`; this file does not duplicate them.

| Group | Original clusters | Decision relevance | Local source |
|---|---|---|---|
| Verification and selective answering | Agentic RAG; low-resource safety | Supports structured claims, abstention, safety-monotone action | `01_agentic_rag_verifier_systems.md`, `02_llm_safety_low_resource.md`, `11_RESEARCH_GAPS_competitive_matrix.md` |
| Bengali dialect and retrieval | Bengali NLP; low-resource retrieval | Supports parallel intent sets, normalization ablation, human validation | `03_low_resource_nlp_bengali.md`, `07_retrieval_low_resource_rag_eval.md` |
| Agricultural advisory and escalation | Agricultural systems; ICT4D | Defines domain comparators, expert ground truth, Bangladesh study constraints | `04_agri_ai_advisory_systems.md`, `09_ict4d_global_south.md` |
| Vision and multimodal routing | Crop disease vision | Supports honest classification and source-grounded treatment; secondary scope | `05_vision_crop_disease.md` |
| Systems evidence and compute | Track conventions; edge/streaming | Requires component evaluation, latency accounting, artifacts, human evidence | `06_system_industry_track_conventions.md`, `08_edge_slm_streaming_systems.md` |

## Selected gaps

### Gap A: structured dosage verification and calibrated abstention

The designated gap input establishes missing calibrated abstention for Bengali agricultural QA and missing safety-monotone refusal in corrective RAG. The broader package reports generic and medical claim verifiers but no agricultural relation verifier for Bengali dosage-bearing advice. The execution target is narrower than “agentic verification”: typed agricultural relations plus risk-aware abstention.

### Gap B: dialect-sensitive retrieval with safety-preserving normalization

The literature package finds no published dialect-to-retrieval measurement for Bangla agriculture and no dialectal safety benchmark. Normalization may improve retrieval but may also erase or alter harmful intent. The study must measure both effects on paired inputs.

## Why these gaps

- They map to existing ports and do not require a new orchestration topology.
- Each yields falsifiable component-level claims.
- They use the team’s resource lineage without duplicating a general QA or retrieval benchmark.
- They address the verified weak points of the current system: lexical dosage matching, no calibrated coverage decision, BM25-only runtime, and unmeasured dialect behavior.

## Closest-system matrix

All external facts below come from the current literature package. Re-check URLs before paper submission.

| System/method | Retrieval | Safety/abstention | Claim/dosage verification | Bengali/dialect | Field evidence | Difference | Source | Confidence |
|---|---|---|---|---|---|---|---|---|
| Farmer.Chat | RAG | No published domain gate | No | Multilingual, not this Bangla study | Large deployment studies | Scale leader; lacks typed dosage verifier | https://arxiv.org/abs/2409.08916; `04_*`, `09_*` | High |
| KrishokBondhu | Bengali voice RAG | Referral text; no reported safety layer | No claim-level verifier | Bengali; no reported dialect eval | No farmer field evaluation in review | Closest language/system competitor | https://arxiv.org/abs/2510.18355; `04_*`, `09_*` | High |
| Cross-lingual Bengali agricultural RAG | Translation-centric FAISS | OOD rejection | No | Dialects left open | No field study reported | Tests translation path, not native dialect safety | https://arxiv.org/abs/2601.02065; `04_*`, `07_*` | High |
| My Climate CoPilot | Grounded agricultural QA | Transparency focus | No typed dosage verifier reported | Not Bengali | Domain-expert evaluation | System-demo evaluation template | https://aclanthology.org/2025.acl-demo.7/; `01_*`, `06_*` | High |
| DG-Eval/Farmer.Chat evaluation | Atomic facts and contradiction | Stitching safety layer | Expert-grounded fact checking | Not Bengali dialect focus | Expert data | Strong evaluation baseline; schema differs | https://arxiv.org/abs/2603.03294; `03_*`, `04_*` | High |
| RAGChecker / RAGAS | Generic claim decomposition | No domain action policy | Claim-level NLI | No validated Bengali agri judge | Benchmark evidence | Method baseline, not advisory system | `07_retrieval_low_resource_rag_eval.md` | Medium-high |
| ClinicBot / MedRAGChecker family | Clinical RAG | Medical abstention/validation | Numeric or KG+NLI checks | English clinical | Domain evaluation | Transferable mechanism; different relations and risk | `01_agentic_rag_verifier_systems.md` | Medium-high |
| BhasaBodh/BUNO | Not agricultural RAG | No safety outcome | No | Dialect/romanized normalization | Native parallel resources | Normalization baselines only | ACL Anthology paths in `03_*`, `07_*` | High |
| Current KrishokTech code | BM25 | Six-way pre-retrieval terminal gate | Lexical numeric dosage match | Deterministic Bengali/Banglish checks; no published dialect eval | None established | Starting system; proposed work adds measurement | local code paths | High |

## Expected differentiator

The paper should claim a measured relation-verification and abstention protocol for Bengali agricultural advice, paired with an intent-preserving dialect normalization evaluation. It should not claim novelty from multiple agents, a trace UI, generic RAG, or classification-only vision.

## Complementarity to existing team resources

The next benchmark must add claim spans, typed relations, support labels, risk labels, paired language varieties, and normalization outcomes. It must not recreate general QA, treatment QA, table QA, or a broad retrieval leaderboard already associated with the two local PDFs. Exact overlap remains TODO until Stage 0 reconciles those PDFs and dataset artifacts.
