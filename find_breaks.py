import docx
doc = docx.Document('JSPulse_OHMS_Merged_Internship_Report.docx')
for i, p in enumerate(doc.paragraphs):
    p_xml = p._p.xml
    if 'type="page"' in p_xml:
         print(f'Hard Page Break at para {i}: {repr(p.text[:40])}')
