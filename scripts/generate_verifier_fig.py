#!/usr/bin/env python3
"""
Generate publication-sharp 300 DPI diagram of the 14-Field Atomic Claim Verifier Schema
using Nirmala UI / Segoe UI for native Bengali glyph rendering.
"""

import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'Nirmala UI'
plt.rcParams['font.sans-serif'] = ['Nirmala UI', 'Segoe UI', 'Arial']

FIG_DIR = pathlib.Path(r"d:\KrishokChat Advisory System\capstone\poster-design\figures")

def generate_verifier_schema():
    fig = plt.figure(figsize=(12, 16), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 160)
    ax.axis('off')

    def draw_box(x, y, w, h, bg, border, lw=1.2, r=1.5):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={r}",
                                      facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
        ax.add_patch(rect)

    # Main Title
    ax.text(60, 154, "Structured Claim Grounding & Verification Engine",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(60, 149, "Deterministic 14-field extraction and 6-relation factual entailment pipeline",
            ha='center', va='center', fontsize=11, color='#64748B')

    # SECTION 1: Generated Text Extraction Example
    draw_box(4, 124, 112, 20, '#F8FAFC', '#CBD5E1', lw=1.4)
    ax.text(8, 140, "1   Generated Advisory Extraction Example", fontsize=11, fontweight='bold', color='#1E293B')
    ax.text(60, 134, "“ধানের ব্লাইট দমনে ট্রাইসাইক্লাজোল ৭৫ ডব্লিউপি প্রতি লিটার পানিতে ০.৮ গ্রাম মিশিয়ে স্প্রে করুন (PHI: ১৪ দিন)”",
            ha='center', va='center', fontsize=11.5, fontweight='bold', color='#0F172A')
    ax.text(60, 127.5, "(Model Output / Generated Agrochemical Advisory Sentence)",
            ha='center', va='center', fontsize=9.5, style='italic', color='#64748B')

    # SECTION 2: 14-Field Normalized Claim Slot Schema
    draw_box(4, 52, 112, 68, '#FFFFFF', '#CBD5E1', lw=1.4)
    ax.text(8, 116, "2   14-Field Normalized Atomic Chemical Claim (Slot Schema)", fontsize=11, fontweight='bold', color='#1E293B')

    # 2A: Entity Anchors (Green)
    draw_box(6, 92, 108, 20, '#F0FDF4', '#86EFAC', lw=1.2)
    ax.text(10, 107, "ENTITY ANCHORS (Non-Quantitative)", fontsize=9.5, fontweight='bold', color='#166534')
    slots_green = [
        ("1. crop", "ধান", "Target crop"),
        ("2. disease", "ব্লাইট", "Target pathogen"),
        ("3. action", "দমন", "Intended effect"),
        ("4. chemical", "ট্রাইসাইক্লাজোল", "Active ingredient"),
        ("5. polarity", "affirmative", "Claim stance")
    ]
    for i, (name, val, desc) in enumerate(slots_green):
        x = 10 + i * 21.5
        ax.text(x, 99.5, name, fontsize=8.5, fontweight='bold', color='#14532D')
        ax.text(x, 94.5, f"[{val}]", fontsize=8.5, fontweight='bold', color='#059669')

    # 2B: Safety-Critical Quantitative Fields (Orange/Alert)
    draw_box(6, 64, 108, 25, '#FFFBEB', '#F59E0B', lw=1.5)
    ax.text(10, 84, "⚠️ SAFETY-CRITICAL QUANTITATIVE FIELDS (Strict Entailment Required)", fontsize=9.5, fontweight='bold', color='#B45309')
    slots_orange = [
        ("6. formulation", "75 WP", "Formulation type"),
        ("7. amount", "0.8", "Dose quantity"),
        ("8. unit", "g", "Metric unit"),
        ("9. denom", "1 L water", "Carrier volume"),
        ("10. interval", "7-10 days", "Repeat frequency"),
        ("11. PHI_safety", "14 days", "Pre-harvest safety")
    ]
    for i, (name, val, desc) in enumerate(slots_orange):
        x = 10 + (i % 3) * 36
        y = 76 if i < 3 else 68
        ax.text(x, y + 2.5, name, fontsize=8.5, fontweight='bold', color='#92400E')
        ax.text(x + 18, y + 2.5, f"→ {val}", fontsize=8.5, fontweight='bold', color='#D97706')

    # 2C: Meta & Grounding
    draw_box(6, 54, 108, 8, '#F8FAFC', '#E2E8F0', lw=1)
    ax.text(10, 58, "META:  12. applicability: standing_crop  |  13. uncertainty: 0.0  |  14. source_id: DAE_Rice_P14",
            fontsize=8.5, fontweight='600', color='#475569')

    # SECTION 3: 6-Way Factual Entailment Matcher Table
    draw_box(4, 4, 112, 44, '#FFFFFF', '#CBD5E1', lw=1.4)
    ax.text(8, 44, "3   6-Way Factual Entailment Matcher (Evidence ↔ Claim Slot)", fontsize=11, fontweight='bold', color='#1E293B')

    table_data = [
        ("SUPPORTED", "Evidence fully supports claim slot", "Keep claim as-is", "PASS", "#059669", "#ECFDF5"),
        ("CONTRADICTED", "Evidence explicitly contradicts claim", "Drop claim & trigger alert", "DROP & ALERT", "#DC2626", "#FEF2F2"),
        ("PARTIALLY_SUPP.", "Partial support (e.g. chem ok, dose off)", "Strip unverified dosage", "STRIP & KEEP", "#D97706", "#FFFBEB"),
        ("UNSUPPORTED", "No evidence found for claim slot", "Drop claim entirely", "DROP", "#DC2626", "#FEF2F2"),
        ("AMBIGUOUS", "Conflicting or insufficient evidence", "Fail-closed → 16123 referral", "FAIL-CLOSED", "#475569", "#F1F5F9"),
        ("NOT_APPLICABLE", "Not applicable to context/crop stage", "Informational exclusion", "INFORMATIONAL", "#475569", "#F1F5F9")
    ]

    # Table Header
    ax.plot([6, 114], [40, 40], color='#CBD5E1', lw=1)
    ax.text(8, 41.5, "Relation", fontsize=9, fontweight='bold', color='#64748B')
    ax.text(32, 41.5, "Semantic Meaning", fontsize=9, fontweight='bold', color='#64748B')
    ax.text(70, 41.5, "Action in KrishokChat", fontsize=9, fontweight='bold', color='#64748B')
    ax.text(98, 41.5, "Status", fontsize=9, fontweight='bold', color='#64748B')

    for i, (rel, mean, act, stat, c_text, c_bg) in enumerate(table_data):
        y = 35.5 - i * 5.8
        ax.text(8, y, rel, fontsize=8.5, fontweight='bold', color='#0F172A')
        ax.text(32, y, mean, fontsize=8, color='#334155')
        ax.text(70, y, act, fontsize=8, fontweight='600', color='#0F172A')
        
        # Pill
        p_box = patches.FancyBboxPatch((96, y - 1.2), 16, 3.8, boxstyle="round,pad=0.4",
                                       facecolor=c_bg, edgecolor=c_text, linewidth=0.8, zorder=3)
        ax.add_patch(p_box)
        ax.text(104, y + 0.6, stat, ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_text)
        
        if i < len(table_data) - 1:
            ax.plot([6, 114], [y - 2.5, y - 2.5], color='#F1F5F9', lw=0.8)

    plt.tight_layout()
    out_path = FIG_DIR / "F4_verifier_schema.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == '__main__':
    generate_verifier_schema()
