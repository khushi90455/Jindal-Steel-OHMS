import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def setup_styles(doc):
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    for i in range(1, 4):
        h_style = doc.styles[f'Heading {i}']
        h_font = h_style.font
        h_font.name = 'Times New Roman'
        h_font.color.rgb = RGBColor(0, 0, 0)
        
def add_paragraph(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.add_run(text)
    return p

def main():
    doc = Document()
    setup_styles(doc)
    
    doc.add_heading('Chapter 2: System Architecture and Technologies', level=1)
    
    # 2.1 Existing System vs Proposed System
    doc.add_heading('2.1 Existing System vs Proposed System', level=2)
    add_paragraph(doc, "The evolution from the legacy manual system to the JS Pulse OHMS platform marks a significant paradigm shift in how Jindal Steel & Power manages occupational health data at the Patratu plant. The existing system was entirely paper-based and characterized by profound operational bottlenecks that stifled efficiency and compromised medical response times. Daily Outpatient Department (OPD) logs, dispensing registers, and extensive medical stock books were all maintained on physical paper. This archaic approach necessitated manual writing by doctors, nurses, and pharmacists, leading to frequent transcription errors, illegible handwriting issues, and massive data redundancy. For example, a prescription written by a doctor in the OPD log had to be manually re-entered into the pharmacy dispensing log before a patient could receive medication.")
    add_paragraph(doc, "Furthermore, manual calculations were required to balance stock levels at the end of each shift. Pharmacists had to individually count tablets, syrups, and injectables, cross-referencing them against the daily dispensing logs. This manual arithmetic frequently led to discrepancies between physical inventory and the paper ledger records, creating inventory shrinkage and stockouts of critical emergency medicines. Auditing capability was practically nonexistent under this framework. Tracking the longitudinal medical history of a specific employee over a decade, compiling the monthly medical compliance reports required by the Factories Act, or cross-referencing audiometry and spirometry results for occupational hazard profiling required physical sorting of thousands of fragile pages—a process taking days to complete and prone to human error.")
    add_paragraph(doc, "In stark contrast, the proposed JS Pulse OHMS is a modern, offline-first medical management application wrapped in an Electron desktop container, tailored specifically to resolve these localized industrial issues. The new system features automated, real-time data pipelines where prescriptions logged in the digital OPD sheet automatically and instantaneously appear in the pharmacist's secure dispensing queue, entirely eliminating redundant data entry and transcription errors. Live inventory tracking ensures that dispensing a medication automatically deducts the precise quantity from the central digital stock ledger in real-time, executing complex state updates without manual intervention.")
    add_paragraph(doc, "The proposed system also introduces proactive visual compliance alerts that were impossible in the paper regime. The React-based dashboard continuously monitors the drug database and highlights low-stock and near-expiry medical items using a dynamic, color-coded warning system, drastically reducing pharmaceutical wastage and ensuring critical supplies are always available for trauma care. Additionally, the application introduces a high-performance custom data grid capable of handling thousands of health records smoothly through advanced DOM virtualization techniques, and integrates an offline NLP (Natural Language Processing) chatbot capable of instantly answering clinical and administrative queries based purely on the localized IndexedDB database, requiring zero cloud connectivity.")
    
    # 2.2 Technology Stack Breakdown
    doc.add_heading('2.2 Technology Stack Breakdown', level=2)
    add_paragraph(doc, "The technology stack chosen for JS Pulse OHMS was meticulously selected to balance rapid user interface development, native operating system integration, high computational performance, and absolute offline resilience. At the core of the application lies React 19, an industry-leading component-based JavaScript library for building dynamic user interfaces. React 19 was explicitly selected for its advanced concurrent rendering capabilities, optimized diffing algorithm, and declarative paradigm. These features allow for the rapid construction of complex clinical dashboards, interactive medical grids, and real-time state management without sacrificing frame rates or UI responsiveness. The UI components were designed utilizing a custom Vanilla CSS3 Grid System, completely avoiding heavy third-party CSS frameworks to maintain a low memory footprint. This bespoke styling system features dynamic CSS variables that enable seamless switching between Dark and Light modes, ensuring visual comfort for clinic staff working exhaustive 24-hour shift rotations under varying lighting conditions.")
    add_paragraph(doc, "To compile, optimize, and bundle the React application, Vite v8 was employed as the primary build tool. Vite provides an exceptionally fast, native ESM-based development server with instantaneous hot-module replacement (HMR). This drastically reduced build times compared to legacy bundlers like Webpack, allowing for rapid iteration and testing during the software development lifecycle. For complex data visualization, the Recharts library was integrated. Recharts leverages scalable, declarative SVG-based analytical graphs to visualize localized patient admission trends, occupational hazard statistics, and inventory consumption rates securely, directly within the client environment.")
    add_paragraph(doc, "Because the industrial network at the Patratu plant is geographically isolated and subject to severe electromagnetic interference and network fluctuations, a standard cloud-hosted web application was deemed fundamentally unsuitable. Instead, the React application is tightly wrapped inside Electron v42, a powerful framework that embeds the Chromium rendering engine and Node.js runtime. This allows the web application to function as a standalone, native Windows desktop executable. Electron provides direct access to the local file system and operating system APIs via Inter-Process Communication (IPC). This native system access is actively leveraged for automated PDF and Excel document generation using libraries like jspdf, jspdf-autotable, and SheetJS (xlsx), enabling the clinic to instantly print statutory health reports directly to local plant printers without requiring any internet access.")
    add_paragraph(doc, "For data persistence, traditional client-server relational databases (like PostgreSQL or MySQL) were eschewed to eliminate the need for an on-premise database server and network routing. Instead, IndexedDB, a low-level API for client-side storage of significant amounts of structured data, serves as the primary data engine. Because standard HTML5 localStorage is strictly limited to 5MB and is synchronous (blocking the main thread), it is wholly insufficient for a medical application. To interface with IndexedDB efficiently, a highly optimized custom database driver, named `sheetDB.js`, was engineered. This driver handles connection pooling, asynchronous transaction management, and complex cursor-based queries, providing a robust, offline-first database engine that stores gigabytes of patient records safely on the local hard drive, completely insulated from industrial network outages.")
    
    # 2.3 Hardware & Software Requirements
    doc.add_heading('2.3 Hardware & Software Requirements', level=2)
    add_paragraph(doc, "JS Pulse OHMS is architected to be highly resource-efficient, capable of executing flawlessly on standard, budget-conscious administrative desktop terminals already provided within the Jindal Steel & Power clinic. By optimizing the virtualization of DOM elements and managing memory garbage collection actively within the React lifecycle, the application avoids the heavy processing overhead typically associated with Electron applications. The hardware requirements are deliberately optimized to ensure maximum backward compatibility with the existing legacy IT infrastructure at the Patratu plant.")
    add_paragraph(doc, "The absolute minimum processing requirement is an Intel Core i3 (7th Generation) or an equivalent AMD Ryzen 3 processor. However, for optimally handling extremely large datasets—such as simultaneously loading the entire yearly employee medical history in the virtualization grid for auditing purposes—an Intel Core i5 processor (or AMD Ryzen 5) or higher is strongly recommended. The application requires a baseline minimum of 4 GB of System RAM. Nevertheless, 8 GB of RAM is strongly recommended by the deployment guidelines to provide adequate memory overhead for Electron's multi-process Chromium rendering engine, especially when visualizing complex interactive Recharts graphs and processing massive PDF binary buffers entirely in memory before piping them to the local printer.")
    add_paragraph(doc, "In terms of persistent storage, the base application footprint (the compiled Electron binaries, ASAR archives, and bundled React assets) is relatively small, requiring only about 500 MB of free storage space. However, because the system relies entirely on an offline-first IndexedDB storage mechanism that archives sensitive medical data, X-ray metadata, and inventory logs locally over time, a Solid State Drive (SSD) with at least 50 GB of free, unallocated space is highly recommended. The use of an NVMe or SATA SSD rather than a mechanical Hard Disk Drive (HDD) is critical to ensure rapid IndexedDB read/write transaction speeds and reliable data persistence over years of continuous 24/7 operation. The display requirements mandate a minimum resolution of 1366x768 pixels, with 1920x1080 (Full HD) heavily recommended to fully utilize the expansive data grid interfaces, multi-pane layouts, and analytical dashboards without requiring excessive vertical or horizontal scrolling by the medical staff.")
    add_paragraph(doc, "On the software side, the application is pre-compiled as a standalone executable specifically targeted for Microsoft Windows (Windows 10 or Windows 11, 64-bit architecture), aligning with JSP's standard operating system policies. Because the Electron framework packages its own isolated Node.js runtime and Chromium V8 JavaScript engine internally, there is absolutely no requirement to install external database servers, web servers (such as Apache, Nginx, or IIS), or specific browser dependencies on the host machines. This zero-dependency architecture drastically simplifies the IT deployment process, allowing for instant 'plug-and-play' installation by simply running the executable on any clinic computer.")
    
    # 2.4 High-Level System Architecture Design
    doc.add_heading('2.4 High-Level System Architecture Design', level=2)
    add_paragraph(doc, "The high-level architecture of JS Pulse OHMS follows a strict, security-first separation of concerns, fundamentally decoupling the presentation and UI rendering layer from the secure data access and privileged operating system execution layers. Because the application processes highly sensitive, personally identifiable medical information (PII) and occupational health records, it adheres strictly to the Principle of Least Privilege by actively utilizing Electron's advanced context isolation and multi-process sandboxing features.")
    add_paragraph(doc, "The system architecture is inherently divided into two distinct primary processes: the Main Process (operating within a full Node.js environment) and the Renderer Process (operating within a restricted Chromium browser environment). The Renderer Process hosts the entire React 19 application. It is exclusively responsible for handling all user interactions, UI state management, complex DOM virtualization for the medical spreadsheets, and client-side data validation. Crucially, the Renderer Process is entirely sandboxed and has absolutely no direct access to the underlying Windows operating system, the file system, or Node.js built-in modules. This sandbox ensures that even if malicious code were somehow injected into the UI (e.g., via Cross-Site Scripting), it could not escape the browser context to compromise the host industrial machine.")
    add_paragraph(doc, "When the React frontend needs to perform a privileged system operation—such as querying the localized IndexedDB via the `sheetDB.js` wrapper, saving a massively compiled exported Excel ledger to the documents folder, or commanding the local system printer to output an automated PDF compliance report—it cannot do so directly. Instead, it must serialize the request and send a message through a highly secure, asynchronous Inter-Process Communication (IPC) bridge. This bridge is explicitly established during the window initialization phase by a dedicated `preload.js` script. The preload script utilizes Electron's `contextBridge` API to expose a tightly controlled, strictly typed API surface to the global window object, ensuring the React frontend can only invoke explicitly whitelisted commands.")
    add_paragraph(doc, "The Main Process listens for these incoming IPC messages, executes the requested Node.js operations natively and securely, and then asynchronously returns the serialized results back across the bridge to the Renderer. This dual-process architectural design not only provides military-grade security for the clinic's medical data but also ensures that intensive computational tasks—such as heavy file I/O, database transaction commits, and PDF binary stream generation—do not block the Chromium UI thread. This architectural decision guarantees that the application maintains a fluid, uninterrupted 60 frames-per-second experience for the clinical staff, even under heavy computational load.")
    
    # Embed diagram
    img_path = 'diagram_images/diagram_0.png'
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(img_path, width=Inches(6.0))
        caption = doc.add_paragraph('Figure 2.1: High-Level Electron System Architecture & Secure IPC Context Bridge Flow')
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption.runs[0].italic = True
    else:
        add_paragraph(doc, "[System Architecture Diagram: diagram_images/diagram_0.png not found]")

    add_paragraph(doc, "As meticulously illustrated in Figure 2.1 above, the flow of operational data moves seamlessly both synchronously and asynchronously across the context bridge. This structured, localized approach allows JS Pulse OHMS to operate entirely independently of any external cloud servers or corporate intranets. By completely eliminating network latency and server dependency, the application embodies a true localized, high-performance architecture perfectly suited for the uncompromising, mission-critical demands of the Jindal Steel & Power industrial environment.")
    
    out_path = 'JSPulse_OHMS_Chapter2.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
