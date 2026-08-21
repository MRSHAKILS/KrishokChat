import os
import shutil
import json
from pathlib import Path
from huggingface_hub import HfApi

TOKEN = os.environ.get("HF_TOKEN")
REPO_ID = "RaiyanKhaan/KrishokChat-Advisory-System"

BASE_DIR = Path(r"d:\KrishokChat Advisory System")
ML_ASSETS = BASE_DIR / "backend" / "ml_assets"
STAGING_DIR = BASE_DIR / "hf_staging"

if STAGING_DIR.exists():
    shutil.rmtree(STAGING_DIR)
STAGING_DIR.mkdir(parents=True, exist_ok=True)

print(f"Staging directory prepared: {STAGING_DIR}")

# 1. Vision Models
vision_src = ML_ASSETS / "vision"
vision_dst = STAGING_DIR / "vision"
vision_dst.mkdir(parents=True, exist_ok=True)

vision_folders = ["crop_classifier", "brassica_disease", "corn_disease", "potato_disease", "rice_disease", "wheat_disease"]
for folder in vision_folders:
    src_folder = vision_src / folder
    dst_folder = vision_dst / folder
    dst_folder.mkdir(parents=True, exist_ok=True)
    for item in src_folder.iterdir():
        if item.is_file():
            print(f"Linking vision file: {item.name} -> vision/{folder}/{item.name}")
            shutil.copy2(item, dst_folder / item.name)

if (vision_src / "verification_report.json").exists():
    shutil.copy2(vision_src / "verification_report.json", vision_dst / "verification_report.json")
if (vision_src / "verification_report_live.md").exists():
    shutil.copy2(vision_src / "verification_report_live.md", vision_dst / "verification_report_live.md")

# 2. Gemma LLM Models (GGUF & Checkpoint)
gemma_src = ML_ASSETS / "gemma"
gemma_dst = STAGING_DIR / "gemma_llm"
gemma_dst.mkdir(parents=True, exist_ok=True)

if (gemma_src / "krishokchat.f16.gguf").exists():
    print("Linking GGUF model: krishokchat.f16.gguf")
    # Using hardlink or copy
    try:
        os.link(gemma_src / "krishokchat.f16.gguf", gemma_dst / "krishokchat.f16.gguf")
    except Exception:
        shutil.copy2(gemma_src / "krishokchat.f16.gguf", gemma_dst / "krishokchat.f16.gguf")

ckpt_src = gemma_src / "raw" / "checkpoint-4020"
ckpt_dst = gemma_dst / "checkpoint-4020"
ckpt_dst.mkdir(parents=True, exist_ok=True)
for item in ckpt_src.iterdir():
    if item.is_file() and item.name != "optimizer.pt":  # skip raw 140MB optimizer state to keep it clean, keep adapter + weights
        print(f"Linking LLM checkpoint file: {item.name}")
        shutil.copy2(item, ckpt_dst / item.name)

# 3. RAG Knowledge & Retrieval Index
rag_src = ML_ASSETS / "rag_index"
rag_dst = STAGING_DIR / "rag_knowledge_index"
rag_dst.mkdir(parents=True, exist_ok=True)

# Indexes
(rag_dst / "indexes").mkdir(parents=True, exist_ok=True)
for f in ["nodes.faiss", "embeddings.npy", "bm25_index.pkl", "bm25_corpus_tok.pkl", "node_ids.json", "term_map.json", "index_sha256.txt"]:
    p = rag_src / "indexes" / f
    if p.exists():
        print(f"Linking RAG index file: {f}")
        try:
            os.link(p, rag_dst / "indexes" / f)
        except Exception:
            shutil.copy2(p, rag_dst / "indexes" / f)

dialect_p = BASE_DIR / "dataset_release" / "safety" / "phase4_dialect_map.json"
if dialect_p.exists():
    shutil.copy2(dialect_p, rag_dst / "indexes" / "phase4_dialect_map.json")

# Processed Nodes
(rag_dst / "processed").mkdir(parents=True, exist_ok=True)
for f in ["knowledge_nodes_clean.jsonl", "knowledge_nodes_refined.jsonl"]:
    p = rag_src / "processed" / f
    if p.exists():
        print(f"Linking RAG processed node: {f}")
        try:
            os.link(p, rag_dst / "processed" / f)
        except Exception:
            shutil.copy2(p, rag_dst / "processed" / f)

# Eval & Provenance
(rag_dst / "eval").mkdir(parents=True, exist_ok=True)
for f in ["farmer_benchmark_1000.jsonl", "coverage_gaps_v1.json", "dialect_map_derivation_audit_v1.json", "golden_retrieval_probe.json", "hybrid_smoke.json"]:
    p = rag_src / "eval" / f
    if p.exists():
        shutil.copy2(p, rag_dst / "eval" / f)

(rag_dst / "provenance").mkdir(parents=True, exist_ok=True)
for f in ["manifest_md_to_qa.json", "manifest_node_to_qa.json"]:
    p = rag_src / "provenance" / f
    if p.exists():
        try:
            os.link(p, rag_dst / "provenance" / f)
        except Exception:
            shutil.copy2(p, rag_dst / "provenance" / f)

if (rag_src / "manifest.json").exists():
    shutil.copy2(rag_src / "manifest.json", rag_dst / "manifest.json")
if (rag_src / "README.md").exists():
    shutil.copy2(rag_src / "README.md", rag_dst / "README.md")

# 4. Advisory Engine
adv_src = ML_ASSETS / "advisory"
adv_dst = STAGING_DIR / "advisory_engine"
adv_dst.mkdir(parents=True, exist_ok=True)
for item in adv_src.iterdir():
    if item.is_file():
        shutil.copy2(item, adv_dst / item.name)

# 5. Model Card README.md
readme_content = """---
language:
- bn
- en
license: mit
tags:
- agriculture
- bangladesh
- crop-disease-detection
- yolov8
- gemma
- lora
- rag
- faiss
- bm25
- bengali-nlp
- computer-vision
pipeline_tag: text-generation
---

# KrishokChat: Agricultural Advisory & Disease Detection Model Suite

**KrishokChat** is an end-to-end provenance-traceable multi-task Bengali agricultural advisory and crop disease diagnosis system designed for Bangladeshi farming ecosystems.

This repository contains the complete suite of models, fine-tuned weights, knowledge indexes, and advisory maps used by the KrishokChat application.

---

## 📂 Repository Structure

```
RaiyanKhaan/KrishokChat-Advisory-System/
├── README.md                                  # Main Model Card & Usage Guide
├── vision/                                    # Ultralytics YOLO Crop & Disease Vision Models
│   ├── crop_classifier/
│   │   ├── model.pt                           # 9-Crop Root Classifier (11.96 MB)
│   │   └── class_names.json                   # Crop class mapping
│   ├── brassica_disease/
│   │   ├── model.pt                           # Brassica Disease Classifier (10.54 MB)
│   │   ├── class_names.json                   # Disease labels (Alternaria, Black Rot, Downy Mildew, etc.)
│   │   └── disease_details.json               # Symptoms & remedy metadata
│   ├── corn_disease/
│   │   ├── model.pt                           # Corn / Maize Disease Classifier (10.52 MB)
│   │   ├── class_names.json                   # Labels (Common Rust, Gray Leaf Spot, Northern Leaf Blight, Healthy)
│   │   └── disease_details.json
│   ├── potato_disease/
│   │   ├── model.pt                           # Potato Disease Classifier (10.52 MB)
│   │   ├── class_names.json                   # Labels (Early Blight, Late Blight, Healthy)
│   │   └── disease_details.json
│   ├── rice_disease/
│   │   ├── model.pt                           # Rice Disease Classifier (3.06 MB)
│   │   ├── class_names.json                   # Labels (Bacterial Blight, Brown Spot, Blast, Rice Hispa, Sheath Blight)
│   │   └── disease_details.json
│   ├── wheat_disease/
│   │   ├── model.pt                           # Wheat Disease Classifier (9.00 MB)
│   │   ├── class_names.json                   # Labels (Wheat Blast, Leaf Rust, Stem Rust, Stripe Rust, etc.)
│   │   ├── disease_details.json
│   │   └── metadata.json
│   ├── verification_report.json               # Benchmark accuracies & test validation outputs
│   └── verification_report_live.md
├── gemma_llm/                                 # Bengali Agricultural Domain Language Models
│   ├── krishokchat.f16.gguf                   # 16-bit GGUF model for fast CPU/GPU inference via llama.cpp/Ollama (1.29 GB)
│   └── checkpoint-4020/                       # Stage-1 SFT Fine-Tuned LoRA Adapter Weights & Tokenizer
│       ├── adapter_model.safetensors          # LoRA weights (266.2 MB)
│       ├── adapter_config.json                # LoRA hyperparameter configuration
│       ├── tokenizer.json                     # Bengali-extended SentencePiece tokenizer (30.68 MB)
│       ├── tokenizer_config.json
│       ├── processor_config.json
│       ├── chat_template.jinja                # Jinja2 chat template for conversation turns
│       ├── trainer_state.json                 # Training history & loss curves
│       └── training_args.bin
├── rag_knowledge_index/                       # Hybrid Dense (FAISS) + Sparse (BM25) Knowledge System
│   ├── indexes/
│   │   ├── nodes.faiss                        # FAISS FlatIP index (BGE-M3 1024-dim dense embeddings) (8.34 MB)
│   │   ├── embeddings.npy                     # Dense embedding matrix
│   │   ├── bm25_index.pkl                     # Sparse BM25 Okapi retrieval index (16.23 MB)
│   │   ├── bm25_corpus_tok.pkl                # Tokenized BM25 corpus (4.47 MB)
│   │   ├── node_ids.json                      # Node identifier lookup table
│   │   ├── term_map.json                      # Domain taxonomy, pesticide brand mapping & disease synonyms
│   │   └── phase4_dialect_map.json            # 6-Region Dialect normalization map (Barisal, Chittagong, Sylhet, etc.)
│   ├── processed/
│   │   ├── knowledge_nodes_clean.jsonl        # 2,135 Clean Knowledge Nodes (BARC, BARI, BRRI, CABI, DAE) (11.99 MB)
│   │   └── knowledge_nodes_refined.jsonl      # Refined multi-turn grounded knowledge nodes (9.95 MB)
│   ├── eval/
│   │   ├── farmer_benchmark_1000.jsonl        # 1,000 real-world Bengali farmer benchmark queries
│   │   ├── coverage_gaps_v1.json              # Coverage gap audit report
│   │   └── dialect_map_derivation_audit_v1.json
│   ├── provenance/
│   │   ├── manifest_md_to_qa.json             # Literature-to-QA audit trail (9.98 MB)
│   │   └── manifest_node_to_qa.json           # Node-to-QA audit trail (2.78 MB)
│   ├── manifest.json                          # Build manifest with version hashes
│   └── README.md
└── advisory_engine/                           # Structured Advisory Mapping
    ├── disease_knowledge_map.json             # Disease-to-remedy & dosage structured dictionary
    ├── generated_knowledge_nodes.jsonl        # Multi-step expert verified advisory nodes
    ├── generation_tasks.json                  # Advisory evaluation tasks
    └── test_cases.md                          # Clinical test cases & expected responses
```

---

## 🌿 1. Vision Models (Crop & Disease Detection)

The vision pipeline implements a two-stage hierarchical classifier using **Ultralytics YOLO**:
1. **Stage 1 (Root Crop Classifier)**: Identifies the crop species (`Brassica`, `Corn`, `Potato`, `Rice`, `Wheat`, `Solanacea`, etc.).
2. **Stage 2 (Disease Specialist)**: Routes the image to the dedicated crop disease classifier to determine the specific pathogen / health state.

### Classes Supported:
- **Rice Diseases**: Bacterial Leaf Blight, Brown Spot, Healthy Leaf, Leaf Blast, Leaf Scald, Narrow Brown Leaf Spot, Rice Hispa, Sheath Blight.
- **Wheat Diseases**: Wheat Blast, Black Point, Fusarium Foot Rot, Leaf Rust, Leaf Blight, Powdery Mildew, Stem Rust, Stripe Rust, Healthy.
- **Potato Diseases**: Early Blight, Late Blight, Healthy Leaf.
- **Corn Diseases**: Common Rust, Gray Leaf Spot, Northern Leaf Blight, Healthy.
- **Brassica Diseases**: Cabbage Alternaria Spot, Cabbage Black Rot, Cabbage Downy Mildew, Cauliflower Downy Mildew, Cauliflower Bacterial Soft Rot, Cauliflower Black Spot, Healthy.

### Usage Example:
```python
from ultralytics import YOLO
from PIL import Image

# 1. Classify Crop
crop_model = YOLO("vision/crop_classifier/model.pt")
crop_result = crop_model("leaf.jpg")[0]
predicted_crop = crop_model.names[crop_result.probs.top1]
print(f"Detected Crop: {predicted_crop}")

# 2. Classify Disease (e.g., Rice)
if predicted_crop.lower() == "rice":
    disease_model = YOLO("vision/rice_disease/model.pt")
    disease_result = disease_model("leaf.jpg")[0]
    predicted_disease = disease_model.names[disease_result.probs.top1]
    print(f"Diagnosis: {predicted_disease}")
```

---

## 🤖 2. Language Models (Gemma Bengali Agriculture LLM)

- **Base Model**: Google Gemma 4B Instruction-Tuned
- **Fine-Tuning**: LoRA Stage 1 Supervised Fine-Tuning (SFT) on verified Bengali agricultural Q&A datasets.
- **GGUF Quantization**: 16-bit GGUF model optimized for CPU/GPU edge deployment.

### Usage with Hugging Face Transformers & PEFT:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

base_model_id = "google/gemma-2-2b-it" # or 4B base
tokenizer = AutoTokenizer.from_pretrained("gemma_llm/checkpoint-4020")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = PeftModel.from_pretrained(base_model, "gemma_llm/checkpoint-4020")

prompt = "<start_of_turn>user\\nধানের ব্লাস্ট রোগের লক্ষণ ও প্রতিকার কী?<end_of_turn>\\n<start_of_turn>model\\n"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.2)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Usage with llama-cpp (GGUF):
```python
from llama_cpp import Llama

llm = Llama(
    model_path="gemma_llm/krishokchat.f16.gguf",
    n_ctx=2048,
    n_threads=6
)
output = llm(
    "<start_of_turn>user\\nআলুর লেট ব্লাইট কীভাবে প্রতিরোধ করব?<end_of_turn>\\n<start_of_turn>model\\n",
    max_tokens=256,
    temperature=0.2
)
print(output["choices"][0]["text"])
```

---

## 📚 3. Hybrid RAG Knowledge & Retrieval System

The RAG index combines dense semantic search and sparse lexical matching:
- **Dense Index**: FAISS FlatIP index with 1024-dimensional `BAAI/bge-m3` multilingual embeddings across 2,135 curated agricultural knowledge nodes.
- **Sparse Index**: BM25 Okapi index tokenized for Bengali domain vocabulary.
- **Dialect Normalization**: 6 Regional Bangladeshi dialects (Rajshahi, Sylhet, Chittagong, Barisal, Rangpur, Noakhali) mapped to standard terms.
- **Sources**: Bangladesh Agricultural Research Council (BARC FRG 2024), BARI, BRRI, CABI, DAE, DLS, DoF.

### Usage Example:
```python
import faiss
import numpy as np
import pickle
import json

# 1. Load FAISS index and metadata
index = faiss.read_index("rag_knowledge_index/indexes/nodes.faiss")
with open("rag_knowledge_index/indexes/node_ids.json", "r", encoding="utf-8") as f:
    node_ids = json.load(f)

# 2. Load BM25 index
with open("rag_knowledge_index/indexes/bm25_index.pkl", "rb") as f:
    bm25 = pickle.load(f)

print(f"FAISS index loaded with {index.ntotal} vectors.")
```

---

## 🔗 Integration with Frontend (`suggested-questions.tsx`)

In KrishokChat's user interface, `suggested-questions.tsx` connects directly to this model suite:
- Vision outputs (`predicted_crop`, `predicted_disease`) are mapped via `CROP_LABELS` and `DISEASE_LABELS` to dynamically generate targeted Bengali advisory prompts.
- `DialectSelector` triggers regional dialect queries normalized by `phase4_dialect_map.json` into the hybrid RAG retrieval pipeline.

---

## 📄 License & Attribution

- **License**: MIT License
- **Developed by**: Raiyan Reza ([RaiyanKhaan](https://github.com/RaiyanKhaan))
- **Project**: KrishokChat - A Provenance-Traceable Multi-Task Bengali Agricultural Advisory System
"""

(STAGING_DIR / "README.md").write_text(readme_content, encoding="utf-8")
print("README.md written successfully!")
