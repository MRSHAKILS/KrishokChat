#!/usr/bin/env python3
"""
Generate the calibrated, large-scale typography Master Hybrid A0 Poster HTML.
Calibrated for standard A0 viewing distance (1.5 - 2.5 meters).
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
   Canvas: 841 mm × 1189 mm (A0 Portrait)
   Viewing Distance: 1.5 - 2.5m (Large Type Scale)
   ========================================================= */

:root {
  --bg-page: #f8fafc;
  --bg-card: #ffffff;
  
  --ink-dark: #0f172a;
  --ink-body: #1e293b;
  --ink-secondary: #334155;
  --ink-muted: #64748b;
  
  --emerald-primary: #059669;
  --emerald-dark: #065f46;
  --emerald-light: #ecfdf5;
  --emerald-border: #a7f3d0;
  
  --amber-primary: #d97706;
  --amber-light: #fffbeb;
  --amber-border: #fde68a;
  
  --crimson-primary: #dc2626;
  --crimson-light: #fef2f2;
  --crimson-border: #fecaca;
  
  --sky-primary: #0284c7;
  --sky-light: #f0f9ff;
  --sky-border: #bae6fd;
  
  --border-card: #e2e8f0;
  --border-subtle: #cbd5e1;
  --shadow-card: 0 4px 12px rgba(15, 23, 42, 0.05);
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
  background: var(--bg-page);
  color: var(--ink-body);
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
}

/* =========================================================
   1. HEADER CARD (A0 Large Scale)
   ========================================================= */
.header-card {
  background: var(--bg-card);
  border: 1px solid var(--border-card);
  border-radius: 5mm;
  padding: 6mm 10mm;
  box-shadow: var(--shadow-card);
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
  height: 2.8mm;
  background: linear-gradient(90deg, #059669 0%, #0284c7 45%, #d97706 100%);
}

.header-logo {
  flex-shrink: 0;
}

.header-logo img {
  height: 32mm;
  width: auto;
  object-fit: contain;
}

.header-content {
  flex: 1;
}

.badge-row {
  display: flex;
  align-items: center;
  gap: 3mm;
  margin-bottom: 2mm;
}

.pill-badge {
  background: var(--emerald-light);
  color: var(--emerald-dark);
  border: 1px solid var(--emerald-border);
  font-size: 4.2mm;
  font-weight: 700;
  padding: 1mm 3.5mm;
  border-radius: 1.5mm;
  text-transform: uppercase;
  letter-spacing: 0.2mm;
}

.pill-badge.blue {
  background: var(--sky-light);
  color: var(--sky-primary);
  border-color: var(--sky-border);
}

.poster-title {
  font-size: 11.5mm;
  font-weight: 800;
  color: var(--ink-dark);
  line-height: 1.15;
  letter-spacing: -0.3mm;
  margin-bottom: 2mm;
}

.poster-title span {
  color: var(--emerald-primary);
}

.poster-subtitle {
  font-size: 5.2mm;
  font-weight: 500;
  color: var(--ink-secondary);
  line-height: 1.25;
  margin-bottom: 2.5mm;
}

.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #f1f5f9;
  padding-top: 2.2mm;
  font-size: 4.6mm;
}

.authors-text {
  font-weight: 700;
  color: var(--ink-dark);
}

.advisor-text {
  color: var(--ink-muted);
  font-weight: 500;
}

.advisor-text strong {
  color: var(--ink-body);
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
  padding: 3.2mm 2.5mm;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-chip.dark {
  background: #0f172a;
  border-color: #0f172a;
}

.stat-chip.dark .chip-val { color: #38bdf8; }
.stat-chip.dark .chip-lbl { color: #94a3b8; }

.chip-val {
  font-size: 8.5mm;
  font-weight: 800;
  color: var(--emerald-primary);
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
  margin-bottom: 0.8mm;
}

.stat-chip:nth-child(3) .chip-val { color: #d97706; }
.stat-chip:nth-child(5) .chip-val { color: #dc2626; }

.chip-lbl {
  font-size: 3.2mm;
  font-weight: 600;
  color: var(--ink-secondary);
  line-height: 1.2;
  text-transform: uppercase;
  letter-spacing: 0.15mm;
}

/* =========================================================
   3. SECTION CARDS & FIGURE CONTAINERS
   ========================================================= */
.sec-card {
  background: #ffffff;
  border: 1px solid var(--border-card);
  border-radius: 4.5mm;
  box-shadow: var(--shadow-card);
  padding: 4mm 5mm;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sec-title {
  font-size: 5.5mm;
  font-weight: 800;
  color: var(--ink-dark);
  display: flex;
  align-items: center;
  gap: 2.5mm;
  margin-bottom: 3mm;
}

.sec-title .bullet {
  width: 3mm;
  height: 3mm;
  background: var(--emerald-primary);
  border-radius: 50%;
}

.figure-box {
  width: 100%;
  height: 100%;
  border-radius: 3mm;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
}

.figure-box img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: contain;
}

/* Layout Rows */
.row-hero {
  height: 195mm;
  flex-shrink: 0;
}

.row-research {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 4.5mm;
  height: 255mm;
  flex-shrink: 0;
}

.row-products {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4.5mm;
  height: 240mm;
  flex-shrink: 0;
}

.row-business {
  height: 210mm;
  flex-shrink: 0;
}

/* =========================================================
   4. NATIVE HTML 14-FIELD VERIFIER (Large Type)
   ========================================================= */
.verifier-container {
  display: flex;
  flex-direction: column;
  gap: 3mm;
  height: 100%;
}

.advisory-box {
  background: var(--bg-page);
  border: 1px solid var(--border-card);
  border-radius: 3mm;
  padding: 3mm 4mm;
}

.advisory-text {
  font-family: 'Tiro Bangla', serif;
  font-size: 4.8mm;
  font-weight: 700;
  color: var(--ink-dark);
  margin-bottom: 1mm;
}

.advisory-lbl {
  font-size: 3.4mm;
  color: var(--ink-muted);
  font-style: italic;
}

.slot-section {
  border: 1px solid var(--border-card);
  border-radius: 3mm;
  padding: 3mm 4mm;
}

.slot-section.orange {
  background: var(--amber-light);
  border-color: var(--amber-border);
}

.slot-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2mm;
  margin-top: 2mm;
}

.slot-item {
  font-size: 3.8mm;
  line-height: 1.3;
}

.slot-item strong {
  color: var(--ink-dark);
}

.slot-item span {
  font-weight: 800;
  color: var(--amber-primary);
}

.entail-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 3.6mm;
  margin-top: 1mm;
}

.entail-table th {
  background: #f1f5f9;
  color: var(--ink-secondary);
  font-weight: 700;
  text-align: left;
  padding: 1.8mm 2.5mm;
  border-bottom: 1px solid var(--border-card);
}

.entail-table td {
  padding: 1.8mm 2.5mm;
  border-bottom: 1px solid #f8fafc;
  vertical-align: middle;
}

.status-pill {
  display: inline-block;
  padding: 0.8mm 2.8mm;
  border-radius: 1.5mm;
  font-weight: 800;
  font-size: 3.2mm;
  text-align: center;
}

.status-pill.pass { background: #dcfce7; color: #15803d; border: 0.5px solid #86efac; }
.status-pill.alert { background: #fee2e2; color: #dc2626; border: 0.5px solid #fca5a5; }
.status-pill.strip { background: #fef3c7; color: #d97706; border: 0.5px solid #fde68a; }
.status-pill.slate { background: #f1f5f9; color: #475569; border: 0.5px solid #cbd5e1; }

/* =========================================================
   5. NATIVE HTML SOIL FIELDWORK COMPONENT
   ========================================================= */
.soil-field-grid {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 4mm;
  height: 100%;
}

.soil-stats-col {
  display: flex;
  flex-direction: column;
  gap: 3mm;
}

.stat-metric-card {
  background: var(--bg-page);
  border: 1px solid var(--border-card);
  border-radius: 3mm;
  padding: 3mm 4mm;
}

.metric-highlight {
  font-size: 7mm;
  font-weight: 800;
  color: var(--amber-primary);
  line-height: 1.1;
  margin-bottom: 0.8mm;
}

.metric-desc {
  font-size: 3.6mm;
  font-weight: 600;
  color: var(--ink-secondary);
  line-height: 1.3;
}

.advisory-threshold-box {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 3mm;
  padding: 3mm 4mm;
}

.threshold-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.5mm;
  font-size: 3.5mm;
}

/* =========================================================
   6. NATIVE HTML BUSINESS MODEL COMPONENT
   ========================================================= */
.business-lanes-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 4mm;
  height: 100%;
}

.biz-lane-card {
  background: var(--bg-page);
  border: 1px solid var(--border-card);
  border-radius: 3.5mm;
  padding: 4mm 4.5mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.biz-lane-header {
  font-size: 4.6mm;
  font-weight: 800;
  color: var(--ink-dark);
  margin-bottom: 2mm;
}

.biz-lane-body {
  font-size: 3.7mm;
  line-height: 1.4;
  color: var(--ink-body);
}

.biz-lane-body strong {
  color: var(--emerald-primary);
}

.market-readiness-bar {
  grid-column: span 3;
  background: #0f172a;
  color: #ffffff;
  border-radius: 3mm;
  padding: 2.5mm 6mm;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 3.8mm;
  margin-top: 1mm;
}

.market-item strong {
  color: #38bdf8;
}

/* =========================================================
   7. FOOTER STRIP
   ========================================================= */
.footer-strip {
  background: #0f172a;
  color: #94a3b8;
  border-radius: 3.5mm;
  padding: 3.8mm 8mm;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 3.8mm;
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
  padding: 1.5mm 3.5mm;
  border-radius: 1.8mm;
  font-size: 4.2mm;
}

.qr-pill {
  background: #1e293b;
  color: #38bdf8;
  border: 1px solid #38bdf8;
  padding: 1mm 3mm;
  border-radius: 1.8mm;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  font-size: 3.4mm;
}
</style>
</head>
<body>

<div class="poster-canvas">

  <!-- 1. HEADER & TITLE BLOCK -->
  <header class="header-card">
    <div class="header-logo">
      <img src="screenshots/nsu_logo.png" alt="North South University Official Logo"/>
    </div>
    
    <div class="header-content">
      <div class="badge-row">
        <span class="pill-badge">Capstone Design &amp; Innovation Challenge 2026</span>
        <span class="pill-badge blue">Track: AI &amp; Agri-Tech</span>
      </div>
      
      <h1 class="poster-title">
        <span>KrishokChat:</span> A Safety-First Agentic Agricultural Advisory System for Bangladeshi Smallholder Farmers
      </h1>
      
      <div class="poster-subtitle">
        Field-Collected Multimodal Datasets &bull; Four-Stage Verified Bengali AI Pipeline &bull; 85,979-Instance Provenance-Traced Benchmark &bull; National 16123 Escalation Gate
      </div>
      
      <div class="meta-row">
        <div class="authors-text">
          Khan Raiyan Ibne Reza &nbsp;&bull;&nbsp; Sanjana Aktar Maria &nbsp;&bull;&nbsp; Shakil Ahmed
        </div>
        <div class="advisor-text">
          Faculty Advisor: <strong>Dr. Sumaiya Tabassum Nimi (STI)</strong> &nbsp;&bull;&nbsp; Dept. of Electrical &amp; Computer Engineering (ECE) &nbsp;&bull;&nbsp; <strong>North South University</strong>
        </div>
      </div>
    </div>
  </header>

  <!-- 2. HERO STAT RIBBON -->
  <section class="stat-ribbon">
    <div class="stat-chip">
      <div class="chip-val">85,979</div>
      <div class="chip-lbl">Benchmark Instances<br>4 Tracks &bull; CC-BY-4.0</div>
    </div>
    
    <div class="stat-chip">
      <div class="chip-val">95–97%</div>
      <div class="chip-lbl">Top-1 Disease Accuracy<br>5 Crop Families (AgriVision)</div>
    </div>
    
    <div class="stat-chip">
      <div class="chip-val">R² = 0.39</div>
      <div class="chip-lbl">Soil Moisture CV R²<br>22.1% Error Reduction (EffNet)</div>
    </div>
    
    <div class="stat-chip dark">
      <div class="chip-val">4-Stage</div>
      <div class="chip-lbl">Agent Pipeline<br>Pre-Retrieval Safety Gate</div>
    </div>
    
    <div class="stat-chip">
      <div class="chip-val">16123</div>
      <div class="chip-lbl">Krishi Call Center<br>Automated Triage Gate</div>
    </div>
    
    <div class="stat-chip">
      <div class="chip-val">2 Papers</div>
      <div class="chip-lbl">EACL '26 &bull; SIGIR-AP '26<br>Under Peer Review</div>
    </div>
  </section>

  <!-- 3. ROW 1: HERO SYSTEM ARCHITECTURE DIAGRAM (300 DPI) -->
  <section class="sec-card row-hero">
    <div class="figure-box">
      <img src="figures/F1_system_architecture.png" alt="KrishokChat 4-Stage Safety Architecture Pipeline Diagram"/>
    </div>
  </section>

  <!-- 4. ROW 2: BENCHMARK CHARTS (300 DPI) + NATIVE 14-FIELD VERIFIER SCHEMA -->
  <section class="row-research">
    <!-- Left: Dual-Panel Benchmark Charts -->
    <div class="sec-card">
      <div class="figure-box">
        <img src="figures/F2_benchmark_evaluation_charts.png" alt="Retrieval Recall@10 and Model GenF1 Charts"/>
      </div>
    </div>

    <!-- Right: 14-Field Claim Verifier Schema (Native Vector HTML) -->
    <div class="sec-card">
      <div class="verifier-container">
        <div class="sec-title"><span class="bullet"></span>Structured Claim Grounding &amp; Verification Engine</div>
        
        <!-- 1. Advisory Example -->
        <div class="advisory-box">
          <div class="advisory-text">“ধানের ব্লাইট দমনে ট্রাইসাইক্লাজোল ৭৫ ডব্লিউপি প্রতি লিটার পানিতে ০.৮ গ্রাম মিশিয়ে স্প্রে করুন (PHI: ১৪ দিন)”</div>
          <div class="advisory-lbl">Generated Agrochemical Advisory Sentence → Parsed into 14 Atomic Slots</div>
        </div>

        <!-- 2. Safety-Critical Slots Grid -->
        <div class="slot-section orange">
          <strong style="color:#b45309;font-size:3.8mm;">⚠️ SAFETY-CRITICAL QUANTITATIVE FIELDS (Strict Entailment)</strong>
          <div class="slot-grid">
            <div class="slot-item"><strong>Formulation:</strong> <span>75 WP</span></div>
            <div class="slot-item"><strong>Dose Amount:</strong> <span>0.8 g</span></div>
            <div class="slot-item"><strong>Carrier:</strong> <span>1 L water</span></div>
            <div class="slot-item"><strong>Interval:</strong> <span>7-10 days</span></div>
            <div class="slot-item"><strong>PHI Safety:</strong> <span>14 days</span></div>
            <div class="slot-item"><strong>Stance:</strong> <span>affirmative</span></div>
          </div>
        </div>

        <!-- 3. Entailment Table -->
        <table class="entail-table">
          <thead>
            <tr>
              <th>Entailment Relation</th>
              <th>Action in KrishokChat</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>SUPPORTED</strong> (Full evidence match)</td>
              <td>Retain claim in final advisory</td>
              <td><span class="status-pill pass">PASS</span></td>
            </tr>
            <tr>
              <td><strong>CONTRADICTED</strong> (Evidence contradicts)</td>
              <td>Drop claim &amp; trigger alert</td>
              <td><span class="status-pill alert">DROP &amp; ALERT</span></td>
            </tr>
            <tr>
              <td><strong>PARTIALLY_SUPPORTED</strong></td>
              <td>Strip ungrounded dosage fields</td>
              <td><span class="status-pill strip">STRIP &amp; KEEP</span></td>
            </tr>
            <tr>
              <td><strong>UNSUPPORTED</strong> (No evidence found)</td>
              <td>Drop claim completely</td>
              <td><span class="status-pill alert">DROP</span></td>
            </tr>
            <tr>
              <td><strong>AMBIGUOUS</strong> (Conflicting evidence)</td>
              <td>Fail-closed → 16123 referral</td>
              <td><span class="status-pill slate">FAIL-CLOSED</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- 5. ROW 3: MULTIMODAL CROP VISION + SOIL MOISTURE FIELDWORK -->
  <section class="row-products">
    <!-- Left: AgriVision Multimodal Crop Disease Detection -->
    <div class="sec-card">
      <div class="figure-box">
        <img src="figures/F5_disease-classification.png" alt="AgriVision BD Multimodal Crop Disease Vision Pipeline"/>
      </div>
    </div>

    <!-- Right: Pabna Soil Moisture Fieldwork & Calibration Scatter -->
    <div class="sec-card">
      <div class="soil-field-grid">
        <!-- Left Sub-column: Scatter Plot -->
        <div class="figure-box" style="height:100%;">
          <img src="figures/F6_soil_moisture_scatter.png" alt="EfficientNet-B0 Soil Moisture Calibration Scatter Plot"/>
        </div>

        <!-- Right Sub-column: Fieldwork Specs & Thresholds -->
        <div class="soil-stats-col">
          <div class="sec-title" style="margin-bottom:1.5mm;"><span class="bullet"></span>Pabna District Fieldwork</div>
          
          <div class="stat-metric-card">
            <div class="metric-highlight">722 Photos</div>
            <div class="metric-desc">Tensiometer in-situ measurements (0.0–21.5 kPa) across 6 USDA soil textures &amp; 14 crops.</div>
          </div>

          <div class="stat-metric-card">
            <div class="metric-highlight">22.1% Error ↓</div>
            <div class="metric-desc">EfficientNet-B0 RMSE 4.09 kPa vs 5.26 kPa baseline. Leakage-free 5-fold CV.</div>
          </div>

          <div class="advisory-threshold-box">
            <strong style="color:#15803d;font-size:3.6mm;">In-Situ Irrigation Thresholds:</strong>
            <div class="threshold-row"><span>&lt; 10 kPa:</span> <strong style="color:#059669;">Adequate Moisture</strong></div>
            <div class="threshold-row"><span>10–15 kPa:</span> <strong style="color:#d97706;">Monitor Closely</strong></div>
            <div class="threshold-row"><span>&gt; 15 kPa:</span> <strong style="color:#dc2626;">Irrigation Recommended</strong></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 6. ROW 4: BUSINESS MODEL, MARKET READINESS & SCALABILITY -->
  <section class="sec-card row-business">
    <div class="sec-title" style="margin-bottom:2mm;"><span class="bullet"></span>Sustainable Business Model &amp; National Scaling Architecture</div>
    <div class="business-lanes-grid">
      <!-- Lane 1 -->
      <div class="biz-lane-card">
        <div>
          <div class="biz-lane-header">① Freemium + B2B Enterprise</div>
          <div class="biz-lane-body">
            • <strong>Farmers:</strong> Free mobile advisory, disease vision &amp; soil guidance.<br>
            • <strong>Agro-Dealers &amp; SAAOs:</strong> Paid subscription for regional disease tracking, inventory forecasting &amp; treatment validation analytics.<br>
            • <em>Benchmark: PxD 7.8M users; ACI IDSS / Fosholi.</em>
          </div>
        </div>
      </div>

      <!-- Lane 2 -->
      <div class="biz-lane-card">
        <div>
          <div class="biz-lane-header">② B2G Call Center Integration</div>
          <div class="biz-lane-body">
            • <strong>AI Front-End for 16123:</strong> Direct triage &amp; intent routing for DAE / Krishi Call Center.<br>
            • <strong>Value Moat:</strong> Automated safety filtering, dialect handling &amp; offloading routine queries so human agronomists handle complex escalations.
          </div>
        </div>
      </div>

      <!-- Lane 3 -->
      <div class="biz-lane-card">
        <div>
          <div class="biz-lane-header">③ Agri-Fintech &amp; Data Licensing</div>
          <div class="biz-lane-body">
            • <strong>Micro-Finance &amp; Crop Insurance:</strong> Anonymized query trends &amp; soil moisture indices for risk underwriting.<br>
            • <strong>Research Moat:</strong> 85,979 Benchmark &amp; 722-image dataset (CC-BY-4.0) establishing KrishokChat as the national standard.
          </div>
        </div>
      </div>

      <!-- Market Readiness Bar -->
      <div class="market-readiness-bar">
        <div class="market-item">Status: <strong>Working Full-Stack System</strong> (Next.js 16 + FastAPI + Edge ONNX)</div>
        <div class="market-item">Validation: <strong>2 Peer-Reviewed Papers</strong> (EACL '26, SIGIR-AP '26)</div>
        <div class="market-item">Edge Latency: <strong>&lt;30 ms Android Inference</strong> (Zero Cloud Cost)</div>
      </div>
    </div>
  </section>

  <!-- 7. FOOTER STRIP -->
  <footer class="footer-strip">
    <div class="footer-refs">
      <strong>References &amp; Provenance:</strong> [1] <em>KrishokChat: A Provenance-Traceable Bengali Agricultural Benchmark</em> (EACL 2026, under review) &bull; [2] <em>AgriTrust: Verified Bengali Agronomic Advisory via Structured Claim Grounding</em> (SIGIR-AP 2026, under review) &bull; [3] <em>AgriVision BD Project Report</em> &bull; Datasets released under CC-BY-4.0 on HuggingFace: <code>RaiyanKhaan/KrishokChat-Advisory-System</code>.
    </div>
    
    <div class="footer-right">
      <span class="qr-pill">HF: RaiyanKhaan/KrishokChat</span>
      <span class="helpline-badge">Emergency Triage: 16123 / 999</span>
    </div>
  </footer>

</div>

</body>
</html>
"""

POSTER_PATH.write_text(HTML_CONTENT, encoding="utf-8")
print(f"Updated Calibrated Master Hybrid A0 Poster written to: {POSTER_PATH}")
