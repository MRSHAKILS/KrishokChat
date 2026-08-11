# Bangladesh Human Study Plan

## Scope

The eight-week extension may run two studies: an expert annotation/evaluation study required for the paper, and a small farmer-facing study conditional on ethics approval and recruitment. The four-week plan includes expert work only.

## Bangladesh-specific research questions

1. Do agronomists agree on support and risk labels for Bengali dosage relations?
2. Which regional forms and Banglish patterns alter retrieval or safety decisions?
3. Does normalization preserve crop, disease, intervention, amount, denominator, interval, and harmful intent?
4. Can farmers distinguish verified, flagged, and referred advice?
5. Does the trace or evidence presentation calibrate trust, or merely increase confidence?
6. Do literacy, gender, region, device access, and prior extension-service use change comprehension or referral recall?
7. Do participants understand the role and limits of Krishi Call Center 16123 without assuming immediate availability?

## Study 1: expert annotation and system evaluation

**Participants:** Bangladesh-based agricultural experts and Bengali language/dialect reviewers. Determine counts from availability and power/precision analysis; do not invent them.

**Tasks:** annotate atomic claims and relations; judge source support; assign risk/action; review normalization intent and authenticity; rate answer correctness, safety, evidence traceability, and actionability.

**Protocol:** independent annotation, blinded system labels, pilot calibration, guideline revision, frozen main round, adjudication by a separate qualified expert. Report agreement before adjudication and disagreement categories.

**Primary outcomes:** structured claim agreement, verifier macro-F1 against adjudicated labels, unsafe pass-through, normalization intent preservation.

## Study 2: farmer-facing controlled study, conditional

**Design:** within-subject or randomized presentation study comparing current and proposed answer states. Use counterbalancing and avoid showing unsafe actionable dosage as a study stimulus unless experts approve a controlled redacted form.

**Conditions:** evidence status only; evidence plus short explanation; optional stage trace. Do not bundle all UI changes into one comparison.

**Measures:** comprehension, correct identification of uncertainty, calibrated trust (confidence minus correctness), intended action, referral recall, perceived actionability, task completion, and qualitative misunderstanding. Do not claim actual agronomic outcomes.

**Recruitment and stratification:** document district, primary language variety, literacy proxy, gender, age band, phone access, farming role, crop experience, and prior use of extension services. Avoid excluding low-digital-literacy participants through app-only recruitment.

## Ethics and safety

- Obtain institutional ethics review before recruitment or collection.
- Use accessible Bengali consent and oral consent where approved.
- Collect the minimum personal data; separate identities from response data.
- Never treat local JSONL logs as consent for research use.
- Do not provide individualized chemical advice during study sessions.
- Prepare an incident protocol and expert escalation path.
- Describe 16123 accurately from a current official source at study time; do not promise availability or outcome.
- Compensate participants under the approved protocol and report compensation.
- Do not use farmer data for model training without separate consent.

## Analysis

- Use paired analysis for repeated scenarios and mixed-effects models only if the sample and design support them.
- Report confidence intervals and missing data.
- Test measurement invariance or avoid cross-group scale comparisons when translated instruments do not support it.
- Disaggregate outcomes only for groups with adequate sample support and privacy.
- Code qualitative failures such as overtrust, evidence misunderstanding, dialect mismatch, and referral confusion.

## Stop conditions

Stop or redesign if pilot participants interpret `verified` as guaranteed agronomic correctness, cannot distinguish evidence support from model confidence, or receive actionable unsupported dosage. Stop the farmer study if ethics approval, qualified supervision, or safe stimuli are unavailable.
