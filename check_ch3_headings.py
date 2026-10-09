import docx
doc = docx.Document(r'C:\Users\KHUSHI\.gemini\antigravity\brain\52546b67-bb16-4f38-9852-f6f9063e206e\JSPulse_OHMS_Chapter3_WithSpaces.docx')
for i, p in enumerate(doc.paragraphs):
    if p.style.name.startswith('Heading'):
         print(f'{i}: [{p.style.name}] {repr(p.text)}')
