# RAG Database — KrishokTech Advisory System

## Overview

This folder contains the retrieval-augmented generation (RAG) database for the KrishokTech Bengali agricultural advisory system.

**2,120 knowledge nodes** covering crops, diseases, pests, fertilizers, and cultivation practices — sourced from 13 Bangladeshi agricultural institutions (BARC, BARI, DAE, CABI, etc.).

## Folder Structure

```
rag_index/
├── raw/                          # Original unmodified data
│   └── knowledge_nodes.json      # 2,120 nodes from AgriTrust
│
├── source_md/                    # 2,946 source markdown files
│   ├── BARC/                     # 321 files
│   ├── BARI/                     # 1,506 files
│   ├── DAE/                      # 340 files
│   └── ... (12 publishers)
│
├── processed/
│   ├── knowledge_nodes_clean.jsonl       # Cleaned + normalized
│   ├── knowledge_nodes_refined.jsonl     # Gemini-refined (checkpoint)
│   └── knowledge_nodes_final.jsonl       # Final merged output
│
├── indexes/
│   ├── bm25_index.pkl            # BM25Okapi sparse index
│   ├── bm25_corpus_tok.pkl       # Tokenized corpus
│   ├── embeddings.npy            # Dense vectors (mE5-small, 384d)
│   ├── nodes.faiss               # FAISS IndexFlatIP
│   ├── node_ids.json             # Row index → node_id mapping
│   ├── chunks_bm25.pkl           # R13: BM25 over 4,815 source_md chunks (fallback evidence)
│   ├── chunks_corpus.jsonl       # R13: chunk records (path+offsets+sha256, no text copy)
│   └── chunks_sha256.txt         # R13: pin of the chunk artifacts
│
├── provenance/                   # Node→QA and MD→QA manifests (top level, not raw/)
│   └── node_to_md_map.json       # R13: precision-first node→MD coverage map (1,713/2,120)
│
├── scripts/
│   ├── 01_clean_and_normalize.py # Bengali Unicode normalization + cleaning
│   ├── 02_build_bm25.py         # Build BM25 index (k1=2.2, b=0.4)
│   ├── 03_refine_nodes_gemini.py # Gemini refinement (one node per call)
│   ├── 04_merge_refined.py       # Merge + quality gate
│   ├── 05_build_embeddings.py    # Dense embeddings via mE5
│   ├── 06_build_faiss.py         # FAISS exact index
│   └── 07_evaluate.py            # Retrieval evaluation
│
├── logs/
│   ├── cleaning_report.json
│   ├── refinement_log.json
│   └── quality_report.json
│
└── manifest.json                 # This dataset's metadata + config
```

## Pipeline

### Phase 1: Data Preparation
1. `01_clean_and_normalize.py` — Bengali Unicode normalization, field mapping
2. Source MD files organized by publisher (for context enrichment)

### Phase 2: Refinement (Gemini API)
3. `03_refine_nodes_gemini.py` — Two workers, round-robin key rotation, checkpoint after every node
4. `04_merge_refined.py` — Merge refined nodes with quality report

### Phase 3: Retrieval Index
5. `02_build_bm25.py` — BM25Okapi sparse index (Bengali-tuned params)
6. `05_build_embeddings.py` — Dense embeddings (mE5-small or API-based)
7. `06_build_faiss.py` — FAISS exact inner-product index

### Phase 4: Evaluation
8. `07_evaluate.py` — Recall@k, MRR, nDCG@k against farmer benchmark

## Running Refinement

```powershell
# With API keys directly:
uv run python scripts/03_refine_nodes_gemini.py --keys "key1,key2,key3"

# With .env file:
uv run python scripts/03_refine_nodes_gemini.py --keys-file ..\.env
```

**Key behaviors:**
- Two parallel workers (round-robin key rotation)
- Checkpoint saved after EVERY node (append mode — never lost)
- Resumable: skips already-refined node IDs
- On 429: rotates to next key automatically
- On 401/403: aborts immediately

## Safety Constraints

- Chemical names, dosages, units: **preserved exactly** (never modified)
- No new treatments generated — only refinement of existing content
- Source MD content used as context for richer refinement
- All provenance tracked (node → source document → publisher)

## Retrieval Configuration

| Component | Choice | Rationale |
|---|---|---|
| Sparse | BM25Okapi (k1=2.2, b=0.4) | Bengali-tuned params (FIRE evaluation) |
| Dense | mE5-small or BGE-M3 (via API) | Best Bengali retrieval per FLOP |
| Vector DB | FAISS IndexFlatIP | Exact search at 2K scale = no recall loss |
| Fusion | RRF (k=20, depth=50) | Scale-free, no labels needed |
