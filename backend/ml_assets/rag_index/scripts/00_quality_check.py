"""Deep check Bengali content quality — is it real Bangla or just noise?"""
import json
import unicodedata
from pathlib import Path
from collections import Counter

nodes_path = Path(__file__).resolve().parent.parent / "processed" / "knowledge_nodes_clean.jsonl"

nodes = []
with open(nodes_path, "r", encoding="utf-8") as f:
    for line in f:
        nodes.append(json.loads(line))

BENGALI_RANGE = (0x0980, 0x09FF)


def count_bengali_chars(text):
    count = 0
    for ch in text:
        if BENGALI_RANGE[0] <= ord(ch) <= BENGALI_RANGE[1]:
            count += 1
    return count


def count_total_meaningful(text):
    """Count non-whitespace, non-punctuation chars."""
    count = 0
    for ch in text:
        if ch.isalpha():
            count += 1
    return count


def is_real_bengali(text, min_bengali_ratio=0.3):
    """Check if text has real Bengali content."""
    text = text.strip()
    if len(text) < 10:
        return False, 0, 0
    bn_chars = count_bengali_chars(text)
    total_chars = count_total_meaningful(text)
    if total_chars == 0:
        return False, 0, 0
    ratio = bn_chars / total_chars
    return ratio >= min_bengali_ratio, bn_chars, ratio


# Check each node
real_bn = 0
weak_bn = 0
no_bn = 0
total = len(nodes)

quality_issues = []
samples_real = []
samples_weak = []
samples_empty = []

for n in nodes:
    bn_text = n.get("content_bn", "").strip()
    title_bn = n.get("title_bn", "").strip()

    # Check content_bn
    is_real, bn_count, ratio = is_real_bengali(bn_text)

    # Also check title
    title_real, title_bn_count, title_ratio = is_real_bengali(title_bn)

    if is_real:
        real_bn += 1
        if len(samples_real) < 3:
            samples_real.append((n["id"], bn_text[:200], ratio))
    elif len(bn_text) > 0:
        weak_bn += 1
        if len(samples_weak) < 10:
            samples_weak.append((n["id"], bn_text[:200], bn_count, ratio))
    else:
        no_bn += 1
        if len(samples_empty) < 5:
            samples_empty.append(n["id"])

print("=" * 70)
print("BENGALI CONTENT QUALITY DEEP CHECK")
print("=" * 70)
print(f"Total nodes: {total}")
print()
print(f"Real Bengali content (>30% Bengali chars):  {real_bn:5d}  ({real_bn/total*100:.1f}%)")
print(f"Weak Bengali (has text but <30% Bangla):     {weak_bn:5d}  ({weak_bn/total*100:.1f}%)")
print(f"Empty content_bn:                             {no_bn:5d}  ({no_bn/total*100:.1f}%)")
print()

print("=" * 70)
print("SAMPLES: REAL BENGALI")
print("=" * 70)
for nid, text, ratio in samples_real:
    print(f"  [{nid}] ratio={ratio:.2f}")
    print(f"  {text}")
    print()

print("=" * 70)
print("SAMPLES: WEAK/QUESTIONABLE BENGALI")
print("=" * 70)
for nid, text, bn_count, ratio in samples_weak:
    print(f"  [{nid}] bn_chars={bn_count}, ratio={ratio:.2f}")
    print(f"  {text}")
    print()

print("=" * 70)
print("SAMPLES: EMPTY content_bn")
print("=" * 70)
for nid in samples_empty:
    print(f"  [{nid}]")
print()

# Check title_bn quality
print("=" * 70)
print("TITLE QUALITY")
print("=" * 70)
title_has_bn = sum(1 for n in nodes if count_bengali_chars(n.get("title_bn", "")) > 3)
title_no_bn = total - title_has_bn
print(f"title_bn has Bengali: {title_has_bn} ({title_has_bn/total*100:.1f}%)")
print(f"title_bn empty/latin: {title_no_bn} ({title_no_bn/total*100:.1f}%)")

# Check summary field
summary_has_bn = sum(1 for n in nodes if count_bengali_chars(n.get("summary", "")) > 3)
print(f"summary has Bengali:  {summary_has_bn} ({summary_has_bn/total*100:.1f}%)")

# Check natural_intro_bn
intro_has_bn = sum(1 for n in nodes if count_bengali_chars(n.get("natural_intro_bn", "")) > 3)
print(f"natural_intro_bn has Bengali: {intro_has_bn} ({intro_has_bn/total*100:.1f}%)")

# Distribution of Bengali character ratios
print()
print("=" * 70)
print("BENGALI RATIO DISTRIBUTION (content_bn)")
print("=" * 70)
buckets = {"0%": 0, "1-10%": 0, "10-30%": 0, "30-50%": 0, "50-70%": 0, "70-90%": 0, "90-100%": 0}
for n in nodes:
    bn_text = n.get("content_bn", "").strip()
    bn = count_bengali_chars(bn_text)
    total_alpha = count_total_meaningful(bn_text)
    if total_alpha == 0:
        buckets["0%"] += 1
    else:
        r = bn / total_alpha
        if r <= 0.01:
            buckets["0%"] += 1
        elif r <= 0.1:
            buckets["1-10%"] += 1
        elif r <= 0.3:
            buckets["10-30%"] += 1
        elif r <= 0.5:
            buckets["30-50%"] += 1
        elif r <= 0.7:
            buckets["50-70%"] += 1
        elif r <= 0.9:
            buckets["70-90%"] += 1
        else:
            buckets["90-100%"] += 1

for bucket, count in buckets.items():
    bar = "#" * (count // 10)
    print(f"  {bucket:>8}: {count:5d}  {bar}")
