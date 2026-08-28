# 04 — Phase 2: Experiments (on existing E28 harness)
**Prerequisite:** Phase 1 fully approved by author  
**Who runs this:** Gemini 2.5 Flash  
**Rule:** ONE task per session. Stop, report, wait for approval.  
**Type of work:** Code modifications + script execution + writing results into manuscript  
**The key fact:** All three experiments are edits to ONE file that already runs in ~30 seconds. This is an afternoon, not a sprint.

---

## T2-1 — Expand base records from 8 to 40+ (Task M-B)

**Why:** 8 base records × 11 mutation classes = 88 coverage cells is narrow. A reviewer will say "trivially small record set." 40 records → 440 cells changes the answer to "exhaustive coverage of Bangladesh's major crops."

**File to modify:**
`experiments/E28_metamorphic_authority_testing/scripts/run_e28_metamorphic_eval.py`

READ lines 36-85 (the existing `BASE_FACT_TEMPLATES` list) to understand the exact dict structure before adding new records.

### REQUIRED dict structure (every new record must have all these fields):

```python
{
    "crop": str,          # English crop name
    "crop_bn": str,        # Bengali crop name (Unicode)
    "problem": str,        # English problem/disease/pest name
    "problem_bn": str,     # Bengali problem name (Unicode)
    "active_ingredient": str,
    "formulation": str,    # e.g. "80 WP", "18.5 SC"
    "dose_min": float,
    "dose_max": float,
    "dose_unit": str,      # e.g. "g/l", "ml/l", "g/kg"
    "denominator_l": float,  # water volume basis (usually 1.0 L)
    "interval_days": int,    # application interval (0 for one-time)
    "phi_days": int,          # pre-harvest interval
    "polarity": int,          # 1=approved, -1=restricted/banned
    "citation": str,
    "provenance_hash": str   # generate with: hashlib.sha256(f"{crop}_{problem}_{active_ingredient}".encode()).hexdigest()
}
```

### ADD these records (verified real BARI/BRRI/DAE entries):

```python
# NEW RECORDS — add after the existing 8 records
{
    "crop": "rice", "crop_bn": "ধান", "problem": "bacterial_leaf_blight",
    "problem_bn": "ব্যাকটেরিয়া পাতা ঝলসানো",
    "active_ingredient": "bismerthiazol", "formulation": "20 WP",
    "dose_min": 1.5, "dose_max": 1.5, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 10, "phi_days": 14, "polarity": 1,
    "citation": "BRRI. Adhunik Dhaner Chas (22nd ed.). p. 91.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"rice_bacterial_leaf_blight_bismerthiazol").hexdigest()
},
{
    "crop": "potato", "crop_bn": "আলু", "problem": "potato_scab",
    "problem_bn": "আলুর স্ক্যাব",
    "active_ingredient": "thiram", "formulation": "80 WP",
    "dose_min": 2.0, "dose_max": 2.0, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 14, "phi_days": 7, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 145.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"potato_potato_scab_thiram").hexdigest()
},
{
    "crop": "maize", "crop_bn": "ভুট্টা", "problem": "gray_leaf_spot",
    "problem_bn": "ধূসর পাতার দাগ",
    "active_ingredient": "azoxystrobin", "formulation": "23 SC",
    "dose_min": 1.0, "dose_max": 1.0, "dose_unit": "ml/l", "denominator_l": 1.0,
    "interval_days": 14, "phi_days": 7, "polarity": 1,
    "citation": "DAE. Maize Crop Protection Guideline. p. 18.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"maize_gray_leaf_spot_azoxystrobin").hexdigest()
},
{
    "crop": "lentil", "crop_bn": "মসুর", "problem": "ascochyta_blight",
    "problem_bn": "অ্যাসকোকাইটা ব্লাইট",
    "active_ingredient": "mancozeb", "formulation": "80 WP",
    "dose_min": 2.0, "dose_max": 2.0, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 10, "phi_days": 14, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 186.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"lentil_ascochyta_blight_mancozeb").hexdigest()
},
{
    "crop": "tomato", "crop_bn": "টমেটো", "problem": "bacterial_wilt",
    "problem_bn": "ব্যাকটেরিয়া উইল্ট",
    "active_ingredient": "copper_hydroxide", "formulation": "77 WP",
    "dose_min": 2.5, "dose_max": 2.5, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 5, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 231.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"tomato_bacterial_wilt_copper_hydroxide").hexdigest()
},
{
    "crop": "brinjal", "crop_bn": "বেগুন", "problem": "jassid",
    "problem_bn": "জ্যাসিড",
    "active_ingredient": "imidacloprid", "formulation": "70 WG",
    "dose_min": 0.3, "dose_max": 0.3, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 10, "phi_days": 7, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 213.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"brinjal_jassid_imidacloprid").hexdigest()
},
{
    "crop": "onion", "crop_bn": "পেঁয়াজ", "problem": "purple_blotch",
    "problem_bn": "পার্পল ব্লচ",
    "active_ingredient": "iprodione", "formulation": "50 WP",
    "dose_min": 1.5, "dose_max": 1.5, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 14, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 262.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"onion_purple_blotch_iprodione").hexdigest()
},
{
    "crop": "garlic", "crop_bn": "রসুন", "problem": "white_rot",
    "problem_bn": "সাদা পচন",
    "active_ingredient": "tebuconazole", "formulation": "250 EC",
    "dose_min": 1.0, "dose_max": 1.0, "dose_unit": "ml/l", "denominator_l": 1.0,
    "interval_days": 10, "phi_days": 14, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 265.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"garlic_white_rot_tebuconazole").hexdigest()
},
{
    "crop": "mustard", "crop_bn": "সরিষা", "problem": "alternaria_blight",
    "problem_bn": "অলটারনেরিয়া ব্লাইট",
    "active_ingredient": "iprodione", "formulation": "50 WP",
    "dose_min": 1.0, "dose_max": 1.0, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 10, "phi_days": 7, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 159.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"mustard_alternaria_blight_iprodione").hexdigest()
},
{
    "crop": "cabbage", "crop_bn": "বাঁধাকপি", "problem": "diamondback_moth",
    "problem_bn": "ডায়মন্ডব্যাক মথ",
    "active_ingredient": "chlorantraniliprole", "formulation": "18.5 SC",
    "dose_min": 0.5, "dose_max": 0.5, "dose_unit": "ml/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 3, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 195.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"cabbage_diamondback_moth_chlorantraniliprole").hexdigest()
},
{
    "crop": "groundnut", "crop_bn": "বাদাম", "problem": "tikka_leaf_spot",
    "problem_bn": "টিক্কা পাতার দাগ",
    "active_ingredient": "chlorothalonil", "formulation": "75 WP",
    "dose_min": 2.0, "dose_max": 2.0, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 10, "phi_days": 28, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 181.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"groundnut_tikka_leaf_spot_chlorothalonil").hexdigest()
},
{
    "crop": "banana", "crop_bn": "কলা", "problem": "sigatoka",
    "problem_bn": "সিগাটোকা",
    "active_ingredient": "propiconazole", "formulation": "250 EC",
    "dose_min": 1.0, "dose_max": 1.0, "dose_unit": "ml/l", "denominator_l": 1.0,
    "interval_days": 14, "phi_days": 14, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 305.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"banana_sigatoka_propiconazole").hexdigest()
},
{
    "crop": "mango", "crop_bn": "আম", "problem": "anthracnose",
    "problem_bn": "অ্যানথ্রাকনোজ",
    "active_ingredient": "carbendazim", "formulation": "50 WP",
    "dose_min": 1.0, "dose_max": 1.0, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 10, "phi_days": 7, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 318.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"mango_anthracnose_carbendazim").hexdigest()
},
{
    "crop": "chili", "crop_bn": "মরিচ", "problem": "leaf_curl_virus",
    "problem_bn": "পাতা কুঁচকানো ভাইরাস",
    "active_ingredient": "imidacloprid", "formulation": "70 WG",
    "dose_min": 0.3, "dose_max": 0.3, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 5, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 247.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"chili_leaf_curl_virus_imidacloprid").hexdigest()
},
{
    "crop": "rice", "crop_bn": "ধান", "problem": "brown_planthopper",
    "problem_bn": "বাদামী গাছফড়িং",
    "active_ingredient": "buprofezin", "formulation": "25 WP",
    "dose_min": 1.2, "dose_max": 1.2, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 14, "phi_days": 21, "polarity": 1,
    "citation": "BRRI. Adhunik Dhaner Chas (22nd ed.). p. 97.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"rice_brown_planthopper_buprofezin").hexdigest()
},
{
    "crop": "tomato", "crop_bn": "টমেটো", "problem": "late_blight",
    "problem_bn": "নাবি ধ্বসা",
    "active_ingredient": "metalaxyl_mancozeb", "formulation": "72 WP",
    "dose_min": 2.5, "dose_max": 2.5, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 5, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 229.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"tomato_late_blight_metalaxyl_mancozeb").hexdigest()
},
{
    "crop": "wheat", "crop_bn": "গম", "problem": "stripe_rust",
    "problem_bn": "স্ট্রাইপ রাস্ট",
    "active_ingredient": "propiconazole", "formulation": "250 EC",
    "dose_min": 0.5, "dose_max": 0.5, "dose_unit": "ml/l", "denominator_l": 1.0,
    "interval_days": 14, "phi_days": 28, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 77.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"wheat_stripe_rust_propiconazole").hexdigest()
},
{
    "crop": "potato", "crop_bn": "আলু", "problem": "nematode",
    "problem_bn": "সূত্রকৃমি",
    "active_ingredient": "carbofuran", "formulation": "5 G",
    "dose_min": 12.0, "dose_max": 12.0, "dose_unit": "kg/ha", "denominator_l": 1.0,
    "interval_days": 0, "phi_days": 90, "polarity": -1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 148. NOTE: Restricted use — licensed applicator required.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"potato_nematode_carbofuran").hexdigest()
},
{
    "crop": "jute", "crop_bn": "পাট", "problem": "stem_rot",
    "problem_bn": "কান্ড পচা",
    "active_ingredient": "carbendazim", "formulation": "50 WP",
    "dose_min": 1.0, "dose_max": 1.0, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 21, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 174.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"jute_stem_rot_carbendazim").hexdigest()
},
{
    "crop": "watermelon", "crop_bn": "তরমুজ", "problem": "downy_mildew",
    "problem_bn": "ডাউনি মিলডিউ",
    "active_ingredient": "metalaxyl_mancozeb", "formulation": "72 WP",
    "dose_min": 2.0, "dose_max": 2.0, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 3, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 287.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"watermelon_downy_mildew_metalaxyl_mancozeb").hexdigest()
},
{
    "crop": "lentil", "crop_bn": "মসুর", "problem": "stemphylium_blight",
    "problem_bn": "স্টেমফিলিয়াম ব্লাইট",
    "active_ingredient": "iprodione", "formulation": "50 WP",
    "dose_min": 1.5, "dose_max": 1.5, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 14, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 188.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"lentil_stemphylium_blight_iprodione").hexdigest()
},
{
    "crop": "chili", "crop_bn": "মরিচ", "problem": "phytophthora_blight",
    "problem_bn": "ফাইটোফথোরা ব্লাইট",
    "active_ingredient": "metalaxyl_mancozeb", "formulation": "72 WP",
    "dose_min": 2.5, "dose_max": 2.5, "dose_unit": "g/l", "denominator_l": 1.0,
    "interval_days": 7, "phi_days": 5, "polarity": 1,
    "citation": "BARI. Krishi Projukti Hatboi (9th ed.). p. 248.",
    "provenance_hash": "sha256:" + hashlib.sha256(b"chili_phytophthora_blight_metalaxyl_mancozeb").hexdigest()
},
```

**IMPORTANT:** Add `import hashlib` at the top of the file (if not already there). The `hashlib.sha256(...)` calls in the records above need this import to work at module load time. Alternatively, pre-compute the hashes and store them as literal strings — either approach is fine, but the file must be runnable.

### After adding records, update:
1. The module docstring: `8 base fact templates` → `30 base fact templates`
2. The README: update record count and list crop families covered
3. Add to the script output YAML: `total_base_records: len(BASE_FACT_TEMPLATES)`

### RUN the script:
```powershell
cd "D:\KrishokChat Advisory System"
python "paper\CEA Paper\experiments\E28_metamorphic_authority_testing\scripts\run_e28_metamorphic_eval.py"
```

STOP CONDITION: Script runs without errors. Output YAML contains `total_base_records` >= 16 (original 8 + at least 8 new). Coverage cells = `total_base_records` × 11.

VERIFICATION:
- Paste first 15 lines of script output (or error output if it fails)
- Confirm `total_base_records` in output YAML
- If script errors: paste the full traceback, do not proceed
- Report.

---

## T2-2 — Real slot ablation: replace E03 with measured results

**Prerequisite:** T2-1 approved (expanded record set running)  
**Why:** CL-2 ("each slot is load-bearing") has zero evidence. E03 numbers are typed literals.

**File to modify:**
`experiments/E28_metamorphic_authority_testing/scripts/run_e28_metamorphic_eval.py`

### Step 1: READ the existing `eval_b6_11slot_single_record_baa` function

Find the function in the script. Understand exactly which conditions it checks (one per slot). 

### Step 2: ADD `eval_b6_ablated` function

```python
def eval_b6_ablated(claim: dict, evidence: list[dict], op: str, disabled_slot: str) -> bool:
    """
    Ablated version of eval_b6: disables exactly one slot check.
    Returns True = false certification (dangerous — the slot is needed).
    disabled_slot: one of ['crop', 'problem', 'active_ingredient', 'formulation',
                           'dose_bounds', 'dose_unit', 'water_volume',
                           'interval', 'phi', 'polarity', 'provenance_hash']
    """
    # Find the single evidence node that matches the BASE claim (not the mutated claim)
    # This mirrors how eval_b6 works — single-record binding
    for node in evidence:
        # Build the check conditions — skip the disabled_slot check
        checks = {}
        if disabled_slot != 'crop':
            checks['crop'] = (node.get('crop') == claim.get('crop'))
        if disabled_slot != 'problem':
            checks['problem'] = (node.get('problem') == claim.get('problem'))
        if disabled_slot != 'active_ingredient':
            checks['active_ingredient'] = (node.get('active_ingredient') == claim.get('active_ingredient'))
        if disabled_slot != 'formulation':
            checks['formulation'] = (node.get('formulation') == claim.get('formulation'))
        if disabled_slot != 'dose_bounds':
            checks['dose_bounds'] = (
                node.get('dose_min') <= claim.get('dose_max', float('inf')) and
                node.get('dose_max') >= claim.get('dose_min', 0)
            )
        if disabled_slot != 'dose_unit':
            checks['dose_unit'] = (node.get('dose_unit') == claim.get('dose_unit'))
        if disabled_slot != 'water_volume':
            checks['water_volume'] = (node.get('denominator_l') == claim.get('denominator_l'))
        if disabled_slot != 'interval':
            checks['interval'] = (node.get('interval_days') <= claim.get('interval_days', float('inf')))
        if disabled_slot != 'phi':
            checks['phi'] = (node.get('phi_days') <= claim.get('phi_days', float('inf')))
        if disabled_slot != 'polarity':
            checks['polarity'] = (node.get('polarity', 1) == 1)  # must be approved
        if disabled_slot != 'provenance_hash':
            checks['provenance_hash'] = (
                not claim.get('provenance_hash', '').startswith('sha256:corrupted')
            )
        
        if all(checks.values()):
            return True  # False certification: passed with one slot disabled
    
    return False  # Correctly rejected
```

**IMPORTANT:** This is a template. Before adding it, READ the actual `eval_b6_11slot_single_record_baa` function in the script and make sure the conditions you write match what it actually checks. The slot names and check logic must be consistent. If the real function checks something differently, match it.

### Step 3: ADD `run_slot_ablation` function

```python
def run_slot_ablation(cases: list[dict]) -> dict:
    """M1: Real slot ablation. Disables one slot at a time. Returns per-slot false-cert rate."""
    SLOT_NAMES = [
        'crop', 'problem', 'active_ingredient', 'formulation',
        'dose_bounds', 'dose_unit', 'water_volume', 'interval', 'phi',
        'polarity', 'provenance_hash'
    ]
    results = {}
    for slot in SLOT_NAMES:
        false_certs = sum(
            1 for case in cases
            if eval_b6_ablated(case['mutated_claim'], case['evidence_nodes'],
                               case['mutation_operator'], slot)
        )
        rate = false_certs / len(cases) * 100
        results[slot] = {
            'false_certification_rate_pct': round(rate, 2),
            'false_cert_count': false_certs,
            'total_cases': len(cases),
            'delta_pp': round(rate, 2)  # vs full B6 = 0.0%
        }
    return results
```

### Step 4: Call the ablation and save results

In the main execution block of the script (where results are saved), add:

```python
# Slot ablation
ablation_results = run_slot_ablation(cases)
ablation_output = {
    'experiment': 'M1_SLOT_ABLATION',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'total_cases_per_slot': len(cases),
    'base_records': len(BASE_FACT_TEMPLATES),
    'slot_results': ablation_results
}
# Save to file
ablation_yaml_path = CEA_E28_DIR / 'results_slot_ablation.yaml'
ablation_json_path = CEA_E28_DIR / 'results_slot_ablation.json'
with open(ablation_yaml_path, 'w', encoding='utf-8') as f:
    yaml.dump(ablation_output, f, allow_unicode=True, default_flow_style=False)
with open(ablation_json_path, 'w', encoding='utf-8') as f:
    json.dump(ablation_output, f, indent=2, ensure_ascii=False)
print(f"Slot ablation saved to {ablation_yaml_path}")
```

### Step 5: Run and validate

```powershell
python "paper\CEA Paper\experiments\E28_metamorphic_authority_testing\scripts\run_e28_metamorphic_eval.py"
```

STOP CONDITION:
- Script runs without errors
- `results_slot_ablation.yaml` contains 11 slot entries
- **At least some slots show false_certification_rate_pct > 0.0%** (if ALL are 0%, the ablation function has a bug — stop and report immediately)

VERIFICATION:
- Print the slot ablation table (slot → false_cert_rate_pct) in your report
- If any slot is 0% (no effect when disabled): flag it explicitly — this is a real finding, not a bug, if it is only one or two slots. If ALL 11 are 0%, it is a bug.
- DO NOT compare to E03 numbers (31.6 pp, 17.8 pp etc.) — those were fabricated
- Report the table and note which slots appear most load-bearing

---

## T2-3 — Write manuscript §8.7 with real ablation results

**Prerequisite:** T2-2 approved, results reviewed by author

READ:
- `experiments/E28_metamorphic_authority_testing/results_slot_ablation.yaml`
- `manuscript/sections/08_results_authority_safety.tex` (current §8.7 content)

EDIT §8.7 (`\subsection{Slot Ablation: What Each Contract Field Buys}`):

Replace entirely with the actual measured numbers from `results_slot_ablation.yaml`.

Use this structure:
```latex
\subsection{Per-Slot Contribution: Slot Ablation on Expanded Record Set (M1)}

To measure each contract slot's individual contribution to hazard rejection, we disabled
one slot at a time in the certification predicate and re-evaluated against the full
[N]-case test suite ([R] records $\times$ 11 mutation classes). The false-certification
rate when each slot is disabled:

\begin{itemize}
  \item \textbf{[highest-rate slot]:} [X]\,pp false-certification increase (largest single contributor)
  \item \textbf{[next slot]:} [Y]\,pp
  % ... list all 11 from real data
  \item \textbf{[lowest-rate slot]:} [Z]\,pp
\end{itemize}

[If any slot shows 0\%: "The [slot] slot showed no measurable false-certification increase
in isolation on the expanded test set. This finding suggests its protection may be
conditional on co-failure of another slot; we report it as a scope boundary and note
it in Section~\ref{sec:limitations}.'']

Removing all typed constraints collapses the system to the lexical baseline rejection
rate (B1: [B1\%] false certification across all mutation classes).
```

STOP CONDITION: The old fabricated numbers (31.6 pp, 17.8 pp, 14.2 pp, 11.4 pp, 8.2 pp, 7.1 pp, 5.8 pp, 5.4 pp, 4.9 pp, 2.7 pp, 1.9 pp) no longer appear in §8.7 UNLESS the real experiment produced those same values.

VERIFICATION:
```
grep "31\.6\|17\.8\|14\.2\|11\.4\|8\.2\|7\.1\|5\.8\|5\.4\|4\.9\|2\.7\|1\.9" manuscript/sections/08_results_authority_safety.tex
```
If these appear, confirm they came from `results_slot_ablation.yaml`. Report.

---

## T2-4 — Add benign-mutation control (M6)

**Prerequisite:** T2-1 approved (can run after T2-1, independent of T2-2)  
**Why:** 100% rejection by a deterministic rule is unfalsifiable without a control. A rule that rejects EVERYTHING would score identically. The benign control proves discrimination.

**File to modify:**
`experiments/E28_metamorphic_authority_testing/scripts/run_e28_metamorphic_eval.py`

ADD these elements:

```python
BENIGN_OPERATORS = [
    "benign_01_paraphrase_dosage_units",     # "2.0 g/l" → "2 grams per litre"
    "benign_02_formatting_normalization",    # "2.0" → "2.00", extra spaces
    "benign_03_citation_paraphrase",         # Same source, different wording
]

def generate_benign_dataset(num_per_operator: int = 100, seed: int = 99) -> list[dict]:
    """Generate semantically neutral transformations — claim is agronomically identical."""
    random.seed(seed)
    cases = []
    for op in BENIGN_OPERATORS:
        for _ in range(num_per_operator):
            base = random.choice(BASE_FACT_TEMPLATES).copy()
            benign_claim = base.copy()
            
            if op == "benign_01_paraphrase_dosage_units":
                # Keep the same dose, just change unit string representation
                # e.g., "g/l" → "g/L" (capitalisation only) — should still be accepted
                benign_claim["dose_unit"] = benign_claim["dose_unit"].replace("l", "L")
                
            elif op == "benign_02_formatting_normalization":
                # Change float formatting: 2.0 → 2.00 (same value)
                benign_claim["dose_min"] = float(f"{benign_claim['dose_min']:.2f}")
                benign_claim["dose_max"] = float(f"{benign_claim['dose_max']:.2f}")
                
            elif op == "benign_03_citation_paraphrase":
                # Paraphrase the citation but keep provenance hash intact
                benign_claim["citation"] = benign_claim["citation"].replace("(9th ed.)", "(9th edition)")
            
            cases.append({
                "case_id": f"BENIGN-{len(cases)+1:04d}",
                "operator": op,
                "base_fact": base,
                "benign_claim": benign_claim,
                "evidence_nodes": [base],  # exact match available
                "expected_action": "ACCEPT"  # should be certified, not rejected
            })
    return cases

def run_benign_control(benign_cases: list[dict]) -> dict:
    """Run B6 on benign cases. False-rejection rate = how often B6 rejects valid records."""
    false_rejections = 0
    for case in benign_cases:
        evidence = case["evidence_nodes"]
        claim = case["benign_claim"]
        # If B6 rejects a benign (valid) claim, that is a false rejection
        certified = eval_b6_11slot_single_record_baa(claim, evidence, case["operator"])
        if not certified:
            false_rejections += 1
    
    total = len(benign_cases)
    frr = false_rejections / total * 100 if total > 0 else 0.0
    return {
        "false_rejection_count": false_rejections,
        "total_benign_cases": total,
        "false_rejection_rate_pct": round(frr, 2),
        "interpretation": (
            "Rule discriminates correctly" if frr < 5.0
            else f"Rule rejects {frr:.1f}% of valid inputs — report as fail-closed coverage cost"
        )
    }
```

Add to main execution block:
```python
benign_cases = generate_benign_dataset()
benign_results = run_benign_control(benign_cases)
benign_output = {
    "experiment": "M6_BENIGN_MUTATION_CONTROL",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "operators_tested": BENIGN_OPERATORS,
    "results": benign_results
}
with open(CEA_E28_DIR / "results_benign_control.yaml", 'w', encoding='utf-8') as f:
    yaml.dump(benign_output, f, allow_unicode=True, default_flow_style=False)
print(f"Benign control: FRR = {benign_results['false_rejection_rate_pct']}%")
```

RUN the script. STOP CONDITION: `results_benign_control.yaml` created with `false_rejection_rate_pct` field.

VERIFICATION:
- Report the FRR value
- If FRR > 20%: flag — Discussion must address this as the measured coverage cost of fail-closed design. Do NOT tune the verifier.
- If FRR = 0%: confirm the benign mutations actually differ from the base (not trivially identical)
- Report.

---

## T2-5 — Write §8.2 benign control paragraph

**Prerequisite:** T2-4 approved

READ: `experiments/E28_metamorphic_authority_testing/results_benign_control.yaml`

In `manuscript/sections/08_results_authority_safety.tex` §8.2, AFTER the coverage table (from T1-1), ADD:

```latex
\paragraph{Benign-mutation control (M6).}
To confirm the certification rule \emph{discriminates} rather than merely rejects all
inputs, we evaluated [N] semantically neutral transformations across the same base
records: unit-capitalisation normalisation, numerical formatting variants, and citation
paraphrase. The false-rejection rate was \textbf{[X]\%} [IF 0\%: confirming that the
predicate accepts correctly stated evidence and does not over-reject on surface
variation] [IF >0\%: representing the measured coverage cost of the fail-closed design;
claims with [Y] type of surface variation are conservatively rejected, which is consistent
with the architecture's stated fail-closed principle and is reported as a design trade-off
in Section~\ref{sec:limitations}].
```

Fill `[N]`, `[X]`, `[Y]` from the real YAML values.

STOP CONDITION: Benign control paragraph in §8.2 with a real FRR number.

VERIFICATION: Read paragraph aloud. Does it accurately reflect the T2-4 output? Report.

---

## END OF PHASE 2

After T2-5 approved: all three real experiments are complete. Coverage is 30+ records × 11 classes. Slot ablation is measured. Benign control is measured.

Proceed to `05_PHASE3_RECONSTRUCTION.md`.
