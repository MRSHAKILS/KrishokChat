# T04: Active Code Behavior Snapshot

## Evidence Source
- Date: 2026-08-12
- Commit: ef0d9d8c92b888c983836ab4f76e6687e7c4f452
- Branch: main

## Verification Results

### 1. BM25-Only Retrieval
- Evidence file: `backend/app/application/container.py:33-36`
- Finding: `BM25Retriever` is the **only** retriever instantiated. No FAISS, Chroma, or dense adapter exists anywhere in `infrastructure/retrieval/` (only `bm25.py` and `__init__.py`). The `QAPipeline` constructor takes a single `retriever: Retriever` port; no hybrid/ensemble retriever is composed.
- Exact quote:
  ```python
  retriever = BM25Retriever(
      index_path=settings.rag_index_path / "indexes" / "bm25_index.pkl",
      corpus_path=settings.rag_index_path / "processed" / "knowledge_nodes_clean.jsonl",
  )
  ```
- Status: **CONFIRMED**

### 2. Lexical Verifier
- Evidence file: `backend/app/infrastructure/verification/dosage.py`
- Finding: The `DosageVerifier` does pure string matching on normalized dosage expressions. No embedding comparison, no LLM call.
- **Regex patterns:**
  - `_CLAIM_RE` (line 12-15): Matches `(?P<amount>\d+(?:[.]\d+)?)\s*(?P<unit>mg|ml|gm|g|kg|l|চামচ|কাপ)` and `(?P<fraction>আধা|অর্ধেক)\s*(?P<funit>চামচ|কাপ|লিটার|l)`
- **Normalization rules** (`_normalize`, line 25-33):
  1. Bengali digits → ASCII: `০১২৩৪৫৬৭৮৯` → `0123456789` via `_BN_DIGITS`
  2. Lowercase, comma → dot, whitespace collapse
  3. Bengali/English unit alias canonicalization (e.g. `মিলিলিটার` → `ml`, `কেজি` → `kg`, `গ্রাম` → `g`, `লিটার` → `l`)
- **Verification logic** (line 49-64): Extracts claims from the answer, normalizes sources, checks each claim `not in normalized_sources`. Returns `FLAGGED_UNVERIFIED` if any ungrounded claim; `LOW_CONFIDENCE` if no sources; `VERIFIED` otherwise.
- Status: **CONFIRMED**

### 3. Safety-before-Retrieval
- Evidence file: `backend/app/application/qa_pipeline.py:103-129`
- Finding: Execution order is strictly:
  1. `PipelineStage.SAFETY` — classify query (line 104-106)
  2. If `decision.terminal` → emit SKIP for RETRIEVAL/GENERATION/VERIFIER, return canned response (line 108-118)
  3. `PipelineStage.RETRIEVAL` — only reached if safety passed (line 120-129)
  4. `PipelineStage.GENERATION` (line 131-150)
  5. `PipelineStage.VERIFIER` (line 152-164)
- Test evidence: `test_rule_block_stops_before_llm_and_retrieval` (line 85-95) confirms `retriever.calls == 0` when safety blocks.
- Status: **CONFIRMED**

### 4. Fail-Closed Safety
- Evidence file: `backend/app/application/safety.py:69-77`, `backend/app/domain/safety_policy.py:45-55`
- Finding:
  - **Provider failure** (line 69-77): `except Exception` → returns `SafetyDecision(category=LOW_CONFIDENCE, confidence=0.0, requires_escalation=True, response=canned_response(LOW_CONFIDENCE))`. Retrieval is blocked.
  - **Malformed JSON** (line 46-48): `classify_json` raises `LLMError` → caught by the same `except Exception` → fail-closed to `LOW_CONFIDENCE`.
  - **Unknown category** (line 48-49): `if raw_category not in VALID_CATEGORIES: raise ValueError("Classifier returned an unknown category")` → caught by `except Exception` → fail-closed.
  - **Low confidence safe_agri** (line 57-60): If `category == SAFE_AGRI` but `confidence < 0.65` or `requires_escalation`, reclassified to `LOW_CONFIDENCE`.
  - **Deterministic precheck** (safety_policy.py:45-55): Regex rules for `SELF_HARM_OR_POISONING_RISK` > `PROMPT_INJECTION` > `BANNED_OR_RESTRICTED_CHEMICAL`. Matching bypasses LLM entirely.
- Test evidence: `test_classifier_failure_fails_closed` (line 97-106) confirms `category == "low_confidence"` and `confidence == "blocked"` when classifier returns invalid JSON.
- Status: **CONFIRMED**

### 5. SSE/JSON Parity
- Evidence file: `backend/app/api/qa.py:107-135`
- Finding: Both endpoints call `QAPipeline` via the same `AppContainer`:
  - `POST /api/qa` (line 107-109): calls `container.qa.run(_input(payload))`
  - `POST /api/qa/stream` (line 112-135): calls `container.qa.stream(_input(payload))` which internally calls `self.run(request, on_event=publish)` (qa_pipeline.py:225)
- Both use the same `_input()` helper (line 23-31) and the same `_response()` serializer (line 91-104). The stream endpoint wraps the same `QAResult` as `final:` SSE event. The non-streaming path returns the identical `QAResponse` model directly.
- Status: **CONFIRMED**

### 6. Vision Classification-Only
- Evidence file: `backend/app/application/vision_pipeline.py:350`, `backend/app/api/vision.py:70`, `backend/app/infrastructure/vision/ultralytics_classifier.py:30-33`
- Finding:
  - `UltralyticsClassificationRunner.predict()` (line 30-33): `if spec.task != "classify": raise VisionInferenceError("Unsupported artifact task ... classification adapter refuses to fabricate boxes")`
  - API route `detect_disease` (vision.py:70): `detection_mode="classification"` hardcoded in response.
  - API route (vision.py:76): `boxes=[]` always empty list.
  - Audit log (vision_pipeline.py:350): `"detection_mode": "classification"` hardcoded.
  - `VisionModelSpec.task` default is `"classify"` (domain/vision.py:31).
- Status: **CONFIRMED**

### 7. Vision Fallback Evidence Defect
- Evidence file: `backend/app/application/vision_pipeline.py:280-294`
- Finding: Two code paths exhibit the defect:
  1. **Advisory exists but confidence is blocked/low** (line 283-286): When `advisory.confidence.value in {"blocked", "low_confidence"}` and `info.get("solution_bn")` exists, the code sets:
     - `treatment_advice = str(info["solution_bn"])` — raw knowledge base text
     - `treatment_confidence = "verified"` — **misleadingly stamped as verified** despite no LLM grounding or verification
     - `treatment_sources = ()` — **empty sources**, so the farmer cannot trace where the advice came from
  2. **No advisory at all** (line 289-293): When `advisory is None` (exception caught at line 266), falls back to `solution_bn` with same `"verified"` label and empty sources.
- The defect: Knowledge base text is presented as "verified" without passing through the verifier, and treatment_sources are empty, breaking the provenance chain.
- Status: **CONFIRMED**

### 8. Benchmark Placeholder
- Evidence file: `backend/app/api/benchmark.py:11-17`
- Finding:
  ```python
  @router.get("/api/benchmark")
  async def benchmark_endpoint():
      """Placeholder. Will serve precomputed stats from backend/ml_assets/rag_index/."""
      return {
          "status": "not_implemented",
          "message": "Will serve precomputed retrieval benchmarks and dataset stats",
      }
  ```
- Status: **CONFIRMED**

### 9. Model Adapter Seam
- Evidence file: `backend/app/infrastructure/llm/factory.py`
- Finding: Three providers supported:
  1. **`ollama`** (line 36-44): `OpenAICompatibleClient` pointed at local Ollama `/v1` endpoint
  2. **`openrouter`** (line 45-53): `OpenAICompatibleClient` pointed at `https://openrouter.ai/api/v1`
  3. **`gemini`** (line 54-62): `GeminiClient` using `google-genai` SDK
  4. **Fallback** (line 63): `UnavailableLLMClient` — raises `LLMError` on any call
- **Role-based routing** (line 32-34): `create_llm_client(settings, *, role="generation")` — if `role == "intent"`, uses `settings.intent_model_name`; if `"generation"`, uses `settings.generation_model_name`.
- **`auto` resolution** (line 18-29): Priority order: openrouter > ollama > gemini > ollama (fallback).
- The `UnavailableLLMClient` (openai_compatible.py:128-139) raises `LLMError("No LLM provider is configured")` for all methods, which triggers fail-closed behavior in safety.py.
- Status: **CONFIRMED**

### 10. Session Architecture
- Evidence file: `backend/app/infrastructure/sessions/memory.py`
- Finding: In-memory TTL store with configurable parameters:
  - **Default max_turns: 10** (line 9) → `max_messages = max_turns * 2 = 20` (line 10) — stores both user and assistant messages
  - **Default TTL: 1800 seconds (30 min)** (line 9)
  - **Storage**: `OrderedDict[str, list[dict[str, str]]]` — LRU-like, newest messages kept via `history[-self.max_messages:]` (line 33)
  - **Eviction**: Lazy `_evict()` on every `get()`/`append()` call, removes sessions older than TTL (line 16-20)
  - **Thread-safe**: `Lock()` on all operations (line 14)
- Status: **CONFIRMED**

### 11. Audit Architecture
- Evidence file: `backend/app/infrastructure/audit/jsonl.py`
- Finding: JSONL file sink, thread-safe append.
  - **Fields logged per QA entry** (qa_pipeline.py:200-216): `query`, `category`, `action` ("blocked-canned-response" | "answered"), `flagged` (bool), `verifier_flag`, `model`, `source_ids` (list), `error`, `channel`, `crop`, `disease`, `model_choice`
  - **Fields logged per Vision entry** (vision_pipeline.py:339-352): `channel`, `action`, `status`, `crop`, `crop_confidence`, `disease`, `disease_confidence`, `treatment_confidence`, `verifier_flag`, `detection_mode`, `error`
  - **Common**: `timestamp` (UTC ISO format, prepended by jsonl.py:16)
  - **Storage**: Single JSONL file at `settings.resolved_audit_log_path`, append-only with threading lock.
- Status: **CONFIRMED**

### 12. Safety Categories
- Evidence file: `backend/app/domain/enums.py:4-10`
- Finding: All `SafetyCategory` values:
  1. `SAFE_AGRI` = `"safe_agri"`
  2. `BANNED_OR_RESTRICTED_CHEMICAL` = `"banned_or_restricted_chemical"`
  3. `SELF_HARM_OR_POISONING_RISK` = `"self_harm_or_poisoning_risk"`
  4. `OFF_TOPIC` = `"off_topic"`
  5. `PROMPT_INJECTION` = `"prompt_injection"`
  6. `LOW_CONFIDENCE` = `"low_confidence"`
- Status: **CONFIRMED**

### 13. Verification Confidence Levels
- Evidence file: `backend/app/domain/enums.py:13-17`
- Finding: All `VerificationConfidence` values:
  1. `VERIFIED` = `"verified"`
  2. `FLAGGED_UNVERIFIED` = `"flagged-unverified"`
  3. `LOW_CONFIDENCE` = `"low_confidence"`
  4. `BLOCKED` = `"blocked"`
- Status: **CONFIRMED**

### 14. Pipeline Stages
- Evidence file: `backend/app/domain/enums.py:20-24`
- Finding: All `PipelineStage` values:
  1. `SAFETY` = `"safety"`
  2. `RETRIEVAL` = `"retrieval"`
  3. `GENERATION` = `"generation"`
  4. `VERIFIER` = `"verifier"`
- Status: **CONFIRMED**

## Test Results
| Test | Status | Notes |
|------|--------|-------|
| `test_api.py::test_health_and_terminal_qa_contract` | PASSED | Health check + paraquat blocked + vision black image |
| `test_pipeline.py::test_rule_block_stops_before_llm_and_retrieval` | PASSED | Regex precheck blocks before LLM call |
| `test_pipeline.py::test_classifier_failure_fails_closed` | PASSED | Invalid JSON → low_confidence, no retrieval |
| `test_pipeline.py::test_safe_query_uses_one_shared_pipeline_and_one_audit_record` | PASSED | Safe query flows through full pipeline |
| `test_pipeline.py::test_streaming_uses_same_pipeline_without_a_second_generation_call` | PASSED | Stream yields tokens + final, no double generate |
| `test_pipeline.py::test_bengali_numeral_dosage_is_matched_after_normalization` | PASSED | Bengali ২ ml normalizes to match "2 ml" |
| `test_pipeline.py::test_ungrounded_dosage_is_flagged` | PASSED | Unmatched ৫০ ml flagged as unverified |
| `test_pipeline.py::test_auto_provider_uses_configured_openrouter_key` | PASSED | auto + openrouter key → OpenAICompatibleClient |
| `test_vision.py::test_artifact_registry_uses_real_class_maps_and_matches_details` | PASSED | Registry loads real class maps, disease_info matches |
| `test_vision.py::test_classification_routes_to_advisory_workflow_without_boxes` | PASSED | Full vision pipeline → DIAGNOSED, treatment_confidence=verified |
| `test_vision.py::test_low_detail_image_stops_before_model_inference` | PASSED | Black image → INVALID_IMAGE |
| **Total: 11** | **11 passed** | **0 failed, 0 skipped** |

## Key Findings Summary
1. **BM25-only retrieval**: No dense/hybrid retrieval exists. The single BM25Retriever is the only retrieval adapter.
2. **Lexical verifier**: DosageVerifier is purely regex-based with Bengali digit normalization — no semantic understanding of dosage safety.
3. **Safety-before-retrieval**: Hard ordering enforced in qa_pipeline.py; deterministic regex precheck bypasses LLM for known harmful patterns.
4. **Fail-closed safety**: Provider failure, malformed JSON, unknown category, and low-confidence safe_agri all route to `LOW_CONFIDENCE` → blocked.
5. **SSE/JSON parity**: Both endpoints use the same `QAPipeline.run()` via the same `_input()` converter and `_response()` serializer.
6. **Vision classification-only**: `UltralyticsClassificationRunner` rejects non-`classify` tasks; boxes are always `[]`; detection_mode is hardcoded `"classification"`.
7. **Vision fallback defect**: When advisory confidence is blocked/low or advisory is None, the system falls back to raw `solution_bn` from disease_details.json and stamps it `treatment_confidence="verified"` with **empty treatment_sources** — breaking provenance.
8. **Benchmark placeholder**: Returns `{"status": "not_implemented"}` — no real data served.
9. **Model adapter seam**: Three providers (ollama/openrouter/gemini) behind `LLMClient` protocol; role-based routing selects model by intent vs generation role.
10. **Session architecture**: In-memory OrderedDict with 30-min TTL, 10-turn (20-message) window, lazy eviction.
11. **Audit architecture**: Append-only JSONL with UTC timestamps, thread-safe locking.
12. **Streaming parity**: `stream()` internally calls `run()` with an event callback; `generate_from_text()` wraps streamed text without a second LLM call.

## Open Questions for T05
1. **Vision fallback `treatment_confidence="verified"` with empty sources**: Should T05 introduce a distinct `treatment_confidence="kb_fallback"` value and include `treatment_sources` from the disease_details.json provenance path?
2. **BM25-only retrieval**: If T05 adds dense retrieval, how should the hybrid ensemble be composed? Is there a precomputed dense index already on disk?
3. **DosageVerifier lexical-only**: Should T05 add semantic verification (e.g., embedding similarity) or is the regex approach sufficient for the demo?
4. **Benchmark placeholder**: What exact precomputed stats should be served? Are they already in `backend/ml_assets/rag_index/`?
5. **Session TTL/turns**: Are the defaults (30min, 10 turns) appropriate for the demo, or should they be configurable via `.env`?
6. **OpenAI streaming**: Both `OpenAICompatibleClient.stream()` and `GeminiClient.stream()` yield the entire response as a single chunk — true chunked streaming is not implemented. Is this acceptable for the demo?
7. **Safety precheck patterns**: The deterministic regex covers self-harm, prompt injection, and banned chemicals — should `OFF_TOPIC` also have deterministic patterns, or is LLM classification sufficient?
