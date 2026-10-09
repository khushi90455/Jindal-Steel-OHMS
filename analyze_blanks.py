from docx import Document
from docx.oxml.ns import qn

doc = Document('JSPulse_OHMS_Merged_Internship_Report_Final.docx')

blank_count = 0
page_break_count = 0
empty_para_count = 0
section_break_count = 0

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    xml_str = p._element.xml

    # Count page breaks (w:br with type=page)
    has_page_break = False
    for br in p._element.findall('.//' + qn('w:br')):
        btype = br.get(qn('w:type'))
        if btype == 'page':
            has_page_break = True

    if has_page_break:
        page_break_count += 1
        if text == '':
            blank_count += 1
            print(f'  Para {i}: BLANK PAGE BREAK')

    # Count pageBreakBefore
    pPr = p._element.find(qn('w:pPr'))
    if pPr is not None:
        pB = pPr.find(qn('w:pageBreakBefore'))
        if pB is not None:
            print(f'  Para {i}: pageBreakBefore => {text[:60]}')

    # Count empty paragraphs with no content and no break
    if text == '' and not has_page_break:
        empty_para_count += 1

# Count section breaks
for i, sec in enumerate(doc.sections):
    secPr = sec._sectPr
    pgtype = secPr.find(qn('w:type'))
    if pgtype is not None:
        print(f'  Section {i}: type={pgtype.get(qn("w:val"))}')
    section_break_count += 1

print(f'\nTotal paragraphs: {len(doc.paragraphs)}')
print(f'Page breaks (w:br type=page): {page_break_count}')
print(f'Blank page break paras: {blank_count}')
print(f'Empty paragraphs (no break): {empty_para_count}')
print(f'Sections: {section_break_count}')
