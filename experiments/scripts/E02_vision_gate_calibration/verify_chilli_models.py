from pathlib import Path
from PIL import Image
import torch
from ultralytics import YOLO
import time

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
variants = ['yolo26n', 'yolo26s', 'yolo26m', 'yolo26x']
full_lib = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "test_images" / "full_library"

target_classes = {
    'Chili__Bacterial_Spot': 'Bacterial Spot',
    'Chili__Cercospora_Leaf_Spot': 'Cercospora Leaf Spot',
    'Chili__Curl_Virus': 'Curl Virus',
    'Chili__Healthy_Leaf': 'Healthy Leaf',
}

images_by_folder = {}
for folder_name in target_classes:
    p = full_lib / folder_name
    imgs = sorted(list(p.glob('*.jpg')) + list(p.glob('*.png')) + list(p.glob('*.jpeg')))
    images_by_folder[folder_name] = imgs

total_test_images = sum(len(v) for v in images_by_folder.values())
print(f"Total Chili test images: {total_test_images}")

results = {}

CHILLI_SRC = WORKSPACE_ROOT / "backend" / "ml_assets" / "updated retrain" / "chilli disease classifier"

import zipfile

zip_files = {
    'yolo26n': list(CHILLI_SRC.glob('yolo26n-chilli*.zip'))[0],
    'yolo26s': list(CHILLI_SRC.glob('yolo26s-chilli*.zip'))[0],
    'yolo26m': list(CHILLI_SRC.glob('yolo26m-chilli*.zip'))[0],
    'yolo26x': list(CHILLI_SRC.glob('yolo26x-chilli*.zip'))[0],
}

cache_dir = WORKSPACE_ROOT / "experiments" / "results" / "E02_vision_gate_calibration" / "chilli_weights_cache"
cache_dir.mkdir(parents=True, exist_ok=True)

for v in variants:
    pt_path = cache_dir / f"{v}.pt"
    if not pt_path.exists():
        with zipfile.ZipFile(zip_files[v], 'r') as z:
            for member in z.namelist():
                if member.endswith('best.pt'):
                    with z.open(member) as zf, open(pt_path, 'wb') as out_f:
                        out_f.write(zf.read())
                elif member.endswith('best.onnx'):
                    with z.open(member) as zf, open(cache_dir / f"{v}.onnx", 'wb') as out_f:
                        out_f.write(zf.read())
    model = YOLO(str(pt_path))
    names = model.names
    
    correct = 0
    total = 0
    per_class_correct = {k: 0 for k in target_classes}
    latencies = []
    
    for folder_name, true_class in target_classes.items():
        imgs = images_by_folder[folder_name]
        for img_path in imgs:
            t0 = time.perf_counter()
            res = model(str(img_path), imgsz=224, verbose=False)[0]
            latencies.append((time.perf_counter() - t0) * 1000)
            
            top1_id = int(res.probs.top1)
            pred_name = names[top1_id]
            conf = float(res.probs.top1conf)
            
            # Check match
            is_correct = (pred_name.lower().replace(" ", "").replace("_", "") == true_class.lower().replace(" ", "").replace("_", ""))
            if is_correct:
                correct += 1
                per_class_correct[folder_name] += 1
            total += 1
            
    p50_lat = sorted(latencies)[len(latencies)//2]
    pt_size_mb = Path(pt_path).stat().st_size / (1024 * 1024)
    onnx_path = cache_dir / f"{v}.onnx"
    onnx_size_mb = onnx_path.stat().st_size / (1024 * 1024) if onnx_path.exists() else 0.0
    
    results[v] = {
        'correct': correct,
        'total': total,
        'acc': correct / total if total else 0,
        'per_class': per_class_correct,
        'pt_size_mb': pt_size_mb,
        'onnx_size_mb': onnx_size_mb,
        'p50_lat_ms': p50_lat,
        'names': names
    }

print("\n" + "="*75)
print(f"{'Variant':<10} | {'Field Acc':<12} | {'PyTorch MB':<12} | {'ONNX MB':<10} | {'p50 Lat (ms)':<12}")
print("="*75)
for v in variants:
    r = results[v]
    print(f"{v:<10} | {r['correct']}/{r['total']} ({r['acc']*100:.2f}%) | {r['pt_size_mb']:<12.2f} | {r['onnx_size_mb']:<10.2f} | {r['p50_lat_ms']:<12.2f}")

print("="*75)
for v in variants:
    r = results[v]
    print(f"\nBreakdown for {v}:")
    for k, v_count in r['per_class'].items():
        print(f"  {k}: {v_count}/10")
