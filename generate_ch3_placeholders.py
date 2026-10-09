import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def setup_doc(doc):
    """Set A4 page size, 1-inch margins, Times New Roman 12pt base style."""
    for section in doc.sections:
        section.page_width  = Inches(8.27)
        section.page_height = Inches(11.69)
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

def para(doc, text, bold=False, space_before=0, space_after=6):
    """Add a justified, 1.5-spaced Times New Roman paragraph."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = bold
    return p

def placeholder(doc, fig_text):
    """Insert a centred, bordered, grey-background figure placeholder box."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.5)
    p.paragraph_format.right_indent = Inches(0.5)

    # Add border shading via paragraph XML
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'E8E8E8')   # light grey background
    pPr.append(shd)

    pBdr = OxmlElement('w:pBdr')
    for side in ('top', 'left', 'bottom', 'right'):
        bdr = OxmlElement(f'w:{side}')
        bdr.set(qn('w:val'), 'single')
        bdr.set(qn('w:sz'), '12')
        bdr.set(qn('w:space'), '4')
        bdr.set(qn('w:color'), '404040')
        pBdr.append(bdr)
    pPr.append(pBdr)

    run = p.add_run(fig_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.bold = True
    run.italic = True

def caption(doc, text):
    """Add an italicised centred caption below a placeholder."""
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(14)
    r = p.runs[0]
    r.italic = True
    r.font.size = Pt(10)
    r.font.name = 'Times New Roman'


def main():
    doc = Document()
    setup_doc(doc)

    # ─────────────────────────────────────────────────────────────
    # CHAPTER 3 TITLE
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('Chapter 3: Advanced UML and Architecture Flows', level=1)

    # ─────────────────────────────────────────────────────────────
    # 3.1  System Architecture Diagram
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.1 System Architecture Diagram', level=2)

    placeholder(doc, '[Insert Figure 3.1: System Architecture Diagram]')
    caption(doc,    'Figure 3.1: JS Pulse OHMS Complete System Architecture')

    para(doc, "The JS Pulse OHMS system architecture is founded on the Electron framework, which merges a Node.js native runtime with a Chromium-based web renderer to produce a full-featured offline desktop application. The architecture is divided into two isolated process domains: the Main Process and the Renderer Process. The Main Process, controlled by electron/main.js, owns all Node.js capabilities including file-system I/O, native Windows dialogs, system tray management, and IndexedDB schema migration. The Renderer Process, controlled by main.jsx and the React 19 component tree, manages the entire clinical user interface including the OPD console, pharmacy dispense queue, medicine stock ledger, periodic examination records, and first aid kit tracker.")
    para(doc, "The security boundary between these two processes is enforced through context isolation. When the BrowserWindow is created in main.js, two flags are explicitly set: contextIsolation: true and nodeIntegration: false. These settings prevent the Renderer Process from importing Node.js modules or accessing system APIs directly. All cross-process communication is routed through a dedicated preload.js script, which is injected by Electron before any web content loads. The preload script uses Electron's contextBridge.exposeInMainWorld API to attach a minimal, whitelisted set of functions to the global window.electron object, making them callable from React components.")
    para(doc, "At the data layer, the architecture uses a three-tier storage model. The first tier is an in-memory Map cache maintained by the localStorage proxy engine injected in main.jsx. This provides sub-millisecond read access for all data rendered in the active React component tree. The second tier is the browser's IndexedDB, accessed exclusively through the sheetDB.js custom wrapper. It stores all clinical records in three primary object stores: cms_daily_opd_sheet (OPD and consultation records), cms_dispense_log (prescription dispensing history), and cms_medstock_data (pharmaceutical inventory). The third tier is the native Windows file system (C:\\OHSData), which stores JSON backup copies of all records via the Electron IPC bridge, providing a disaster-recovery layer that survives even a complete browser storage corruption event.")
    para(doc, "The six functional module groups (Clinical, Pharmacy, Inventory, Reports, System Health, and Administration) are implemented as independent React component subtrees, each reading from and writing to the shared IndexedDB storage through the sheetDB abstraction. This decoupled architecture means that a failure in the Pharmacy module does not affect the OPD module's ability to accept new patient registrations. The automated prescription sync engine, implemented as a setInterval polling loop in DispenseMedicine.jsx, bridges the Clinical and Pharmacy modules by reading unprocessed OPD records every 10 seconds and creating corresponding entries in the dispense queue without any direct inter-component function calls.")

    # ─────────────────────────────────────────────────────────────
    # 3.2  Use Case Diagram
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.2 Use Case Diagram', level=2)

    placeholder(doc, '[Insert Figure 3.2: Use Case Diagram]')
    caption(doc,    'Figure 3.2: JS Pulse OHMS Use Case Diagram — Actors and System Functions')

    para(doc, "The Use Case Diagram formally identifies the four distinct human actors who interact with the JS Pulse OHMS system and maps each actor to the specific system functions they are permitted to invoke. The four actors are: the Nurse or Receptionist, the Consulting Doctor, the Pharmacist, and the Clinic Administrator. Each actor corresponds to a defined role in the JSP Patratu Occupational Health Centre's operational hierarchy, and their access permissions within the application reflect the actual clinical responsibilities of each role.")
    para(doc, "The Nurse or Receptionist actor initiates the patient encounter workflow by registering the patient's employee identification number and personal details, and recording initial vital signs such as blood pressure, body temperature, pulse rate, and blood oxygen saturation (SpO2). This use case is implemented in the OPDCounter.jsx component, which writes the initial patient record to the cms_daily_opd_sheet IndexedDB object store with all medical fields populated. The Nurse actor has read-only access to the OPD queue and cannot modify consultation or prescription data entered by the doctor.")
    para(doc, "The Consulting Doctor actor can access the consultation interface to view the active patient queue, record examination findings, enter diagnoses using the ICD-10 classification system, and draft electronic prescriptions that include medicine names, dosage instructions, and treatment duration. The doctor's use cases are implemented across the OPDForm.jsx and PrescriptionBuilder.jsx components. Once a prescription is submitted, the patient record's extracted field is set to false, which flags it for automatic extraction by the pharmacy sync engine during its next polling cycle.")
    para(doc, "The Pharmacist actor handles all downstream prescription processing. Their use cases include viewing the pending dispensing queue, marking prescriptions as dispensed, manually initiating stock deduction for consumed medicines, and monitoring the current stock levels and expiry dates of all medicines in the clinic's inventory. These functions are implemented across DispenseMedicine.jsx and DailyConsume.jsx. The Clinic Administrator has the broadest permission set, encompassing all the above use cases plus exclusive access to medicine master data management (adding new medicines, updating reorder levels, and removing expired stock entries) and the compliance report generation module, which produces PDF and Excel reports for regulatory submission.")
    para(doc, "The use case architecture directly reflects the role-based navigation routing implemented in App.jsx. Each actor's permitted navigation routes are conditionally rendered based on the active role selection, ensuring that clinical staff cannot accidentally access or modify data outside their operational domain. This role enforcement is purely client-side since the application has no remote authentication server, relying instead on a locally stored role token to determine the active user context.")

    # ─────────────────────────────────────────────────────────────
    # 3.3  Activity Diagram
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.3 Activity Diagram — Patient Clinical Journey', level=2)

    placeholder(doc, '[Insert Figure 3.3: Activity Diagram — Patient Clinical Journey]')
    caption(doc,    'Figure 3.3: Activity Diagram Showing the Complete Patient Workflow')

    para(doc, "The Activity Diagram models the complete end-to-end workflow of a patient encounter at the JSP Patratu Occupational Health Centre, tracing every action from the moment of arrival at the reception counter to the dispensing of prescribed medication at the pharmacy window. This diagram is particularly valuable because it spans the responsibilities of three distinct operational roles (Nurse, Doctor, and Pharmacist) and includes the fully automated background synchronization step that requires no human intervention, demonstrating how the application's architecture automates what was previously a manual paper-transfer process between departments.")
    para(doc, "The activity begins at the Start node when a patient enters the clinic. The nurse opens the OPDCounter.jsx component, searches for the patient by their employee code, and enters the current day's vital measurements. This action writes a new JSON record to the cms_daily_opd_sheet IndexedDB object store. The record initially contains the patient's identity, vitals, and a timestamp, with the medicines and diagnosis fields left empty, and the extracted field pre-initialized to false. The patient's name then appears in the doctor's consultation queue, which is rendered by polling the same object store every 10 seconds.")
    para(doc, "The doctor selects the patient from the queue, performs the examination, records findings in free-text diagnosis fields, and uses the PrescriptionBuilder interface to select medicines from the master stock database. Each selected medicine is added to an in-memory medicines array with its name, dose, frequency, and duration. When the doctor clicks Submit, the entire record — now complete with diagnosis and prescription — is written back to cms_daily_opd_sheet using the sheetDB.js put() method. This single put() call performs an upsert operation, replacing the empty initial record with the fully completed clinical encounter record, with extracted still set to false.")
    para(doc, "The decision node labeled 'Sync Queue Sweep?' represents the 10-second setInterval polling loop running in DispenseMedicine.jsx. Every 10 seconds, it reads all records from cms_daily_opd_sheet, filters for those where extracted equals false, and processes each unextracted record by creating one dispense log entry per medicine line in cms_dispense_log, then updating the original OPD record's extracted field to true to prevent duplicate processing. The pharmacist's queue UI is also refreshed by this same interval, displaying the newly arrived prescriptions as pending dispense entries. The pharmacist processes each entry, clicks Mark as Dispensed, which triggers the stock deduction algorithm in DailyConsume.jsx to decrement the corresponding medicine quantities in cms_medstock_data. The workflow concludes at the End node when stock has been successfully adjusted.")

    # ─────────────────────────────────────────────────────────────
    # 3.4  Sequence Diagram — IPC Communication Flow
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.4 Sequence Diagram — Electron IPC Communication Flow', level=2)

    placeholder(doc, '[Insert Figure 3.4: Sequence Diagram — Electron IPC Communication Flow]')
    caption(doc,    'Figure 3.4: Sequence Diagram Showing the Headless PDF Print IPC Transaction')

    para(doc, "The Sequence Diagram captures the precise temporal ordering of all messages exchanged between the system components during the Print Preview operation — the most complex and security-sensitive IPC transaction in the entire JS Pulse OHMS codebase. This operation requires the React UI to bridge the Chromium sandbox boundary, invoke a Node.js-privileged printing function, wait for an asynchronous PDF rendering process to complete, and deliver the result back to the user through the operating system's native shell. The entire transaction traverses six distinct component boundaries and involves three different JavaScript execution contexts.")
    para(doc, "The sequence begins when the clinic administrator clicks the Print Preview button in the compliance report generation UI. The React component calls window.electron.previewPrint(htmlPayload), where htmlPayload is a serialized string containing the fully formatted HTML report including inline CSS styles, embedded Recharts SVG charts, and Mermaid.js diagram markup. This call invokes the function exposed by preload.js through contextBridge.exposeInMainWorld. Internally, the preload function translates this into ipcRenderer.invoke('preview-print', htmlPayload), which sends the serialized payload as a structured IPC message to the Electron Main Process.")
    para(doc, "In the electron/main.js file, the ipcMain.handle('preview-print') listener receives the message payload. It creates a new hidden BrowserWindow instance using new BrowserWindow({ show: false }), which spins up a fresh, invisible Chromium rendering context. The HTML content is loaded into this hidden window using win.loadURL() with a data URL encoding. The system then attaches a did-finish-load event listener and, critically, uses a setTimeout with a 2,500-millisecond delay before calling win.webContents.printToPDF(). This delay is not arbitrary — it is the minimum time required for the Mermaid.js CDN library to fetch, initialize, parse all diagram markup, and render the SVG elements into the DOM.")
    para(doc, "After the timeout, printToPDF() is called with configuration options specifying A4 page size and full background printing enabled. Chromium's print engine generates a binary PDF buffer, which is written to a temporary file in the operating system's temporary directory using Node.js's fs.writeFileSync. The Electron dialog.showSaveDialog API then presents the user with a native Windows Save As dialog, allowing them to choose the final file destination. Once confirmed, the temporary file is copied to the chosen path using fs.copyFileSync, and the IPC handler resolves the Promise with a success result that propagates back through the contextBridge to the React component, which displays a confirmation toast notification.")

    # ─────────────────────────────────────────────────────────────
    # 3.5  Electron IPC Communication and App Lifecycle
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.5 Electron Application Lifecycle and Context Isolation', level=2)

    placeholder(doc, '[Insert Figure 3.5(a): Electron App Lifecycle — Main Process Boot Sequence (Part 1)]')
    caption(doc,    'Figure 3.5(a): Electron App Lifecycle — Main Process Boot Sequence (Part 1 of 2)')

    placeholder(doc, '[Insert Figure 3.5(b): Electron App Lifecycle — DB Connection and Dashboard Mount (Part 2)]')
    caption(doc,    'Figure 3.5(b): Electron App Lifecycle — DB Connection Verification and Dashboard Mount (Part 2 of 2)')

    para(doc, "The Electron Application Lifecycle diagram illustrates the precise sequence of initialization steps that must complete successfully before a clinic staff member can interact with the clinical dashboard. The lifecycle is split into two phases: the Main Process initialization phase (Figure 3.5a) and the Renderer Process initialization phase (Figure 3.5b). These two phases execute sequentially; the Renderer phase cannot begin until the Main Process has fully established the security configuration and IPC channel registrations.")
    para(doc, "The Main Process initialization begins when the Electron executable is launched. The electron/main.js entry point runs in the Node.js environment and immediately registers all IPC channel handlers using ipcMain.handle for each named channel (save-local-data, load-local-data, preview-print, export-excel, print-to-pdf). This registration must happen before any IPC messages are sent, otherwise the Renderer Process would receive unhandled channel errors. After handler registration, the app.whenReady() Promise resolves and the primary BrowserWindow is created with the security configuration object that enforces contextIsolation: true and nodeIntegration: false.")
    para(doc, "With the BrowserWindow created, Electron injects preload.js into the window's web preferences before loading any content. The preload script executes in a privileged intermediate V8 context that can access both Electron's ipcRenderer API and the browser's window object simultaneously. It uses contextBridge.exposeInMainWorld('electron', {...}) to attach a minimal set of five whitelisted functions to window.electron: saveLocalData, loadLocalData, previewPrint, saveExcelFile, and printToPDF. After this exposure, Electron loads the React application's index.html bundle into the window.")
    para(doc, "The Renderer Process initialization begins with React mounting the App.jsx root component. A useEffect hook with an empty dependency array runs immediately after mount, executing three sequential initialization tasks. First, it checks for the presence of window.electron to confirm the application is running inside Electron (rather than a development browser). If confirmed, it installs the localStorage Proxy Engine by reassigning window.localStorage to a JavaScript Proxy object. Second, it calls sheetDB.openConnection() to establish the IndexedDB connection pool, invoking the auto-recovery routine (which attempts to delete and re-open the database) if the initial connection fails. Third, it loads all clinical data stores into React state using Promise.all(), hydrating the OPD, dispense, stock, and examination states simultaneously. Only after all three tasks complete does the application render the main clinical dashboard, replacing the loading splash screen.")

    # ─────────────────────────────────────────────────────────────
    # 3.6  IndexedDB Data Flow
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.6 IndexedDB Data Flow and Schema Migration', level=2)

    placeholder(doc, '[Insert Figure 3.6(a): IndexedDB Migration Hook and Quota Trigger (Part 1)]')
    caption(doc,    'Figure 3.6(a): IndexedDB Migration Hook and Storage Quota Evaluation (Part 1 of 2)')

    placeholder(doc, '[Insert Figure 3.6(b): IndexedDB Batch Write Execution and Legacy Purge (Part 2)]')
    caption(doc,    'Figure 3.6(b): IndexedDB Batch Write Execution and Legacy Data Purge (Part 2 of 2)')

    para(doc, "The IndexedDB Data Flow diagrams document the storage management and migration pipeline that protects the JS Pulse OHMS clinical database from the browser's 5MB localStorage quota limitation. Because all clinical data is stored locally without a remote server, and because the clinic may accumulate thousands of patient records over months of operation, the risk of reaching the browser storage limit is real and must be handled gracefully. The migration pipeline implements an automated, background defense mechanism that transparently migrates aging data from the quota-limited localStorage cache to the much larger IndexedDB storage when the cumulative size approaches the threshold.")
    para(doc, "The migration hook (Figure 3.6a) is triggered during the application's startup initialization sequence and again on every data write operation that adds significant new data to the store. It calculates the total byte size of all localStorage keys by iterating through the storage index using a for loop over localStorage.length and summing (key.length + value.length) * 2 for each entry (multiplying by 2 because JavaScript strings use UTF-16 encoding, which allocates two bytes per character). If the calculated total exceeds 4.5MB (a conservative threshold below the 5MB browser limit), the migration hook proceeds to the aggregation phase. If not, it logs a healthy status and exits.")
    para(doc, "The aggregation phase (Figure 3.6b) identifies all localStorage keys that correspond to clinical data stores (recognized by the cms_ key prefix convention used throughout the application). It groups these keys into a batch array and calls sheetDB.openConnection() to ensure the IndexedDB connection pool is active. For each key in the batch, it uses the IndexedDB put() method within a readwrite transaction to write the JSON-parsed record array to the corresponding IndexedDB object store. After each successful transaction, the transaction complete event fires and the system marks that key as successfully migrated.")
    para(doc, "Once all keys in the batch have been successfully written to IndexedDB, the system calls localStorage.removeItem() for each migrated key, purging it from the quota-limited cache and freeing the occupied space. This two-phase commit approach (write to IndexedDB first, then delete from localStorage) ensures that no data is ever lost due to a partial failure: if the IndexedDB write fails for any key, the deletion does not proceed for that key, and the data remains safely in localStorage until the next migration attempt. In the event of a complete IndexedDB failure (such as a corrupted database), the system executes an emergency fallback that calls window.electron.saveLocalData() to write all the data directly to the Windows file system as JSON backup files, ensuring business continuity even in catastrophic storage failure scenarios.")

    # ─────────────────────────────────────────────────────────────
    # 3.7  ER Diagram
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.7 Entity-Relationship (ER) Diagram', level=2)

    placeholder(doc, '[Insert Figure 3.7: ER Diagram — PATIENT_VISITS, DISPENSE_LOG, and MED_STOCK Entities]')
    caption(doc,    'Figure 3.7: Entity-Relationship Diagram for the JS Pulse OHMS IndexedDB Schema')

    para(doc, "Although JS Pulse OHMS uses IndexedDB — a non-relational, key-value object store — rather than a traditional SQL relational database, the logical relationships between its three primary data entities are formally equivalent to those of a relational schema and can be modeled using an Entity-Relationship (ER) diagram. This formal model is important for understanding how data integrity is maintained across the application, how the automated prescription sync pipeline links clinical and pharmacy records, and how future migrations to a remote database system (such as PostgreSQL or MySQL) could be structured if the application is scaled beyond a single offline workstation.")
    para(doc, "The first entity, PATIENT_VISITS, corresponds to the cms_daily_opd_sheet IndexedDB object store. Its attributes are: date (a string in YYYY-MM-DD format representing the consultation date), empCode (the JSP employee identification number, serving as the natural primary key for each visit), patientName (the employee's full name), drName (the consulting physician's name), medicinesDetails (a JSON-serialized string encoding the array of prescribed medicines, each with name, dose, frequency, and duration sub-fields), and the critical extracted boolean flag. The extracted field is the sole driver of the automated OPD-to-pharmacy synchronization pipeline: records with extracted set to false are queued for processing by the DispenseMedicine sync engine, while records with extracted set to true have already been forwarded to the pharmacy queue and are considered read-only archived encounters.")
    para(doc, "The second entity, DISPENSE_LOG, corresponds to the cms_dispense_log object store. Each dispense record is created automatically by the sync engine when it processes an unextracted OPD record. Its primary key is a system-generated unique string combining the current timestamp (Date.now()) with a random alphanumeric suffix (Math.random().toString(36).substr(2, 9)) to prevent key collisions. Its foreign key reference is medicineName, which links it to the MED_STOCK entity. The status field tracks the dispensing lifecycle: it begins as 'Pending' when created by the sync engine and transitions to 'Deducted' when the pharmacist confirms dispensing and the stock deduction algorithm completes successfully.")
    para(doc, "The third entity, MED_STOCK, corresponds to the cms_medstock_data object store. It serves as the master pharmaceutical inventory ledger for the clinic. Its primary key is a system-generated unique ID string. Its key attributes include medicineName (the canonical medicine name, used as the matching key for stock deduction lookups), category (the therapeutic classification such as analgesic, antibiotic, or antipyretic), quantity (the current available stock count, which is decremented by each successful dispensing event), expiry (the medicine expiry date, used by the inventory management module to identify and flag near-expiry stock), and reorderLevel (the minimum stock threshold below which the system generates an automated low-stock alert in the clinic dashboard). The two logical relationships are a 1:N relationship (one OPD visit generates many dispense entries) and an N:1 relationship (many dispense entries reference one medicine stock record).")

    # ─────────────────────────────────────────────────────────────
    # 3.8  localStorage Proxy and Storage Architecture
    # ─────────────────────────────────────────────────────────────
    doc.add_heading('3.8 localStorage Proxy Engine and Storage Architecture', level=2)

    placeholder(doc, '[Insert Figure 3.8: localStorage Proxy Engine — Data Interception and Routing Flow]')
    caption(doc,    'Figure 3.8: localStorage Proxy Engine and Multi-Tier Storage Architecture Flow')

    para(doc, "The localStorage Proxy Engine is one of the most innovative architectural features of JS Pulse OHMS. Standard web applications store data using the browser's native localStorage API, which is limited to 5MB of storage per origin. For an enterprise clinical management system expected to store multiple years of patient records, this constraint is fundamentally incompatible with the operational requirements. The localStorage Proxy Engine solves this by transparently intercepting all localStorage operations at the API level and routing them through a multi-tier storage pipeline without requiring any changes to the hundreds of localStorage.setItem() and localStorage.getItem() calls distributed throughout the React component tree.")
    para(doc, "The proxy is implemented in src/main.jsx using JavaScript's native Proxy object, which is a built-in mechanism for intercepting and customizing operations on JavaScript objects. A Proxy wraps the original window.localStorage object and intercepts the get trap (which captures both property accesses and method calls). When a React component calls localStorage.setItem(key, value), the proxy intercepts this call and performs three operations simultaneously: it writes the value to an in-memory Map cache (memoryStorage) for instant synchronous read-back, it calls the original localStorage.setItem() to maintain compatibility with any direct DOM access, and it asynchronously calls window.electron.saveLocalData(key, value) to persist the data to the Windows file system at C:\\OHSData through the Electron IPC bridge.")
    para(doc, "This three-layer write strategy provides distinct performance and reliability guarantees at each tier. The in-memory Map tier provides O(1) read performance with zero I/O latency, ensuring that the React component tree can re-render at 60 frames per second without any storage bottlenecks. The localStorage tier provides browser-native persistence across tab refreshes and browser restarts, maintaining compatibility with development environments where Electron IPC is not available. The file system tier, accessible only through the Electron IPC bridge, provides unlimited capacity (bounded only by the Windows disk size) and disaster-recovery capability, ensuring that all clinical data survives even a complete IndexedDB corruption event or a browser storage quota wipe.")
    para(doc, "The proxy architecture is also critical for enabling the quota migration system described in Section 3.6. Because all writes are intercepted at the proxy level, the migration trigger can accurately track total storage utilization in real time, identifying when the localStorage portion is approaching the 5MB limit and proactively initiating the migration to IndexedDB before any data loss occurs. The proxy's transparent nature means that this entire multi-tier storage management system operates completely invisibly to all clinical module components, which continue to use the simple localStorage.setItem() and localStorage.getItem() API as if the 5MB limit did not exist. This backward compatibility was an explicit design requirement to ensure that none of the forty-plus React components required modification when the storage architecture was upgraded.")

    # SAVE
    out_path = 'JSPulse_OHMS_Chapter3_PlaceholderVersion.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == '__main__':
    main()
