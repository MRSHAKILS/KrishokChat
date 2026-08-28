#!/usr/bin/env python3
"""
compile_innovation_fair_pdf.py

Compiles the 20-Page Supporting Dossier and the 8-Slide Pitch Deck
into publication-grade, styled PDF documents for the Bangladesh Innovation Fair 2026.
Uses headless Microsoft Edge / Google Chrome with print CSS for exact pagination.
"""

import os
import subprocess
import markdown
from pathlib import Path

FAIR_DIR = Path(r"d:\KrishokChat Advisory System\paper\Innovation Fair")

# Locate browser binary
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER = CHROME_PATH if os.path.exists(CHROME_PATH) else EDGE_PATH

def render_html_to_pdf(html_content: str, out_pdf_path: Path, landscape: bool = False):
    temp_html = FAIR_DIR / "temp_render.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    cmd = [
        BROWSER,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={str(out_pdf_path)}",
        "--no-pdf-header-footer",
        str(temp_html)
    ]
    
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if temp_html.exists():
        temp_html.unlink()
    print(f"  [Compiled PDF] -> {out_pdf_path.name} ({out_pdf_path.stat().st_size / 1024:.1f} KB)")

# ----------------------------------------------------------------------------
# 1. COMPILE 20-PAGE SUPPORTING DOSSIER
# ----------------------------------------------------------------------------
def build_dossier_pdf():
    dossier_md_path = FAIR_DIR / "05_20_PAGE_SUPPORTING_DOSSIER.md"
    with open(dossier_md_path, encoding="utf-8") as f:
        md_text = f.read()
        
    # Split into sections or page breaks
    body_html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])
    
    # Custom CSS for executive government/investor due-diligence report
    dossier_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>KrishokChat — Research Evidence & Deployment Dossier</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 18mm 16mm 20mm 16mm;
    @bottom-right {{
      content: "Page " counter(page);
      font-size: 8pt;
      font-family: 'Segoe UI', sans-serif;
      color: #5C5248;
    }}
    @bottom-left {{
      content: "KrishokChat | Bangladesh Innovation Fair 2026";
      font-size: 8pt;
      font-family: 'Segoe UI', sans-serif;
      color: #5C5248;
    }}
  }}
  
  body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #2C241E;
    line-height: 1.55;
    font-size: 10pt;
    background: #FFFFFF;
  }}
  
  h1 {{
    color: #1E5E3A;
    font-size: 18pt;
    border-bottom: 2px solid #1E5E3A;
    padding-bottom: 4px;
    margin-top: 24pt;
    page-break-before: always;
  }}
  h1:first-of-type {{
    page-break-before: avoid;
  }}
  
  h2 {{
    color: #B87333;
    font-size: 13pt;
    margin-top: 16pt;
    border-bottom: 1px solid #E5DFD5;
    padding-bottom: 3px;
  }}
  
  h3 {{
    color: #1E5E3A;
    font-size: 11pt;
    margin-top: 12pt;
  }}
  
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0;
    font-size: 8.5pt;
  }}
  
  th, td {{
    border: 1px solid #D8D2C6;
    padding: 6px 8px;
    text-align: left;
  }}
  
  th {{
    background-color: #F4F1EA;
    color: #1E5E3A;
    font-weight: 600;
  }}
  
  tr:nth-child(even) {{
    background-color: #FAF8F5;
  }}
  
  blockquote {{
    background: #F4F1EA;
    border-left: 4px solid #1E5E3A;
    margin: 10pt 0;
    padding: 8pt 12pt;
    font-style: italic;
    color: #4A4036;
  }}
  
  pre, code {{
    font-family: 'Cascadia Code', Consolas, 'Courier New', monospace;
    font-size: 8pt;
    background: #F3EFEA;
    padding: 2px 4px;
    border-radius: 3px;
  }}
  
  pre {{
    padding: 10pt;
    border: 1px solid #D8D2C6;
    overflow-x: auto;
    line-height: 1.35;
    white-space: pre-wrap;
  }}
  
  .badge {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 600;
  }}
  
  .badge-green {{ background: #EAF7EA; color: #2E6F40; border: 1px solid #2E6F40; }}
  .badge-gold {{ background: #FDF6E2; color: #B87333; border: 1px solid #B87333; }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""
    out_pdf = FAIR_DIR / "KrishokChat_Supporting_Dossier_20_Pages.pdf"
    render_html_to_pdf(dossier_html, out_pdf, landscape=False)

# ----------------------------------------------------------------------------
# 2. COMPILE 8-SLIDE PITCH DECK PDF
# ----------------------------------------------------------------------------
def build_deck_pdf():
    deck_md_path = FAIR_DIR / "03_8_SLIDE_PITCH_DECK.md"
    with open(deck_md_path, encoding="utf-8") as f:
        md_text = f.read()
        
    slides_raw = md_text.split("---")
    slides_html = ""
    
    for idx, s in enumerate(slides_raw[1:], start=1):
        parsed = markdown.markdown(s.strip(), extensions=['tables', 'fenced_code'])
        slides_html += f"""
        <div class="slide">
          <div class="slide-header">
            <span class="logo">KrishokChat</span>
            <span class="slide-num">SLIDE {idx} / 8</span>
          </div>
          <div class="slide-content">
            {parsed}
          </div>
          <div class="slide-footer">
            <span>Bangladesh Innovation Fair 2026 • Research Track & National Deployment</span>
            <span>Ref: 36 Empirical CEA Layers</span>
          </div>
        </div>
        """
        
    deck_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>KrishokChat — 8-Slide Innovation Fair Deck</title>
<style>
  @page {{
    size: 297mm 210mm; /* A4 Landscape */
    margin: 0;
  }}
  
  body {{
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: #2C241E;
    background: #FAF8F5;
  }}
  
  .slide {{
    width: 297mm;
    height: 210mm;
    page-break-after: always;
    box-sizing: border-box;
    padding: 16mm 20mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #FFFFFF;
    border-bottom: 3px solid #1E5E3A;
  }}
  
  .slide-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #1E5E3A;
    padding-bottom: 8px;
  }}
  
  .logo {{
    font-size: 16pt;
    font-weight: 800;
    color: #1E5E3A;
    letter-spacing: -0.5px;
  }}
  
  .slide-num {{
    font-size: 10pt;
    font-weight: 700;
    color: #B87333;
    background: #FAF3E8;
    padding: 3px 10px;
    border-radius: 12px;
    border: 1px solid #E5DFD5;
  }}
  
  .slide-content {{
    flex: 1;
    padding: 12mm 0;
    font-size: 11pt;
    line-height: 1.5;
  }}
  
  .slide-content h2 {{
    color: #1E5E3A;
    font-size: 18pt;
    margin-top: 0;
    margin-bottom: 12pt;
    font-weight: 700;
  }}
  
  .slide-content h3 {{
    color: #B87333;
    font-size: 13pt;
    margin-top: 10pt;
    margin-bottom: 6pt;
  }}
  
  .slide-content ul {{
    margin: 6pt 0;
    padding-left: 20px;
  }}
  
  .slide-content li {{
    margin-bottom: 6pt;
  }}
  
  .slide-content strong {{
    color: #1E5E3A;
  }}
  
  .slide-content pre {{
    background: #F4F1EA;
    padding: 8pt 12pt;
    border-radius: 6px;
    border: 1px solid #D8D2C6;
    font-size: 9pt;
    line-height: 1.35;
  }}
  
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #E5DFD5;
    padding-top: 8px;
    font-size: 8.5pt;
    color: #7A6F62;
  }}
</style>
</head>
<body>
{slides_html}
</body>
</html>
"""
    out_pdf = FAIR_DIR / "KrishokChat_8_Slide_Pitch_Deck.pdf"
    render_html_to_pdf(deck_html, out_pdf, landscape=True)

if __name__ == "__main__":
    print("=" * 80)
    print("COMPILING BANGLADESH INNOVATION FAIR 2026 PDF ARTIFACTS")
    print("=" * 80)
    build_dossier_pdf()
    build_deck_pdf()
    print("=" * 80)
    print("ALL INNOVATION FAIR PDFS GENERATED SUCCESSFULLY IN:", FAIR_DIR)
    print("=" * 80)
