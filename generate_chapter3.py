import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT, WD_SECTION_START

IMG_DIR = 'diagram_images_hq'

# Actual image dimensions (width x height) in pixels
DIAGRAM_DIMS = {
    'diagram_2.png':  (2897, 1118),
    'diagram_13.png': (711, 1313),
    'diagram_14.png': (849, 1837),
    'diagram_15.png': (998, 1561),
    'diagram_16.png': (1044, 1534),
    'diagram_17.png': (793, 1496),
    'diagram_18.png': (612, 1095),
    'diagram_4.png':  (2225, 858),
    'diagram_12.png': (2955, 1641),
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

    doc.add_heading('Chapter 3: Advanced UML and Architecture Flows', level=1)

    # --- 3.1 Electron IPC Bridge Communication Flow ---
    doc.add_heading('3.1 Electron IPC Bridge Communication Flow', level=2)
    add_paragraph(doc, "The Electron Inter-Process Communication (IPC) bridge is the fundamental security backbone of the JS Pulse OHMS application. In any Electron application, there exist two fundamentally distinct process domains: the Main Process and the Renderer Process. The Main Process runs within a full Node.js environment and has unrestricted access to operating system APIs, the native file system, system dialogs, and hardware peripherals such as printers. The Renderer Process, on the other hand, runs inside a sandboxed Chromium browser context and hosts the React 19 user interface. For security reasons, the Renderer is explicitly prohibited from directly accessing Node.js modules or the file system.")
    add_paragraph(doc, "The IPC bridge is the exclusive mechanism by which these two isolated worlds communicate. In the JS Pulse OHMS codebase, this bridge is established through a dedicated preload.js script that executes in a privileged intermediate context. The preload script uses Electron's contextBridge.exposeInMainWorld API to inject a tightly controlled set of callable functions into the browser's global window object. These functions act as secure, one-way message tunnels: the React application can invoke them to send serialized requests to the Main Process, but it can never directly access Node.js primitives or bypass the bridge to execute arbitrary system-level code.")
    add_paragraph(doc, "When the React frontend triggers a privileged operation, such as saving a patient record to the local file system, exporting an Excel report, or printing a PDF compliance document, the request is serialized into a structured JSON payload containing the operation type, the target data, and any metadata required for execution. This payload is transmitted through the IPC channel using Electron's ipcRenderer.invoke method, which returns a Promise. The Main Process listens for these incoming messages via ipcMain.handle, deserializes the payload, validates its structure, executes the requested Node.js operation, and then returns the result asynchronously back through the bridge to the waiting React component.")
    add_paragraph(doc, "This architectural pattern ensures several critical properties for the clinical application. First, it provides defense-in-depth security: the React UI cannot be exploited to gain file system access. Second, it guarantees non-blocking UI performance: since heavy file I/O and PDF generation occur in the Main Process (a separate V8 isolate), the Chromium Renderer thread remains free to process user interactions at 60 frames per second. Third, it enables clean separation of concerns in the codebase: all system-level logic is isolated in the Electron main process handlers, while the React components remain purely declarative and focused on presentation logic.")

    insert_diagram(doc, 'diagram_2.png',
                   'Figure 3.1: Electron IPC Bridge Secure Communication Sequence Diagram (A4 Landscape, 300 DPI Original Size)')

    add_paragraph(doc, "As depicted in Figure 3.1, the complete lifecycle of an IPC transaction begins when the user triggers an action in the React UI. The React component calls window.electron.someFunction(), which was injected by preload.js. This function internally calls ipcRenderer.invoke with a channel name and payload. The Electron Main Process receives the invocation, performs the requested Node.js operation (such as writing a file or querying IndexedDB), and resolves the Promise with the result. The React component then receives the response and updates its state accordingly. This entire round-trip is asynchronous, ensuring that the user interface remains completely responsive throughout the operation.")

    # --- 3.2 Secure Context Isolation Mechanism ---
    doc.add_heading('3.2 Secure Context Isolation Mechanism', level=2)
    add_paragraph(doc, "Context isolation is a critical Electron security feature that creates a completely separate JavaScript execution environment for the preload script, distinct from both the Main Process and the Renderer Process. When context isolation is enabled (which it is by default in modern Electron versions and explicitly enforced in JS Pulse OHMS), the preload script runs in its own isolated V8 context. This means that even though the preload script can access Node.js modules and Electron APIs, the web page loaded in the Renderer cannot access these same objects through prototype chain pollution, property overriding, or any other JavaScript-level attack vector.")
    add_paragraph(doc, "In the JS Pulse OHMS implementation, the preload.js script carefully constructs a minimal API surface using contextBridge.exposeInMainWorld. This API surface is deliberately constrained to expose only the exact set of functions that the React application legitimately needs. For example, the exposed API includes functions for saving and loading localStorage data, triggering PDF generation, opening native file save dialogs, and invoking Excel export operations. Critically, it does not expose raw fs module access, child_process spawning, or any method that could be used to execute arbitrary system commands.")
    add_paragraph(doc, "The security implications of this design are profound in a medical context. Patient health records, prescription histories, and pharmaceutical inventory data constitute highly sensitive personally identifiable information (PII). If context isolation were disabled or improperly configured, a cross-site scripting (XSS) vulnerability in any React component could potentially allow an attacker to read the entire local file system, exfiltrate patient data, or install malicious software on the clinic's computer. By strictly enforcing context isolation and exposing only whitelisted IPC channels, JS Pulse OHMS ensures that even a compromised UI cannot breach the security boundary between the browser sandbox and the operating system.")
    add_paragraph(doc, "The implementation also leverages nodeIntegration: false in the BrowserWindow configuration, which prevents the Renderer Process from directly requiring Node.js modules. Combined with context isolation, this creates a dual-layered security model. The first layer (nodeIntegration: false) prevents direct Node.js access from the web page. The second layer (contextIsolation: true) prevents indirect access through prototype pollution of the preload script's globals. This defense-in-depth approach aligns with industry best practices for securing desktop applications that handle sensitive healthcare data.")

    insert_diagram(doc, 'diagram_13.png',
                   'Figure 3.2(a): Electron App Lifecycle and Boot Sequence Flow (Part 1 - A4 Portrait, 300 DPI Original Size)')
    insert_diagram(doc, 'diagram_14.png',
                   'Figure 3.2(b): Electron App Lifecycle and Connection Verification Flow (Part 2 - A4 Portrait, 300 DPI Original Size)')

    add_paragraph(doc, "Figures 3.2(a) and 3.2(b) provide a comprehensive visualization of the entire Electron application lifecycle and security layer. Figure 3.2(a) shows the initial launch of main.js, browser window creation, and loading of the React build assets. Figure 3.2(b) tracks the connection verification loop managed by sheetDB.js and the final UI hydration. The diagram clearly illustrates how the context bridge acts as a secure boundary layer between the privileged Node.js environment and the sandboxed Chromium renderer, ensuring that all inter-process communication flows through explicitly defined, auditable channels.")

    # --- 3.3 Database Transaction & Schema Flowchart ---
    doc.add_heading('3.3 Database Transaction and Schema Flowchart', level=2)
    add_paragraph(doc, "The database layer of JS Pulse OHMS is one of the most architecturally distinctive components of the application. Unlike conventional web applications that rely on a remote SQL or NoSQL database server, JS Pulse OHMS implements a fully localized, offline-first storage engine built on top of the browser's native IndexedDB API. This design decision was driven by the operational reality of the Patratu plant: the industrial network infrastructure is unreliable, and the clinic cannot afford any downtime due to database connectivity failures.")
    add_paragraph(doc, "The custom database wrapper, internally named sheetDB.js, acts as an abstraction layer over the raw IndexedDB API. It provides a high-level interface for creating, reading, updating, and deleting records across multiple object stores (which function analogously to tables in a relational database). Each object store corresponds to a specific clinical data domain: cms_patient_visit_log stores outpatient department records, cms_medstock_data stores pharmaceutical inventory, cms_dispense_log tracks medication dispensing events, and cms_periodic_exam stores periodic occupational health examination results.")
    add_paragraph(doc, "The sheetDB driver implements connection pooling to prevent the performance degradation that occurs when multiple React components simultaneously attempt to open IndexedDB connections. When the application initializes, sheetDB opens a single persistent connection to the database and maintains it throughout the application's lifecycle. All subsequent read and write operations are multiplexed through this single connection using IndexedDB's built-in transaction mechanism. Transactions are automatically scoped to the minimum required object stores, ensuring optimal concurrency and preventing deadlocks.")
    add_paragraph(doc, "Data integrity is maintained through a combination of structural validation at the application layer and IndexedDB's native ACID transaction guarantees. Before any record is written to the database, the React component validates the data against a schema definition that specifies required fields, data types, and acceptable value ranges. For example, a patient record must include a non-empty patient name, a valid employee ID, a consultation date, and at least one diagnosis entry. If validation fails, the write operation is rejected before it reaches the database layer, preventing corrupt or incomplete records from entering the system.")

    insert_diagram(doc, 'diagram_15.png',
                   'Figure 3.3(a): IndexedDB Migration Hook and Schema Versioning Check (Part 1 - A4 Portrait, 300 DPI Original Size)')
    insert_diagram(doc, 'diagram_16.png',
                   'Figure 3.3(b): IndexedDB Migration Execution and Legacy Clean-up (Part 2 - A4 Portrait, 300 DPI Original Size)')

    add_paragraph(doc, "Figures 3.3(a) and 3.3(b) illustrate the database migration flow that executes when the application detects a schema version change. In Part 1, the hook scans the browser's current storage space and evaluates if key formats match legacy versions. In Part 2, the aggregation loop writes these legacy data items into IndexedDB and purges the old local storage fields. This process ensures backward compatibility when the application is updated to a new version that introduces additional data fields or restructured object stores.")

    insert_diagram(doc, 'diagram_17.png',
                   'Figure 3.4(a): Clinical Intake and Vitals Transition States (Part 1 - A4 Portrait, 300 DPI Original Size)')
    insert_diagram(doc, 'diagram_18.png',
                   'Figure 3.4(b): Doctor Consultation and Pharmacy Dispensing Transition States (Part 2 - A4 Portrait, 300 DPI Original Size)')

    add_paragraph(doc, "As shown in Figures 3.4(a) and 3.4(b), the patient record progresses through a series of well-defined states within the clinical workflow. Part 1 covers the reception counter where vitals are recorded and marked as PendingVitals. Part 2 tracks the transition into consultation, prescription drafting, the pharmacy queue, and finally daily consume deduction. Each state transition is logged with a timestamp, creating a complete audit trail for regulatory compliance.")

    # --- 3.4 Application Lifecycle and State Management Diagram ---
    doc.add_heading('3.4 Application Lifecycle and State Management Diagram', level=2)
    add_paragraph(doc, "The application lifecycle of JS Pulse OHMS encompasses the entire chain of events from the moment the user double-clicks the desktop executable to the point where the clinic staff is interacting with a fully loaded, data-populated clinical dashboard. Understanding this lifecycle is critical because it reveals the precise sequence in which security contexts are established, database connections are initialized, cached data is hydrated, and the React component tree is mounted.")
    add_paragraph(doc, "When the application executable is launched, the Electron Main Process initializes first. The main.js script registers all IPC message handlers, sets up global error logging, and creates the primary BrowserWindow instance with the security configuration (contextIsolation: true, nodeIntegration: false). The preload.js script is then injected into the BrowserWindow's web preferences. Only after these security layers are established does Electron load the React application's index.html entry point into the Renderer Process.")
    add_paragraph(doc, "Once the React application mounts, it immediately invokes a series of initialization hooks. The first hook checks whether the application is running inside an Electron environment or a standard browser (for development purposes). If Electron IPC is detected, the application activates the localStorage proxy engine, which intercepts all localStorage.setItem and localStorage.getItem calls and routes them through the IPC bridge to the native file system. This proxy is transparent to the rest of the application: all React components continue to use the standard localStorage API without any modification, but behind the scenes, the data is being persisted to the file system rather than the browser's 5MB-limited storage.")
    add_paragraph(doc, "The second initialization hook hydrates the application's state by loading all cached clinical data from the local storage backend. This includes the full patient visit log, the pharmaceutical inventory, the dispensing history, the periodic examination records, and the first aid kit tracking data. Each dataset is loaded asynchronously and injected into the appropriate React state variables, ensuring that the user sees a fully populated dashboard within seconds of launching the application, even if the dataset contains tens of thousands of records.")

    insert_diagram(doc, 'diagram_4.png',
                   'Figure 3.5: Custom localStorage Proxy and File System Persistence Flow (A4 Landscape, 300 DPI Original Size)')

    add_paragraph(doc, "Figure 3.5 demonstrates the localStorage proxy mechanism in action. When the React application calls localStorage.setItem(key, data), the proxy intercepts this call, updates an in-memory Map object synchronously (ensuring instant read-back performance), and then asynchronously invokes the Electron IPC bridge to persist the data to a JSON file on the native file system. This dual-write strategy combines the speed of in-memory caching with the durability of file system persistence, ensuring zero data loss even during unexpected application crashes or power failures at the plant.")

    insert_diagram(doc, 'diagram_12.png',
                   'Figure 3.6: Complete JSPulse OHMS Macro System Architecture Overview (A4 Landscape, 300 DPI Original Size)')

    add_paragraph(doc, "Figure 3.6 presents the complete macro-level system architecture of JS Pulse OHMS, showing all major subsystems and their interconnections within the Electron native wrapper. The diagram illustrates how the React frontend components, the IPC bridge layer, the Node.js backend handlers, the IndexedDB storage engine, and the native OS integration services (file system, printers, system dialogs) work together as a cohesive, fully offline clinical management platform. This holistic view demonstrates the application's ability to operate entirely independently of cloud infrastructure, making it ideally suited for deployment in the geographically isolated and network-constrained environment of the Jindal Steel and Power Patratu facility.")

    # Save
    out_path = 'JSPulse_OHMS_Chapter3.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
