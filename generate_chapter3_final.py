import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT, WD_SECTION_START

IMG_DIR = 'diagram_images_hq'

# Exact pixel dims of every image used in Chapter 3
DIAGRAM_DIMS = {
    'diagram_2.png':  (2897, 1118),
    'diagram_13.png': (711,  1313),
    'diagram_14.png': (849,  1837),
    'diagram_15.png': (998,  1561),
    'diagram_16.png': (1044, 1534),
    'diagram_17.png': (793,  1496),
    'diagram_18.png': (612,  1095),
    'diagram_4.png':  (2225, 858),
    'diagram_12.png': (2955, 1641),
    'diagram_23.png': (2955, 745),   # Use Case
    'diagram_24.png': (711,  2722),  # Activity (tall -> split)
    'diagram_25.png': (2955, 599),   # DFD
    'diagram_26.png': (803,  3689),  # ER (very tall -> split)
}

# Physical A4 page area for images
PORTRAIT_MAX_W   = 6.27   # 8.27 - 2*1.0 margins
PORTRAIT_MAX_H   = 9.69   # 11.69 - 2*1.0 margins
LANDSCAPE_MAX_W  = 9.69   # 11.69 - 2*1.0 margins
LANDSCAPE_MAX_H  = 6.27   # 8.27 - 2*1.0 margins

def fit_in(img_w_px, img_h_px, max_w_in, max_h_in):
    """Scale image to fit within max_w x max_h, preserving aspect ratio."""
    ratio = img_w_px / img_h_px
    w = min(img_w_px / 300.0, max_w_in)
    h = w / ratio
    if h > max_h_in:
        h = max_h_in
        w = h * ratio
    return round(w, 4), round(h, 4)

def setup_portrait(section):
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width  = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin   = Inches(1.0)
    section.right_margin  = Inches(1.0)

def setup_landscape(section):
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width  = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin   = Inches(1.0)
    section.right_margin  = Inches(1.0)

def add_para(doc, text, space_before=0, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_caption(doc, text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(12)
    r = p.runs[0]
    r.italic = True
    r.font.size = Pt(10)
    r.font.name = 'Times New Roman'

def insert_diagram(doc, img_filename, caption_text):
    """
    Inserts one diagram on its own page.
    Automatically chooses portrait or landscape, scales to fit 300 DPI or page-fit
    (whichever is smaller), and restores portrait for subsequent text.
    """
    img_path = os.path.join(IMG_DIR, img_filename)
    if not os.path.exists(img_path):
        add_para(doc, f"[Diagram not found: {img_filename}]")
        return

    px_w, px_h = DIAGRAM_DIMS[img_filename]
    natural_w_in = px_w / 300.0

    # Choose orientation based on natural width
    if natural_w_in > PORTRAIT_MAX_W:
        # Wide image -> landscape page
        diag_w, diag_h = fit_in(px_w, px_h, LANDSCAPE_MAX_W, LANDSCAPE_MAX_H - 0.6)
        sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
        setup_landscape(sec)
    else:
        # Tall or square image -> portrait page
        diag_w, diag_h = fit_in(px_w, px_h, PORTRAIT_MAX_W, PORTRAIT_MAX_H - 0.6)
        sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
        setup_portrait(sec)

    # Insert image
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(4)
    p.add_run().add_picture(img_path, width=Inches(diag_w), height=Inches(diag_h))

    add_caption(doc, caption_text)

    # Return to portrait for text that follows
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_portrait(sec2)

def insert_split_diagram(doc, img_filename, part_labels):
    """
    For very tall images: split vertically into equal-height strips
    and place each strip on its own portrait page.
    part_labels: list of caption strings, one per strip.
    """
    from PIL import Image as PILImage
    img_path = os.path.join(IMG_DIR, img_filename)
    if not os.path.exists(img_path):
        add_para(doc, f"[Diagram not found: {img_filename}]")
        return

    img = PILImage.open(img_path)
    full_w, full_h = img.size
    n = len(part_labels)
    strip_h = full_h // n

    for i, caption in enumerate(part_labels):
        top    = i * strip_h
        bottom = (i + 1) * strip_h if i < n - 1 else full_h
        strip  = img.crop((0, top, full_w, bottom))

        tmp_path = f'_tmp_strip_{img_filename}_{i}.png'
        strip.save(tmp_path)

        s_w, s_h = strip.size
        diag_w, diag_h = fit_in(s_w, s_h, PORTRAIT_MAX_W, PORTRAIT_MAX_H - 0.6)

        sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
        setup_portrait(sec)

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after  = Pt(4)
        p.add_run().add_picture(tmp_path, width=Inches(diag_w), height=Inches(diag_h))
        add_caption(doc, caption)

    # Cleanup tmp files
    for i in range(n):
        tmp = f'_tmp_strip_{img_filename}_{i}.png'
        if os.path.exists(tmp):
            os.remove(tmp)

    # Return to portrait
    sec3 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_portrait(sec3)


def main():
    doc = Document()
    setup_portrait(doc.sections[0])

    # Apply base Normal style
    ns = doc.styles['Normal']
    ns.font.name = 'Times New Roman'
    ns.font.size = Pt(12)
    for i in range(1, 5):
        hs = doc.styles[f'Heading {i}']
        hs.font.name = 'Times New Roman'
        hs.font.color.rgb = RGBColor(0, 0, 0)

    # ==========================================================
    # CHAPTER 3 HEADING
    # ==========================================================
    doc.add_heading('Chapter 3: Advanced UML and Architecture Flows', level=1)

    # ----------------------------------------------------------
    # 3.1 System Architecture Diagram
    # ----------------------------------------------------------
    doc.add_heading('3.1 System Architecture Diagram', level=2)
    add_para(doc, "The JS Pulse OHMS system architecture is built on a dual-process Electron framework that separates the user interface from the privileged system operations layer. The Renderer Process hosts the entire React 19 application, including all clinical modules such as the OPD console, pharmacy dispensary, stock manager, and report generator. This process runs inside a sandboxed Chromium environment with no direct access to the operating system. The Main Process hosts the Node.js runtime environment and handles all privileged tasks including file system operations, native print dialogs, and IndexedDB schema management.")
    add_para(doc, "The two processes are connected by the Electron IPC (Inter-Process Communication) bridge, implemented through a preload.js script. The contextBridge.exposeInMainWorld API exposes a minimal, whitelisted set of callable functions into the browser's window object. This design ensures that even if a React component is compromised through an XSS vulnerability, it cannot access Node.js APIs or the file system directly. All sensitive operations are routed through named IPC channels and validated by the Main Process before execution.")
    add_para(doc, "At the data layer, the application uses a custom sheetDB.js wrapper over IndexedDB as its primary storage engine, replacing the standard browser localStorage that is limited to 5MB. Additionally, a localStorage Proxy Engine intercepts all getItem and setItem calls made by the React components and transparently re-routes write operations to the native file system via the IPC bridge. This creates a transparent, backward-compatible caching layer that supports datasets exceeding 100MB while maintaining the standard Web Storage API contract for all React components.")

    insert_diagram(doc, 'diagram_12.png',
                   'Figure 3.1: JS Pulse OHMS Complete System Architecture Overview (A4 Landscape, 300 DPI)')

    add_para(doc, "Figure 3.1 illustrates the complete macro-level architecture showing the Electron native wrapper surrounding the React Renderer and Node.js Main process. The six core module groups visible in the diagram (Clinical, Pharmacy, Inventory, Reports, System Health, and Administration) each communicate with the shared IndexedDB storage through the sheetDB.js abstraction layer. The outward-facing arrows represent OS-level integration points including the Windows file system for JSON backups, the native printer interface for compliance documents, and the system tray for persistent background operation.")

    # ----------------------------------------------------------
    # 3.2 Use Case Diagram
    # ----------------------------------------------------------
    doc.add_heading('3.2 Use Case Diagram', level=2)
    add_para(doc, "The Use Case Diagram defines all the functional interactions between the four distinct system actors and the JS Pulse OHMS application. The four identified actors are: the Nurse or Receptionist, who is responsible for patient registration and vital sign recording at the clinic entrance; the Consulting Doctor, who performs medical examination, records diagnoses, and drafts electronic prescriptions; the Pharmacist, who processes the prescription queue and manages medication dispensing and inventory; and the Clinic Administrator, who has elevated privileges to manage the master medicine stock, configure system settings, and generate regulatory compliance reports.")
    add_para(doc, "The use cases are organized into a layered structure. The primary clinical workflow begins with patient registration and flows through consultation, prescription drafting, pharmacy queue processing, and stock deduction. Each use case encapsulates a distinct business function that maps directly to a React component within the codebase. For example, the Register Patient and Record Vitals use case corresponds to the OPDCounter.jsx component, while the Dispense Prescribed Medication use case is implemented within DispenseMedicine.jsx.")
    add_para(doc, "The use case architecture reflects the role-based access control (RBAC) model embedded within the application's routing system. Each actor can only access the navigation routes and data operations that correspond to their assigned role. The Admin actor has the broadest set of permissions, including access to all use cases available to the other three actors plus exclusive access to system-wide audit logs and stock configuration. This role hierarchy ensures data integrity and prevents unauthorized modification of clinical records.")

    insert_diagram(doc, 'diagram_23.png',
                   'Figure 3.2: JS Pulse OHMS Use Case Diagram — All Actors and System Functions (A4 Landscape, 300 DPI)')

    add_para(doc, "Figure 3.2 shows the complete use case diagram with all four actors positioned on the left side (Nurse, Doctor, Pharmacist, Administrator) and the seven primary use cases organized in the central box. Each actor's arrows trace their permitted interactions. The Doctor connects to Consultation and Prescription use cases; the Pharmacist connects to Dispensing, Stock Deduction, and Inventory Management; the Nurse connects to Registration only; and the Administrator connects to Inventory Management and Report Generation, in addition to being able to perform all other roles as needed during off-hours clinic operation.")

    # ----------------------------------------------------------
    # 3.3 Activity Diagram
    # ----------------------------------------------------------
    doc.add_heading('3.3 Activity Diagram — Patient Clinical Journey', level=2)
    add_para(doc, "The Activity Diagram models the complete sequential workflow that a patient undergoes from the moment of arrival at the JSP Patratu Occupational Health Centre to the final dispensing of prescribed medication. This end-to-end workflow spans three distinct operational stations: the reception desk (managed by the nurse), the consulting room (managed by the doctor), and the pharmacy counter (managed by the pharmacist). Understanding this activity flow is critical to appreciating the design decisions made in the application's module architecture and data synchronization pipeline.")
    add_para(doc, "The workflow begins with patient registration at the reception desk, where the nurse enters the patient's employee identification number, personal details, and records initial vital signs such as blood pressure, temperature, and pulse rate. This data is immediately written to the cms_daily_opd_sheet object store in IndexedDB. The patient is then added to the doctor's consultation queue, which is rendered in real-time by the OPDCounter.jsx component using a 10-second polling interval to detect new arrivals.")
    add_para(doc, "After the doctor completes the consultation and records the diagnosis with prescribed medications, the patient record is updated with the extracted field set to false, signaling to the pharmacy sync engine that a new unprocessed prescription exists. The automated background sync engine (a setInterval running in DispenseMedicine.jsx) sweeps the OPD store every 10 seconds and extracts all unprocessed prescription records into the cms_dispense_log store, creating one dispense entry per medicine line. The pharmacist then processes these queue entries, marks them as dispensed, and the stock deduction algorithm atomically decrements the corresponding medicines in cms_medstock_data. The workflow concludes with the patient receiving their medication and a system-generated dispensing receipt.")

    insert_diagram(doc, 'diagram_24.png',
                   'Figure 3.3: Patient Clinical Journey Activity Diagram (A4 Portrait, 300 DPI)')

    add_para(doc, "Figure 3.3 depicts the complete activity flow from the Start node through registration, queue management, consultation, prescription drafting, automated sync polling, pharmacy dispensing, and stock deduction to the End node. The decision diamond labeled 'Sync Queue Sweep?' represents the 10-second background polling mechanism implemented through JavaScript's setInterval API. This continuous polling eliminates the need for manual page refreshes or push notifications, providing a seamless real-time coordination experience between the OPD and pharmacy stations without requiring any network infrastructure.")

    # ----------------------------------------------------------
    # 3.4 Sequence Diagram — IPC Communication Flow
    # ----------------------------------------------------------
    doc.add_heading('3.4 Sequence Diagram — Electron IPC Communication Flow', level=2)
    add_para(doc, "The Sequence Diagram captures the precise temporal ordering of messages exchanged between the system components during the critical Print Preview operation — one of the most complex IPC transactions in the application. This operation requires the React UI to trigger a native Windows printing operation that involves creating an invisible Electron BrowserWindow, loading HTML content with embedded charts, waiting for SVG diagrams to fully render, capturing a pixel-perfect PDF buffer, and saving it to the user's chosen file system path.")
    add_para(doc, "The sequence begins when the clinic administrator clicks the Print Preview button in the Reports module. The React component (Print Hook) calls window.electron.previewPrint(), which is the IPC bridge function exposed by preload.js through contextBridge.exposeInMainWorld. This invocation is internally translated to ipcRenderer.invoke('preview-print', htmlPayload), which sends the serialized HTML content as a message payload to the Electron Main Process via the named IPC channel.")
    add_para(doc, "In the Main Process, the ipcMain.handle('preview-print') listener receives the message, deserializes the HTML payload, and creates a new hidden BrowserWindow instance with show: false. The HTML content (which contains embedded Mermaid.js charts, Recharts SVG visualizations, and styled patient data tables) is loaded into this invisible window. The system waits 2,500 milliseconds for all asynchronous JavaScript rendering to complete before calling win.webContents.printToPDF(). This generates a binary PDF buffer that is written to a temporary file in the OS temporary directory and then opened with the system's default PDF viewer using Electron's shell.openPath API.")

    insert_diagram(doc, 'diagram_2.png',
                   'Figure 3.4: Electron IPC Communication Sequence Diagram — Headless Print Preview Flow (A4 Landscape, 300 DPI)')

    add_para(doc, "Figure 3.4 shows the autonumbered sequence diagram with six participant lifelines: the end User, the React View (Print Hook), the Preload contextBridge, the electron/main.js handler, the Headless Chromium Print engine, and the Windows OS shell. The numbered arrows show the precise ordering of messages: the user click triggers a chain of IPC invocations that traverse the security boundary, execute the privileged operation in the Main Process, and return the result back to the user through the operating system's native shell interface. This flow demonstrates how Electron's architecture enables desktop-grade native capabilities while preserving React's declarative UI model.")

    # ----------------------------------------------------------
    # 3.5 Electron App Lifecycle Flow
    # ----------------------------------------------------------
    doc.add_heading('3.5 Electron Application Lifecycle and Context Isolation', level=2)
    add_para(doc, "The Electron Application Lifecycle encompasses the full initialization sequence that must complete before the clinic staff can interact with the clinical dashboard. This sequence is critical to understand because it establishes the security boundary, the database connection pool, and the data hydration pipeline in a precise order. Any failure at any stage of this lifecycle results in the application displaying an error recovery UI rather than the clinical dashboard, ensuring that staff never interact with a partially initialized system that could produce inconsistent data.")
    add_para(doc, "The lifecycle begins when the Electron executable is launched by the operating system. The electron/main.js script is the entry point that runs in the Node.js environment. It immediately registers all IPC message handlers using ipcMain.handle, sets up the global error logger, and creates the primary BrowserWindow with a configuration object that enforces the security constraints: contextIsolation: true ensures the preload script runs in a separate V8 context, nodeIntegration: false prevents the web page from importing Node.js modules directly, and webSecurity: true enables the Chromium same-origin policy.")
    add_para(doc, "After the BrowserWindow is created, Electron injects the preload.js script before any web content is loaded. This script executes in the privileged intermediate context and uses contextBridge.exposeInMainWorld to attach the whitelisted API (window.electron) to the browser's global scope. Only after this API is attached does Electron load the index.html bundle, which triggers the React application to mount. React's root render function initializes the App.jsx component tree, which runs a series of useEffect hooks to: detect the Electron environment, activate the localStorage proxy, open the IndexedDB connection pool, and hydrate the component state with all existing clinical data.")

    insert_diagram(doc, 'diagram_13.png',
                   'Figure 3.5(a): Electron App Lifecycle — Main Process Boot Sequence (Part 1 of 2, A4 Portrait, 300 DPI)')
    insert_diagram(doc, 'diagram_14.png',
                   'Figure 3.5(b): Electron App Lifecycle — IDB Connection Verification and Dashboard Mount (Part 2 of 2, A4 Portrait, 300 DPI)')

    add_para(doc, "Figures 3.5(a) and 3.5(b) present the application lifecycle as a two-part flowchart split at the React mount boundary. Part 1 covers the Main Process initialization: the executable launch, BrowserWindow creation with security constraints, preload script injection, and loading of the index.html React bundle. Part 2 covers the Renderer Process initialization: the App.jsx mount, sheetDB.js connection pool testing with automatic recovery, storage quota verification, and the final Dashboard render. The connection auto-recovery node in Part 2 represents the error handling code that attempts to re-open a corrupted IndexedDB connection before falling back to an emergency JSON file read via the IPC bridge.")

    # ----------------------------------------------------------
    # 3.6 IndexedDB Data Flow and Migration
    # ----------------------------------------------------------
    doc.add_heading('3.6 IndexedDB Data Flow and Schema Migration', level=2)
    add_para(doc, "The IndexedDB data layer is the core persistence mechanism for all clinical records in JS Pulse OHMS. Unlike traditional relational databases, IndexedDB is a transactional, key-value object store system that is native to Chromium-based browsers. The sheetDB.js module abstracts this API and provides a promise-based interface that supports connection pooling, version-based schema migration, bulk transaction batching, and storage quota monitoring. The migration system is particularly important for maintaining continuity when the application is updated to a new version that introduces additional fields or restructured object stores.")
    add_para(doc, "The storage quota defense mechanism activates automatically when the cumulative size of all stored data approaches 4.5MB. At this threshold, the system calculates the byte-size of every key in the localStorage proxy cache using the UTF-16 encoding formula (two bytes per character). Keys that represent historical records older than 30 days are aggregated into a backup batch and written to IndexedDB object stores through the sheetDB bulk-write API. After confirming a successful IndexedDB write through the transaction completion event, the system purges the corresponding keys from the in-memory proxy cache, freeing capacity for new incoming clinical records. In the event of an IndexedDB write failure, the system falls back to an emergency JSON dump operation that writes the data to the Windows file system through the Electron IPC bridge.")
    add_para(doc, "The schema migration flow (depicted in Figures 3.6a and 3.6b) is triggered by the onupgradeneeded callback of indexedDB.open when the DB_VERSION constant in sheetDB.js is incremented in a new application release. The migration handler creates new object stores, adds required indexes, and transforms existing records to conform to the new schema structure. All migration operations execute within a single IndexedDB upgrade transaction, ensuring atomicity: if any part of the migration fails, the entire upgrade transaction is rolled back and the database remains in its previous consistent state.")

    insert_diagram(doc, 'diagram_15.png',
                   'Figure 3.6(a): IndexedDB Migration Hook and Quota Trigger (Part 1 of 2, A4 Portrait, 300 DPI)')
    insert_diagram(doc, 'diagram_16.png',
                   'Figure 3.6(b): IndexedDB Batch Write Execution and Legacy Purge (Part 2 of 2, A4 Portrait, 300 DPI)')

    add_para(doc, "Figure 3.6(a) shows the initial migration hook evaluation: it reads all localStorage keys, calculates the total byte size, and determines whether the 4.5MB threshold has been crossed. If not, the system reports healthy status. If yes, it begins aggregating keys for batch migration to IndexedDB. Figure 3.6(b) shows the execution phase: opening the sheetDB connection, pushing aggregated records to the appropriate object stores, validating write success, and purging the migrated keys from localStorage. The emergency JSON dump path in Figure 3.6(b) serves as a final failsafe that prevents data loss even in scenarios of complete IndexedDB failure.")

    # ----------------------------------------------------------
    # 3.7 Data Flow Diagram (DFD Level 1)
    # ----------------------------------------------------------
    doc.add_heading('3.7 Data Flow Diagram (DFD) — Level 1', level=2)
    add_para(doc, "The Level 1 Data Flow Diagram (DFD) provides a functional decomposition of the JS Pulse OHMS system, showing how data flows between the four primary external actors (Patient, Doctor, Pharmacist, Administrator) and the five internal processing subsystems, with arrows indicating the direction and nature of each data flow. Unlike the sequence diagram which focuses on temporal ordering, the DFD focuses on the transformation of data as it moves through the system, making it particularly useful for understanding the complete data lifecycle from initial clinical capture through final reporting.")
    add_para(doc, "The five processing subsystems identified in the DFD are: 1.0 Registration, which accepts patient identity and vital data from the Nurse actor and writes structured records to the cms_daily_opd_sheet store; 2.0 Consultation, which accepts prescription inputs from the Doctor actor and appends diagnosis and medicine details to the patient records; 3.0 Sync Engine, which continuously reads the OPD store for unextracted records and writes extracted prescription data to the cms_dispense_log store; 4.0 Pharmacy Dispensing, which reads from the dispense log and updates stock levels in cms_medstock_data; and 5.0 Report Generator, which reads from all data stores to produce structured Excel and PDF output files for the Administrator.")
    add_para(doc, "The three data stores (cms_daily_opd_sheet, cms_dispense_log, and cms_medstock_data) act as the integration points between the processing subsystems, enabling asynchronous data sharing without direct inter-component communication. This decoupled architecture means that the OPD component and the Pharmacy component never directly call each other's functions; they communicate exclusively through the shared IndexedDB stores with the sync engine acting as the automated middleware. This design is essential for the offline-first requirement: since there is no network server to coordinate real-time updates, the shared database becomes the single source of truth for all clinical operations.")

    insert_diagram(doc, 'diagram_25.png',
                   'Figure 3.7: JS Pulse OHMS Level 1 Data Flow Diagram (DFD) (A4 Landscape, 300 DPI)')

    add_para(doc, "Figure 3.7 illustrates the complete Level 1 DFD with external actors on the left and right sides connected to the five numbered processing bubbles in the center. The three rectangular data stores (cms_daily_opd_sheet, cms_dispense_log, cms_medstock_data) sit between the processing bubbles, showing both inbound write arrows and outbound read arrows. The automated sync engine (bubble 3.0) occupies a pivotal position between the OPD and Pharmacy subsystems, representing the background 10-second polling mechanism that drives the prescription flow through the system without requiring manual intervention from clinical staff.")

    # ----------------------------------------------------------
    # 3.8 Patient Record State Machine
    # ----------------------------------------------------------
    doc.add_heading('3.8 Patient Record State Machine Diagram', level=2)
    add_para(doc, "The Patient Record State Machine models the complete lifecycle of a single clinical encounter within the JS Pulse OHMS system as a finite-state automaton. Each state represents a distinct operational condition of the patient record, and each transition arrow represents a specific action taken by a clinical staff member or an automated system process. Understanding the state machine is essential for validating the application's business logic: every user interaction in the system corresponds to a state transition, and the system enforces the valid transition rules through component-level conditional rendering and data validation logic.")
    add_para(doc, "The lifecycle begins at the initial state (represented by a filled circle) and immediately transitions to PendingVitals when a patient arrives at the reception counter. The nurse's entry of the patient's vital signs (blood pressure, body temperature, pulse rate, SpO2) triggers the transition to InConsultation. At this point, the doctor's OPD dashboard displays the patient in the active consultation queue. The doctor's examination and diagnosis entry transitions the record into the PrescriptionDrafting composite state, which contains its own nested sub-states representing the drug interaction check loop (CheckInteractions -> AddDrug -> CheckInteractions) that continues until all prescribed medicines pass the safety validation matrix.")
    add_para(doc, "Once the doctor finalizes and submits the prescription, the record transitions to PharmacyQueue with the extracted field set to false. The automated sync engine detects this state change during its next polling cycle and transitions the record to DispensingPending by creating the corresponding entry in cms_dispense_log. The pharmacist's dispensing confirmation action triggers the final transition to Completed, which simultaneously marks the dispense log entry as 'Deducted' and triggers the stock deduction algorithm in DailyConsume.jsx. The record then transitions to its terminal state, leaving a permanent, immutable audit trail in the database.")

    insert_diagram(doc, 'diagram_17.png',
                   'Figure 3.8(a): Patient Record State Machine — Reception to Prescription Drafting (Part 1 of 2, A4 Portrait, 300 DPI)')
    insert_diagram(doc, 'diagram_18.png',
                   'Figure 3.8(b): Patient Record State Machine — Pharmacy Queue to Completion (Part 2 of 2, A4 Portrait, 300 DPI)')

    add_para(doc, "Figures 3.8(a) and 3.8(b) together present the complete state machine in two segments. Part 1 shows the initial reception states (PendingVitals, InConsultation) and the composite PrescriptionDrafting state with its nested drug interaction check sub-states. Part 2 shows the pharmacy-side states (PharmacyQueue, DispensingPending, Completed) and the terminal state transition that occurs when the stock deduction algorithm confirms successful inventory adjustment. The split is made at the prescription submission boundary, which is also the boundary between the clinical and pharmacy operational domains within the application.")

    # ----------------------------------------------------------
    # 3.9 Entity-Relationship (ER) Diagram
    # ----------------------------------------------------------
    doc.add_heading('3.9 Entity-Relationship (ER) Diagram', level=2)
    add_para(doc, "Although JS Pulse OHMS uses IndexedDB (a non-relational object store) rather than a traditional SQL database, the logical data relationships between its object stores can be formally modeled using an Entity-Relationship (ER) diagram. This model is important for understanding how clinical data integrity is maintained across the three primary object stores and for planning future database migrations or integration with external systems such as the Jindal Steel corporate ERP platform.")
    add_para(doc, "The three primary entities are: PATIENT_VISITS (corresponding to the cms_daily_opd_sheet object store), DISPENSE_LOG (corresponding to the cms_dispense_log object store), and MED_STOCK (corresponding to the cms_medstock_data object store). The PATIENT_VISITS entity has a composite primary key consisting of the employee code (empCode) and the visit date, as an employee may have multiple visits on different days but only one per day. Its key fields include patientName, drName, medicinesDetails (a JSON-serialized array of prescribed medicines), and the critical extracted boolean flag that drives the OPD-to-pharmacy sync pipeline.")
    add_para(doc, "The two logical relationships are: a one-to-many (1:N) relationship between PATIENT_VISITS and DISPENSE_LOG, where a single OPD visit can generate multiple dispense log entries (one per prescribed medicine line); and a many-to-one (N:1) relationship between DISPENSE_LOG and MED_STOCK, where multiple dispense entries across different patients may reference the same medicine in the master stock inventory. These relationships are enforced at the application layer through the sync engine and deduction algorithm, since IndexedDB does not natively support foreign keys or referential integrity constraints.")

    insert_split_diagram(doc, 'diagram_26.png', [
        'Figure 3.9(a): ER Diagram — PATIENT_VISITS and DISPENSE_LOG Entities (Part 1 of 2, A4 Portrait, 300 DPI)',
        'Figure 3.9(b): ER Diagram — DISPENSE_LOG and MED_STOCK Entities with Relationships (Part 2 of 2, A4 Portrait, 300 DPI)'
    ])

    add_para(doc, "Figures 3.9(a) and 3.9(b) present the ER diagram in two segments. Part 1 shows the PATIENT_VISITS entity with all its attributes, with the primary key (empCode) underlined, and the one-to-many relationship line connecting it to DISPENSE_LOG. Part 2 shows the DISPENSE_LOG entity's attributes (with the medicineName acting as a foreign key reference) and the many-to-one relationship line connecting it to the MED_STOCK entity. The crow's foot notation on the relationship lines clearly indicates the cardinality: a single patient visit generates zero or many dispense entries, and many dispense entries may reference a single medicine stock record.")

    # Save
    out_path = 'JSPulse_OHMS_Chapter3_Final.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
