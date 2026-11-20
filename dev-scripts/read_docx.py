import sys
from docx import Document

doc = Document('/home/z/my-project/upload/1.docx')
print('=== PARAGRAPHS ===')
for p in doc.paragraphs:
    t = p.text.strip()
    if t:
        print(t)
print('\n=== TABLES ===')
for i, tbl in enumerate(doc.tables):
    print(f'--- table {i} ---')
    for row in tbl.rows:
        cells = [c.text.strip().replace('\n', ' / ') for c in row.cells]
        print(' | '.join(cells))
