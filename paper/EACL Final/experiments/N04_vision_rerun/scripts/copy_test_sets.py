"""Copy test datasets from D:\\499A Dataset into backend/ml_assets/vision/test_images/
so that all test sets are stored locally in the repository for reviewers.

Copies:
1. Corn: D:\\499A Dataset\\Corn\\test -> backend/ml_assets/vision/test_images/corn_disease/
2. Chilli: D:\\499A Dataset\\Solanaceae\\test (7 Chili classes) -> backend/ml_assets/vision/test_images/chilli_disease/ & full_library/
3. Potato: D:\\499A Dataset\\Potato\\test -> backend/ml_assets/vision/test_images/potato_disease/ & full_library/
4. Brassica: D:\\499A Dataset\\Brassica\\test -> backend/ml_assets/vision/test_images/brassica_disease/ & full_library/
"""

import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
TEST_IMAGES_DIR = REPO_ROOT / "backend" / "ml_assets" / "vision" / "test_images"
FULL_LIBRARY_DIR = TEST_IMAGES_DIR / "full_library"

CHILLI_CLASSES = [
    "Chili__Bacterial_Spot",
    "Chili__Cercospora_Leaf_Spot",
    "Chili__Curl_Virus",
    "Chili__Healthy_Leaf",
    "Chili__Nutrition_Deficiency",
    "Chili__Powdery_Mildew",
    "Chili__White_Spot",
]

def copy_folder(src: Path, dst: Path, desc: str):
    print(f"Copying {desc}: {src} -> {dst}...", flush=True)
    dst.mkdir(parents=True, exist_ok=True)
    copied = 0
    for root, dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        target_dir = dst / rel
        target_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            src_file = Path(root) / f
            dst_file = target_dir / f
            if not dst_file.exists():
                shutil.copy2(src_file, dst_file)
                copied += 1
    print(f"  Done {desc}. Copied {copied} new files.", flush=True)

def main():
    # 1. Corn
    corn_src = Path(r"D:\499A Dataset\Corn\test")
    corn_dst = TEST_IMAGES_DIR / "corn_disease"
    copy_folder(corn_src, corn_dst, "Corn")

    # 2. Potato
    potato_src = Path(r"D:\499A Dataset\Potato\test")
    potato_dst = TEST_IMAGES_DIR / "potato_disease"
    copy_folder(potato_src, potato_dst, "Potato (to potato_disease)")
    copy_folder(potato_src, FULL_LIBRARY_DIR, "Potato (to full_library)")

    # 3. Brassica
    brassica_src = Path(r"D:\499A Dataset\Brassica\test")
    brassica_dst = TEST_IMAGES_DIR / "brassica_disease"
    copy_folder(brassica_src, brassica_dst, "Brassica (to brassica_disease)")
    copy_folder(brassica_src, FULL_LIBRARY_DIR, "Brassica (to full_library)")

    # 4. Chilli
    chilli_src = Path(r"D:\499A Dataset\Solanaceae\test")
    chilli_dst = TEST_IMAGES_DIR / "chilli_disease"
    for c in CHILLI_CLASSES:
        src_c = chilli_src / c
        if src_c.exists():
            copy_folder(src_c, chilli_dst / c, f"Chilli {c} (to chilli_disease)")
            copy_folder(src_c, FULL_LIBRARY_DIR / c, f"Chilli {c} (to full_library)")

    print("\nAll test sets copied into backend/ml_assets/vision/test_images/ successfully!", flush=True)

if __name__ == "__main__":
    main()
