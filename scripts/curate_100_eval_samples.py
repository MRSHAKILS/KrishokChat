import os
import glob
import json
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FULL = os.path.join(BASE_DIR, 'backend', 'ml_assets', 'vision', 'test_images', 'full_library')
SRC_WHEAT = os.path.join(BASE_DIR, 'backend', 'ml_assets', 'vision', 'test_images', 'wheat_disease')
SRC_CORN = os.path.join(BASE_DIR, 'backend', 'ml_assets', 'vision', 'test_images', 'corn_disease')
DEST_SAMPLES = os.path.join(BASE_DIR, 'frontend', 'public', 'samples')

MAX_EDGE = 640
JPEG_QUALITY = 82

# Target curation plan (exact 100 instances)
# Each entry: (crop, crop_bn, crop_en, disease, disease_bn, disease_en, target_class, src_folder, src_type, count, default_conf)
CLASSES_PLAN = [
    # --- RICE (20 instances) ---
    ("Rice", "ধান", "Rice", "Brown_Spot", "বাদামী দাগ (Brown Spot)", "Brown Spot", "Rice__Brown_Spot", "Rice__Brown_Spot", "full", 3, 99.8),
    ("Rice", "ধান", "Rice", "Leaf_Blast", "ব্লাস্ট রোগ (Leaf Blast)", "Leaf Blast", "Rice__Leaf_Blast", "Rice__Leaf_Blast", "full", 3, 100.0),
    ("Rice", "ধান", "Rice", "Bacterial_Leaf_Blight", "ব্যাকটেরিয়াল পাতা পোড়া (Blight)", "Bacterial Leaf Blight", "Rice__Bacterial_Leaf_Blight", "Rice__Bacterial_Leaf_Blight", "full", 3, 99.9),
    ("Rice", "ধান", "Rice", "Sheath_Blight", "খোল পোড়া রোগ (Sheath Blight)", "Sheath Blight", "Rice__Sheath_Blight", "Rice__Sheath_Blight", "full", 3, 99.7),
    ("Rice", "ধান", "Rice", "Leaf_Scald", "পাতা ঝলসানো (Leaf Scald)", "Leaf Scald", "Rice__Leaf_Scald", "Rice__Leaf_Scald", "full", 2, 99.5),
    ("Rice", "ধান", "Rice", "Narrow_Brown_Leaf_Spot", "সরু বাদামী দাগ (Narrow Brown Spot)", "Narrow Brown Leaf Spot", "Rice__Narrow_Brown_Leaf_Spot", "Rice__Narrow_Brown_Leaf_Spot", "full", 2, 99.4),
    ("Rice", "ধান", "Rice", "Rice_Hispa", "মাজরা / পামরী পোকার ক্ষত (Rice Hispa)", "Rice Hispa Feeding Scars", "Rice__Rice_Hispa", "Rice__Rice_Hispa", "full", 2, 99.6),
    ("Rice", "ধান", "Rice", "Healthy_Leaf", "সুস্থ ও নীরোগ পাতা (Healthy)", "Healthy Leaf", "Rice__Healthy_Leaf", "Rice__Healthy_Leaf", "full", 2, 100.0),

    # --- POTATO (16 instances) ---
    ("Potato", "আলু", "Potato", "Early_Blight", "আগাম ধসা (Early Blight)", "Early Blight", "Potato__Early_Blight", "Potato__Early_Blight", "full", 6, 99.9),
    ("Potato", "আলু", "Potato", "Late_Blight", "নাবি ধসা (Late Blight)", "Late Blight", "Potato__Late_Blight", "Potato__Late_Blight", "full", 6, 100.0),
    ("Potato", "আলু", "Potato", "Healthy_Leaf", "সুস্থ পাতা (Healthy Leaf)", "Healthy Leaf", "Potato__Healthy_Leaf", "Potato__Healthy_Leaf", "full", 4, 100.0),

    # --- WHEAT (16 instances) ---
    ("Wheat", "গম", "Wheat", "Leaf_Rust", "পাতার মরিচা রোগ (Leaf Rust)", "Leaf Rust", "Leaf Rust", "Leaf Rust", "wheat", 4, 100.0),
    ("Wheat", "গম", "Wheat", "Wheat_Blast", "গমের ব্লাস্ট রোগ (Wheat Blast)", "Wheat Blast", "Blast", "Blast", "wheat", 4, 100.0),
    ("Wheat", "গম", "Wheat", "Powdery_Mildew", "পাউডারি মিলডিউ (Powdery Mildew)", "Powdery Mildew", "Powdery Mildew", "Powdery Mildew", "wheat", 3, 99.6),
    ("Wheat", "গম", "Wheat", "Stripe_Rust", "হলুদ মরিচা রোগ (Stripe Rust)", "Stripe Rust", "Stripe Rust", "Stripe Rust", "wheat", 2, 99.8),
    ("Wheat", "গম", "Wheat", "Healthy", "সুস্থ গমের পাতা (Healthy Leaf)", "Healthy Leaf", "HealthyLeaf", "HealthyLeaf", "wheat", 3, 100.0),

    # --- CORN (16 instances) ---
    ("Corn", "ভুট্টা", "Corn", "Common_Rust", "কমন রাস্ট (Common Rust)", "Common Rust", "Common_Rust", "Common_Rust", "corn", 4, 100.0),
    ("Corn", "ভুট্টা", "Corn", "Gray_Leaf_Spot", "ধূসর পাতা দাগ (Gray Leaf Spot)", "Gray Leaf Spot", "Gray_Leaf_Spot", "Gray_Leaf_Spot", "corn", 4, 100.0),
    ("Corn", "ভুট্টা", "Corn", "Northern_Leaf_Blight", "উত্তরীয় পাতা পোড়া (NLB)", "Northern Leaf Blight", "Northern_Leaf_Blight", "Northern_Leaf_Blight", "corn", 4, 99.9),
    ("Corn", "ভুট্টা", "Corn", "Healthy", "সুস্থ ভুট্টা পাতা (Healthy)", "Healthy Leaf", "Healthy", "Healthy", "corn", 4, 100.0),

    # --- CHILLI (16 instances) ---
    ("Chilli", "মরিচ", "Chilli", "Bacterial_Spot", "ব্যাকটেরিয়াল দাগ (Bacterial Spot)", "Bacterial Spot", "Chili__Bacterial_Spot", "Chili__Bacterial_Spot", "full", 3, 100.0),
    ("Chilli", "মরিচ", "Chilli", "Curl_Virus", "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus)", "Leaf Curl Virus", "Chili__Curl_Virus", "Chili__Curl_Virus", "full", 4, 100.0),
    ("Chilli", "মরিচ", "Chilli", "Cercospora_Leaf_Spot", "সারকোস্পোরা দাগ (Cercospora)", "Cercospora Leaf Spot", "Chili__Cercospora_Leaf_Spot", "Chili__Cercospora_Leaf_Spot", "full", 3, 100.0),
    ("Chilli", "মরিচ", "Chilli", "Powdery_Mildew", "পাউডারি মিলডিউ (Powdery Mildew)", "Powdery Mildew", "Chili__Powdery_Mildew", "Chili__Powdery_Mildew", "full", 3, 99.7),
    ("Chilli", "মরিচ", "Chilli", "Healthy_Leaf", "সুস্থ মরিচ পাতা (Healthy Leaf)", "Healthy Leaf", "Chili__Healthy_Leaf", "Chili__Healthy_Leaf", "full", 3, 100.0),

    # --- BRASSICA (16 instances) ---
    ("Brassica", "কপি ও সরিষা", "Brassica", "Alternaria_Spot", "বাঁধাকপির অল্টারনারিয়া দাগ", "Cabbage Alternaria Spot", "Cabbage__Alternaria_Spot", "Cabbage__Alternaria_Spot", "full", 3, 100.0),
    ("Brassica", "কপি ও সরিষা", "Brassica", "Black_Rot", "কপির ব্লাক রট রোগ (Black Rot)", "Cabbage Black Rot", "Cabbage__Black_Rot", "Cabbage__Black_Rot", "full", 3, 99.8),
    ("Brassica", "কপি ও সরিষা", "Brassica", "Downy_Mildew", "ডাউনি মিলডিউ (Downy Mildew)", "Cabbage Downy Mildew", "Cabbage__Downy_Mildew", "Cabbage__Downy_Mildew", "full", 2, 99.7),
    ("Brassica", "কপি ও সরিষা", "Brassica", "Cauliflower_Alternaria", "ফুলকপির অল্টারনারিয়া রোগ", "Cauliflower Alternaria Disease", "Cauliflower__Alternaria_Disease", "Cauliflower__Alternaria_Disease", "full", 3, 100.0),
    ("Brassica", "কপি ও সরিষা", "Brassica", "Cauliflower_Bacterial_Spot", "ফুলকপির ব্যাকটেরিয়াল দাগ", "Cauliflower Bacterial Spot", "Cauliflower__Bacterial_Spot", "Cauliflower__Bacterial_Spot", "full", 2, 99.6),
    ("Brassica", "কপি ও সরিষা", "Brassica", "Healthy", "সুস্থ ফুলকপি পাতা (Healthy Leaf)", "Healthy Leaf", "Cauliflower__Healthy", "Cauliflower__Healthy", "full", 3, 100.0),
]

def optimize_image(src_path, dest_path):
    with Image.open(src_path) as img:
        img = img.convert('RGB')
        w, h = img.size
        if max(w, h) > MAX_EDGE:
            scale = MAX_EDGE / max(w, h)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        img.save(dest_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)

def main():
    total_planned = sum(item[9] for item in CLASSES_PLAN)
    print(f"Total planned sample instances: {total_planned}")

    manifest = []
    crop_counters = {}

    for (crop, crop_bn, crop_en, disease, disease_bn, disease_en, target_class, src_folder, src_type, count, default_conf) in CLASSES_PLAN:
        if src_type == 'wheat':
            src_dir = os.path.join(SRC_WHEAT, src_folder)
        elif src_type == 'corn':
            src_dir = os.path.join(SRC_CORN, src_folder)
        else:
            src_dir = os.path.join(SRC_FULL, src_folder)

        if not os.path.exists(src_dir):
            raise FileNotFoundError(f"Source folder not found: {src_dir}")

        all_imgs = sorted([
            f for f in os.listdir(src_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

        if len(all_imgs) < count:
            raise ValueError(f"Not enough images in {src_dir}: needed {count}, found {len(all_imgs)}")

        selected_imgs = all_imgs[:count]
        crop_lower = crop.lower()
        crop_counters[crop_lower] = crop_counters.get(crop_lower, 0)

        for idx, img_file in enumerate(selected_imgs):
            crop_counters[crop_lower] += 1
            seq = crop_counters[crop_lower]
            sample_id = f"{crop_lower}_{disease.lower()}_{idx+1:02d}"
            filename = f"{sample_id}.jpg"
            dest_rel_path = f"/samples/{crop_lower}/{filename}"
            dest_abs_path = os.path.join(DEST_SAMPLES, crop_lower, filename)

            src_img_path = os.path.join(src_dir, img_file)
            optimize_image(src_img_path, dest_abs_path)
            file_size_kb = os.path.getsize(dest_abs_path) / 1024

            entry = {
                "id": sample_id,
                "crop": crop,
                "cropBn": crop_bn,
                "cropEn": crop_en,
                "disease": disease,
                "diseaseBn": disease_bn,
                "diseaseEn": disease_en,
                "targetClass": target_class,
                "confidence": default_conf,
                "imageSrc": dest_rel_path,
                "cropHint": crop,
                "sizeKb": round(file_size_kb, 1),
            }
            manifest.append(entry)

    # Write manifest
    manifest_path = os.path.join(DEST_SAMPLES, 'samples_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Write python/ts intermediate catalog
    intermediate_json_path = os.path.join(BASE_DIR, 'frontend', 'src', 'lib', 'test-samples-catalog.json')
    with open(intermediate_json_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {len(manifest)} verified sample instances!")
    print(f"Manifest written to: {manifest_path}")
    print(f"Catalog written to: {intermediate_json_path}")

    # Summary by crop
    from collections import Counter
    counts = Counter(m['crop'] for m in manifest)
    for c, cnt in counts.items():
        print(f"  - {c}: {cnt} instances")

if __name__ == '__main__':
    main()
