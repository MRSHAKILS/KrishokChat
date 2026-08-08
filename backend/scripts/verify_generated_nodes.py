"""Verify generated knowledge nodes quality."""
import json
import pathlib

f = pathlib.Path(r"D:\KrishokChat Advisory System\backend\ml_assets\advisory\generated_knowledge_nodes.jsonl")
nodes = [json.loads(l) for l in f.read_text(encoding="utf-8").strip().split("\n") if l.strip()]
print(f"Generated nodes: {len(nodes)}")
for n in nodes:
    has_bn = bool(n.get("content_bn"))
    has_en = bool(n.get("content_en"))
    print(f"  {n['id']:45s} title={n.get('title_en','')[:40]:40s} bn_len={len(n.get('content_bn',''))} en_len={len(n.get('content_en',''))} tags={n.get('tags',[])[:3]}")
