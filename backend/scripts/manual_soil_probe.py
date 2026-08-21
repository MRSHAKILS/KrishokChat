# Manual live probe — hits running backend at http://127.0.0.1:8000/api/soil/analyze
# Not a pytest test. Run with: python backend/scripts/manual_soil_probe.py (backend must be running)
# Kept for demo verification, not CI.
import urllib.request
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

img_path = 'demo-assets/images/soil/P0001_Doash_8.0kpa.jpg'
with open(img_path, 'rb') as f:
    img_data = f.read()

BOUNDARY = 'SoilBoundary123'
body = (
    f'--{BOUNDARY}\r\nContent-Disposition: form-data; name="file"; filename="P0001_Doash_8.0kpa.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
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

print('Status:', res.get('status'))
print('Notice message:', res.get('error'))
print('Trace:')
for ev in res.get('agent_trace', []):
    print(f"  - {ev.get('stage')}: {ev.get('status')} ({ev.get('detail')})")

print('\nDataset info returned:')
ds = res.get('dataset', {})
print(f"  - Total images in released dataset: {ds.get('total_images')}")
print(f"  - kPa Range: {ds.get('kpa_range')}")
print(f"  - Soil Types: {[t.get('name') for t in ds.get('soil_types', [])]}")
print(f"  - Model benchmarks: {[m.get('model') + ': RMSE ' + str(m.get('rmse')) for m in ds.get('model_results', [])]}")
