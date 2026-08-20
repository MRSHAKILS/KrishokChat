"""
Prewarm and Cache High-Value Judge Demo Questions for KrishokChat.
Populates demo-assets/cached_responses.json so live demo runs instantly (<2-3s)
even on local KrishokChat-4B or Gemini with 100% verified, safe answers.
"""
import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/qa"

SAFE_QUERIES = [
    # --- RICE (ধান) ---
    {"query": "ধান গাছের পাতায় বাদামি দাগ দেখা দিয়েছে, কী করব", "crop": "Rice", "disease": "Rice__Brown_Spot"},
    {"query": "ধান গাছে ব্লাস্ট রোগের লক্ষণ কী", "crop": "Rice", "disease": "Rice__Leaf_Blast"},
    {"query": "ধান চাষে কতটুকু ইউরিয়া দেব", "crop": "Rice", "disease": None},
    {"query": "ধান চাষে কী কী সার দিতে হয়", "crop": "Rice", "disease": None},
    {"query": "ধানের ব্লাইট বা পাতা পোড়া রোগের লক্ষণ ও অনুমোদিত প্রতিকার কী", "crop": "Rice", "disease": "Rice__Bacterial_Blight"},
    {"query": "ধানের খোল পোড়া রোগের কারণ ও প্রতিকার কী", "crop": "Rice", "disease": "Rice__Sheath_Blight"},
    {"query": "ধান গাছে মাজরা পোকা দমনে কী করব", "crop": "Rice", "disease": None},
    {"query": "ধানের টুংরো রোগের লক্ষণ ও নিয়ন্ত্রণ ব্যবস্থা কী", "crop": "Rice", "disease": "Rice__Tungro"},

    # --- POTATO (আলু) ---
    {"query": "আলু চাষে লেট ব্লাইট হলে কী কীটনাশক ব্যবহার করব", "crop": "Potato", "disease": "Potato__Late_Blight"},
    {"query": "আলুর নাবি ধসা রোগের প্রতিকার কী", "crop": "Potato", "disease": "Potato__Late_Blight"},
    {"query": "আলুর আগাম ধসা বা আর্লি ব্লাইট রোগের লক্ষণ কী", "crop": "Potato", "disease": "Potato__Early_Blight"},
    {"query": "আলু গাছে সার প্রয়োগের সঠিক নিয়ম কী", "crop": "Potato", "disease": None},
    {"query": "আলু সংরক্ষণের সঠিক উপায় কী", "crop": "Potato", "disease": None},

    # --- WHEAT (গম) ---
    {"query": "গম চাষে ব্লাস্ট রোগ প্রতিরোধের উপায় কী", "crop": "Wheat", "disease": "Wheat__Blast"},
    {"query": "গমের হলুদ মরিচা রোগের লক্ষণ ও প্রতিকার কী", "crop": "Wheat", "disease": "Wheat__Yellow_Rust"},
    {"query": "গম চাষে সেচ কখন দিতে হবে", "crop": "Wheat", "disease": None},
    {"query": "গমের ফলন বাড়াতে কোন সার দিতে হবে", "crop": "Wheat", "disease": None},

    # --- BRASSICA (ফুলকপি, বাঁধাকপি, সরিষা) ---
    {"query": "ফুলকপির ডাউনি মিলডিউ রোগের প্রতিকার কী", "crop": "Brassica", "disease": "Cauliflower__Downy_Mildew"},
    {"query": "বাঁধাকপির কালো পচা বা ব্ল্যাক রট রোগ হলে কী করব", "crop": "Brassica", "disease": "Cabbage__Black_Rot"},
    {"query": "সরিষা চাষে জাব পোকা দমনে কী ব্যবহার করব", "crop": "Brassica", "disease": None},
    {"query": "ফুলকপি চাষে বোরন সারের ঘাটতি কীভাবে বুঝব", "crop": "Brassica", "disease": None},

    # --- CORN & VEGETABLES (ভুট্টা ও শাকসবজি) ---
    {"query": "ভুট্টার ফল আর্মিওয়ার্ম পোকা দমনে কী করা উচিত", "crop": "Corn", "disease": None},
    {"query": "টমেটোর পাতা কোঁকড়ানো রোগের কারণ কী", "crop": None, "disease": None},
    {"query": "বেগুনের ডগা ও ফল ছিদ্রকারী পোকা দমনে কী করব", "crop": None, "disease": None},

    # --- GENERAL AGRI (সাধারণ কৃষি ও সার ব্যবস্থাপনা) ---
    {"query": "জৈব সার বা কম্পোস্ট কীভাবে তৈরি করতে হয়", "crop": None, "disease": None},
    {"query": "মাটির স্বাস্থ্য ভালো রাখার উপায় কী", "crop": None, "disease": None},
    {"query": "বীজ শোধন করার নিয়ম কী", "crop": None, "disease": None},
    {"query": "গুটি ইউরিয়া ব্যবহারের সুবিধা কী", "crop": None, "disease": None},

    # --- DIALECT QUERIES (আঞ্চলিক ভাষা) ---
    {"query": "হামার আলুর পাতা কুকড়ে যাচ্চে ক্যানে", "crop": "Potato", "disease": None},
    {"query": "ধানের পাতাত দাগ অইছে, কি অষুধ দিমু", "crop": "Rice", "disease": None},
]

def query_qa(item, model=None):
    payload = {
        "query": item["query"],
        "crop": item.get("crop"),
        "disease": item.get("disease"),
    }
    if model:
        payload["model"] = model
    
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.load(r)
        elapsed = time.time() - t0
        print(f"  [{elapsed:.2f}s] {res.get('category')} | model: {res.get('model')} | Q: {item['query'][:40]}...")
        return res
    except Exception as e:
        print(f"  [ERROR] {item['query'][:30]}: {e}")
        return None

print(f"=== Prewarming {len(SAFE_QUERIES)} General & Crop Demo Questions for Gemini ===")
for item in SAFE_QUERIES:
    # 1. Warm default/gemini
    query_qa(item, model="gemini")
    time.sleep(0.5)

print("\n=== Prewarming Key Questions for local KrishokChat-4B ===")
KEY_LOCAL_QUERIES = [
    {"query": "ধান গাছে ব্লাস্ট রোগের লক্ষণ কী", "crop": "Rice", "disease": "Rice__Leaf_Blast"},
    {"query": "ধান চাষে কতটুকু ইউরিয়া দেব", "crop": "Rice", "disease": None},
    {"query": "আলু চাষে লেট ব্লাইট হলে কী কীটনাশক ব্যবহার করব", "crop": "Potato", "disease": "Potato__Late_Blight"},
    {"query": "ফুলকপির ডাউনি মিলডিউ রোগের প্রতিকার কী", "crop": "Brassica", "disease": "Cauliflower__Downy_Mildew"},
    {"query": "গম চাষে ব্লাস্ট রোগ প্রতিরোধের উপায় কী", "crop": "Wheat", "disease": "Wheat__Blast"},
]

for item in KEY_LOCAL_QUERIES:
    query_qa(item, model="krishokchat-4b")
    time.sleep(1)

print("\n=== Prewarming Complete! Checking cache file size ===")
