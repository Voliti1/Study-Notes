import os
import re

files = [
    '_site/sql/index.html', 
    '_site/2026-05-09-sql_notes.html', 
    '_site/2026-05-01-python_notes_01_01_number.html',
    '_site/2026-05-02-python_notes_01_02_sequence.html',
    '_site/index.html'
]

for f in files:
    exists = os.path.exists(f)
    print(f'{f} exists:', exists)
    if exists:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f'Checking {f}:')
        
        # 1. Check Python category LI
        py_match = re.search(r'<li class="([^"]*collapsible-category[^"]*)"[^>]*data-level="([^"]*)"[^>]*data-path="[^"]*python/"', content)
        if py_match:
            print(f'  Python category: Class = "{py_match.group(1)}", data-level = "{py_match.group(2)}"')
        else:
            print('  Python category NOT found!')
            
        # 2. Check SQL category LI
        sql_match = re.search(r'<li class="([^"]*collapsible-category[^"]*)"[^>]*data-level="([^"]*)"[^>]*data-path="[^"]*sql/"', content)
        if sql_match:
            print(f'  SQL category: Class = "{sql_match.group(1)}", data-level = "{sql_match.group(2)}"')
        else:
            print('  SQL category NOT found!')
            
        # 3. Check some posts' data-levels
        posts_levels = re.findall(r'<li class="chapter[^"]*"[^>]*data-level="([^"]*)"[^>]*data-path="([^"]*)"', content)
        print('  Some posts levels:')
        for level, path in posts_levels[:12]:
            if 'python_notes' in path or 'sql_notes' in path:
                print(f'    Path: {path.split("/")[-1]} -> data-level: {level}')
        print('-' * 40)
