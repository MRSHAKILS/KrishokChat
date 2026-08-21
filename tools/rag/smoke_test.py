"""Smoke test: refine ONE node with Gemini."""
import json
import sys
from pathlib import Path

import httpx

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
NODES_PATH = RAG_ROOT / "processed" / "knowledge_nodes_clean.jsonl"
SOURCE_MD_DIR = RAG_ROOT / "source_md"

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"

# Use first key
API_KEY = "AIzaSyBhHqS8SAk0d-Y5GuBHO9kJPCrBo8HlgCI"


def load_first_node():
    with open(NODES_PATH, "r", encoding="utf-8") as f:
        return json.loads(f.readline())


def find_source_md(node):
    publisher = node.get("publisher", "").strip()
    section = node.get("section_title", "").strip()
    if not publisher:
        return None
    pub_dir = SOURCE_MD_DIR / publisher
    if not pub_dir.exists():
        return None
    for md_file in pub_dir.rglob("*.md"):
        fname = md_file.stem.lower()
        if section and section.lower()[:40] in fname:
            return md_file
    return None


def main():
    node = load_first_node()
    print(f"Node: {node['id']}")
    print(f"Category: {node.get('category')}")
    print(f"Publisher: {node.get('publisher')}")
    print(f"Title EN: {node.get('title_en', '')[:80]}")
    print(f"Content BN ({len(node.get('content_bn', ''))} chars): {node.get('content_bn', '')[:150]}...")
    print()

    # Find source
    source_md = find_source_md(node)
    md_content = None
    if source_md:
        print(f"Found source MD: {source_md.name}")
        md_content = source_md.read_text(encoding="utf-8")[:3000]
    else:
        print("No source MD found, using node data only")
    print()

    # Build prompt
    section_context = ""
    if md_content:
        section_context = f"\n### মূল উৎস দলিল (Source Markdown):\n{md_content}\n"

    prompt = f"""আপনি একজন বাংলাদেশের কৃষি সম্প্রসারণ অফিসার। আপনার কাজ হলো নিচে দেওয়া তথ্য থেকে একটি সম্পূর্ণ, সুসংগঠিত, কৃষক-বান্ধব জ্ঞান নোড তৈরি করা।

## মূল নিয়ম
1. সব তথ্য কৃষি বিজ্ঞানসম্মত ও সঠিক হতে হবে
2. রাসায়নিক নাম, মাত্রা (dosage), একক ইত্যাদি যথাযথভাবে সংরক্ষণ করুন — এগুলো পরিবর্তন করবেন না
3. ভাষা সহজ, প্রাঞ্জল, কৃষকের বোঝার মতো করে লিখুন
4. ইংরেজি প্রযুক্তিগত শব্দের পাশাপাশি বাংলা পরিভাষা ব্যবহার করুন
5. কোনো নতুন চিকিৎসা বা পরামর্শ তৈরি করবেন না — শুধু যা আছে তাকে সুন্দরভাবে সাজান
6. ছোট কন্টেন্টকে প্রসারিত করুন — বিস্তারিত ব্যাখ্যা দিন, উদাহরণ দিন
7. কন্টেন্ট অন্তত ১৫০ শব্দের হতে হবে
{section_context}
### বর্তমান নোড ডেটা:
- ক্যাটাগরি: {node.get('category', 'N/A')}
- শিরোনাম (EN): {node.get('title_en', '')}
- বিষয়বস্তু (BN): {node.get('content_bn', '')[:500]}
- সারসংক্ষেপ: {node.get('summary', '')}
- ট্যাগ: {node.get('tags', [])}
- উৎস: {node.get('source_document', '')}
- প্রকাশক: {node.get('publisher', '')}

## আউটপুট ফরমাট (JSON উত্তর দিন, কোনো অতিরিক্ত টেক্সট ছাড়া):

{{
  "id": "{node.get('id', '')}",
  "category": "{node.get('category', '')}",
  "title_bn": "বাংলা শিরোনাম (সংক্ষিপ্ত, অর্থপূর্ণ)",
  "title_en": "{node.get('title_en', '')}",
  "summary": "১-২ লাইনের সারসংক্ষেপ",
  "natural_intro_bn": "কৃষকের কাছে উপযোগী ভাষায় ভূমিকা (২-৩ বাক্য)",
  "content_bn": "বিস্তারিত বিষয়বস্তু — সুসংগঠিত, পয়েন্টযুক্ত, পড়াতে সহজ",
  "content_en": "Detailed content in English — well-organized, structured",
  "key_points": ["পয়েন্ট ১", "পয়েন্ট ২"],
  "tags": ["ট্যাগ১", "ট্যাগ২"],
  "safety_notes": "সতর্কতা (যদি থাকে, না থাকলে empty string)",
  "source_document": "{node.get('source_document', '')}",
  "publisher": "{node.get('publisher', '')}"
}}"""

    print("Calling Gemini 3.1 Flash Lite...")
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096, "topP": 0.9},
    }

    resp = httpx.post(f"{GEMINI_URL}?key={API_KEY}", headers=headers, json=payload, timeout=120)
    print(f"Status: {resp.status_code}")

    if resp.status_code != 200:
        print(f"ERROR: {resp.text[:500]}")
        return

    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    print("\n--- RAW OUTPUT ---")
    print(text[:2000])
    print("--- END RAW ---\n")

    # Try parse
    try:
        result = json.loads(text)
        print("✅ JSON PARSED SUCCESSFULLY")
        print(f"  title_bn: {result.get('title_bn', '')[:80]}")
        print(f"  content_bn ({len(result.get('content_bn', ''))} chars): {result.get('content_bn', '')[:200]}...")
        print(f"  key_points: {len(result.get('key_points', []))} items")
        print(f"  tags: {result.get('tags', [])}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON PARSE ERROR: {e}")


if __name__ == "__main__":
    main()
