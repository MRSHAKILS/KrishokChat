#!/usr/bin/env python3
"""KrishokChat ML Suite — Hugging Face Model Hub Uploader.

Uploads the clean, folderized `backend_models` directory to:
    https://huggingface.co/RaiyanKhaan/KrishokChat-Advisory-System

Usage:
    # Option 1: Using environment variable HF_TOKEN
    export HF_TOKEN="hf_..."
    python upload_to_huggingface.py

    # Option 2: Passing token as argument
    python upload_to_huggingface.py --token hf_...
"""

import os
import sys
import time
import argparse
from pathlib import Path

try:
    from huggingface_hub import HfApi, create_repo
except ImportError:
    print("Error: huggingface_hub is required. Install via: pip install huggingface_hub")
    sys.exit(1)

REPO_ID = "RaiyanKhaan/KrishokTech-Models"
MODELS_DIR = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Upload backend models to Hugging Face Hub")
    parser.add_argument("--token", type=str, default=os.environ.get("HF_TOKEN"), help="Hugging Face User Access Token (Write)")
    parser.add_argument("--repo-id", type=str, default=REPO_ID, help="Target Hugging Face repository ID")
    parser.add_argument("--private", action="store_true", help="Set repository to private if creating new")
    args = parser.parse_args()

    token = args.token
    if not token:
        print("=" * 70)
        print(" Hugging Face Access Token Required!")
        print("=" * 70)
        print("Please provide a token with 'Write' permissions via:")
        print("  1. --token argument: python upload_to_huggingface.py --token <HF_TOKEN>")
        print("  2. Set environment variable: $env:HF_TOKEN = '<HF_TOKEN>' (PowerShell)")
        print("  3. Or run 'huggingface-cli login'")
        print("=" * 70)
        token = input("Enter your Hugging Face Write Token: ").strip()

    if not token:
        print("Error: No token provided. Aborting upload.")
        sys.exit(1)

    print(f"\nAuthenticating with Hugging Face Hub as target repo '{args.repo_id}' ...")
    api = HfApi(token=token)

    try:
        api.create_repo(repo_id=args.repo_id, repo_type="model", private=args.private, exist_ok=True)
        print(f"Verified repository: https://huggingface.co/{args.repo_id}")
    except Exception as e:
        print(f"Notice during repository check: {e}")

    print(f"\nUploading contents of:\n  {MODELS_DIR}\nto:\n  https://huggingface.co/{args.repo_id} ...\n")
    start_time = time.time()

    try:
        api.upload_folder(
            folder_path=str(MODELS_DIR),
            repo_id=args.repo_id,
            repo_type="model",
            commit_message="Release KrishokChat backend ML suite: YOLO26 vision models and 5-fold soil moisture regression",
            ignore_patterns=["__pycache__/*", "*.pyc", ".git/*", ".DS_Store"],
        )
        elapsed = time.time() - start_time
        print("\n" + "=" * 70)
        print(f" SUCCESS! All models uploaded in {elapsed:.1f}s.")
        print(f" Public Model URL: https://huggingface.co/{args.repo_id}")
        print("=" * 70)
    except Exception as exc:
        print(f"\nUpload failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
