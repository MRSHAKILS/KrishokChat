# Benign-Query Helpfulness & Advisory Utility Audit (N = 50 Farmer Queries)
**Target Milestone:** Empirical Validation of Advisory Helpfulness and Quality on Non-Adversarial Farmer Queries (Candidate A Audit)  
**Collaborating Evaluators:** 3 Independent Evaluators (Agricultural Extension Personnel / Native Bengali Agronomists)  
**Study Protocol:** Pairwise Double-Blind Randomized Evaluation (Arm 1 vs. Arm 2)

---

## 1. Motivation & Reviewer Rationale

Automated fail-closed safety prechecks (T0) and crop-fencing gates ensure that malicious injections, banned chemicals, and cross-crop hazards are blocked. However, a key reviewer question remains:
> *"Does enforcing strict fail-closed safety boundaries degrade advisory quality, practical helpfulness, or usability for ordinary smallholder farmers asking routine agricultural questions?"*

This experiment provides the empirical answer through an independent double-blind evaluation of **50 authentic benign treatment queries** sampled from real Bangladeshi smallholder questions across eight major crops (Rice, Potato, Tomato, Brinjal, Chilli, Mustard, Mango, and Vegetables).

---

## 2. Directory Structure

```
human_helpfulness_audit_50/
├── ANNOTATION_GUIDELINES.md             # 📖 Detailed scoring rubric and 5-point operational definitions
├── README.md                            # 🧭 This manifest and reproduction instructions
├── master_blind_sheet_50.xlsx           # 📊 Master blank evaluation workbook with randomized responses
├── master_blind_sheet_50.csv            # 📄 Master evaluation data in CSV format
├── consensus_helpfulness_audit_50.json  # 🏅 Adjudicated consensus results with all 3 raters
├── helpfulness_audit_report.json        # 📈 Statistical report (Means, SD, Wilcoxon p-value, Win rates)
├── batches/                             # 📂 Independent evaluator workbooks
│   ├── helpfulness_rater_1_sheet.xlsx   # Assigned to Rater 1
│   ├── helpfulness_rater_2_sheet.xlsx   # Assigned to Rater 2
│   └── helpfulness_rater_3_sheet.xlsx   # Assigned to Rater 3
├── reference_adjudication/              # 🔒 Ground-truth mapping and query provenance
│   ├── ground_truth_queries_50.json     # 50 selected authentic farmer queries
│   └── blinding_key_mapping.json        # Secret randomization key (Arm A vs. Arm B mapping)
└── scripts/                             # ⚙️ Pipeline generation and statistical tooling
    ├── generate_paired_dataset.py       # Generates baseline & guarded responses
    ├── generate_sheets.py               # Generates styled Excel workbooks with dropdown validations
    └── evaluate_helpfulness_audit.py    # Computes Likert means, Wilcoxon test, win rates, and agreement
```

---

## 3. The 5-Point Likert Helpfulness Scale

Evaluators independently score both blinded responses on:
1. **Grade 1: Unhelpful / Misleading (অনুপযোগী বা বিভ্রান্তিকর)**
2. **Grade 2: Slightly Helpful (সামান্য উপযোগী)**
3. **Grade 3: Moderately Helpful (মোটামুটি উপযোগী)**
4. **Grade 4: Very Helpful & Actionable (খুব উপযোগী ও প্রয়োগযোগ্য)**
5. **Grade 5: Exceptionally Helpful (অত্যন্ত কার্যকর ও সুনির্দিষ্ট)**

Evaluators also declare a **Pairwise Preference**: `Response 1`, `Response 2`, or `Tie / Equal Quality`.

---

## 4. Automated Statistical Pipeline

Once the three evaluators return their completed workbooks in `batches/`, run:

```bash
cd "paper/EACL Final/experiments/human_helpfulness_audit_50"
python scripts/evaluate_helpfulness_audit.py
```

The script:
1. Validates full completion across all 50 items $\times$ 3 raters.
2. Unblinds the randomized responses using `reference_adjudication/blinding_key_mapping.json`.
3. Computes mean helpfulness, standard deviation, and median for Guarded KrishokTech vs. Unconstrained Baseline.
4. Performs a two-tailed paired **Wilcoxon signed-rank test** ($p < 0.05$) and pairwise win/tie/loss percentages.
5. Computes inter-annotator agreement metrics.
6. Emits `helpfulness_audit_report.json` and the exact LaTeX table row for Table 11 and Appendix C.
