import re

content = open('deploy/hf_space/static/_next/static/chunks/0vn0qenfr622s.css', encoding='utf-8').read()

with open('scratch/patch_index_html.py', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'new_section = """(.*?)"""', text, re.DOTALL)
new_section = m.group(1)

classes = set()
for c in re.findall(r'class="([^"]*)"', new_section):
    for word in c.split():
        classes.add(word)

missing = []
for c in sorted(classes):
    # CSS class selector escape
    # in CSS, characters like / : [ ] are escaped with \
    css_sel = c.replace('/', '\\/').replace(':', '\\:').replace('[', '\\[').replace(']', '\\]').replace('.', '\\.').replace('%', '\\%').replace(',', '\\,')
    if ('.' + css_sel) not in content and ('.' + c) not in content:
        missing.append(c)

print(f"Total classes: {len(classes)}")
print(f"Missing classes ({len(missing)}):")
for m in missing:
    print(" ", m)
