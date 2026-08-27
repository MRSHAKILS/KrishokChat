# EACL Demo Section 02: System Architecture & Decision Pipeline (Draft Skeleton)

## 2.1 Architectural Blueprint & Subsystems
- Decoupled port-and-adapter architecture (FastAPI backend + Next.js 14 frontend).
- Five coordinated pipeline stages (Table 1):
  1. Safety Screening Gate (6-way intent classification).
  2. Multimodal Perception Router (INT8 ONNX crop & disease classifiers).
  3. Deterministic Knowledge Resolver (3-hop SQLite graph traversal over 2,135 nodes).
  4. Hybrid Grounded Generation (BM25 + dense retrieval + fine-tuned Gemma-4 4-bit LoRA).
  5. Relational Verifier (11-slot fail-closed single-record certification).

## 2.2 Dual-Audience User Experience (Farmer vs. Expert)
- Farmer Mode: Minimalist Bengali UI, voice/photo inputs, audio playback, structured Safe Action Cards.
- Expert/Extension Mode: Detailed model confidence, retrieved passages, 11-slot verification matrix, telemetry audit logs.
