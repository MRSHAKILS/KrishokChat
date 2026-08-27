# Section 10: Results — Linguistic & Multimodal Robustness (Draft Skeleton)

## 10.1 Bengali Linguistic Registers
- Standard Bengali, Regional Dialects (Sylheti/Chittagonian), Romanized Banglish, Authentic Farmer queries (Table 8).
- Text-first RAG suffers 57.1% abstention on regional dialects due to morphological drift (Layer E06).
- Detection gating restores dialect coverage to 89.8% (+46.9 pp) with 0.0% CUAR (Layer E21).

## 10.2 Multimodal Perception & Visual Conditioning
- INT8 ONNX vision classifier collapses knowledge node search space by 75.64% (Layer E17).
- 96.4% top-1 accuracy on field crop leaf photographs.

## 10.3 Cross-Modal Conflict Policy
- Automatic conflict detection between uploaded images and contradictory query symptoms, triggering safe conversational clarification.
