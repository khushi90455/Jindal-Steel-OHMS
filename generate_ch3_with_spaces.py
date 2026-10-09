import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips
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

def fig_label(doc, fig_num, title):
    """Bold centred figure label line, e.g. 'Figure 3.1: System Architecture Diagram'."""
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
    """
    Insert a single-cell table with a fixed row height to reserve space
    for a diagram. A dashed border and light fill make it visually obvious.
    Height is in inches; use 5.0 for half-page, 9.0 for full-page.
    """
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'

    cell = table.rows[0].cells[0]

    # ── Fixed row height ──────────────────────────────────────────
    tr   = cell._tc.getparent()
    trPr = OxmlElement('w:trPr')
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), str(int(height_inches * 1440)))  # 1440 twips per inch
    trHeight.set(qn('w:hRule'), 'exact')
    trPr.append(trHeight)
    tr.insert(0, trPr)

    # ── Light grey shading ────────────────────────────────────────
    tcPr = cell._tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  'F0F0F0')
    tcPr.append(shd)

    # ── Dashed border on all four sides ──────────────────────────
    tcBdr = OxmlElement('w:tcBorders')
    for side in ('top', 'left', 'bottom', 'right'):
        bdr = OxmlElement(f'w:{side}')
        bdr.set(qn('w:val'),   'dashDotStroked')
        bdr.set(qn('w:sz'),    '12')
        bdr.set(qn('w:space'), '0')
        bdr.set(qn('w:color'), '808080')
        tcBdr.append(bdr)
    tcPr.append(tcBdr)

    # ── Centred label inside the box ─────────────────────────────
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    run = p.add_run('[Space reserved for diagram — insert figure here]')
    run.font.name  = 'Times New Roman'
    run.font.size  = Pt(10)
    run.italic     = True
    run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

    # Paragraph after the table
    after = doc.add_paragraph()
    after.paragraph_format.space_before = Pt(6)
    after.paragraph_format.space_after  = Pt(8)

def sub_caption(doc, text):
    """Italic centred caption below the blank space box."""
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(14)
    r = p.runs[0]
    r.italic = True
    r.font.size = Pt(10)
    r.font.name = 'Times New Roman'


def insert_figure(doc, fig_num, title, height_inches=5.0, caption_text=None):
    """Full figure block: label + blank space + optional sub-caption."""
    fig_label(doc, fig_num, title)
    blank_diagram_space(doc, height_inches)
    if caption_text:
        sub_caption(doc, caption_text)


def main():
    doc = Document()
    setup_doc(doc)

    # ═══════════════════════════════════════════════════════════
    # CHAPTER 3 TITLE
    # ═══════════════════════════════════════════════════════════
    doc.add_heading('Chapter 3: Advanced UML and Architecture Flows', level=1)

    # -----------------------------------------------------------
    # 3.1  System Architecture Diagram
    # -----------------------------------------------------------
    doc.add_heading('3.1 System Architecture Diagram', level=2)

    insert_figure(doc,
        fig_num='Figure 3.1',
        title='JS Pulse OHMS Complete System Architecture',
        height_inches=5.5,
        caption_text='Figure 3.1: Complete JS Pulse OHMS System Architecture showing the Electron Dual-Process Model, IPC Bridge, and IndexedDB Storage Layer')

    para(doc, "The JS Pulse OHMS system architecture is founded on the Electron framework, which merges a Node.js native runtime with a Chromium-based web renderer to produce a full-featured offline desktop application. The architecture is divided into two isolated process domains: the Main Process and the Renderer Process. The Main Process, controlled by electron/main.js, owns all Node.js capabilities including file-system I/O, native Windows dialogs, system tray management, and IndexedDB schema migration. The Renderer Process, controlled by main.jsx and the React 19 component tree, manages the entire clinical user interface including the OPD console, pharmacy dispense queue, medicine stock ledger, periodic examination records, and first aid kit tracker.")
    para(doc, "The security boundary between these two processes is enforced through context isolation. When the BrowserWindow is created in main.js, two flags are explicitly set: contextIsolation: true and nodeIntegration: false. These settings prevent the Renderer Process from importing Node.js modules or accessing system APIs directly. All cross-process communication is routed through a dedicated preload.js script, which is injected by Electron before any web content loads. The preload script uses Electron's contextBridge.exposeInMainWorld API to attach a minimal, whitelisted set of functions to the global window.electron object, making them callable from React components.")
    para(doc, "At the data layer, the architecture uses a three-tier storage model. The first tier is an in-memory Map cache maintained by the localStorage proxy engine injected in main.jsx. This provides sub-millisecond read access for all data rendered in the active React component tree. The second tier is the browser's IndexedDB, accessed exclusively through the sheetDB.js custom wrapper. It stores all clinical records in three primary object stores: cms_daily_opd_sheet, cms_dispense_log, and cms_medstock_data. The third tier is the native Windows file system, which stores JSON backup copies of all records via the Electron IPC bridge, providing a disaster-recovery layer that survives even a complete browser storage corruption event.")
    para(doc, "The six functional module groups (Clinical, Pharmacy, Inventory, Reports, System Health, and Administration) are implemented as independent React component subtrees, each reading from and writing to the shared IndexedDB storage through the sheetDB abstraction. The automated prescription sync engine, implemented as a setInterval polling loop in DispenseMedicine.jsx, bridges the Clinical and Pharmacy modules by reading unprocessed OPD records every 10 seconds and creating corresponding entries in the dispense queue without any direct inter-component function calls. This decoupled architecture means that a failure in the Pharmacy module does not affect the OPD module's ability to accept new patient registrations, ensuring continuous clinical operation during partial system faults.")

    # -----------------------------------------------------------
    # 3.2  Use Case Diagram
    # -----------------------------------------------------------
    doc.add_heading('3.2 Use Case Diagram', level=2)

    insert_figure(doc,
        fig_num='Figure 3.2',
        title='JS Pulse OHMS Use Case Diagram — Actors and System Functions',
        height_inches=5.0,
        caption_text='Figure 3.2: Use Case Diagram showing the four system actors and their permitted interactions with the JS Pulse OHMS modules')

    para(doc, "The Use Case Diagram formally identifies the four distinct human actors who interact with the JS Pulse OHMS system and maps each actor to the specific system functions they are permitted to invoke. The four actors are: the Nurse or Receptionist, the Consulting Doctor, the Pharmacist, and the Clinic Administrator. Each actor corresponds to a defined role in the JSP Patratu Occupational Health Centre's operational hierarchy, and their access permissions within the application reflect the actual clinical responsibilities of each role.")
    para(doc, "The Nurse or Receptionist actor initiates the patient encounter workflow by registering the patient's employee identification number and personal details, and recording initial vital signs such as blood pressure, body temperature, pulse rate, and blood oxygen saturation (SpO2). This use case is implemented in the OPDCounter.jsx component, which writes the initial patient record to the cms_daily_opd_sheet IndexedDB object store. The Nurse actor has read-only access to the OPD queue and cannot modify consultation or prescription data entered by the doctor.")
    para(doc, "The Consulting Doctor actor can access the consultation interface to view the active patient queue, record examination findings, enter diagnoses, and draft electronic prescriptions including medicine names, dosage instructions, and treatment duration. The doctor's use cases are implemented across the OPDForm.jsx and PrescriptionBuilder.jsx components. Once a prescription is submitted, the patient record's extracted field is set to false, which flags it for automatic extraction by the pharmacy sync engine during its next polling cycle.")
    para(doc, "The Pharmacist actor handles all downstream prescription processing. Their use cases include viewing the pending dispensing queue, marking prescriptions as dispensed, manually initiating stock deduction for consumed medicines, and monitoring current stock levels and expiry dates of all medicines in the clinic inventory. The Clinic Administrator has the broadest permission set, encompassing all the above use cases plus exclusive access to medicine master data management and the compliance report generation module, which produces PDF and Excel reports for regulatory submission under the Factories Act, 1948.")

    # -----------------------------------------------------------
    # 3.3  Activity Diagram
    # -----------------------------------------------------------
    doc.add_heading('3.3 Activity Diagram — Patient Clinical Journey', level=2)

    insert_figure(doc,
        fig_num='Figure 3.3',
        title='Patient Clinical Journey Activity Diagram',
        height_inches=6.5,
        caption_text='Figure 3.3: Activity Diagram showing the complete patient journey from registration through consultation, prescription, and pharmacy dispensing')

    para(doc, "The Activity Diagram models the complete end-to-end workflow of a patient encounter at the JSP Patratu Occupational Health Centre, tracing every action from the moment of arrival at the reception counter to the dispensing of prescribed medication at the pharmacy window. This diagram spans the responsibilities of three distinct operational roles (Nurse, Doctor, and Pharmacist) and includes the fully automated background synchronization step that requires no human intervention, demonstrating how the application automates what was previously a manual paper-transfer process between departments.")
    para(doc, "The activity begins at the Start node when a patient enters the clinic. The nurse opens the OPDCounter.jsx component, searches for the patient by their employee code, and enters the current day's vital measurements. This action writes a new JSON record to the cms_daily_opd_sheet IndexedDB object store. The record initially contains the patient's identity, vitals, and a timestamp, with the medicines and diagnosis fields left empty, and the extracted field pre-initialized to false. The patient's name then appears in the doctor's consultation queue, which is rendered by polling the same object store every 10 seconds.")
    para(doc, "The doctor selects the patient from the queue, performs the examination, records findings in free-text diagnosis fields, and uses the PrescriptionBuilder interface to select medicines from the master stock database. Each selected medicine is added to an in-memory medicines array with its name, dose, frequency, and duration. When the doctor clicks Submit, the entire record — now complete with diagnosis and prescription — is written back to cms_daily_opd_sheet using the sheetDB.js put() method, with the extracted field still set to false.")
    para(doc, "The decision node labeled 'Sync Queue Sweep?' represents the 10-second setInterval polling loop running in DispenseMedicine.jsx. Every 10 seconds, it reads all records from cms_daily_opd_sheet, filters for those where extracted equals false, creates one dispense log entry per medicine line in cms_dispense_log, then updates the original OPD record's extracted field to true to prevent duplicate processing. The pharmacist processes each queue entry, marks it as dispensed, and the stock deduction algorithm in DailyConsume.jsx decrements the corresponding medicine quantities in cms_medstock_data. The workflow concludes when stock has been successfully adjusted.")

    # -----------------------------------------------------------
    # 3.4  Sequence Diagram — IPC Communication Flow
    # -----------------------------------------------------------
    doc.add_heading('3.4 Sequence Diagram — Electron IPC Communication Flow', level=2)

    insert_figure(doc,
        fig_num='Figure 3.4',
        title='Electron IPC Communication Sequence Diagram — Headless PDF Print Transaction',
        height_inches=5.5,
        caption_text='Figure 3.4: Sequence Diagram showing the six-component IPC message chain from user click to PDF generation and native file save')

    para(doc, "The Sequence Diagram captures the precise temporal ordering of all messages exchanged between the system components during the Print Preview operation — the most complex and security-sensitive IPC transaction in the entire JS Pulse OHMS codebase. This operation requires the React UI to bridge the Chromium sandbox boundary, invoke a Node.js-privileged printing function, wait for an asynchronous PDF rendering process to complete, and deliver the result back to the user through the operating system's native shell. The entire transaction traverses six distinct component boundaries and involves three different JavaScript execution contexts.")
    para(doc, "The sequence begins when the clinic administrator clicks the Print Preview button in the compliance report generation UI. The React component calls window.electron.previewPrint(htmlPayload), where htmlPayload is a serialized string containing the fully formatted HTML report including inline CSS styles, embedded Recharts SVG charts, and Mermaid.js diagram markup. Internally, the preload function translates this into ipcRenderer.invoke('preview-print', htmlPayload), which sends the serialized payload as a structured IPC message to the Electron Main Process.")
    para(doc, "In electron/main.js, the ipcMain.handle('preview-print') listener creates a new hidden BrowserWindow instance using new BrowserWindow({ show: false }), which spins up a fresh, invisible Chromium rendering context. The HTML content is loaded using win.loadURL() with a data URL encoding. The system then uses a setTimeout with a 2,500-millisecond delay before calling win.webContents.printToPDF(). This delay is not arbitrary — it is the minimum time required for Mermaid.js CDN to initialize, parse all diagram markup, and render SVG elements into the DOM, ensuring the final PDF contains fully rendered visual content rather than raw diagram code.")
    para(doc, "After the timeout, printToPDF() generates a binary PDF buffer written to a temporary file in the operating system's temporary directory using fs.writeFileSync. The Electron dialog.showSaveDialog API presents the user with a native Windows Save As dialog, allowing them to choose the final file destination. Once confirmed, the temporary file is copied to the chosen path using fs.copyFileSync, and the IPC handler resolves the Promise with a success result that propagates back through the contextBridge to the React component, which displays a confirmation toast notification to the clinic administrator.")

    # -----------------------------------------------------------
    # 3.5  Electron App Lifecycle
    # -----------------------------------------------------------
    doc.add_heading('3.5 Electron Application Lifecycle and Context Isolation', level=2)

    insert_figure(doc,
        fig_num='Figure 3.5(a)',
        title='Electron App Lifecycle — Main Process Boot Sequence (Part 1 of 2)',
        height_inches=5.0,
        caption_text='Figure 3.5(a): Main Process boot sequence from executable launch through BrowserWindow creation and preload script injection')

    insert_figure(doc,
        fig_num='Figure 3.5(b)',
        title='Electron App Lifecycle — DB Connection and Dashboard Mount (Part 2 of 2)',
        height_inches=5.0,
        caption_text='Figure 3.5(b): Renderer Process initialization — IndexedDB connection verification, data hydration, and Dashboard mount')

    para(doc, "The Electron Application Lifecycle diagram illustrates the precise sequence of initialization steps that must complete successfully before a clinic staff member can interact with the clinical dashboard. The lifecycle is split into two phases: the Main Process initialization phase (Figure 3.5a) and the Renderer Process initialization phase (Figure 3.5b). These two phases execute sequentially; the Renderer phase cannot begin until the Main Process has fully established the security configuration and IPC channel registrations.")
    para(doc, "The Main Process initialization begins when the Electron executable is launched. The electron/main.js entry point runs in the Node.js environment and immediately registers all IPC channel handlers using ipcMain.handle for each named channel (save-local-data, load-local-data, preview-print, export-excel, print-to-pdf). After handler registration, the app.whenReady() Promise resolves and the primary BrowserWindow is created with the security configuration: contextIsolation: true, nodeIntegration: false, and webSecurity: true.")
    para(doc, "With the BrowserWindow created, Electron injects preload.js before loading any content. The preload script executes in a privileged intermediate V8 context and uses contextBridge.exposeInMainWorld('electron', {...}) to attach five whitelisted functions to window.electron: saveLocalData, loadLocalData, previewPrint, saveExcelFile, and printToPDF. Only after this exposure does Electron load the React application's index.html bundle.")
    para(doc, "The Renderer Process initialization begins with React mounting the App.jsx root component. A useEffect hook with an empty dependency array runs immediately after mount, executing three sequential initialization tasks: detecting the Electron environment and installing the localStorage Proxy Engine; calling sheetDB.openConnection() to establish the IndexedDB connection pool with automatic recovery; and loading all clinical data stores into React state using Promise.all(). Only after all three tasks complete does the application render the main clinical dashboard, replacing the loading splash screen with the fully hydrated clinical interface.")

    # -----------------------------------------------------------
    # 3.6  IndexedDB Data Flow
    # -----------------------------------------------------------
    doc.add_heading('3.6 IndexedDB Data Flow and Schema Migration', level=2)

    insert_figure(doc,
        fig_num='Figure 3.6(a)',
        title='IndexedDB Migration Hook and Storage Quota Evaluation (Part 1 of 2)',
        height_inches=5.0,
        caption_text='Figure 3.6(a): Migration hook evaluation — localStorage byte-size calculation and 4.5 MB quota threshold check')

    insert_figure(doc,
        fig_num='Figure 3.6(b)',
        title='IndexedDB Batch Write Execution and Legacy Data Purge (Part 2 of 2)',
        height_inches=5.0,
        caption_text='Figure 3.6(b): Batch write execution to IndexedDB, write validation, legacy key purge, and emergency JSON fallback')

    para(doc, "The IndexedDB Data Flow diagrams document the storage management and migration pipeline that protects the JS Pulse OHMS clinical database from the browser's 5MB localStorage quota limitation. Because all clinical data is stored locally without a remote server, and because the clinic may accumulate thousands of patient records over months of operation, the risk of reaching the browser storage limit is real and must be handled gracefully. The migration pipeline implements an automated, background defense mechanism that transparently migrates aging data from the quota-limited localStorage cache to the much larger IndexedDB storage when the cumulative size approaches the threshold.")
    para(doc, "The migration hook (Figure 3.6a) is triggered during the application's startup initialization sequence and again on every significant data write. It calculates the total byte size of all localStorage keys by iterating through localStorage.length and summing (key.length + value.length) * 2 for each entry, using the UTF-16 encoding formula. If the calculated total exceeds 4.5MB, the migration hook proceeds to the aggregation phase. If not, it logs a healthy status and exits.")
    para(doc, "The aggregation phase (Figure 3.6b) identifies all localStorage keys with the cms_ prefix convention and groups them into a batch array. For each key in the batch, sheetDB.js uses the IndexedDB put() method within a readwrite transaction. After each successful transaction completion event, the system marks that key as migrated. Once all keys are written to IndexedDB, localStorage.removeItem() is called for each migrated key, freeing the quota-limited cache space.")
    para(doc, "This two-phase commit approach (write to IndexedDB first, then delete from localStorage) ensures that no data is ever lost due to a partial failure: if the IndexedDB write fails for any key, the deletion does not proceed for that key, and the data remains safely in localStorage until the next migration attempt. In the event of a complete IndexedDB failure, the system executes an emergency fallback that calls window.electron.saveLocalData() to write all the data directly to the Windows file system as JSON backup files at C:\\OHSData, ensuring business continuity even in catastrophic storage failure scenarios.")

    # -----------------------------------------------------------
    # 3.7  ER Diagram
    # -----------------------------------------------------------
    doc.add_heading('3.7 Entity-Relationship (ER) Diagram', level=2)

    insert_figure(doc,
        fig_num='Figure 3.7',
        title='ER Diagram — PATIENT_VISITS, DISPENSE_LOG, and MED_STOCK Entities',
        height_inches=6.5,
        caption_text='Figure 3.7: Entity-Relationship Diagram showing the three IndexedDB object stores and their logical 1:N and N:1 relationships')

    para(doc, "Although JS Pulse OHMS uses IndexedDB rather than a traditional SQL relational database, the logical relationships between its three primary data entities are formally equivalent to those of a relational schema and can be modeled using an Entity-Relationship (ER) diagram. This formal model is important for understanding how data integrity is maintained across the application, how the automated prescription sync pipeline links clinical and pharmacy records, and how future migrations to a remote database system such as PostgreSQL could be structured if the application is scaled beyond a single offline workstation.")
    para(doc, "The first entity, PATIENT_VISITS, corresponds to the cms_daily_opd_sheet IndexedDB object store. Its attributes are: date (a string in YYYY-MM-DD format), empCode (the JSP employee identification number, serving as the natural primary key), patientName, drName, medicinesDetails (a JSON-serialized array of prescribed medicines with name, dose, frequency, and duration sub-fields), and the extracted boolean flag. The extracted field is the sole driver of the automated OPD-to-pharmacy synchronization pipeline: records with extracted set to false are queued for processing, while records with extracted set to true have already been forwarded to the pharmacy queue.")
    para(doc, "The second entity, DISPENSE_LOG, corresponds to the cms_dispense_log object store. Each record is created automatically by the sync engine. Its primary key is a system-generated unique string combining Date.now() with Math.random().toString(36).substr(2,9) to prevent collisions. Its foreign key reference is medicineName, which links it to the MED_STOCK entity. The status field tracks the dispensing lifecycle: it begins as 'Pending' when created and transitions to 'Deducted' when the pharmacist confirms dispensing and the stock deduction algorithm completes successfully.")
    para(doc, "The third entity, MED_STOCK, corresponds to the cms_medstock_data object store and serves as the master pharmaceutical inventory ledger. Its primary key is a system-generated unique ID. Key attributes include medicineName (used as the matching key for stock deduction lookups via case-insensitive String comparison), category (therapeutic classification), quantity (decremented by each dispensing event), expiry (used to flag near-expiry stock), and reorderLevel (the minimum threshold below which the system generates automated low-stock alerts in the dashboard). The two logical relationships are a 1:N relationship between PATIENT_VISITS and DISPENSE_LOG (one OPD visit generates multiple dispense entries) and an N:1 relationship between DISPENSE_LOG and MED_STOCK (multiple dispense entries reference one medicine stock record).")

    # -----------------------------------------------------------
    # 3.8  localStorage Proxy Engine
    # -----------------------------------------------------------
    doc.add_heading('3.8 localStorage Proxy Engine and Storage Architecture', level=2)

    insert_figure(doc,
        fig_num='Figure 3.8',
        title='localStorage Proxy Engine — Data Interception and Multi-Tier Routing Flow',
        height_inches=5.0,
        caption_text='Figure 3.8: localStorage Proxy Engine showing the three-tier write strategy: in-memory Map, browser localStorage, and native file system')

    para(doc, "The localStorage Proxy Engine is one of the most innovative architectural features of JS Pulse OHMS. Standard web applications store data using the browser's native localStorage API, which is limited to 5MB of storage per origin. For an enterprise clinical management system expected to store multiple years of patient records, this constraint is fundamentally incompatible with the operational requirements. The localStorage Proxy Engine solves this by transparently intercepting all localStorage operations at the API level and routing them through a multi-tier storage pipeline without requiring any changes to the hundreds of localStorage.setItem() and localStorage.getItem() calls distributed throughout the React component tree.")
    para(doc, "The proxy is implemented in src/main.jsx using JavaScript's native Proxy object, which is a built-in mechanism for intercepting and customizing operations on JavaScript objects. A Proxy wraps the original window.localStorage object and intercepts the get trap. When a React component calls localStorage.setItem(key, value), the proxy intercepts this call and performs three operations simultaneously: it writes the value to an in-memory Map cache (memoryStorage) for instant synchronous read-back; it calls the original localStorage.setItem() to maintain compatibility; and it asynchronously calls window.electron.saveLocalData(key, value) to persist the data to the Windows file system at C:\\OHSData through the Electron IPC bridge.")
    para(doc, "This three-layer write strategy provides distinct performance and reliability guarantees at each tier. The in-memory Map tier provides O(1) read performance with zero I/O latency, ensuring that the React component tree can re-render at 60 frames per second without any storage bottlenecks. The localStorage tier provides browser-native persistence across application restarts, maintaining compatibility with development environments where Electron IPC is not available. The file system tier provides unlimited capacity bounded only by the Windows disk size, and full disaster-recovery capability ensuring all clinical data survives even a complete IndexedDB corruption event or browser storage quota wipe.")
    para(doc, "The proxy architecture also enables the quota migration system described in Section 3.6. Because all writes are intercepted at the proxy level, the migration trigger can accurately track total storage utilization in real time. The proxy's transparent nature means that this entire multi-tier storage management system operates completely invisibly to all clinical module components, which continue to use the simple localStorage API as if the 5MB limit did not exist. This backward compatibility was an explicit design requirement to ensure that none of the forty-plus React components required modification when the storage architecture was upgraded from a simple localStorage approach to the current multi-tier system.")

    # SAVE
    out_path = 'JSPulse_OHMS_Chapter3_WithSpaces.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == '__main__':
    main()
