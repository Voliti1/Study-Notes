from bs4 import BeautifulSoup
import difflib

def get_sidebar_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    summary = soup.find('ul', class_='summary')
    return summary.prettify()

sb1 = get_sidebar_html('_site/2026-05-01-python_notes_01_01_number.html')
sb2 = get_sidebar_html('_site/2026-05-02-python_notes_01_02_sequence.html')

# Normalize the active classes and titles/links specific to each file
import re
sb1 = re.sub(r'active', '', sb1)
sb2 = re.sub(r'active', '', sb2)
sb1 = re.sub(r'2026-05-01-python_notes_01_01_number', 'PLACEHOLDER', sb1)
sb2 = re.sub(r'2026-05-02-python_notes_01_02_sequence', 'PLACEHOLDER', sb2)
sb1 = re.sub(r'01_01\. 숫자형과 연산자', 'TITLE_PLACEHOLDER', sb1)
sb2 = re.sub(r'01_02\. 시퀀스 자료형', 'TITLE_PLACEHOLDER', sb2)

diff = difflib.unified_diff(
    sb1.splitlines(),
    sb2.splitlines(),
    fromfile='number.html',
    tofile='sequence.html',
    lineterm=''
)

for line in diff:
    print(line)
