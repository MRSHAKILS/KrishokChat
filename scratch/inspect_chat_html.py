import re

content = open("deploy/hf_space/templates/chat.html", encoding="utf-8").read()
static_matches = re.findall(r'/_next/static/[^"\'\s>]+', content)
print("Count of /_next/static matches in chat.html:", len(static_matches))
for m in static_matches[:10]:
    print(" ", m)
