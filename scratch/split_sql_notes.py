import os
import re

filepath = '_posts/2026-05-09-sql_notes.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's split content using regex that matches the H2 headers
# We find all matches of '^## 1. ...', '^## 2. ...', etc.
pattern = r'^##\s+(\d+)\.\s+(.*?)$'
matches = list(re.finditer(pattern, content, re.MULTILINE))

titles = {
    1: "01. 데이터베이스 개요 & 데이터 관리",
    2: "02. 데이터 모델링 & 데이터베이스 구조",
    3: "03. 키 & 무결성 제어",
    4: "04. SQL 개요 및 DDL (데이터 정의어)",
    5: "05. SQL DML (데이터 조작어)",
    6: "06. 고급 SQL 기능"
}

dates = {
    1: "2026-05-09",
    2: "2026-05-10",
    3: "2026-05-11",
    4: "2026-05-12",
    5: "2026-05-13",
    6: "2026-05-14"
}

front_matter_template = """---
layout: post
date: {date}
title: {title}
author: Voliti
category_name: sql
---

"""

# Extract each section's content
for idx, match in enumerate(matches):
    sec_num = int(match.group(1))
    start_pos = match.end()
    end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
    
    sec_content = content[start_pos:end_pos].strip()
    
    # Generate new post
    filename = f"{dates[sec_num]}-sql_notes_{sec_num:02d}.md"
    new_filepath = os.path.join('_posts', filename)
    
    fm = front_matter_template.format(date=dates[sec_num], title=titles[sec_num])
    
    # We can prepend a nice heading to the section if we want
    full_content = fm + "### " + titles[sec_num] + "\n\n" + sec_content
    
    with open(new_filepath, 'w', encoding='utf-8') as f_out:
        f_out.write(full_content)
    print(f"Created {filename}")

# Remove the original file
os.remove(filepath)
print(f"Deleted original {filepath}")
