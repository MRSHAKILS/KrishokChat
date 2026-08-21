import os
import sys
import time
from pathlib import Path
from huggingface_hub import HfApi

TOKEN = os.environ.get("HF_TOKEN")
REPO_ID = "RaiyanKhaan/KrishokChat-Advisory-System"
STAGING_DIR = Path(r"d:\KrishokChat Advisory System\hf_staging")

print(f"Starting upload of {STAGING_DIR} to https://huggingface.co/{REPO_ID} ...")
start_time = time.time()

api = HfApi(token=TOKEN)

try:
    future = api.upload_folder(
        folder_path=str(STAGING_DIR),
        repo_id=REPO_ID,
        repo_type="model",
        commit_message="Release complete KrishokChat multi-modal agricultural advisory and detection model suite",
    )
    elapsed = time.time() - start_time
    print(f"\nSUCCESS! Upload finished in {elapsed:.1f}s.")
    print(f"Repository URL: https://huggingface.co/{REPO_ID}")
except Exception as e:
    print(f"\nERROR during upload: {e}", file=sys.stderr)
    sys.exit(1)
