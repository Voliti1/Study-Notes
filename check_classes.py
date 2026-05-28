import os
import re

site_dir = "_site"
for filename in os.listdir(site_dir):
    if filename.endswith(".html") and ("python_notes" in filename or filename == "index.html" or "python" in filename):
        filepath = os.path.join(site_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            
        match = re.search(r'<li class="([^"]*collapsible-category[^"]*)"', html)
        if match:
            print(f"{filename}: Class = '{match.group(1)}'")
        else:
            print(f"{filename}: collapsible-category not found")
