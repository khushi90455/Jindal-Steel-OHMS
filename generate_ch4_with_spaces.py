import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def setup_doc(doc):
    for section in doc.sections:
        section.page_width    = Inches(8.27)
        section.page_height   = Inches(11.69)
        section.top_margin    = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin   = Inches(1.0)
        section.right_margin  = Inches(1.0)

    ns = doc.styles['Normal']
    ns.font.name = 'Times New Roman'
    ns.font.size = Pt(12)
    for i in range(1, 5):
        hs = doc.styles[f'Heading {i}']
        hs.font.name = 'Times New Roman'
        hs.font.color.rgb = RGBColor(0, 0, 0)
        hs.font.bold = True

def para(doc, text, space_before=0, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing  = 1.5
    p.paragraph_format.space_before  = Pt(space_before)
    p.paragraph_format.space_after   = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def code_block(doc, lines_text, caption_text=None):
    """Monospaced indented code block."""
    for line in lines_text.strip().split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing  = 1.0
        p.paragraph_format.space_before  = Pt(0)
        p.paragraph_format.space_after   = Pt(0)
        p.paragraph_format.left_indent   = Inches(0.5)
        run = p.add_run(line)
        run.font.name = 'Courier New'
        run.font.size = Pt(9)
    if caption_text:
        c = doc.add_paragraph(caption_text)
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.space_before = Pt(4)
        c.paragraph_format.space_after  = Pt(12)
        cr = c.runs[0]
        cr.italic = True
        cr.font.size = Pt(10)
        cr.font.name = 'Times New Roman'

def fig_label(doc, fig_num, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(f'{fig_num}: {title}')
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    return p

def blank_diagram_space(doc, height_inches=5.0):
    """Fixed-height grey dashed-border table cell to reserve diagram space."""
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    cell = table.rows[0].cells[0]

    # Fixed row height
    tr   = cell._tc.getparent()
    trPr = OxmlElement('w:trPr')
    trH  = OxmlElement('w:trHeight')
    trH.set(qn('w:val'),   str(int(height_inches * 1440)))
    trH.set(qn('w:hRule'), 'exact')
    trPr.append(trH)
    tr.insert(0, trPr)

    # Light grey fill
    tcPr = cell._tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  'F0F0F0')
    tcPr.append(shd)

    # Dashed border
    tcBdr = OxmlElement('w:tcBorders')
    for side in ('top', 'left', 'bottom', 'right'):
        bdr = OxmlElement(f'w:{side}')
        bdr.set(qn('w:val'),   'dashDotStroked')
        bdr.set(qn('w:sz'),    '12')
        bdr.set(qn('w:space'), '0')
        bdr.set(qn('w:color'), '808080')
        tcBdr.append(bdr)
    tcPr.append(tcBdr)

    # Label inside
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    run = p.add_run('[Space reserved for diagram — insert figure here]')
    run.font.name  = 'Times New Roman'
    run.font.size  = Pt(10)
    run.italic     = True
    run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

    after = doc.add_paragraph()
    after.paragraph_format.space_before = Pt(6)
    after.paragraph_format.space_after  = Pt(8)

def sub_caption(doc, text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(14)
    r = p.runs[0]
    r.italic = True
    r.font.size = Pt(10)
    r.font.name = 'Times New Roman'

def insert_figure(doc, fig_num, title, height_inches=5.0, caption_text=None):
    fig_label(doc, fig_num, title)
    blank_diagram_space(doc, height_inches)
    if caption_text:
        sub_caption(doc, caption_text)


# ═══════════════════════════════════════════════════════════════
def main():
    doc = Document()
    setup_doc(doc)

    # ──────────────────────────────────────────────────────────
    # CHAPTER 4 TITLE
    # ──────────────────────────────────────────────────────────
    doc.add_heading('Chapter 4: Implementation Deep-Dive and Algorithms', level=1)

    # ──────────────────────────────────────────────────────────
    # 4.1  Custom IndexedDB Wrapper — sheetDB.js
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.1 Custom IndexedDB Wrapper — sheetDB.js', level=2)

    para(doc, "The sheetDB.js module is the most performance-critical and architecturally significant component in the entire JS Pulse OHMS codebase. It serves as the exclusive data access layer for all clinical operations, providing a high-level, promise-based API that abstracts the considerable complexity of the raw IndexedDB interface. The design motivation for building a custom wrapper, rather than adopting an existing library such as Dexie.js or idb, was driven by the need for precise control over transaction lifecycle management, connection pooling behaviour, and error recovery strategies tailored to the industrial deployment environment at the JSP Patratu plant.")
    para(doc, "At its core, sheetDB.js manages IndexedDB connections through a single module-level variable (dbConnection) that is initialised once and reused for all subsequent operations. The openDB function first checks whether dbConnection is already populated; if so, it resolves immediately without incurring any I/O overhead. If not, it calls indexedDB.open(DB_NAME, DB_VERSION) and attaches three event handlers: onupgradeneeded (which creates object stores and indexes if they do not exist or if the schema version has incremented), onsuccess (which stores the opened database reference in dbConnection and resolves the Promise), and onerror (which rejects the Promise and logs the failure for the global error handler). This connection-pooling pattern ensures that the application never opens more than one concurrent IndexedDB connection, preventing resource contention on low-specification clinic workstations.")
    para(doc, "Write operations are wrapped in explicit readwrite transactions using the IndexedDB put() method, which performs an upsert: if a record with the given primary key already exists, it is replaced; if not, a new record is inserted. This behaviour is essential for the OPD module, where a patient record may be updated multiple times during a single consultation (first with vitals, then with diagnosis, then with the final prescription). Each put() call within sheetDB.js wraps the operation in a Promise that resolves on the transaction's oncomplete event, ensuring that the Promise does not resolve until the data has been durably written to disk, not merely buffered in memory.")
    para(doc, "The bulk write operation implemented in sheetDB.js is critical for performance during data import operations. Without batching, inserting 10,000 records would require 10,000 separate transactions, each incurring its own disk-flush overhead. With batching, all records are inserted within a single readwrite transaction, reducing the total I/O cost to a single disk flush and improving import performance by one to two orders of magnitude. The error recovery strategy classifies failures as recoverable (triggering a background cleanup that purges expired log entries) or non-recoverable (triggering an emergency IPC call to write a JSON backup to the Windows file system via the Electron bridge).")

    code_block(doc, """// sheetDB.js — Core Connection Pool
const DB_NAME = 'JSPulseOHMS_DB';
const DB_VERSION = 3;
let dbConnection = null;

const openDB = () => new Promise((resolve, reject) => {
    if (dbConnection) { resolve(dbConnection); return; }
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
        const db = e.target.result;
        ['patient_visits','med_stock','dispense_log'].forEach(store => {
            if (!db.objectStoreNames.contains(store))
                db.createObjectStore(store, { keyPath: 'id' });
        });
    };
    req.onsuccess = (e) => { dbConnection = e.target.result; resolve(dbConnection); };
    req.onerror   = (e) => reject(e.target.error);
});""", "Code Listing 4.1: sheetDB.js Core Connection Pooling and Schema Initialisation")

    # ──────────────────────────────────────────────────────────
    # 4.2  DOM Virtualization Algorithm
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.2 DOM Virtualization Algorithm for Medical Spreadsheets', level=2)

    insert_figure(doc,
        fig_num='Figure 4.1',
        title='DOM Viewport Virtualization Row Calculation Sequence Diagram',
        height_inches=5.0,
        caption_text='Figure 4.1: Sequence diagram showing the row visibility calculation, spacer height computation, and DOM node management in ExcelGrid.jsx')

    para(doc, "The medical spreadsheet component (ExcelGrid.jsx) is the primary data interaction surface in JS Pulse OHMS, used by clinical staff to view, edit, and manage thousands of patient records, pharmaceutical inventory entries, and dispensing logs. Rendering this volume of data using standard React rendering would create tens of thousands of DOM nodes, overwhelming the browser's layout engine and causing severe performance degradation including dropped frames, sluggish scrolling, and unresponsive user input on the clinic's workstation computers.")
    para(doc, "To solve this challenge, ExcelGrid.jsx implements a custom DOM virtualization algorithm. The core principle is simple but powerful: instead of rendering all rows in the dataset, the algorithm calculates which rows are currently visible within the user's viewport and renders only those rows. Rows above the visible area are replaced by a single top spacer div whose height equals the combined height of all hidden rows above, and rows below are replaced by a bottom spacer div. This creates the illusion of a fully rendered scrollable grid while maintaining a constant, minimal number of actual DOM nodes, regardless of the total dataset size.")
    para(doc, "The algorithm runs inside a React useMemo hook so that the visible-row calculations are only recomputed when the dataset, row heights array, scroll position, or container dimensions change. For each row, the algorithm accumulates a running offset by summing all preceding row heights. A row is included in the visible set if its offset falls within the window defined by (scrollTop minus a 150-pixel buffer) to (scrollTop plus containerHeight plus a 150-pixel buffer). The 150-pixel overscan buffer ensures that rows are pre-rendered just before they enter the visible viewport, eliminating visible content-popping during fast scrolling. Without virtualization, a 5,000-row dataset with 15 columns would create 75,000 DOM cells. With virtualization, only 30 to 50 rows are rendered at any time, reducing the active DOM count to roughly 450 to 750 nodes.")

    code_block(doc, """// ExcelGrid.jsx — DOM Virtualization Core
const visibleRows = useMemo(() => {
    let start = 0, end = data.length - 1;
    let topSpacer = 0, bottomSpacer = 0;
    const buffer = 150;
    let offset = 0;

    for (let i = 0; i < data.length; i++) {
        const rh = rowHeights[i] || 30;
        if (offset + rh < scrollTop - buffer) {
            start = i + 1; topSpacer += rh;
        } else if (offset > scrollTop + containerH + buffer) {
            end = i - 1; break;
        }
        offset += rh;
    }
    if (end < start) end = start;
    for (let i = end + 1; i < data.length; i++)
        bottomSpacer += (rowHeights[i] || 30);

    return { start, end, topSpacer, bottomSpacer };
}, [data, rowHeights, scrollTop, containerH]);""", "Code Listing 4.2: ExcelGrid.jsx DOM Virtualization with Variable Row Height Support")

    # ──────────────────────────────────────────────────────────
    # 4.2.1  Undo/Redo and Formula Engine
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.2.1 Undo/Redo State History and Formula Evaluation Engine', level=3)

    insert_figure(doc,
        fig_num='Figure 4.2',
        title='Undo/Redo State History Stack Management Flow',
        height_inches=5.0,
        caption_text='Figure 4.2: Flowchart showing the bidirectional undo/redo stack operations, 30-entry cap, and deep-clone mechanism in ExcelGrid.jsx')

    para(doc, "To provide a native Microsoft Excel-like editing experience, the ExcelGrid component implements isolated memory stacks for undo and redo operations. Every time the user edits a cell, adds a row, or deletes a column, the entire current state of the spreadsheet (both the data array and the column definitions array) is deep-cloned using JSON.stringify followed by JSON.parse and pushed onto the undoStack array. The stack is deliberately capped at 30 entries: when a new state is pushed and the stack already contains 30 entries, the oldest entry is removed from the bottom using Array.shift(), preventing unbounded heap growth during long editing sessions on low-memory clinic computers.")
    para(doc, "The undo operation pops the top entry from undoStack, pushes the current state onto redoStack (so it can be re-applied), and replaces the active spreadsheet state with the popped snapshot. The redo operation reverses this: it pops from redoStack, pushes the current state back onto undoStack, and applies the redo snapshot. Any new user edit after an undo clears the entire redoStack, matching the behaviour of standard desktop spreadsheet applications. This bidirectional stack architecture provides a forgiving, intuitive editing experience that is essential for clinical staff who may need to quickly revert accidental deletions of patient records or prescription entries.")

    insert_figure(doc,
        fig_num='Figure 4.3',
        title='Spreadsheet Formula Parsing and Recursive Evaluation Flow',
        height_inches=5.0,
        caption_text='Figure 4.3: Flowchart showing the formula parser, SUM range detection, recursive cell resolution, and 50-level depth guard in ExcelGrid.jsx')

    para(doc, "The ExcelGrid component also supports spreadsheet formulas such as =SUM(A1:B5) and =A1+B2, evaluated by a recursive formula engine. When a cell value begins with the equals sign character, the evaluateFormula function is invoked with the cell's value string and the current recursion depth counter. The depth counter is checked against a hard limit of 50 levels at the start of every recursive call; if the limit is exceeded, the function returns the string 'CIRCULAR REF' and exits, preventing infinite loops caused by circular cell references such as a cell referencing itself through an intermediate chain of other cells.")
    para(doc, "The parser uses a regular expression to detect range expressions of the form LETTER+DIGIT:LETTER+DIGIT (for example A1:C3). For range expressions, it extracts the start and end column letters and row numbers, converts column letters to zero-based numeric indices using charCodeAt arithmetic, and iterates over the two-dimensional range, recursively evaluating each referenced cell's value before summing all resolved numeric results. For simple cell references such as =A1, the parser extracts the column letter and row number, looks up the corresponding value in the data grid, and recursively evaluates it in case it also contains a formula. This recursive evaluation with depth-limiting provides sufficient formula power for the statistical summary rows used in the clinic's monthly OPD count tables and inventory valuation calculations.")

    # ──────────────────────────────────────────────────────────
    # 4.3  PDF Compilation and Report Generation
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.3 Automated PDF Compilation and Report Generation', level=2)

    para(doc, "Statutory compliance reporting is a critical operational requirement for any Occupational Health Centre operating under the Factories Act, 1948. The JSP Patratu clinic must regularly produce detailed medical reports for submission to government health inspectors, plant safety management, and the corporate human resources division. Prior to JS Pulse OHMS, these reports were compiled manually by transcribing data from multiple paper ledgers into formatted documents — a process that consumed several hours of staff time per report and was prone to transcription errors that could compromise regulatory compliance.")
    para(doc, "JS Pulse OHMS automates this entire reporting pipeline through two complementary mechanisms. The first mechanism uses the jspdf library and jspdf-autotable plugin to construct PDF documents directly from JavaScript data structures, without requiring any browser rendering. This path is used for purely tabular reports such as the daily OPD register, monthly medicine consumption summary, and quarterly stock audit. The jspdf-autotable plugin generates professionally formatted tables with alternating row colours, bold headers, automatic page breaks, and JSP corporate branding applied through a custom header hook function that runs on every page.")
    para(doc, "The second mechanism, used for reports that contain embedded SVG charts and Mermaid.js diagrams, leverages a headless Electron BrowserWindow print pipeline. The React component assembles the complete report as an HTML string with embedded CSS and chart markup, then sends it through the IPC bridge to the Main Process. The Main Process creates a hidden BrowserWindow, loads the HTML content, waits 2,500 milliseconds for all asynchronous JavaScript rendering (including Mermaid diagram SVG generation and Recharts SVG layout) to complete, and then calls win.webContents.printToPDF() to capture the fully rendered page as a binary PDF buffer. This produces publication-quality output including visual analytics suitable for formal regulatory submission.")

    code_block(doc, """// electron/main.js — Headless PDF Print Bridge
ipcMain.handle('print-to-pdf', async (event, htmlContent, defaultPath) => {
    return new Promise((resolve) => {
        let win = new BrowserWindow({ show: false });
        win.loadURL(`data:text/html;charset=utf-8,
            ${encodeURIComponent(htmlContent)}`);
        win.webContents.on('did-finish-load', () => {
            setTimeout(() => {
                win.webContents.printToPDF({
                    printBackground: true, pageSize: 'A4'
                }).then(data => {
                    const tmp = path.join(os.tmpdir(), 'report.pdf');
                    fs.writeFileSync(tmp, data);
                    dialog.showSaveDialog({ defaultPath }).then(r => {
                        if (!r.canceled) fs.copyFileSync(tmp, r.filePath);
                        resolve({ success: !r.canceled, filePath: r.filePath });
                        win.close();
                    });
                });
            }, 2500);  // Wait for Mermaid + Recharts SVG render
        });
    });
});""", "Code Listing 4.3: Headless PDF Print Bridge in electron/main.js with 2.5-second Render Delay")

    # ──────────────────────────────────────────────────────────
    # 4.3.1  Offline NLP Chat Engine
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.3.1 Offline NLP Chat Engine and Token Classifier', level=3)

    insert_figure(doc,
        fig_num='Figure 4.4',
        title='Local ChatBrain NLP Intent Classification and Database Query Flow',
        height_inches=5.5,
        caption_text='Figure 4.4: Flowchart showing the dual-path NLP engine — online Gemini API routing and offline chatBrain.js regex token classification')

    para(doc, "JS Pulse OHMS integrates an offline-capable Natural Language Processing (NLP) chat engine that allows clinic staff to query the system using plain English sentences rather than navigating through module menus. This feature is particularly valuable for the clinic administrator who may need to quickly retrieve information such as current paracetamol stock, the number of OPD visits this month, or whether a specific employee has undergone their annual periodic examination, without knowing which module contains that data.")
    para(doc, "The chat engine operates in two modes depending on network availability. When the plant's internet connection is available, queries are forwarded to the Google Gemini API (gemini-pro model) via a fetch call with a structured system prompt that describes the available data stores and their schemas. The Gemini API returns a natural language response that may include structured data retrieved from the system's context. When the network is unavailable, the engine falls back to the local chatBrain.js module, which implements a rule-based intent classification system using JavaScript regular expressions.")
    para(doc, "The local chatBrain.js classifier normalises the user's input by converting it to lowercase and trimming whitespace. It then tests the normalised string against a priority-ordered array of regex patterns, each associated with a specific intent category (inventory-lookup, patient-search, stock-alert, count-query, and general-query). For inventory-lookup intents, the classifier extracts the medicine name from the matched groups and searches the cms_medstock_data store. For patient-search intents, it extracts the employee code or name and searches the cms_daily_opd_sheet store. For count-query intents, it counts records within a specified date range. The matched result is formatted into a human-readable response string and displayed in the chat interface. The 200-millisecond debounce on the input event prevents the classifier from running on every keystroke, reducing unnecessary computation during normal typing speed.")

    # ──────────────────────────────────────────────────────────
    # 4.3.2  Debounced Global Search Indexer
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.3.2 Debounced Global Search Indexer', level=3)

    insert_figure(doc,
        fig_num='Figure 4.5(a)',
        title='Global Search — Debounce and Scan Initialisation (Part 1 of 2)',
        height_inches=4.5,
        caption_text='Figure 4.5(a): Global search flow Part 1 — user input debouncing, timer reset, and localStorage key scanning loop initialisation')

    insert_figure(doc,
        fig_num='Figure 4.5(b)',
        title='Global Search — Record Matching, Snippet Generation, and Result Cap (Part 2 of 2)',
        height_inches=4.5,
        caption_text='Figure 4.5(b): Global search flow Part 2 — per-record lowercase match, snippet extraction, and 100-result cap to prevent UI freeze')

    para(doc, "The application provides a system-wide instant search feature accessible via the CTRL+K keyboard shortcut, allowing clinic staff to locate any patient record, medicine entry, dispense log, or examination result across all data domains simultaneously without switching between modules. The search implementation is deliberately designed to be extremely fast even on large datasets, using a combination of debouncing, lazy parsing, and early exit to keep the UI responsive during real-time query processing.")
    para(doc, "The search engine operates by maintaining a clearTimeout/setTimeout debounce pattern with a 200-millisecond delay. When the user types a character, any existing pending search timeout is cancelled using clearTimeout and a new 200-millisecond timeout is started. Only when the user pauses typing for 200 milliseconds does the actual search execution begin, preventing the expensive scan loop from running on every individual keystroke during fast typing.")
    para(doc, "The scan loop (Figure 4.5b) iterates over all keys in the localStorage proxy cache using a for loop over localStorage.length. For each key, it attempts to JSON.parse the value into an array. If the parse succeeds and the value is an array (indicating a valid clinical data table), the loop iterates over each record object in the array, converts the entire record to a lowercase string using JSON.stringify followed by toLowerCase, and checks whether that string includes the lowercased search query. If a match is found, the loop extracts a 120-character contextual snippet centred around the match position and pushes a result object containing the key name, matched field, and snippet to the results array. Once the results array reaches 100 entries, the outer loop is immediately broken using a labelled break statement, preventing the scan from freezing the UI thread on datasets exceeding 100,000 records.")

    # ──────────────────────────────────────────────────────────
    # 4.4  Data Synchronization and Local Caching Strategy
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.4 Data Synchronization and Local Caching Strategy', level=2)

    insert_figure(doc,
        fig_num='Figure 4.6',
        title='Background OPD-to-Pharmacy Prescription Synchronization Pipeline',
        height_inches=5.0,
        caption_text='Figure 4.6: Sequence diagram showing the 10-second polling sync pipeline that moves prescription data from cms_daily_opd_sheet to cms_dispense_log')

    para(doc, "The data synchronization architecture of JS Pulse OHMS is one of the most technically innovative aspects of the entire system. As a fully offline application, its synchronization challenges involve maintaining consistency between multiple local storage layers (in-memory state, localStorage proxy cache, IndexedDB, and file system JSON backups) and ensuring that automated data pipelines between clinical modules operate reliably without any network infrastructure. The primary synchronization mechanism is the automated OPD-to-pharmacy prescription pipeline.")
    para(doc, "When a doctor completes a patient consultation and submits the prescription in the OPD module, the patient record is written to cms_daily_opd_sheet with the extracted field set to false. A background synchronization interval running inside the DispenseMedicine component's useEffect hook polls this object store every 10,000 milliseconds (10 seconds). On each polling cycle, the sync function reads all records from cms_daily_opd_sheet, filters for those where extracted is false, and for each unextracted record, iterates over the medicines array to create one new entry in cms_dispense_log per medicine line. Each dispense entry receives a unique ID generated by combining the current timestamp (Date.now()) with a nine-character random alphanumeric string, preventing key collisions even when multiple prescriptions are processed within the same second.")
    para(doc, "After creating all dispense entries, the sync function updates the original OPD record's extracted field to true using a sheetDB put() operation, preventing duplicate extraction on subsequent polling cycles. The pharmacist's pending queue UI is refreshed by the same polling interval, so new prescriptions appear automatically within 10 seconds of being submitted by the doctor, without requiring any manual page refresh. This creates a seamless, real-time coordination experience between the OPD and pharmacy stations that was previously only achievable with network-connected server-side push notifications.")

    code_block(doc, """// DispenseMedicine.jsx — OPD Prescription Sync Pipeline
const extractFromOPD = () => {
    const opd      = getStorageData('cms_daily_opd_sheet') || [];
    const dispense = getStorageData('cms_dispense_log')    || [];
    let updated    = false;

    opd.forEach(rec => {
        if (rec.medicines?.length && !rec.extracted) {
            rec.medicines.forEach(med => {
                dispense.push({
                    id:          `disp-${Date.now()}-${Math.random()
                                    .toString(36).substr(2,9)}`,
                    date:        rec.date,
                    patientName: rec.patientName,
                    empId:       rec.empCode,
                    medicineName: med.name,
                    quantity:    med.qty,
                    status:      'Pending',
                    source:      'OPD'
                });
            });
            rec.extracted = true;
            updated = true;
        }
    });

    if (updated) {
        saveStorageData('cms_daily_opd_sheet', opd);
        saveStorageData('cms_dispense_log',    dispense);
    }
};

// Polling interval — runs every 10 seconds
useEffect(() => {
    const id = setInterval(extractFromOPD, 10000);
    return () => clearInterval(id);   // Cleanup on unmount
}, []);""", "Code Listing 4.4: OPD-to-Pharmacy Prescription Extraction and 10-second Sync Interval in DispenseMedicine.jsx")

    # ──────────────────────────────────────────────────────────
    # 4.5  Stock Deduction Algorithm
    # ──────────────────────────────────────────────────────────
    doc.add_heading('4.5 Pharmaceutical Stock Deduction Algorithm', level=2)

    insert_figure(doc,
        fig_num='Figure 4.7(a)',
        title='Medicine Verification and Stock Lookup (Part 1 of 2)',
        height_inches=4.5,
        caption_text='Figure 4.7(a): Stock deduction Part 1 — iterating prescribed medicines, case-insensitive name matching, and stock availability check')

    insert_figure(doc,
        fig_num='Figure 4.7(b)',
        title='Stock Quantity Update, Timestamp Logging, and Missing Medicine Alert (Part 2 of 2)',
        height_inches=4.5,
        caption_text='Figure 4.7(b): Stock deduction Part 2 — safe quantity subtraction, lastUpdated timestamp, missingMeds queue, and pharmacist alert')

    para(doc, "The pharmaceutical stock deduction algorithm in DailyConsume.jsx is the critical operation that maintains the accuracy of the clinic's medicine inventory after each dispensing event. When the pharmacist confirms a dispensing action by clicking the Mark as Dispensed button for a pending dispense log entry, the algorithm must atomically deduct the dispensed quantities from the master stock database (cms_medstock_data) while gracefully handling the case where a prescribed medicine is not found in the inventory, without aborting the entire deduction operation.")
    para(doc, "The algorithm begins by creating a shallow copy of the stockData array using the spread operator ([...stockData]) to avoid mutating the original React state directly. It then iterates over the medicines array of the dispense record being processed. For each medicine, it searches the stock copy using Array.findIndex() with a case-insensitive comparison (converting both the stock medicine name and the prescribed medicine name to lowercase before comparing) to find the matching stock entry.")
    para(doc, "If a matching stock entry is found (findIndex returns a non-negative index), the algorithm calculates the new stock quantity by subtracting the dispensed quantity from the current stock quantity, using Math.max(0, currentStock minus consumeQty) to ensure that the stock value never becomes negative even if a data entry error has resulted in a dispensed quantity that exceeds the recorded stock. The algorithm also updates the lastUpdated field of the matched stock entry to the current date in YYYY-MM-DD format, creating an automatic audit trail of every stock modification event. If no matching stock entry is found (findIndex returns minus one), the medicine name is pushed into a missingMeds array rather than causing an exception that would abort the entire deduction batch. After processing all medicines, if missingMeds is non-empty, a user-facing alert dialog lists all unmatched medicine names so the pharmacist can manually investigate and correct the stock database.")

    code_block(doc, """// DailyConsume.jsx — Resilient Stock Deduction Algorithm
const updatedStock = [...stockData];
const missingMeds  = [];

record.medicines.forEach(med => {
    const idx = updatedStock.findIndex(
        s => s.medicineName.toLowerCase() === med.name.toLowerCase()
    );
    if (idx !== -1) {
        const curr = parseInt(updatedStock[idx].currentStock) || 0;
        const qty  = parseInt(med.qty) || 0;
        updatedStock[idx].currentStock  = Math.max(0, curr - qty);
        updatedStock[idx].lastUpdated   =
            new Date().toISOString().split('T')[0];
        updatedStock[idx].status        = 'Deducted';
    } else {
        missingMeds.push(med.name);
    }
});

// Save updated stock
saveStorageData('cms_medstock_data', updatedStock);
setStockData(updatedStock);

// Alert for unmatched medicines
if (missingMeds.length > 0)
    alert(`Stock not deducted for: ${missingMeds.join(', ')}`);""", "Code Listing 4.5: Resilient Stock Deduction with Case-Insensitive Matching and Missing Medicine Queue in DailyConsume.jsx")

    para(doc, "The resilient design of this algorithm is intentional: in a clinical setting, it is better to partially complete an operation and alert the user about exceptions than to abort the entire transaction and leave the pharmacist uncertain about which items were processed. The Math.max(0, ...) floor guard prevents negative stock values that would corrupt the inventory database and cause incorrect low-stock alerts. The case-insensitive comparison is necessary because medicine names may be entered with varying capitalisation across different modules (for example, 'Paracetamol 500mg' versus 'paracetamol 500mg'), and a case-sensitive match would fail to deduct stock for a medicine that is clearly present in the inventory under a differently cased name. These implementation details reflect real-world operational lessons learned during the initial deployment and testing phase of JS Pulse OHMS at the JSP Patratu Occupational Health Centre.")

    # SAVE
    out_path = 'JSPulse_OHMS_Chapter4_WithSpaces.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == '__main__':
    main()
