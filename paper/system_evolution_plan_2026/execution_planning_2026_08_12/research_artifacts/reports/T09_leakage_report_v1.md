# T09 Leakage Report v1

- Tool: `check_leakage.py v2`
- Generated (UTC): 2026-08-12T19:13:47.640579+00:00
- **Intent-level leakage (exact/norm question across splits): False**

| Split pair | Check | Distinct texts | Records covered (A/B) |
|---|---|---|---|
| T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_dev_v1.jsonl | exact_answer | 1 | 7/7 |
| T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_dev_v1.jsonl | norm_answer | 1 | 15/7 |
| T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl | exact_answer | 3 | 412/126 |
| T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl | norm_answer | 3 | 412/126 |

Samples (up to 5 per check):

- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_dev_v1.jsonl` [exact_answer] in A=7 recs / B=7 recs: `মাটির উর্বরতা ও ফসলের চাহিদা অনুযায়ী সুষম সার প্রয়োগ।`
- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_dev_v1.jsonl` [norm_answer] in A=15 recs / B=7 recs: `মাটির উর্বরতা ও ফসলের চাহিদা অনুযায়ী সুষম সার প্রয়োগ।`
- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl` [exact_answer] in A=132 recs / B=26 recs: `Adverse Weather & Production-Increase Measures
পেঁয়াজ গাছ মূলত পত্রগুচ্ছ ও বোটার সমন্বয়ে গঠিত। জাত`
- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl` [exact_answer] in A=208 recs / B=10 recs: `Back Cover
তুলা ফসলে বিভিন্ন ক্ষতিকারক পোকার আক্রমণ যখন নির্দিষ্ট মাত্রায় পৌঁছায়, তখন তা দমনের জন্য `
- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl` [exact_answer] in A=72 recs / B=90 recs: `Climate, Soil & Production-Technology Overview
বারি মরিচ-২ একটি গ্রীষ্মকালীন উচ্চ ফলনশীল মরিচের জাত।`
- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl` [norm_answer] in A=132 recs / B=26 recs: `adverse weather & production-increase measures পেঁয়াজ গাছ মূলত পত্রগুচ্ছ ও বোটার সমন্বয়ে গঠিত। জাত`
- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl` [norm_answer] in A=208 recs / B=10 recs: `back cover তুলা ফসলে বিভিন্ন ক্ষতিকারক পোকার আক্রমণ যখন নির্দিষ্ট মাত্রায় পৌঁছায়, তখন তা দমনের জন্`
- `T09_treatment_qa_train_v1.jsonl vs T09_treatment_qa_test_v1.jsonl` [norm_answer] in A=72 recs / B=90 recs: `climate, soil & production-technology overview বারি মরিচ-২ একটি গ্রীষ্মকালীন উচ্চ ফলনশীল মরিচের জাত।`

Notes:
- Intent checks (exact/norm question) gate the split: any hit = STOP.
- Answer-templating matches are reported as a data-quality finding for expert sign-off.
- Same-group variants (qtype/dialect forms of one intent) are intentionally in one split.
