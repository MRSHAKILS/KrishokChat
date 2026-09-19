# Human Reviewer Package — KrishokChat 200 Farmer Queries

**Target Limitation:**  
`| 9 | Single-reviewer labels (200 crop slots) + autopsies | Disclosed | Second human pass listed as upgrade path; hazard numbers labeled single-reviewer. |`

This directory provides the complete independent double-blind evaluation setup for a **second human reviewer** to annotate all 200 authentic Bengali farmer queries, allowing computation of **inter-annotator agreement (Cohen's Kappa $\kappa$)** and production of a dual-reviewed consensus gold standard.

---

## 📁 Package Structure

```
human_annotation_gate_200/
├── ANNOTATION_GUIDELINES.pdf          # 📄 High-res printable 4-page PDF with full rules, samples, and tables
├── ANNOTATION_GUIDELINES.md          # 📖 Markdown protocol: definitions, taxonomy, & worked samples
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
│   ├── build_guidelines_pdf.py       # 🖨️ Script that generates the styled 4-page guidelines PDF
│   └── evaluate_dual_review.py      # 📈 Automated Cohen's Kappa, agreement, and autopsy runner
└── reference_ground_truth/
    └── reviewer_1_labels_sealed.json # 🔒 Sealed Reviewer 1 ground truth (strictly isolated from annotators)
```

---

## 🚀 Quick Start for Annotators

1. **Read the Protocol:** Open and read [`ANNOTATION_GUIDELINES.pdf`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/ANNOTATION_GUIDELINES.pdf) (or [`ANNOTATION_GUIDELINES.md`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/ANNOTATION_GUIDELINES.md)) to familiarize yourself with the 37 controlled crop options, the 6 intent definitions, and the worked boundary samples.
2. **Choose Your Annotation Mode:**
   - **Mode A (Recommended — Modular Batches):** Open each file in [`batches/`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/batches) (20 queries per file, ~10-15 minutes per batch).
   - **Mode B (Single Master File):** Open [`master_blind_sheet_200.xlsx`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/master_blind_sheet_200.xlsx) and fill in either the `All 200 Queries` sheet or the individual batch tabs.
3. **Fill the Input Columns (Columns E to J):**
   - **Col E (`Crop Name` / বাংলায় ফসলের নাম):** Name of the crop in Bangla (e.g., `ধান`, `আলু`, `টমেটো`), or leave blank if no crop is stated.
   - **Col F (`Crop Taxonomy` / English):** English standardized name (`rice`, `potato`, `wheat`, `chilli`, `brinjal`, etc.).
   - **Col G (`Is Crop Specified?`):** Select `YES` or `NO` from the dropdown menu.
   - **Col H (`Intent Category`):** Select from the dropdown menu (`Treatment`, `Fertilizer`, `Prevention`, `General`, `Crisis`, `Off-Topic`).
   - **Col I (`Confidence`):** Select `High`, `Medium`, or `Low`.
   - **Col J (`Reviewer Notes`):** Optional comments explaining colloquial terms or nuances.
4. **Save the File(s).**

---

## 📊 Evaluation Runners & Multi-Reviewer Results

Both external annotator sets are preserved in `batches/`:
- `batches/reviewer 1 response/`: 10 CSV files (20 queries each) completed by External Annotator 1.
- `batches/reviewer 2 response/`: 10 XLSX files (20 queries each) completed by External Annotator 2.
- `reference_ground_truth/reviewer_1_labels_sealed.json`: Sealed initial baseline reference.

To run the complete multi-reviewer evaluation pipeline:

```bash
cd "D:\KrishokChat Advisory System\paper\EACL Final\experiments\human_annotation_gate_200"
python scripts/evaluate_all_reviewers.py
```

### Empirical Results (N = 200 authentic farmer queries):

1. **Independent External Reviewers (Reviewer 1 vs. Reviewer 2):**
   - **Binary Crop Ambiguity (`Is Crop Specified?`):** **100.00%** agreement ($200/200$, Cohen's $\kappa = \mathbf{1.0000}$, Perfect Agreement).
   - **Controlled Crop Taxonomy (37 classes):** **99.50%** agreement ($199/200$, Cohen's $\kappa = \mathbf{0.9945}$, Near-Perfect Agreement).  
     *(Single edge-case difference: `farmer_q_848` on pomelo/বাতাবি লেবু mapped to `lemon` [citrus] vs `other_crop`).*
   - **Query Intent Category:** **93.50%** agreement ($187/200$, Cohen's $\kappa = \mathbf{0.8958}$).
   - **High-Confidence Rates:** 91.0% (R1) and 92.5% (R2).

2. **Tri-Annotator Consensus (External R1 + External R2 + Sealed Baseline R0):**
   - **Fleiss' Multi-Rater Kappa (Binary Presence):** $\mathbf{0.8954}$ (Substantial / Near-Perfect Reliability).
   - **Unanimous 3-Way Binary Agreement:** $189 / 200$ (**94.50%**).
   - **Unanimous 3-Way Taxonomy Agreement:** $188 / 200$ (**94.00%**).
   - **Majority 2-to-1 Consensus:** $200 / 200$ (**100.00%**).

3. **Outputs & Adjudication Artifacts:**
   - [`consensus_gold_200.json`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/consensus_gold_200.json): Full 200-row consensus gold dataset with all 3 raters, confidence scores, notes, and adjudication verdicts.
   - [`dual_review_report.json`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/dual_review_report.json) / [`multi_reviewer_evaluation_report.json`](file:///D:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/human_annotation_gate_200/multi_reviewer_evaluation_report.json): Complete machine-readable audit report.
