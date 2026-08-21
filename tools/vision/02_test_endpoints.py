"""Test vision endpoints with real images."""
import json
import sys
from pathlib import Path

import httpx

BASE = Path(__file__).resolve().parent.parent.parent
TEST_DIR = BASE / "vision" / "test_images"

def test_classify(image_path: Path):
    """Test /api/classify endpoint."""
    print(f"\n--- Testing /api/classify with {image_path.name} ---")
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        resp = httpx.post("http://localhost:8000/api/classify", files=files, timeout=30)

    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Crop: {data['crop']} ({data['confidence']:.1%})")
        print(f"Has disease model: {data['has_disease_model']}")
        print(f"Top 3: {data['top3']}")
    else:
        print(f"Error: {resp.text}")
    return resp.status_code == 200


def test_detect(image_path: Path):
    """Test /api/detect endpoint."""
    print(f"\n--- Testing /api/detect with {image_path.name} ---")
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        resp = httpx.post("http://localhost:8000/api/detect", files=files, timeout=30)

    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Crop: {data['crop']} ({data['crop_confidence']:.1%})")
        print(f"Disease: {data['disease']} ({data['disease_confidence']:.1%})")
        if data.get("disease_info"):
            info = data["disease_info"]
            print(f"  Description: {info.get('description_bn', '')[:100]}")
            print(f"  Solution: {info.get('solution_bn', '')[:100]}")
        else:
            print("  No disease info matched")
    else:
        print(f"Error: {resp.text}")
    return resp.status_code == 200


def main():
    print("=" * 60)
    print("VISION ENDPOINT TESTING")
    print("=" * 60)

    # Test crop classifier
    crop_tests = list((TEST_DIR / "crop_classifier").glob("*.jpg")) + list((TEST_DIR / "crop_classifier").glob("*.png"))
    if crop_tests:
        test_classify(crop_tests[0])
        test_detect(crop_tests[0])

    # Test rice disease
    rice_tests = list((TEST_DIR / "rice_disease").glob("*.jpg")) + list((TEST_DIR / "rice_disease").glob("*.png"))
    if rice_tests:
        test_detect(rice_tests[0])

    # Test potato disease
    potato_tests = list((TEST_DIR / "potato_disease").glob("*.jpg")) + list((TEST_DIR / "potato_disease").glob("*.png"))
    if potato_tests:
        test_detect(potato_tests[0])

    # Test brassica disease
    brassica_tests = list((TEST_DIR / "brassica_disease").glob("*.jpg")) + list((TEST_DIR / "brassica_disease").glob("*.png"))
    if brassica_tests:
        test_detect(brassica_tests[0])

    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
