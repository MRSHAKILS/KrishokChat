# EACL Demo Section 05: Deployment, Portability & Ethics (Draft Skeleton)

## 5.1 Deployment Footprint & Hardware Accessibility
- Total container footprint (measured 2026-08-30, deduped): 95.64 MB unique ONNX (40.59 MB browser primary) + 55.60 MB .pt fallbacks, 112.7 MB RAG index, minimal 284.0 MB / full 339.6 MB (previous 2.63 GB/3.70 GB fabricated, see STATE.md S3).
- Deploys on low-cost Linux VPS ($45/month) or edge servers without proprietary cloud API dependencies.

## 5.2 Ethical AI & Smallholder Safeguards
- Zero tolerance for autonomous chemical hallucinations: LLM cannot invent dosages or PHI.
- Verified government helpline integration (Krishi Call Center 16123).
- Strict privacy: Ephemeral on-prem image/voice processing without commercial third-party retention.
