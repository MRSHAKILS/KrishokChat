#!/usr/bin/env python3
"""Generate the four figures for the KrishokChat CEA paper."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

# Palette (matches LaTeX definecolor)
TEAL   = "#006666"
DARK   = "#182B31"
RED     = "#B42828"
BLUE    = "#1C5AA0"
GREEN   = "#22783C"
LGRAY   = "#F8F9FA"
BORDER  = "#C8CDD2"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": DARK,
    "axes.linewidth": 0.8,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

# -------------------------------------------------------------------
# Figure 1 — Architecture
# -------------------------------------------------------------------
def fig1():
    fig, ax = plt.subplots(figsize=(12, 6.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.4); ax.axis("off")

    def box(x, y, w, h, text, fc, tc="white", fs=9.5, ec=None):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                           linewidth=1.2, edgecolor=ec or fc, facecolor=fc, zorder=2)
        ax.add_patch(p)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                color=tc, fontsize=fs, weight="bold", zorder=3, wrap=True)

    def arrow(x1, y1, x2, y2, color=DARK, style="-|>", lw=1.6):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                     mutation_scale=14, linewidth=lw, color=color, zorder=1))

    # Inputs (left column)
    box(0.2, 4.9, 2.2, 0.8, "Image\n(crop photo)", GREEN)
    box(0.2, 3.5, 2.2, 0.8, "Text query\n(Bengali)", BLUE)
    box(0.2, 2.1, 2.2, 0.8, "SMS / USSD\n(feature phone)", "#8A6D00", tc="white")

    # DGDR core
    box(3.1, 2.9, 2.6, 2.0, "Detection-Gated\nDeterministic\nRouting\n(DGDR)", TEAL, fs=11)

    # Tier ladder
    box(6.4, 5.0, 4.9, 0.62, "T0  Deterministic Safety Guard (6.4%)", RED, fs=9)
    box(6.4, 4.25, 4.9, 0.62, "T1  Detection-Gated Fact Resolution (32.2%)", GREEN, fs=9)
    box(6.4, 3.5, 4.9, 0.62, "T2  Glossary / Templated Advisory (18.8%)", GREEN, fs=9)
    box(6.4, 2.75, 4.9, 0.62, "T3  Grounded Generative RAG — Gemma-4 (38.5%)", BLUE, fs=9)
    box(6.4, 2.0, 4.9, 0.62, "T4  Honest Refusal / 16123 escalation (4.1%)", "#555", fs=9)

    # Verifier (critical path)
    box(6.4, 0.55, 4.9, 1.0, "Fail-Closed Typed Relational Verifier  (11-slot, single-record binding)",
        DARK, fs=9.5)

    # Channels (bottom)
    box(0.2, 0.55, 2.0, 0.9, "Online PWA", TEAL, fs=9)
    box(2.4, 0.55, 2.0, 0.9, "Offline hash-\nchained cache", "#0A4D4D", fs=8.5)

    # Arrows inputs -> DGDR
    for yy in (5.3, 3.9, 2.5):
        arrow(2.4, yy, 3.1, 3.9)
    # DGDR -> tiers
    for yy in (5.31, 4.56, 3.81, 3.06, 2.31):
        arrow(5.7, 3.9, 6.4, yy, color=BORDER, lw=1.1)
    # tiers -> verifier
    arrow(8.85, 2.0, 8.85, 1.55, color=DARK)
    # verifier -> channels
    arrow(6.4, 1.05, 4.4, 1.0, color=DARK)

    ax.text(6.0, 6.15, "LLM (Tier 3) sits OFF the critical path for 61.52% of traffic",
            ha="center", fontsize=10, style="italic", color=RED, weight="bold")
    fig.savefig(os.path.join(OUT, "fig_1_architecture.png"))
    plt.close(fig)

# -------------------------------------------------------------------
# Figure 2 — DGDR decision flow
# -------------------------------------------------------------------
def fig2():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 9); ax.set_ylim(0, 6); ax.axis("off")

    def box(x, y, w, h, text, fc, tc="white", fs=9.5):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                           linewidth=1.2, edgecolor=fc, facecolor=fc, zorder=2)
        ax.add_patch(p)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                color=tc, fontsize=fs, weight="bold", zorder=3)

    def diamond(cx, cy, w, h, text, fc):
        pts = [(cx, cy+h/2), (cx+w/2, cy), (cx, cy-h/2), (cx-w/2, cy)]
        ax.add_patch(plt.Polygon(pts, closed=True, facecolor=fc, edgecolor=fc, zorder=2))
        ax.text(cx, cy, text, ha="center", va="center", color="white",
                fontsize=9, weight="bold", zorder=3)

    def arrow(x1, y1, x2, y2, color=DARK, lw=1.6, label=None, lx=0, ly=0):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                     mutation_scale=13, linewidth=lw, color=color, zorder=1))
        if label:
            ax.text((x1+x2)/2 + lx, (y1+y2)/2 + ly, label, fontsize=8.5,
                    color=color, weight="bold")

    box(3.0, 5.2, 3.0, 0.7, "On-device detect  (c, p, kappa)", GREEN)
    box(3.0, 4.3, 3.0, 0.6, "Intent classify (1.25 MB)", BLUE, fs=9)
    diamond(4.5, 3.2, 3.0, 1.2, "kappa >= 0.80 ?", TEAL)
    box(6.6, 2.6, 2.3, 1.0, "Partition fact base\n2135 -> 516.4\n(-75.6%)", "#0A4D4D", fs=8.5)
    box(0.2, 2.6, 2.3, 1.0, "Text-first\nhybrid retrieval\n(fallback)", "#8A6D00", fs=8.5)
    box(6.6, 1.2, 2.3, 0.9, "<=3-hop traverse\n0 LLM calls", GREEN, fs=8.5)
    box(3.2, 0.3, 2.6, 0.8, "Fail-Closed Verifier", DARK, fs=9.5)

    arrow(4.5, 5.2, 4.5, 4.9)
    arrow(4.5, 4.3, 4.5, 3.8)
    arrow(6.0, 3.2, 6.6, 3.1, color=GREEN, label="yes", lx=-0.15, ly=0.15)
    arrow(3.0, 3.2, 2.5, 3.1, color=RED, label="no", lx=-0.1, ly=0.15)
    arrow(7.75, 2.6, 7.75, 2.1)
    arrow(7.75, 1.2, 4.5, 1.1, color=DARK)
    arrow(1.35, 2.6, 3.2, 0.9, color="#8A6D00")

    fig.savefig(os.path.join(OUT, "fig_2_dgdr.png"))
    plt.close(fig)

# -------------------------------------------------------------------
# Figure 3 — Tier mix (donut)
# -------------------------------------------------------------------
def fig3():
    fig, ax = plt.subplots(figsize=(8, 5.4))
    labels = ["T1 Fact (32.2%)", "T2 Templated (18.8%)", "T0 Safety (6.4%)",
              "T4 Refusal (4.1%)", "T3 Generative RAG (38.5%)"]
    sizes  = [32.22, 18.82, 6.4, 4.08, 38.48]
    colors = [GREEN, "#2E9E52", RED, "#777777", BLUE]
    explode = [0.03, 0.03, 0.03, 0.03, 0.0]
    wedges, _ = ax.pie(sizes, colors=colors, startangle=90, counterclock=False,
                       explode=explode, wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
    ax.text(0, 0.12, "61.52%", ha="center", va="center", fontsize=22, weight="bold", color=DARK)
    ax.text(0, -0.22, "zero-LLM\nresolution", ha="center", va="center", fontsize=11, color=DARK)
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1.02, 0.5),
              frameon=False, fontsize=10)
    ax.set_aspect("equal")
    fig.savefig(os.path.join(OUT, "fig_3_tier_mix.png"))
    plt.close(fig)

# -------------------------------------------------------------------
# Figure 4 — Delivery by network profile
# -------------------------------------------------------------------
def fig4():
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    profiles = ["Perfect\n4G\n0%", "Urban\n3G\n5%", "Rural\nEdge\n15%", "Severe\n2G\n30%"]
    ours  = np.array([100.0, 99.8, 91.4, 58.1])
    cloud = np.array([100.0, 99.6, 82.0, 12.8])
    x = np.arange(len(profiles))
    width = 0.34
    b1 = ax.bar(x - width/2, cloud, width, color=RED, alpha=0.88, label="Cloud-only RAG")
    b2 = ax.bar(x + width/2, ours, width, color=TEAL, alpha=0.92, label="Offline-first cache")
    ax.bar_label(b1, fmt="%.1f", padding=2, fontsize=8)
    ax.bar_label(b2, fmt="%.1f", padding=2, fontsize=8)
    ax.annotate("+45.3 pp", xy=(3 + width/2, 58.1), xytext=(2.3, 72),
                arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2),
                color=DARK, weight="bold", fontsize=10)
    ax.set_xticks(x, profiles, fontsize=9)
    ax.set_xlabel("Simulated network profile and packet loss", fontsize=11)
    ax.set_ylabel("Advisory delivery rate (%)", fontsize=11)
    ax.set_ylim(0, 105); ax.set_xlim(-1, 31)
    ax.set_xlim(-0.65, len(profiles)-0.35)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    fig.savefig(os.path.join(OUT, "fig_4_network.png"))
    plt.close(fig)

# -------------------------------------------------------------------
# Figure 5 — SMS safety-slot survival
# -------------------------------------------------------------------
def fig5():
    fig, ax = plt.subplots(figsize=(10, 3.8))
    slots = ["crop", "pest", "active", "formulation", "dose", "unit", "volume", "interval", "PHI", "helpline"]
    template = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100])
    llm      = np.array([100, 100, 100, 79.0, 86.4, 79.0, 100, 62.9, 35.6, 41.9])
    naive    = np.array([100, 100, 0, 0, 0, 0, 0, 0, 0, 0])
    data = np.vstack([template, llm, naive])
    im = ax.imshow(data, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(np.arange(len(slots)), slots, rotation=35, ha="right", fontsize=9)
    ax.set_yticks(np.arange(3), ["Deterministic template", "LLM-composed", "Naive truncation"], fontsize=9)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            color = "white" if val < 45 else DARK
            ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8, color=color, weight="bold")
    ax.set_xlabel("Safety-critical message slot", fontsize=11)
    ax.set_title("Tested slot survival within the GSM-160 composition budget", fontsize=11, pad=10)
    cb = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.025)
    cb.set_label("Survival (%)", fontsize=9)
    fig.savefig(os.path.join(OUT, "fig_5_sms_slots.png"))
    plt.close(fig)

fig1(); fig2(); fig3(); fig4(); fig5()
print("all figures written to", OUT)
