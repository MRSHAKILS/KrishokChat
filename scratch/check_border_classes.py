import re

with open('scratch/old_section.html', encoding='utf-8') as f:
    s = f.read()

# find all class attributes
classes = re.findall(r'class="([^"]*)"', s)
border_classes = set()
for c in classes:
    for word in c.split():
        if 'border' in word:
            border_classes.add(word)

print("Border classes found in old section:")
for bc in sorted(border_classes):
    print(" ", bc)
