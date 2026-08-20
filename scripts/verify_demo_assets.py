import glob
import json
import os
from pathlib import Path
import sys
import urllib.request

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8000"

def test_detect(image_path, crop_hint=None):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()
    
    if crop_hint:
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="crop_hint"\r\n\r\n{crop_hint}\r\n'.encode())
        
    filename = os.path.basename(image_path)
    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode())
    with open(image_path, "rb") as f:
        body.extend(f.read())
    body.extend(f"\r\n--{boundary}--\r\n".encode())
    
    req = urllib.request.Request(
        f"{BASE}/api/detect",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode("utf-8"))
            return True, data
    except Exception as e:
        return False, str(e)

def test_qa(query):
    payload = json.dumps({"query": query}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/api/qa",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode("utf-8"))
            return True, data
    except Exception as e:
        return False, str(e)

print("=" * 60)
print("1. TESTING ALL DEMO-ASSETS IMAGES (with and without crop_hint)")
print("=" * 60)

for path in sorted(REPO_ROOT.glob("demo-assets/images/**/*.jpg")):
    path_str = str(path)
    if "soil" in path_str:
        continue
    hint = None
    if "rice" in path_str:
        hint = "Rice"
    elif "potato" in path_str:
        hint = "Potato"
    
    ok, res = test_detect(path_str, hint)
    if ok:
        print(f"IMAGE: {path.relative_to(REPO_ROOT)}")
        print(f"  -> status: {res.get('status')}")
        print(f"  -> crop: {res.get('crop')} (conf: {res.get('crop_confidence'):.4f})")
        print(f"  -> disease: {res.get('disease')} (conf: {res.get('disease_confidence'):.4f})")
        print(f"  -> advice length: {len(res.get('treatment_advice') or '')} chars, confidence: {res.get('treatment_confidence')}")
    else:
        print(f"IMAGE: {path.relative_to(REPO_ROOT)} -> FAILED: {res}")
    print()

print("=" * 60)
print("2. TESTING BRASSICA IMAGES (from ml_assets test_images)")
print("=" * 60)
for path in sorted(REPO_ROOT.glob("backend/ml_assets/vision/test_images/brassica_disease/*.jpg"))[:3]:
    path_str = str(path)
    ok, res = test_detect(path_str, crop_hint=None)
    if ok:
        print(f"BRASSICA IMAGE: {path.relative_to(REPO_ROOT)}")
        print(f"  -> status: {res.get('status')}")
        print(f"  -> crop: {res.get('crop')} (conf: {res.get('crop_confidence'):.4f})")
        print(f"  -> disease: {res.get('disease')} (conf: {res.get('disease_confidence'):.4f})")
        print(f"  -> advice confidence: {res.get('treatment_confidence')}")
    else:
        print(f"BRASSICA IMAGE: {path.relative_to(REPO_ROOT)} -> FAILED: {res}")
    print()

print("=" * 60)
print("3. TESTING ALL MANIFEST DEMO CASES")
print("=" * 60)
manifest_path = REPO_ROOT / "demo-assets" / "manifests" / "demo_cases.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for case in manifest.get("cases", []):
    case_id = case.get("id")
    family = case.get("family")
    print(f"CASE [{case_id}] ({family}):")
    if family == "chat":
        inp = case.get("input")
        ok, res = test_qa(inp)
        if ok:
            cat = res.get("category")
            conf = res.get("confidence")
            ans_len = len(res.get("answer") or "")
            print(f"  -> Result: category={cat}, confidence={conf}, answer_len={ans_len}")
        else:
            print(f"  -> FAILED: {res}")
    print()
