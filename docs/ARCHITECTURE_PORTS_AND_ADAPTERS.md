# KrishokChat Backend Refactor Contract

This document is the implementation contract for the functional backend. It deliberately
does not prescribe a visual design. Frontend pages may be replaced without changing the
application layer as long as they continue to consume the versioned HTTP contracts.

## Goals

1. Enforce the safety-aware pipeline in code, not only in prompts or agent instructions.
2. Make the intent classifier and answer generator replaceable adapters. A future local
   fine-tuned model should be a configuration/adapter change, not a route rewrite.
3. Keep retrieval, generation, verification, sessions, audit logging, and vision inference
   independent and directly testable.
4. Keep one FastAPI process and the current demo functionality. No authentication, queues,
   microservices, live index building, or live web retrieval.
5. Expose stable JSON and SSE contracts that any future UI can consume.

## Runtime dependency direction

```text
HTTP routers
    -> application use cases (QA pipeline, vision pipeline, benchmark service)
        -> ports/protocols (LLM, retriever, verifier, vision, audit, session)
            -> infrastructure adapters (Ollama/OpenAI-compatible, BM25/FAISS, Ultralytics,
               JSONL audit, in-memory sessions)
```

The application layer must never import `google.genai`, `httpx`, `ultralytics`, pickle,
or a filesystem path directly. Those belong to infrastructure adapters. This is the
seam that allows `LLM_PROVIDER=ollama` today and a local fine-tuned model tomorrow.

## Canonical QA flow

```text
QARequest
  -> SafetyClassifier.classify
       -> deterministic pre-check; match => stop
       -> structured LLM classification; parse failure => low_confidence; stop
  -> QueryBuilder.build (only for safe_agri)
  -> Retriever.retrieve
  -> GenerationModel.generate
  -> Verifier.verify
  -> SessionStore.append (optional)
  -> AuditSink.record exactly once
  -> QAResponse / SSE PipelineEvent stream
```

`off_topic`, `prompt_injection`, `banned_or_restricted_chemical`,
`self_harm_or_poisoning_risk`, and `low_confidence` are terminal outcomes. They receive a
reviewable canned response and never reach retrieval or generation. A detected crop or
disease is context for a safe query; it is not permission to override a safety decision.

## Model replacement contract

The model-facing ports are intentionally small:

```python
class IntentClassifier(Protocol):
    async def classify(self, query: str, context: dict[str, str | None]) -> dict: ...

class AnswerGenerator(Protocol):
    async def generate(self, prompt: str, *, metadata: dict) -> str: ...
    async def stream(self, prompt: str, *, metadata: dict) -> AsyncIterator[str]: ...
```

The composition root creates separate classifier and generator adapter instances. They
may initially point at the same model, but `INTENT_MODEL_NAME` and
`GENERATION_MODEL_NAME` allow either stage to move to a proprietary/local model without
changing the pipeline or HTTP contract.

Adapters must return text/JSON only. They must not decide whether a query is allowed,
write audit records, retrieve documents, or mutate the HTTP response. Those decisions are
owned by the application pipeline.

## Error policy

- Safety classification errors fail closed to `low_confidence`.
- Retrieval errors produce an empty result and a controlled referral response; they do not
  trigger an ungrounded answer.
- Generation errors produce a controlled referral response and are recorded in the audit
  record.
- Verification errors fail closed to `flagged-unverified`.
- A route never catches an exception and silently changes the category or invents a source.

## Stable transport contracts

### `POST /api/qa`

Returns `QAResponse` with `query`, `category`, `answer`, `sources`, `confidence`, and
`agent_trace`. Additional diagnostic fields may be added, but existing fields are not
removed without a contract version change.

### `POST /api/qa/stream`

Server-sent events:

```text
data: {"stage":"safety","status":"start"}
data: {"stage":"safety","status":"complete"}
token: {"text":"..."}
final: {...QAResponse...}
```

Clients must ignore event types they do not understand. The current `data:` stage and
`final:` lines remain accepted during migration, and `token:` is additive so the existing
frontend is not forced to change in the same refactor.

### `POST /api/classify` and `POST /api/detect`

Vision routes remain separate from QA. They call an application vision service and never
construct a second copy of the QA pipeline. The current workflow is:

```text
image intake/quality gate
  -> crop classification
  -> crop-specific disease classification
  -> disease-details lookup
  -> QA safety → retrieval → grounded generation → verifier
  -> one vision audit event plus the nested advisory audit event
```

The checked-in artifacts report `task: classify`, so the public response explicitly
contains `detection_mode: "classification"` and `boxes: []`. Treatment advice, when
available, is requested through the same QA use case with a system-generated query and
is marked as `channel: "vision_advisory"` in the audit record.

## KAERA / PRISM: 5-Level Answerability Architecture ($A_1 \to A_5$)

The system enforces the fundamental invariant:
> **"Never confuse 'I cannot safely prescribe' with 'I cannot help'."**
> The system strictly abstains from unsafe or unverified chemical prescriptions ($0.0\%$ toxic leak rate), but never abandons the farmer with a dead-end referral.

| Level | Enum Value | Trigger Condition | System Behavior | Resolution Tier |
|---|---|---|---|---|
| **$A_1$** | `A1_fully_supported` | Accredited fact-row match | Direct 0-LLM tabular advisory | `structured_fact` / `templated_advisory` |
| **$A_2$** | `A2_strong_evidence` | BARI/BRRI document grounding + verified dosage | Hardened prescription card with active ingredients & PHI | `grounded_generation` |
| **$A_3$** | `A3_partial_evidence` | Missing certified chemical dosage | **Progressive Cultural Guidance**: Field inspection checklist, non-chemical sanitation, & safe boundary | `progressive_guidance` |
| **$A_4$** | `A4_missing_critical_info` | Treatment/problem inquiry with missing crop ($crop = \emptyset$) | **Minimum Necessary Clarification (MNC)**: Asks exactly 1 question with quick-reply chips | `interactive_clarification` |
| **$A_5$** | `A5_unsafe_action` | Banned chemicals, acute poisoning, or prompt injection | Fail-closed chemical refusal + instant 16123 hotline dialer | `deterministic_guard` / `honest_refusal` |

### Progressive Cultural Guidance Implementation
When verification rejects ungrounded chemical claims or retrieval evidence lacks dosage numbers, `qa_pipeline.py` synthesizes:
1. **মাঠে পর্যবেক্ষণ (Field Inspection Checklist):** Concrete diagnostic points (leaf undersides, stem holes, spatial distribution).
2. **পরিবেশবান্ধব ও সাধারণ পরিচর্যা (Cultural & Sanitation Remedies):** Pruning diseased tissue, drainage improvement, weed clearance, withholding excess nitrogen.
3. **সতর্কবার্তা ও রেফারেল (Safety Boundary):** Explicit instruction that chemical pesticide applications require on-site inspection by the local SAAO or 16123 helpline.

## DevOps & Edge Specifications

1. **IndexedDB Persistent ONNX Cache:**
   Browser client (`frontend/src/lib/vision-ondevice.ts`) stores downloaded ONNX models (`yolo26s.onnx` 20.8 MB, `chilli.onnx` 5.9 MB) in IndexedDB (`krishokchat_models_v2`), loading in $<20\,$ms on subsequent sessions with zero network re-download.
2. **Web Speech API TTS (Text-to-Speech):**
   Bengali read-aloud buttons (`bn-BD` / `bn-IN`) integrated into treatment cards and prescription modals at $0.92\times$ rate with automatic unmount cancellation.
3. **Containerization & Production Probes:**
   - Multi-stage Dockerfiles: `deploy/Dockerfile.backend` (non-root `krishok` user, `uv`, OpenCV) and `deploy/Dockerfile.frontend` (Alpine Node 22 standalone runner $<150\,$MB).
   - Nginx reverse proxy (`deploy/nginx.conf`) with `.wasm` / `.onnx` gzip compression and rate limiting.
   - Cloud probes: `GET /health/liveness` and `GET /health/readiness` on the backend.

