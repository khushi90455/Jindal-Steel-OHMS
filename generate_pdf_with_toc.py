"""
Generate PDF from the merged Word report using MS Word COM automation.
Steps:
1. First, modify the .docx to insert a TOC field at the very beginning
2. Open in MS Word via COM
3. Update all fields (TOC, page numbers, cross-references)
4. Export to PDF
"""

import os
import sys
import time
import copy
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def insert_toc_field(doc):
    """Insert a Table of Contents field at the beginning of the document."""
    
    # Create a "Table of Contents" heading paragraph
    toc_title = OxmlElement('w:p')
    
    # Paragraph properties for centered heading
    pPr = OxmlElement('w:pPr')
    
    # Style = no TOC style pickup (use manual styling)
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center')
    pPr.append(jc)
    
    # Spacing after
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:after'), '480')
    spacing.set(qn('w:before'), '240')
    pPr.append(spacing)
    
    toc_title.append(pPr)
    
    # Run with "TABLE OF CONTENTS" text
    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    
    b = OxmlElement('w:b')
    rPr.append(b)
    
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '32')  # 16pt
    rPr.append(sz)
    
    szCs = OxmlElement('w:szCs')
    szCs.set(qn('w:val'), '32')
    rPr.append(szCs)
    
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    rPr.append(rFonts)
    
    run.append(rPr)
    
    t = OxmlElement('w:t')
    t.text = 'TABLE OF CONTENTS'
    run.append(t)
    
    toc_title.append(run)
    
    # Create the TOC field paragraph
    toc_para = OxmlElement('w:p')
    
    # Paragraph properties
    toc_pPr = OxmlElement('w:pPr')
    toc_para.append(toc_pPr)
    
    # Begin field char
    r1 = OxmlElement('w:r')
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    r1.append(fldChar1)
    toc_para.append(r1)
    
    # Field instruction: TOC with heading levels 1-3, hyperlinks, dot leaders
    r2 = OxmlElement('w:r')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = r' TOC \o "1-3" \h \z \u '
    r2.append(instrText)
    toc_para.append(r2)
    
    # Separate field char
    r3 = OxmlElement('w:r')
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    r3.append(fldChar2)
    toc_para.append(r3)
    
    # Placeholder text
    r4 = OxmlElement('w:r')
    r4_rPr = OxmlElement('w:rPr')
    r4_noProof = OxmlElement('w:noProof')
    r4_rPr.append(r4_noProof)
    r4.append(r4_rPr)
    t4 = OxmlElement('w:t')
    t4.text = '[Table of Contents - Update this field in Word]'
    r4.append(t4)
    toc_para.append(r4)
    
    # End field char
    r5 = OxmlElement('w:r')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r5.append(fldChar3)
    toc_para.append(r5)
    
    # Page break after TOC
    pb_para = OxmlElement('w:p')
    pb_pPr = OxmlElement('w:pPr')
    pb_para.append(pb_pPr)
    pb_r = OxmlElement('w:r')
    pb_br = OxmlElement('w:br')
    pb_br.set(qn('w:type'), 'page')
    pb_r.append(pb_br)
    pb_para.append(pb_r)
    
    # Insert at the very beginning of the document body
    body = doc.element.body
    first_element = body[0] if len(body) > 0 else None
    
    if first_element is not None:
        body.insert(0, pb_para)
        body.insert(0, toc_para)
        body.insert(0, toc_title)
    else:
        body.append(toc_title)
        body.append(toc_para)
        body.append(pb_para)
    
    return doc


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    src_docx = os.path.join(base_dir, 'JSPulse_OHMS_Merged_Internship_Report_Final.docx')
    toc_docx = os.path.join(base_dir, 'JSPulse_OHMS_Report_WithTOC.docx')
    out_pdf  = os.path.join(base_dir, 'JSPulse_OHMS_Internship_Report_Final.pdf')
    
    if not os.path.exists(src_docx):
        print(f"ERROR: Source file not found: {src_docx}")
        sys.exit(1)
    
    # Step 1: Insert TOC field into the Word document
    print("Step 1: Inserting TOC field into document...")
    doc = Document(src_docx)
    doc = insert_toc_field(doc)
    doc.save(toc_docx)
    print(f"  Saved document with TOC field: {toc_docx}")
    
    # Step 2: Use MS Word COM automation to update fields and export PDF
    print("Step 2: Opening in Microsoft Word via COM automation...")
    
    try:
        import win32com.client
        import pythoncom
    except ImportError:
        print("ERROR: pywin32 (win32com) is not installed.")
        print("Please install it with: pip install pywin32")
        sys.exit(1)
    
    pythoncom.CoInitialize()
    
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False  # Run in background
        word.DisplayAlerts = 0  # Suppress dialogs
        
        print("  Opening document in Word...")
        doc_path = os.path.abspath(toc_docx)
        wdoc = word.Documents.Open(doc_path)
        
        # Update all fields (this populates the TOC with page numbers)
        print("  Updating all fields (TOC, page numbers, cross-references)...")
        
        # Update fields in the main document body
        wdoc.Fields.Update()
        
        # Update TOC specifically
        for toc in wdoc.TablesOfContents:
            toc.Update()
        
        # Update fields in headers and footers
        for section in wdoc.Sections:
            for header in section.Headers:
                header.Range.Fields.Update()
            for footer in section.Footers:
                footer.Range.Fields.Update()
        
        # Save the updated Word document
        print("  Saving updated Word document...")
        wdoc.Save()
        
        # Export to PDF
        print(f"  Exporting to PDF: {out_pdf}")
        # wdFormatPDF = 17
        wdoc.SaveAs(os.path.abspath(out_pdf), FileFormat=17)
        
        print("  Closing document...")
        wdoc.Close(False)
        
        print(f"\n{'='*60}")
        print(f"SUCCESS! PDF generated with complete Table of Contents.")
        print(f"  Word file: {toc_docx}")
        print(f"  PDF file:  {out_pdf}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"ERROR during Word COM automation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if word:
            try:
                word.Quit()
            except:
                pass
        pythoncom.CoUninitialize()


if __name__ == '__main__':
    main()
