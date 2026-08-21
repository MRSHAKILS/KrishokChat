import urllib.request, json, sys, os

sys.stdout.reconfigure(encoding='utf-8')

test_images = [
    ('rice-brown-spot', 'demo-assets/images/rice/brown_spot.jpg', 'Rice', 'Rice__Brown_Spot'),
    ('rice-leaf-blast', 'demo-assets/images/rice/leaf_blast.jpg', 'Rice', 'Rice__Leaf_Blast'),
    ('rice-healthy', 'demo-assets/images/rice/healthy_leaf.jpg', 'Rice', None),
    ('potato-early-blight', 'demo-assets/images/potato/early_blight.jpg', 'Potato', 'Potato__Early_Blight'),
    ('potato-late-blight', 'demo-assets/images/potato/late_blight.jpg', 'Potato', 'Potato__Late_Blight'),
    ('potato-healthy', 'demo-assets/images/potato/healthy_leaf.jpg', 'Potato', None),
    ('brassica-downy-mildew', 'demo-assets/images/brassica/cauliflower_downy_mildew.jpg', 'Brassica', 'Cauliflower__Downy_Mildew'),
    ('brassica-healthy', 'demo-assets/images/brassica/cauliflower_healthy.jpg', 'Brassica', None),
    ('tomato-no-model', 'demo-assets/images/tomato/late_blight.jpg', None, None),
    ('wheat-blast', 'demo-assets/images/wheat/wheat_blast.png', 'Wheat', 'Wheat__Blast'),
]

BOUNDARY = 'kcboundary123'

results = []
for label, img_path, expected_crop, expected_disease in test_images:
    if not os.path.exists(img_path):
        print(f'MISSING: {img_path}')
        results.append({'label': label, 'status': 'MISSING'})
        continue
    with open(img_path, 'rb') as f:
        img_data = f.read()
    fname = os.path.basename(img_path)
    ctype = 'image/png' if fname.endswith('.png') else 'image/jpeg'
    body = (
        f'--{BOUNDARY}\r\nContent-Disposition: form-data; name="file"; filename="{fname}"\r\nContent-Type: {ctype}\r\n\r\n'
    ).encode() + img_data + f'\r\n--{BOUNDARY}--\r\n'.encode()
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/detect',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={BOUNDARY}'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.load(r)
        status = result.get('status', '?')
        crop = result.get('crop', '?')
        disease = result.get('disease', '?')
        conf = result.get('disease_confidence', result.get('confidence_score', 0)) or 0
        ok = 'OK'
        if expected_crop and crop != expected_crop:
            ok = 'CROP_MISMATCH'
        results.append({'label': label, 'status': status, 'crop': crop, 'disease': disease, 'conf': conf, 'test_ok': ok})
        print(f'{ok} | {label:30s} | status={status:20s} crop={crop:10s} disease={str(disease):35s} conf={float(conf):.2f}')
    except Exception as e:
        results.append({'label': label, 'status': 'ERROR', 'error': str(e)})
        print(f'ERROR | {label:30s} | {e}')

print('\nSummary:', sum(1 for r in results if r.get('test_ok') == 'OK'), '/', len(results), 'passed')
