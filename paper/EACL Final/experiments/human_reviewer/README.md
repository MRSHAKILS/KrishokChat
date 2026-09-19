# Human Reviewer Package — KrishokChat 200 Farmer Queries

**Target Limitation:**  
`| 9 | Single-reviewer labels (200 crop slots) + autopsies | Disclosed | Second human pass listed as upgrade path; hazard numbers labeled single-reviewer. |`

This directory provides the complete independent double-blind evaluation setup for a **second human reviewer** to annotate all 200 authentic Bengali farmer queries, allowing computation of **inter-annotator agreement (Cohen's Kappa $\kappa$)** and production of a dual-reviewed consensus gold standard.

---

## 📁 Package Structure

```
human_reviewer/
├── ANNOTATION_GUIDELINES.md          # 📖 Step-by-step annotation rules, taxonomy, and examples
├── README.md                         # 🧭 This manifest & quick start guide
├── master_blind_sheet_200.xlsx       # 📊 All 200 queries in a single multi-tab workbook
├── batches/                          # 📂 10 modular workbooks (20 queries each) for easy distribution
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
│   ├── build_annotation_sheets.py    # ⚙️ Script that formatted and generated all Excel sheets
│   └── evaluate_dual_review.py      # 📈 Automated Cohen's Kappa, agreement, and autopsy runner
└── reference_ground_truth/
    └── reviewer_1_labels_sealed.json # 🔒 Sealed Reviewer 1 ground truth (strictly isolated from annotators)
```

---

## 🚀 Quick Start for Annotators

1. **Read the Protocol:** Read [`ANNOTATION_GUIDELINES.md`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_reviewer/ANNOTATION_GUIDELINES.md) first to familiarize yourself with the crop vocabulary and intent categories.
2. **Choose Your Annotation Mode:**
   - **Mode A (Recommended — Modular Batches):** Open each file in [`batches/`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_reviewer/batches) (20 queries per file, ~10-15 minutes per batch).
   - **Mode B (Single Master File):** Open [`master_blind_sheet_200.xlsx`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_reviewer/master_blind_sheet_200.xlsx) and fill in either the `All 200 Queries` sheet or the individual batch tabs.
3. **Fill the Input Columns (Columns E to J):**
   - **Col E (`Crop Name` / বাংলায় ফসলের নাম):** Name of the crop in Bangla (e.g., `ধান`, `আলু`, `টমেটো`), or leave blank if no crop is stated.
   - **Col F (`Crop Taxonomy` / English):** English standardized name (`rice`, `potato`, `wheat`, `chilli`, `brinjal`, etc.).
   - **Col G (`Is Crop Specified?`):** Select `YES` or `NO` from the dropdown menu.
   - **Col H (`Intent Category`):** Select from the dropdown menu (`Treatment`, `Fertilizer`, `Prevention`, `General`, `Crisis`, `Off-Topic`).
   - **Col I (`Confidence`):** Select `High`, `Medium`, or `Low`.
   - **Col J (`Reviewer Notes`):** Optional comments explaining colloquial terms or nuances.
4. **Save the File(s).**

---

## 📊 Computing Agreement & Kappa

Once the second reviewer has finished annotating the sheets, run the evaluation pipeline:

```bash
cd "D:\KrishokChat Advisory System\paper\EACL Final\experiments\human_reviewer\scripts"
python evaluate_dual_review.py
```

The script will automatically:
1. Scan `batches/*.xlsx` or `master_blind_sheet_200.xlsx`.
2. Extract Reviewer 2's annotations and match them with Reviewer 1's sealed ground truth.
3. Calculate:
   - **Binary Crop Ambiguity Agreement (%)** & **Cohen's Kappa ($\kappa$)**
   - **Exact Crop Taxonomy Agreement (%)** & **Cohen's Kappa ($\kappa$)**
   - **Discrepancy Count**
4. Output a detailed JSON discrepancy autopsy file (`dual_review_report.json`), ready for final consensus review and updating the paper text!
