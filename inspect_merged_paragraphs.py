import docx
doc = docx.Document('JSPulse_OHMS_Merged_Internship_Report.docx')
for i, p in enumerate(doc.paragraphs[:100]):
    if 'Chapter 3' in p.text:
         print(f'{i}: text={repr(p.text)}, style={repr(p.style.name)}')
