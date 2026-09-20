import re

with open('deploy/hf_space/templates/index.html', encoding='utf-8') as f:
    html = f.read()

start_marker = 'কৃষক সিদ্ধান্ত কেন্দ্র • Task-First Decisions'
idx = html.find(start_marker)
sec_start = html.rfind('<section', 0, idx)
sec_end = html.find('</section>', idx) + len('</section>')

print(f"Section length: {sec_end - sec_start}")
section_html = html[sec_start:sec_end]
with open('scratch/old_section.html', 'w', encoding='utf-8') as f_out:
    f_out.write(section_html)

print("Wrote scratch/old_section.html successfully")
