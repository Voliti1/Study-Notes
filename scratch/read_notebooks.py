import json
import os

def parse_ipynb(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    output_lines = []
    cells = notebook.get('cells', [])
    for idx, cell in enumerate(cells):
        cell_type = cell.get('cell_type')
        source = "".join(cell.get('source', []))
        
        output_lines.append(f"=== CELL {idx} ({cell_type}) ===")
        output_lines.append(source)
        
        # If it's a code cell, look at outputs
        if cell_type == 'code':
            outputs = cell.get('outputs', [])
            for out_idx, out in enumerate(outputs):
                out_type = out.get('output_type')
                output_lines.append(f"  --- OUTPUT {out_idx} ({out_type}) ---")
                if 'text' in out:
                    output_lines.append("".join(out.get('text', [])))
                elif 'data' in out:
                    data = out.get('data', {})
                    if 'text/plain' in data:
                        output_lines.append("".join(data.get('text/plain', [])))
    return "\n".join(output_lines)

text1 = parse_ipynb('../1. 선형회귀분석_공유용.ipynb')
with open('scratch/notebook1_dump.txt', 'w', encoding='utf-8') as f:
    f.write(text1)

text2 = parse_ipynb('../2. 다중회귀분석_공부시간시험성적_공유용.ipynb')
with open('scratch/notebook2_dump.txt', 'w', encoding='utf-8') as f:
    f.write(text2)

print("Dumped notebook contents to scratch directory.")
print("Notebook 1 length:", len(text1))
print("Notebook 2 length:", len(text2))
