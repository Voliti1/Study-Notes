import os
import re

site_dir = "_site"
for filename in os.listdir(site_dir):
    if filename.endswith(".html") and "python_notes" in filename:
        filepath = os.path.join(site_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            
        start_idx = html.find('<ul class="summary">')
        if start_idx == -1:
            print(f"{filename}: No summary list found")
            continue
            
        # Slicing the sidebar from the start of the summary ul to the end of the summary ul.
        # Since there are nested uls, we need to count to find the matching closing tag.
        idx = start_idx + len('<ul class="summary">')
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
                
        sidebar_html = html[start_idx:idx]
        
        ul_open = sidebar_html.count('<ul')
        ul_close = sidebar_html.count('</ul>')
        li_open = sidebar_html.count('<li')
        li_close = sidebar_html.count('</li>')
        
        balance_ul = ul_open - ul_close
        balance_li = li_open - li_close
        
        print(f"{filename}: UL diff = {balance_ul} (open={ul_open}, close={ul_close}), LI diff = {balance_li} (open={li_open}, close={li_close})")
