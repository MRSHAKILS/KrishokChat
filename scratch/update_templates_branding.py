import os

templates_dir = "deploy/hf_space/templates"
files_updated = 0

for filename in os.listdir(templates_dir):
    if filename.endswith(".html") or filename.endswith(".rsc"):
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content.replace("কৃষক চ্যাট", "কৃষকটেক")
        new_content = new_content.replace("KrishokChat", "KrishokTech")
        new_content = new_content.replace("krishokchat", "krishoktech")

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            files_updated += 1
            print(f"Updated branding in {filename}")

print(f"Total files updated: {files_updated}")
