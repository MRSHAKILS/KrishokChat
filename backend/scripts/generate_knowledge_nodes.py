"""Generate missing knowledge nodes for Category B diseases using free Gemini keys."""
import json
import os
import pathlib
import sys
import time

import dotenv

sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
TASKS_FILE = ROOT / "ml_assets/advisory/generation_tasks.json"
OUT_FILE = ROOT / "ml_assets/advisory/generated_knowledge_nodes.jsonl"

# Load env from project root .env
dotenv.load_dotenv(r"D:\KrishokChat Advisory System\.env")


def get_gemini_keys():
    keys = []
    for i in range(1, 30):
        k = os.getenv(f"GEMINI_API_KEY_{i}")
        if k:
            keys.append(k)
    k = os.getenv("GEMINI_API_KEY")
    if k:
        keys.append(k)
    return keys


_key_idx = 0
_last_call = {}


def next_key(keys):
    global _key_idx
    key = keys[_key_idx % len(keys)]
    _key_idx += 1
    # Rate limit: 1.5s between calls per key
    elapsed = time.time() - _last_call.get(id(key), 0)
    if elapsed < 1.5:
        time.sleep(1.5 - elapsed)
    _last_call[id(key)] = time.time()
    return key


def generate_node(task, keys):
    """Generate a knowledge node for a disease using Gemini."""
    crop = task["crop"]
    disease = task["disease"]
    cls_name = task["class"]
    needs = task["needs"]

    # Build context from existing data
    context_parts = []
    if task.get("details_content"):
        dc = task["details_content"]
        if dc.get("description_bn"):
            context_parts.append(f"বর্ণনা: {dc['description_bn'][:200]}")
        if dc.get("solution_bn"):
            context_parts.append(f"প্রতিকার: {dc['solution_bn'][:200]}")
        if dc.get("cause_bn"):
            context_parts.append(f"কারণ: {dc['cause_bn'][:200]}")

    if task.get("rag_content"):
        rc = task["rag_content"]
        if rc.get("title_en"):
            context_parts.append(f"শিরোনাম: {rc['title_en']}")
        if rc.get("content_en"):
            context_parts.append(f"বিষয়বস্তু: {rc['content_en'][:300]}")
        if rc.get("tags"):
            context_parts.append(f"ট্যাগ: {', '.join(rc['tags'])}")

    context = "\n".join(context_parts) if context_parts else "কোনো পূর্ববর্তী তথ্য নেই।"

    if needs == "rag_node":
        prompt = f"""তুমি একজন কৃষি বিশেষজ্ঞ। নিচের রোগের জন্য একটি পূর্ণাঙ্গ জ্ঞান নোড তৈরি করো।

ফসল: {crop}
রোগ: {disease} ({cls_name})

বিদ্যমান তথ্য:
{context}

দয়া করে নিম্নলিখিত ফরম্যাটে JSON আউটপুট দাও:
{{
  "title_bn": "রোগের বাংলা শিরোনাম",
  "title_en": "English title",
  "content_bn": "রোগের বিস্তারিত বর্ণনা, কারণ, লক্ষণ, এবং প্রতিকার (বাংলায়, বিস্তারিত)",
  "content_en": "Detailed description, cause, symptoms, and treatment (in English)",
  "tags": ["ট্যাগ১", "ট্যাগূ", "{crop}", "{disease}"],
  "treatment_summary_bn": "প্রতিকারের সংক্ষিপ্ত সারাংশ (বাংলায়)",
  "prevention_bn": "প্রতিরোধের উপায় (বাংলায়)"
}}

শুধুমাত্র JSON আউটপুট দাঠ, অন্য কিছু নয়।"""
    else:
        prompt = f"""তুমি একজন কৃষি বিশেষজ্ঞ। নিচের রোগের জন্য বিস্তারিত তথ্য তৈরি করো।

ফসল: {crop}
রোগ: {disease} ({cls_name})

বিদ্যমান তথ্য:
{context}

দয়া করে নিম্নলিখিত ফরম্যাটে JSON আউটপুট দাও:
{{
  "title_bn": "রোগের বাংলা শিরোনাম",
  "content_bn": "রোগের বিস্তারিত বর্ণনা, কারণ, লক্ষণ, এবং প্রতিকার (বাংলায়, বিস্তারিত)",
  "content_en": "Detailed description, cause, symptoms, and treatment (in English)",
  "tags": ["ট্যাগ১", "ট্যাগূ", "{crop}", "{disease}"],
  "treatment_summary_bn": "প্রতিকারের সংক্ষিপ্ত সারাংশ (বাংলায়)",
  "prevention_bn": "প্রতিরোধের উপায় (বাংলায়)"
}}

শুধুমাত্র JSON আউটপুট দাও, অন্য কিছু নয়।"""

    key = next_key(keys)
    try:
        from google import genai
        client = genai.Client(api_key=key)
        resp = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
            ),
        )
        _last_call[id(key)] = time.time()
        text = resp.text.strip()
        # Strip markdown code block if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"    ERROR: {e}")
        return None


def main():
    tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    keys = get_gemini_keys()
    print(f"Keys available: {len(keys)}")
    print(f"Tasks to process: {len(tasks)}")

    generated = []
    for i, task in enumerate(tasks):
        cls = task["class"]
        print(f"\n[{i+1}/{len(tasks)}] Generating for: {cls} ({task['needs']})")

        # Skip healthy leaves
        if "healthy" in cls.lower() or "সুস্থ" in cls.lower():
            print("  SKIPPED (healthy leaf)")
            continue

        result = generate_node(task, keys)
        if result:
            node = {
                "id": f"GEN_{task['crop'].upper()}_{cls.replace('__','_').replace(' ','_')}",
                "category": "disease",
                "title_bn": result.get("title_bn", ""),
                "title_en": result.get("title_en", task["disease"]),
                "content_bn": result.get("content_bn", ""),
                "content_en": result.get("content_en", ""),
                "summary": result.get("content_bn", "")[:100],
                "tags": result.get("tags", [task["crop"], task["disease"]]),
                "source_document": "Generated by Gemini-3.1-Flash-Lite (advisory workflow)",
                "publisher": "AI-Generated",
                "citation": f"Generated for {task['crop']} - {task['disease']}",
                "section_title": task["disease"],
                "treatment_summary_bn": result.get("treatment_summary_bn", ""),
                "prevention_bn": result.get("prevention_bn", ""),
                "bm25_text": f"{result.get('title_bn','')} {result.get('title_en','')} {result.get('content_bn','')} {result.get('content_en','')} {' '.join(result.get('tags',[]))} disease {' '.join(result.get('tags',[]))}",
                "embed_text": f"{result.get('content_en','')} {result.get('content_bn','')}",
                "generated": True,
            }
            generated.append(node)
            print(f"  OK: {node['title_en'][:50]}")
        else:
            print(f"  FAILED")

    # Append to output file
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for node in generated:
            f.write(json.dumps(node, ensure_ascii=False) + "\n")

    print(f"\nGenerated {len(generated)} knowledge nodes")
    print(f"Saved to {OUT_FILE}")
    return generated


if __name__ == "__main__":
    main()
