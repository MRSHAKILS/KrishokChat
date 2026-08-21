#!/usr/bin/env python3
"""Write the full A0 KrishokChat capstone poster to poster.html"""
import pathlib

OUT = pathlib.Path(r"d:\KrishokChat Advisory System\capstone\poster-design\poster.html")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>KrishokChat &mdash; A0 Capstone Poster</title>
<link href="https://fonts.googleapis.com/css2?family=Tiro+Bangla:ital@0;1&family=Noto+Sans+Bengali:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
<style>
:root{
  --paper:#faf6ef;--paper-2:#f2ebdc;--bone:#e7dfd0;--ink:#1a1611;
  --leaf:#2f5d3a;--leaf-2:#3d7a4d;--leaf-3:#4a9560;
  --ochre:#c8893c;--ochre-2:#dda04a;--clay:#a8542b;--mist:#8a7d6e;
  --t-title:19mm;--t-sub:10.6mm;--t-head:10.6mm;--t-subh:9.9mm;
  --t-body:8.5mm;--t-sm:7.8mm;--t-cap:7.1mm;--t-foot:6.4mm;
  --t-chipn:14.1mm;--t-chipl:7.1mm;--t-hook:9.9mm;
}
*{margin:0;padding:0;box-sizing:border-box;}
@page{size:841mm 1189mm;margin:0;}
body{width:841mm;min-height:1189mm;background:var(--paper);color:var(--ink);font-family:'Inter','Noto Sans Bengali',sans-serif;font-size:var(--t-body);line-height:1.35;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
.poster{width:841mm;min-height:1189mm;display:flex;flex-direction:column;padding:8mm 10mm 6mm;gap:0;}
/* Title */
.title-block{display:flex;align-items:flex-start;gap:8mm;padding-bottom:6mm;border-bottom:1.2mm solid var(--leaf);}
.title-block__text{flex:1;}
.poster-title{font-family:'Tiro Bangla',serif;font-size:var(--t-title);font-weight:700;color:var(--leaf);line-height:1.15;margin-bottom:3mm;}
.poster-subtitle{font-size:var(--t-sub);color:var(--ink);line-height:1.3;margin-bottom:4mm;font-weight:400;}
.authors{font-size:var(--t-body);font-weight:600;color:var(--ink);margin-bottom:1.5mm;}
.affil{font-size:var(--t-sm);color:var(--mist);}
.title-block__logo{display:flex;flex-direction:column;align-items:center;gap:3mm;flex-shrink:0;}
.title-block__logo img{height:28mm;width:auto;object-fit:contain;}
.dept-badge{background:var(--leaf);color:#fff;font-size:var(--t-foot);font-weight:600;padding:1.5mm 4mm;border-radius:2mm;text-align:center;}
/* Hero */
.hero-strip{background:var(--ink);border-radius:3mm;padding:6mm 8mm;margin:5mm 0;}
.hook-line{font-size:var(--t-hook);font-weight:600;color:#fff;line-height:1.3;margin-bottom:5mm;}
.hook-line span{color:var(--ochre);}
.stat-chips{display:flex;gap:4mm;flex-wrap:wrap;}
.stat-chip{background:rgba(255,255,255,0.08);border:0.5mm solid rgba(255,255,255,0.18);border-radius:3mm;padding:3mm 5mm;flex:1;min-width:90mm;text-align:center;}
.stat-chip__num{font-size:var(--t-chipn);font-weight:800;color:var(--ochre);display:block;line-height:1.1;font-variant-numeric:tabular-nums;}
.stat-chip__lbl{font-size:var(--t-chipl);color:rgba(255,255,255,0.75);display:block;margin-top:1mm;line-height:1.25;}
/* Columns */
.columns{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm;flex:1;}
.col{display:flex;flex-direction:column;gap:4mm;}
/* Cards */
.card{background:var(--paper-2);border:0.4mm solid var(--bone);border-radius:3mm;padding:5mm 6mm;}
.card--leaf{border-left:2mm solid var(--leaf);}
.card--ochre{border-left:2mm solid var(--ochre);}
.card--clay{border-left:2mm solid var(--clay);}
.card--bone{background:var(--bone);}
.sec-head{font-family:'Tiro Bangla',serif;font-size:var(--t-head);font-weight:700;color:var(--leaf);margin-bottom:3mm;line-height:1.2;}
.sub-head{font-size:var(--t-subh);font-weight:700;color:var(--ink);margin:3mm 0 2mm;line-height:1.2;}
.body-sm{font-size:var(--t-sm);line-height:1.4;}
.caption{font-size:var(--t-cap);color:var(--mist);font-style:italic;line-height:1.3;margin-top:2mm;}
.divider{height:0.4mm;background:var(--bone);margin:2mm 0;}
.mt-2{margin-top:2mm;}.mb-2{margin-bottom:2mm;}
.text-leaf{color:var(--leaf);}.text-clay{color:var(--clay);}.fw-700{font-weight:700;}
/* Tables */
table{width:100%;border-collapse:collapse;font-size:var(--t-sm);margin:3mm 0;}
th{background:var(--leaf);color:#fff;font-weight:600;padding:2mm 3mm;text-align:left;border:0.3mm solid var(--leaf-2);font-size:var(--t-cap);}
td{padding:2mm 3mm;border:0.3mm solid var(--bone);vertical-align:top;line-height:1.35;}
tr:nth-child(even) td{background:rgba(47,93,58,0.05);}
td.hi{color:var(--leaf);font-weight:700;}
td.num{font-variant-numeric:tabular-nums;font-weight:600;}
td.check{color:var(--leaf);font-weight:700;font-size:var(--t-body);text-align:center;}
td.cross{color:var(--clay);font-weight:700;font-size:var(--t-body);text-align:center;}
td.partial{color:var(--ochre);font-weight:600;text-align:center;font-size:var(--t-sm);}
/* KPI pills */
.kpi-row{display:flex;gap:3mm;flex-wrap:wrap;margin:3mm 0;}
.kpi-pill{background:var(--bone);border:0.4mm solid var(--ochre);border-radius:2mm;padding:2mm 4mm;text-align:center;flex:1;}
.kpi-pill__num{font-size:var(--t-subh);font-weight:800;color:var(--ochre);display:block;font-variant-numeric:tabular-nums;line-height:1.1;}
.kpi-pill__lbl{font-size:var(--t-foot);color:var(--mist);display:block;line-height:1.3;}
/* Bar chart */
.bar-chart{margin:3mm 0;}
.bar-row{display:flex;align-items:center;gap:3mm;margin-bottom:2.5mm;}
.bar-label{font-size:var(--t-sm);width:38mm;flex-shrink:0;text-align:right;font-weight:500;}
.bar-track{flex:1;height:7mm;background:var(--bone);border-radius:1.5mm;overflow:hidden;}
.bar-fill{height:100%;background:var(--leaf);border-radius:1.5mm;display:flex;align-items:center;justify-content:flex-end;padding-right:2mm;}
.bar-fill.winner{background:var(--ochre);}
.bar-fill.clay-bar{background:var(--clay);}
.bar-val{font-size:var(--t-cap);font-weight:700;color:#fff;}
/* Bullets */
.bullet-list{font-size:var(--t-sm);padding-left:5mm;line-height:1.5;}
.bullet-list li{margin-bottom:1.5mm;}
.bullet-list li strong{color:var(--leaf);}
/* Pipeline */
.pipeline-diagram{background:var(--ink);border-radius:3mm;padding:6mm;color:#fff;}
.pipeline-title{font-family:'Tiro Bangla',serif;font-size:var(--t-head);color:var(--ochre);font-weight:700;text-align:center;margin-bottom:4mm;line-height:1.2;}
.pipeline-input{text-align:center;font-size:var(--t-sm);color:rgba(255,255,255,0.7);font-style:italic;margin-bottom:3mm;}
.stage-box{background:rgba(255,255,255,0.07);border:0.5mm solid rgba(255,255,255,0.2);border-radius:2.5mm;padding:3.5mm 5mm;width:100%;margin-bottom:0;}
.stage-box.s1{border-left:2mm solid #4a9560;}
.stage-box.s2{border-left:2mm solid #c8893c;}
.stage-box.s3{border-left:2mm solid #dda04a;}
.stage-box.s4{border-left:2mm solid #6ba8d8;}
.stage-box.s5{border-left:2mm solid #8a7d6e;background:rgba(255,255,255,0.04);}
.stage-num{font-size:var(--t-cap);color:var(--ochre);font-weight:700;letter-spacing:0.5mm;text-transform:uppercase;}
.stage-name{font-size:var(--t-body);font-weight:700;color:#fff;line-height:1.2;}
.stage-detail{font-size:var(--t-cap);color:rgba(255,255,255,0.62);line-height:1.3;}
.pipe-arrow{display:flex;justify-content:center;color:rgba(255,255,255,0.35);font-size:5mm;line-height:1;margin:2mm 0;}
.unsafe-branch{display:flex;align-items:flex-start;gap:3mm;margin:3mm 0;}
.unsafe-arrow{color:#a8542b;font-size:var(--t-body);font-weight:700;flex-shrink:0;margin-top:1mm;}
.unsafe-box{background:rgba(168,84,43,0.18);border:0.5mm solid #a8542b;border-radius:2mm;padding:3mm 4mm;flex:1;}
.unsafe-head{font-size:var(--t-sm);font-weight:700;color:#c46535;margin-bottom:1mm;}
.unsafe-num{font-size:var(--t-subh);font-weight:800;color:#ff7f5c;font-variant-numeric:tabular-nums;}
.pipe-output{text-align:center;background:rgba(47,93,58,0.25);border:0.5mm solid #4a9560;border-radius:2mm;padding:3mm;margin-top:3mm;font-size:var(--t-sm);color:rgba(255,255,255,0.85);line-height:1.3;}
.pipe-output strong{color:#7de89d;}
/* Safety chips */
.safety-chips{display:grid;grid-template-columns:1fr 1fr;gap:2mm;margin:3mm 0;}
.safety-chip{border-radius:2mm;padding:2.5mm 3.5mm;font-size:var(--t-cap);font-weight:600;line-height:1.3;}
.chip-g{background:rgba(47,93,58,0.15);border:0.4mm solid #3d7a4d;color:#2f5d3a;}
.chip-c{background:rgba(168,84,43,0.12);border:0.4mm solid #a8542b;color:#a8542b;}
.chip-o{background:rgba(200,137,60,0.12);border:0.4mm solid #c8893c;color:#7a4a00;}
.chip-m{background:rgba(138,125,110,0.12);border:0.4mm solid #8a7d6e;color:#4a3e32;}
.chip-route{font-size:var(--t-foot);font-weight:400;opacity:0.8;display:block;margin-top:0.5mm;}
/* Verifier schema */
.schema-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5mm;margin:2mm 0;}
.schema-f{background:var(--bone);border-radius:1.5mm;padding:1.5mm 2mm;font-size:var(--t-foot);font-weight:500;text-align:center;line-height:1.2;}
.schema-f.crit{background:rgba(168,84,43,0.12);border:0.3mm solid #a8542b;color:#a8542b;font-weight:700;}
.rel-chips{display:flex;flex-wrap:wrap;gap:2mm;margin:2mm 0;}
.rel-chip{background:var(--paper-2);border:0.4mm solid var(--bone);border-radius:1.5mm;padding:1mm 3mm;font-size:var(--t-foot);font-family:'Inter',monospace;color:var(--mist);}
/* Screenshots */
.screenshot-wrap{border-radius:2mm;overflow:hidden;border:0.4mm solid var(--bone);box-shadow:0 1mm 3mm rgba(0,0,0,0.08);}
.screenshot-wrap img{width:100%;height:auto;display:block;}
.screenshot-caption{background:var(--bone);padding:2mm 3mm;font-size:var(--t-cap);color:var(--mist);font-style:italic;text-align:center;}
/* Impact */
.impact-item{display:flex;gap:3mm;align-items:flex-start;margin-bottom:3mm;}
.impact-icon{font-size:var(--t-subh);flex-shrink:0;margin-top:-1mm;}
.impact-text{font-size:var(--t-sm);line-height:1.45;}
.impact-text strong{color:var(--leaf);font-weight:700;}
/* Biz */
.biz-lane{background:var(--bone);border-radius:2mm;padding:3mm 4mm;border-left:2mm solid var(--ochre);margin-bottom:2.5mm;}
.biz-lane__head{font-size:var(--t-sm);font-weight:700;color:var(--ochre);margin-bottom:1mm;}
.biz-lane__body{font-size:var(--t-cap);color:var(--ink);line-height:1.35;}
/* Roadmap */
.roadmap-item{font-size:var(--t-cap);color:var(--ink);padding-left:4mm;border-left:1mm solid #3d7a4d;line-height:1.3;margin-bottom:2mm;}
/* QR */
.qr-row{display:flex;gap:4mm;justify-content:space-around;margin-top:3mm;}
.qr-item{display:flex;flex-direction:column;align-items:center;gap:2mm;}
.qr-box{width:28mm;height:28mm;background:var(--ink);border-radius:2mm;display:flex;align-items:center;justify-content:center;font-size:var(--t-foot);color:rgba(255,255,255,0.5);text-align:center;padding:2mm;line-height:1.2;}
.qr-label{font-size:var(--t-foot);font-weight:600;color:var(--mist);text-align:center;}
/* Soil */
.soil-scatter{border-radius:2mm;overflow:hidden;border:0.4mm solid var(--bone);margin:3mm 0;}
.soil-scatter img{width:100%;height:auto;display:block;}
/* Novelty badge */
.novelty-badge{background:rgba(47,93,58,0.08);border:0.4mm solid #3d7a4d;border-radius:1.5mm;padding:1.5mm 3mm;display:inline-block;font-size:var(--t-cap);font-weight:600;color:#2f5d3a;margin:1mm 1mm 1mm 0;}
/* Footer */
.footer{border-top:0.8mm solid var(--bone);margin-top:5mm;padding-top:3mm;font-size:var(--t-foot);color:var(--mist);line-height:1.4;display:flex;gap:8mm;}
.footer__refs{flex:1;}
.footer__contact{flex-shrink:0;text-align:right;}
</style>
</head>
<body>
<div class="poster">

<!-- ROW 0: TITLE BLOCK -->
<div class="title-block">
  <div class="title-block__text">
    <div class="poster-title">KrishokChat: A Safety-First Agentic Agricultural Advisory System for Bangladeshi Smallholder Farmers</div>
    <div class="poster-subtitle">Field-collected crop-disease and soil-moisture datasets &middot; four-stage verified Bengali AI pipeline &middot; 85,979-instance provenance-traced benchmark</div>
    <div class="authors">Khan Raiyan Ibne Reza &nbsp;&middot;&nbsp; Sanjana Aktar Maria &nbsp;&middot;&nbsp; Shakil Ahmed</div>
    <div class="affil">Faculty Advisor: Dr. Sumaiya Tabassum Nimi (STI) &nbsp;&middot;&nbsp; Department of Electrical and Computer Engineering (ECE) &nbsp;&middot;&nbsp; North South University, Bangladesh</div>
  </div>
  <div class="title-block__logo">
    <img src="screenshots/nsu_logo.png" alt="North South University"/>
    <div class="dept-badge">CSE 499B &middot; Capstone 2026</div>
  </div>
</div>

<!-- ROW 1: HERO STAT RIBBON -->
<div class="hero-strip">
  <div class="hook-line">The first Bengali agricultural assistant that <span>classifies safety before retrieval</span>, verifies every chemical claim against government sources, diagnoses crop diseases from photos at <span>95&ndash;97% accuracy</span>, and estimates soil moisture from field images &mdash; built on a <span>published 85,979-instance benchmark</span> and escalating unsafe queries to the national Krishi Call Center (<span>16123</span>).</div>
  <div class="stat-chips">
    <div class="stat-chip"><span class="stat-chip__num">85,979</span><span class="stat-chip__lbl">benchmark instances<br>4 tracks &middot; CC-BY-4.0</span></div>
    <div class="stat-chip"><span class="stat-chip__num">95&ndash;97%</span><span class="stat-chip__lbl">crop disease top-1 accuracy<br>Brassica, Rice, Corn, Potato</span></div>
    <div class="stat-chip"><span class="stat-chip__num">R&sup2;=0.39</span><span class="stat-chip__lbl">soil moisture regression<br>EffNet-B0 &middot; 5-fold OOF</span></div>
    <div class="stat-chip"><span class="stat-chip__num">4-stage</span><span class="stat-chip__lbl">safety-verified agent pipeline<br>Safety &rarr; Retrieve &rarr; Generate &rarr; Verify</span></div>
    <div class="stat-chip"><span class="stat-chip__num">16123</span><span class="stat-chip__lbl">Krishi Call Center escalation<br>active national helpline</span></div>
    <div class="stat-chip"><span class="stat-chip__num">2 papers</span><span class="stat-chip__lbl">EACL 2026 &middot; SIGIR-AP 2026<br>under review</span></div>
  </div>
</div>

<!-- ROW 2: THREE COLUMNS -->
<div class="columns">

<!-- ============ COLUMN A ============ -->
<div class="col">

<!-- A1 Problem -->
<div class="card card--clay">
  <div class="sec-head">The Problem</div>
  <div class="body-sm">Rural Bangladesh has <strong style="color:#a8542b">~47 million farming households</strong> with limited access to reliable Bengali-language agricultural advisory. The national Krishi Call Center (16123) received 92,094 calls in FY 2025&ndash;26 &mdash; a fraction of actual need.</div>
  <div class="divider"></div>
  <div class="body-sm mt-2">LLM-based advisory tools can hallucinate pesticide dosages. In our benchmark, six architecturally different LLMs maintain a <strong style="color:#a8542b">4.05&ndash;7.00% chemical-hallucination floor</strong> even under oracle evidence. A wrong dose can burn a crop, poison a farmer, or contaminate soil and water.</div>
  <div class="body-sm mt-2">KrishokChat closes this gap with a safety-first pipeline that stops unsafe queries before generation, verifies every dosage against government sources, and grounds answers in a <strong>2,882-node knowledge graph</strong> from 284 government publications.</div>
</div>

<!-- A2 Benchmark -->
<div class="card card--leaf">
  <div class="sec-head">85,979-Instance Provenance-Traced Benchmark</div>
  <div class="kpi-row">
    <div class="kpi-pill"><span class="kpi-pill__num">28,993</span><span class="kpi-pill__lbl">General QA</span></div>
    <div class="kpi-pill"><span class="kpi-pill__num">11,224</span><span class="kpi-pill__lbl">Treatment QA</span></div>
    <div class="kpi-pill"><span class="kpi-pill__num">25,650</span><span class="kpi-pill__lbl">Table QA</span></div>
    <div class="kpi-pill"><span class="kpi-pill__num">20,112</span><span class="kpi-pill__lbl">Safety</span></div>
  </div>
  <div class="body-sm">Four tracks, <strong>CC-BY-4.0</strong>, on HuggingFace (<em>RaiyanKhaan/KrishokChat-Advisory-System</em>). Treatment QA: 7,437 chemical-bearing instances (66.3%), provenance-traced. Table QA: 6 dialects &times; 4,275 base instances, 3 complexity levels.</div>
  <div class="divider"></div>
  <div class="sub-head">Knowledge Graph</div>
  <div class="body-sm"><strong style="color:#2f5d3a">2,882 nodes</strong> &middot; 19,768 entities (6.9/node) &middot; 17,501 factual triples &middot; 1,022 image-linked nodes (35.5%). Sources: 284 government publications, 13 institutions (BARC, BARI, BRRI, DAE, CABI Plantwise, &hellip;). Inter-annotator &kappa; = 0.72 (farmer+safety), 0.78 (KG-grounded).</div>
  <div class="body-sm mt-2"><strong>Farmer benchmark:</strong> 1,000 real queries &mdash; 300 field interviews in Rajshahi &amp; Natore, 483 from farmer Facebook groups, 217 from krishibangla.com.</div>
</div>

<!-- A3 Retrieval -->
<div class="card card--leaf">
  <div class="sec-head">Hybrid Retrieval Wins on Bengali</div>
  <div class="body-sm mb-2">Recall@10 across 900 answerable queries, 5 retrieval architectures:</div>
  <div class="bar-chart">
    <div class="bar-row"><div class="bar-label">Hybrid RRF</div><div class="bar-track"><div class="bar-fill winner" style="width:100%"><span class="bar-val">0.539</span></div></div></div>
    <div class="bar-row"><div class="bar-label">BM25</div><div class="bar-track"><div class="bar-fill" style="width:93.9%"><span class="bar-val">0.506</span></div></div></div>
    <div class="bar-row"><div class="bar-label">ColBERT</div><div class="bar-track"><div class="bar-fill" style="width:90.4%"><span class="bar-val">0.487</span></div></div></div>
    <div class="bar-row"><div class="bar-label">Dense (Gemini)</div><div class="bar-track"><div class="bar-fill" style="width:86.1%"><span class="bar-val">0.464</span></div></div></div>
    <div class="bar-row"><div class="bar-label">BGE-M3</div><div class="bar-track"><div class="bar-fill clay-bar" style="width:75.7%"><span class="bar-val">0.408</span></div></div></div>
  </div>
  <div class="caption">BM25 outperforms dense by 9% (p&lt;0.001, Wilcoxon) on Bengali. Dense collapses on colloquial farmer queries (R@10=0.093) but near-perfect on formal safety queries (0.970). Hybrid RRF wins overall. Source: AgriTrust, SIGIR-AP 2026.</div>
</div>

<!-- A4 Model -->
<div class="card card--leaf">
  <div class="sec-head">KrishokChat-4B: Fine-Tuned Gemma-4 4-bit</div>
  <div class="body-sm mb-2">Closed-book General QA Token F1 (900 answerable instances):</div>
  <table>
    <tr><th>Model</th><th>GenF1</th><th>Treatment Correct%</th></tr>
    <tr><td class="hi"><strong>KrishokChat-4B</strong><br><span style="font-size:var(--t-foot);color:#8a7d6e">Gemma-4-E4B 4-bit, LoRA r=32</span></td><td class="num hi">0.314</td><td class="num hi">35.55%</td></tr>
    <tr><td>LLaMA-3.1-8B (best zero-shot)</td><td class="num">0.165</td><td class="num">12.43%</td></tr>
    <tr><td>Gemini-2.5-Flash-Lite</td><td class="num">0.104</td><td class="num">43.64%</td></tr>
    <tr><td>Gemma-4-26B</td><td class="num">0.087</td><td class="num">38.73%</td></tr>
  </table>
  <div class="body-sm">KrishokChat-4B achieves <strong style="color:#2f5d3a">1.9&times; the General F1</strong> of the best zero-shot baseline (p &asymp; 6.7&times;10&#8315;&#8309;). Trained on single NVIDIA L4 (24 GB), bfloat16, effective batch 16, max seq 4,096.</div>
  <div class="body-sm mt-2"><strong>Safety compliance:</strong> KrishokChat-4B incorrectly complied with a harmful safety-test request in only <strong style="color:#2f5d3a">0.31% of cases (1/323)</strong> &mdash; the lowest across all tested models.</div>
  <div class="body-sm mt-2"><strong style="color:#a8542b">Chemical-hallucination floor</strong> across all 6 LLMs under oracle evidence: 4.05&ndash;7.00% &mdash; structural proof that a deterministic verifier is necessary.</div>
</div>

<!-- A5 Novelty -->
<div class="card card--ochre">
  <div class="sec-head">What We Built &mdash; Four Contributions</div>
  <table>
    <tr><th>Capability</th><th>Generic chatbots</th><th>KrishokBondhu</th><th>KrishokChat</th></tr>
    <tr><td>Safety classify before retrieval</td><td class="cross">&#10007;</td><td class="cross">&#10007;</td><td class="check">&#10003;</td></tr>
    <tr><td>Structured dosage verifier (14-field)</td><td class="cross">&#10007;</td><td class="cross">&#10007;</td><td class="check">&#10003;</td></tr>
    <tr><td>Audit log + analytics panel</td><td class="cross">&#10007;</td><td class="cross">&#10007;</td><td class="check">&#10003;</td></tr>
    <tr><td>Bengali + 6 dialects (text)</td><td class="partial">partial</td><td class="partial">voice only</td><td class="check">&#10003;</td></tr>
    <tr><td>Published 85,979 benchmark</td><td class="cross">&#10007;</td><td class="partial">pilot only</td><td class="check">&#10003;</td></tr>
    <tr><td>Photo &rarr; grounded treatment (95&ndash;97%)</td><td class="partial">partial</td><td class="cross">&#10007;</td><td class="check">&#10003;</td></tr>
    <tr><td>Field soil-moisture dataset + model</td><td class="cross">&#10007;</td><td class="cross">&#10007;</td><td class="check">&#10003;</td></tr>
  </table>
  <div class="sub-head mt-2">Four Novel Contributions</div>
  <ul class="bullet-list">
    <li><strong>Four-stage safety-verified agent pipeline</strong> &mdash; Safety/Router &rarr; Retrieval &rarr; Generation &rarr; Verifier &mdash; unsafe categories stop before any retrieval.</li>
    <li><strong>Structured claim verifier</strong> with a 14-field atomic claim schema and 6 relation types, checking each chemical amount/unit/dosage/PHI against retrieved evidence.</li>
    <li><strong>Two original field-collected Bengali datasets</strong> &mdash; 722 tensiometer-labeled soil-moisture images (Pabna District) + 1,000-query farmer benchmark (300 field interviews, Rajshahi &amp; Natore).</li>
    <li><strong>85,979-instance provenance-traced benchmark</strong> across 4 tracks, CC-BY-4.0, enabling third-party validation.</li>
  </ul>
</div>

</div><!-- /col A -->

<!-- ============ COLUMN B ============ -->
<div class="col">

<!-- Pipeline diagram -->
<div class="pipeline-diagram">
  <div class="pipeline-title">The System: Four-Stage Safety-Verified Pipeline</div>
  <div class="pipeline-input">&laquo; &nbsp;&#2453;&#2499;&#2487;&#2453;&#2503;&#2480; &#2474;&#2509;&#2480;&#2486;&#2509;&#2472; / &#2474;&#2494;&#2468;&#2494;&#2480; &#2455;&#2476;&#2495;&nbsp; &raquo;<br><span style="color:rgba(255,255,255,0.45);font-size:var(--t-cap)">Farmer query in Bengali dialect or leaf photo upload</span></div>
  <div class="pipe-arrow">&#9660;</div>
  <div class="stage-box s1">
    <div class="stage-num">Stage 1</div>
    <div class="stage-name">Safety / Router &mdash; Classify BEFORE Retrieval</div>
    <div class="stage-detail">Deterministic rule pre-filter + LLM structured-output call. Fail-closed: unknown categories &rarr; low_confidence &rarr; 16123. Never reaches retrieval or generation if unsafe.</div>
  </div>
  <div class="unsafe-branch">
    <div class="unsafe-arrow">&#8630; UNSAFE &rarr;</div>
    <div class="unsafe-box">
      <div class="unsafe-head">Immediate redirect &mdash; generation &amp; retrieval entirely skipped</div>
      <div class="unsafe-num">16123</div>
      <div style="font-size:var(--t-cap);color:rgba(255,255,255,0.7);margin-top:1mm">Krishi Call Center (banned chemical, low confidence) &middot; <strong style="color:#ff7f5c">999</strong> (self-harm/poisoning risk) &middot; Silent drop (prompt injection)</div>
    </div>
  </div>
  <div class="pipe-arrow">&#9660;</div>
  <div class="stage-box s2">
    <div class="stage-num">Stage 2</div>
    <div class="stage-name">Retrieval &mdash; Hybrid BM25 + FAISS Dense, RRF Fusion</div>
    <div class="stage-detail">Top-5 passages from 2,882-node KG / 284 govt. publications. R@10 = 0.539 (Hybrid RRF). Bengali + 6 dialect queries supported.</div>
  </div>
  <div class="pipe-arrow">&#9660;</div>
  <div class="stage-box s3">
    <div class="stage-num">Stage 3</div>
    <div class="stage-name">Generation &mdash; Gemma-4-E4B 4-bit (KrishokChat-4B LoRA r=32)</div>
    <div class="stage-detail">Streamed Bengali response, source-cited. 0.31% safety failure rate &mdash; lowest across all tested models. GenF1 0.314 vs 0.165 best zero-shot.</div>
  </div>
  <div class="pipe-arrow">&#9660;</div>
  <div class="stage-box s4">
    <div class="stage-num">Stage 4</div>
    <div class="stage-name">Structured Claim Verifier &mdash; 14-field schema, 6 relation types</div>
    <div class="stage-detail">Each chemical claim split into 14 atomic fields. Safety-critical claims need all fields supported against retrieved evidence &mdash; else abstain. Deterministic-first, fail-closed.</div>
  </div>
  <div class="pipe-arrow">&#9660;</div>
  <div class="stage-box s5">
    <div class="stage-num">Audit Log</div>
    <div class="stage-name">Local JSONL &rarr; /analytics Dashboard</div>
    <div class="stage-detail">Every decision logged locally. /analytics shows Safe vs. Blocked donut, category breakdown, retrieval hit rate, verifier pass rate, and CSV export.</div>
  </div>
  <div class="pipe-output">&#2474;&#2509;&#2480;&#2468;&#2495;&#2453;&#2509;&#2480;&#2495;&#2527;&#2494; + &#2494;&#2468;&#2509;&#2488; + &#2472;&#2495;&#2480;&#2494;&#2474;&#2468;&#2509;&#2468;&#2494; &#2475;&#2509;&#2482;&#2509;&#2479;&#2494;&#2455; &nbsp;&middot;&nbsp; <strong>Answer + sources + safety flags</strong></div>
</div>

<!-- B2 Safety taxonomy -->
<div class="card card--clay">
  <div class="sec-head">Six-Way Safety Classification</div>
  <div class="body-sm mb-2">Deterministic rule pre-filter runs first; LLM structured-output call classifies the rest. Unknown categories and classifier outages <strong>fail closed to <em>low_confidence</em></strong> &mdash; never permission to retrieve or generate.</div>
  <div class="safety-chips">
    <div class="safety-chip chip-g"><strong>safe_agri</strong><span class="chip-route">&rarr; proceed to retrieval</span></div>
    <div class="safety-chip chip-c"><strong>banned_or_restricted_chemical</strong><span class="chip-route">&rarr; 16123 Krishi Call Center</span></div>
    <div class="safety-chip chip-c"><strong>self_harm_or_poisoning_risk</strong><span class="chip-route">&rarr; 999 + 16123 + medical help</span></div>
    <div class="safety-chip chip-o"><strong>off_topic</strong><span class="chip-route">&rarr; scope message</span></div>
    <div class="safety-chip chip-m"><strong>prompt_injection</strong><span class="chip-route">&rarr; silent refusal</span></div>
    <div class="safety-chip chip-m"><strong>low_confidence</strong><span class="chip-route">&rarr; 16123 referral</span></div>
  </div>
</div>

<!-- B3 Verifier -->
<div class="card card--leaf">
  <div class="sec-head">Structured Dosage Verification (SOTA)</div>
  <div class="body-sm mb-2">Each generated answer is split into <strong>atomic claims</strong>. Each claim carries a <strong>14-field schema</strong> (red fields are safety-critical):</div>
  <div class="schema-grid">
    <div class="schema-f">crop</div><div class="schema-f">disease</div><div class="schema-f">action</div><div class="schema-f">chemical</div>
    <div class="schema-f crit">formulation</div><div class="schema-f crit">amount</div><div class="schema-f crit">unit</div><div class="schema-f crit">denominator</div>
    <div class="schema-f crit">interval</div><div class="schema-f crit">PHI/safety</div><div class="schema-f">polarity</div><div class="schema-f">applicability</div>
    <div class="schema-f">uncertainty</div><div class="schema-f">source_id</div><div class="schema-f" style="grid-column:span 2;font-style:italic;color:#8a7d6e">14 fields total</div>
  </div>
  <div class="body-sm mt-2 mb-2">Every claim matched against retrieved evidence through <strong>6 relation types</strong>:</div>
  <div class="rel-chips">
    <div class="rel-chip">supported</div><div class="rel-chip">contradicted</div><div class="rel-chip">partially_supported</div>
    <div class="rel-chip">unsupported</div><div class="rel-chip">ambiguous</div><div class="rel-chip">not_applicable</div>
  </div>
  <div class="body-sm mt-2"><strong style="color:#a8542b">Safety-critical claims</strong> require all fields present and supported against retrieved evidence. Missing evidence &rarr; <strong>abstain</strong> (annotate-and-drop). Verifier is deterministic-first: parser/normalizer + structured relation matcher + fail-closed safety policy.</div>
</div>

<!-- Screenshot: Safety refusal -->
<div style="border-radius:3mm;overflow:hidden;border:0.4mm solid var(--bone);">
  <div class="screenshot-wrap"><img src="screenshots/02_chat_safety_refusal_16123.png" alt="Chat safety refusal: banned chemical query gets 16123 redirect"/></div>
  <div class="screenshot-caption">Banned chemical query &rarr; immediate 16123 redirect. Retrieval, generation &amp; verifier entirely skipped.</div>
</div>

<!-- Screenshot: Analytics -->
<div style="border-radius:3mm;overflow:hidden;border:0.4mm solid var(--bone);">
  <div class="screenshot-wrap"><img src="screenshots/04_analytics_audit_dashboard.png" alt="Analytics audit dashboard: Safe vs Blocked donut, metrics"/></div>
  <div class="screenshot-caption">/analytics &mdash; real-time Safe vs. Blocked donut &middot; 100% source retrieval hit rate &middot; 63% verifier pass rate &middot; CSV export</div>
</div>

</div><!-- /col B -->

<!-- ============ COLUMN C ============ -->
<div class="col">

<!-- C1 Crop disease -->
<div class="card card--leaf">
  <div class="sec-head">Crop Disease Detection &mdash; 95&ndash;97% Accuracy</div>
  <div class="body-sm mb-2">Five crop families, 37 disease classes (live system), ~22,544 training images. Models exported to <strong>ONNX FP16 + TFLite INT8/FP16</strong> for &lt;30 ms inference on Android edge devices.</div>
  <table>
    <tr><th>Crop</th><th>Classes</th><th>Top-1</th><th>Wt. F1</th><th>Edge format</th></tr>
    <tr><td><strong>Brassica</strong></td><td class="num">11</td><td class="num hi">97.29%</td><td class="num">0.965</td><td style="font-size:var(--t-foot)">ONNX 21.8 MB</td></tr>
    <tr><td><strong>Rice</strong></td><td class="num">8</td><td class="num hi">96.49%</td><td class="num">0.965</td><td style="font-size:var(--t-foot)">ONNX 6.2 MB &middot; 1.1 ms/img</td></tr>
    <tr><td><strong>Corn</strong></td><td class="num">4</td><td class="num hi">97.23%</td><td class="num">0.972</td><td style="font-size:var(--t-foot)">ONNX 21.8 MB</td></tr>
    <tr><td><strong>Potato</strong></td><td class="num">3</td><td class="num hi">95.04%</td><td class="num">0.951</td><td style="font-size:var(--t-foot)">TFLite INT8 1.6 MB</td></tr>
    <tr><td><strong>Wheat</strong></td><td class="num">11</td><td class="num">88% (live)</td><td class="num">&mdash;</td><td style="font-size:var(--t-foot)">ONNX</td></tr>
  </table>
  <div class="body-sm mt-2">/detect page: crop classifier &rarr; per-crop disease model &rarr; Bengali treatment from knowledge map &rarr; same 4-stage verifier.</div>
  <div class="mt-2">
    <span class="novelty-badge">Wheat: 50/50 (100%) Bengali treatment returned</span>
    <span class="novelty-badge">437-image library: 436/437 (99.8%) Bengali advisory</span>
  </div>
  <div class="caption">Production pipeline results &mdash; photo-to-Bengali-treatment end-to-end, not training metrics.</div>
</div>

<!-- Screenshot: Detect -->
<div style="border-radius:3mm;overflow:hidden;border:0.4mm solid var(--bone);">
  <div class="screenshot-wrap"><img src="screenshots/01_detect_rice_disease_diagnosis.png" alt="Detect page: rice leaf brown spot at 98% confidence with Bengali treatment"/></div>
  <div class="screenshot-caption">/detect &mdash; uploaded rice specimen &rarr; 4-node agent trace &rarr; &#2476;&#2494;&#2470;&#2494;&#2478;&#2496; &#2470;&#2494;&#2455; &#2480;&#2507;&#2455; (Brown Spot) at 98% confidence with grounded Bengali treatment</div>
</div>

<!-- C2 Soil moisture -->
<div class="card card--ochre">
  <div class="sec-head">Soil Moisture &mdash; Field Dataset + Regression Model</div>
  <div class="body-sm mb-2"><strong>Original fieldwork:</strong> 722 tensiometer-labeled RGB soil photos &middot; 0.0&ndash;21.5 kPa &middot; 6 USDA soil types &middot; 14 crops &middot; 8 growth stages. Pabna District, 3-day campaign (May 29&ndash;31, 2026). 693 usable samples after removing 29 duplicates. 46 series, series-stratified split, leakage-free.</div>
  <div class="soil-scatter"><img src="../../../backend/ml_assets/soil/pred_vs_actual.png" alt="Soil moisture predicted vs actual scatter R2=0.39"/></div>
  <table>
    <tr><th>Metric</th><th>EffNet-B0 (5-fold OOF, N=693)</th><th>Mean baseline</th></tr>
    <tr><td><strong>RMSE</strong></td><td class="num hi">4.09 kPa</td><td class="num">5.26 kPa</td></tr>
    <tr><td><strong>MAE</strong></td><td class="num hi">3.19 kPa</td><td class="num">&mdash;</td></tr>
    <tr><td><strong>R&sup2;</strong></td><td class="num hi">0.39</td><td class="num">0.00</td></tr>
    <tr><td><strong>Improvement</strong></td><td class="num hi" colspan="2">22% RMSE reduction over mean-predictor baseline</td></tr>
  </table>
  <div class="body-sm mt-2">EfficientNet-B0 (4.17M params), Optuna-tuned (15 trials), SmoothL1Loss, 15 epochs, 5-fold CV. Per-fold R&sup2; 0.22&ndash;0.52; best fold R&sup2;=0.52. Best soil MAE: Atel (Clay) 2.98 kPa.</div>
</div>

<!-- Screenshot: Chat advisory -->
<div style="border-radius:3mm;overflow:hidden;border:0.4mm solid var(--bone);">
  <div class="screenshot-wrap"><img src="screenshots/03_chat_verified_advisory.png" alt="Chat page: grounded Bengali advisory with source citations and verified badge"/></div>
  <div class="screenshot-caption">/chat &mdash; agronomic query &rarr; streamed Bengali response with citations [&#9699;] &middot; &#2479;&#2494;&#2458;&#2494;&#2439;&#2453;&#2499;&#2468; (Verified) badge &middot; TTS &#2486;&#2497;&#2472;&#2497;&#2472; &middot; 5 grounded references</div>
</div>

<!-- C4 Impact -->
<div class="card card--leaf">
  <div class="sec-head">Impact on Society &amp; Environment</div>
  <div class="impact-item"><div class="impact-icon">&#128737;</div><div class="impact-text"><strong>Health &amp; Safety:</strong> Refusing unsafe agrochemical queries and verifying dosages against government sources reduces pesticide misuse and accidental poisoning. At-risk users are redirected to 16123 and 999.</div></div>
  <div class="impact-item"><div class="impact-icon">&#127807;</div><div class="impact-text"><strong>Environment:</strong> Source-grounded dosage advice lowers over-application of pesticides and fertilizers, reducing soil and water contamination. Edge-deployable models reduce cloud compute requirements.</div></div>
  <div class="impact-item"><div class="impact-icon">&#128225;</div><div class="impact-text"><strong>Access:</strong> ~47 million farming households; laptop-deployable and offline-capable. Android edge models (&lt;30 ms) reach the connectivity gap that cloud-only tools cannot.</div></div>
</div>

<!-- C5 Business model -->
<div class="card card--ochre">
  <div class="sec-head">Business Model &amp; Market Readiness</div>
  <div class="biz-lane"><div class="biz-lane__head">&#9312; Freemium + B2B</div><div class="biz-lane__body">Free advisory + diagnosis for farmers; paid audit/analytics dashboard for agro-dealers, SAAOs, extension officers. Comparator: PxD 7.8M users; ACI IDSS/Fosholi &euro;3.5M 2025 target.</div></div>
  <div class="biz-lane"><div class="biz-lane__head">&#9313; B2G &mdash; Government Partnership</div><div class="biz-lane__body">AI front-end to 16123 Krishi Call Center (triage + escalation). The audit engine is the least-commoditized trust asset for DAE/a2i.</div></div>
  <div class="biz-lane"><div class="biz-lane__head">&#9314; Dataset + API Licensing</div><div class="biz-lane__body">85,979 benchmark + 722-image soil dataset (CC-BY-4.0). Advisory API for agri-fintech; third-party validation access.</div></div>
  <div class="body-sm mt-2"><strong>Market readiness:</strong> working end-to-end prototype (chat + vision + soil + audit + research panel), two papers under peer review, datasets published, edge-deployable models.</div>
</div>

<!-- C6 Roadmap + QR -->
<div class="card card--bone">
  <div class="sec-head" style="color:var(--ink)">Roadmap &amp; Access</div>
  <div class="roadmap-item">Voice-output TTS for low-literacy users (Bengali audio advisory)</div>
  <div class="roadmap-item">Extended dialect coverage across all 6 regional variants</div>
  <div class="roadmap-item">Soil-model refinement for higher-accuracy irrigation advisories</div>
  <div class="roadmap-item">B2B pilot with district extension office</div>
  <div class="roadmap-item">Full business model &amp; market evaluation for capstone delivery</div>
  <div class="qr-row">
    <div class="qr-item"><div class="qr-box">Dataset<br>HuggingFace<br>RaiyanKhaan/<br>KrishokChat</div><div class="qr-label">Dataset (HF)</div></div>
    <div class="qr-item"><div class="qr-box">GitHub<br>RaiyaanReza/<br>KrishokChat-<br>Advisory</div><div class="qr-label">Code &amp; Demo</div></div>
    <div class="qr-item"><div class="qr-box">EACL 2026<br>&amp;<br>SIGIR-AP 2026<br>Papers</div><div class="qr-label">Research Papers</div></div>
  </div>
</div>

</div><!-- /col C -->
</div><!-- /columns -->

<!-- FOOTER -->
<div class="footer">
  <div class="footer__refs"><strong>References:</strong> KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory (EACL 2026, under review) &middot; AgriTrust: Verified Bengali Agricultural Advisory via Structured Claim Grounding (SIGIR-AP 2026, under review) &middot; AgriVision BD: Disease Detection for Bangladeshi Crops (Project Report 3, April 2026). Datasets CC-BY-4.0. Source institutions: BARC, BARI, BRRI, IRRI, DAE, DLS, DoF, CABI Plantwise + 5 others. HuggingFace: RaiyanKhaan/KrishokChat-Advisory-System.</div>
  <div class="footer__contact">North South University, Bangladesh &middot; 2026<br/>Faculty Advisor: Dr. Sumaiya Tabassum Nimi (STI)<br/>Krishi Call Center: 16123 &middot; Emergency: 999</div>
</div>

</div><!-- /poster -->
</body>
</html>"""

OUT.write_text(HTML, encoding="utf-8")
size_kb = OUT.stat().st_size / 1024
print(f"Written: {OUT}")
print(f"Size: {size_kb:.1f} KB")
