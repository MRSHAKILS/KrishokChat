import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import load_corpus, utf8_stdout, LOGS_DIR
utf8_stdout()

recs = load_corpus()
print("records:", len(recs))
r = next(x for x in recs if x["disease_bn"] and x["dosage_text"])
print(json.dumps(r, ensure_ascii=False, indent=1)[:3000])
print("\n=== normalization ops ===")
rep = json.loads((LOGS_DIR / "cleaning_report.json").read_text(encoding="utf-8"))
print(json.dumps(rep["normalization_ops"], ensure_ascii=False, indent=1))
print(json.dumps(rep["problem_type_distribution"], ensure_ascii=False, indent=1))
print("\n=== safety sample ===")
s = next(x for x in recs if x["safety_warnings"])
print(json.dumps(s["safety_warnings"], ensure_ascii=False, indent=1)[:800])
print("\n=== legal sample ===")
for x in recs:
    if x["legal_status"].startswith("restricted"):
        print(x["legal_status"][:400]); break
