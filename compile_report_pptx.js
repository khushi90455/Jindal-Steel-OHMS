import pptxgen from 'pptxgenjs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const pptx = new pptxgen();

// Configure layout
pptx.layout = 'LAYOUT_16x9';
pptx.defineSlideMaster({
  title: 'MASTER_SLIDE',
  background: { color: 'F8FAFC' },
  slideNumber: { x: '95%', y: '95%', fontFace: 'Inter', fontSize: 10, color: '64748B' }
});

// Colors
const COLOR_PRIMARY_DARK = '1E3A8A'; // Blue 900
const COLOR_PRIMARY = '3B82F6';      // Blue 500
const COLOR_ACCENT_ORANGE = 'F97316'; // Orange 500
const COLOR_ACCENT_GREEN = '10B981';  // Emerald 500
const COLOR_TEXT_DARK = '0F172A';     // Slate 900
const COLOR_TEXT_MUTED = '475569';    // Slate 600
const COLOR_BG_WHITE = 'FFFFFF';
const COLOR_BG_DARK = '0F172A';

// Helper to add slide header
function addSlideHeader(slide, title) {
  slide.addText(title, {
    x: 0.6,
    y: 0.4,
    w: 12.1,
    h: 0.6,
    fontSize: 22,
    bold: true,
    color: COLOR_PRIMARY_DARK,
    fontFace: 'Outfit'
  });
  
  // Underline bar
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.6,
    y: 1.0,
    w: 12.1,
    h: 0.04,
    fill: { color: COLOR_PRIMARY }
  });
}

// ----------------------------------------------------
// SLIDE 1: Title Slide (Dark Theme)
// ----------------------------------------------------
const slide1 = pptx.addSlide();
slide1.background = { color: COLOR_BG_DARK };

// Orange Accent Bar
slide1.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6,
  y: 1.2,
  w: 1.5,
  h: 0.08,
  fill: { color: COLOR_ACCENT_ORANGE }
});

// Title
slide1.addText('JSPulse OHMS\nOCCUPATIONAL HEALTH MANAGEMENT SYSTEM', {
  x: 0.6,
  y: 1.5,
  w: 12.1,
  h: 1.8,
  fontSize: 34,
  bold: true,
  color: 'FFFFFF',
  fontFace: 'Outfit'
});

// Subtitle
slide1.addText('A Technical Internship Report on an Offline-First Enterprise Occupational Health and Safety Registry', {
  x: 0.6,
  y: 3.4,
  w: 12.1,
  h: 0.5,
  fontSize: 16,
  color: '94A3B8',
  fontFace: 'Inter'
});

// Horizontal Divider
slide1.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6,
  y: 4.2,
  w: 12.1,
  h: 0.02,
  fill: { color: '334155' }
});

// Details Grid
slide1.addText('Developed By:\nAshwini Kumar\nIntern ID: JSPL-2026-IT-042', {
  x: 0.6,
  y: 4.6,
  w: 3.8,
  h: 1.2,
  fontSize: 13,
  color: 'CBD5E1',
  fontFace: 'Inter'
});

slide1.addText('Host Organization:\nJindal Steel\nRaigarh Plant Clinic Operations', {
  x: 4.8,
  y: 4.6,
  w: 3.8,
  h: 1.2,
  fontSize: 13,
  color: 'CBD5E1',
  fontFace: 'Inter'
});

slide1.addText('Academic & Industry Mentors:\nSenior Medical Officer (OHC)\nLead Systems Administrator (IT)', {
  x: 9.0,
  y: 4.6,
  w: 3.7,
  h: 1.2,
  fontSize: 13,
  color: 'CBD5E1',
  fontFace: 'Inter'
});

// Green Accent Bar at Bottom
slide1.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6,
  y: 6.2,
  w: 12.1,
  h: 0.08,
  fill: { color: COLOR_ACCENT_GREEN }
});


// ----------------------------------------------------
// SLIDE 2: Executive Summary
// ----------------------------------------------------
const slide2 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide2, 'EXECUTIVE SUMMARY');

slide2.addText('Industrial steel plants (blast furnaces, melt shops) operate in high-risk environments. Health and safety readiness is mandated under the Indian Factories Act, 1948.', {
  x: 0.6,
  y: 1.3,
  w: 12.1,
  h: 0.8,
  fontSize: 15,
  bold: true,
  color: COLOR_PRIMARY_DARK,
  fontFace: 'Inter'
});

// Left Column - The Problem
slide2.addText('Manual Ledger Challenges:\n' +
  '• Fragmented clinical patient logs across paper notebooks\n' +
  '• Redundant double-entry copying prescription records\n' +
  '• Serious risks of expired drug dispensing\n' +
  '• Time-consuming manual audits for medical compliance', {
  x: 0.6,
  y: 2.3,
  w: 5.8,
  h: 4.0,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});

// Right Column - The Solution
slide2.addText('JSPulse OHMS Solution:\n' +
  '• Offline-First Desktop App (Electron + React 19 + Vite)\n' +
  '• Custom high-performance spreadsheet engine (ExcelGrid)\n' +
  '• Automatic background OPD-to-Dispense synchronizer\n' +
  '• Persistent IndexedDB data pool bypassing 5MB limits\n' +
  '• Color-coded alarms for expirations and medical checks', {
  x: 6.8,
  y: 2.3,
  w: 5.8,
  h: 4.0,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});


// ----------------------------------------------------
// SLIDE 3: System Architecture
// ----------------------------------------------------
const slide3 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide3, 'SYSTEM ARCHITECTURE: ELECTRON & REACT');

slide3.addText('The application leverages Electron to package React 19 into a native desktop container, securing system-level operations in an offline sandbox.', {
  x: 0.6,
  y: 1.3,
  w: 12.1,
  h: 0.6,
  fontSize: 14,
  italic: true,
  color: COLOR_TEXT_MUTED,
  fontFace: 'Inter'
});

// Two Blocks: Main Process vs Renderer Process
// Block 1: Main Process
slide3.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.6,
  y: 2.1,
  w: 5.7,
  h: 4.3,
  fill: { color: 'E2E8F0' },
  line: { color: 'CBD5E1', width: 1 }
});

slide3.addText('Electron Main Process (main.js)\n' +
  '• Direct operating system execution layer\n' +
  '• Manages native BrowserWindow instance\n' +
  '• Handles system file dialogs for backup/restore\n' +
  '• Runs headless print-to-PDF Chrome engine\n' +
  '• Secures desktop isolation (sandbox = true)', {
  x: 0.8,
  y: 2.3,
  w: 5.3,
  h: 3.9,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});

// Block 2: Renderer Process
slide3.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 6.8,
  y: 2.1,
  w: 5.9,
  h: 4.3,
  fill: { color: 'E0F2FE' },
  line: { color: 'BAE6FD', width: 1 }
});

slide3.addText('Renderer Process (React 19)\n' +
  '• Component-driven UI client layer\n' +
  '• Double-buffered state arrays and portals\n' +
  '• Renders ExcelGrid engine & Recharts analytics\n' +
  '• Secure Preload contextBridge IPC bindings\n' +
  '• Automatic IndexedDB database storage pool', {
  x: 7.0,
  y: 2.3,
  w: 5.5,
  h: 3.9,
  fontSize: 14,
  color: COLOR_PRIMARY_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});


// ----------------------------------------------------
// SLIDE 4: Database Architecture & sheetDB
// ----------------------------------------------------
const slide4 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide4, 'DATABASE DRIVER: BYPASSING STORAGE LIMITS');

// Left Text
slide4.addText('Browser-based applications are restricted to a 5MB localStorage limit. Storing 10+ clinical sheets quickly crashes operations.\n\n' +
  'IndexedDB Storage Solution:\n' +
  '• Custom DB Driver (sheetDB.js) wraps transactions\n' +
  '• Expands local data quota to 50MB - 250MB+ on physical disk\n' +
  '• Structured Object Stores: sheet_data for rows, sheet_meta for schema\n' +
  '• Connection Pooling: Automatically recovers on connection drops\n' +
  '• LevelDB persistence ensures offline-first local speed', {
  x: 0.6,
  y: 1.4,
  w: 6.2,
  h: 4.8,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});

// Right block: Table Layout
slide4.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 7.2,
  y: 1.4,
  w: 5.5,
  h: 4.8,
  fill: { color: 'F1F5F9' },
  line: { color: 'E2E8F0', width: 1 }
});

// Title of schema
slide4.addText('Key Object Store Schemas:', {
  x: 7.4,
  y: 1.6,
  w: 5.1,
  h: 0.4,
  fontSize: 14,
  bold: true,
  color: COLOR_PRIMARY_DARK,
  fontFace: 'Outfit'
});

slide4.addText('• cms_daily_opd_sheet: Logs dates, employee codes, doctor names, diagnoses, and prescription tags.\n\n' +
  '• cms_dispense_log: Links patient names, prescribed items, dispensed quantities, and transaction statuses.\n\n' +
  '• cms_medstock_data: Medicine stock levels, batch details, reorder warnings, and expiration dates.', {
  x: 7.4,
  y: 2.2,
  w: 5.1,
  h: 3.8,
  fontSize: 13,
  color: COLOR_TEXT_MUTED,
  fontFace: 'Inter',
  lineSpacing: 18
});


// ----------------------------------------------------
// SLIDE 5: Core Engineering: ExcelGrid
// ----------------------------------------------------
const slide5 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide5, 'THE EXCELGRID SPREADSHEET ENGINE');

slide5.addText('To bridge the transition from manual ledger books, the system uses a custom React spreadsheet engine matching Microsoft Excel workflows.', {
  x: 0.6,
  y: 1.3,
  w: 12.1,
  h: 0.6,
  fontSize: 14,
  italic: true,
  color: COLOR_TEXT_MUTED,
  fontFace: 'Inter'
});

// Three Columns of features
// Col 1: Keystroke Navigation
slide5.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.6,
  y: 2.1,
  w: 3.8,
  h: 4.3,
  fill: { color: 'FFFFFF' },
  line: { color: 'E2E8F0', width: 1 }
});
slide5.addText('Keystroke Controls\n\n' +
  '• Tab / Shift+Tab: Move focus horizontally\n' +
  '• Enter / Shift+Enter: Commit edit, move vertically\n' +
  '• Escape: Cancel edits, return to cell selection\n' +
  '• Ctrl+Z / Ctrl+Y: Undo/Redo stack navigation', {
  x: 0.8,
  y: 2.3,
  w: 3.4,
  h: 3.9,
  fontSize: 13,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter'
});

// Col 2: Formula Parser
slide5.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 4.75,
  y: 2.1,
  w: 3.8,
  h: 4.3,
  fill: { color: 'FFFFFF' },
  line: { color: 'E2E8F0', width: 1 }
});
slide5.addText('Dynamic Formula Engine\n\n' +
  '• Evaluates cell expressions starting with =\n' +
  '• Supports coordinates calculations (e.g. A1+B2)\n' +
  '• Evaluates ranges (e.g. SUM(C1:C10))\n' +
  '• Circular reference checking prevents infinite loops', {
  x: 4.95,
  y: 2.3,
  w: 3.4,
  h: 3.9,
  fontSize: 13,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter'
});

// Col 3: Viewport Virtualization
slide5.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 8.9,
  y: 2.1,
  w: 3.8,
  h: 4.3,
  fill: { color: 'FFFFFF' },
  line: { color: 'E2E8F0', width: 1 }
});
slide5.addText('Viewport Virtualization\n\n' +
  '• Computes absolute row offsets heights dynamically\n' +
  '• Renders only visible rows in the browser viewport\n' +
  '• Handles 10,000+ data rows with zero keystroke lag\n' +
  '• Automatically disables during print runs', {
  x: 9.1,
  y: 2.3,
  w: 3.4,
  h: 3.9,
  fontSize: 13,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter'
});


// ----------------------------------------------------
// SLIDE 6: Automated Sync Pipelines
// ----------------------------------------------------
const slide6 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide6, 'AUTOMATED DATA SYNC PIPELINES');

// Left Column - OPD to Pharmacy
slide6.addText('OPD-to-Dispense Synchronization:\n' +
  '• Background polling sync thread runs every 10 seconds\n' +
  '• Scans Daily OPD ledger rows for prescription text\n' +
  '• Extracts name, employee code, dosage, and doctor details\n' +
  '• Pushes new record to Clinical Dispense Queue as Pending\n' +
  '• Sets extracted = true on OPD row to prevent duplicates\n' +
  '• Eliminates double manual copying data entries', {
  x: 0.6,
  y: 1.5,
  w: 5.8,
  h: 4.8,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});

// Right Column - Stock Deduction
slide6.addText('Pharmacy Inventory Decrement:\n' +
  '• Pharmacist reviews queue item, clicks "Deduct & Save"\n' +
  '• Core script matches drug name against Stock register\n' +
  '• Automatically deducts quantity from active stock balances\n' +
  '• Out-of-Stock Catch: Warns pharmacist if drug count is low\n' +
  '• Flags missing items as "Out of Stock" to protect database\n' +
  '• Dynamic Undo: Pharmacist can restore stock instantly if erroneous', {
  x: 6.8,
  y: 1.5,
  w: 5.8,
  h: 4.8,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});


// ----------------------------------------------------
// SLIDE 7: UI Features & HSE Compliance
// ----------------------------------------------------
const slide7 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide7, 'HSE COMPLIANCE & UI CAPABILITIES');

// Two Columns: Features list
// Left
slide7.addText('Compliance Registries:\n' +
  '• Annual Checkups: Logs Factories Act vision, lung, and hearing tests. Overdues highlight in Red.\n\n' +
  '• Injury Logs: Logs plant accidents, departments, and doctor remarks in compliance with Form 21.\n\n' +
  '• Occupational Disease: Tracks chronic worker conditions (Silicosis, Hearing Loss) for chief inspectors.\n\n' +
  '• Ambulance Dispatch: Emergency 🚨 dispatch logger instantly timestamps and tracks dispatch stages.', {
  x: 0.6,
  y: 1.4,
  w: 5.8,
  h: 5.0,
  fontSize: 13,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 18
});

// Right
slide7.addText('Interactive Capabilities:\n' +
  '• Real-time Dashboard: Compiles KPI widgets, radial stock health charts, and top-8 medicine counts.\n\n' +
  '• Local AI Assistant (chatBrain.js): NLP chatbot works 100% offline. Answers medical guidelines queries and deep-searches database entries.\n\n' +
  '• Interaction Checker: Evaluates selected drugs against a matrix of contraindications (e.g. NSAIDs + Warfarin).\n\n' +
  '• System Health Tool: Quota estimator, clean database repair, and backup file migration systems.', {
  x: 6.8,
  y: 1.4,
  w: 5.8,
  h: 5.0,
  fontSize: 13,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 18
});


// ----------------------------------------------------
// SLIDE 8: System Health & Headless Printing
// ----------------------------------------------------
const slide8 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide8, 'SYSTEM HEALTH & HEADLESS PRINT PREVIEW');

// Left Column - Storage Quota
slide8.addText('Storage Quota Optimization:\n' +
  '• System Health Tool monitors database storage sizes\n' +
  '• Automatically checks for legacy backups in localStorage\n' +
  '• Runs database migrations to move backup data to IndexedDB\n' +
  '• Frees browser storage to prevent save block exceptions\n' +
  '• Ensures 100% database schema auto-migrations during upgrades\n' +
  '• Protects historical employee health card records', {
  x: 0.6,
  y: 1.5,
  w: 5.8,
  h: 4.8,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});

// Right Column - Headless Printing
slide8.addText('Headless PDF Print Preview Flow:\n' +
  '• Client clicks "Print Preview" button in UI\n' +
  '• React hooks invoke preload contextBridge channel\n' +
  '• IPC message is intercepted by electron/main.js\n' +
  '• Electron invokes printToPDF and generates binary buffer\n' +
  '• Buffer is written to OS temporary folder\n' +
  '• OS default PDF viewer opens file instantly (Adobe/Edge)\n' +
  '• Prevents system dialog popup clutter', {
  x: 6.8,
  y: 1.5,
  w: 5.8,
  h: 4.8,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});


// ----------------------------------------------------
// SLIDE 9: Project Outcomes
// ----------------------------------------------------
const slide9 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide9, 'PROJECT OUTCOMES: BEFORE VS AFTER');

// Comparison Table Data
const tableRows = [
  [
    { text: 'Operational Task', options: { bold: true, fill: '1E3A8A', color: 'FFFFFF' } },
    { text: 'Paper Ledger System (Before)', options: { bold: true, fill: '1E3A8A', color: 'FFFFFF' } },
    { text: 'Digital JSPulse OHMS (After)', options: { bold: true, fill: '1E3A8A', color: 'FFFFFF' } },
    { text: 'Improvement Metric', options: { bold: true, fill: '1E3A8A', color: 'FFFFFF' } }
  ],
  ['Recording OPD visits', 'Hand-written in paper ledger (1-2 mins)', 'Keyboard entry in ExcelGrid (10-15 secs)', '80% faster logging'],
  ['Dispensing medicines', 'Manually copied from OPD log (1 min)', 'Auto-syncs to pharmacy queue (Instant)', 'Double entry eliminated'],
  ['Stock deductions', 'Recalculated by hand daily (30 mins)', 'Automated on pharmacist confirm (Instant)', 'Stock errors eliminated'],
  ['Finding expired drugs', 'Manual checks of shelves', 'Highlighted in Red in Stock Register', '100% automated alerts'],
  ['Auditing compliance', 'Manual page-by-page register searches', 'One-click Excel & PDF exports', 'Audit-ready in seconds']
];

// Draw table
slide9.addTable(tableRows, {
  x: 0.6,
  y: 1.5,
  w: 12.1,
  h: 4.0,
  fontSize: 12,
  fontFace: 'Inter',
  align: 'left',
  border: { color: 'CBD5E1', width: 1 }
});

slide9.addText('Conclusion: The implementation of JSPulse OHMS successfully eliminated clinical redundancy, ensured safety compliance reporting, and established offline-first resilience.', {
  x: 0.6,
  y: 5.8,
  w: 12.1,
  h: 0.5,
  fontSize: 13,
  italic: true,
  bold: true,
  color: COLOR_PRIMARY_DARK,
  fontFace: 'Inter'
});


// ----------------------------------------------------
// SLIDE 11: FLOWCHART: System Bootstrap & DB Pool Driver
// ----------------------------------------------------
const slide11 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide11, 'BOOTSTRAP & DATABASE CONNECTION FLOW');

// Node 1: Start
slide11.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.8, w: 2.2, h: 1.0, fill: { color: '1E3A8A' } });
slide11.addText('User launches\nJSPulse App', { x: 0.6, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 1 -> 2
slide11.addShape(pptx.shapes.RIGHT_ARROW, { x: 2.9, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 2: Electron runs main.js
slide11.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide11.addText('main.js runs\n& starts window', { x: 3.4, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 2 -> 3
slide11.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 3: React Mounts
slide11.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide11.addText('React mounts\nApp.jsx View', { x: 6.2, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 3 -> 4
slide11.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.5, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 4: DB tests connection
slide11.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide11.addText('sheetDB.js opens\nIndexedDB Pool', { x: 9.0, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 4 -> 5 (DOWN)
slide11.addShape(pptx.shapes.DOWN_ARROW, { x: 9.9, y: 2.9, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 5: Decision (Diamond)
slide11.addShape(pptx.shapes.DIAMOND, { x: 9.0, y: 3.4, w: 2.2, h: 1.2, fill: { color: 'FEF3C7' }, line: { color: 'F59E0B', width: 1 } });
slide11.addText('Connection\nNominal?', { x: 9.0, y: 3.4, w: 2.2, h: 1.2, align: 'center', color: 'B45309', fontSize: 10, bold: true, fontFace: 'Inter' });

// Arrow 5 -> 6 (LEFT - YES)
slide11.addShape(pptx.shapes.LEFT_ARROW, { x: 8.5, y: 3.8, w: 0.4, h: 0.4, fill: { color: '10B981' } });
slide11.addText('YES', { x: 8.5, y: 3.4, w: 0.4, h: 0.3, align: 'center', color: '10B981', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 6: Quota check
slide11.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 3.5, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide11.addText('Verify quota via\nbackupDB.js', { x: 6.2, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 6 -> 7
slide11.addShape(pptx.shapes.LEFT_ARROW, { x: 5.7, y: 3.8, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 7: Dashboard Render
slide11.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 3.5, w: 2.2, h: 1.0, fill: { color: '10B981' } });
slide11.addText('Dashboard KPI\nRendered Offline', { x: 3.4, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 5 -> 8 (DOWN - NO)
slide11.addShape(pptx.shapes.DOWN_ARROW, { x: 9.9, y: 4.7, w: 0.4, h: 0.4, fill: { color: 'EF4444' } });
slide11.addText('NO', { x: 10.4, y: 4.7, w: 0.4, h: 0.3, align: 'center', color: 'EF4444', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 8: Recovery
slide11.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 5.2, w: 2.2, h: 1.0, fill: { color: 'FEE2E2' }, line: { color: 'FCA5A5', width: 1 } });
slide11.addText('Trigger DB Pool\nConnection Recovery', { x: 9.0, y: 5.2, w: 2.2, h: 1.0, align: 'center', color: '991B1B', fontSize: 11, bold: true, fontFace: 'Inter' });


// ----------------------------------------------------
// SLIDE 12: FLOWCHART: Prescription Sync & Stock Deduction
// ----------------------------------------------------
const slide12 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide12, 'PRESCRIPTION SYNC & INVENTORY FLOW');

// Node 1
slide12.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.8, w: 2.2, h: 1.0, fill: { color: '1E3A8A' } });
slide12.addText('Nurse logs\nprescription in OPD', { x: 0.6, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 1 -> 2
slide12.addShape(pptx.shapes.RIGHT_ARROW, { x: 2.9, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 2
slide12.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide12.addText('OPD row saved\n(extracted = false)', { x: 3.4, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 2 -> 3
slide12.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 3
slide12.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide12.addText('Sync thread polls\nOPD table (10s)', { x: 6.2, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 3 -> 4
slide12.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.5, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 4
slide12.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide12.addText('Pushed to Dispense\nQueue as Pending', { x: 9.0, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 4 -> 5 (DOWN)
slide12.addShape(pptx.shapes.DOWN_ARROW, { x: 9.9, y: 2.9, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 5
slide12.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 3.5, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide12.addText('Pharmacist clicks\n"Deduct & Save"', { x: 9.0, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 5 -> 6 (LEFT)
slide12.addShape(pptx.shapes.LEFT_ARROW, { x: 8.5, y: 3.8, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 6
slide12.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 3.5, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide12.addText('Stock Registry\ncounts decremented', { x: 6.2, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 6 -> 7
slide12.addShape(pptx.shapes.LEFT_ARROW, { x: 5.7, y: 3.8, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 7
slide12.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 3.5, w: 2.2, h: 1.0, fill: { color: '10B981' } });
slide12.addText('DailyConsume & Balance\nSheets updated', { x: 3.4, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });


// ----------------------------------------------------
// SLIDE 13: FLOWCHART: Headless PDF Print Compiler
// ----------------------------------------------------
const slide13 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide13, 'HEADLESS PDF COMPILER FLOW');

// Node 1
slide13.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.8, w: 2.2, h: 1.0, fill: { color: '1E3A8A' } });
slide13.addText('User triggers\nPrint Preview in UI', { x: 0.6, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 1 -> 2
slide13.addShape(pptx.shapes.RIGHT_ARROW, { x: 2.9, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 2
slide13.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide13.addText('Preload bridge\ninvokes IPC channel', { x: 3.4, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 2 -> 3
slide13.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 3
slide13.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide13.addText('main.js intercepts\n"preview-print"', { x: 6.2, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 3 -> 4
slide13.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.5, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 4
slide13.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide13.addText('webContents invokes\nprintToPDF API', { x: 9.0, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 4 -> 5 (DOWN)
slide13.addShape(pptx.shapes.DOWN_ARROW, { x: 9.9, y: 2.9, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 5
slide13.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 3.5, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide13.addText('Writes PDF buffer\nto OS temp directory', { x: 9.0, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 5 -> 6 (LEFT)
slide13.addShape(pptx.shapes.LEFT_ARROW, { x: 8.5, y: 3.8, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 6
slide13.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 3.5, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide13.addText('OS shell calls\nopenPath(tempFile)', { x: 6.2, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 6 -> 7
slide13.addShape(pptx.shapes.LEFT_ARROW, { x: 5.7, y: 3.8, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 7
slide13.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 3.5, w: 2.2, h: 1.0, fill: { color: '10B981' } });
slide13.addText('Launches default PDF\nViewer application', { x: 3.4, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });


// ----------------------------------------------------
// SLIDE 14: CODE: Formula Evaluation Algorithm
// ----------------------------------------------------
const slide14 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide14, 'CODE: EXCELGRID FORMULA EVALUATION');

slide14.addText('Evaluates spreadsheet cell equations dynamically. Handles coordinates and ranges (like SUM) recursively with depth guards:', {
  x: 0.6, y: 1.2, w: 12.1, h: 0.5, fontSize: 13, color: COLOR_TEXT_MUTED, fontFace: 'Inter'
});

slide14.addText('// Recursively evaluates Excel formulas in cell edits\n' +
  'const evaluateFormula = (formulaStr, allData, cols, depth = 0) => {\n' +
  '  if (depth > 50) return 0; // Circular reference guard\n' +
  '  if (!formulaStr || !String(formulaStr).startsWith(\'=\')) return formulaStr;\n' +
  '  try {\n' +
  '    let expr = String(formulaStr).substring(1).toUpperCase();\n' +
  '    // Resolve SUM(C1:C10) ranges\n' +
  '    expr = expr.replace(/SUM\\(([A-Z]+)(\\d+):([A-Z]+)(\\d+)\\)/g, (match, c1, r1, c2, r2) => {\n' +
  '      let sum = 0;\n' +
  '      const startR = Math.min(parseInt(r1), parseInt(r2)) - 1;\n' +
  '      const endR = Math.max(parseInt(r1), parseInt(r2)) - 1;\n' +
  '      const c1Idx = cols.findIndex(c => c.letter === c1), c2Idx = cols.findIndex(c => c.letter === c2);\n' +
  '      for (let r = startR; r <= endR; r++) {\n' +
  '        for (let c = Math.min(c1Idx, c2Idx); c <= Math.max(c1Idx, c2Idx); c++) {\n' +
  '          const num = parseFloat(evaluateFormula(allData[r][cols[c].key], allData, cols, depth + 1));\n' +
  '          if (!isNaN(num)) sum += num;\n' +
  '        }\n' +
  '      }\n' +
  '      return sum;\n' +
  '    });\n' +
  '    return eval(expr); // Evaluate expressions\n' +
  '  } catch (err) { return \'#ERROR!\'; }\n' +
  '};', {
  x: 0.6, y: 1.8, w: 12.1, h: 4.8, fontSize: 11.5, fontFace: 'Fira Code', color: '0F172A',
  fill: { color: 'F1F5F9' }, inset: 15
});


// ----------------------------------------------------
// SLIDE 15: CODE: Persistent IndexedDB Driver (sheetDB)
// ----------------------------------------------------
const slide15 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide15, 'CODE: PERSISTENT INDEXEDDB CONNECTION POOL');

slide15.addText('Wraps asynchronous IndexedDB connections in a persistent, self-healing pool to prevent memory leaks and transaction drops:', {
  x: 0.6, y: 1.2, w: 12.1, h: 0.5, fontSize: 13, color: COLOR_TEXT_MUTED, fontFace: 'Inter'
});

slide15.addText('let _dbInstance = null, _dbPromise = null;\n' +
  'function getDB() {\n' +
  '  if (_dbInstance) {\n' +
  '    try {\n' +
  '      const testTx = _dbInstance.transaction(\'sheet_data\', \'readonly\');\n' +
  '      testTx.abort();\n' +
  '      return Promise.resolve(_dbInstance);\n' +
  '    } catch (e) {\n' +
  '      _dbInstance.close(); _dbInstance = null; _dbPromise = null; // Stale conn: reset\n' +
  '    }\n' +
  '  }\n' +
  '  if (_dbPromise) return _dbPromise;\n' +
  '  _dbPromise = new Promise((resolve, reject) => {\n' +
  '    const request = indexedDB.open(\'JSPulseOHMS_Sheets\', 1);\n' +
  '    request.onsuccess = () => {\n' +
  '      _dbInstance = request.result;\n' +
  '      _dbInstance.onclose = () => { _dbInstance = null; _dbPromise = null; };\n' +
  '      resolve(_dbInstance);\n' +
  '    };\n' +
  '    request.onerror = () => { _dbInstance = null; _dbPromise = null; reject(request.error); };\n' +
  '  });\n' +
  '  return _dbPromise;\n' +
  '}', {
  x: 0.6, y: 1.8, w: 12.1, h: 4.8, fontSize: 11.5, fontFace: 'Fira Code', color: '0F172A',
  fill: { color: 'F1F5F9' }, inset: 15
});


// ----------------------------------------------------
// SLIDE 16: CODE: DOM Viewport Virtualization
// ----------------------------------------------------
const slide16 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide16, 'CODE: VIEWPORT VIRTUALIZATION SCROLL');

slide16.addText('Renders only DOM elements inside the container scroll boundaries. Keeps rendering speeds high for 10,000+ data rows:', {
  x: 0.6, y: 1.2, w: 12.1, h: 0.5, fontSize: 13, color: COLOR_TEXT_MUTED, fontFace: 'Inter'
});

slide16.addText('// Calculates vertical offsets of visible elements\n' +
  'const { visibleRows, topSpacerHeight, bottomSpacerHeight } = useMemo(() => {\n' +
  '  if (isPrinting) return { visibleRows: filteredData, topSpacerHeight: 0, bottomSpacerHeight: 0 };\n' +
  '  const offsets = []; let current = 0;\n' +
  '  for (let i = 0; i < filteredData.length; i++) {\n' +
  '    offsets.push(current);\n' +
  '    current += rowHeights[rowToIndexMap.get(filteredData[i])] || 30; // Row height index\n' +
  '  }\n' +
  '  const totalHeight = current;\n' +
  '  const viewportTop = Math.max(0, scrollTop - 150);\n' +
  '  const viewportBottom = scrollTop + containerHeight + 150;\n' +
  '  let startIndex = offsets.findIndex(offset => offset > viewportTop);\n' +
  '  startIndex = startIndex === -1 ? 0 : Math.max(0, startIndex - 1);\n' +
  '  let endIndex = offsets.findIndex(offset => offset > viewportBottom);\n' +
  '  endIndex = endIndex === -1 ? filteredData.length - 1 : endIndex;\n' +
  '  \n' +
  '  return {\n' +
  '    visibleRows: filteredData.slice(startIndex, endIndex + 1),\n' +
  '    topSpacerHeight: offsets[startIndex] || 0,\n' +
  '    bottomSpacerHeight: Math.max(0, totalHeight - (offsets[endIndex] || totalHeight))\n' +
  '  };\n' +
  '}, [filteredData, rowHeights, scrollTop, containerHeight, isPrinting]);', {
  x: 0.6, y: 1.8, w: 12.1, h: 4.8, fontSize: 10.5, fontFace: 'Fira Code', color: '0F172A',
  fill: { color: 'F1F5F9' }, inset: 15
});


// ----------------------------------------------------
// SLIDE 17: CODE: Expiry checks & State-Safe Mutations
// ----------------------------------------------------
const slide17 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide17, 'CODE: IMMUTABLE CELLS & COLOR ALERT HIGH');

slide17.addText('Safe mutation copying logic that avoids assignment errors on frozen React arrays. Combines with automatic expiration date highlights:', {
  x: 0.6, y: 1.2, w: 12.1, h: 0.5, fontSize: 13, color: COLOR_TEXT_MUTED, fontFace: 'Inter'
});

slide17.addText('// Performs deep copy updates on sheet edits\n' +
  'const handleCellChange = (rowIndex, colKey, value) => {\n' +
  '  pushUndo(); // Record current state on stack\n' +
  '  setData(prevData => {\n' +
  '    const nextData = [...prevData];\n' +
  '    const targetRow = { ...nextData[rowIndex] }; // Clone target row object\n' +
  '    targetRow[colKey] = value;\n' +
  '    \n' +
  '    // Automatic Expiry Status evaluation\n' +
  '    if (colKey === \'expiry\') {\n' +
  '      const expDate = new Date(value);\n' +
  '      const now = new Date();\n' +
  '      const soon = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);\n' +
  '      targetRow.expiryStatus = expDate < now ? \'Expired\' : expDate <= soon ? \'Critical\' : \'In Stock\';\n' +
  '    }\n' +
  '    nextData[rowIndex] = targetRow;\n' +
  '    return nextData;\n' +
  '  });\n' +
  '};', {
  x: 0.6, y: 1.8, w: 12.1, h: 4.8, fontSize: 11, fontFace: 'Fira Code', color: '0F172A',
  fill: { color: 'F1F5F9' }, inset: 15
});


// ----------------------------------------------------
// SLIDE 18: CODE: Electron IPC Print Preview Handler
// ----------------------------------------------------
const slide18 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide18, 'CODE: ELECTRON NATIVE IPC PRINT PROCESS');

slide18.addText('Electron main process intercepts the print command, captures the BrowserWindow viewport, and prints a headless PDF stream:', {
  x: 0.6, y: 1.2, w: 12.1, h: 0.5, fontSize: 13, color: COLOR_TEXT_MUTED, fontFace: 'Inter'
});

slide18.addText('// Intercepts preview-print event from Renderer process\n' +
  'ipcMain.on(\'preview-print\', async (event) => {\n' +
  '  const win = BrowserWindow.fromWebContents(event.sender);\n' +
  '  try {\n' +
  '    // headless render to PDF using Chromium engine\n' +
  '    const pdfData = await win.webContents.printToPDF({\n' +
  '      printBackground: true,\n' +
  '      pageSize: \'A4\',\n' +
  '      margins: { top: 1, bottom: 1, left: 1, right: 1 },\n' +
  '      landscape: true // Sheets print in landscape\n' +
  '    });\n' +
  '    const tempPath = path.join(os.tmpdir(), `print-preview-${Date.now()}.pdf`);\n' +
  '    fs.writeFileSync(tempPath, pdfData);\n' +
  '    \n' +
  '    // Open file in default system PDF viewer\n' +
  '    const err = await shell.openPath(tempPath);\n' +
  '    if (err) throw new Error(err);\n' +
  '  } catch (error) {\n' +
  '    console.error(\'PDF printing failed:\', error);\n' +
  '    win.webContents.print({ silent: false, printBackground: true }); // Fallback\n' +
  '  }\n' +
  '});', {
  x: 0.6, y: 1.8, w: 12.1, h: 4.8, fontSize: 11, fontFace: 'Fira Code', color: '0F172A',
  fill: { color: 'F1F5F9' }, inset: 15
});


// ----------------------------------------------------
// SLIDE 19: FLOWCHART: Offline NLP Database Search Flow
// ----------------------------------------------------
const slide19 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide19, 'FLOWCHART: OFFLINE NLP DATABASE SEARCH FLOW');

// Node 1
slide19.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.8, w: 2.2, h: 1.0, fill: { color: '1E3A8A' } });
slide19.addText('User enters query\nin ChatAssistant', { x: 0.6, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 1 -> 2
slide19.addShape(pptx.shapes.RIGHT_ARROW, { x: 2.9, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 2
slide19.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide19.addText('Tokenize and\nnormalize terms', { x: 3.4, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 2 -> 3
slide19.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 3 (Decision)
slide19.addShape(pptx.shapes.DIAMOND, { x: 6.2, y: 1.7, w: 2.2, h: 1.2, fill: { color: 'FEF3C7' }, line: { color: 'F59E0B', width: 1 } });
slide19.addText('Match Clinical\nRules?', { x: 6.2, y: 1.7, w: 2.2, h: 1.2, align: 'center', color: 'B45309', fontSize: 10, bold: true, fontFace: 'Inter' });

// Arrow 3 -> 4 (DOWN - YES)
slide19.addShape(pptx.shapes.DOWN_ARROW, { x: 7.1, y: 3.0, w: 0.4, h: 0.4, fill: { color: '10B981' } });
slide19.addText('YES', { x: 7.6, y: 3.0, w: 0.4, h: 0.3, align: 'center', color: '10B981', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 4 (Clinical response)
slide19.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 3.6, w: 2.2, h: 1.0, fill: { color: '10B981' } });
slide19.addText('Return First Aid /\nDosage response', { x: 6.2, y: 3.6, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 3 -> 5 (RIGHT - NO)
slide19.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.5, y: 2.1, w: 0.4, h: 0.4, fill: { color: 'EF4444' } });
slide19.addText('NO', { x: 8.5, y: 1.7, w: 0.4, h: 0.3, align: 'center', color: 'EF4444', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 5 (DB Search)
slide19.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide19.addText('Scan database keys\nin localStorage', { x: 9.0, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 5 -> 6 (DOWN)
slide19.addShape(pptx.shapes.DOWN_ARROW, { x: 9.9, y: 2.9, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 6 (Parse JSON)
slide19.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 3.5, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide19.addText('Parse JSON arrays\n& score matches', { x: 9.0, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 6 -> 7 (LEFT)
slide19.addShape(pptx.shapes.LEFT_ARROW, { x: 8.5, y: 3.8, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 7 (Display results)
slide19.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 5.0, w: 2.2, h: 1.0, fill: { color: 'E0F2FE' }, line: { color: 'BAE6FD', width: 1 } });
slide19.addText('Display top matching\nrecords in Markdown', { x: 9.0, y: 5.0, w: 2.2, h: 1.0, align: 'center', color: '0369A1', fontSize: 11, bold: true, fontFace: 'Inter' });


// ----------------------------------------------------
// SLIDE 20: FLOWCHART: Quota Check and Backup Migration
// ----------------------------------------------------
const slide20 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide20, 'FLOWCHART: QUOTA & BACKUP MIGRATION FLOW');

// Node 1
slide20.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.8, w: 2.2, h: 1.0, fill: { color: '1E3A8A' } });
slide20.addText('SystemHealthTool\nis mounted', { x: 0.6, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 1 -> 2
slide20.addShape(pptx.shapes.RIGHT_ARROW, { x: 2.9, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 2
slide20.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide20.addText('Estimate local\nquota bytes (UTF-16)', { x: 3.4, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 2 -> 3
slide20.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 3 (Decision)
slide20.addShape(pptx.shapes.DIAMOND, { x: 6.2, y: 1.7, w: 2.2, h: 1.2, fill: { color: 'FEF3C7' }, line: { color: 'F59E0B', width: 1 } });
slide20.addText('Quota >= 70%\nor 90%?', { x: 6.2, y: 1.7, w: 2.2, h: 1.2, align: 'center', color: 'B45309', fontSize: 10, bold: true, fontFace: 'Inter' });

// Arrow 3 -> 4 (DOWN - YES)
slide20.addShape(pptx.shapes.DOWN_ARROW, { x: 7.1, y: 3.0, w: 0.4, h: 0.4, fill: { color: 'EF4444' } });
slide20.addText('YES', { x: 7.6, y: 3.0, w: 0.4, h: 0.3, align: 'center', color: 'EF4444', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 4
slide20.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 3.6, w: 2.2, h: 1.0, fill: { color: 'FEE2E2' }, line: { color: 'FCA5A5', width: 1 } });
slide20.addText('Flag warning or\ncritical badge in UI', { x: 6.2, y: 3.6, w: 2.2, h: 1.0, align: 'center', color: '991B1B', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 3 -> 5 (RIGHT - NO)
slide20.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.5, y: 2.1, w: 0.4, h: 0.4, fill: { color: '10B981' } });
slide20.addText('NO', { x: 8.5, y: 1.7, w: 0.4, h: 0.3, align: 'center', color: '10B981', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 5
slide20.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 1.8, w: 2.2, h: 1.0, fill: { color: '10B981' } });
slide20.addText('Flag storage status\nas nominal (OK)', { x: 9.0, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 2 -> 6 (DOWN)
slide20.addShape(pptx.shapes.DOWN_ARROW, { x: 4.5, y: 2.9, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 6
slide20.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 3.5, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide20.addText('Find legacy backups\nin localStorage', { x: 3.4, y: 3.5, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 6 -> 7 (DOWN)
slide20.addShape(pptx.shapes.DOWN_ARROW, { x: 4.5, y: 4.6, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 7
slide20.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 5.1, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide20.addText('Write backup JSON\nto IndexedDB store', { x: 3.4, y: 5.1, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 7 -> 8 (RIGHT)
slide20.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 5.4, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 8
slide20.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 5.1, w: 2.2, h: 1.0, fill: { color: 'E0F2FE' }, line: { color: 'BAE6FD', width: 1 } });
slide20.addText('Delete old backups\nfrom localStorage', { x: 6.2, y: 5.1, w: 2.2, h: 1.0, align: 'center', color: '0369A1', fontSize: 11, bold: true, fontFace: 'Inter' });


// ----------------------------------------------------
// SLIDE 21: FLOWCHART: ExcelGrid Keyboard event flow
// ----------------------------------------------------
const slide21 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide21, 'FLOWCHART: EXCELGRID KEYDOWN EVENT FLOW');

// Node 1
slide21.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 2.5, w: 2.2, h: 1.0, fill: { color: '1E3A8A' } });
slide21.addText('Keystroke event\nfired in cell', { x: 0.6, y: 2.5, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 1 -> 2
slide21.addShape(pptx.shapes.RIGHT_ARROW, { x: 2.9, y: 2.8, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 2 (Decision)
slide21.addShape(pptx.shapes.DIAMOND, { x: 3.4, y: 2.4, w: 2.2, h: 1.2, fill: { color: 'FEF3C7' }, line: { color: 'F59E0B', width: 1 } });
slide21.addText('Cell in\nEditing mode?', { x: 3.4, y: 2.4, w: 2.2, h: 1.2, align: 'center', color: 'B45309', fontSize: 10, bold: true, fontFace: 'Inter' });

// Arrow 2 -> 3 (UP - YES)
slide21.addShape(pptx.shapes.UP_ARROW, { x: 4.3, y: 1.9, w: 0.4, h: 0.4, fill: { color: '10B981' } });
slide21.addText('YES', { x: 4.8, y: 1.9, w: 0.4, h: 0.3, align: 'center', color: '10B981', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 3
slide21.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 0.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide21.addText('Check keys: Enter,\nTab, or Escape', { x: 3.4, y: 0.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 3 -> 4 (RIGHT)
slide21.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 1.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 4
slide21.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 0.8, w: 2.2, h: 1.0, fill: { color: '10B981' } });
slide21.addText('Commit value &\nmove x/y selection', { x: 6.2, y: 0.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 2 -> 5 (DOWN - NO)
slide21.addShape(pptx.shapes.DOWN_ARROW, { x: 4.3, y: 3.7, w: 0.4, h: 0.4, fill: { color: 'EF4444' } });
slide21.addText('NO', { x: 4.8, y: 3.7, w: 0.4, h: 0.3, align: 'center', color: 'EF4444', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 5
slide21.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 4.2, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide21.addText('Check keys: Arrow\nkeys or Enter', { x: 3.4, y: 4.2, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 5 -> 6 (RIGHT)
slide21.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 4.5, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 6
slide21.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 4.2, w: 2.2, h: 1.0, fill: { color: 'E0F2FE' }, line: { color: 'BAE6FD', width: 1 } });
slide21.addText('Change coordinate\npointer or trigger edit', { x: 6.2, y: 4.2, w: 2.2, h: 1.0, align: 'center', color: '0369A1', fontSize: 11, bold: true, fontFace: 'Inter' });


// ----------------------------------------------------
// SLIDE 22: FLOWCHART: Monthly MIS Aggregation
// ----------------------------------------------------
const slide22 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide22, 'FLOWCHART: MONTHLY MIS DATA AGGREGATION');

// Node 1
slide22.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.8, w: 2.2, h: 1.0, fill: { color: '1E3A8A' } });
slide22.addText('User selects\nMonth and Year', { x: 0.6, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 1 -> 2
slide22.addShape(pptx.shapes.RIGHT_ARROW, { x: 2.9, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 2
slide22.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide22.addText('Fetch all sheet\nobjects from sheetDB', { x: 3.4, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 2 -> 3
slide22.addShape(pptx.shapes.RIGHT_ARROW, { x: 5.7, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 3
slide22.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide22.addText('Filter sheets starting\nwith cms_daily_opd', { x: 6.2, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 3 -> 4
slide22.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.5, y: 2.1, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 4
slide22.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 1.8, w: 2.2, h: 1.0, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 1 } });
slide22.addText('Loop row dates\n& extract month/year', { x: 9.0, y: 1.8, w: 2.2, h: 1.0, align: 'center', color: '0F172A', fontSize: 11, fontFace: 'Inter' });

// Arrow 4 -> 5 (DOWN)
slide22.addShape(pptx.shapes.DOWN_ARROW, { x: 9.9, y: 2.9, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 5 (Decision)
slide22.addShape(pptx.shapes.DIAMOND, { x: 9.0, y: 3.5, w: 2.2, h: 1.2, fill: { color: 'FEF3C7' }, line: { color: 'F59E0B', width: 1 } });
slide22.addText('Date matches\nMonth/Year?', { x: 9.0, y: 3.5, w: 2.2, h: 1.2, align: 'center', color: 'B45309', fontSize: 10, bold: true, fontFace: 'Inter' });

// Arrow 5 -> 6 (LEFT - YES)
slide22.addShape(pptx.shapes.LEFT_ARROW, { x: 8.5, y: 3.9, w: 0.4, h: 0.4, fill: { color: '10B981' } });
slide22.addText('YES', { x: 8.5, y: 3.5, w: 0.4, h: 0.3, align: 'center', color: '10B981', fontSize: 10, bold: true, fontFace: 'Inter' });

// Node 6
slide22.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.2, y: 3.6, w: 2.2, h: 1.0, fill: { color: 'E0F2FE' }, line: { color: 'BAE6FD', width: 1 } });
slide22.addText('Increment count and\ncheck referral diagnoses', { x: 6.2, y: 3.6, w: 2.2, h: 1.0, align: 'center', color: '0369A1', fontSize: 11, bold: true, fontFace: 'Inter' });

// Arrow 6 -> 7 (LEFT)
slide22.addShape(pptx.shapes.LEFT_ARROW, { x: 5.7, y: 3.9, w: 0.4, h: 0.4, fill: { color: '3B82F6' } });

// Node 7
slide22.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3.4, y: 3.6, w: 2.2, h: 1.0, fill: { color: '10B981' } });
slide22.addText('Set MIS states and\nupdate charts/tables', { x: 3.4, y: 3.6, w: 2.2, h: 1.0, align: 'center', color: 'FFFFFF', fontSize: 11, bold: true, fontFace: 'Inter' });


// ----------------------------------------------------
// SLIDE 10: Conclusion & Recommendations
// ----------------------------------------------------
const slide10 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
addSlideHeader(slide10, 'RECOMMENDATIONS & FUTURE SCOPE');

// Left Column - Achievements
slide10.addText('Key Achievements:\n' +
  '• Successfully digitized 100% of paper clinical logs\n' +
  '• Replaced unstable storage caches with IndexedDB connection pool\n' +
  '• Virtualized DOM renders to handle 10,000+ data rows\n' +
  '• Replaced absolute asset paths with print-safe inline SVGs\n' +
  '• Resolved EPERM lock build errors in packaged EXE installers\n' +
  '• Completed clean-installation validation checks', {
  x: 0.6,
  y: 1.5,
  w: 5.8,
  h: 4.8,
  fontSize: 14,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 22
});

// Right Column - Future Recommendations
slide10.addText('Recommended Extensions:\n' +
  '• USB Barcode Scanners: Support barcode reader triggers in the dispense queue to speed up drug verification checks.\n\n' +
  '• OCR Prescription Scanner: Integrate camera scanner module to extract text details from printed prescription slips.\n\n' +
  '• Encrypted Cloud Sync: Establish optional background sync threads to upload encrypted clinical logs when network is active.', {
  x: 6.8,
  y: 1.5,
  w: 5.8,
  h: 4.8,
  fontSize: 13,
  color: COLOR_TEXT_DARK,
  fontFace: 'Inter',
  lineSpacing: 18
});


// Save presentation file
const pptxPath = path.join(__dirname, 'JSPulse_OHMS_Final_Comprehensive_Internship_Report.pptx');
pptx.writeFile({ fileName: pptxPath }).then(() => {
  console.log(`Success! PPTX presentation generated successfully at:\n${pptxPath}`);
  process.exit(0);
}).catch(err => {
  console.error("PPTX generation script failed: ", err);
  process.exit(1);
});
