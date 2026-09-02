# Manual live probe — hits running backend at http://127.0.0.1:8000/api/soil/analyze for 3 demo images
# Not a pytest test. Run with: python backend/scripts/manual_soil_probe_all.py (backend must be running)
import urllib.request
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

test_samples = [
    ("demo-assets/images/soil/P0001_Doash_8.0kpa.jpg", "P0001_Doash_8.0kpa.jpg"),
    ("demo-assets/images/soil/P0064_Bele_0.0kpa.jpg", "P0064_Bele_0.0kpa.jpg"),
    ("demo-assets/images/soil/P0406_Atel_16.5kpa.jpg", "P0406_Atel_16.5kpa.jpg"),
]

BOUNDARY = 'SoilBoundary123'

print("=== Testing Soil Moisture Diagnosis for all 3 Demo Images ===")
for path, filename in test_samples:
    with open(path, 'rb') as f:
        img_data = f.read()

    body = (
        f'--{BOUNDARY}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
        + img_data
        + f'\r\n--{BOUNDARY}--\r\n'.encode()
    )

    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/soil/analyze',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={BOUNDARY}'},
        method='POST'
    )

    with urllib.request.urlopen(req, timeout=10) as r:
        res = json.load(r)

    print(f"\n[FILE: {filename}]")
    print(f"  Status: {res.get('status')}")
    print(f"  Soil Type: {res.get('soil_type_bn')} ({res.get('soil_type')})")
    print(f"  Moisture Tension: {res.get('kpa')} kPa")
    print(f"  Condition: {res.get('moisture_status_bn')}")
    print(f"  Confidence: {int((res.get('confidence') or 0)*100)}%")
    print(f"  Advisory: {res.get('advisory_bn')}")
    print("  Pipeline Rail Stages:")
    for ev in res.get('agent_trace', []):
        print(f"    - {ev.get('stage')}: {ev.get('status')} ({ev.get('detail')})")
