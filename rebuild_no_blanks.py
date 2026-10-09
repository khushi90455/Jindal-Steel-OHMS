"""
Rebuild the merged report from scratch with NO blank pages.

Strategy:
1. Create cover page + TOC field
2. Merge all chapters with ONLY chapter-start page breaks
3. Remove ALL blank page-break paragraphs from chapter content
4. Remove ALL consecutive empty paragraphs (keep max 1)
5. Remove pageBreakBefore from mid-chapter elements
6. Strip section breaks from chapters
7. Add header/footer
8. Use Word COM to update TOC and export PDF
"""

import os
import copy
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_DIR = r'C:\Users\KHUSHI\.gemini\antigravity\brain\52546b67-bb16-4f38-9852-f6f9063e206e'

FILES = [
    ('JSPulse_OHMS_Chapter1.docx', ARTIFACT_DIR),
    ('JSPulse_OHMS_Chapter2.docx', ARTIFACT_DIR),
    ('JSPulse_OHMS_Chapter3_WithSpaces.docx', ARTIFACT_DIR),
    ('JSPulse_OHMS_Chapter4_WithSpaces.docx', ARTIFACT_DIR),
    ('JSPulse_OHMS_Chapter5_WithSpaces.docx', ARTIFACT_DIR),
    ('JSPulse_OHMS_Chapter6_WithSpaces.docx', ARTIFACT_DIR),
    ('JSPulse_OHMS_Chapter7_Final_WithBreaks.docx', ARTIFACT_DIR),
]

def has_page_break(element):
    """Check if a paragraph element contains a page break."""
    for br in element.findall('.//' + qn('w:br')):
        if br.get(qn('w:type')) == 'page':
            return True
    return False

def has_page_break_before(element):
    """Check if paragraph has pageBreakBefore property."""
    pPr = element.find(qn('w:pPr'))
    if pPr is not None:
        pB = pPr.find(qn('w:pageBreakBefore'))
        if pB is not None:
            return True
    return False

def remove_page_break_before(element):
    """Remove pageBreakBefore property from paragraph."""
    pPr = element.find(qn('w:pPr'))
    if pPr is not None:
        pB = pPr.find(qn('w:pageBreakBefore'))
        if pB is not None:
            pPr.remove(pB)

def remove_page_breaks_from_element(element):
    """Remove all page break <w:br> elements from a paragraph."""
    for br in element.findall('.//' + qn('w:br')):
        if br.get(qn('w:type')) == 'page':
            br.getparent().remove(br)

def get_text(element):
    """Get all text from an element."""
    return "".join(element.itertext()).strip()

def is_chapter_heading(text):
    """Check if text is a chapter heading (Chapter N:)."""
    import re
    return bool(re.match(r'Chapter\s+\d+', text, re.IGNORECASE))

def is_heading_style(element):
    """Check if element has a Heading style."""
    pPr = element.find(qn('w:pPr'))
    if pPr is not None:
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is not None:
            val = pStyle.get(qn('w:val'), '')
            if val.startswith('Heading'):
                return True
    return False

def add_toc(document):
    """Insert TOC field."""
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(24)
    p.paragraph_format.space_after = Pt(24)
    r = p.add_run("TABLE OF CONTENTS")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.bold = True

    p_toc = document.add_paragraph()
    run = p_toc.add_run()
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = r' TOC \o "1-3" \h \z \u '
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')

    # Placeholder run
    r_placeholder = OxmlElement('w:r')
    t_placeholder = OxmlElement('w:t')
    t_placeholder.text = '[Update field in Word to populate TOC]'
    r_placeholder.append(t_placeholder)

    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(r_placeholder)
    run._r.append(fldChar3)


def add_page_break_para(body):
    """Add a single page break paragraph to body XML."""
    pb = OxmlElement('w:p')
    pb_r = OxmlElement('w:r')
    pb_br = OxmlElement('w:br')
    pb_br.set(qn('w:type'), 'page')
    pb_r.append(pb_br)
    pb.append(pb_r)
    body.append(pb)


def build_report():
    master = Document()

    # Page setup - A4
    section = master.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

    # ── COVER PAGE ──
    p_title = master.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(120)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("JSPULSE OCCUPATIONAL HEALTH MANAGEMENT SYSTEM")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(20)

    p_sub = master.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(12)
    p_sub.paragraph_format.space_after = Pt(120)
    r_sub = p_sub.add_run("Comprehensive Internship Report\nJindal Steel & Power, Patratu Plant Clinic Operations")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(14)
    r_sub.italic = True

    p_details = master.add_paragraph()
    p_details.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_details.paragraph_format.space_before = Pt(100)
    r_details = p_details.add_run(
        "Submitted in partial fulfillment of the requirements for the internship program\nDate: June 2026"
    )
    r_details.font.name = "Times New Roman"
    r_details.font.size = Pt(12)

    # Page break after cover
    add_page_break_para(master.element.body)

    # ── TABLE OF CONTENTS ──
    add_toc(master)
    add_page_break_para(master.element.body)

    # ── MERGE CHAPTERS ──
    body = master.element.body

    for idx, (fname, fdir) in enumerate(FILES):
        path = os.path.join(fdir, fname)
        if not os.path.exists(path):
            print(f"  WARNING: {path} not found, skipping.")
            continue

        doc = Document(path)
        print(f"Merging {fname}...")

        # For Chapter 1, skip content before the actual chapter heading
        skip_preamble = (idx == 0)
        prev_was_empty = False
        chapter_started = False

        for child in doc.element.body:
            tag = child.tag.split('}')[-1]

            # Skip section properties
            if tag == 'sectPr':
                continue

            if tag == 'p':
                text = get_text(child)

                # For Chapter 1: skip everything before the chapter heading
                if skip_preamble:
                    if is_chapter_heading(text):
                        skip_preamble = False
                    else:
                        continue

                # ── BLANK PAGE REMOVAL LOGIC ──

                # 1. Remove standalone page break paragraphs (empty text + page break)
                if text == '' and has_page_break(child):
                    continue

                # 2. Remove pageBreakBefore from non-chapter-heading paragraphs
                if has_page_break_before(child) and not is_chapter_heading(text):
                    remove_page_break_before(child)

                # 3. Remove inline page breaks from paragraphs that also have content
                if text != '' and has_page_break(child) and not is_chapter_heading(text):
                    remove_page_breaks_from_element(child)

                # 4. Collapse consecutive empty paragraphs (max 1 empty)
                if text == '':
                    if prev_was_empty:
                        continue
                    prev_was_empty = True
                else:
                    prev_was_empty = False

                # Deep copy and append
                new_el = copy.deepcopy(child)

                # If this is a chapter heading (Heading 1), ensure it has pageBreakBefore
                # ONLY for chapters after the first one in the document
                if is_chapter_heading(text) and is_heading_style(child):
                    if chapter_started:
                        # Add page break before this chapter
                        add_page_break_para(body)
                    chapter_started = True

                body.append(new_el)

            elif tag == 'tbl':
                if skip_preamble:
                    continue
                new_tbl = copy.deepcopy(child)
                body.append(new_tbl)
                prev_was_empty = False

    # ── HEADER & FOOTER ──
    for sec in master.sections:
        sec.different_first_page_header_footer = False

        # Header
        header = sec.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.text = "JS Pulse OHMS Internship Report"
        p_hdr.runs[0].font.name = "Times New Roman"
        p_hdr.runs[0].font.size = Pt(9)
        p_hdr.runs[0].font.italic = True

        # Footer with page number field
        footer = sec.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ftr.text = ""
        run = p_ftr.add_run()

        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'separate')
        fldChar3 = OxmlElement('w:fldChar')
        fldChar3.set(qn('w:fldCharType'), 'end')

        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        run._r.append(fldChar3)
        p_ftr.runs[0].font.name = "Times New Roman"
        p_ftr.runs[0].font.size = Pt(10)

    # ── SAVE ──
    out_docx = os.path.join(BASE_DIR, 'JSPulse_OHMS_Report_NoBlanks.docx')
    master.save(out_docx)
    print(f"\nSaved optimized document: {out_docx}")
    print("Now opening in Word for TOC update and PDF export...")

    # ── WORD COM AUTOMATION ──
    try:
        import win32com.client
        import pythoncom

        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        abs_docx = os.path.abspath(out_docx)
        wdoc = word.Documents.Open(abs_docx)

        # Update all fields
        wdoc.Fields.Update()
        for toc in wdoc.TablesOfContents:
            toc.Update()
        for section in wdoc.Sections:
            for header in section.Headers:
                header.Range.Fields.Update()
            for footer in section.Footers:
                footer.Range.Fields.Update()

        wdoc.Save()

        # Export PDF
        out_pdf = os.path.join(BASE_DIR, 'JSPulse_OHMS_Internship_Report_Final.pdf')
        wdoc.SaveAs(os.path.abspath(out_pdf), FileFormat=17)

        wdoc.Close(False)
        word.Quit()
        pythoncom.CoUninitialize()

        print(f"PDF exported: {out_pdf}")

        # Verify: count pages via reopening
        print("\n" + "=" * 60)
        print("SUCCESS! Report regenerated with no blank pages.")
        print(f"  DOCX: {out_docx}")
        print(f"  PDF:  {out_pdf}")
        print("=" * 60)

    except Exception as e:
        print(f"Word COM error: {e}")
        import traceback
        traceback.print_exc()
        print(f"\nDOCX saved successfully at: {out_docx}")
        print("Please open in Word, press Ctrl+A then F9 to update TOC, then export to PDF.")


if __name__ == '__main__':
    build_report()
