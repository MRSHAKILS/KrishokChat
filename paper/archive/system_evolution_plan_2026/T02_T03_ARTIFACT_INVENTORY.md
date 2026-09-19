# T02 + T03: Artifact Inventory Report

**Generated:** 2026-08-12
**Scope:** Dataset artifacts, RAG index, vision models, Gemma checkpoint, and eval files
**Verification method:** Line counts, file sizes, SHA-256 hashes, schema sampling

---

## 1. T02 — Dataset Inventory

### 1.1 External Dataset: `E:\CSE498R\Agri-LLM\KrishokTech\krishoktech_dataset_main`

#### 1.1.1 Farmers Benchmark

| File | Lines | Size (bytes) | SHA-256 | Schema (first record fields) |
|------|-------|-------------|---------|------------------------------|
| `farmers_benchmark/farmer_benchmark_1000.jsonl` | 1,000 | 5,648,266 | `E2ADC30D69AED9DEE1D1B3F5F0EBF7584861B1DF9C687B1B32812B6215A7B7AA` | `question`, `gold_answer`, `messages[]`, `metadata{source, expert_provided}`, `row_id` |
| `farmers_benchmark/splits/test.jsonl` | 350 | 2,122,297 | `69CE51E70BC1ED04A599FFB5B50A57C20112CAF24C48FD55FE0E8DA5E46888DB` | `question`, `gold_answer`, `messages[]`, `metadata{source, expert_provided, augmented}`, `row_id` |

**Note:** No `splits/train.jsonl` in `farmers_benchmark/`. Split manifest references 30 source books across train/dev/test.

#### 1.1.2 Text QA — Safety

| File | Lines | Size (bytes) | SHA-256 | Schema (first record fields) |
|------|-------|-------------|---------|------------------------------|
| `text_qa/safety/safety_refusal_t3.jsonl` | 3,216 | 3,636,107 | `27ACDB644C9E379436439B80BE62C25BF0C942DB2A7657E0DF1035248F6C0BB9` | `safety_id`, `safety_mode=refusal`, `category`, `severity`, `pattern`, `dialect`, `persona`, `harmful_prompt`, `safe_response`, `refusal_type`, `over_refusal_test`, `adversarial_rewrite`, `safety_check`, `source` |
| `text_qa/safety/safety_requery_t4.jsonl` | 16,896 | 15,854,076 | `A578023429CF3CC48A5954FC2A8438E8F3C48DAD5A13631E40A384E07DB0C2FA` | `safety_id`, `safety_mode=requery`, `missing_slots[]`, `missing_slot_count`, `highest_dp_slot`, `dp_score`, `dialect`, `persona`, `incomplete_query`, `requery_response`, `safety_check`, `source`, `source_node_id`, `source_org`, `source_crop` |
| `text_qa/safety/splits/dev.jsonl` | 2,025 | 1,977,155 | `7BE6CC2014CF58AFA8D378A39EA09B22D02CA8F4F10FC5ECED2A523DB4C08EC3` | Mixed T3+T4 schema |
| `text_qa/safety/splits/test.jsonl` | 323 | 307,261 | `96101A6ED1E8EC9619800EC5A405345A57209860A51EF3A810061254AA742577` | Mixed T3+T4 schema |
| `text_qa/safety/splits/train.jsonl` | 16,070 | 15,572,076 | `13115239EF8E1BD02FB2392D45E8D7DD4A15850417128158E06AAB1854B65EC2` | Mixed T3+T4 schema |

**Split verification:** dev (2,025) + test (323) + train (16,070) = 18,418. Total in parent files: 3,216 + 16,896 = 20,112. **Mismatch:** splits sum to 18,418, not 20,112. The splits are a proper subset.

#### 1.1.3 Text QA — General and Treatment

| File | Lines | Size (bytes) | SHA-256 | Schema (first record fields) |
|------|-------|-------------|---------|------------------------------|
| `text_qa/general/general_full.jsonl` | 28,993 | 40,490,278 | `6EE95FE936E830AA07A3A6C525D59577815F0396BCC1AF1ABFA5CAFFA09AC449` | `cell_id`, `category`, `qtype`, `dialect`, `persona`, `formulation`, `scenario`, `bloom`, `question`, `answer`, `treatment_flag`, `chemical_trace[]`, `source_md`, `source_pages[]`, `citation`, `publisher`, `source_document`, `gen_mode`, `node_id`, `node_file`, `answer_status` |
| `text_qa/treatment/treatment_full.jsonl` | 11,224 | 22,026,143 | `DC9B87A04DD49680628B827D9817B154D70510E8198D038082897ADAD0A50E5F` | `cell_id`, `category=disease`, `qtype`, `dialect`, `persona`, `formulation`, `scenario`, `bloom`, `question`, `answer`, `treatment_flag=true`, `chemical_trace[]`, `source_md`, `source_pages[]`, `citation`, `publisher`, `source_document`, `gen_mode`, `node_id`, `node_file`, `answer_mode`, `verified`, `answer_status` |

#### 1.1.4 Table QA

| File | Lines | Size (bytes) | SHA-256 | Schema (first record fields) |
|------|-------|-------------|---------|------------------------------|
| `table_qa/qa/tableqa_all.jsonl` | 9,022 | 6,904,746 | `26E3A9F6E93CC15D63314D9CF8615056F699F611D58567859929FAABB326E5A0` | `qa_id`, `table_id`, `complexity_level`, `question_type`, `question`, `answer`, `answer_source{row_id, column}`, `multiple_sources[]`, `language`, `dialect`, `provenance{source_book, publisher, page, row_id, column}`, `citation`, `category`, `node_category` |
| `table_qa/qa/dialects/tableqa_all_dialects.jsonl` | 25,650 | 17,040,666 | `BA8362AD37D050115BCC46BA20031A7A35BF178C90C63144B9C959A2E93DDD63` | Same as tableqa_all + `quality_scores{correctness, completeness, naturalness, reasoning, average, passed}` |

#### 1.1.5 Image QA

| File | Lines | Size (bytes) | SHA-256 | Schema (first record fields) |
|------|-------|-------------|---------|------------------------------|
| `image_qa/image_qa_pairs.jsonl` | 2,045 | 5,306,535 | `5829D1A53AD080CE4429B173A76426DF1FD1BDC8A69C9654E85126FE9E3E9ED5` | `qa_id`, `image_node_id`, `qa_category`, `question_en`, `question_bn`, `answer_en`, `answer_bn`, `visual_grounding_evidence_en/bn`, `institutional_context_summary`, `images[]` |

#### 1.1.6 Markdown Corpus — QA

| File | Lines | Size (bytes) | SHA-256 | Schema (first record fields) |
|------|-------|-------------|---------|------------------------------|
| `markdown_corpus/qa/complete_queries.jsonl` | 1,536 | 1,613,671 | `073C83AA62AA8C2D0A63BF0D003D078244B6A3E8AC594FA3A2E3C907863C9BC1` | `query_bn`, `slots{crop, symptom, onset, severity, growth_stage, chemical_history}`, `source_node_id`, `source_org`, `source_file`, `source_publisher`, `source_document`, `source_pages[]`, `generated_at`, `generated_by`, `worker_id` |
| `markdown_corpus/qa/critical_treatment.jsonl` | 2,190 | 5,361,262 | `414D17F5ECD1A21060897489CEA05D13676E556BD9F377009482522D37FBA379` | `id`, `doc_id`, `category`, `qtype`, `safety_tier=critical`, `treatment_flag`, `answer_mode`, `answer`, `chemical_trace[]`, `citation`, `publisher`, `source_document`, `source_pages[]` |
| `markdown_corpus/qa/general_sft_diverse_full.jsonl` | 28,993 | 34,923,017 | `D8A32C3A32328291571C50D97B6427A38016F9D3C28EDFD5EF968BC562ED93B2` | `cell_id`, `category`, `qtype`, `dialect`, `persona`, `formulation`, `scenario`, `bloom`, `question`, `answer`, `treatment_flag`, `chemical_trace[]`, `source_md`, `source_pages[]`, `citation`, `publisher`, `source_document`, `gen_mode` |

#### 1.1.7 Markdown Corpus — Retriever

| File | Lines | Size (bytes) | SHA-256 | Schema (first record fields) |
|------|-------|-------------|---------|------------------------------|
| `markdown_corpus/retriever/retriever_train.jsonl` | 9,231 | 73,865,004 | `5A8FF2E45DCCCAF48972091D0C3CEBEABEFA6A33B1310C2E36D59A5B447E1DD7` | `query_bn`, `query_en`, `qtype`, `category`, `pos_doc_id`, `pos_text`, `pos_citation`, `neg_doc_ids[]`, `neg_texts[]` |

#### 1.1.8 Dataset Split Manifest

| File | Size (bytes) | SHA-256 | Content |
|------|-------------|---------|---------|
| `dataset_split_manifest.json` | 1,456 | `CB5A46C32863716500C94B072A80006356FBFD61848A02B1678F5FE13E280329` | `seed=42`, `total_books=30`, splits: train (24 books), dev (3 books), test (3 books) |

#### 1.1.9 External Dataset — Size Summary

| Category | Total Lines | Total Size (bytes) | Total Size (MB) |
|----------|------------|---------------------|-----------------|
| Farmers Benchmark | 1,350 | 7,770,563 | 7.4 |
| Safety (T3+T4 parent) | 20,112 | 18,490,183 | 17.6 |
| Safety Splits | 18,418 | 17,856,492 | 17.0 |
| General QA | 28,993 | 40,490,278 | 38.6 |
| Treatment QA | 11,224 | 22,026,143 | 21.0 |
| Table QA | 9,022 | 6,904,746 | 6.6 |
| Table QA Dialects | 25,650 | 17,040,666 | 16.3 |
| Image QA | 2,045 | 5,306,535 | 5.1 |
| Complete Queries | 1,536 | 1,613,671 | 1.5 |
| Critical Treatment | 2,190 | 5,361,262 | 5.1 |
| General SFT Diverse | 28,993 | 34,923,017 | 33.3 |
| Retriever Train | 9,231 | 73,865,004 | 70.4 |
| **TOTAL (unique files)** | **158,764** | **233,648,560** | **~222.8** |

---

### 1.2 External Knowledge Nodes: `E:\CSE498R\Agri-LLM\KrishokTech\agritrust knowledge nodes`

| File | Items/Lines | Size (bytes) | SHA-256 |
|------|------------|-------------|---------|
| `master/knowledge_nodes.json` | 2,120 items (145,623 lines) | 9,157,705 | `95A4CB55B6575FF951BBDA0DFDEC49AE8E3796CE586456A6B14EA96AED695F62` |
| `image_nodes/image_nodes_high_quality.jsonl` | 1,022 lines | 5,808,249 | `AF1B06E81F2910044E5F49E989DE8902FD7D4EEAEB05607B39CF7B81D5034A7B` |
| `image_nodes/image_nodes.json` | — | 6,492,604 | `EAA630423C03A1AD3F470C11841A13365D8AF3A1834CD56A524D987E6897E689` |
| `image_nodes/image_nodes_stats.json` | — | 1,376 | `5149944B3D9B456C684C74B0F674DDDBC97D849731E53A13D73BEF10DF7AEC54` |

**Institutions with source nodes:** BARC, BARI, BRRI_IRRI, BSRTI, CABI, CDB, DAE, DLS, DoF, MoA_NARS_SRDI, WorldFish

---

### 1.3 In-Repo Datasets: `D:\KrishokTech Advisory System\backend\ml_assets\`

| File | Lines/Items | Size (bytes) | SHA-256 | Schema |
|------|------------|-------------|---------|--------|
| `rag_index/raw/knowledge_nodes.json` | 2,120 items (145,623 lines) | 9,157,705 | `95A4CB55B6575FF951BBDA0DFDEC49AE8E3796CE586456A6B14EA96AED695F62` | JSON array of objects: `category`, `title_bn`, `title_en`, `content_bn`, `content_en`, `tags[]`, `source`, `publisher`, `section_title` |
| `rag_index/processed/knowledge_nodes_clean.jsonl` | 2,135 lines | 12,571,594 | `0A5FC281384EDD212395EA46C59AEBAD29C251899B3A8A035915577D73671BC2` | `id`, `category`, `title_bn`, `title_en`, `content_bn`, `content_en`, `summary`, `tags[]`, `source_document`, `publisher`, `citation`, `section_title`, `bm25_text`, `embed_text` |
| `rag_index/processed/knowledge_nodes_refined.jsonl` | 2,079 lines | 10,436,470 | `4D48B60C040199452A2C82B62F0E4FDD362CF21364B49E753EF94EDF2EC2425F` | `id`, `category`, `title_bn`, `title_en`, `summary`, `natural_intro_bn`, `content_bn`, `content_en`, `tags[]`, `source_document`, `publisher`, `citation`, `section_title`, `bm25_text`, `embed_text` |
| `rag_index/eval/farmer_benchmark_1000.jsonl` | 1,000 lines | 5,648,266 | `E2ADC30D69AED9DEE1D1B3F5F0EBF7584861B1DF9C687B1B32812B6215A7B7AA` | Same as external `farmers_benchmark_1000.jsonl` |
| `rag_index/eval/quality_summary.json` | 31 lines | 5,121 | `3A978362C1F9F6BD25370CDA10443FB05D13DF9AF68445862832F575AE0F3D7A` | `timestamp`, `nodes_evaluated=5`, `dimension_averages{6 dims}`, `overall_average=8.632`, `pass_rate=1.0`, `pass_count=5`, `fail_count=0`, `critical_issues[]` |
| `rag_index/eval/quality_spot_check.jsonl` | 5 lines | 9,130 | `B3D5AED4C4424FE710D223BB109B63CDB837E125C821348ED4AEF4DD5DBC1001` | `node_id`, `scores{6 dims}`, `overall_score`, `critical_issues[]`, `positive_points[]`, `verdict`, `timestamp` |
| `advisory/disease_knowledge_map.json` | 34 keys | 16,443 | `C31B972C55D741870E9E4C1384E95E45192CB6ECF23204B813AB7326EAB05F5C` | JSON object, keys like `Rice__Bacterial_Leaf_Blight`, values: `crop`, `disease_name`, `category` |
| `advisory/generated_knowledge_nodes.jsonl` | 13 lines | 205,847 | `CC177AE634B60663E408A38822627B45EE375FEDC19F7A73355C179631B04092` | `id`, `category=disease`, `title_bn`, `title_en`, `content_bn`, `content_en`, `summary`, `tags[]`, `source_document`, `publisher`, `citation`, `section_title`, `bm25_text`, `embed_text` |
| `advisory/generation_tasks.json` | — | 70,062 | `69A6EA8D53F08A83C9369607B4543B37C63C6022B68D74F65F382B028D9F835D` | Task definitions for knowledge generation |

---

### 1.4 Cross-File Duplicate Analysis

| External File | In-Repo File | SHA-256 Match | Status |
|---------------|-------------|---------------|--------|
| `farmers_benchmark/farmer_benchmark_1000.jsonl` | `rag_index/eval/farmer_benchmark_1000.jsonl` | `E2ADC30D...` = `E2ADC30D...` | **IDENTICAL** |
| `agritrust knowledge nodes/master/knowledge_nodes.json` | `rag_index/raw/knowledge_nodes.json` | `95A4CB55...` = `95A4CB55...` | **IDENTICAL** |

**Cross-reference notes:**
- `markdown_corpus/qa/general_sft_diverse_full.jsonl` (28,993 lines) and `text_qa/general/general_full.jsonl` (28,993 lines) have the same line count but different SHA-256 hashes (`D8A32C3A...` vs `6EE95FE9...`). They share the same schema but differ in content — the general_sft version lacks `node_id` and `node_file` fields present in the text_qa version.
- `complete_queries.jsonl` (1,536 lines) is the source for T4 slot-expansion queries referenced in `safety_requery_t4.jsonl`.
- `critical_treatment.jsonl` (2,190 lines) contains safety-tier="critical" treatment records, a subset relevant to the safety pipeline.

---

## 2. T03 — RAG Index, Model, and Eval Artifact Inventory

### 2.1 RAG Index Files

| File | Size (bytes) | SHA-256 | Description |
|------|-------------|---------|-------------|
| `rag_index/indexes/bm25_index.pkl` | 17,013,819 | `2AB484ACA38B694937A92A4A27BB2779C9E2FFB89F397D3FA168F7CA19E836C5` | BM25Okapi sparse retrieval index (k1=2.2, b=0.4) |
| `rag_index/indexes/bm25_corpus_tok.pkl` | 4,685,526 | `23C137071266C09532E6B6B73D3E8297CECF21CC465CF279CC8CCDD0DC45397E` | Tokenized corpus for BM25 index |
| `rag_index/manifest.json` | 2,194 | `11884B2BEC2D7023CE7E4543AE2B50EC045BEE1AB12A79523FB9F9BC6B28FF2E` | RAG database manifest |

**manifest.json key fields:**
- `version`: "1.0.0"
- `created`: "2026-08-08"
- `corpus.total_nodes`: 2,120
- `retrieval.bm25.variant`: "BM25Okapi", `k1`: 2.2, `b`: 0.4
- `retrieval.dense.model`: "intfloat/multilingual-e5-small", `dimension`: 384
- `retrieval.dense.file`: "indexes/embeddings.npy" (declared in manifest)
- `retrieval.faiss.type`: "IndexFlatIP"
- `retrieval.faiss.file`: "indexes/nodes.faiss" (declared in manifest)
- `retrieval.fusion.method`: "RRF", `k`: 20, `candidate_depth`: 50
- `refinement.model`: "gemini-3.1-flash-lite"

**FAISS/Dense index status: DECLARED BUT NOT BUILT.** The manifest references `indexes/embeddings.npy` and `indexes/nodes.faiss`, but these files do NOT exist on disk. Only BM25 index files are present.

### 2.2 Vision Models

| Model | File | Size (bytes) | SHA-256 | Classes | Task |
|-------|------|-------------|---------|---------|------|
| Crop Classifier | `vision/crop_classifier/model.pt` | 12,545,559 | `6F14484768E54F28C2EDC2C5D3858C2C1A57F18D7DE40A001A119CBC04240C94` | 6 | classify |
| Rice Disease | `vision/rice_disease/model.pt` | 3,205,243 | `F25243959A3D7DD0851F4D2E53E30890515CADD5E318871FFE04C0413865D61A` | 8 | classify |
| Wheat Disease | `vision/wheat_disease/model.pt` | 9,437,091 | `F4C6D2FA835744B2CAB4392275556B918171CCE61F04A058497E6DBE9965C7F3` | 11 | classify |
| Potato Disease | `vision/potato_disease/model.pt` | 11,032,834 | `D57B961EBF78280C03EBD9FF25CB414A2A2151A50EEC584D4FA9168BB56B6698` | 3 | classify |
| Corn Disease | `vision/corn_disease/model.pt` | 11,030,843 | `A5B92794445299BCB81FBACF664D7AC0478298E993E1F6B99230C6A01486D7A0` | 4 | classify |
| Brassica Disease | `vision/brassica_disease/model.pt` | 11,049,979 | `C3632475083492BE7F1D6DB5601ED9CD44F1A3FECBC74D8419D4A738B83CF99E` | 11 | classify |

**Total vision model size:** ~57.3 MB (6 models)

#### 2.2.1 Class Names

**Crop Classifier (6 classes):**
```
0: Brassica, 1: Corn, 2: GourdGuava, 3: Potato, 4: Solanacea, 5: Wheat
```

**Rice Disease (8 classes):**
```
0: Rice__Bacterial_Leaf_Blight, 1: Rice__Brown_Spot, 2: Rice__Healthy_Leaf,
3: Rice__Leaf_Blast, 4: Rice__Leaf_Scald, 5: Rice__Narrow_Brown_Leaf_Spot,
6: Rice__Rice_Hispa, 7: Rice__Sheath_Blight
```

**Wheat Disease (11 classes):**
```
0: BlackPoint, 1: Blast, 2: FusariumFootRot, 3: Healthy, 4: HealthyLeaf,
5: Leaf Rust, 6: LeafBlight, 7: Powdery Mildew, 8: Stem Rust, 9: Stripe Rust, 10: WheatBlast
```

**Potato Disease (3 classes):**
```
0: Potato__Early_Blight, 1: Potato__Healthy_Leaf, 2: Potato__Late_Blight
```

**Corn Disease (4 classes):**
```
0: Common_Rust, 1: Gray_Leaf_Spot, 2: Healthy, 3: Northern_Leaf_Blight
```

**Brassica Disease (11 classes):**
```
0: Cabbage__Alternaria_Spot, 1: Cabbage__Black_Rot, 2: Cabbage__Downy_Mildew,
3: Cabbage__Healthy_Leaf, 4: Cauliflower__Alternaria_Disease,
5: Cauliflower__Bacterial_Soft_Rot, 6: Cauliflower__Bacterial_Spot,
7: Cauliflower__Black_Spot, 8: Cauliflower__Downy_Mildew,
9: Cauliflower__Healthy, 10: Cauliflower__Nutrient_Deficiency
```

#### 2.2.2 Verification Report

**File:** `vision/verification_report.json` (6,573 bytes, SHA: `9E7E53480156F8F976036C44743D6B63E99DE5AE46E7F41A838598D82B7DFB5A`)

**Key fields per model:** `name`, `classes[]`, `task`, `model_size_mb`, `predictions[{image, predicted_class, confidence, top3[]}]`

**Prediction results summary:**
| Model | Sample Predictions | Avg Confidence |
|-------|-------------------|----------------|
| crop_classifier | 3 images | 0.9895 |
| rice_disease | 2 images | 1.0000 |
| wheat_disease | 0 images | — |
| corn_disease | 0 images | — |
| potato_disease | 2 images | 0.9882 |
| brassica_disease | 3 images | 0.9999 |

**Critical note:** wheat_disease and corn_disease have empty prediction arrays in the verification report — no sample inference was run for these models.

#### 2.2.3 Wheat Disease Metadata

**File:** `vision/wheat_disease/metadata.json` (704 bytes, SHA: `A82B0E09F8B6B529047715B4ADF90903048FC6B87CC5A7DBA926D32B0E53AC10`)

Key fields:
- `model_name`: "wheat-disease"
- `version`: "2.0.0"
- `framework`: "ultralytics-yolo11"
- `task`: "classify"
- `source`: "WheatBest.pt (wheatBT.zip from user downloads, 2026-08-08)"
- `replaced.previous`: "fake placeholder (byte-identical copy of crop_classifier, 12,545,559 bytes)"
- `replaced.reason`: "verified fake via byte-identical size; real model is 9,437,091 bytes with 11 genuine wheat classes"
- `input_size`: [640, 640]
- `test_images`: "test_images/wheat_disease/ (800 images, 11 classes)"

### 2.3 Gemma LoRA Checkpoint

**Location:** `backend/ml_assets/gemma/raw/checkpoint-4020/`

| File | Size (bytes) | SHA-256 | Description |
|------|-------------|---------|-------------|
| `adapter_model.safetensors` | 279,129,344 | `72357C2210198128DF3E208540AD48F0AF07607E9CF64F264507D9AA99DE13CA` | LoRA adapter weights |
| `adapter_config.json` | 1,487 | `F06FFE643D5850F12102F58F6305AEDA55814D40808698BDB96E763773C9F85A` | Adapter configuration |
| `tokenizer.json` | 32,169,880 | `435198DD84A7FA659300AF3E5C30918FB6ACAAF3365D6398B67AB87D1EB36288` | Tokenizer |
| `tokenizer_config.json` | 6,893 | `38205DDFA2AEEA37D4944E0CD5451C510A6A0DCD2A65AC627BB69066E03444B0` | Tokenizer config |
| `trainer_state.json` | 76,348 | `2AFBDCE9D72B8C39C5F32BDAC79F2FAEA60E44B8A85A95F06B02746E400C45EE` | Training state |
| `processor_config.json` | 1,689 | `32BDF45D2AD4CC29A0822DDD157A182DE76644F0419A6228D151495256E9813C` | Processor config |

**adapter_config.json key fields:**
- `base_model_name_or_path`: "unsloth/gemma-4-E4B-it-unsloth-bnb-4bit"
- `peft_type`: "LORA"
- `r`: 32
- `lora_alpha`: 64
- `lora_dropout`: 0
- `bias`: "none"
- `task_type`: "CAUSAL_LM"
- `peft_version`: "0.19.1"
- `auto_mapping.base_model_class`: "Gemma4ForConditionalGeneration"
- `auto_mapping.parent_library`: "transformers.models.gemma4.modeling_gemma4"
- `auto_mapping.unsloth_fixed`: true

**Total checkpoint size:** ~311.5 MB (including tokenizer, optimizer, scheduler)

### 2.4 Eval Files

| File | Lines | Size (bytes) | SHA-256 | Content |
|------|-------|-------------|---------|---------|
| `rag_index/eval/quality_summary.json` | 31 | 5,121 | `3A978362C1F9F6BD25370CDA10443FB05D13DF9AF68445862832F575AE0F3D7A` | Aggregate quality scores across 5 evaluated nodes |
| `rag_index/eval/quality_spot_check.jsonl` | 5 | 9,130 | `B3D5AED4C4424FE710D223BB109B63CDB837E125C821348ED4AEF4DD5DBC1001` | Per-node quality scores with detailed feedback |
| `rag_index/eval/farmer_benchmark_1000.jsonl` | 1,000 | 5,648,266 | `E2ADC30D69AED9DEE1D1B3F5F0EBF7584861B1DF9C687B1B32812B6215A7B7AA` | Farmer benchmark evaluation data |

**quality_summary.json key metrics:**
- `nodes_evaluated`: 5
- `overall_average`: 8.632 / 10
- `pass_rate`: 1.0 (100%)
- `pass_count`: 5, `fail_count`: 0
- `dimension_averages`: factual_accuracy=8.4, completeness=7.2, language_quality=9.4, organization=9.4, safety=8.6, no_hallucination=9.0
- `critical_issues`: 13 Bengali-language issues (missing dosage specifics, pH recommendations, environmental safety notes)

**quality_spot_check.jsonl verdicts:** All 5 nodes passed (verdict: "pass")

**Node IDs evaluated:** B4_DAEEXT_FC7E3C_001, B5_BARCAG_84A95A_003, B4_FRG2024_BF2CDE_002, B8_FERT2018_D38E0F_003, B6_DOC_ABCC5F_001

---

## 3. Summary Table of All Artifacts

### 3.1 In-Repo Artifacts

| Path | Type | Size (bytes) | SHA-256 | Status |
|------|------|-------------|---------|--------|
| `ml_assets/rag_index/indexes/bm25_index.pkl` | Pickle | 17,013,819 | `2AB484AC...` | Present |
| `ml_assets/rag_index/indexes/bm25_corpus_tok.pkl` | Pickle | 4,685,526 | `23C13707...` | Present |
| `ml_assets/rag_index/manifest.json` | JSON | 2,194 | `11884B2B...` | Present |
| `ml_assets/rag_index/raw/knowledge_nodes.json` | JSON | 9,157,705 | `95A4CB55...` | Present |
| `ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl` | JSONL | 12,571,594 | `0A5FC281...` | Present |
| `ml_assets/rag_index/processed/knowledge_nodes_refined.jsonl` | JSONL | 10,436,470 | `4D48B60C...` | Present |
| `ml_assets/rag_index/eval/farmer_benchmark_1000.jsonl` | JSONL | 5,648,266 | `E2ADC30D...` | Present |
| `ml_assets/rag_index/eval/quality_summary.json` | JSON | 5,121 | `3A978362...` | Present |
| `ml_assets/rag_index/eval/quality_spot_check.jsonl` | JSONL | 9,130 | `B3D5AED4...` | Present |
| `ml_assets/vision/crop_classifier/model.pt` | PyTorch | 12,545,559 | `6F144847...` | Present |
| `ml_assets/vision/rice_disease/model.pt` | PyTorch | 3,205,243 | `F2524395...` | Present |
| `ml_assets/vision/wheat_disease/model.pt` | PyTorch | 9,437,091 | `F4C6D2FA...` | Present |
| `ml_assets/vision/potato_disease/model.pt` | PyTorch | 11,032,834 | `D57B961E...` | Present |
| `ml_assets/vision/corn_disease/model.pt` | PyTorch | 11,030,843 | `A5B92794...` | Present |
| `ml_assets/vision/brassica_disease/model.pt` | PyTorch | 11,049,979 | `C3632475...` | Present |
| `ml_assets/vision/verification_report.json` | JSON | 6,573 | `9E7E5348...` | Present |
| `ml_assets/gemma/raw/checkpoint-4020/adapter_model.safetensors` | SafeTensors | 279,129,344 | `72357C22...` | Present |
| `ml_assets/gemma/raw/checkpoint-4020/adapter_config.json` | JSON | 1,487 | `F06FFE64...` | Present |
| `ml_assets/advisory/disease_knowledge_map.json` | JSON | 16,443 | `C31B972C...` | Present |
| `ml_assets/advisory/generated_knowledge_nodes.jsonl` | JSONL | 205,847 | `CC177AE6...` | Present |

### 3.2 External Artifacts (counted/verified)

| Path | Type | Records | Size (bytes) | SHA-256 |
|------|------|---------|-------------|---------|
| `krishoktech_dataset_main/farmers_benchmark/farmer_benchmark_1000.jsonl` | JSONL | 1,000 | 5,648,266 | `E2ADC30D...` |
| `krishoktech_dataset_main/farmers_benchmark/splits/test.jsonl` | JSONL | 350 | 2,122,297 | `69CE51E7...` |
| `krishoktech_dataset_main/text_qa/safety/safety_refusal_t3.jsonl` | JSONL | 3,216 | 3,636,107 | `27ACDB64...` |
| `krishoktech_dataset_main/text_qa/safety/safety_requery_t4.jsonl` | JSONL | 16,896 | 15,854,076 | `A5780234...` |
| `krishoktech_dataset_main/text_qa/general/general_full.jsonl` | JSONL | 28,993 | 40,490,278 | `6EE95FE9...` |
| `krishoktech_dataset_main/text_qa/treatment/treatment_full.jsonl` | JSONL | 11,224 | 22,026,143 | `DC9B87A0...` |
| `krishoktech_dataset_main/table_qa/qa/tableqa_all.jsonl` | JSONL | 9,022 | 6,904,746 | `26E3A9F6...` |
| `krishoktech_dataset_main/table_qa/qa/dialects/tableqa_all_dialects.jsonl` | JSONL | 25,650 | 17,040,666 | `BA8362AD...` |
| `krishoktech_dataset_main/image_qa/image_qa_pairs.jsonl` | JSONL | 2,045 | 5,306,535 | `5829D1A5...` |
| `krishoktech_dataset_main/markdown_corpus/qa/complete_queries.jsonl` | JSONL | 1,536 | 1,613,671 | `073C83AA...` |
| `krishoktech_dataset_main/markdown_corpus/qa/critical_treatment.jsonl` | JSONL | 2,190 | 5,361,262 | `414D17F5...` |
| `krishoktech_dataset_main/markdown_corpus/qa/general_sft_diverse_full.jsonl` | JSONL | 28,993 | 34,923,017 | `D8A32C3A...` |
| `krishoktech_dataset_main/markdown_corpus/retriever/retriever_train.jsonl` | JSONL | 9,231 | 73,865,004 | `5A8FF2E4...` |
| `agritrust knowledge nodes/master/knowledge_nodes.json` | JSON | 2,120 | 9,157,705 | `95A4CB55...` |
| `agritrust knowledge nodes/image_nodes/image_nodes_high_quality.jsonl` | JSONL | 1,022 | 5,808,249 | `AF1B06E8...` |

---

## 4. Missing Artifacts

### 4.1 In-Repo

| Artifact | Referenced In | Status |
|----------|--------------|--------|
| `rag_index/indexes/embeddings.npy` | `manifest.json` `retrieval.dense.file` | **NOT FOUND** — Dense embedding index not built |
| `rag_index/indexes/nodes.faiss` | `manifest.json` `retrieval.faiss.file` | **NOT FOUND** — FAISS index not built |
| `rag_index/bm25_build_report.json` | Task specification | **NOT FOUND** — Build report missing |
| `dataset_release/` | CLAUDE.md session summary | **NOT FOUND** at `D:\KrishokTech Advisory System\` |
| Embedding model weights | Manifest declares `intfloat/multilingual-e5-small` | **NOT FOUND** — No local embedding model files |

### 4.2 External

| Artifact | Referenced In | Status |
|----------|--------------|--------|
| `image_nodes/image_nodes_high_quality.jsonl` at `krishoktech_dataset_main/` | Task specification | **NOT FOUND** — Only exists at `agritrust knowledge nodes/image_nodes/` |
| `farmers_benchmark/splits/train.jsonl` | Split convention | **NOT FOUND** — Only `test.jsonl` split exists |

### 4.3 Gemma Checkpoint

| Artifact | Status |
|----------|--------|
| `optimizer.pt` | Present (size not computed — binary, large) |
| `scheduler.pt` | Present |
| `rng_state.pth` | Present |
| `training_args.bin` | Present |
| `chat_template.jinja` | Present |
| `README.md` | Present |

---

## 5. Cross-Reference: External to In-Repo Mapping

| External Source | In-Repo Copy | Relationship |
|-----------------|-------------|--------------|
| `krishoktech_dataset_main/farmers_benchmark/farmer_benchmark_1000.jsonl` | `ml_assets/rag_index/eval/farmer_benchmark_1000.jsonl` | **Bit-identical** (SHA match) |
| `agritrust knowledge nodes/master/knowledge_nodes.json` | `ml_assets/rag_index/raw/knowledge_nodes.json` | **Bit-identical** (SHA match) |
| `krishoktech_dataset_main/text_qa/general/general_full.jsonl` | `ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl` | **Different** — different schemas, different content. general_full has 28,993 QA pairs; clean nodes have 2,135 knowledge nodes. |
| `krishoktech_dataset_main/markdown_corpus/qa/general_sft_diverse_full.jsonl` | `ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl` | **Different** — same line count (28,993 vs 2,135) is coincidental; different file types (QA pairs vs knowledge nodes) |
| `krishoktech_dataset_main/markdown_corpus/qa/complete_queries.jsonl` | `ml_assets/advisory/generated_knowledge_nodes.jsonl` | **Different** — complete_queries (1,536) are T4 slot queries; generated_knowledge_nodes (13) are disease knowledge nodes |
| `krishoktech_dataset_main/markdown_corpus/qa/critical_treatment.jsonl` | `ml_assets/advisory/disease_knowledge_map.json` | **Different** — critical_treatment has 2,190 QA pairs; disease_knowledge_map has 34 disease entries. Complementary. |

**Key insight:** Only 2 files are true bit-identical copies between external and in-repo. The in-repo files are processed/refined derivatives of the external source data, not raw copies.

---

*End of report.*
