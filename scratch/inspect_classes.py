import re

content = open('frontend/src/app/(marketing)/page.tsx', encoding='utf-8').read()
matches = re.findall(r'className=["\'][^"\']*(?:surface-lift|rule)[^"\']*["\']', content)
for m in matches[:15]:
    print(m)
