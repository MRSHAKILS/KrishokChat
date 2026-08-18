#!/usr/bin/env python3
"""
Generate vector-sharp, publication-grade System Architecture Diagram
for KrishokChat 4-Stage Safety Pipeline.
"""

import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

FIG_DIR = pathlib.Path(r"d:\KrishokChat Advisory System\capstone\poster deisgn\figures")

def generate_system_architecture():
    fig = plt.figure(figsize=(16, 8.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 85)
    ax.axis('off')

    # Title
    ax.text(80, 80, "KrishokChat: Safety-First Agentic Bengali Agricultural Advisory Pipeline",
            ha='center', va='center', fontsize=18, fontweight='bold', color='#0F172A')

    # Helper for drawing rounded boxes
    def draw_box(x, y, w, h, bg, border, lw=1.5, r=2):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={r}",
                                      facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
        ax.add_patch(rect)

    # 1. INPUT BOX (x=4, y=36, w=22, h=34)
    draw_box(4, 36, 22, 34, '#F8FAFC', '#CBD5E1', lw=1.5)
    ax.text(15, 66, "INPUT", ha='center', va='center', fontsize=11, fontweight='bold', color='#64748B')
    ax.text(15, 57, "Farmer\nMultimodal\nInput", ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')
    ax.plot([6, 24], [48, 48], color='#E2E8F0', lw=1)
    ax.text(15, 42, "Bengali Text /\nDialect Query or\nLeaf Image", ha='center', va='center', fontsize=10, color='#475569', multialignment='center')

    # Arrow 1 -> 2
    ax.annotate('', xy=(31, 53), xytext=(27, 53),
                arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=2, mutation_scale=15), zorder=4)

    # 2. STAGE 1: SAFETY & ROUTER (x=32, y=34, w=29, h=38)
    draw_box(32, 34, 29, 38, '#EEF2FF', '#4F46E5', lw=1.8)
    ax.text(46.5, 68, "STAGE 1", ha='center', va='center', fontsize=11, fontweight='bold', color='#4F46E5')
    ax.text(46.5, 63, "Safety & Policy Router", ha='center', va='center', fontsize=13, fontweight='bold', color='#1E1B4B')
    ax.text(46.5, 57, "Pre-Retrieval Rule Filter +\n6-Way Intent Classifier", ha='center', va='center', fontsize=9.5, color='#4338CA', multialignment='center')

    # 6 Category Chips
    chips = [('[safe_agri]', '#059669', '#ECFDF5'),
             ('[banned_chem]', '#DC2626', '#FEF2F2'),
             ('[self_harm]', '#DC2626', '#FEF2F2'),
             ('[off_topic]', '#D97706', '#FFFBEB'),
             ('[prompt_inj]', '#475569', '#F1F5F9'),
             ('[low_conf]', '#475569', '#F1F5F9')]
    
    cx = [34, 47, 34, 47, 34, 47]
    cy = [48, 48, 43, 43, 38, 38]
    for (lbl, c_text, c_bg), x_c, y_c in zip(chips, cx, cy):
        c_box = patches.FancyBboxPatch((x_c, y_c), 11, 3.2, boxstyle="round,pad=0.6",
                                       facecolor=c_bg, edgecolor=c_text, linewidth=0.8, zorder=3)
        ax.add_patch(c_box)
        ax.text(x_c + 5.5, y_c + 1.6, lbl, ha='center', va='center', fontsize=8, fontweight='bold', color=c_text)

    # RED UNSAFE BRANCH DOWNWARD
    ax.annotate('', xy=(46.5, 23), xytext=(46.5, 33),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.2, mutation_scale=15), zorder=4)
    ax.text(46.5, 28.5, "If Unsafe / Banned / Poisoning", ha='center', va='center', fontsize=9, fontweight='bold', color='#DC2626',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#FECACA", lw=0.8))

    # RED ALERT BOX (x=24, y=5, w=45, h=16)
    draw_box(24, 5, 45, 16, '#FEF2F2', '#DC2626', lw=1.8)
    ax.text(46.5, 16.5, "Zero-Inference Immediate Escalation", ha='center', va='center', fontsize=11, fontweight='bold', color='#991B1B')
    ax.text(46.5, 12, "→ Krishi Call Center: 16123  |  Emergency: 999", ha='center', va='center', fontsize=11, fontweight='800', color='#DC2626')
    ax.text(46.5, 7.5, "Retrieval, Generation & Verifier are 100% BYPASSED", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#7F1D1D')

    # Arrow 2 -> 3
    ax.annotate('', xy=(66, 53), xytext=(62, 53),
                arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=2, mutation_scale=15), zorder=4)

    # 3. STAGE 2: RETRIEVAL (x=67, y=34, w=27, h=38)
    draw_box(67, 34, 27, 38, '#FFFBEB', '#D97706', lw=1.8)
    ax.text(80.5, 68, "STAGE 2", ha='center', va='center', fontsize=11, fontweight='bold', color='#D97706')
    ax.text(80.5, 63, "Hybrid Retrieval", ha='center', va='center', fontsize=13, fontweight='bold', color='#78350F')
    ax.text(80.5, 55, "BM25 + FAISS Dense\nReciprocal Rank Fusion\n(RRF, k=60)", ha='center', va='center', fontsize=9.5, color='#92400E', multialignment='center')
    ax.plot([70, 91], [46, 46], color='#FDE68A', lw=1, linestyle='--')
    ax.text(80.5, 40, "Corpus:\n2,882-Node KG +\n284 Govt. Docs (BARC, DAE)", ha='center', va='center', fontsize=9, color='#78350F', multialignment='center')

    # Arrow 3 -> 4
    ax.annotate('', xy=(99, 53), xytext=(95, 53),
                arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=2, mutation_scale=15), zorder=4)

    # 4. STAGE 3: GENERATION (x=100, y=34, w=26, h=38)
    draw_box(100, 34, 26, 38, '#ECFDF5', '#059669', lw=1.8)
    ax.text(113, 68, "STAGE 3", ha='center', va='center', fontsize=11, fontweight='bold', color='#059669')
    ax.text(113, 63, "Domain Generation", ha='center', va='center', fontsize=13, fontweight='bold', color='#064E3B')
    ax.text(113, 55, "KrishokChat-4B\n(Gemma-4-E4B LoRA)\n4-bit Q4_K_M, bf16", ha='center', va='center', fontsize=9.5, color='#065F46', multialignment='center')
    ax.plot([103, 123], [46, 46], color='#A7F3D0', lw=1, linestyle='--')
    ax.text(113, 40, "Constraint:\nStrict evidence grounding\n0.31% safety compliance", ha='center', va='center', fontsize=9, color='#047857', multialignment='center')

    # Arrow 4 -> 5
    ax.annotate('', xy=(131, 53), xytext=(127, 53),
                arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=2, mutation_scale=15), zorder=4)

    # 5. STAGE 4: VERIFIER (x=132, y=34, w=25, h=38)
    draw_box(132, 34, 25, 38, '#F0F9FF', '#0284C7', lw=1.8)
    ax.text(144.5, 68, "STAGE 4", ha='center', va='center', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(144.5, 63, "14-Field Verifier", ha='center', va='center', fontsize=13, fontweight='bold', color='#0C4A6E')
    ax.text(144.5, 55, "Extracts Atomic Claims\nMatches Dosage, Unit,\nFormulation & PHI", ha='center', va='center', fontsize=9.5, color='#0369A1', multialignment='center')
    ax.plot([135, 154], [46, 46], color='#BAE6FD', lw=1, linestyle='--')
    ax.text(144.5, 40, "Action:\nDrops ungrounded claims\nFail-closed safety policy", ha='center', va='center', fontsize=9, color='#0284C7', multialignment='center')

    # OUTPUT & AUDIT BOX (x=85, y=5, w=72, h=16)
    draw_box(85, 5, 72, 16, '#F8FAFC', '#0F172A', lw=1.5)
    ax.text(121, 16.5, "OUTPUT: Verified Bengali Advisory + Grounded Citations [1..k]",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')
    ax.text(121, 11, "Local Immutable Audit Log (powers /analytics dashboard)",
            ha='center', va='center', fontsize=10, fontweight='600', color='#059669')
    ax.text(121, 7, "Includes: Actionable Dosages · Application Timings · Safety PHI Precautions · Source Provenance",
            ha='center', va='center', fontsize=8.5, color='#64748B')

    # Arrow Stage 4 -> Output
    ax.annotate('', xy=(144.5, 22), xytext=(144.5, 33),
                arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=2, mutation_scale=15), zorder=4)

    plt.tight_layout()
    out_path = FIG_DIR / "F1_system_architecture.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == '__main__':
    generate_system_architecture()
