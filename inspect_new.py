from docx import Document
from docx.oxml.ns import qn

doc = Document('JSPulse_OHMS_Report_NoBlanks.docx')

# Check what's around paras 70-77
for i in range(70, 77):
    if i < len(doc.paragraphs):
        p = doc.paragraphs[i]
        text = p.text.strip()[:80]
        style = p.style.name
        has_pb = any(br.get(qn('w:type')) == 'page' for br in p._element.findall('.//' + qn('w:br')))
        marker = ' [PAGE BREAK]' if has_pb else ''
        print(f'  Para {i} [{style}]: "{text}"{marker}')

print()
# Check first 10 paragraphs
for i in range(0, 10):
    p = doc.paragraphs[i]
    text = p.text.strip()[:80]
    style = p.style.name
    has_pb = any(br.get(qn('w:type')) == 'page' for br in p._element.findall('.//' + qn('w:br')))
    marker = ' [PAGE BREAK]' if has_pb else ''
    print(f'  Para {i} [{style}]: "{text}"{marker}')

print(f'\nTotal paragraphs: {len(doc.paragraphs)}')
# Count pages in chapters
headings = []
for i, p in enumerate(doc.paragraphs):
    if p.style.name == 'Heading 1':
        headings.append((i, p.text.strip()[:60]))
print(f'\nChapter headings found:')
for idx, txt in headings:
    print(f'  Para {idx}: {txt}')
