# Scoped Adjudication Execution Rules

These rules apply to implementation of this adjudication package. Root `AGENTS.md`, `docs/PAPER_POLICY.md`, and refactor architecture contracts take precedence.

1. Read `README.md`, `MEMORY.md`, `03_THESIS_DECISION.md`, and the assigned row in `11_FINAL_IMPLEMENTATION_SPEC.md` before work.
1a. This folder is the single active execution authority. Parent-folder documents are evidence and historical rationale only. If a parent task graph, thesis, or priority conflicts with this package, follow this package and record any required change through the dated amendment process.
2. The frozen decision is **OPTION B: Keep A, modify B.** Do not restore a broad A+B thesis without a dated approved amendment.
3. During T05-T07 evidence and protocol work, create research artifacts only. Do not modify application code or existing planning documents.
4. One agent owns one task and its declared outputs. Do not redesign hypotheses, relations, endpoints, margins, or contribution wording during implementation.
5. Use stable IDs for sources, evidence spans, intents, variants, claims, annotations, runs, models, dictionaries, calibrators, and outputs. Never identify evidence by list position alone.
6. Every expert label retains annotator ID, guideline/schema version, timestamp, raw label, confidence/notes where approved, and adjudication lineage. Never replace raw labels with only the consensus label.
7. Every dataset and run has a manifest with paths, SHA-256 hashes, split IDs, source/intent/transformation lineage, seed, code revision, dirty-tree flag, configuration, model/provider/version, prompt hash where applicable, hardware, dependencies, failures, and output hashes.
8. Preserve raw audit artifacts: source snapshots or permitted references, original/normalized text, normalization diffs, parser traces, raw model outputs, relation traces, safety decisions, and test logs. Release only what licensing/privacy permits, but retain an internal evidence index.
9. Fail closed. Missing evidence IDs/spans, parser failure on safety-bearing text, unresolved dimensions, polarity, applicability, source conflict, calibration artifact, or optional-model failure cannot produce certification.
10. Preserve safety before retrieval, BM25-only runtime, shared JSON/SSE use case, local-only audit, existing ports, and classification-only vision behavior. Do not add an agent topology, graph/dense retriever, web fallback, service, queue, auth, or telemetry.
11. Never create an active implementation in legacy `backend/app/agents/` or `services/advisory/`. Extend domain, port, application, infrastructure, and container boundaries only after offline gates pass.
12. Reproduce the current lexical verifier without silent fixes. Implement the proposed deterministic parser/normalizer plus structured relation matcher as a separate candidate.
13. An LLM judge is never gold. Optional NLI and fixed LLM-judge baselines retain exact model/version, prompt, raw output, failures, and costs; they cannot override hard safety rules.
14. Split by source, intent, and transformation lineage. Keep all regional, Banglish, adversarial, and normalized forms of one intent in one split.
15. Do not access test data to edit parsers, dictionaries, unit tables, prompts, calibrators, or thresholds. Any test-informed change invalidates the confirmatory run and requires a versioned re-freeze.
16. Do not implement a learned normalizer by default. Begin only after the dictionary baseline leaves the frozen development gap and every safety/intent/slot gate is specified.
17. Native/expert review is required for dialect authenticity, intent equivalence, relation gold, applicability, source conflict, and safety criticality. Automatic scores may assist but cannot replace these labels.
18. Fix the vision fallback so source-empty treatment is never marked verified. Route sourced advice through the same verifier or return an explicit uncertified/abstained result.
19. Treat all T01 local-PDF numbers as **NEEDS RECONCILIATION** until T05 records a stable artifact, hash, and count method. Do not average conflicts or infer missing counts.
20. Follow root paper policy. Do not mention, cite, summarize, quote, or reuse prohibited material. Reference authoritative local papers only as permitted by policy.
21. A task is complete only when its stop/go gate passes, exact commands and failures are recorded, outputs are hashed, and `MEMORY.md` receives an append-only completion or blocker entry.
22. Local-model integration follows `13_LOCAL_MODEL_INTEGRATION_PLAN.md` as an independent engineering lane. Preserve the existing `gemini` and `krishoktech-4b` model IDs and selector behavior; do not replace the default model, duplicate the QA pipeline, or modify research components while enabling the GGUF.
23. The checked-in filename `backend/ml_assets/gemma/krishoktech.f16.gguf` does not by itself prove 4-bit quantization. Record GGUF metadata, architecture, chat template, file hash, and quantization before making model-format claims.
24. Ollama remains the default serving path. Direct llama.cpp serving is approved only for the base+LoRA runtime and boundaries recorded in `14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md` and the root-stack amendment; an agent must not introduce another provider or alter shared pipeline behavior.
