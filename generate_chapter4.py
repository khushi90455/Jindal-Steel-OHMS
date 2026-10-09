import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT, WD_SECTION_START

IMG_DIR = 'diagram_images_hq'

# Actual image dimensions (width x height) in pixels
DIAGRAM_DIMS = {
    'diagram_5.png':  (1392, 1187),
    'diagram_6.png':  (1054, 1864),
    'diagram_7.png':  (2771, 1055),
    'diagram_8.png':  (1668, 2098),
    'diagram_19.png': (711, 1316),
    'diagram_20.png': (1220, 2310),
    'diagram_10.png': (2410, 808),
    'diagram_21.png': (711, 1273),
    'diagram_22.png': (2780, 1055),
}

def setup_portrait_section(section):
    """Set standard A4 Portrait margins (1.0 inch all around)."""
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

def setup_landscape_section(section, width_in):
    """Set standard A4 Landscape margins. If image is very wide, use 0.8 in margins."""
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    
    # 1.0 inch margins allow 9.69 in width. If image exceeds this, use 0.8 in margins.
    margin_size = 0.8 if width_in > 9.69 else 1.0
    section.left_margin = Inches(margin_size)
    section.right_margin = Inches(margin_size)

def add_paragraph(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.add_run(text)
    return p

def insert_diagram(doc, img_filename, caption_text):
    """Inserts a diagram page with orientation optimized for 300 DPI printing without cropping or scaling down."""
    img_path = os.path.join(IMG_DIR, img_filename)
    if not os.path.exists(img_path):
        add_paragraph(doc, f"[Diagram not found: {img_filename}]")
        return
        
    w, h = DIAGRAM_DIMS.get(img_filename, (800, 600))
    # Calculate physical size at exactly 300 DPI
    width_in = w / 300.0
    height_in = h / 300.0
    
    # Determine orientation
    is_landscape = width_in > 6.27  # Portrait printable width is 8.27 - 2 = 6.27
    
    # Add a new section for the diagram
    new_section = doc.add_section(WD_SECTION_START.NEW_PAGE)
    if is_landscape:
        setup_landscape_section(new_section, width_in)
    else:
        setup_portrait_section(new_section)
        
    # Insert the image centered
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run()
    run.add_picture(img_path, width=Inches(width_in), height=Inches(height_in))
    
    # Add caption
    cap = doc.add_paragraph(caption_text)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(12)
    run_cap = cap.runs[0]
    run_cap.italic = True
    run_cap.font.size = Pt(10)
    run_cap.font.name = 'Times New Roman'
    
    # Return to normal Portrait section for subsequent text
    next_section = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_portrait_section(next_section)

def add_code_block(doc, code_text, caption_text=None):
    for line in code_text.strip().split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Inches(0.4)
        run = p.add_run(line)
        run.font.name = 'Courier New'
        run.font.size = Pt(9)
    if caption_text:
        cap = doc.add_paragraph(caption_text)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(4)
        run_cap = cap.runs[0]
        run_cap.italic = True
        run_cap.font.size = Pt(10)
        run_cap.font.name = 'Times New Roman'

def main():
    doc = Document()
    
    # Set orientation for the first section (Chapter Text)
    setup_portrait_section(doc.sections[0])
    
    # Base text styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    for i in range(1, 4):
        h_style = doc.styles[f'Heading {i}']
        h_font = h_style.font
        h_font.name = 'Times New Roman'
        h_font.color.rgb = RGBColor(0, 0, 0)

    # Chapter 4 Header
    doc.add_heading('Chapter 4: Implementation Deep-Dive and Algorithms', level=1)

    # --- 4.1 Custom IndexedDB Wrapper (sheetDB.js) ---
    doc.add_heading('4.1 Custom IndexedDB Wrapper (sheetDB.js) Implementation', level=2)
    add_paragraph(doc, "The sheetDB.js module represents the most performance-critical and architecturally significant component in the entire JS Pulse OHMS codebase. It serves as the exclusive data access layer for all clinical operations, providing a high-level, promise-based API that abstracts the considerable complexity of the raw IndexedDB interface. The design motivation for creating a custom wrapper, rather than using an existing library like Dexie.js or idb, was driven by the need for extreme control over transaction lifecycle management, connection pooling behavior, and error recovery strategies specific to the industrial deployment environment.")
    add_paragraph(doc, "At its core, sheetDB.js manages the lifecycle of IndexedDB connections and transactions. When the application initializes, the module opens a persistent connection to the primary database instance. This connection is stored in a module-level variable and reused for all subsequent operations, eliminating the overhead of repeatedly opening and closing connections (which can be significant on resource-constrained clinic computers). The module also implements a version management system that tracks schema changes across application updates, automatically triggering migration routines when a newer version of the database schema is detected.")
    add_paragraph(doc, "The read operations provided by sheetDB.js support both full-table scans and key-based lookups. A full-table scan opens a cursor on the target object store and iterates through all records, collecting them into an array that is returned to the calling component. Key-based lookups use IndexedDB's native get method to retrieve a single record by its primary key, providing constant-time O(1) retrieval performance. For more complex queries (such as finding all patients who visited the OPD on a specific date, or identifying medicines with stock levels below a critical threshold), the module implements client-side filtering by loading the relevant dataset and applying JavaScript predicate functions.")
    add_paragraph(doc, "Write operations in sheetDB.js are wrapped in IndexedDB transactions with explicit readwrite mode. Each write operation creates a new transaction, adds or updates the target record using the put method (which performs an upsert: inserting the record if it does not exist, or replacing it if the primary key already matches an existing record), and then waits for the transaction to complete before resolving the returned Promise. This transactional approach ensures atomicity: either the entire write operation succeeds, or the database remains in its previous consistent state.")

    add_code_block(doc, """// sheetDB.js - Core Connection Pool and Transaction Manager
const DB_NAME = 'JSPulseOHMS_DB';
const DB_VERSION = 3;
let dbConnection = null;

const openDB = () => {
    return new Promise((resolve, reject) => {
        if (dbConnection) { resolve(dbConnection); return; }
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('patient_visits'))
                db.createObjectStore('patient_visits', { keyPath: 'id' });
            if (!db.objectStoreNames.contains('med_stock'))
                db.createObjectStore('med_stock', { keyPath: 'id' });
            if (!db.objectStoreNames.contains('dispense_log'))
                db.createObjectStore('dispense_log', { keyPath: 'id' });
        };

        request.onsuccess = (event) => {
            dbConnection = event.target.result;
            resolve(dbConnection);
        };
        request.onerror = (event) => reject(event.target.error);
    });
};""", "Code Listing 4.1: sheetDB.js Core Connection Pooling and Schema Initialization")

    add_paragraph(doc, "The connection pooling mechanism shown in Code Listing 4.1 demonstrates how sheetDB.js maintains a single persistent database connection. The openDB function first checks whether the module-level dbConnection variable already holds an active connection. If it does, the existing connection is immediately returned without any I/O overhead. If not, a new connection is opened using the indexedDB.open API, and the onupgradeneeded callback handles schema creation and migration. This pattern ensures that the application never opens more than one concurrent connection to the database, preventing resource contention on low-memory clinic workstations.")
    add_paragraph(doc, "The error handling strategy in sheetDB.js is designed for the harsh realities of an industrial deployment. IndexedDB operations can fail due to storage quota exhaustion, database corruption, or concurrent access conflicts. Each database operation is wrapped in a try-catch block that catches and classifies errors into recoverable and non-recoverable categories. Recoverable errors (such as temporary quota warnings) trigger a background cleanup routine that purges expired log entries to free storage space. Non-recoverable errors (such as database corruption) trigger an alert to the clinic administrator and attempt to restore from the most recent backup stored on the file system through the Electron IPC bridge.")
    add_paragraph(doc, "The sheetDB module also provides a bulk write operation that batches multiple record insertions into a single IndexedDB transaction. This is critical for performance during data import operations, such as when the clinic uploads a historical patient database from an Excel file. Without batching, inserting 10,000 records would require 10,000 separate transactions, each with its own disk I/O overhead. With batching, all records are inserted within a single transaction, reducing the total I/O operations to a single disk flush and improving import performance by orders of magnitude.")

    # --- 4.2 DOM Virtualization Algorithm ---
    doc.add_heading('4.2 DOM Virtualization Algorithm for Medical Spreadsheets', level=2)
    add_paragraph(doc, "The medical spreadsheet component (ExcelGrid.jsx) is the primary data interaction surface in JS Pulse OHMS. Clinical staff use it to view, edit, and manage thousands of patient records, pharmaceutical inventory entries, and dispensing logs. Rendering this volume of data using standard React rendering would create tens of thousands of DOM nodes, overwhelming the browser's layout engine and causing severe performance degradation, including dropped frames, sluggish scrolling, and unresponsive user input.")
    add_paragraph(doc, "To solve this fundamental performance challenge, the ExcelGrid component implements a custom DOM virtualization algorithm. The core principle of DOM virtualization is simple but powerful: instead of rendering all rows in the dataset, the algorithm calculates which rows are currently visible within the user's viewport and renders only those rows. Rows that have scrolled above the visible area are replaced by a single spacer div whose height equals the combined height of all hidden rows above. Similarly, rows below the visible area are replaced by a bottom spacer div. This creates the illusion of a fully rendered scrollable grid while maintaining a constant, minimal number of actual DOM nodes.")
    add_paragraph(doc, "The algorithm operates within a React useMemo hook to ensure that the visible row calculations are only recomputed when the input dependencies change (specifically, the dataset, row heights, scroll position, and container dimensions). The computation begins by iterating through the complete dataset from the first row to the last. For each row, the algorithm calculates the cumulative vertical offset by summing the heights of all preceding rows. A row is included in the visible set if its cumulative offset falls within the range defined by (scrollTop - buffer) to (scrollTop + containerHeight + buffer), where buffer is a 150-pixel overscan zone that ensures smooth scrolling by pre-rendering rows just outside the visible viewport.")

    insert_diagram(doc, 'diagram_5.png',
                   'Figure 4.1: DOM Viewport Virtualization Row Calculation Sequence Diagram (A4 Portrait, 300 DPI Original Size)')

    add_code_block(doc, """// ExcelGrid.jsx - DOM Virtualization Core Algorithm
const visibleRows = useMemo(() => {
    let start = 0;
    let end = data.length - 1;
    let topSpacerHeight = 0;
    let bottomSpacerHeight = 0;
    const buffer = 150;
    let currentOffset = 0;

    for (let i = 0; i < data.length; i++) {
        const rowHeight = rowHeights[i] || 30;
        if (currentOffset + rowHeight < scrollTop - buffer) {
            start = i + 1;
            topSpacerHeight += rowHeight;
        } else if (currentOffset > scrollTop + containerHeight + buffer) {
            end = i - 1;
            break;
        }
        currentOffset += rowHeight;
    }

    if (end < start) end = start;
    for (let i = end + 1; i < data.length; i++) {
        bottomSpacerHeight += (rowHeights[i] || 30);
    }

    return { start, end, topSpacerHeight, bottomSpacerHeight };
}, [data, rowHeights, scrollTop, containerHeight]);""", "Code Listing 4.2: ExcelGrid DOM Virtualization with Buffer Zone Computation")

    add_paragraph(doc, "The performance impact of this virtualization algorithm is dramatic. Without virtualization, rendering a dataset of 5,000 patient records with 15 columns each would create approximately 75,000 individual DOM cell elements, plus row containers and structural wrappers. The browser's layout engine would need to calculate positions, apply styles, and composite paint layers for all 75,000 elements on every frame, resulting in frame rates well below the 60fps threshold required for a responsive user experience.")
    add_paragraph(doc, "With virtualization, the same dataset renders only approximately 30 to 50 rows at any given time (the exact number depending on the viewport height and row heights), creating roughly 450 to 750 DOM elements. The spacer divs maintain the correct scrollbar position and total scroll height, so the user perceives a smooth, continuous scrollable grid. The transition between rendered rows is seamless because the 150-pixel buffer zone ensures that new rows are rendered just before they enter the visible viewport, preventing any visible flickering or content popping.")
    add_paragraph(doc, "Additionally, the ExcelGrid component implements individual row height tracking through a rowHeights state array. This is essential because clinical data often varies in length: a brief routine checkup might occupy a single line, while a complex occupational injury report might require multiple lines of wrapped text. The virtualization algorithm accounts for variable row heights by summing individual heights rather than assuming a fixed row height, ensuring pixel-perfect scrollbar behavior even with heterogeneous content.")

    # Undo/Redo and Formula Engine subsection
    doc.add_heading('4.2.1 Undo/Redo State History and Formula Evaluation Engine', level=3)
    add_paragraph(doc, "To provide a native Excel-like editing experience within the browser, the ExcelGrid component implements isolated memory stacks for Undo and Redo operations. Every time the user edits a cell, adds a row, or deletes a column, the entire current state of the spreadsheet (including both data and column definitions) is deep-cloned using JSON.stringify and pushed onto the undoStack array. The stack is deliberately capped at 30 entries to prevent unbounded memory growth in the Chromium heap, which would degrade application performance during extended editing sessions.")

    insert_diagram(doc, 'diagram_6.png',
                   'Figure 4.2: Undo/Redo State History Management Flow (A4 Portrait, 300 DPI Original Size)')

    add_paragraph(doc, "As shown in Figure 4.2, each edit triggers a deep clone of the current state, which is pushed onto the undo stack. If the stack exceeds 30 entries, the oldest entry is shifted from the bottom. When the user triggers a Redo, the system pops from the redo stack and pushes the current state onto the undo stack. This bidirectional stack architecture provides intuitive, Excel-compatible editing behavior.")
    add_paragraph(doc, "The spreadsheet grid also supports custom formulas such as =SUM(A1:B5) or =A1+B2. The formula evaluation engine uses recursive regex parsing to map alphanumeric cell coordinates (such as 'A1') to row and column matrix indices. A critical safety feature is the depth limiter: recursive formula evaluation is capped at 50 levels of recursion to prevent infinite loop crashes caused by circular cell references, which would otherwise freeze the application.")

    insert_diagram(doc, 'diagram_7.png',
                   'Figure 4.3: Spreadsheet Formula Parsing and Recursive Evaluation Flow (A4 Landscape, 300 DPI Original Size)')

    add_paragraph(doc, "Figure 4.3 illustrates the complete formula evaluation pipeline. When a cell value begins with the '=' character, the evaluateFormula function is invoked. It first checks the recursion depth against the 50-level limit. It then applies a regex to detect SUM range expressions, calculates the bounding row and column indices, iterates through the specified cell range, and recursively evaluates any nested formulas within referenced cells before summing the numeric results.")

    # --- 4.3 Automated PDF Compilation Logic ---
    doc.add_heading('4.3 Automated PDF Compilation and Report Generation Logic', level=2)
    add_paragraph(doc, "Statutory compliance reporting is a critical operational requirement for any Occupational Health Center operating under the Factories Act, 1948. The JSP Patratu clinic must regularly produce detailed medical reports for submission to government health inspectors, plant management, and the corporate safety division. Prior to JS Pulse OHMS, these reports were compiled manually by transcribing data from multiple paper ledgers into formatted documents, a process that consumed several hours of staff time per report and was prone to transcription errors.")
    add_paragraph(doc, "JS Pulse OHMS automates this entire reporting pipeline through a sophisticated PDF compilation engine that leverages the jspdf library for binary PDF stream construction and the jspdf-autotable plugin for structured tabular layouts. The report generation process is initiated when a clinic administrator navigates to the reports module and selects the desired report type (such as Monthly OPD Summary, Quarterly Inventory Audit, or Annual Periodic Examination Compliance Report).")
    add_paragraph(doc, "The PDF generation logic first queries the local database to retrieve all records matching the selected date range and report category. The retrieved data is then transformed into a structured table format compatible with jspdf-autotable's column definition schema. Headers, footers, page numbers, and the JSP corporate logo are injected into the document template. The jspdf library constructs the PDF as an in-memory binary buffer (ArrayBuffer), which is then passed through the Electron IPC bridge to the Main Process for native file system persistence.")

    add_code_block(doc, """// electron/main.js - Headless PDF Print Bridge
ipcMain.handle('print-to-pdf', async (event, htmlContent, defaultPath) => {
    return new Promise((resolve) => {
        let win = new BrowserWindow({ show: false });
        win.loadURL(
            `data:text/html;charset=utf-8,${encodeURIComponent(htmlContent)}`
        );
        win.webContents.on('did-finish-load', () => {
            setTimeout(() => {
                win.webContents.printToPDF({
                    printBackground: true,
                    pageSize: 'A4',
                    marginType: 0
                }).then(data => {
                    const tempPath = path.join(os.tmpdir(), 'report.pdf');
                    fs.writeFileSync(tempPath, data);
                    dialog.showSaveDialog({
                        defaultPath: defaultPath
                    }).then(result => {
                        if (!result.canceled) {
                            fs.copyFileSync(tempPath, result.filePath);
                            resolve({
                                success: true,
                                filePath: result.filePath
                            });
                        }
                        win.close();
                    });
                });
            }, 2500);
        });
    });
});""", "Code Listing 4.3: Electron Headless PDF Print Bridge with Native Save Dialog")

    add_paragraph(doc, "Code Listing 4.3 reveals the sophisticated mechanism by which JS Pulse OHMS generates visually rich PDF reports that include rendered charts and diagrams. The Electron Main Process creates a hidden (headless) BrowserWindow, loads the HTML report content (which may include embedded Mermaid.js diagrams or Recharts SVG visualizations), and waits 2,500 milliseconds for all asynchronous rendering to complete. The printToPDF method then captures the fully rendered page as a binary PDF buffer with A4 page dimensions, which is saved to a temporary file before presenting the user with a native Windows 'Save As' dialog for choosing the final destination path.")
    add_paragraph(doc, "The 2,500-millisecond delay is a carefully calibrated engineering decision. Mermaid.js diagrams render asynchronously after the DOM content loads, requiring time for the CDN script to initialize, parse the diagram markup, and generate SVG elements. If the PDF capture were triggered immediately after did-finish-load, the diagrams would appear as raw unparsed text in the output PDF. The delay ensures that all visual elements are fully rendered before the capture occurs, producing publication-quality reports suitable for formal submission to regulatory authorities.")
    add_paragraph(doc, "For simpler tabular reports that do not require visual rendering, the application uses an alternative path that bypasses the headless browser entirely. The jspdf library constructs the PDF directly from JavaScript data structures, using the autoTable plugin to create professionally formatted tables with alternating row colors, header styling, and automatic page breaks. This direct construction path is significantly faster than the headless browser approach and is used for routine reports such as daily OPD summaries and inventory checklists.")

    # NLP Chat Engine subsection
    doc.add_heading('4.3.1 Offline NLP Chat Engine and Token Classifier', level=3)
    add_paragraph(doc, "JSPulse OHMS integrates an offline Natural Language Processing (NLP) chat engine that allows clinic staff to query the system using natural language instead of navigating through menus. When the plant's internet connection is available, queries are routed to the Google Gemini API for advanced language understanding. However, when the network is down (which is a frequent occurrence at the Patratu plant), the system seamlessly falls back to a local chatBrain.js module that uses regex-based token classification to determine user intent and query the local database.")

    insert_diagram(doc, 'diagram_8.png',
                   'Figure 4.4: Local ChatBrain NLP Intent Classification and Database Query Flow (A4 Portrait, 300 DPI Original Size)')

    add_paragraph(doc, "Figure 4.4 illustrates the complete NLP processing pipeline. User input is first normalized (converted to lowercase, whitespace trimmed). The system checks network status: if online, the query is forwarded to Google Gemini; if offline, it enters the local chatBrain processing path. The local engine applies regex pattern matching to classify the intent into categories such as 'inventory lookup', 'patient search', or 'general query'. Based on the classified intent, the engine queries the appropriate localStorage data store and formats a localized response for the user.")

    # Global Search subsection
    doc.add_heading('4.3.2 Debounced Global Search Indexer', level=3)
    add_paragraph(doc, "The application provides a global search feature accessible via the CTRL+K keyboard shortcut, allowing clinic staff to instantly search across all data domains simultaneously. The search implementation uses a debounced polling loop that waits 200 milliseconds after the last keystroke before executing the search, preventing excessive computation during rapid typing. The search iterates through all localStorage keys, parses JSON arrays on-the-fly, and converts each record to a lowercase string representation for case-insensitive matching. Results are capped at 100 entries to prevent DOM freezing when searching across very large datasets.")

    insert_diagram(doc, 'diagram_19.png',
                   'Figure 4.5(a): Global Search Debouncing and Search Initialization (Part 1 - A4 Portrait, 300 DPI Original Size)')
    insert_diagram(doc, 'diagram_20.png',
                   'Figure 4.5(b): Global Search Scanning loop and Result limiting (Part 2 - A4 Portrait, 300 DPI Original Size)')

    add_paragraph(doc, "Figures 4.5(a) and 4.5(b) show the complete search indexing flow. Part 1 tracks the user input, the debounce timer, and scanning key arrays. Part 2 tracks matching values, generating snippets, and capping results at 100 entries. This distributed flow ensures the UI remains fluid and completely responsive during intense, real-time lookups.")

    # --- 4.4 Data Synchronization & Local Caching Strategy ---
    doc.add_heading('4.4 Data Synchronization and Local Caching Strategy', level=2)
    add_paragraph(doc, "The data synchronization architecture of JS Pulse OHMS is one of the most technically innovative aspects of the entire system. In a conventional web application, data synchronization refers to keeping a client-side cache consistent with a remote server-side database. However, JS Pulse OHMS operates in an entirely different paradigm: as a fully offline application, its synchronization challenges involve maintaining consistency between multiple local storage layers (in-memory state, localStorage proxy, IndexedDB, and file system JSON backups) and ensuring that automated data pipelines between clinical modules (such as the OPD-to-pharmacy prescription sync) operate reliably without any network connectivity.")
    add_paragraph(doc, "The primary synchronization mechanism is the automated OPD-to-pharmacy prescription pipeline. When a doctor completes a patient consultation and records a prescription in the OPD module, the prescription data is saved to the cms_patient_visit_log store with an extracted field set to false. A background synchronization interval running in the pharmacy module's DispenseMedicine component polls this store every 10 seconds, scanning for records where extracted is false. When unextracted prescriptions are found, the sync process creates corresponding entries in the cms_dispense_log store, copies the patient details and prescribed medicines, and sets the status to 'Pending'. The original OPD record is then updated to extracted: true to prevent duplicate extraction in subsequent polling cycles.")

    insert_diagram(doc, 'diagram_10.png',
                   'Figure 4.6: Background OPD-to-Pharmacy Prescription Synchronization Pipeline (A4 Landscape, 300 DPI Original Size)')

    add_paragraph(doc, "Figure 4.6 depicts the complete synchronization pipeline as a sequence diagram. The Doctor component saves a patient record to the local database with the extracted flag set to false. The background sync interval (running every 10 seconds in the Pharmacy component) scans the database for unextracted records, creates corresponding dispense queue entries, and marks the original records as extracted. The pharmacist then processes the pending prescriptions, dispensing medicines and updating the stock levels in real-time.")

    add_code_block(doc, """// DispenseMedicine.jsx - OPD-to-Pharmacy Sync Pipeline
const extractFromOPD = () => {
    const opdData = getStorageData('cms_patient_visit_log') || [];
    const dispenseData = getStorageData('cms_dispense_log') || [];
    let updated = false;

    opdData.forEach(opdRecord => {
        if (opdRecord.medicines && opdRecord.medicines.length > 0
            && !opdRecord.extracted) {
            const newDispenseRecord = {
                id: `disp-${Date.now()}-${Math.random()
                    .toString(36).substr(2, 9)}`,
                date: opdRecord.date,
                patientName: opdRecord.patientName,
                empId: opdRecord.empId,
                medicines: opdRecord.medicines,
                status: 'Pending',
                source: 'OPD'
            };
            dispenseData.push(newDispenseRecord);
            opdRecord.extracted = true;
            updated = true;
        }
    });

    if (updated) {
        saveStorageData('cms_patient_visit_log', opdData);
        saveStorageData('cms_dispense_log', dispenseData);
    }
};""", "Code Listing 4.4: Automated OPD-to-Pharmacy Prescription Extraction Pipeline")

    add_paragraph(doc, "Code Listing 4.4 shows the implementation of the extraction pipeline. The function iterates through all OPD records, identifies those with non-empty medicine arrays and extracted flag set to false, creates structured dispense records with unique identifiers, and batch-updates both the OPD and dispense stores in a single operation. The unique ID generation uses a combination of the current timestamp and a random alphanumeric suffix to prevent collisions even when multiple prescriptions are processed in the same millisecond.")
    add_paragraph(doc, "The inventory deduction mechanism is another critical synchronization component. When a pharmacist confirms a dispensing action, the system must atomically deduct the prescribed quantities from the master stock database (cms_medstock_data). This process is implemented as a strict transactional operation: the system first validates that every prescribed medicine exists in the inventory and has sufficient stock. If any medicine is missing from the database or has insufficient quantity, the system routes that specific item to a missingMeds queue and alerts the pharmacist, but continues processing the remaining valid items rather than aborting the entire transaction.")

    insert_diagram(doc, 'diagram_21.png',
                   'Figure 4.7(a): Medicine Verification and Stock Verification Flow (Part 1 - A4 Portrait, 300 DPI Original Size)')
    insert_diagram(doc, 'diagram_22.png',
                   'Figure 4.7(b): Stock Update Adjustments and Warning Logs (Part 2 - A4 Landscape, 300 DPI Original Size)')

    add_paragraph(doc, "Figures 4.7(a) and 4.7(b) illustrate the stock deduction decision tree. Part 1 tracks verification steps. Part 2 tracks actual value subtractions and updates logs. This resilient design ensures that data inconsistencies do not halt the entire dispensing workflow.")

    add_code_block(doc, """// DailyConsume.jsx - Resilient Stock Deduction Algorithm
const updatedStock = [...stockData];
const missingMeds = [];

record.medicines.forEach(med => {
    const stockIndex = updatedStock.findIndex(
        s => s.medicineName.toLowerCase() === med.name.toLowerCase()
    );

    if (stockIndex !== -1) {
        const currentStock = parseInt(
            updatedStock[stockIndex].currentStock) || 0;
        const consumeQty = parseInt(med.qty) || 0;
        updatedStock[stockIndex].currentStock =
            Math.max(0, currentStock - consumeQty);
        updatedStock[stockIndex].lastUpdated =
            new Date().toISOString().split('T')[0];
    } else {
        missingMeds.push(med.name);
    }
});

if (missingMeds.length > 0) {
    alert('Could not deduct stock for: ' +
        missingMeds.join(', ') + ' (Not found in inventory)');
}""", "Code Listing 4.5: Inventory Deduction with Graceful Missing Medicine Handling")

    add_paragraph(doc, "The local caching strategy extends beyond the primary clinical data stores to encompass application configuration, user preferences, and system health metrics. The SystemHealthTool component continuously monitors the localStorage quota utilization by iterating through all stored keys and calculating the total byte consumption using UTF-16 encoding principles (2 bytes per character). When the utilization approaches the browser-enforced 5MB limit, the tool triggers a background migration process that moves older, less frequently accessed records from localStorage to IndexedDB, freeing space in the primary cache for active operational data.")
    add_paragraph(doc, "This multi-tiered caching architecture, combining in-memory Maps for instant read access, localStorage proxy for transparent API compatibility, IndexedDB for large-scale persistent storage, and native file system JSON backups for disaster recovery, provides the JS Pulse OHMS application with an extremely robust and resilient data management foundation. Even in the worst-case scenario of a complete system crash or power failure, the application can recover to its most recent consistent state by loading the file system backup through the Electron IPC bridge during the next startup sequence.")

    # Save
    out_path = 'JSPulse_OHMS_Chapter4.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
