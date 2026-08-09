"""Generate knowledge node generation guide as PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

ROOT = r"D:\KrishokChat Advisory System"
OUT = os.path.join(ROOT, "docs", "knowledge_node_generation_guide.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=0.6*inch, rightMargin=0.6*inch,
                        topMargin=0.6*inch, bottomMargin=0.6*inch)

s = lambda n, **kw: ParagraphStyle(n, **kw)
title = s('KsTitle', fontSize=22, leading=28, textColor=HexColor('#1a5632'), alignment=TA_CENTER, spaceAfter=18)
h1 = s('KsH1', fontSize=15, leading=20, textColor=HexColor('#2d7d46'), spaceBefore=16, spaceAfter=8)
h2 = s('KsH2', fontSize=12, leading=16, textColor=HexColor('#3d8b4f'), spaceBefore=12, spaceAfter=6)
body = s('KsBody', fontSize=10, leading=14, textColor=HexColor('#333333'), spaceAfter=5)
code = s('KsCode', fontSize=9, leading=12, textColor=HexColor('#1a1a1a'), fontName='Courier', backColor=HexColor('#f5f5f5'), leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4, borderPadding=6)
prompt = s('KsPrompt', fontSize=9, leading=12, textColor=HexColor('#1a1a1a'), fontName='Courier', backColor=HexColor('#e8f5e9'), leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=8, borderPadding=6, borderColor=HexColor('#2d7d46'), borderWidth=1)
note = s('KsNote', fontSize=9, leading=12, textColor=HexColor('#b35900'), backColor=HexColor('#fff8e1'), leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=8, borderPadding=6, borderColor=HexColor('#b35900'), borderWidth=1)

story = []
story.append(Paragraph("KrishokChat — Knowledge Node Generation Guide", title))
story.append(Paragraph("Bangladesh Agricultural AI Advisory System", body))
story.append(Spacer(1, 16))

story.append(Paragraph("Overview", h1))
story.append(Paragraph("This guide explains how to generate knowledge nodes for crop diseases using web LLMs (ChatGPT, Gemini, Claude, etc.). Workers follow each prompt below, collect outputs as JSON, and submit for merging into the RAG index.", body))
story.append(Spacer(1, 8))

story.append(Paragraph("Workflow", h1))
story.append(Paragraph("1. Pick one disease from the list below", body))
story.append(Paragraph("2. Copy the EXACT prompt into a web LLM (ChatGPT / Gemini / Claude)", body))
story.append(Paragraph("3. Copy the JSON output into a file named [crop]_[disease].json", body))
story.append(Paragraph("4. Repeat for all 12 diseases", body))
story.append(Paragraph("5. Submit all JSON files for merging into the RAG index", body))
story.append(Spacer(1, 8))

story.append(Paragraph("Output JSON Format (copy exactly)", h1))
story.append(Paragraph('{<br/>  "id": "GEN_WHEAT_BlackPoint",<br/>  "category": "disease",<br/>  "title_bn": "...",<br/>  "title_en": "...",<br/>  "content_bn": "...",<br/>  "content_en": "...",<br/>  "summary": "...",<br/>  "tags": ["tag1", "tag2"],<br/>  "source_document": "...",<br/>  "publisher": "...",<br/>  "treatment_summary_bn": "...",<br/>  "prevention_bn": "...",<br/>  "bm25_text": "...",<br/>  "embed_text": "..."<br/>}', code))
story.append(Spacer(1, 16))

story.append(PageBreak())
story.append(Paragraph("PROMPTS — Copy each one into a web LLM", h1))

prompts = [
    ("1. BlackPoint (Wheat)", """You are a Bangladeshi agricultural expert. Write a detailed knowledge node for Black Point disease of wheat (গমের ব্ল্যাক পয়েন্ট রোগ) in Bangladesh context.

Include:
- description_bn / description_en: What is Black Point? Symptoms on grain (black discoloration at germ end).
- cause_bn / cause_en: Fungal pathogens (Bipolaris, Alternaria), humid weather, rain during grain filling.
- treatment_summary_bn: Seed treatment (Provax-200, Tilt 250 EC — APPROXIMATE rates per kg seed), fungicide spray options.
- prevention_bn: Resistant varieties, crop rotation, proper drying and storage, use certified seed.

IMPORTANT: Use Bangladesh-specific context. Mention BARC/BARI recommendations if known. Add disclaimer: 'বিস্তারিত মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২ৃ' at end of treatment_summary_bn.

Return ONLY valid JSON matching the Output Format above."""),
    ("2. Cabbage Alternaria Spot", """You are a Bangladeshi agricultural expert. Write a detailed knowledge node for Alternaria Spot of cabbage (বাঁধাকপির অল্টারনেরিয়া দাগ রোগ) in Bangladesh context.

Include:
- description_bn/en: Dark brown spots with concentric rings on leaves, leaf drop.
- cause_bn/en: Alternaria brassicicola, humid conditions, infected seeds/crop debris.
- treatment_summary_bn: Mancozeb (approx 2.5g/L), Rovral 50 WP, Copper oxychloride — APPROXIMATE rates.
- prevention_bn: Seed treatment with hot water (50C 30 min), 2-3 year crop rotation, field sanitation, resistant varieties.

Add disclaimer at end of treatment: 'বিস্তারিত মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২ৃ'. Return ONLY valid JSON. id: GEN_BRASSICA_Cabbage_Alternaria_Spot"""),
    ("3. Cabbage Black Rot", """Write knowledge node for Black Rot of cabbage (বাঁধাকপির ব্ল্যাক রট রোগ) in Bangladesh. Bacterial disease (Xanthomonas campestris). V-shaped yellow lesions from leaf margin, black veins. Treatment: Copper hydroxide, Streptomycin sulfate, bleach seed treatment. Prevention: 2-3 year rotation, certified seed, avoid overhead irrigation, field sanitation. Add 16123 disclaimer. id: GEN_BRASSICA_Cabbage_Black_Rot. Return ONLY valid JSON."""),
    ("4. Cabbage Downy Mildew", """Write knowledge node for Downy Mildew of cabbage (বাঁধাকপির ডাউনি মিলডিউ রোগ) in Bangladesh. Pathogen: Hyaloperonospora brassicae. White/gray fuzz on underside of leaves, yellow patches above. Treatment: Metalaxyl-Mancozeb, Copper hydroxide, Aliette — APPROXIMATE rates. Prevention: Good air circulation, avoid overhead irrigation, resistant varieties, field sanitation. Add 16123 disclaimer. id: GEN_BRASSICA_Cabbage_Downy_Mildew. Return ONLY valid JSON."""),
    ("5. Cauliflower Alternaria Disease", """Write knowledge node for Alternaria Disease of cauliflower (ফুলকপির অল্টারনেরিয়া রোগ) in Bangladesh. Dark brown to black spots on curd and leaves, fuzzy spore masses in humid weather. Treatment: Mancozeb, Iprodione, Chlorothalonil — APPROXIMATE rates. Prevention: Seed treatment, 2-3 year rotation, remove infected debris, resistant varieties. Add 16123 disclaimer. id: GEN_BRASSICA_Cauliflower_Alternaria_Disease. Return ONLY valid JSON."""),
    ("6. Cauliflower Bacterial Soft Rot", """Write knowledge node for Bacterial Soft Rot of cauliflower (ফুলকপির ব্যাকটেরিয়াল সফট রট রোগ) in Bangladesh. Soft, watery rot with foul odor, curd disintegration. Pathogens: Pectobacterium carotovorum, Erwinia. Treatment: Copper-based sprays (preventive), remove infected plants, avoid mechanical injury. Prevention: Good drainage, crop rotation, sanitation, careful harvesting. Add 16123 disclaimer. id: GEN_BRASSICA_Cauliflower_Bacterial_Soft_Rot. Return ONLY valid JSON."""),
    ("7. Cauliflower Bacterial Spot", """Write knowledge node for Bacterial Spot of cauliflower (ফুলকপির ব্যাকটেরিয়াল স্পট রোগ) in Bangladesh. Small, water-soaked spots on leaves that turn brown/necrotic. Pathogen: Xanthomonas campestris pv. armoraciae. Treatment: Copper hydroxide, Copper oxychloride — APPROXIMATE rates. Prevention: Hot water seed treatment, crop rotation, certified seed, field sanitation. Add 16123 disclaimer. id: GEN_BRASSICA_Cauliflower_Bacterial_Spot. Return ONLY valid JSON."""),
    ("8. Cauliflower Black Spot", """Write knowledge node for Black Spot of cauliflower (ফুলকপির ব্ল্যাক স্পট রোগ) in Bangladesh. Dark brown to black spots on curd and wrapper leaves. Pathogens: Alternaria brassicicola, A. brassicae. Treatment: Mancozeb, Chlorothalonil, Iprodione — APPROXIMATE rates. Prevention: Seed treatment, 2-3 year rotation, remove debris, proper spacing. Add 16123 disclaimer. id: GEN_BRASSICA_Cauliflower_Black_Spot. Return ONLY valid JSON."""),
    ("9. Cauliflower Downy Mildew", """Write knowledge node for Downy Mildew of cauliflower (ফুলকপির ডাউনি মিলডিউ রোগ) in Bangladesh. Pathogen: Hyaloperonospora brassicae. White/gray fungal growth under leaves, yellow patches above. Treatment: Metalaxyl, Copper hydroxide, Dimethomorph — APPROXIMATE rates. Prevention: Good air circulation, avoid overhead irrigation, resistant varieties, field sanitation. Add 16123 disclaimer. id: GEN_BRASSICA_Cauliflower_Downy_Mildew. Return ONLY valid JSON."""),
    ("10. Cauliflower Nutrient Deficiency", """Write knowledge node for Nutrient Deficiency in cauliflower (ফুলকপির পুষ্টির ঘাটতি) in Bangladesh. Focus on Boron deficiency (brown/rotted curd, hollow stem, distorted leaves) and Magnesium deficiency (interveinal chlorosis on older leaves). Treatment: Borax (approx 10-20 kg/ha soil or 0.2-0.3% foliar), Magnesium sulfate (approx 0.5% foliar), Epsom salt. Prevention: Soil testing, balanced NPK fertilization, organic matter addition, liming if acidic. Add 16123 disclaimer. id: GEN_BRASSICA_Cauliflower_Nutrient_Deficiency. Return ONLY valid JSON."""),
    ("11. Rice Healthy Leaf", """Write knowledge node for Healthy Rice Leaf (সুস্থ ধানের পাতা) in Bangladesh. Indicators of healthy rice plant: dark green upright leaves, no spots or lesions, uniform growth, strong tillers. General care: Proper water management (alternate wetting and drying), balanced fertilization (NPK, Zn, S), integrated pest management (avoid prophylactic spraying), regular field monitoring for early pest/disease signs. When to be concerned: yellowing, spots, wilting, stunting. Prevention: Use resistant varieties (BRRI dhan series), maintain field hygiene, proper spacing. This is a POSITIVE health node — not a disease. id: GEN_RICE_Healthy_Leaf. Return ONLY valid JSON."""),
    ("12. Cabbage Healthy Leaf", """Write knowledge node for Healthy Cabbage Leaf (সুস্থ বাঁধাকপির পাতা) in Bangladesh. Indicators: firm, crisp, uniformly green leaves without yellowing, spots, or insect damage. General care: Consistent moisture (not waterlogged), balanced fertilization (NPK), mulching, regular inspection for early pest signs (aphids, diamondback moth). Healthy plants resist disease better. Prevention: Proper spacing for air circulation, crop rotation, clean field practices, use quality seed. This is a POSITIVE health node — not a disease. id: GEN_BRASSICA_Cabbage_Healthy_Leaf. Return ONLY valid JSON."""),
]

for title, prompt in prompts:
    story.append(Paragraph(title, h2))
    story.append(Paragraph(prompt, prompt))

story.append(PageBreak())
story.append(Paragraph("QUALITY CHECKLIST", h1))
checks = [
    "Every field is filled (no empty strings)",
    "description_bn and content_bn contain ACTUAL Bangla text (not English transliteration)",
    "Chemical names are generic (Mancozeb, Copper hydroxide, Metalaxyl, Borax) — not brand names",
    "Rates are APPROXIMATE (approx) with disclaimer to call 16123",
    "Tags include crop name AND disease name",
    "source_document mentions real source (book, institution, expert, website)",
    "Valid JSON — test at jsonlint.com before submitting",
    "For healthy nodes: no disease/treatment info — focus on positive indicators and care",
]
for c in checks:
    story.append(Paragraph("• " + c, body))

story.append(Spacer(1, 16))
story.append(Paragraph("IMPORTANT NOTES", h1))
story.append(Paragraph("• ALWAYS add at end of treatment_summary_bn: 'বিস্তারিত মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২ৃ'", note))
story.append(Paragraph("• Do NOT invent specific chemical dosages — use APPROXIMATE ranges or general names only", note))
story.append(Paragraph("• Bangladesh-specific context is CRITICAL — mention BRRI/BARI/BARC if known", note))
story.append(Paragraph("• Cite real sources when possible — books, extension websites, research papers", note))
story.append(Spacer(1, 16))
story.append(Paragraph("HOW TO SUBMIT", h1))
story.append(Paragraph("1. Save each LLM output as a separate .json file", body))
story.append(Paragraph("2. File naming: [Crop]_Disease.json (e.g., WHEAT_BlackPoint.json)", body))
story.append(Paragraph("3. Place all files in a single folder", body))
story.append(Paragraph("4. Submit the folder — they will be merged into RAG index", body))
story.append(Paragraph("5. After merging: diseases become Category A (full info available for farmers)", body))

doc.build(story)
print(f"PDF generated: {OUT}")
