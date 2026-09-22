# KrishokChat Backend Test Suite Directory Structure

This directory is organized into modular categories corresponding to system boundaries, decision-ladder tiers, and domain services.

```
backend/tests/
├── README.md                      # Test suite documentation & run commands
├── test_pipeline.py               # Compatibility shim (re-exports fakes for legacy imports)
├── run_e2e.py                     # Compatibility shim (forwards to tests/e2e/run_e2e.py)
│
├── safety_gates/                  # Tier 0 & Tier 1 Pre-checks, Safety & Verification Gates
│   ├── test_coverage_gate.py          # Out-of-scope / Unanswerable gate (0 LLM tokens)
│   ├── test_chemical_registry.py      # Banned / Restricted chemicals & 16123 referral
│   ├── test_verifier_hardening.py     # Relational dosage verifier & unsupported claim dropping
│   ├── test_crop_matcher_boundary.py  # Crop entity extraction & dialectal boundaries
│   ├── test_answerability.py          # Answerability contracts & domain scope
│   └── test_redaction.py              # PII and security token redaction
│
├── rag_pipeline/                  # PRISM-RAG, Knowledge Retrieval, Grounding & Advisories
│   ├── test_prism_rag.py              # Working memory, concept normalizer, adaptive router
│   ├── test_retrieval.py              # BM25 and vector retrieval
│   ├── test_structured_resolver.py    # Structured fact resolver (0-LLM fact base)
│   ├── test_fact_base.py              # Fact base queries & validation
│   ├── test_fact_base_maize_rice.py   # Crop-specific fact base validations
│   ├── test_fact_pack.py              # Knowledge chunk compilation & fact packs
│   ├── test_chunk_fallback.py         # Chunk fallback coverage & guarantees
│   ├── test_dose_reference.py         # Canonical dosage references
│   ├── test_advisory_templates.py     # Bilingual advisory generation templates
│   ├── test_rewrite.py                # Dialectal query normalization & rewriting
│   ├── test_resolution_tier.py        # Tier-0 to Tier-4 decision ladder assignment
│   ├── test_pipeline.py               # End-to-end pipeline execution with fakes
│   └── test_intent_extraction.py      # Slot, symptom, and intent extraction
│
├── e2e/                           # End-to-End System Tests & Paper Claims
│   ├── e2e_queries.json               # Canonical paper evaluation queries (T0–T9)
│   ├── run_e2e.py                     # E2E paper-claims test runner against live server
│   ├── test_smoke_live_e2e.py         # Live endpoint smoke test
│   ├── test_smoke_qa_pipeline.py      # End-to-end QA pipeline smoke test
│   ├── test_smoke_bm25_retrieval.py   # BM25 indexing smoke test
│   └── test_golden_invariants.py      # Golden invariant checks across all tiers
│
├── api_routes/                    # FastAPI HTTP Endpoints, Middleware, Auth & SSE
│   ├── test_api.py                    # Core advisory endpoints & contracts
│   ├── test_api_versioning_keys_ratelimit.py # API keys, versioning, rate limiting
│   ├── test_admin_authz.py            # Admin role authorization & security
│   ├── test_auth.py                   # User authentication & session cookies
│   ├── test_request_id_middleware.py  # Request tracing & JSON logging middleware
│   ├── test_exception_envelope.py     # Standardized JSON error response envelope
│   ├── test_health_readiness.py       # Liveness, readiness, and /health endpoints
│   ├── test_bootstrap_checks.py       # Startup integrity checks
│   └── test_sse_heartbeat.py          # Server-Sent Events (SSE) streaming keepalive
│
├── domain_services/               # Multimodal Vision, Soil, Weather, Speech, Calendar
│   ├── test_vision.py                 # On-device YOLO leaf detection & multimodal inference
│   ├── test_soil.py                   # Soil test parsing & NPK recommendations
│   ├── test_speech.py                 # Bangla speech recognition & TTS synthesis
│   ├── test_late_blight.py            # Late blight weather risk model & alerts
│   ├── test_weather_snapshot.py       # Weather snapshot parsing & ingestion
│   ├── test_sms_compressor.py         # SMS advisory compression (160 char limit)
│   ├── test_crop_calendar.py          # Crop calendar timings & season boundaries
│   ├── test_farm_profile.py           # Farmer profile & plot management
│   └── test_notifications.py          # Proactive advisory notifications
│
└── infrastructure/                # Storage, Caching, Telemetry, LLM Failover & Ingestion
    ├── test_storage_sqlite.py         # SQLite database repository operations
    ├── test_session_sqlite.py         # SQLite conversation session store
    ├── test_audit.py                  # Audit record formatting & invariants
    ├── test_audit_sqlite.py           # Durable SQLite audit trail
    ├── test_audit_telemetry.py        # Telemetry metrics collection
    ├── test_demo_cache.py             # In-memory and disk cache layer
    ├── test_cost_pricing.py           # Token accounting & model pricing calculator
    ├── test_capability_registry.py    # Hardware/model capability discovery
    ├── test_llm_failover.py           # Gateway retries, exponential backoff, failover
    ├── test_local_lane_concurrency.py # Local model concurrency limiter
    ├── test_ondevice_parity.py        # Edge ONNX vs FP32 parity tests
    ├── test_ingestion_contract.py     # Dataset ingestion & schema validation
    └── test_history.py                # Multi-turn conversation history repository
```

---

## Running Tests

### 1. Run All Tests
```bash
uv run pytest backend/tests -v
```

### 2. Run Specific Subsystem / Folder
```bash
# Safety & Precheck Gates
uv run pytest backend/tests/safety_gates -v

# PRISM-RAG & Grounding Pipeline
uv run pytest backend/tests/rag_pipeline -v

# API Routes & Middleware
uv run pytest backend/tests/api_routes -v

# Domain Services (Vision, Soil, Weather, etc.)
uv run pytest backend/tests/domain_services -v

# Infrastructure & Storage
uv run pytest backend/tests/infrastructure -v
```

### 3. Run E2E Paper-Claims Suite Against Live Backend
```bash
# Ensure backend is running on http://127.0.0.1:8000
python backend/tests/e2e/run_e2e.py

# Or via backward-compatible shim:
python backend/tests/run_e2e.py

# Run specific groups (T0: Safety, T1: ASK Disambiguation, T3: Grounded)
python backend/tests/e2e/run_e2e.py --group T0 T1 T3
```
