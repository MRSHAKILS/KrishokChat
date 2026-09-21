import requests
import json
from pathlib import Path

url = "https://krishoktech-one.vercel.app/api/detect"

# Find a sample image from frontend/public/samples/
sample_path = Path("frontend/public/samples/rice/leaf_blast_1.jpg")
if not sample_path.exists():
    sample_path = list(Path("frontend/public/samples").glob("**/*.jpg"))[0]

print("Using sample:", sample_path)
with open(sample_path, "rb") as f:
    files = {"file": ("sample.jpg", f, "image/jpeg")}
    data = {"crop_hint": "rice"}
    resp = requests.post(url, files=files, data=data, timeout=30)
    print("Status:", resp.status_code)
    try:
        print("JSON:", json.dumps(resp.json(), indent=2))
    except Exception:
        print("Text:", resp.text)
