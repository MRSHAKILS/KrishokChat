"""
Merge refined nodes with already-good nodes, produce final output.
Also generates quality report.
"""
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
CLEAN_PATH = RAG_ROOT / "processed" / "knowledge_nodes_clean.jsonl"
REFINED_PATH = RAG_ROOT / "processed" / "knowledge_nodes_refined.jsonl"
FINAL_PATH = RAG_ROOT / "processed" / "knowledge_nodes_final.jsonl"
REPORT_PATH = RAG_ROOT / "logs" / "quality_report.json"


def count_words_bengali(text):
    """Rough word count (space-separated)."""
    if not text:
        return 0
    return len(text.split())


def main():
    print("Loading refined nodes...")
    refined = {}
    if REFINED_PATH.exists():
        with open(REFINED_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    node = json.loads(line)
                    if "id" in node and not node.get("error"):
                        refined[node["id"]] = node
                except json.JSONDecodeError:
                    pass

    print(f"  Loaded {len(refined)} refined nodes")

    print("Loading original nodes...")
    originals = []
    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                originals.append(json.loads(line))

    print(f"  Loaded {len(originals)} original nodes")

    # Merge: use refined if available, else keep original
    final = []
    stats = {"refined": 0, "original": 0, "total": 0}
    quality = {
        "title_bn_empty": 0,
        "content_bn_short": 0,
        "content_bn_good": 0,
        "has_key_points": 0,
        "has_tags": 0,
        "category_distribution": Counter(),
    }

    for orig in originals:
        node_id = orig.get("id", "")
        if node_id in refined:
            node = refined[node_id]
            stats["refined"] += 1
        else:
            node = orig
            stats["original"] += 1

        stats["total"] += 1

        # Quality checks
        if not node.get("title_bn", "").strip():
            quality["title_bn_empty"] += 1

        bn_content = node.get("content_bn", "")
        if count_words_bengali(bn_content) < 50:
            quality["content_bn_short"] += 1
        else:
            quality["content_bn_good"] += 1

        if node.get("key_points"):
            quality["has_key_points"] += 1
        if node.get("tags"):
            quality["has_tags"] += 1

        quality["category_distribution"][node.get("category", "unknown")] += 1

        final.append(node)

    # Save final
    with open(FINAL_PATH, "w", encoding="utf-8") as f:
        for node in final:
            f.write(json.dumps(node, ensure_ascii=False) + "\n")

    print(f"\nFinal output: {FINAL_PATH}")
    print(f"  Total: {stats['total']}")
    print(f"  Refined: {stats['refined']}")
    print(f"  Original (kept): {stats['original']}")

    # Save report
    quality["category_distribution"] = dict(quality["category_distribution"].most_common())
    report = {
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
        "quality": quality,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nQuality report: {REPORT_PATH}")
    print(f"  Title_bn empty: {quality['title_bn_empty']}")
    print(f"  Content_bn short (<50 words): {quality['content_bn_short']}")
    print(f"  Content_bn good (>=50 words): {quality['content_bn_good']}")
    print(f"  Has key_points: {quality['has_key_points']}")
    print(f"  Has tags: {quality['has_tags']}")

    print(f"\nCategory distribution:")
    for cat, count in quality["category_distribution"].items():
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
