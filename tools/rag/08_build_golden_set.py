"""08 — Build the P4 golden benchmark set (golden_qa_v1).

Stratified sample from the 1,000 real farmer queries (fb_group_real_farmer):
  - dosage (ডোজ/পরিমাণ), timing (কখন/কতদিন), pest_disease (রোগ/পোকা/লক্ষণ),
    general (answerable agronomy: spacing, soil, water, spray practice),
    off_topic (unrelated), unanswerable (agri-related but outside the corpus:
    prices, weather, local availability, subsidies, contact info) —
    >= 10 unanswerables per roadmap P4.

Category assignment is heuristic first, then human-reviewed: the script emits
a review dump; REVIEW_OVERRIDES below hold every correction from that review
(with the reason). The scoring sheet (10_scoring_sheet) also asks both
evaluators to CONFIRM the category per item, and disagreements are logged.

Every row keeps its original row_id so runs and scores trace back to the
published farmer-query dataset.
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC = BACKEND_ROOT / "ml_assets" / "rag_index" / "eval" / "farmer_benchmark_1000.jsonl"
OUT_DIR = BACKEND_ROOT.parent / "dataset_release" / "benchmark"
GOLDEN = OUT_DIR / "golden_qa_v1.jsonl"
REVIEW_DUMP = OUT_DIR / "golden_review_dump_v1.md"

# Category targets: 46 items, >= 10 unanswerable (roadmap P4). off_topic is
# capped by the honest pool size: of 1,000 real farmer queries only 2 are
# genuinely unrelated to agriculture (export rules, DAE institutional role).
TARGETS = {"dosage": 10, "timing": 10, "pest_disease": 9, "general": 3, "off_topic": 2, "unanswerable": 12}
SEED = 7

# NOTE on precision: Bengali text has no word boundaries, so naive patterns
# false-positive on substrings ("গান" in "লাগানো", "ভর্তি" in "ধান ভর্তি",
# "কবে" in "থাকবে"). Patterns below are phrased to avoid those traps; the
# human review dump is the authoritative second pass.
DOSAGE_RE = re.compile(r"(কত\s*(মিলি|গ্রাম|কেজি|লিটার|কিলো)|ডোজ|(?:^|\s)মাত্রা|কতটুকু|কত\s*পরিমাণ|কত\s*(ইউরিয়া|ডিএপি|টিএসপি|এমওপি|জিপি)|মিলি\s*(প্রতি|জল)|প্রতি\s*(লিটার|শতাংশ))")
TIMING_RE = re.compile(r"(কখন|(?:^|\s)কবে(?=\s|$)|কোন\s*(সময়|ঋতু|মৌসুম)|সকালে|বিকালে|কত\s*দিন|কতদিন|দিন\s*পর|মাসে|সপ্তাহে|মৌসুমে|শীতকালে|বর্ষায়|গ্রীষ্মে|কোন\s*বয়সে|বয়সে|জীবনকাল)")
PEST_RE = re.compile(r"(রোগ|পোকা|কীট|লক্ষণ|দাগ|পচা|হলুদ|শুকিয়ে|মরছে|মরার|মরে|ছত্রাক|ব্যাকটেরিয়া|ভাইরাস|জাব|মাজরা|থ্রিপস|পিঁপড়া|শামুক|হোয়াইট|ব্লাস্ট|লিফ\s*রোলার|ঝরে|ফুল\s*ধরে)")
UNANSWERABLE_RE = re.compile(r"(বাজার\s*দর|বাজারদর|দাম\s*কত|কত\s*দাম|আবহাওয়া|বৃষ্টির\s*পূর্বাভাস|কোথায়\s*পাব|কোথায়\s*কিনব|কোথায়\s*পাওয়া|কোথায়\s*পেলাম|সাবসিডি|ভর্তুকি|ঋণ|লোন|টাকার\s*লোন|সরকারি\s*সুবিধা|প্রণোদনা|ক্ষতিপূরণ|ইনস্যুরেন্স|বীমা|অফিসের\s*ফোন|মোবাইল\s*নম্বর|ফোন\s*নং|ঠিকানা|বিয়ে|ভাড়া|জমি\s*বিক্রি|জমি\s*লিজ|ট্রেনিং|প্রশিক্ষণ|যোগাযোগের\s*ঠিকানা|রপ্তানি)")
OFF_TOPIC_RE = re.compile(r"(চাকরি|(?:^|\s)ভর্তি(?=\s|$)|(?:^|\s)গান(?=\s|$)|স্কুল|কলেজ|হাসপাতাল|মেডিকেল|আদালত|মামলা|রাজনীতি|ফুটবল|ক্রিকেট|মোবাইল\s*ফোন|সিম\s*কার্ড|ইন্টারনেট|সংগীত|সিনেমা|খেলাধুলা)")


def categorize(question: str) -> str:
    q = question.lower()
    if DOSAGE_RE.search(q):
        return "dosage"
    if TIMING_RE.search(q):
        return "timing"
    if PEST_RE.search(q):
        return "pest_disease"
    if OFF_TOPIC_RE.search(q):
        return "off_topic"
    if UNANSWERABLE_RE.search(q):
        return "unanswerable"
    return "general"  # fallback bucket; reviewed in the dump


# Human-reviewed corrections (row_id -> category). Every entry below was
# decided by reading the question + gold answer in the review dump.
REVIEW_OVERRIDES: dict[str, str] = {
    # "পর্যাপ্ত পরিমাণ" substring false-positive; it is a storage-pest question.
    "farmer_q_25": "pest_disease",
    # "লাগানোর" contains "গান" (off-topic false positive); damping-off disease.
    "farmer_q_435": "pest_disease",
    # Plant-spacing question — answerable agronomy, not pest.
    "farmer_q_787": "general",
    # Late TSP application method — answerable agronomy.
    "farmer_q_841": "general",
    # Asks for an exporter's phone number — outside corpus.
    "farmer_q_982": "unanswerable",
    # Local seedling availability in Cumilla — outside corpus.
    "farmer_q_993": "unanswerable",
    # Quail/mushroom + local training info — livestock, outside corpus.
    "farmer_q_721": "unanswerable",
    # Water requirement question — answerable agronomy, not pest.
    "farmer_q_487": "general",
    # Soil fertility question — answerable agronomy.
    "farmer_q_438": "general",
    # Flowering/fruit-set problem in March — symptom problem.
    "farmer_q_655": "pest_disease",
    # Flooding damage recovery — answerable agronomy.
    "farmer_q_854": "general",
    # Salinity diagnosis — the corpus covers coastal salinity, answerable.
    "farmer_q_580": "general",
    # Spray-mix compatibility — answerable agronomy, not dosage.
    "farmer_q_81": "general",
    # Institutional role of DAE — not crop advisory, off-topic.
    "farmer_q_718": "off_topic",
    # Litchi export rules — not crop advisory, off-topic.
    "farmer_q_851": "off_topic",
    # Variety recommendation (heat-tolerant chili) — "তাপমাত্রা" contains the
    # dosage word "মাত্রা"; the question asks for a variety name, not a dose.
    "farmer_q_0": "general",
    "farmer_q_91": "general",
    # Cauliflower not growing — a symptom problem, not a general agronomy ask.
    "farmer_q_471": "pest_disease",
    # Long intro; the actual ask is training + government land subsidy.
    "farmer_q_690": "unanswerable",
    # Cucumber fruit-drop ("ঝইরা" is dialect for "ঝরে") — symptom problem.
    "farmer_q_624": "pest_disease",
    # Tomato flower-drop (dialect "ঝইরা") — symptom problem, not agronomy.
    "farmer_q_629": "pest_disease",
}

# The final reviewed sample, pinned after 3 review passes (2026-08-14).
# Rebuilds use this list verbatim — overrides may re-tag rows, they never
# re-sample, so the golden set stays stable and reproducible.
PINNED_SAMPLE = [
    "farmer_q_12", "farmer_q_197", "farmer_q_222", "farmer_q_290", "farmer_q_317",
    "farmer_q_360", "farmer_q_379", "farmer_q_625", "farmer_q_75", "farmer_q_867",
    "farmer_q_45", "farmer_q_469", "farmer_q_629",
    "farmer_q_718", "farmer_q_851",
    "farmer_q_105", "farmer_q_106", "farmer_q_156", "farmer_q_242", "farmer_q_648",
    "farmer_q_667", "farmer_q_678", "farmer_q_751", "farmer_q_752",
    "farmer_q_127", "farmer_q_29", "farmer_q_38", "farmer_q_389", "farmer_q_43",
    "farmer_q_455", "farmer_q_676", "farmer_q_824", "farmer_q_825", "farmer_q_97",
    "farmer_q_684", "farmer_q_690", "farmer_q_693", "farmer_q_721", "farmer_q_806",
    "farmer_q_850", "farmer_q_852", "farmer_q_895", "farmer_q_967", "farmer_q_969",
    "farmer_q_970", "farmer_q_993",
]


def main() -> None:
    rows = [json.loads(line) for line in SRC.open(encoding="utf-8") if line.strip()]
    print(f"source rows: {len(rows)}")

    # Human-reviewed corrections (row_id -> category). Filled after inspecting
    # golden_review_dump_v1.md; kept here so rebuilds are reproducible.
    overrides = REVIEW_OVERRIDES

    pools: dict[str, list[dict]] = {cat: [] for cat in TARGETS}
    for row in rows:
        cat = overrides.get(row["row_id"], categorize(row["question"]))
        if cat in pools:
            pools[cat].append(row)

    rng = random.Random(SEED)
    if PINNED_SAMPLE:
        by_id = {row["row_id"]: row for row in rows}
        missing = [rid for rid in PINNED_SAMPLE if rid not in by_id]
        if missing:
            raise SystemExit(f"pinned sample references missing row_ids: {missing}")
        chosen = [by_id[rid] for rid in PINNED_SAMPLE]
        for row in chosen:
            row["golden_category"] = overrides.get(row["row_id"], categorize(row["question"]))
    else:
        chosen = []
        for cat, target in TARGETS.items():
            pool = pools[cat]
            if len(pool) < target:
                raise SystemExit(f"not enough {cat} candidates: {len(pool)} < {target}")
            for row in rng.sample(pool, target):
                chosen.append({**row, "golden_category": cat})

    chosen.sort(key=lambda r: (r["golden_category"], r["row_id"]))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with GOLDEN.open("w", encoding="utf-8") as handle:
        for row in chosen:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {GOLDEN} ({len(chosen)} rows)")

    with REVIEW_DUMP.open("w", encoding="utf-8") as handle:
        handle.write("# Golden set review dump — verify categories\n\n")
        for row in chosen:
            handle.write(f"## {row['row_id']} — {row['golden_category']}\n\n")
            handle.write(f"**Question:** {row['question']}\n\n")
            handle.write(f"**Gold answer:** {row['gold_answer'][:400]}\n\n")
            handle.write("---\n\n")
    print(f"review dump: {REVIEW_DUMP}")

    from collections import Counter
    print("categories:", dict(Counter(r["golden_category"] for r in chosen)))


if __name__ == "__main__":
    main()