"""
Batch export trained YOLO .pt models to ONNX format.

Usage:
    python scripts/export_yolo_models.py --input-dir backend/ml_assets/yolo --output-dir backend/ml_assets/yolo

Prerequisites:
    - .pt weight files placed in backend/ml_assets/yolo/
    - ultralytics installed in backend environment
"""

import argparse
from pathlib import Path

from ultralytics import YOLO


def export_model(pt_path: Path, output_dir: Path, imgsz: int = 640) -> Path:
    """Export a single .pt model to ONNX."""
    print(f"Loading {pt_path.name}...")
    model = YOLO(str(pt_path))

    print(f"Exporting to ONNX (imgsz={imgsz})...")
    export_path = model.export(
        format="onnx",
        imgsz=imgsz,
        simplify=True,
        opset=17,
        dynamic=False,
    )

    exported = Path(export_path)
    print(f"  -> {exported.name} ({exported.stat().st_size / 1e6:.1f} MB)")
    return exported


def main():
    parser = argparse.ArgumentParser(description="Export YOLO .pt models to ONNX")
    parser.add_argument("--input-dir", type=Path, required=True, help="Directory containing .pt files")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory to save .onnx files")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size (default: 640)")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    pt_files = sorted(args.input_dir.glob("*.pt"))
    if not pt_files:
        print(f"No .pt files found in {args.input_dir}")
        return

    print(f"Found {len(pt_files)} model(s) to export")
    results = []
    for pt_file in pt_files:
        try:
            onnx_path = export_model(pt_file, args.output_dir, args.imgsz)
            results.append((pt_file.name, onnx_path.name, True, None))
        except Exception as e:
            print(f"  FAILED: {pt_file.name} — {e}")
            results.append((pt_file.name, None, False, str(e)))

    print("\n" + "=" * 60)
    print("EXPORT SUMMARY")
    print("=" * 60)
    for name, onnx, ok, err in results:
        status = "OK" if ok else f"FAILED: {err}"
        print(f"  {name} -> {onnx or '(none)'} [{status}]")


if __name__ == "__main__":
    main()
