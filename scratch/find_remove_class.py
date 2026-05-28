import re

with open('assets/gitbook/theme.js', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'\.removeClass\([\'"]active[\'"]\)', text):
    start = max(0, m.start() - 150)
    end = min(len(text), m.end() + 150)
    print(f'Match at {m.start()}:\n{text[start:end]}')
    print('='*50)
