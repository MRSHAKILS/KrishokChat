import os
import shutil

repo_root = os.path.abspath(".")
src_static = os.path.join(repo_root, "frontend", ".next", "static")
dst_static = os.path.join(repo_root, "deploy", "hf_space", "static", "_next", "static")

if os.path.exists(dst_static):
    shutil.rmtree(dst_static)
os.makedirs(os.path.dirname(dst_static), exist_ok=True)
shutil.copytree(src_static, dst_static)
print(f"Copied static chunks to {dst_static}")

src_public = os.path.join(repo_root, "frontend", "public")
dst_public = os.path.join(repo_root, "deploy", "hf_space", "public")
os.makedirs(dst_public, exist_ok=True)

# Copy public assets
src_assets = os.path.join(src_public, "assets")
if os.path.exists(src_assets):
    dst_assets = os.path.join(dst_public, "assets")
    if os.path.exists(dst_assets):
        shutil.rmtree(dst_assets)
    shutil.copytree(src_assets, dst_assets)

src_packs = os.path.join(src_public, "packs")
if os.path.exists(src_packs):
    dst_packs = os.path.join(dst_public, "packs")
    if os.path.exists(dst_packs):
        shutil.rmtree(dst_packs)
    shutil.copytree(src_packs, dst_packs)

for item in os.listdir(src_public):
    src_p = os.path.join(src_public, item)
    if os.path.isfile(src_p):
        if not item.endswith(".gif") and not item.endswith(".mp4"):
            shutil.copy2(src_p, os.path.join(dst_public, item))
print(f"Copied public assets to {dst_public}")

# Copy templates
src_server = os.path.join(repo_root, "frontend", ".next", "server", "app")
dst_templates = os.path.join(repo_root, "deploy", "hf_space", "templates")
os.makedirs(dst_templates, exist_ok=True)
for f in os.listdir(src_server):
    if f.endswith(".html") or f.endswith(".rsc") or f.endswith(".body"):
        shutil.copy2(os.path.join(src_server, f), os.path.join(dst_templates, f))
print(f"Copied templates to {dst_templates}")
