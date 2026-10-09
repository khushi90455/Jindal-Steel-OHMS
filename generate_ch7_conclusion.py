import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

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
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing  = 1.5
    p.paragraph_format.space_before  = Pt(0)
    p.paragraph_format.space_after   = Pt(4)
    p.paragraph_format.left_indent   = Inches(0.25 + level * 0.25)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def code_block(doc, lines_text, caption_text=None):
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

def reference(doc, number, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.left_indent  = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    
    run_num = p.add_run(f'[{number}] ')
    run_num.bold = True
    run_num.font.name = 'Times New Roman'
    run_num.font.size = Pt(12)
    
    run_text = p.add_run(text)
    run_text.font.name = 'Times New Roman'
    run_text.font.size = Pt(12)

def main():
    doc = Document()
    setup_doc(doc)

    # ═══════════════════════════════════════════════════════════
    # CHAPTER 7 TITLE
    # ═══════════════════════════════════════════════════════════
    doc.add_heading('Chapter 7: Installation, Deployment, References & Conclusion', level=1)

    # ───────────────────────────────────────────────────────────
    # 7.1 Installation & Environment Setup
    # ───────────────────────────────────────────────────────────
    doc.add_heading('7.1 Installation & Environment Setup', level=2)
    
    para(doc, "The JS Pulse OHMS deployment at the Jindal Steel plant in Patratu requires a precise, documented environment setup to ensure stability and compatibility across target clinic workstations. Because the system is designed to run in a fully offline desktop environment, all runtime frameworks and dependencies are compiled and bundled directly into the installation package. The following sections outline the hardware, software, runtime installation steps, directory configurations, and core build structures.")
    
    doc.add_heading('7.1.1 Hardware and Software Prerequisites', level=3)
    para(doc, "Before beginning installation, the target system must satisfy the following hardware and software parameters:")
    bullet(doc, "Hardware: A workstation with an Intel i3 (or AMD equivalent) 8th generation processor or newer, a minimum of 4 GB DDR4 RAM (8 GB recommended), and at least 500 MB of available storage for the application bin files and database object stores.")
    bullet(doc, "Operating System: Microsoft Windows 10 (version 1909 or later) or Windows 11 (64-bit architecture is required).")
    bullet(doc, "Prerequisites: Microsoft Visual C++ Redistributable 2022 is required for Electron's native filesystem bindings to compile and execute properly.")

    doc.add_heading('7.1.2 Development Environment Configuration', level=3)
    para(doc, "For maintenance engineers setting up a new development environment or compiling the code from source, the installation sequence is structured as follows:")
    
    bullet(doc, "Node.js Installation: Download and install Node.js v20.12.2 LTS. This version is selected to align with Electron v29.1's internal V8 engine version, ensuring that native binary modules do not throw ABI mismatch errors.")
    bullet(doc, "Repository Cloning: Clone the project code package into the target deployment workspace. The active project layout must conform to the standard structure shown in Listing 7.1.")
    bullet(doc, "Dependency Resolution: From the project root directory, run npm install to resolve and fetch the required dependencies. This installs React 19, Lucide React, SheetJS, JSPDF, and Electron DevDependencies.")

    code_block(doc, """JSPulse-OHMS/
├── electron/
│   ├── main.js        # Main Electron process controller
│   └── preload.js     # Context bridge IPC script
├── src/
│   ├── components/    # React functional view layers (OPD, Pharmacy, etc.)
│   ├── utils/         # sheetDB.js, chatBrain.js, and helper functions
│   ├── App.jsx        # Routing configuration and main layout
│   └── main.jsx       # Entry script with localStorage proxy override
├── public/            # Static assets and icons
├── package.json       # Project configurations and dependency listings
└── vite.config.js     # Dev server and bundler settings""", "Code Listing 7.1: JS Pulse OHMS Development Environment Directory Layout")

    doc.add_heading('7.1.3 Build & Run Commands', level=3)
    para(doc, "The development server is started using Vite, providing hot module replacement (HMR) for the Renderer UI, while Electron is launched simultaneously using a watch script defined in package.json. The CLI commands used during testing, building, and development packaging are listed below:")
    
    code_block(doc, """# Start dev environment with hot-reloading
npm run dev

# Compile React frontend to static assets
npm run build

# Run application inside Electron container
npm run electron:start

# Compile and package application into Windows .exe installer
npm run package""", "Code Listing 7.2: Build, Compilation, and Development Runtime CLI Commands")

    # ───────────────────────────────────────────────────────────
    # 7.2 Build Process & Deployment
    # ───────────────────────────────────────────────────────────
    doc.add_heading('7.2 Build Process & Deployment', level=2)

    para(doc, "The build and deployment process converts the human-readable React and Node.js source files into a production-grade Windows desktop application. Because the target clinic workstations are not connected to the internet, the deployment pipeline must compile all frontend assets, copy native assets, resolve dependency paths, and generate a self-contained offline installer.")

    doc.add_heading('7.2.1 Frontend Compilation and Packaging', level=3)
    para(doc, "The build process consists of three main phases:")
    bullet(doc, "Vite Frontend Compilation: Running 'npm run build' compiles the React 19 application. Vite reads the entries in index.html, runs the ESBuild compiler to bundle the Javascript modules, and processes all CSS assets, outputting the optimized bundle to the /dist folder.")
    bullet(doc, "Asset Optimization: Unused import code is removed through tree-shaking, and CSS styles are minified to reduce memory overhead and speed up component mounting on slower clinic computers.")
    bullet(doc, "Electron Packaging: The electron-builder tool is invoked to bundle the compiled /dist folder, the electron/main.js and preload.js scripts, and a lightweight Node.js runtime into a single Windows NSIS installer.")

    doc.add_heading('7.2.2 Deployment and Common Troubleshooting', level=3)
    para(doc, "The resulting installer, JSPulse-OHMS-Setup-x64.exe, is copied to a USB drive and run on the clinic workstations. On launch, the NSIS installer copies the bin files, registers shortcuts, and creates the default local data directory at C:\\OHSData\\ to store JSON backups and system exports.")
    para(doc, "Common deployment issues and their solutions include:")
    bullet(doc, "Windows Defender SmartScreen Alerts: This alert occurs because the application does not have a commercial code-signing certificate. The installer can be run safely by clicking 'More info' and selecting 'Run anyway'.")
    bullet(doc, "Write Access Denied to C:\\OHSData: This issue occurs if the Windows user account lacks administrative privileges. The solution is to right-click the installer and select 'Run as Administrator', or manually configure full access permissions on the C:\\OHSData directory.")
    bullet(doc, "IndexedDB Corruption Warnings: If database files are corrupted due to sudden power outages, click the 'Reset Connection' button in the System Settings tab to run the auto-recovery routine, which deletes and re-initializes the IndexedDB schema.")

    # ───────────────────────────────────────────────────────────
    # 7.3 Testing Methodologies & Security Validation
    # ───────────────────────────────────────────────────────────
    doc.add_heading('7.3 Testing Methodologies & Security Validation', level=2)

    para(doc, "To verify the application's stability and security for clinical use, the development team implemented a rigorous testing pipeline. This testing verified that the system remains responsive under load and securely isolates clinical records on local storage.")

    doc.add_heading('7.3.1 Software Testing Strategy', level=3)
    para(doc, "The testing strategy follows a structured bottom-up testing pipeline, covering:")
    bullet(doc, "Unit Testing: Individual functional units, such as the recursive spreadsheet formula parser and case-insensitive stock deduction calculations, were verified in isolation using in-memory mock datasets.")
    bullet(doc, "Integration Testing: This phase validated the interaction between modules. For example, testing verified that the background sync engine correctly queries cms_daily_opd_sheet and creates new entries in cms_dispense_log without duplicate processing.")
    bullet(doc, "Functional Testing: User acceptance testing was conducted with the clinic nursing staff to ensure that workflows—such as patient check-in, prescription entry, and stock adjustment—operate smoothly.")

    doc.add_heading('7.3.2 Security Validation and Error Isolation', level=3)
    para(doc, "Security testing focused on verifying the separation of the web UI from native Node.js APIs. The contextBridge interface was audited to confirm that no raw Node.js modules are exposed to the global window scope. Attempts to call Node's fs or path modules from the browser dev console confirmed that the sandbox is secure. Error handling was validated by simulating storage issues (such as filling local storage to the 5MB browser quota). The system successfully handled this by migrating aging records to IndexedDB and saving emergency JSON backups to the local filesystem without data loss.")

    # ───────────────────────────────────────────────────────────
    # 7.4 Conclusion & Future Enhancements (FORCED PAGE BREAK)
    # ───────────────────────────────────────────────────────────
    doc.add_page_break()
    doc.add_heading('7.4 Conclusion & Future Enhancements', level=2)

    para(doc, "The development and deployment of JS Pulse OHMS at the Jindal Steel plant in Patratu successfully addresses the clinic's core administrative challenges. It replaces manual paper record-keeping with a secure, responsive, offline-first clinical application.")

    doc.add_heading('7.4.1 Learning Outcomes and Skills Gained', level=3)
    para(doc, "The internship project provided valuable experience in building production desktop applications using modern web technologies. Key learning outcomes and skills gained include:")
    bullet(doc, "Process Separation Architecture: Gained experience in designing and securing Electron applications using process isolation, context preloading, and safe IPC communication channels.")
    bullet(doc, "DOM Virtualization: Implemented performance optimizations for large-scale data grids using custom viewport calculations and dynamic spacer heights.")
    bullet(doc, "Offline Storage and Connection Pools: Designed resilient local databases using IndexedDB connection pooling and transparent localStorage proxy interception.")
    bullet(doc, "Industrial Safety and Compliance: Developed an understanding of industrial health requirements, chemical exposure tracking, and compliance reporting under the Factories Act, 1948.")

    doc.add_heading('7.4.2 Advantages and Limitations of JS Pulse OHMS', level=3)
    para(doc, "The application offers several key advantages for the plant clinic: it operates fully offline, preventing issues from network drops; features a familiar, Excel-like data grid; uses a debounced instant search interface; and automatically syncs prescriptions between the OPD and pharmacy modules. However, the current implementation has a few limitations: it runs on a single desktop workstation, meaning data cannot be shared across multiple computers in real time; backups must be managed locally on the host hard drive; and the local NLP assistant relies on regular expression matching, which requires precise keyword usage.")

    doc.add_heading('7.4.3 Future Scope and Enhancements', level=3)
    para(doc, "Planned future updates for the system include:")
    bullet(doc, "Local Peer-to-Peer Synchronization: Implementing a local network synchronization protocol (such as Yjs or CouchDB sync) to allow multiple clinic computers to share data in real time without requiring an internet connection.")
    bullet(doc, "Automated Encrypted Backups: Adding support for automated, encrypted backups to the plant's local NAS (Network Attached Storage) to protect against workstation hardware failures.")
    bullet(doc, "Local LLM Integration: Upgrading the local NLP chat assistant to run a small, quantized large language model (such as Llama-3-8B-Instruct via WebGPU) to provide more natural conversational support offline.")

    # ───────────────────────────────────────────────────────────
    # 7.5 References (FORCED PAGE BREAK)
    # ───────────────────────────────────────────────────────────
    doc.add_page_break()
    doc.add_heading('7.5 References', level=2)
    
    para(doc, "The following references cite the official documentations, academic publications, and technical resources used to design, implement, and optimize the JS Pulse OHMS application:")

    reference(doc, "1", "Electron Documentation Team, \"Electron Security Guidelines and Context Isolation,\" Electron Core Documentation, 2024. [Online]. Available: https://www.electronjs.org/docs/latest/tutorial/security. [Accessed: Jan. 15, 2026].")
    reference(doc, "2", "React Core Team, \"React 19 Hooks and Rendering Performance Optimization,\" React Official Documentation, 2024. [Online]. Available: https://react.dev/reference/react. [Accessed: Feb. 10, 2026].")
    reference(doc, "3", "W3C Web Apps Working Group, \"Indexed Database API 3.0 Specification,\" W3C Candidate Recommendation, May 2024. [Online]. Available: https://www.w3.org/TR/IndexedDB-3/. [Accessed: Mar. 05, 2026].")
    reference(doc, "4", "D. Flanagan, JavaScript: The Definitive Guide, 7th ed. Sebastopol, CA: O'Reilly Media, 2020.")
    reference(doc, "5", "Vite Core Team, \"Vite 5.0 Production Bundling and ESBuild Configuration,\" Vite Guide, 2024. [Online]. Available: https://vitejs.dev/guide/build.html. [Accessed: Apr. 12, 2026].")
    reference(doc, "6", "Government of India, \"The Factories Act, 1948: Provisions on Occupational Health and Welfare Centres,\" Ministry of Labour and Employment, Government of India, 1948.")
    reference(doc, "7", "M. Cantelon, M. Harter, T. J. Holowaychuk, and N. Rajlich, Node.js in Action, 2nd ed. Shelter Island, NY: Manning Publications, 2017.")
    reference(doc, "8", "IEEE Computer Society, \"IEEE Standard for Software Test Documentation (IEEE Std 829-2008),\" IEEE Software Engineering Standards, 2008.")
    reference(doc, "9", "A. Hunt and D. Thomas, The Pragmatic Programmer: Your Journey to Mastery, 20th Anniversary Edition. Boston, MA: Addison-Wesley, 2019.")
    reference(doc, "10", "World Health Organization, \"ICD-11: International Classification of Diseases for Mortality and Morbidity Statistics,\" WHO Geneva, 2022.")

    # SAVE
    out_path = 'JSPulse_OHMS_Chapter7_Final_WithBreaks.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == '__main__':
    main()
