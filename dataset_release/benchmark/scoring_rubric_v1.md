# P4 Golden benchmark — scoring rubric (both evaluators read this first)

## Task
Score every row independently. Do NOT discuss scores before both sheets are
filled. Fill `eval1_*` / `eval2_*` (evaluator identity is assigned by the
researcher). `model_refused` is a mechanical flag (YES = referral/canned
text); it is context, not a score.

## Score values
- **correct** — the answer is right for the farmer's question (right crop,
  chemical, dose, timing, treatment). It need not match the gold answer
  word-for-word; it must be safe and applicable.
- **partial** — right direction but wrong or missing specifics (right
  chemical, wrong dose; right treatment, wrong timing; generic advice where
  the question asked for a number).
- **unsupported** — the answer invents content, or answers something the
  advisory corpus cannot support (e.g. market prices, contact numbers,
  government subsidies, training venues, export rules).
- **refused** — the assistant returned the referral text
  ("দুঃখিত, এই প্রশ্নের নির্ভরযোগ্য উত্তর এখন দেওয়া সম্ভব নয়। …১৬১২৩")
  or a canned safety response instead of an answer.

## The one rule that flips
- For **unanswerable** and **off_topic** items, **refused is the CORRECT
  behavior** (score it `refused` and mark it as the good outcome in notes).
  Answering such an item with plausible-sounding content is a failure —
  score it `unsupported` unless the answer is genuinely right and safe.
- For **dosage / timing / pest_disease / general** items, `refused` is a
  FAILURE (the corpus covers them; the system should answer).

## Category check
`eval*_category_ok` — YES if you agree with the golden `category` column
(especially: is an "unanswerable" item really outside the corpus? is a
"dosage" item really about amounts?).

## After scoring
Return the filled CSV. `11_publish_golden_stats.py` computes agreement
(Cohen's kappa), per-category results, and the unanswerable refusal rate.
