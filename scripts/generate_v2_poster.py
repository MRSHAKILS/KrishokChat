#!/usr/bin/env python3
"""
Generate the finalized, pixel-perfect A0 Poster HTML for KrishokChat.
Calibrated for exact 841mm x 1189mm single-page print budget.
"""
import pathlib

POSTER_PATH = pathlib.Path(r"d:\KrishokChat Advisory System\capstone\poster deisgn\poster.html")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>KrishokChat — Capstone Innovation Challenge A0 Poster</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Tiro+Bangla:ital@0;1&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet"/>
<style>
/* =========================================================
   A0 POSTER MASTER SPECIFICATION
   Dimensions: 841 mm × 1189 mm (A0 Portrait)
   Strict Single-Page Print Layout
   ========================================================= */

:root {
  --bg-main: #f8fafc;
  --bg-card: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-muted: #64748b;
  
  --emerald-dark: #065f46;
  --emerald-primary: #059669;
  --emerald-light: #ecfdf5;
  --emerald-border: #a7f3d0;
  
  --navy-dark: #0f172a;
  --navy-primary: #1e293b;
  
  --amber-primary: #d97706;
  --amber-light: #fffbeb;
  
  --crimson-primary: #dc2626;
  --crimson-light: #fef2f2;
  
  --border-card: #e2e8f0;
  --border-subtle: #cbd5e1;
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.03);
  --shadow-md: 0 4px 10px rgba(15, 23, 42, 0.05);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

@page {
  size: 841mm 1189mm;
  margin: 0;
}

html, body {
  width: 841mm;
  height: 1189mm;
  background: var(--bg-main);
  color: var(--text-primary);
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.3;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  overflow: hidden;
}

.poster-canvas {
  width: 841mm;
  height: 1189mm;
  padding: 10mm 12mm 8mm 12mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: var(--bg-main);
}

/* =========================================================
   1. HEADER & TITLE BLOCK
   ========================================================= */
.header-card {
  background: #ffffff;
  border: 1px solid var(--border-card);
  border-radius: 5mm;
  padding: 6mm 10mm;
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  gap: 8mm;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.header-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2.2mm;
  background: linear-gradient(90deg, #059669 0%, #0284c7 45%, #d97706 100%);
}

.header-logo {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-logo img {
  height: 28mm;
  width: auto;
  object-fit: contain;
}

.header-text {
  flex: 1;
}

.title-badge-row {
  display: flex;
  align-items: center;
  gap: 3mm;
  margin-bottom: 1.8mm;
}

.conference-badge {
  background: var(--emerald-light);
  color: var(--emerald-dark);
  border: 1px solid var(--emerald-border);
  font-size: 4.2mm;
  font-weight: 700;
  padding: 0.8mm 3.5mm;
  border-radius: 1.5mm;
  letter-spacing: 0.15mm;
  text-transform: uppercase;
}

.poster-title {
  font-size: 10.5mm;
  font-weight: 800;
  color: var(--navy-dark);
  line-height: 1.15;
  letter-spacing: -0.25mm;
  margin-bottom: 1.5mm;
}

.poster-title span {
  color: var(--emerald-primary);
}

.poster-subtitle {
  font-size: 5mm;
  font-weight: 500;
  color: var(--text-secondary);
  line-height: 1.25;
  margin-bottom: 2.5mm;
}

.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #f1f5f9;
  padding-top: 2mm;
  font-size: 4.2mm;
}

.author-names {
  font-weight: 700;
  color: var(--navy-dark);
}

.advisor-affil {
  color: var(--text-muted);
  font-weight: 500;
}

.advisor-affil strong {
  color: var(--navy-primary);
}

/* =========================================================
   2. HERO STAT RIBBON
   ========================================================= */
.stat-ribbon {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 3.5mm;
  flex-shrink: 0;
}

.stat-chip {
  background: #ffffff;
  border: 1px solid var(--border-card);
  border-radius: 3.5mm;
  padding: 2.8mm 2.5mm;
  text-align: center;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-chip.highlight {
  background: #0f172a;
  border-color: #0f172a;
}

.stat-chip.highlight .stat-val {
  color: #38bdf8;
}

.stat-chip.highlight .stat-lbl {
  color: #94a3b8;
}

.stat-val {
  font-size: 7.5mm;
  font-weight: 800;
  color: var(--emerald-primary);
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
  margin-bottom: 0.6mm;
}

.stat-chip:nth-child(3) .stat-val { color: #d97706; }
.stat-chip:nth-child(5) .stat-val { color: #dc2626; }

.stat-lbl {
  font-size: 3mm;
  font-weight: 600;
  color: var(--text-secondary);
  line-height: 1.2;
  text-transform: uppercase;
  letter-spacing: 0.12mm;
}

/* =========================================================
   3. FIGURE CARDS & GRID STRUCTURES
   ========================================================= */
.section-box {
  background: #ffffff;
  border: 1px solid var(--border-card);
  border-radius: 4.5mm;
  box-shadow: var(--shadow-sm);
  padding: 3mm;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.figure-img-wrap {
  width: 100%;
  height: 100%;
  border-radius: 3mm;
  overflow: hidden;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.figure-img-wrap img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: contain;
}

/* Row 1: Hero Architecture */
.row-hero-pipeline {
  height: 195mm;
  flex-shrink: 0;
}

/* Row 2: Benchmark Charts + Claim Verifier Schema */
.row-research-grid {
  display: grid;
  grid-template-columns: 1.08fr 0.92fr;
  gap: 4.5mm;
  height: 255mm;
  flex-shrink: 0;
}

/* Row 3: Multimodal Vision + Soil Moisture */
.row-product-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4.5mm;
  height: 235mm;
  flex-shrink: 0;
}

/* Row 4: Business Model & Scalability */
.row-business-grid {
  height: 215mm;
  flex-shrink: 0;
}

/* =========================================================
   4. FOOTER STRIP
   ========================================================= */
.footer-strip {
  background: #0f172a;
  color: #94a3b8;
  border-radius: 3.5mm;
  padding: 3.5mm 7mm;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 3.4mm;
  line-height: 1.35;
  flex-shrink: 0;
}

.footer-refs {
  flex: 1;
  padding-right: 6mm;
}

.footer-refs strong {
  color: #f8fafc;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 5mm;
  flex-shrink: 0;
  border-left: 1px solid #334155;
  padding-left: 5mm;
}

.helpline-badge {
  background: #dc2626;
  color: #ffffff;
  font-weight: 800;
  padding: 1.2mm 3mm;
  border-radius: 1.5mm;
  font-size: 3.6mm;
}

.qr-code-pill {
  background: #1e293b;
  color: #38bdf8;
  border: 1px solid #38bdf8;
  padding: 0.8mm 2.5mm;
  border-radius: 1.5mm;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  font-size: 3mm;
}

/* Print Rules */
@media print {
  html, body {
    width: 841mm;
    height: 1189mm;
    overflow: hidden;
  }
  .poster-canvas {
    page-break-inside: avoid;
    break-inside: avoid;
  }
}
</style>
</head>
<body>

<div class="poster-canvas">

  <!-- 1. HEADER & TITLE BLOCK -->
  <header class="header-card">
    <div class="header-logo">
      <img src="screenshots/nsu_logo.png" alt="North South University Logo"/>
    </div>
    
    <div class="header-text">
      <div class="title-badge-row">
        <span class="conference-badge">Capstone Design &amp; Innovation Challenge 2026</span>
        <span class="conference-badge" style="background:#e0f2fe;color:#0369a1;border-color:#bae6fd;">Track: AI &amp; Agri-Tech</span>
      </div>
      
      <h1 class="poster-title">
        <span>KrishokChat:</span> A Safety-First Agentic Agricultural Advisory System for Bangladeshi Smallholder Farmers
      </h1>
      
      <div class="poster-subtitle">
        Field-Collected Multimodal Datasets &bull; Four-Stage Verified Bengali AI Pipeline &bull; 85,979-Instance Provenance-Traced Benchmark &bull; National 16123 Escalation Gate
      </div>
      
      <div class="meta-row">
        <div class="author-names">
          Khan Raiyan Ibne Reza &nbsp;&bull;&nbsp; Sanjana Aktar Maria &nbsp;&bull;&nbsp; Shakil Ahmed
        </div>
        <div class="advisor-affil">
          Faculty Advisor: <strong>Dr. Sumaiya Tabassum Nimi (STI)</strong> &nbsp;&bull;&nbsp; Dept. of Electrical &amp; Computer Engineering (ECE) &nbsp;&bull;&nbsp; <strong>North South University</strong>
        </div>
      </div>
    </div>
  </header>

  <!-- 2. HERO STAT RIBBON -->
  <section class="stat-ribbon">
    <div class="stat-chip">
      <div class="stat-val">85,979</div>
      <div class="stat-lbl">Benchmark Instances<br>4 Tracks &bull; CC-BY-4.0</div>
    </div>
    
    <div class="stat-chip">
      <div class="stat-val">95–97%</div>
      <div class="stat-lbl">Top-1 Disease Accuracy<br>5 Crop Families (AgriVision)</div>
    </div>
    
    <div class="stat-chip">
      <div class="stat-val">R² = 0.39</div>
      <div class="stat-lbl">Soil Moisture CV R²<br>22.1% Error Reduction (EffNet)</div>
    </div>
    
    <div class="stat-chip highlight">
      <div class="stat-val">4-Stage</div>
      <div class="stat-lbl">Agent Pipeline<br>Pre-Retrieval Safety Gate</div>
    </div>
    
    <div class="stat-chip">
      <div class="stat-val">16123</div>
      <div class="stat-lbl">Krishi Call Center<br>Automated Triage Gate</div>
    </div>
    
    <div class="stat-chip">
      <div class="stat-val">2 Papers</div>
      <div class="stat-lbl">EACL '26 &bull; SIGIR-AP '26<br>Under Peer Review</div>
    </div>
  </section>

  <!-- 3. ROW 1: HERO 4-STAGE SAFETY PIPELINE SCHEMATIC -->
  <section class="section-box row-hero-pipeline">
    <div class="figure-img-wrap">
      <img src="v2 images/The Hero 4-Stage Safety Architecture Pipeline.png" alt="KrishokChat 4-Stage Safety Architecture Pipeline Diagram"/>
    </div>
  </section>

  <!-- 4. ROW 2: BENCHMARK EVALUATION & 14-FIELD VERIFIER -->
  <section class="row-research-grid">
    <div class="section-box">
      <div class="figure-img-wrap">
        <img src="v2 images/Publication-Grade Multi-Panel Benchmark Charts.png" alt="Publication-Grade Benchmark Evaluation Charts"/>
      </div>
    </div>

    <div class="section-box">
      <div class="figure-img-wrap">
        <img src="v2 images/The 14-Field Atomic Claim Verifier Schema.png" alt="14-Field Atomic Claim Verifier Schema Diagram"/>
      </div>
    </div>
  </section>

  <!-- 5. ROW 3: MULTIMODAL VISION & SOIL MOISTURE FIELDWORK -->
  <section class="row-product-grid">
    <div class="section-box">
      <div class="figure-img-wrap">
        <img src="v2 images/Crop Disease Multimodal Vision & Edge Architecture.png" alt="AgriVision BD Crop Disease Edge Architecture"/>
      </div>
    </div>

    <div class="section-box">
      <div class="figure-img-wrap">
        <img src="v2 images/Soil Moisture Pabna Fieldwork & EffNet-B0 Regression.png" alt="Pabna District Soil Moisture Field Dataset and Regression Modeling"/>
      </div>
    </div>
  </section>

  <!-- 6. ROW 4: BUSINESS MODEL, MARKET READINESS & SCALE -->
  <section class="section-box row-business-grid">
    <div class="figure-img-wrap">
      <img src="v2 images/Business Model, Market Readiness & Scalability.png" alt="KrishokChat Sustainable Business Model and National Scaling Architecture"/>
    </div>
  </section>

  <!-- 7. FOOTER STRIP: CITATIONS & ACCREDITATION -->
  <footer class="footer-strip">
    <div class="footer-refs">
      <strong>References &amp; Provenance:</strong> [1] <em>KrishokChat: A Provenance-Traceable Bengali Agricultural Benchmark</em> (EACL 2026, under review) &bull; [2] <em>AgriTrust: Verified Bengali Agronomic Advisory via Structured Claim Grounding</em> (SIGIR-AP 2026, under review) &bull; [3] <em>AgriVision BD Project Report</em> &bull; Datasets released under CC-BY-4.0 on HuggingFace: <code>RaiyanKhaan/KrishokChat-Advisory-System</code>.
    </div>
    
    <div class="footer-right">
      <span class="qr-code-pill">HF: RaiyanKhaan/KrishokChat</span>
      <span class="helpline-badge">Emergency Triage: 16123 / 999</span>
    </div>
  </footer>

</div>

</body>
</html>
"""

POSTER_PATH.write_text(HTML_CONTENT, encoding="utf-8")
print(f"Refined single-page A0 Poster HTML written to: {POSTER_PATH}")
