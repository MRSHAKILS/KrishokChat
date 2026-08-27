"""KrishokChat main presentation for the Innovation Fair: 8 slides, 16:9.

Design system
  Page         warm near-white, never a dark full bleed
  Primary      deep teal green, used for type and hairline fills
  Accent       muted slate for labels, pale sage for panels
  Rhythm       one argument per slide, generous margins, real figures
  Sources      arXiv links cited where the claim is actually made

Content is aligned with KrishokChat_Application_Supporting_Doc.tex and covers
the nine evaluation criteria: originality, practical impact, commercialization,
technical capability, SDG contribution, innovative leadership, social
inclusion, ethics and safety, market demand.

python-pptx only. No em-dashes in any output string.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "KrishokChat_Innovation_Fair_Deck.pptx")

F_TEASER = os.path.join(HERE, "teaser_diagram.png")        # 1693x929
F_PROBLEM = os.path.join(FIG, "problem_vs_soluion.png")     # 1536x1024
F_PIPELINE = os.path.join(FIG, "core_pipeline.png")          # 1672x941
F_SAFETY = os.path.join(FIG, "safety_g.png")                # 1536x1024
F_MARKET = os.path.join(FIG, "market opportunity.png")       # 1672x941
F_SDG = os.path.join(FIG, "sgd.png")                         # 1672x941

DIM = {
    F_TEASER: (1693, 929),
    F_PROBLEM: (1536, 1024),
    F_PIPELINE: (1672, 941),
    F_SAFETY: (1536, 1024),
    F_MARKET: (1672, 941),
    F_SDG: (1672, 941),
}

PRIMARY = RGBColor(0x1D, 0x4E, 0x44)
PRIMARY_L = RGBColor(0x2E, 0x6B, 0x5E)
SLATE = RGBColor(0x46, 0x64, 0x73)
BG = RGBColor(0xFA, 0xFA, 0xF8)
PANEL = RGBColor(0xF0, 0xF4, 0xF2)
INK = RGBColor(0x1B, 0x2A, 0x26)
MUTED = RGBColor(0x6B, 0x73, 0x6E)
HAIR = RGBColor(0xD6, 0xDC, 0xD8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Segoe UI"
FONT_SB = "Segoe UI Semibold"
FONT_L = "Segoe UI Light"

TOTAL = 9

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def rect(slide, x, y, w, h, fill, border=None, bw=1.0, rounded=False):
    t = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(t, x, y, w, h)
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if border is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = border
        s.line.width = Pt(bw)
    s.shadow.inherit = False
    if rounded:
        try:
            s.adjustments[0] = 0.04
        except Exception:
            pass
    return s


def txt(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space_after=5, ls=1.14):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)
        p.line_spacing = ls
        for (t, sz, b, col, fn) in para:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(sz)
            r.font.bold = b
            r.font.color.rgb = col
            r.font.name = fn
    return tb


def one(t, sz=14, col=INK, b=False, fn=FONT):
    return [(t, sz, b, col, fn)]


def page(slide, kicker, title, n, sub=None):
    rect(slide, 0, 0, SW, SH, BG)
    rect(slide, 0, 0, Pt(4.5), SH, PRIMARY)
    txt(slide, Inches(0.72), Inches(0.42), Inches(11.5), Inches(0.3),
        [[(kicker.upper(), 11.5, True, SLATE, FONT_SB)]])
    txt(slide, Inches(0.72), Inches(0.72), Inches(12), Inches(0.62),
        [[(title, 26, True, PRIMARY, FONT_SB)]])
    y_rule = Inches(1.36)
    if sub:
        txt(slide, Inches(0.74), Inches(1.32), Inches(11.6), Inches(0.34),
            [[(sub, 13, False, MUTED, FONT)]], ls=1.1)
        y_rule = Inches(1.72)
    rect(slide, Inches(0.74), y_rule, Inches(11.85), Pt(1.1), HAIR)
    txt(slide, Inches(0.72), SH - Inches(0.46), Inches(6), Inches(0.26),
        [[("KrishokChat", 10, True, PRIMARY, FONT_SB),
          ("    Innovation Fair Bangladesh", 10, False, MUTED, FONT)]])
    txt(slide, SW - Inches(1.2), SH - Inches(0.46), Inches(0.7), Inches(0.26),
        [[("%d / %d" % (n, TOTAL), 10, False, MUTED, FONT)]],
        align=PP_ALIGN.RIGHT)
    return y_rule


def figure(slide, path, x, y, max_w, max_h, framed=True):
    if not os.path.exists(path):
        return None, None
    iw, ih = DIM[path]
    w = max_w
    h = Emu(int(w) * ih // iw)
    if int(h) > int(max_h):
        h = max_h
        w = Emu(int(h) * iw // ih)
    if framed:
        rect(slide, x - Pt(0.75), y - Pt(0.75), w + Pt(1.5), h + Pt(1.5),
             None, border=HAIR, bw=0.75)
    slide.shapes.add_picture(path, x, y, width=w, height=h)
    return w, h


def caption(slide, x, y, w, text):
    txt(slide, x, y, w, Inches(0.4), [[(text, 10.5, False, MUTED, FONT)]],
        ls=1.12)


def blocklist(slide, x, y, w, items, title_sz=14, body_sz=12.3, gap=1.18,
              tick=True, body_h=0.86):
    py = y
    for t, d in items:
        if tick:
            rect(slide, x, py + Inches(0.05), Pt(3), Inches(0.21), PRIMARY_L)
            tx = x + Inches(0.22)
            tw = w - Inches(0.25)
        else:
            tx, tw = x, w
        txt(slide, tx, py, tw, Inches(0.3),
            [[(t, title_sz, True, PRIMARY, FONT_SB)]])
        txt(slide, tx, py + Inches(0.29), tw, Inches(body_h),
            [[(d, body_sz, False, INK, FONT)]], ls=1.2)
        py = Emu(int(py) + int(Inches(gap)))
    return py


def statstrip(slide, x, y, w, items):
    n = len(items)
    cw = Emu(int(w) // n)
    for i, (val, lab) in enumerate(items):
        cx = Emu(int(x) + i * int(cw))
        txt(slide, cx, y, cw - Inches(0.18), Inches(0.4),
            [[(val, 20, True, PRIMARY, FONT_SB)]])
        txt(slide, cx, y + Inches(0.36), cw - Inches(0.18), Inches(0.5),
            [[(lab, 10.5, False, MUTED, FONT)]], ls=1.06)
        if i < n - 1:
            rect(slide, Emu(int(cx) + int(cw) - int(Inches(0.14))),
                 y + Inches(0.03), Pt(0.9), Inches(0.66), HAIR)


# =====================================================================
# 1  TITLE
# =====================================================================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, SH, BG)
rect(s, 0, 0, Pt(6), SH, PRIMARY)
rect(s, Inches(7.5), 0, SW - Inches(7.5), SH, PANEL)

txt(s, Inches(0.85), Inches(1.2), Inches(6.2), Inches(0.3),
    [[("AGRICULTURAL ADVISORY SYSTEM FOR BANGLADESH", 12, True, SLATE, FONT_SB)]])
txt(s, Inches(0.82), Inches(1.64), Inches(6.6), Inches(1.1),
    [[("KrishokChat", 54, True, PRIMARY, FONT_SB)]])
rect(s, Inches(0.86), Inches(2.76), Inches(1.9), Pt(2), PRIMARY)
txt(s, Inches(0.86), Inches(3.02), Inches(6.0), Inches(1.5),
    [[("A Bengali-first crop advisory that answers from Bangladeshi "
       "government sources, verifies every chemical dose before a farmer sees "
       "it, and runs on the phone already in his pocket.",
       17, False, INK, FONT_L)]], ls=1.26)

for i, c in enumerate(["Working system, tested baseline",
                       "Grounded in official sources",
                       "Built for low connectivity"]):
    y = Inches(4.82) + Emu(i * int(Inches(0.5)))
    rect(s, Inches(0.86), y + Inches(0.11), Pt(3), Inches(0.19), PRIMARY_L)
    txt(s, Inches(1.12), y, Inches(5.5), Inches(0.38),
        [[(c, 14, True, PRIMARY, FONT_SB)]], anchor=MSO_ANCHOR.MIDDLE)

txt(s, Inches(0.86), Inches(6.5), Inches(6.2), Inches(0.5),
    [[("Research foundation: arxiv.org/abs/2606.29243  and  "
       "arxiv.org/abs/2608.14886", 10.5, False, MUTED, FONT)]], ls=1.1)

txt(s, Inches(8.1), Inches(1.5), Inches(4.4), Inches(0.32),
    [[("THE SITUATION", 11.5, True, SLATE, FONT_SB)]])
txt(s, Inches(8.1), Inches(1.94), Inches(4.5), Inches(3.7),
    [one("A farmer finds dark spots spreading on his brinjal leaves a week "
         "before harvest. He needs to know what it is, what to spray, how "
         "much, and whether it is safe.", 14.5, INK),
     one("", 7),
     one("His options today are a dealer who profits from the sale, a Facebook "
         "group where strangers guess, or a general chatbot that never learned "
         "Bangladeshi crops or official guidance.", 14.5, INK),
     one("", 7),
     one("For a smallholder, a confidently wrong answer is a lost harvest or "
         "an unsafe chemical sprayed on food and water.", 14.5, PRIMARY, True)],
    ls=1.3)
rect(s, Inches(8.12), Inches(5.82), Inches(4.4), Pt(1), HAIR)
txt(s, Inches(8.1), Inches(6.0), Inches(4.5), Inches(0.8),
    [[("About 16 million farm households make these decisions with no expert "
       "in reach.", 13, True, PRIMARY, FONT_SB)]], ls=1.2)

# =====================================================================
# 2  THE GAP AND THE RESPONSE
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "The problem", "Farmers do not lack questions, they lack a trustworthy answer", 2)

figure(s, F_PROBLEM, Inches(0.75), Inches(1.62), Inches(6.9), Inches(4.5))
caption(s, Inches(0.75), Inches(6.28), Inches(6.9),
        "Where advice breaks down today, and what replaces it.")

rx, rw = Inches(8.05), Inches(4.55)
txt(s, rx, Inches(1.62), rw, Inches(0.32),
    [[("WHAT WE BUILT IT AROUND", 11.5, True, SLATE, FONT_SB)]])
txt(s, rx, Inches(2.04), rw, Inches(1.5),
    [one("KrishokChat began from field conversations and the questions farmers "
         "actually ask: what disease is this, what treatment fits, how much to "
         "apply, whether a chemical is even allowed in Bangladesh, and why a "
         "crop is failing to grow.", 14, INK)], ls=1.26)

blocklist(s, rx, Inches(3.62), rw, [
    ("Asked the way farmers speak",
     "Bengali or Banglish, by text, voice, or a photo of the leaf, with dialect "
     "handled rather than corrected."),
    ("Answered from named sources",
     "Guidance is tied to Bangladeshi institutional documents, so the farmer is "
     "reading official practice rather than a model's general memory."),
    ("Refused honestly when it should be",
     "Outside its coverage the system says so and points to the national Krishi "
     "Call Center on 16123."),
], gap=1.1, body_h=0.8)

# =====================================================================
# 3  SYSTEM AT A GLANCE  (teaser)
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "The system at a glance", "One assistant, many inputs, the server optional", 3,
     sub="A farmer's chat, a crop photo, soil and irrigation sensors, and a field drone all feed the same on-device assistant.")

w, h = figure(s, F_TEASER, Inches(0.9), Inches(1.95), Inches(9.3), Inches(4.35))

rx, rw = Inches(10.5), Inches(2.12)
rect(s, rx, Inches(1.95), rw, Inches(4.35), PANEL, border=HAIR, bw=0.9)
txt(s, rx + Inches(0.2), Inches(2.12), rw - Inches(0.36), Inches(0.4),
    [[("Four steps, every time", 13.5, True, PRIMARY, FONT_SB)]], ls=1.1)
steps = [
    ("1", "Safety", "banned and unsafe requests stop here"),
    ("2", "Retrieval", "BM25 over curated official sources"),
    ("3", "Answer", "composed from retrieved evidence"),
    ("4", "Verifier", "each dose checked against its source"),
]
sy = Inches(2.68)
for num, t, d in steps:
    txt(s, rx + Inches(0.2), sy, rw - Inches(0.36), Inches(0.3),
        [[(num + "   ", 13, True, SLATE, FONT_SB),
          (t, 13, True, PRIMARY, FONT_SB)]])
    txt(s, rx + Inches(0.2), sy + Inches(0.26), rw - Inches(0.36), Inches(0.62),
        [[(d, 10.5, False, MUTED, FONT)]], ls=1.12)
    sy = Emu(int(sy) + int(Inches(0.9)))

caption(s, Inches(0.9), Inches(6.42), Inches(9.3),
        "The heavy language model is one step of four. Knowledge, safety rules, "
        "and vision models stay separate from it, which is what makes an "
        "on-device path realistic.")

# =====================================================================
# 4  ORIGINALITY AND RESEARCH FOUNDATION
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "Originality and research foundation", "The contribution is the architecture, not the model choice", 4)

lx, lw = Inches(0.75), Inches(5.85)
txt(s, lx, Inches(1.62), lw, Inches(0.32),
    [[("WHAT IS GENUINELY NEW", 11.5, True, SLATE, FONT_SB)]])
blocklist(s, lx, Inches(2.04), lw, [
    ("Answers are composed, not improvised",
     "High risk questions such as a registered dose resolve from a structured, "
     "source cited knowledge base. The same question returns the same cited "
     "answer every time, which a generative model cannot promise."),
    ("The language model has bounded authority",
     "It phrases and disambiguates. It is never trusted to invent a dose, and "
     "it is bypassed entirely when a cited table can already answer."),
    ("Provenance is structural",
     "Citations are attached by construction rather than requested from the "
     "model, so a fabricated reference is not a failure mode that can occur."),
    ("Dialect and intent are first class",
     "A farmer's vague, dialect heavy question is classified into intent and "
     "converted into a structured request before anything is retrieved."),
], gap=1.14, body_h=0.85)

rx, rw = Inches(7.15), Inches(5.45)
rect(s, rx, Inches(1.62), rw, Inches(2.55), PANEL, border=HAIR, bw=0.9)
txt(s, rx + Inches(0.32), Inches(1.85), rw - Inches(0.64), Inches(0.35),
    [[("PUBLISHED FOUNDATION", 11.5, True, SLATE, FONT_SB)]])
txt(s, rx + Inches(0.32), Inches(2.24), rw - Inches(0.64), Inches(1.75),
    [[("The benchmark and safety critical advisory dataset behind the "
       "assistant: ", 13, False, INK, FONT),
      ("arxiv.org/abs/2606.29243", 13, True, PRIMARY, FONT_SB)],
     [("", 6, False, INK, FONT)],
     [("The provenance traceable retrieval architecture the answers are "
       "grounded in: ", 13, False, INK, FONT),
      ("arxiv.org/abs/2608.14886", 13, True, PRIMARY, FONT_SB)],
     [("", 6, False, INK, FONT)],
     [("A third paper covers the system and its evaluation, with further work "
       "in progress.", 12.5, False, MUTED, FONT)]], ls=1.24)

rect(s, rx, Inches(4.4), rw, Inches(1.9), None, border=HAIR, bw=0.9)
txt(s, rx + Inches(0.32), Inches(4.6), rw - Inches(0.64), Inches(0.35),
    [[("WHY THIS IS NOT AN API WRAPPER", 11.5, True, SLATE, FONT_SB)]])
txt(s, rx + Inches(0.32), Inches(4.98), rw - Inches(0.64), Inches(1.2),
    [[("A quantised Gemma model is served locally through llama.cpp, the "
       "retrieval index and dose references are built offline into versioned "
       "artifacts, and the safety registry is domain specific to Bangladesh. "
       "Nothing critical to a farmer's answer depends on a rented frontier "
       "API.", 12.5, False, INK, FONT)]], ls=1.22)

# =====================================================================
# 5  TECHNICAL CAPABILITY AND MATURITY
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "Technical capability and maturity", "A working prototype, running end to end today", 5)

figure(s, F_PIPELINE, Inches(0.75), Inches(1.62), Inches(7.4), Inches(4.2))
caption(s, Inches(0.75), Inches(5.95), Inches(7.4),
        "The core pipeline, with vision, field intelligence, and the sensor and "
        "drone layer feeding the same advisory surface.")

rx, rw = Inches(8.5), Inches(4.1)
txt(s, rx, Inches(1.62), rw, Inches(0.32),
    [[("WHAT ALREADY WORKS", 11.5, True, SLATE, FONT_SB)]])
blocklist(s, rx, Inches(2.02), rw, [
    ("Photo to grounded guidance",
     "The crop is recognised first, then routed to a crop specific disease "
     "model, then matched to treatment guidance from government manuals in one "
     "screen."),
    ("Retrieval over curated knowledge",
     "BM25 over 2,135 source traced nodes, with hybrid dense retrieval "
     "available, so each answer traces to a real passage."),
    ("More than a chat surface",
     "Soil and irrigation image analysis, sensor based insect prediction, and a "
     "drone field view all report into the same assistant."),
    ("Engineered to stay correct",
     "A fixed regression baseline and a replay set guard every change, which is "
     "what separates a maintainable pilot from a fragile demo."),
], tick=False, title_sz=13.5, body_sz=11.8, gap=1.08, body_h=0.82)

rect(s, Inches(0.75), Inches(6.35), Inches(11.85), Pt(1), HAIR)
statstrip(s, Inches(0.75), Inches(6.5), Inches(11.85), [
    ("410 / 0", "automated tests passing and failing"),
    ("50 / 50", "fixed scenarios reproduced exactly"),
    ("2,135", "source traced knowledge nodes"),
    ("20,112", "safety records, 12 risk categories"),
    ("6", "Bengali dialects, 110 word map"),
])

# =====================================================================
# 6  ETHICS AND SAFETY
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "Ethics and safety", "Refusing well is a feature, not a limitation", 6)

figure(s, F_SAFETY, Inches(0.75), Inches(1.62), Inches(6.85), Inches(4.55))
caption(s, Inches(0.75), Inches(6.3), Inches(6.85),
        "What is blocked before retrieval, and how a numeric claim is verified "
        "before release.")

rx, rw = Inches(8.0), Inches(4.6)
txt(s, rx, Inches(1.62), rw, Inches(0.32),
    [[("WHY IT IS SAFE TO DEPLOY", 11.5, True, SLATE, FONT_SB)]])
blocklist(s, rx, Inches(2.02), rw, [
    ("Safety runs before retrieval",
     "Restricted and banned agrochemical requests are caught against a "
     "Bangladesh specific registry before any answer is formed."),
    ("Every dose is checked against its source",
     "Numeric claims are normalised across Bengali and English numerals, then "
     "matched to the retrieved passage before the farmer sees them."),
    ("A calm response to crisis framing",
     "Anything reading as poisoning or self harm risk receives a supportive "
     "redirect to 16123 and in person medical help, never a normal answer."),
    ("Auditable rather than asserted",
     "Every request, classification, and verification result is written to a "
     "local audit record, kept on the device and never sent to a third party."),
], gap=1.13, body_h=0.84)

rect(s, rx, Inches(6.5), rw, Pt(1), HAIR)
txt(s, rx, Inches(6.66), rw, Inches(0.4),
    [[("Safer chemical use protects the farmer applying it, the family eating "
       "the crop, and the water downstream.", 11.5, False, MUTED, FONT)]],
    ls=1.14)

# =====================================================================
# 7  MARKET DEMAND AND COMMERCIALIZATION
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "Market demand and commercialization", "A route to revenue that does not price out the farmer", 7)

figure(s, F_MARKET, Inches(0.75), Inches(1.62), Inches(7.15), Inches(4.35))
caption(s, Inches(0.75), Inches(6.1), Inches(7.15),
        "Demand indicators and the three revenue paths, each tied to evidence "
        "rather than projection.")

rx, rw = Inches(8.25), Inches(4.35)
txt(s, rx, Inches(1.62), rw, Inches(0.32),
    [[("WHY ADOPTION IS FEASIBLE", 11.5, True, SLATE, FONT_SB)]])
blocklist(s, rx, Inches(2.02), rw, [
    ("The demand is already measurable",
     "The national helpline absorbs roughly 92,094 calls a year. Those are "
     "farmers actively seeking advice they cannot otherwise reach."),
    ("Unit economics allow a free tier",
     "Because common questions resolve from cited tables instead of a paid "
     "model call, serving cost per farmer stays low enough for the core "
     "advisory to remain free."),
    ("Institutions are the paying side",
     "Dealers, cooperatives, input companies, insurers, and extension programs "
     "need multi farmer dashboards, branded advisory channels, and licensed "
     "data, and each of those is a product rather than a promise."),
    ("The audit trail is commercially useful",
     "Any partner who must demonstrate responsible advice can point to a "
     "verifiable record, which a general chatbot cannot provide."),
], tick=False, title_sz=13.5, body_sz=11.8, gap=1.12, body_h=0.86)

# =====================================================================
# 8  INCLUSION AND LEADERSHIP
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "Social inclusion and leadership", "Reaching the farmers usually left out", 8)

lx, lw = Inches(0.75), Inches(5.75)
txt(s, lx, Inches(1.62), lw, Inches(0.32),
    [[("SOCIAL INCLUSION", 11.5, True, SLATE, FONT_SB)]])
blocklist(s, lx, Inches(2.04), lw, [
    ("Literacy is not a barrier to entry",
     "Voice input and Banglish handling mean a farmer who cannot type formal "
     "Bengali still receives the same quality of guidance as anyone else."),
    ("Women managing homestead plots",
     "Advice arrives privately on a household phone, without needing a trip to "
     "a dealer or a male intermediary to ask on her behalf."),
    ("Young and first generation farmers",
     "Free access and plain language lower the cost of learning good practice, "
     "which is exactly where new entrants are most exposed to bad advice."),
    ("Low connectivity is designed for",
     "Keeping knowledge and safety rules separate from the heavy model is what "
     "lets the critical answers work where the network does not."),
], gap=1.18, body_h=0.88)

rx, rw = Inches(7.05), Inches(5.55)
txt(s, rx, Inches(1.62), rw, Inches(0.32),
    [[("INNOVATIVE LEADERSHIP", 11.5, True, SLATE, FONT_SB)]])
txt(s, rx, Inches(2.04), rw, Inches(2.0),
    [one("The work is led as research and as engineering at once. Three papers "
         "document the dataset, the safety critical advisory design, and the "
         "provenance traceable retrieval architecture, while the system itself "
         "is held to a fixed regression baseline with a documented roadmap "
         "executed one reviewed change at a time.", 13.5, INK),
     one("", 7),
     one("Field conversations with farmers set the requirements, and the "
         "refusal behaviour was designed with the national helpline as the "
         "escalation path rather than as a competitor.", 13.5, INK)], ls=1.28)

rect(s, rx, Inches(4.35), rw, Pt(1), HAIR)
txt(s, rx, Inches(4.55), rw, Inches(0.32),
    [[("WHERE WE ARE", 11.5, True, SLATE, FONT_SB)]])
txt(s, rx, Inches(4.94), rw, Inches(1.6),
    [one("A working, tested system today, with the fully offline path, wider "
         "crop coverage, and weather driven alerting landing before the fair. "
         "Not a demonstration looking for a problem, but a working answer to "
         "one that farmers face every season.", 13.5, PRIMARY, True)], ls=1.3)

# =====================================================================
# 9  SUSTAINABLE DEVELOPMENT CONTRIBUTION
# =====================================================================
s = prs.slides.add_slide(BLANK)
page(s, "Sustainable development contribution", "Five goals the system moves in practice, not in principle", 9)

figure(s, F_SDG, Inches(0.85), Inches(1.66), Inches(11.6), Inches(2.6))

rect(s, Inches(0.75), Inches(4.42), Inches(11.85), Pt(1), HAIR)
txt(s, Inches(0.75), Inches(4.6), Inches(11.85), Inches(0.32),
    [[("HOW EACH ONE IS ACTUALLY MOVED", 11.5, True, SLATE, FONT_SB)]])

sdg_cols = [
    ("Goal 2 and Goal 3", [
        "Yield protected by catching disease early instead of after a field is lost.",
        "Chemical exposure reduced by blocking banned actives and verifying every dose before it reaches the farmer.",
    ]),
    ("Goal 9 and Goal 10", [
        "Resilient agri infrastructure built on curated national knowledge and a locally served model rather than rented capacity.",
        "Advisory delivered in Bengali, Banglish, and voice, so access does not depend on literacy or income.",
    ]),
    ("Goal 17", [
        "Designed to escalate into the national Krishi Call Center on 16123 rather than compete with it.",
        "Dataset, benchmarks, and architecture published openly so government, research, and industry can build on the same base.",
    ]),
]
cx, cw, gap = Inches(0.78), Inches(3.83), Inches(0.2)
for title, lines in sdg_cols:
    rect(s, cx, Inches(5.02), cw, Inches(1.62), PANEL, border=HAIR, bw=0.9)
    rect(s, cx, Inches(5.02), Pt(3), Inches(1.62), PRIMARY_L)
    txt(s, cx + Inches(0.24), Inches(5.16), cw - Inches(0.46), Inches(0.3),
        [[(title, 13, True, PRIMARY, FONT_SB)]])
    paras = [[("\u203A  ", 11.5, True, SLATE, FONT_SB),
              (t, 11.3, False, INK, FONT)] for t in lines]
    txt(s, cx + Inches(0.24), Inches(5.5), cw - Inches(0.46), Inches(1.05),
        paras, ls=1.16, space_after=6)
    cx = Emu(int(cx) + int(cw) + int(gap))

txt(s, Inches(0.75), Inches(6.82), Inches(11.85), Inches(0.34),
    [[("Each claim above maps to a mechanism already in the system rather than "
       "an intention, which is the difference between contributing to these "
       "goals and citing them.", 11.5, False, MUTED, FONT)]], ls=1.14)


prs.save(OUT)
print("Saved:", OUT)
print("Slides:", len(prs.slides._sldIdLst))