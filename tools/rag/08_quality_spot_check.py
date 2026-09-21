"""
Quality Spot Check: Send 100 representative refined nodes back to Gemini for evaluation.
Scores each node on 6 dimensions and reports pass/fail.
"""
import json
import os
import random
import statistics
from pathlib import Path
from datetime import datetime

import httpx

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
REFINED_PATH = RAG_ROOT / "processed" / "knowledge_nodes_refined.jsonl"
SOURCE_MD_DIR = RAG_ROOT / "source_md"
REPORT_PATH = RAG_ROOT / "eval" / "quality_spot_check.jsonl"
SUMMARY_PATH = RAG_ROOT / "eval" / "quality_summary.json"

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"
# API key must come from the environment (never commit a real key).
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    raise SystemExit("Set GEMINI_API_KEY in the environment to run this spot check.")

random.seed(2026)


def load_refined_nodes():
    """Load all successfully refined nodes."""
    nodes = []
    with open(REFINED_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                n = json.loads(line)
                if not n.get("error") and n.get("content_bn"):
                    nodes.append(n)
            except:
                pass
    return nodes


def sample_stratified(nodes, n=100):
    """Sample nodes stratified by category."""
    by_cat = {}
    for node in nodes:
        cat = node.get("category", "unknown")
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(node)

    # Calculate samples per category (proportional)
    total = len(nodes)
    samples = []
    remaining = n

    for cat, cat_nodes in sorted(by_cat.items(), key=lambda x: -len(x[1])):
        if remaining <= 0:
            break
        # Proportional allocation
        n_sample = max(1, round(len(cat_nodes) / total * n))
        n_sample = min(n_sample, len(cat_nodes), remaining)
        samples.extend(random.sample(cat_nodes, n_sample))
        remaining -= n_sample

    # Fill remaining if any
    if remaining > 0:
        pool = [n for n in nodes if n not in samples]
        if pool:
            samples.extend(random.sample(pool, min(remaining, len(pool))))

    return samples[:n]


def find_source_md(node):
    """Try to find the source MD file for a node."""
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


def evaluate_node(node, source_md_content=None):
    """Send a refined node to Gemini for quality evaluation."""

    source_context = ""
    if source_md_content:
        source_context = f"""
### ORIGINAL SOURCE MARKDOWN (for factual verification):
{source_md_content[:3000]}
"""

    prompt = f"""আপনি একজন বিশেষজ্ঞ কৃষি বিজ্ঞানী ও ডেটাসেট গুণগত মান পর্যালোককর্তা। নিচে একটি কৃষি জ্ঞান নোড দেওয়া হলো। এটি একটি AI-জেনারেটেড রিফাইনড নোড। আপনার কাজ হলো এর গুণগত মান যাচাই করা।

{source_context}
### রিফাইনড নোড (AI-generated):
শিরোনাম (BN): {node.get('title_bn', '')}
শিরোনাম (EN): {node.get('title_en', '')}
ক্যাটাগরি: {node.get('category', '')}
সারসংক্ষেপ: {node.get('summary', '')}
ভূমিকা: {node.get('natural_intro_bn', '')}
বিষয়বস্তু (BN): {node.get('content_bn', '')}
মূল পয়েন্ট: {node.get('key_points', [])}
ট্যাগ: {node.get('tags', [])}
সতর্কতা: {node.get('safety_notes', '')}
প্রকাশক: {node.get('publisher', '')}

## মূল্যায়ন মানদণ্ড (প্রতিটিতে 1-10 স্কোর দিন):

1. **বাস্তবসম্মততা (Factual Accuracy)**: তথ্যগুলো কি কৃষি বিজ্ঞানের সাথে সামঞ্জস্যপূর্ণ? কোনু ভুল তথ্য আছে কি?
2. **সম্পূর্ণতা (Completeness)**: নোডটি কি পর্যাপ্ত গভীরতায় লেখা? প্রয়োজনীয় তথ্য বাদ পড়েছে কি?
3. **ভাষার গুণগত মান (Language Quality)**: বাংলা কি প্রাঞ্জল, কৃষক-বান্ধব ও বিজ্ঞানসম্মত? ব্যাকরণগত ভুল আছে কি?
4. **সুসংগঠন (Organization)**: নোডটি কি সুন্দরভাবে সাজানো? পয়েন্ট, উপ-শিরোনাম ইত্যাদি আছে কি?
5. **নিরাপত্তা সতর্কতা (Safety)**: রাসায়নিক নাম, মাত্রা, সতর্কতা কি সঠিকভাবে সংরক্ষিত? কোনো বিপজ্জনক পরামর্শ আছে কি?
6. **হ্যালুসিনেশন সনাক্তকরণ (Hallucination)**: AI কি কোন৏ ভুল তথ্য বা বিদ্যমান নয় এমন কিছু যোগ করেছে?

## আউটপুট ফরমাট (JSON):
{{
  "node_id": "{node.get('id', '')}',
  "scores": {{
    "factual_accuracy": <1-10>,
    "completeness": <1-10>,
    "language_quality": <1-10>,
    "organization": <1-10>,
    "safety": <1-10>,
    "no_hallucination": <1-10>
  }},
  "overall_score": <average>,
  "critical_issues": ["সমস্যা ১", "সমস্যা ২"],
  "positive_points": ["ভালো দিক ১", "ভালো দিক ২"],
  "verdict": "pass/fail"
}}"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048},
    }

    try:
        resp = httpx.post(f"{GEMINI_URL}?key={API_KEY}", headers=headers, json=payload, timeout=90)
        if resp.status_code != 200:
            return None, f"http_{resp.status_code}"
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Clean
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        return text, "success"
    except Exception as e:
        return None, str(e)[:100]


def main():
    print("Loading refined nodes...")
    nodes = load_refined_nodes()
    print(f"  Loaded {len(nodes)} successful nodes")

    print("Sampling 100 stratified nodes...")
    samples = sample_stratified(nodes, 100)
    print(f"  Sampled {len(samples)} nodes")

    # Show category distribution
    cats = {}
    for n in samples:
        c = n.get("category", "unknown")
        cats[c] = cats.get(c, 0) + 1
    print("  Category distribution:")
    for c, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"    {c}: {cnt}")

    print("\nSending to Gemini for evaluation...")
    print("(This will take ~15-20 minutes due to rate limits)\n")

    results = []
    for i, node in enumerate(samples):
        node_id = node.get("id", "")
        print(f"[{i+1}/100] Evaluating: {node_id}")

        # Find source MD for context
        source_md = find_source_md(node)
        md_content = None
        if source_md:
            try:
                md_content = source_md.read_text(encoding="utf-8")
            except:
                pass

        result, status = evaluate_node(node, md_content)

        if result is None:
            print(f"  FAILED: {status}")
            continue

        try:
            eval_result = json.loads(result)
            eval_result["timestamp"] = datetime.now().isoformat()
            results.append(eval_result)

            # Save immediately
            REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(REPORT_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(eval_result, ensure_ascii=False) + "\n")
                f.flush()

            score = eval_result.get("overall_score", 0)
            verdict = eval_result.get("verdict", "?")
            print(f"  Score: {score:.1f}/10 — {verdict}")

        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}")
            print(f"  Raw: {result[:200]}")

        # Rate limit: 4s between calls
        import time
        time.sleep(4)

    # Summary
    if results:
        print("\n" + "=" * 60)
        print("QUALITY SPOT CHECK SUMMARY")
        print("=" * 60)

        dimensions = ["factual_accuracy", "completeness", "language_quality", "organization", "safety", "no_hallucination"]
        dim_names = {
            "factual_accuracy": "Factual Accuracy",
            "completeness": "Completeness",
            "language_quality": "Language Quality",
            "organization": "Organization",
            "safety": "Safety",
            "no_hallucination": "No Hallucination",
        }

        print(f"\nNodes evaluated: {len(results)}")
        print("\nDimension Scores (out of 10):")
        for dim in dimensions:
            scores = [r["scores"][dim] for r in results if "scores" in r and dim in r["scores"]]
            if scores:
                avg = statistics.mean(scores)
                med = statistics.median(scores)
                mn = min(scores)
                mx = max(scores)
                print(f"  {dim_names[dim]:>20}: avg={avg:.1f}, med={med:.0f}, min={mn}, max={mx}")

        overall = [r["overall_score"] for r in results if "overall_score" in r]
        if overall:
            print(f"\nOverall Score: {statistics.mean(overall):.2f}/10")
            print(f"  Min: {min(overall):.1f}, Max: {max(overall):.1f}")

        passes = sum(1 for r in results if r.get("verdict") == "pass")
        fails = sum(1 for r in results if r.get("verdict") == "fail")
        print(f"\nPass: {passes}/{len(results)} ({passes/len(results)*100:.0f}%)")
        print(f"Fail: {fails}/{len(results)} ({fails/len(results)*100:.0f}%)")

        # Critical issues
        all_issues = []
        for r in results:
            all_issues.extend(r.get("critical_issues", []))
        if all_issues:
            print(f"\nCritical Issues Found ({len(all_issues)}):")
            from collections import Counter
            for issue, cnt in Counter(all_issues).most_common(10):
                print(f"  [{cnt}x] {issue}")

        # Save summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "nodes_evaluated": len(results),
            "dimension_averages": {},
            "overall_average": statistics.mean(overall) if overall else 0,
            "pass_rate": passes / len(results) if results else 0,
            "pass_count": passes,
            "fail_count": fails,
            "critical_issues": all_issues,
        }
        for dim in dimensions:
            scores = [r["scores"][dim] for r in results if "scores" in r and dim in r["scores"]]
            if scores:
                summary["dimension_averages"][dim] = statistics.mean(scores)

        with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"\nSummary saved to: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
