import docx
doc = docx.Document(r'C:\Users\KHUSHI\.gemini\antigravity\brain\52546b67-bb16-4f38-9852-f6f9063e206e\JSPulse_OHMS_Chapter2.docx')
for i, p in enumerate(doc.paragraphs):
    print(f'Para {i}: text={repr(p.text)}, xml_has_break={"type=\"page\"" in p._p.xml or "lastRenderedPageBreak" in p._p.xml}')
