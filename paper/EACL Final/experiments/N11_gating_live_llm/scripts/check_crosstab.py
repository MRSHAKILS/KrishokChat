import json
import sys

det = {r['id']: r for r in [json.loads(l) for l in open(r'paper\EACL Final\experiments\results\n01b_records_20260917.jsonl', encoding='utf-8')]}
live = {r['id']: r for r in [json.loads(l) for l in open(r'paper\EACL Final\experiments\results\n11_live_gating_20260917.jsonl', encoding='utf-8')]}

crosstab = {}
rows_to_review = []
for id_ in det:
    if id_ in live:
        lh = live[id_].get('halted')
        dh = det[id_].get('gated_halted')
        key = (lh, dh)
        crosstab[key] = crosstab.get(key, 0) + 1
        if lh == False and dh == True:
            rows_to_review.append((id_, live[id_], det[id_]))

print('crosstab:', crosstab)
print('live_pass_det_halt:', len(rows_to_review))

# write to file to avoid encoding issues
with open('crosstab_output.txt', 'w', encoding='utf-8') as f:
    f.write('crosstab: ' + str(crosstab) + '\n')
    f.write('live_pass_det_halt: ' + str(len(rows_to_review)) + '\n\n')
    for id_, l, d in rows_to_review:
        f.write(f'ID: {id_}\n')
        live_ans = str(l.get("answer_preview")) if l.get("answer_preview") else "NONE"
        det_ans = str(d.get("gated_answer_preview")) if d.get("gated_answer_preview") else "NONE"
        f.write(f'  LIVE: tier={l.get("tier")}, answer={live_ans[:150]}\n')
        f.write(f'  DET:  tier={d.get("gated_tier")}, answer={det_ans[:150]}\n')
        f.write('\n')

print('written to crosstab_output.txt')