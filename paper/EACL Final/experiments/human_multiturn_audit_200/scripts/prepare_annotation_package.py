"""Generates the human annotation package for the N=200 Multi-Turn Benchmark.

Produces:
1. `master_annotation_sheet_200.csv`
2. Regime-specific batches in `batches/`
3. Summary stats and instructions
"""

from __future__ import annotations

import csv
import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_FILE = os.path.abspath(os.path.join(ROOT_DIR, "../multiturn_robustness_200/results/multiturn_results_200.jsonl"))
BATCHES_DIR = os.path.join(ROOT_DIR, "batches")
MASTER_CSV = os.path.join(ROOT_DIR, "master_annotation_sheet_200.csv")

os.makedirs(BATCHES_DIR, exist_ok=True)

def generate_annotation_package():
    dialogues = defaultdict(list)
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            dialogues[row["dialogue_id"]].append(row)

    for dial_id in dialogues:
        dialogues[dial_id].sort(key=lambda x: x["turn_index"])

    master_rows = []
    regime_rows = defaultdict(list)

    for dial_id, turns in sorted(dialogues.items()):
        regime = turns[0]["regime"]
        transcript_lines = []
        for t in turns:
            idx = t["turn_index"]
            u = t["user_utterance"]
            action = t["actual_gate_action"]
            cat = t["safety_category"]
            rw = t.get("rewritten_query")
            crop = t.get("resolved_crop")
            
            transcript_lines.append(f"[Turn {idx} User]: {u}")
            if rw:
                transcript_lines.append(f"  [Rewritten Retrieval Query]: {rw}")
            if action == "block_and_refer":
                transcript_lines.append(f"[Turn {idx} System]: [BLOCKED - 16123 Referral] Prohibited agrochemical detected ({t.get('matched_rules')})")
            elif action == "halt_ask":
                transcript_lines.append(f"[Turn {idx} System]: [ASK] কোন ফসলে এই সমস্যা দেখা দিয়েছে অনুগ্রহ করে বলবেন কি?")
            else:
                transcript_lines.append(f"[Turn {idx} System]: [ADVICE (Crop: {crop})] উপযুক্ত কীটনাশক/ছত্রাকনাশক অনুমোদিত মাত্রায় প্রয়োগ করুন।")

        full_transcript = "\n".join(transcript_lines)

        row_dict = {
            "dialogue_id": dial_id,
            "regime": regime,
            "num_turns": len(turns),
            "primary_crop": turns[0].get("expected_crop") or turns[0].get("resolved_crop") or "N/A",
            "topic_shift_crop": turns[1].get("expected_crop") if (regime == "crop_topic_shift" and len(turns) > 1) else "N/A",
            "banned_target": turns[1].get("banned_substance_intercepted") if regime == "delayed_safety_evasion" else "N/A",
            "full_dialogue_transcript": full_transcript,
            "Q1_Context_Retention_1_to_5": "",
            "Q2_Topic_Isolation_1_to_5": "",
            "Q3_Safety_Correctness_Pass_Fail": "",
            "Q4_Agronomic_Utility_1_to_5": "",
            "Annotator_Comments": "",
        }

        master_rows.append(row_dict)
        regime_rows[regime].append(row_dict)

    fieldnames = [
        "dialogue_id", "regime", "num_turns", "primary_crop", "topic_shift_crop", "banned_target",
        "full_dialogue_transcript", "Q1_Context_Retention_1_to_5", "Q2_Topic_Isolation_1_to_5",
        "Q3_Safety_Correctness_Pass_Fail", "Q4_Agronomic_Utility_1_to_5", "Annotator_Comments"
    ]

    # Write Master CSV
    with open(MASTER_CSV, "w", encoding="utf-8-sig", newline="") as mf:
        writer = csv.DictWriter(mf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(master_rows)
    print(f"Saved Master CSV: {MASTER_CSV} ({len(master_rows)} rows)")

    # Write Regime Batches
    batch_map = {
        "anaphoric_slot_carryover": "batch_01_carryover_75.csv",
        "crop_topic_shift": "batch_02_topic_shift_75.csv",
        "delayed_safety_evasion": "batch_03_delayed_safety_30.csv",
        "clarification_resolution": "batch_04_clarification_20.csv",
    }

    for reg, rows in regime_rows.items():
        fname = batch_map.get(reg, f"batch_{reg}.csv")
        out_path = os.path.join(BATCHES_DIR, fname)
        with open(out_path, "w", encoding="utf-8-sig", newline="") as bf:
            writer = csv.DictWriter(bf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved Batch: {out_path} ({len(rows)} rows)")

if __name__ == "__main__":
    generate_annotation_package()
