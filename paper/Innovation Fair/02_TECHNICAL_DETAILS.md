# Bangladesh Innovation Fair 2026 — Technical Details Field

**Project Name:** KrishokChat — Bengali Agricultural Intelligence for Farmers, Extension and Rural Communities  
**Portal Field:** Technical Details (Key components, design, programming languages, materials, tools & equipment)

---

### Technical Specification

KrishokChat is implemented as a modular, production-oriented agricultural advisory platform built on a clean architectural separation of concerns (Application, Domain, Ports/Protocols, and Infrastructure layers). This architecture ensures that core agronomic logic and safety contracts remain immutable, while underlying ML models, retrieval backends, and external telecom gateways can be seamlessly upgraded or swapped.

#### 1. Core Architecture & Languages
* **Frontend:** Next.js 16 (React 19, TypeScript, Tailwind CSS, Motion animations, shadcn/ui components). Implements an offline-capable Progressive Web Application (PWA) with Service Worker precaching of knowledge packs.
* **Backend:** FastAPI (Python 3.11+, asynchronous ASGI runtime, strict Pydantic v2 schemas). Single-service architecture with sub-millisecond local routing.
* **Deployment & Containerization:** Dockerized micro-deployments, pre-warmed ML asset loading, health/readiness endpoints (`/api/health`, `/api/ready`), structured JSON-lines local audit logging, and Server-Sent Events (SSE) for real-time multi-agent execution streaming.

#### 2. Natural Language Processing & 5-Tier Resolution Ladder
* **Bengali Unicode Processing:** NFKC canonicalization, dialect normalization across 5 major regions (Rajshahi, Rangpur, Chittagong, Noakhali, Sylhet), and dual Bengali-English script parsing.
* **Tier 0 Deterministic Safety Gate:** Regex & lexical rules intercept banned/restricted pesticides (e.g., Paraquat, Carbofuran), crisis/poisoning emergencies, and prompt injection attacks prior to any LLM invocation, routing to the national **16123** helpline or emergency services in <0.1 ms.
* **Tier 1 & 2 Deterministic Fact-Base:** Precomputed relational SQLite knowledge graph (`fact_base_v1.json`) resolving common disease management queries deterministically in ~3.8 ms at $0.00 serving cost.
* **Tier 3 Hybrid Retrieval:** BM25 sparse lexical search combined with FAISS dense vector retrieval over multilingual embedding spaces (`multilingual-e5-base`), pre-indexed across 2,946 institutional extension manuals from DAE, BARI, BRRI, and BARC.
* **Generative Advisory Engine:** Grounded response synthesis via fine-tuned Gemma-4 (4-bit quantized) and interchangeable llama.cpp / Ollama local runtimes or OpenRouter APIs.

#### 3. Multimodal Vision & Crop Pathology Pipeline
* **Hierarchical Classification:** Two-stage Ultralytics vision workflow: a crop identifier first routes leaf imagery to dedicated crop-specific pathology models (Potato, Rice, Maize, Wheat, Brassica).
* **Quantized Edge Runtime:** Exported `.pt` weights converted to INT8 ONNX format for on-device inference via `onnxruntime-web` (WebAssembly/WebGL) on low-cost smartphones without image upload latency.
* **Cross-Modal Conflict Resolution:** Automated reconciliation between user textual symptoms and computer vision predictions, triggering clarification requests on contradictory inputs.

#### 4. Relational Verification & Safety Contracts
* **11-Slot Agronomic Contract:** Schema-enforced validation of critical advisory fields (Crop, Problem, Active Ingredient, Min Dose, Max Dose, Unit, Water Dilution, Application Interval, Pre-Harvest Interval, Safety Gear, Regulatory Status).
* **Fail-Closed Dosage Hardening:** Algorithmic verification rejecting ungrounded or hallucinated chemical dosages, reducing critical unsafe acceptance (CUAR) to 0.0%.

#### 5. Rural Delivery & Edge Optimization
* **Bandwidth Adaptation:** Multi-channel response delivery supporting rich Web UI, low-bandwidth WebP compression, offline PWA cache, and template-compressed 160-character Bengali SMS formats for non-smartphone farmers.
