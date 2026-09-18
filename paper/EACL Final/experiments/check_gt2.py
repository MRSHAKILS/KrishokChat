import yaml
with open(r'paper\EACL Final\experiments\ground_truth.yaml', encoding='utf-8') as f:
    gt = yaml.safe_load(f)
print('Total experiments:', len(gt['experiments']))
for k, v in sorted(gt['experiments'].items()):
    print(f'  {k}: {v.get("status")}')