from huggingface_hub import HfApi

api = HfApi(token="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")

print("Starting upload via HfApi.upload_folder...")
future = api.upload_folder(
    folder_path="deploy/hf_space",
    repo_id="RaiyanKhaan/KrishokTech",
    repo_type="space",
    commit_message="Fix Task-First decision cards UI: eliminate black borders, apply warm Field Notebook bone borders, surface-lift shadows, and paper gradients",
    ignore_patterns=[".git", ".git/**", "__pycache__", "__pycache__/**", "*.pyc"]
)
print("Upload result:", future)
