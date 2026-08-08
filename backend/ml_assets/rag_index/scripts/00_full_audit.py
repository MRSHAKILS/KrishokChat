"""Full audit: node quality + provenance tracking to parent MD files."""
import json
from pathlib import Path
from collections import Counter

raw_path = Path(__file__).resolve().parent.parent / "raw" / "knowledge_nodes.json"

with open(raw_path, "r", encoding="utf-8") as f:
    nodes = json.load(f)

total = len(nodes)
print(f"Total knowledge nodes: {total}")
print()

# Check provenance fields
has_source_md = 0
has_file_path = 0
has_extracted_from = 0
has_section_title = 0
has_source_document = 0
has_node_id = 0

# Content quality
bn_content_lengths = []
en_content_lengths = []
stub_count = 0  # < 150 chars
short_count = 0  # < 300 chars
good_count = 0  # > 500 chars

# Check which fields connect to parent MD
for n in nodes:
    if n.get("source_md"):
        has_source_md += 1
    if n.get("file_path"):
        has_file_path += 1
    if n.get("extracted_from"):
        has_extracted_from += 1
    if n.get("section_title"):
        has_section_title += 1
    if n.get("source_document"):
        has_source_document += 1
    if n.get("node_id"):
        has_node_id += 1

    bn = n.get("content_bn", "")
    en = n.get("content_en", "")
    bn_content_lengths.append(len(bn))
    en_content_lengths.append(len(en))

    if len(bn) < 150 and len(en) < 150:
        stub_count += 1
    elif len(bn) < 300 and len(en) < 300:
        short_count += 1
    else:
        good_count += 1

print("=" * 60)
print("PROVENANCE (connection to parent MD files)")
print("=" * 60)
print(f"has source_md:         {has_source_md:5d}  ({has_source_md/total*100:.1f}%)")
print(f"has file_path:         {has_file_path:5d}  ({has_file_path/total*100:.1f}%)")
print(f"has extracted_from:    {has_extracted_from:5d}  ({has_extracted_from/total*100:.1f}%)")
print(f"has section_title:     {has_section_title:5d}  ({has_section_title/total*100:.1f}%)")
print(f"has source_document:   {has_source_document:5d}  ({has_source_document/total*100:.1f}%)")
print(f"has node_id:           {has_node_id:5d}  ({has_node_id/total*100:.1f}%)")
print()

# Check what source_md looks like
print("SAMPLE source_md values:")
count = 0
for n in nodes:
    if n.get("source_md"):
        print(f"  {n['source_md'][:100]}")
        count += 1
        if count >= 5:
            break
print()

# Check what file_path looks like
print("SAMPLE file_path values:")
count = 0
for n in nodes:
    if n.get("file_path"):
        print(f"  {n['file_path'][:100]}")
        count += 1
        if count >= 5:
            break
print()

# Check extracted_from
print("SAMPLE extracted_from values:")
count = 0
for n in nodes:
    if n.get("extracted_from"):
        print(f"  {str(n['extracted_from'])[:100]}")
        count += 1
        if count >= 5:
            break
print()

print("=" * 60)
print("CONTENT QUALITY")
print("=" * 60)
print(f"Stub (<150 chars both):    {stub_count:5d}  ({stub_count/total*100:.1f}%)")
print(f"Short (<300 chars both):   {short_count:5d}  ({short_count/total*100:.1f}%)")
print(f"Good (>300 chars):         {good_count:5d}  ({good_count/total*100:.1f}%)")
print()
print(f"Avg bn content length: {sum(bn_content_lengths)/len(bn_content_lengths):.0f} chars")
print(f"Avg en content length: {sum(en_content_lengths)/len(en_content_lengths):.0f} chars")
print(f"Max bn content length: {max(bn_content_lengths)} chars")
print(f"Max en content length: {max(en_content_lengths)} chars")
print()

# Distribution
print("Content length distribution (max of bn/en per node):")
lengths = [max(len(n.get("content_bn", "")), len(n.get("content_en", ""))) for n in nodes]
buckets = {"0": 0, "1-100": 0, "100-300": 0, "300-500": 0, "500-1000": 0, "1000-2000": 0, "2000+": 0}
for l in lengths:
    if l == 0:
        buckets["0"] += 1
    elif l <= 100:
        buckets["1-100"] += 1
    elif l <= 300:
        buckets["100-300"] += 1
    elif l <= 500:
        buckets["300-500"] += 1
    elif l <= 1000:
        buckets["500-1000"] += 1
    elif l <= 2000:
        buckets["1000-2000"] += 1
    else:
        buckets["2000+"] += 1

for bucket, count in buckets.items():
    bar = "#" * (count // 5)
    print(f"  {bucket:>8}: {count:5d}  {bar}")
print()

# Category distribution
print("Category distribution:")
cat_counts = Counter(n.get("category", "NONE") for n in nodes)
for cat, count in cat_counts.most_common():
    print(f"  {cat:>20}: {count:5d}")
print()

# Publisher distribution
print("Publisher distribution:")
pub_counts = Counter(n.get("publisher", "NONE") for n in nodes)
for pub, count in pub_counts.most_common():
    print(f"  {pub:>25}: {count:5d}")
print()

# Sample a stub node
print("=" * 60)
print("SAMPLE STUB NODE (showing full raw data)")
print("=" * 60)
for n in nodes:
    bn = n.get("content_bn", "")
    en = n.get("content_en", "")
    if len(bn) < 100 and len(en) < 100 and (len(bn) > 0 or len(en) > 0):
        print(json.dumps(n, ensure_ascii=False, indent=2)[:1500])
        break
