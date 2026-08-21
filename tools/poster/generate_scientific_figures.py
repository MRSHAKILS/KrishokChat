#!/usr/bin/env python3
"""
Generate publication-grade, ultra-sharp 300 DPI scientific figures
for the KrishokChat Capstone Poster using real experimental data.
"""

import os
import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd

# Set global styles
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

FIG_DIR = pathlib.Path(r"d:\KrishokChat Advisory System\capstone\poster-design\figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def generate_benchmark_charts():
    """Generate dual-panel benchmark figure: Retrieval R@10 & Model GenF1."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    
    # -------------------------------------------------------------
    # Panel A: Retrieval Recall@10
    # -------------------------------------------------------------
    models_a = ['BGE-M3', 'Dense\nGemini-001', 'ColBERT\n(Late Inter.)', 'BM25\n(Lexical)', 'Hybrid RRF\n(Ours)']
    scores_a = [0.408, 0.464, 0.487, 0.506, 0.539]
    colors_a = ['#94A3B8', '#64748B', '#475569', '#334155', '#059669']
    
    y_pos_a = np.arange(len(models_a))
    bars_a = ax1.barh(y_pos_a, scores_a, color=colors_a, height=0.55, edgecolor='none', zorder=3)
    
    # Labels at bar ends
    for bar, score in zip(bars_a, scores_a):
        ax1.text(score + 0.012, bar.get_y() + bar.get_height()/2, f"{score:.3f}",
                 va='center', ha='left', fontsize=12, fontweight='bold',
                 color='#059669' if score == 0.539 else '#1E293B')
        
    ax1.set_xlim(0, 0.65)
    ax1.set_yticks(y_pos_a)
    ax1.set_yticklabels(models_a, fontsize=11, fontweight='500')
    ax1.set_xlabel('Recall @ 10 (Higher is Better)', fontsize=12, fontweight='600', color='#0F172A', labelpad=8)
    ax1.set_title('A    Retrieval Recall@10 across 900 Answerable Queries', fontsize=13, fontweight='bold', color='#0F172A', loc='left', pad=12)
    
    ax1.grid(axis='x', linestyle='--', alpha=0.5, color='#E2E8F0', zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_facecolor('#FFFFFF')
    
    # Annotation Callout
    ax1.annotate('+9% gain over dense (p < 0.001)\nDense collapses on dialect (R@10=0.093)',
                 xy=(0.506, 3), xytext=(0.32, 1.2),
                 arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.5, connectionstyle="arc3,rad=-0.2"),
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1),
                 fontsize=10, fontweight='600', color='#0F172A')

    # -------------------------------------------------------------
    # Panel B: Closed-Book General QA Token F1
    # -------------------------------------------------------------
    models_b = ['Gemma-4-26B', 'Gemini-2.5\nFlash-Lite', 'LLaMA-3.1-8B\n(Zero-Shot)', 'KrishokChat-4B\n(LoRA, Ours)']
    scores_b = [0.087, 0.104, 0.165, 0.314]
    colors_b = ['#94A3B8', '#64748B', '#334155', '#059669']
    
    y_pos_b = np.arange(len(models_b))
    bars_b = ax2.barh(y_pos_b, scores_b, color=colors_b, height=0.55, edgecolor='none', zorder=3)
    
    for bar, score in zip(bars_b, scores_b):
        ax2.text(score + 0.008, bar.get_y() + bar.get_height()/2, f"{score:.3f}",
                 va='center', ha='left', fontsize=12, fontweight='bold',
                 color='#059669' if score == 0.314 else '#1E293B')
        
    ax2.set_xlim(0, 0.40)
    ax2.set_yticks(y_pos_b)
    ax2.set_yticklabels(models_b, fontsize=11, fontweight='500')
    ax2.set_xlabel('Token F1 Score (Higher is Better)', fontsize=12, fontweight='600', color='#0F172A', labelpad=8)
    ax2.set_title('B    Closed-Book General QA Token F1 Score', fontsize=13, fontweight='bold', color='#0F172A', loc='left', pad=12)
    
    ax2.grid(axis='x', linestyle='--', alpha=0.5, color='#E2E8F0', zorder=0)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_facecolor('#FFFFFF')
    
    # Callout Box
    ax2.text(0.22, 1.2,
             "1.9× GenF1 improvement (p ≈ 6.7e-5)\n────────────────────────\nSafety violation rate: 0.31% (1/323)\nLowest harmful compliance across models",
             bbox=dict(boxstyle="round,pad=0.6", facecolor="#ECFDF5", edgecolor="#A7F3D0", lw=1.2),
             fontsize=10, fontweight='600', color='#065F46')

    plt.tight_layout(pad=2.0)
    out_path = FIG_DIR / "F2_benchmark_evaluation_charts.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def generate_soil_scatter():
    """Generate publication-grade Soil Moisture Scatter Plot from real CSV data."""
    csv_path = pathlib.Path(r"d:\KrishokChat Advisory System\backend\ml_assets\soil\oof_predictions.csv")
    if not csv_path.exists():
        print("Soil CSV not found, skipping scatter.")
        return
        
    df = pd.read_csv(csv_path)
    
    fig, ax = plt.subplots(figsize=(7, 6.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # Map soil types to clean names and distinct colors
    soil_palette = {
        'Atel': '#B45309',       # Clay - Terracotta
        'Doash': '#059669',      # Loam - Emerald
        'Bele-Doash': '#D97706', # Sandy Loam - Amber
        'Atel-Doash': '#854D0E', # Clay Loam - Dark amber
        'Poli': '#0284C7',       # Silt - Sky Blue
        'Bele': '#DC2626'        # Sandy - Crimson
    }
    
    # Plot points by soil type
    if 'SOIL_TYPE' in df.columns:
        for stype, color in soil_palette.items():
            sub = df[df['SOIL_TYPE'] == stype]
            if len(sub) > 0:
                ax.scatter(sub['Kpa'], sub['oof_pred'], label=f"{stype} (n={len(sub)})",
                           color=color, alpha=0.65, edgecolors='none', s=45, zorder=3)
    else:
        ax.scatter(df['Kpa'], df['oof_pred'], color='#059669', alpha=0.6, s=40, zorder=3)
        
    # Diagonal ideal line
    lims = [0, 24]
    ax.plot(lims, lims, '--', color='#0F172A', alpha=0.85, lw=1.8, label='Perfect Prediction (y = x)', zorder=4)
    
    ax.set_xlim(-0.5, 23.5)
    ax.set_ylim(-1.5, 28.5)
    ax.set_xlabel('Ground Truth Tensiometer Moisture (kPa)', fontsize=12, fontweight='600', color='#0F172A', labelpad=8)
    ax.set_ylabel('EfficientNet-B0 Predicted Moisture (kPa)', fontsize=12, fontweight='600', color='#0F172A', labelpad=8)
    ax.set_title('EfficientNet-B0 In-Situ Soil Moisture (5-Fold CV, N=693)', fontsize=13, fontweight='bold', color='#0F172A', pad=12)
    
    ax.grid(True, linestyle='--', alpha=0.4, color='#E2E8F0', zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Legend
    legend = ax.legend(loc='upper left', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9.5)
    legend.get_frame().set_linewidth(0.8)
    
    # Stats Callout Box
    stats_text = (
        "5-Fold OOF Metrics:\n"
        "• Cross-Val R² = 0.394 (Best: 0.52)\n"
        "• RMSE = 4.09 kPa (vs 5.26 Baseline)\n"
        "• MAE = 3.19 kPa\n"
        "• 22.1% Error Reduction over Mean"
    )
    ax.text(0.97, 0.05, stats_text, transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#FEF3C7", edgecolor="#FCD34D", lw=1.2),
            fontsize=10, fontweight='600', color='#92400E')
            
    plt.tight_layout()
    out_path = FIG_DIR / "F6_soil_moisture_scatter.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    generate_benchmark_charts()
    generate_soil_scatter()
    print("All scientific figures successfully generated!")
