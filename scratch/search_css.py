import re

with open('assets/gitbook/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for selectors containing active or expanded and display them
for m in re.finditer(r'[^}]*?(?:active|expanded)[^{]*?\{[^}]*?\}', text):
    print(m.group(0).strip())
    print('='*50)
