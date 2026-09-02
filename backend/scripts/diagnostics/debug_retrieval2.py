"""Test retrieval with full augmentation as qa.py does it."""
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")
from app.agents.retrieval_agent import retrieve

query = "আলুর দেরি ব্লাইট রোগের প্রতিকার কি?"
detected_crop = "Potato"
detected_disease = "Late Blight"

augmented = query
crop_disease_en = ""
if detected_crop:
    crop_disease_en += f" {detected_crop.lower()}"
if detected_disease:
    disease_term = detected_disease.lower().replace("__", " ").replace("_", " ")
    crop_disease_en += f" {disease_term}"
    core = detected_disease.split("__")[-1] if "__" in detected_disease else detected_disease
    crop_disease_en += f" {core.lower().replace('_', ' ')}"
bn_to_en = {"আলুর": "potato", "দেরি ব্লাইট": "late blight", "প্রতিকার": "treatment", "রোগ": "disease", "রাস্ট": "rust"}
for bn, en in bn_to_en.items():
    if bn in query.lower():
        augmented += f" {en}"
augmented += crop_disease_en
augmented += " safe_agri"
augmented = augmented.strip()

print(f"Augmented: '{augmented}'")
srcs = retrieve(augmented, top_k=5)
print("\nResults:")
for s in srcs:
    print(f"  {s['score']:.1f} {s['id'][:45]:45s} {s.get('title_en','')[:50]}")
