with open("_site/2026-05-01-python_notes_01_01_number.html", "r", encoding="utf-8") as f:
    html1 = f.read()
with open("_site/2026-05-02-python_notes_01_02_sequence.html", "r", encoding="utf-8") as f:
    html2 = f.read()

def get_sidebar(html):
    start = html.find('<ul class="summary">')
    # find matching outer ul tag
    idx = start + len('<ul class="summary">')
    ul_count = 1
    while ul_count > 0 and idx < len(html):
        if html[idx:idx+3] == "<ul":
            ul_count += 1
            idx += 3
        elif html[idx:idx+5] == "</ul>":
            ul_count -= 1
            idx += 5
        else:
            idx += 1
    return html[start:idx]

sb1 = get_sidebar(html1)
sb2 = get_sidebar(html2)

# Normalize active classes and page titles so we can see structure diff
sb1_norm = re.sub(r'active|expanded', '', sb1)
sb2_norm = re.sub(r'active|expanded', '', sb2)

print("Are normalized sidebars equal?", sb1_norm == sb2_norm)
if sb1_norm != sb2_norm:
    print("Diff in normalized sidebars exists!")
    # Show length
    print("Len 1:", len(sb1_norm), "Len 2:", len(sb2_norm))
