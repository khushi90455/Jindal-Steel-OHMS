import docx
doc = docx.Document(r'C:\Users\KHUSHI\.gemini\antigravity\brain\52546b67-bb16-4f38-9852-f6f9063e206e\JSPulse_OHMS_Chapter1.docx')
for i, p in enumerate(doc.paragraphs):
    print(f'Para {i}: text={repr(p.text)}')
    if 'w:br' in p._p.xml:
         print(f'   -> has w:br in XML')
    if 'w:pageBreakBefore' in p._p.xml:
         print(f'   -> has w:pageBreakBefore in XML')
