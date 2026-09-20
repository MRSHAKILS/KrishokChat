import os

static_dir = "deploy/hf_space/static/_next/static"
files_updated = 0

for root, dirs, files in os.walk(static_dir):
    for filename in files:
        if filename.endswith(".js"):
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            new_content = content.replace("কৃষক চ্যাট", "কৃষকটেক")
            new_content = new_content.replace("KrishokChat", "KrishokTech")
            new_content = new_content.replace("krishokchat", "krishoktech")

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                files_updated += 1
                print(f"Replaced branding in JS chunk: {filename}")

print(f"Total JS chunk files updated: {files_updated}")
