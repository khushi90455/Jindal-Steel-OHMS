from docx import Document

doc = Document('JSPulse_OHMS_Report_NoBlanks.docx')

figures = []
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if 'Figure' in text and ('placeholder' in text.lower() or 'reserved' in text.lower() or 'insert' in text.lower() or 'space' in text.lower()):
        figures.append((i, text[:120]))
    elif text.lower().startswith('figure') and ':' in text:
        figures.append((i, text[:120]))
    elif '[' in text and 'Figure' in text and ']' in text:
        figures.append((i, text[:120]))

print(f"Found {len(figures)} figure references:\n")
for idx, txt in figures:
    print(f"  Para {idx}: {txt}")
