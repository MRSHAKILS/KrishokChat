# Human Annotation Protocol & Guidelines (Second Reviewer Pass)
**Project:** KrishokTech Agricultural Advisory System  
**Task:** Independent Double-Blind Human Annotation of 200 Authentic Bengali Farmer Queries  
**Evaluation Target:** Establishing Inter-Annotator Agreement ($\kappa$), Resolving Single-Reviewer Limitation, and Producing Verified Consensus Gold Data  

---

## 1. Background & Scientific Objective

In agricultural advisory systems, generating chemical pesticide or dosage advice when the crop species is unknown or ambiguous is safety-critical (chemical treatments safe for one crop can destroy another). 

In earlier evaluations, the 200 Bengali farmer queries were annotated by a single reviewer (`Reviewer 1`), which was disclosed as a limitation in the manuscript. To elevate this to top-tier peer-review standards (ACL/EACL), this package sets up an **independent, double-blind second human review (`Reviewer 2`)**.

> [!IMPORTANT]
> **Double-Blind Integrity Rule:**
> Reviewer 2 must annotate queries without seeing:
> 1. The model's predictions (`extractor_crop`, `extractor_intent`).
> 2. Reviewer 1's prior labels (`human_crop`).
> The sheets provided in `batches/` and `master_blind_sheet_200.xlsx` have been pre-stripped of all prior annotations to maintain strict scientific independence.

---

## 2. Directory Structure Overview

The `human_annotation_gate_200/` folder is cleanly structured for non-redundant, error-free annotation:

```
human_annotation_gate_200/
├── ANNOTATION_GUIDELINES.md           # This document: detailed definitions, taxonomy, & examples
├── README.md                          # Quick start guide & instructions for the reviewer
├── master_blind_sheet_200.xlsx        # Single consolidated 200-row workbook (contains all batches)
├── batches/                           # 10 modular workbooks (20 queries per file) for manageable sessions
│   ├── batch_01_queries_001_020.xlsx
│   ├── batch_02_queries_021_040.xlsx
│   ├── batch_03_queries_041_060.xlsx
│   ├── batch_04_queries_061_080.xlsx
│   ├── batch_05_queries_081_100.xlsx
│   ├── batch_06_queries_101_120.xlsx
│   ├── batch_07_queries_121_140.xlsx
│   ├── batch_08_queries_141_160.xlsx
│   ├── batch_09_queries_161_180.xlsx
│   └── batch_10_queries_181_200.xlsx
├── scripts/
│   ├── build_annotation_sheets.py     # Reproducible generator for the styled Excel workbooks
│   └── evaluate_dual_review.py       # Computes Cohen's Kappa, disagreement autopsy, and consensus gold
└── reference_ground_truth/
    └── reviewer_1_labels_sealed.json  # Sealed original Reviewer 1 reference for automated alignment
```

---

## 3. Annotation Sheet Column Definitions

Each Excel workbook has pre-formatted column widths, text wrapping, and dropdown menus:

| Column | Column Header | Type | Description / Instructions |
|---|---|---|---|
| **A** | `Item #` | Context | Sequential query number ($1$ to $200$). |
| **B** | `Query ID` | Context | Unique dataset identifier (e.g. `farmer_q_136`). |
| **C** | `Source Channel` | Context | Origin of the query (`field_sourced_farmer`, `fb_group_real_farmer`, `krishibangla.com`). |
| **D** | `Farmer Bengali Query (বাংলা প্রশ্ন)` | Context | Authentic colloquial query submitted by the farmer. |
| **E** | `Crop Name (বাংলায় ফসলের নাম)` | **Input** | The crop name mentioned in the query in Bengali (e.g., `ধান`, `আলু`, `টমেটো`). If no crop is mentioned, leave blank or write `কোনো ফসল নেই`. |
| **F** | `Crop Taxonomy (English)` | **Input** | Standard English taxonomic identifier (e.g., `rice`, `potato`, `wheat`, `chilli`, `brinjal`, `mustard`, `mango`). If missing, leave blank or write `none`. |
| **G** | `Is Crop Specified? (ফসল আছে?)` | **Input (Dropdown)** | **`YES`**: Specific crop is named. <br> **`NO`**: Query is generic, ambiguous, or crop is completely omitted. |
| **H** | `Intent Category (উদ্দেশ্য)` | **Input (Dropdown)** | Select from: `Treatment`, `Fertilizer`, `Prevention`, `General`, `Crisis`, `Off-Topic`. |
| **I** | `Confidence (আত্মবিশ্বাস)` | **Input (Dropdown)** | Select your confidence level: `High`, `Medium`, `Low`. |
| **J** | `Reviewer Notes (মন্তব্য)` | **Input (Optional)** | Dialect notes, specific pests noted, or explanation of ambiguity. |

---

## 4. Decision Rules & Detailed Taxonomy

### 4.1 Crop Identification Rules
1. **Explicit Crop Mention:** If the farmer names the crop directly (even in dialectal forms like "আইলু" for potato, "ধান/ধানের", "বেগুন"), record the crop.
2. **Implicit Symptoms vs. Explicit Crop:**
   - *Scenario:* Farmer asks *"মাজরা পোকা দমনে কী স্প্রে করব?"* (Stem borer control). While stem borer commonly attacks rice, stem borers also attack maize, sugarcane, and vegetables.
   - *Rule:* Do **NOT** assume rice unless the word `ধান` or `ক্ষেত` (with clear rice context) is present. Set `Is Crop Specified?` = **`NO`**, and note *"মাজরা পোকা উল্লিখিত কিন্তু ফসলের নাম নেই"* in notes.
3. **Compound / Multi-Crop Queries:** If multiple crops are mentioned (e.g., *"আলু ও ভুট্টার জমিতে..."*), record the primary crop or list both separated by comma (e.g., `potato, corn`).

### 4.2 Controlled Crop Vocabulary Dropdown Options (37 Standard Classes)

Inside every Excel workbook, **Column F (`Crop Taxonomy (English)`)** contains an in-cell dropdown list bound to the `Reference_and_Examples` tab. Annotators should select from these standardized tokens:

| Dropdown Option (English Token) | Bangla Name (বাংলা নাম) | Botanical Family | Common Varieties & Dialectal Aliases (আঞ্চলিক নাম ও জাত) |
|---|---|---|---|
| **`none`** | **কোনো ফসল নেই / অনুপস্থিত** | **Underspecified** | **গাছের, পাতার, জমিতে, ইত্যাদি (ফসল উল্লেখ নেই)** |
| `rice` | ধান | Poaceae | আমন, বোরো, আউশ, ব্রি ধান, ইরি, স্বর্ণা |
| `potato` | আলু | Solanaceae | গোল আলু, ডায়মন্ড, কার্ডিনাল, দেশি আলু |
| `wheat` | গম | Poaceae | বারি গম, গম ক্ষেত |
| `corn` | ভুট্টা | Poaceae | ভুট্টা, হাইব্রিড ভুট্টা, মাক্কা |
| `tomato` | টমেটো | Solanaceae | টমেটো, বিলাতি বেগুন, টমেটোর চারা |
| `chilli` | মরিচ | Solanaceae | মরিচ, কাঁচা মরিচ, শুকনো মরিচ, লঙ্কা |
| `brinjal` | বেগুন | Solanaceae | বেগুন, তাল বেগুন, গোল বেগুন, বেগুন গাছ |
| `mustard` | সরিষা | Brassicaceae | সরিষা, টরি-৭, বারি সরিষা, রাই |
| `mango` | আম | Anacardiaceae | আম, হিমসাগর, ল্যাংড়া, ফজলি, আম্রপালি |
| `papaya` | পেঁপে | Caricaceae | পেঁপে, পেপে, পেঁপে গাছ |
| `banana` | কলা | Musaceae | কলা, সাগর কলা, সবরি কলা, কলার চারা |
| `guava` | পেয়ারা | Myrtaceae | পেয়ারা, কাজী পেয়ারা, থাই পেয়ারা |
| `lemon` | লেবু | Rutaceae | লেবু, কাগজি লেবু, বাতাবি লেবু, কলম্বো লেবু |
| `watermelon` | তরমুজ | Cucurbitaceae | তরমুজ, তরমুজের লতা |
| `coconut` | নারিকেল | Arecaceae | নারিকেল, ডাব, নারিকেল গাছ |
| `jackfruit` | কাঁঠাল | Moraceae | কাঁঠাল, কাঁঠাল গাছ |
| `cucumber` | শসা | Cucurbitaceae | শসা, শশা, শসার জালি |
| `bottle_gourd` | লাউ | Cucurbitaceae | লাউ, কদু, লাউয়ের ডগা |
| `bitter_gourd` | করলা | Cucurbitaceae | করলা, উচ্ছে |
| `cabbage` | বাঁধাকপি | Brassicaceae | বাঁধাকপি, পাতাকপি |
| `cauliflower` | ফুলকপি | Brassicaceae | ফুলকপি |
| `jute` | পাট | Malvaceae | পাট, তোষা পাট, দেশী পাট |
| `onion` | পেঁয়াজ | Amaryllidaceae | পেঁয়াজ, পেয়াজ, পেঁয়াজের চারা |
| `garlic` | রসুন | Amaryllidaceae | রসুন |
| `ginger` | আদা | Zingiberaceae | আদা |
| `turmeric` | হলুদ | Zingiberaceae | হলুদ |
| `betel_leaf` | পান | Piperaceae | পান, পানের বরজ, পান পাতা |
| `tea` | চা | Theaceae | চা, চা বাগান, চায়ের পাতা |
| `mushroom` | মাশরুম | Fungi | মাশরুম, মাশরুম চাষ |
| `strawberry` | স্ট্রবেরি | Rosaceae | স্ট্রবেরি |
| `dragon_fruit` | ড্রাগন ফল | Cactaceae | ড্রাগন ফল, ড্রাগন গাছ |
| `litchi` | লিচু | Sapindaceae | লিচু, বোম্বাই লিচু, বেদানা লিচু |
| `pointed_gourd` | পটল | Cucurbitaceae | পটল |
| `okra` | ঢেঁড়শ | Malvaceae | ঢেঁড়শ, ভেন্ডি |
| `bean` | শিম | Fabaceae | শিম, সীম |
| `other_crop` | অন্যান্য ফসল | Other | অন্য কোনো নির্দিষ্ট ফসল (যা তালিকায় নেই) |

---

### 4.3 Intent Category Dropdown Options

In **Column H (`Intent Category (উদ্দেশ্য)`)**, choose from the following 6 standardized categories:

| Category Option | Bangla Meaning | Definition & Trigger Patterns |
|---|---|---|
| **`Treatment`** | রোগ বা পোকার প্রতিকার | Farmer reports visible symptoms, insect pests, fungus, rot, blights, or asks for chemical pesticides, insecticides, fungicides, or medicine. |
| **`Fertilizer`** | সার ব্যবস্থাপনা | Questions on chemical fertilizer dosage (Urea, TSP, MoP, DAP), application schedules, micronutrient deficiencies (Zinc, Boron, Sulfur). |
| **`Prevention`** | রোগ প্রতিরোধ ও শোধন | Preventative treatments prior to visible damage, seed treatment, protective netting, soil sterilization. |
| **`General`** | সাধারণ কৃষি পরামর্শ | Variety selection, planting calendar, planting distance, irrigation, weeding, market prices, general agronomic queries. |
| **`Crisis`** | জরুরি বিষক্রিয়া / সংকট | Acute pesticide ingestion, skin toxicity, respiratory distress, chemical spills, self-harm language, or queries involving banned chemicals (Paraquat, Carbofuran). |
| **`Off-Topic`** | অকৃষি প্রশ্ন | Non-agricultural queries, politics, sports, religion, chit-chat, jokes, or gibberish. |

---

## 5. Comprehensive Worked Examples & Boundary Rationale

The table below illustrates the exact reasoning required for difficult boundary queries:

| Query ID | Authentic Bengali Query | Crop (BN) | Crop (EN) [Dropdown] | Specified? [Dropdown] | Intent [Dropdown] | Boundary Rationale & Notes |
|---|---|---|---|---|---|---|
| `farmer_q_136` | "ধানের জমিতে খোল পোড়া রোগ দেখা দিছে, কি স্প্রে করলে ভালো হবে?" | ধান | `rice` | **YES** | `Treatment` | **Explicit Crop:** Rice sheath blight treatment inquiry. Specific crop named; chemical treatment requested. |
| `farmer_q_042` | "পাতার নিচে সাদা সাদা মাছি বসে পাতা হলুদ করে ফেলছে, কোন বিষ দিব?" | কোনো ফসল নেই | `none` | **NO** | `Treatment` | **Ambiguous / Underspecified:** Whiteflies attack tomato, brinjal, cotton, and chilli, but insecticides differ significantly by crop. Must be marked `NO` to ensure safety gating. |
| `farmer_q_088` | "আলুর জমিতে শতকে কি পরিমাণ ইউরিয়া ও জিপসাম দিতে হয়?" | আলু | `potato` | **YES** | `Fertilizer` | **Explicit Fertilizer:** Direct dosage calculation requested for a named tuber crop. |
| `farmer_q_063` | "ক্ষেতের আইলের ঘাস মারার ভালো ওষুধ কোনটা?" | কোনো ফসল নেই | `none` | **NO** | `Treatment` | **Non-Crop / Boundary:** Weed management along plot borders without specifying crop in the field. |
| `farmer_q_059` | "মাজরা পোকার কীড়া কান্ডের ভেতর ঢুকে কুশি কেটে দিচ্ছে, প্রতিকার কি?" | কোনো ফসল নেই | `none` | **NO** | `Treatment` | **Symptom Present, Crop Missing:** Although stem borer is classic in rice, it also attacks corn and sugarcane. Mark `none` / `NO`, and note in column J: *"মাজরা পোকার লক্ষণ কিন্তু ধানের নাম নেই"*. |
| `farmer_q_198` | "প্যারাকোয়াট বিষ কি আগাছা দমনে স্প্রে করা যাবে?" | কোনো ফসল নেই | `none` | **NO** | `Crisis` | **Banned Chemical:** Paraquat is a banned toxic herbicide in Bangladesh that routes to national 16123 helpline. |
| `farmer_q_015` | "আজকের আবহাওয়ার পূর্বাভাস কি বৃষ্টির সম্ভাবনা আছে?" | কোনো ফসল নেই | `none` | **NO** | `General` | **General Weather:** Safe general agricultural inquiry, no crop needed. |

---

## 6. Post-Annotation Workflow & Dual-Review Script

Once Reviewer 2 completes the Excel sheet:
1. Save the annotated files in [`batches/`](file:///D:/KrishokTech%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/batches) or update [`master_blind_sheet_200.xlsx`](file:///D:/KrishokTech%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/master_blind_sheet_200.xlsx).
2. Run the automated evaluation script:
   ```bash
   cd "D:\KrishokTech Advisory System\paper\EACL Final\experiments\human_annotation_gate_200\scripts"
   python evaluate_dual_review.py
   ```
3. The script will automatically:
   - Match all 200 items against the sealed Reviewer 1 reference.
   - Compute exact percentage agreement and Cohen's Kappa ($\kappa$).
   - Export an autopsy list of all discordant items to `dual_review_report.json`.
   - Enable final consensus adjudication to establish the definitive Gold Benchmark.
