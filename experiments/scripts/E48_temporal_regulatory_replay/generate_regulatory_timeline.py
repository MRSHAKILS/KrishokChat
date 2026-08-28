#!/usr/bin/env python3
"""
experiments/scripts/E48_temporal_regulatory_replay/generate_regulatory_timeline.py
===================================================================================
Generates the longitudinal regulatory evolution dataset across 4 time periods (2022-2025)
for 10 representative agricultural chemical treatments evolving from APPROVED to BANNED.

Periods:
- 2022: APPROVED (Standard dose, standard PHI, polarity = 1)
- 2023: APPROVED_WITH_CONSTRAINT (Tighter dose bounds, extended PHI, polarity = 1)
- 2024: RESTRICTED (Requires certified applicator/permit, lower dose ceiling, polarity = 1)
- 2025: BANNED (Complete regulatory ban, polarity = -1)

10 chemicals x 4 periods x 5 query types = 200 longitudinal test instances.
Outputs to: research_artifacts/datasets/temporal_regulatory/temporal_regulatory_200.jsonl
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_FILE = WORKSPACE_ROOT / "research_artifacts" / "datasets" / "temporal_regulatory" / "temporal_regulatory_200.jsonl"
SEED = 20260813

CHEMICAL_TIMELINE_SPECS = [
    {
        "crop": "potato", "crop_bn": "আলু", "problem": "late_blight", "problem_bn": "নাবি ধ্বসা",
        "active_ingredient": "mancozeb_synthetic_evolution", "formulation": "80 WP", "dose_unit": "g/l",
        "timeline": {
            2022: {"status": "APPROVED", "dose_min": 2.0, "dose_max": 2.5, "phi_days": 14, "interval_days": 7, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2022: Standard approval for Mancozeb 80 WP."},
            2023: {"status": "APPROVED_WITH_CONSTRAINT", "dose_min": 2.0, "dose_max": 2.0, "phi_days": 21, "interval_days": 10, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2023 Revision: Extended PHI to 21 days for Mancozeb."},
            2024: {"status": "RESTRICTED", "dose_min": 1.5, "dose_max": 1.5, "phi_days": 28, "interval_days": 14, "polarity": 1, "operator_req": True, "citation": "MoA Gazette 2024: Restricted substance schedule - licensed application only."},
            2025: {"status": "BANNED", "dose_min": 0.0, "dose_max": 0.0, "phi_days": 0, "interval_days": 0, "polarity": -1, "operator_req": False, "citation": "MoA Gazette 2025 SRO-88: Complete national prohibition and deregistration."},
        },
        "query_templates": [
            ("dose", "আলুর নাবি ধ্বসায় এই বালাইনাশক কত গ্রাম হারে প্রয়োগ করতে হবে?"),
            ("phi", "স্প্রে করার কত দিন পর আলু ফসল তোলা যাবে (PHI)?"),
            ("safety", "এই বালাইনাশক কি বর্তমান সরকারি গেজেটে অনুমোদিত ও নিরাপদ?"),
            ("interval", "কত দিন পর পর পুনরায় স্প্রে করার নিয়ম?"),
            ("restriction", "সাধারণ কৃষক কি সরাসরি এই ওষুধ প্রয়োগ করতে পারবে নাকি লাইসেন্স লাগবে?"),
        ]
    },
    {
        "crop": "rice", "crop_bn": "ধান", "problem": "blast", "problem_bn": "ব্লাস্ট রোগ",
        "active_ingredient": "tricyclazole_synthetic_evolution", "formulation": "75 WP", "dose_unit": "g/l",
        "timeline": {
            2022: {"status": "APPROVED", "dose_min": 0.75, "dose_max": 1.0, "phi_days": 21, "interval_days": 10, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2022: Standard approval for Tricyclazole."},
            2023: {"status": "APPROVED_WITH_CONSTRAINT", "dose_min": 0.75, "dose_max": 0.75, "phi_days": 28, "interval_days": 14, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2023: PHI extended to 28 days for Tricyclazole."},
            2024: {"status": "RESTRICTED", "dose_min": 0.5, "dose_max": 0.5, "phi_days": 30, "interval_days": 14, "polarity": 1, "operator_req": True, "citation": "MoA Gazette 2024: Restricted schedule application."},
            2025: {"status": "BANNED", "dose_min": 0.0, "dose_max": 0.0, "phi_days": 0, "interval_days": 0, "polarity": -1, "operator_req": False, "citation": "MoA Gazette 2025: Complete ban on Tricyclazole formulation."},
        },
        "query_templates": [
            ("dose", "ধানের ব্লাস্টে সঠিক ডোজ কত?"),
            ("phi", "ধান কাটার কত দিন আগে ট্রাইসাইক্লাজল স্প্রে বন্ধ করতে হবে?"),
            ("safety", "ধানের ব্লাস্টে এই ওষুধ কি সরকারি নিয়মে বৈধ?"),
            ("interval", "ব্লাস্টের ওষুধ কত দিন পর পর স্প্রে করতে হয়?"),
            ("restriction", "এই বালাইনাশক ব্যবহারের ওপর কোনো সরকারি নিষেধাজ্ঞা বা বিধিনিষেধ আছে কি?"),
        ]
    },
    {
        "crop": "rice", "crop_bn": "ধান", "problem": "stem_borer", "problem_bn": "মাজরা পোকা",
        "active_ingredient": "cartap_synthetic_evolution", "formulation": "50 SP", "dose_unit": "g/l",
        "timeline": {
            2022: {"status": "APPROVED", "dose_min": 1.2, "dose_max": 1.5, "phi_days": 21, "interval_days": 14, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2022: Cartap 50 SP approved."},
            2023: {"status": "APPROVED_WITH_CONSTRAINT", "dose_min": 1.2, "dose_max": 1.2, "phi_days": 28, "interval_days": 14, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2023: Cartap dosage upper ceiling tightened."},
            2024: {"status": "RESTRICTED", "dose_min": 1.0, "dose_max": 1.0, "phi_days": 30, "interval_days": 21, "polarity": 1, "operator_req": True, "citation": "MoA Gazette 2024: Restricted pesticide schedule."},
            2025: {"status": "BANNED", "dose_min": 0.0, "dose_max": 0.0, "phi_days": 0, "interval_days": 0, "polarity": -1, "operator_req": False, "citation": "MoA Gazette 2025: Banned active ingredient list."},
        },
        "query_templates": [
            ("dose", "মাজরা পোকা দমনে অনুমোদিত মাত্রা কত?"),
            ("phi", "ধান কাটার আগে কত দিন অপেক্ষা করতে হবে?"),
            ("safety", "মাজরা পোকার এই কীটনাশক ব্যবহার কি বৈধ?"),
            ("interval", "মাজরা পোকার ওষুধ কত দিন ব্যবধানে স্প্রে করতে হয়?"),
            ("restriction", "কীটনাশকটি প্রয়োগে কোনো বিশেষ অনুমতি বা শর্ত আছে কি?"),
        ]
    },
    {
        "crop": "wheat", "crop_bn": "গম", "problem": "bipolaris_leaf_blight", "problem_bn": "পাতা ঝলসানো",
        "active_ingredient": "propiconazole_synthetic_evolution", "formulation": "250 EC", "dose_unit": "ml/l",
        "timeline": {
            2022: {"status": "APPROVED", "dose_min": 0.5, "dose_max": 0.75, "phi_days": 28, "interval_days": 15, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2022: Propiconazole 250 EC approved for wheat."},
            2023: {"status": "APPROVED_WITH_CONSTRAINT", "dose_min": 0.5, "dose_max": 0.5, "phi_days": 35, "interval_days": 15, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2023: Propiconazole PHI extended."},
            2024: {"status": "RESTRICTED", "dose_min": 0.4, "dose_max": 0.4, "phi_days": 42, "interval_days": 20, "polarity": 1, "operator_req": True, "citation": "MoA Gazette 2024: Restricted schedule."},
            2025: {"status": "BANNED", "dose_min": 0.0, "dose_max": 0.0, "phi_days": 0, "interval_days": 0, "polarity": -1, "operator_req": False, "citation": "MoA Gazette 2025: National ban on Propiconazole."},
        },
        "query_templates": [
            ("dose", "গমে পাতা ঝলসানো রোগে প্রপিকোনাজল কত মিলি দিতে হবে?"),
            ("phi", "গম সংগ্রহের কত দিন আগে স্প্রে শেষ করতে হবে?"),
            ("safety", "গমে এই ছত্রাকনাশক ব্যবহার কি অনুমোদিত?"),
            ("interval", "কত দিন পর পর স্প্রে করার নির্দেশ দেওয়া হয়েছে?"),
            ("restriction", "প্রপিকোনাজল কিনতে ও প্রয়োগ করতে কি অনুমতি লাগবে?"),
        ]
    },
    {
        "crop": "brinjal", "crop_bn": "বেগুন", "problem": "fruit_and_shoot_borer", "problem_bn": "ডগা ও ফল ছিদ্রকারী পোকা",
        "active_ingredient": "chlorantraniliprole_synthetic_evolution", "formulation": "18.5 SC", "dose_unit": "ml/l",
        "timeline": {
            2022: {"status": "APPROVED", "dose_min": 0.5, "dose_max": 0.5, "phi_days": 3, "interval_days": 7, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2022: Approved for brinjal."},
            2023: {"status": "APPROVED_WITH_CONSTRAINT", "dose_min": 0.4, "dose_max": 0.4, "phi_days": 5, "interval_days": 10, "polarity": 1, "operator_req": False, "citation": "MoA Gazette 2023: PHI adjusted to 5 days."},
            2024: {"status": "RESTRICTED", "dose_min": 0.3, "dose_max": 0.3, "phi_days": 7, "interval_days": 14, "polarity": 1, "operator_req": True, "citation": "MoA Gazette 2024: Restricted application."},
            2025: {"status": "BANNED", "dose_min": 0.0, "dose_max": 0.0, "phi_days": 0, "interval_days": 0, "polarity": -1, "operator_req": False, "citation": "MoA Gazette 2025: Complete prohibition."},
        },
        "query_templates": [
            ("dose", "বেগুনের ফল ছিদ্রকারী পোকার সঠিক ডোজ কত?"),
            ("phi", "স্প্রে করার কত দিন পর বেগুন তুলে বাজারে বিক্রি করা যাবে?"),
            ("safety", "বেগুনে এই কীটনাশক ব্যবহার কি বৈধ?"),
            ("interval", "কত দিন অন্তর স্প্রে করতে হবে?"),
            ("restriction", "এই কীটনাশক ব্যবহারের জন্য সরকারি বিধিবিধান কী?"),
        ]
    },
]

# Expand to 10 chemicals across other crops
extra_crops = ["maize", "tomato", "chili", "cabbage", "mustard"]
for idx, crop in enumerate(extra_crops):
    src = CHEMICAL_TIMELINE_SPECS[idx % 5]
    entry = {
        "crop": crop,
        "crop_bn": crop,
        "problem": f"{crop}_pest_evolution",
        "problem_bn": f"{crop} বালাই",
        "active_ingredient": f"chemical_synth_{idx+6:02d}_{crop}",
        "formulation": "50 EC",
        "dose_unit": "ml/l",
        "timeline": src["timeline"],
        "query_templates": [
            ("dose", f"{crop} ফসলে অনুমোদিত প্রয়োগ মাত্রা কত?"),
            ("phi", f"{crop} তোলার কত দিন আগে স্প্রে বন্ধ করতে হবে?"),
            ("safety", f"{crop} ফসলে এই ওষুধ ব্যবহার কি সরকার অনুমোদিত?"),
            ("interval", f"{crop} ফসলে কত দিন পর পর স্প্রে করতে হবে?"),
            ("restriction", f"{crop} ফসলে এটি ব্যবহারের সরকারি শর্ত কী?"),
        ]
    }
    CHEMICAL_TIMELINE_SPECS.append(entry)


def generate_dataset():
    cases = []
    case_idx = 1

    years = [2022, 2023, 2024, 2025]

    for year in years:
        for chem_spec in CHEMICAL_TIMELINE_SPECS:
            period_data = chem_spec["timeline"][year]
            crop = chem_spec["crop"]
            problem = chem_spec["problem"]
            active = chem_spec["active_ingredient"]

            # Snapshot evidence record for this year
            evidence_node = {
                "period_year": year,
                "crop": crop,
                "crop_bn": chem_spec["crop_bn"],
                "problem": problem,
                "problem_bn": chem_spec["problem_bn"],
                "active_ingredient": active,
                "formulation": chem_spec["formulation"],
                "dose_min": period_data["dose_min"],
                "dose_max": period_data["dose_max"],
                "dose_unit": chem_spec["dose_unit"],
                "denominator_l": 1.0,
                "interval_days": period_data["interval_days"],
                "phi_days": period_data["phi_days"],
                "polarity": period_data["polarity"],
                "status": period_data["status"],
                "operator_required": period_data["operator_req"],
                "citation": period_data["citation"],
                "provenance_hash": f"sha256:temporal_{year}_{active}"
            }

            for q_type, q_bn in chem_spec["query_templates"]:
                case = {
                    "case_id": f"TEMP-REPLAY-{case_idx:04d}",
                    "period_year": year,
                    "query_type": q_type,
                    "query_bn": q_bn,
                    "crop": crop,
                    "problem": problem,
                    "active_ingredient": active,
                    "evidence_snapshot": evidence_node,
                    "expected_status": period_data["status"],
                    "expected_polarity": period_data["polarity"],
                    "expected_operator_required": period_data["operator_req"],
                    "expected_action": "REFUSE" if period_data["polarity"] == -1 else ("REQUIRE_OPERATOR" if period_data["operator_req"] else "CERTIFY"),
                }
                cases.append(case)
                case_idx += 1

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"Generated {len(cases)} temporal replay evaluation instances in {OUTPUT_FILE}")
    print(f"Years breakdown: { {y: sum(1 for c in cases if c['period_year'] == y) for y in years} }")


if __name__ == "__main__":
    generate_dataset()
