# Section 08: Results — Evidence Authority & Safety Verification (Draft Skeleton)

## 8.1 Relational Misbinding Attack Evaluation
- 10,000 adversarial multi-document misbinding cases (Layer E02).
- Lexical verifiers fail on 80.0% of cases; Citation verifiers fail on 61.8%; LLM Judge fails on 38.65%.
- 11-slot BAA achieves 100.0% detection rate [99.96%, 100.0%] (Table 6).

## 8.2 The 11-Slot Hazard Prevention Ablation
- Exhaustive single-slot ablation across 10k instances (Layer E03).
- Dosage bounds removal (+31.6% hazard), Regulatory polarity (+17.8%), Active ingredient (+14.2%), Crop (+11.4%), Pathogen (+8.2%), Volume (+7.1%), Formulation (+5.8%), Unit (+5.4%), Stage (+4.9%), PHI (+2.7%), Interval (+1.9%).
- Proves necessity of the full 11-slot schema.

## 8.3 Counterfactual Evidence Sensitivity
- Testing single-field mutations (dosage x2, PHI -3).
- BAA achieves 0.0% false certification rate on counterfactual edits vs 72.65% for unconstrained RAG (Layer E05).
