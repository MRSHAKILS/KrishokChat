# Beat D+E Literature Notes — Agri Vision, On-Device Inference, Multimodal Conflict

**Research pass:** 1  
**Cutoff:** 2026-09-17  
**Purpose:** evidence ledger for the Beat D+E story. This is not paper prose.

## A. Closest prior work

| Work | Relevance | How we must position it |
|---|---|---|
| PlantVillage lineage + successors | Crop-disease image classification baselines | Classification itself is precedent; cite as the task foundation |
| AgroGPT (WACV 2025) | AgroInstruct 70k; 3B/7B beat ChatGPT-class on fine-grained disease ID | Diagnosis endpoint, English-only; ours is scope-gating + Bengali advisory integration |
| Farmer.Chat (`arXiv:2409.08916`) | Multimodal (image/audio) farmer advisory at scale | Server-side multimodal without published routing/conflict/degradation design |
| KrishokBondhu (`arXiv:2510.18355`) | Voice-only Bengali advisory | No vision; direct complement, not competitor, on this beat |
| My Climate CoPilot (ACL 2025 demo) | Transparent agri QA | No vision modality at all |
| SMART (CEA literature) | Structured multimodal + human-in-the-loop diagnosis | Closest architectural cousin; distinguish by on-device browser path + conflict badge + measured rates |
| On-device INT8 literature (general) | Quantization with accuracy gates | Method precedent; ours applies reportability gating (n≥100, drop+agreement thresholds) |

## B. Open gaps (to our current knowledge — verify before claiming)

1. No Bengali agricultural system publishes a text-vs-image crop-conflict detection rate.
2. No accepted ACL/EACL demo shows image-conditioned retrieval-space reduction (vs diagnosis display).
3. Few agri-vision papers report browser-WASM timings from a real browser harness alongside parity and INT8 gates.

## C. Follow-up literature to dig (not yet read)

1. **Cross-modal consistency / VQA contradiction detection** (general ML) — for the badge framing. *Not yet verified.*
2. **Calibrated abstention in image classification** (OOD detection, margin-based deferral) — for the tri-state gate framing. *Not yet verified.*
3. **ICT4D on-device ML deployment** — for the WASM/offline significance. *Not yet verified.*

## D. Citation-use rules

- Cite PlantVillage/AgroGPT for the task; never imply diagnosis novelty.
- Cite SMART as the closest cousin with explicit differences.
- Report all vision numbers with n, checkpoint date, and harness (Python vs browser).
- Never substitute Python timings for browser timings or vice versa.
