"""Check mapping entries."""
import json
import pathlib

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
m = json.loads((ROOT / "ml_assets/advisory/disease_knowledge_map.json").read_text(encoding="utf-8"))

for k in ["Rice__Leaf_Blast", "Wheat__Blast", "Potato__Late_Blight"]:
    if k in m:
        info = m[k]
        print(f"{k}: crop={info['crop']}, disease={info['disease_name']}")
    else:
        print(f"{k}: NOT FOUND")

print()
print("All diseases with Blast:", [k for k in m if "blast" in k.lower()])
print()
print("All keys:", list(m.keys())[:10])
