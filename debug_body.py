import docx
from docx.oxml.ns import qn
doc = docx.Document('JSPulse_OHMS_Merged_Internship_Report.docx')
body = doc.element.body
for idx, child in enumerate(body):
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        text = "".join(child.itertext()).strip()
        if 'Chapter 3' in text:
             print(f"Body index {idx}: tag={tag}, text={repr(text)}")
             pPr = child.get_or_add_pPr()
             pStyle = pPr.find(qn('w:pStyle'))
             if pStyle is not None:
                  val = pStyle.get(qn('w:val'))
                  print(f"   -> style val = {repr(val)}")
