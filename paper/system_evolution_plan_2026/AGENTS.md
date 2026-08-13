# Scoped Execution Rules

These rules apply only inside `paper/system_evolution_plan_2026/` and to future execution of this plan. Root `AGENTS.md`, `docs/PAPER_POLICY.md`, and refactor handoff contracts take precedence.

1. **Authority routing:** this parent folder is historical evidence and proposal context. The only active execution authority is `execution_planning_2026_08_12/`. Read its `AGENTS.md`, `README.md`, `MEMORY.md`, and assigned row in `11_FINAL_IMPLEMENTATION_SPEC.md`. Do not execute `09_AGENT_TASK_GRAPH.md` directly.
2. One agent owns one task and its listed deliverables. Do not invoke other agents unless the orchestrator explicitly assigns coordination.
3. Do not modify application code during planning tasks. Implementation tasks may edit only the exact domain/port/adapter/container boundaries approved by the task owner.
4. Never create a second active pipeline under legacy `backend/app/agents/` or `services/advisory/`.
5. Preserve safety before retrieval, fail-closed behavior, shared JSON/SSE use cases, local-only audit, and classification-only vision claims.
6. Never cite, quote, summarize, or reuse the deprecated paper prohibited by root policy.
7. Treat the two PDFs in `paper/done papers/` as authoritative filenames, not self-verifying numeric evidence. Keep numbers TODO until T01/T05 reconcile them with stable artifacts.
8. Compute dataset counts from located files. Record path, schema, count method, SHA-256, and errors. Do not infer root `dataset_release` exists.
9. Every experiment requires a manifest, input/output hashes, split IDs, seed, code revision, configuration, model/provider version, hardware, and failure log.
10. Split by source and intent lineage. Keep all variants of one query intent in one split.
11. Never use LLM judgment as sole gold for Bengali safety, dialect authenticity, or claim support. Use expert/native review and report agreement.
12. Keep research contributions, software engineering, and UI work labeled separately.
13. Do not claim hybrid retrieval is active; `application/container.py` currently wires BM25 only.
14. Do not call the current verifier semantic; it matches normalized dosage strings.
15. Do not mark treatment advice verified without stable evidence IDs and verification.
16. Do not add planner/critic/supervisor loops, web fallback, new services, auth, telemetry, or object detection.
17. Record blockers in `MEMORY.md` without overwriting prior evidence. Change plan decisions through an explicit dated amendment.
18. A task is complete only when its completion criterion passes and its deliverables link to reproducible evidence.
19. The local GGUF/model-selector work is a separate engineering lane defined by `execution_planning_2026_08_12/13_LOCAL_MODEL_INTEGRATION_PLAN.md` and its dated runtime amendment. It must not alter the frozen research thesis or bypass safety, retrieval, verification, or audit behavior.
