# Frozen Artifact Hashes — Vision Checkpoints (2026-09-17)

**Purpose:** appendix hash table + re-run input contract. All SHA-256 over full files.
**N04 re-export (2026-09-17):** all models except chilli re-exported at per-model train imgsz (rice now 224/10-class). Table below is POST-export (verified against disk; critic fix #1 applied — stale pre-export SHAs removed).

## PyTorch checkpoints (`backend/ml_assets/vision/*/model.pt`)

| Model | Bytes | SHA-256 |
|---|---|---|
| brassica_disease | 11049979 | c3632475083492be7f1d6db5601ed9cd44f1a3fecbc74d8419d4a738b83cf99e |
| chilli_disease | 3204482 | 243d9eacfe4fcbe250cc73066dbba8badece240128ee9f7931cd753d32f6165e |
| corn_disease | 11030843 | a5b92794445299bcb81fbacf664d7ac0478298e993e1f6b99230c6a01486d7a0 |
| crop_classifier | 11048514 | 12f6ba58051fc00e93ff84ed307efd833e1b4b0ddc0a408ab62a4653af84622f |
| potato_disease | 11032834 | d57b961ebf78280c03ebd9ff25cb414a2a2151a50eec584d4fa9168bb56b6698 |
| rice_disease | 20903190 | 12c36c85c9f5330be3265ae3f6234978a37e10c0f6e7de4095177970852c302f |
| wheat_disease | 9437091 | f4c6d2fa835744b2cab4392275556b918171cce61f04a058497e6dbe9965c7f3 |

## FP32 ONNX (`backend/ml_assets/vision/onnx/` — re-exported 2026-09-17)

| File | Bytes | SHA-256 |
|---|---|---|
| brassica.onnx | 21840066 | 85ceb12ed2d57f9a4046aae3ce4daf079240ee710a003d710f7b6bd94095a6cf |
| chilli.onnx | 6191953 | 847674752701490177dc9261ae7b1ccacd30b7489ddca8fe4f9a21cae0b79bce |
| corn.onnx | 21803921 | a641c528d68c6b8fec0735db6dffaf8c74126172737f109188bf084989adbd69 |
| crop_classifier.onnx | 21834742 | b9c34acf76a3d8a04820d7f26c8318736478f54c568a655c09a73f55190837a5 |
| potato.onnx | 21798793 | a71016d001d25cca1d263d33ed284dcf9edecc9636d1ca97f525b80d29563a96 |
| rice.onnx | 41476690 | e2d52275bf3f96e650a8827484cabbfe1e7a0e9571835eb5b25d2616dd298f0a |
| wheat.onnx | 6207322 | 06dcd7f57ba868bc552694c7102b6620d885fe20bc584f0f39284a9646289c11 |

## INT8 ONNX (`backend/ml_assets/vision/onnx_int8/`)

| File | Bytes | SHA-256 | Deployable? |
|---|---|---|---|
| brassica_int8.onnx | 5605142 | 2b3a8cc1ae0a9dec93b0041d49be31a6d17b0c501a970c802fa9fcbd944cc5b7 | Eval only (n=51 not reportable) |
| crop_classifier_int8.onnx | 1678848 | 65a7abf0e2d89afce47c73b00e88d8a9aaf697dd2620ea405df082b83f42950b | Yes (n=578 reportable) |
| potato_int8.onnx | 5594555 | b05a344b3ced48451d27b2e5f1305e7265483e78aee00c6c43b03a73e8f1b450 | Eval only (n=15 not reportable) |
| rice_int8.onnx | 1681491 | 728acd97be338587287117f992199a8ea12261bc92fdc3d9879fb5e7031cd051 | NO — rejected (2.5pp drop, agree 0.875) |
| wheat_int8.onnx | 1685294 | 4bf0141f6d2aee69114a8903e01e03bafb6394109b3657b2804ac2ff29eabc23 | Yes (n=400 reportable) |

## Router classes (verified 2026-09-17)

`crop_classifier` = 10 classes: Cabbage, Cauliflower, Chili, Eggplant, Gourd, Guava, Others, Potato, Rice, Tomato. No Wheat / Corn class — Wheat and Corn disease models are reachable only via user-hint bypass. `chilli_disease` = 8 classes (dir `chilli_disease/`).

## Decisions recorded (P0-11)

- [x] Manuscript "10-class" confirmed correct; code comments fixed; STATE.md §4 still says 6-class → update when STATE is next touched (CEA track owns STATE? No — STATE is EACL Demo/state; flag for the EACL state keeper).
- [ ] Wheat-mitigation branch (`crop_label == "Wheat"`) is unreachable with the 10-class router → removal review pending; comment now marks it legacy. Decision needed: remove or keep as dead safety net.
- [ ] E02 re-run contract: THIS hash set + 1,237-image manifest + per-model imgsz.
