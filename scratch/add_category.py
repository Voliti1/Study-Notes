import os

posts_dir = '_posts'
for filename in os.listdir(posts_dir):
    if filename.endswith('.md') and 'python_notes' in filename:
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Locate front matter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            if 'category_name:' not in front_matter:
                # Add category_name: python
                # Ensure it ends with newline
                if not front_matter.endswith('\n'):
                    front_matter += '\n'
                front_matter += 'category_name: python\n'
                parts[1] = front_matter
                new_content = '---'.join(parts)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added category_name to {filename}")
            else:
                print(f"category_name already exists in {filename}")
