import docx

def dump_docx(filepath, outpath):
    doc = docx.Document(filepath)
    fullText = []
    
    # Process paragraphs and tables in order if possible, or just dump paragraphs then tables
    # Since we want to read it, let's write paragraphs and tables.
    # To keep it simple, we can iterate over elements in the document body.
    # A standard way to preserve relative order of tables and paragraphs:
    for element in doc.element.body:
        if element.tag.endswith('p'):
            p = docx.text.paragraph.Paragraph(element, doc)
            if p.text.strip():
                fullText.append(p.text)
        elif element.tag.endswith('tbl'):
            t = docx.table.Table(element, doc)
            fullText.append("\n[TABLE START]")
            for row in t.rows:
                rowText = [cell.text.strip().replace("\n", " ") for cell in row.cells]
                # remove duplicates in cell text that python-docx sometimes yields for merged cells
                # but simple join is fine for reading
                fullText.append(" | ".join(rowText))
            fullText.append("[TABLE END]\n")
            
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write("\n".join(fullText))

dump_docx(r'_posts\데이터베이스 기초 정리.docx', r'scratch\db_base_full.txt')
dump_docx(r'_posts\반도체장비데이터관리 정리.docx', r'scratch\semicon_data_full.txt')

print("Dumped both files successfully.")
with open(r'scratch\db_base_full.txt', 'r', encoding='utf-8') as f:
    print("DB Base length:", len(f.read()))
with open(r'scratch\semicon_data_full.txt', 'r', encoding='utf-8') as f:
    print("Semicon Data length:", len(f.read()))
