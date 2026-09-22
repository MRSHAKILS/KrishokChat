# X3 — Keep the chemical name in compressed SMS (+ correct the encoding statement)

**Priority 3 · 45 min · $0 · small code change + offline re-scoring (no LLM calls)**

## Why this adds value
In N05c the deterministic compressor keeps the dose in 92/100 long advisories but the
chemical name in only 34/100, while the LLM summarizer keeps it in 56/100. A dose without
its chemical is not a usable instruction, and reviewers flagged exactly this. The cause is
in code: `SMSCompressor.compress_from_qa_result` (`backend/app/domain/sms_compressor.py`)
keeps the **first dosage sentence** plus an optional intro sentence, and that sentence often
refers to the chemical only by pronoun or brand. Adding the chemical name as a slot should
lift chemical survival without touching dose survival.

## Required correction found while planning (do this regardless of the result)
The compressor output is **Bengali script** (`"DAE পরামর্শ: …"`, suffix `"| হেল্প: ১৬১২৩"`),
so it is sent as **UCS-2**: 70 characters per single SMS, 67 per segment when concatenated.
The paper currently says (App. B, `app:delivery`): "Lengths are counted in GSM-7 characters on
Latin-script SMS output…" and Table `tab:evidence_b` says "within 160 GSM-7 characters". Only
the 1,000-tuple test (`lang="en"`, 102–115 chars) is GSM-7. Fix in this plan by reporting
segments (step 4).

## Inputs
| Item | Path |
|---|---|
| 100 paired advisories (gold answer per `row_id`) | `experiments/N05_sms_survival/results/n05c_sample_100.json` |
| Frozen LLM-summarizer outputs (reuse, do not regenerate) | `experiments/N05_sms_survival/results/n05c_records_20260919.jsonl` |
| Scorer with frozen dose + chemical detectors | `experiments/N05_sms_survival/scripts/score_n05c.py` (`CHEMICALS`, `dose_pairs`, `chem_tokens`) |
| Compressor | `backend/app/domain/sms_compressor.py::compress_from_qa_result` |

## Part A — code change (behind a flag, default on after tests pass)
In `compress_from_qa_result`, after choosing `primary_dose_sent`:
1. `chem = _find_chemical(clean_ans, primary_dose_sent)`: the chemical/active-ingredient
   mention closest **before or inside** the dose sentence. Source of names: the verifier's
   chemical lexicon (`app/infrastructure/verification/dosage_claims.py` / dose reference) or
   `app/domain/chemical_registry.py`. **Do not** import the scorer's `CHEMICALS` list
   (that would score the change with its own rule).
2. If `chem` is not already in `primary_dose_sent`, build `body = f"{chem}: {primary_dose_sent}"`
   and drop the intro sentence first if needed to fit `avail`.
3. If it still does not fit, truncate the dose sentence at a word boundary but never cut the
   dose number+unit (use `_DOSE_RE` span).
4. Flag: `SMS_CHEM_SLOT` env var (default `"1"`).
5. Tests in `backend/tests/domain_services/test_sms_compressor_chem.py`: chemical prepended
   when missing; not duplicated when present; dose span never cut; length ≤ `max_chars`.
   Run the full backend suite.

## Part B — re-score (offline)
1. Copy `score_n05c.py` → `score_n05d.py`; change the output name to `n05d_summary_<date>.json`
   so the frozen N05c summary is untouched. Keep naive and LLM arms identical (they read frozen
   inputs), recompute only the compressor arm.
2. Add metrics for every arm:
   - `dose_and_chem_together`: SMS contains both a dose pair and a chemical token.
   - `ucs2_segments`: 1 if len ≤ 70 else ceil(len/67), for Bengali-script output; GSM-7 rule
     (160/153) only if the text is pure GSM-7. Report mean and distribution.
3. Sanity: with `SMS_CHEM_SLOT=0` the compressor arm must reproduce 92/100 dose and 34/100 chemical.
4. Also re-run the 1,000-tuple slot-survival check if it lives in the N05 scripts
   (`evaluate_sms_survival_84.py` / E15) to confirm 1,000/1,000 still holds.

Output: `experiments/N05_sms_survival/results/n05d_summary_<date>.json` (+ records jsonl).

## Decision rules and paper updates
Let `c` = new chemical survival, `d` = new dose survival, `b` = dose+chemical together, `s` = mean segments.

**Use if** `c` ≥ 56 (matches or beats the LLM) **and** `d` ≥ 90:
- **§5.3 (`sec:eval-safety`)**, SMS paragraph → "The deterministic packer kept the dose in {d} of 100 long advisories and the chemical name in {c} (both together in {b}), without inventing any value; the LLM summarizer kept them in 89 and 56 and invented one dose."
  Remove "SMS delivery loses information." only if `b` ≥ 85; otherwise keep it.
- **App. B `tab:n05c`**: add a column "Compressor v2" (or replace the compressor column and state the version in the caption), plus a row "Dose + chemical" and a row "UCS-2 segments (mean)".
- **Limitations** ("Delivery"): "SMS compression drops chemical names" → "SMS compression still loses some chemical names ({100−c}/100)" or delete if `c` ≥ 90.
- **App. E** SMS rows: update.

**Encoding fix (always):**
- App. B first sentence → "Bengali-script messages use UCS-2 encoding (70 characters per single SMS), so a 160-character advisory spans {s} segments on average; the 1,000-tuple test uses Latin-script GSM-7 output (102--115 characters, one segment)."
- §5.3 and `tab:evidence_b`: replace "160 GSM-7 characters" with "160 characters".

**If `c` < 56 or `d` drops below 90:** keep the current compressor; only apply the encoding fix
and add the dose+chemical metric for the existing compressor to App. B.
