with open(r'paper\EACL Final\experiments\ground_truth.yaml', encoding='utf-8') as f:
    lines = f.readlines()
line = lines[204]
print('Line 205:', repr(line))
print('Length:', len(line))
if len(line) > 108:
    print('Char at 108:', repr(line[108]))
    print('Context:', repr(line[100:120]))