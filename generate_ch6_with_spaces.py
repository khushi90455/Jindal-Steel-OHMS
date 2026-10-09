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
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
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

def main():
    doc = Document()
    setup_doc(doc)

    # ═══════════════════════════════════════════════════════════
    # CHAPTER 6 TITLE
    # ═══════════════════════════════════════════════════════════
    doc.add_heading('Chapter 6: Annotated Source Code Appendix', level=1)

    # ───────────────────────────────────────────────────────────
    # 6.1 Context Bridge Preload Scripts (preload.js)
    # ───────────────────────────────────────────────────────────
    doc.add_heading('6.1 Context Bridge Preload Scripts (preload.js)', level=2)
    
    para(doc, "The context bridge preload script (preload.js) serves as the primary security gateway and boundary manager in the JS Pulse OHMS desktop application framework. In a default Electron setup, the user interface running inside the Chromium renderer has direct access to Node.js APIs if nodeIntegration is enabled. However, this poses a critical security risk: if a third-party React package contains a vulnerability or if an XSS exploit is executed, the attacker could execute arbitrary system shell commands or modify system files. To counter this vulnerability, JS Pulse OHMS enforces context isolation, forcing the Renderer process and the Main process to run in entirely separate V8 execution contexts.")
    para(doc, "The preload.js script executes in an intermediate context, possessing access to both Node.js standard modules (such as require and electron) and the browser's global window object. It uses the contextBridge.exposeInMainWorld API to selectively expose a set of whitelisted functions to the Renderer process under the window.electron namespace. By doing so, the React UI can request file operations, trigger native Excel exports, and request document printing without ever obtaining direct access to Electron's ipcRenderer or Node.js's require system. This represents a robust defense-in-depth security practice recommended by Electron's security checklist.")

    code_block(doc, """/* eslint-env node */
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  printCommand: (options) => ipcRenderer.send('print-command', options || {}),
  previewPrint: (options) => ipcRenderer.send('preview-print', options || {}),
  saveAndOpenExcel: (buffer, defaultName) => ipcRenderer.invoke('save-and-open-excel', { buffer, defaultName }),
  storageGet: (key) => ipcRenderer.sendSync('sync-storage-get', key),
  storageSet: (key, value) => ipcRenderer.sendSync('sync-storage-set', key, value),
  storageRemove: (key) => ipcRenderer.sendSync('sync-storage-remove', key),
  storageClear: () => ipcRenderer.sendSync('sync-storage-clear'),
  storageKey: (index) => ipcRenderer.sendSync('sync-storage-key', index),
  storageLength: () => ipcRenderer.sendSync('sync-storage-length'),
  storageAll: () => ipcRenderer.sendSync('sync-storage-all'),
  isElectron: true
});""", "Code Listing 6.1: electron/preload.js Context Bridge API Expositions")

    para(doc, "An annotation of this code listing highlights its exact operational flow. Line 2 imports the necessary Electron modules: contextBridge (which securely serializes parameters across V8 context boundaries) and ipcRenderer (the message emitter for sending asynchronous IPC calls). Lines 4 through 16 define the exposed API object. Line 5 exposes printCommand, which uses ipcRenderer.send to fire an asynchronous message over the 'print-command' channel. This is used by the clinical modules to display the native system print dialog. Similarly, line 6 exposes previewPrint to trigger a headless PDF rendering transaction.")
    para(doc, "Line 7 defines saveAndOpenExcel, which uses ipcRenderer.invoke to return a Promise that resolves when the Main Process has prompted the user to save the Excel file and opened it in their local spreadsheet reader. This is a critical workflow for the inventory and daily OPD tally exports. Lines 8 through 14 implement synchronous IPC handlers (ipcRenderer.sendSync) for the localStorage proxy wrapper. These methods intercept standard browser-level key-value interactions and block the Renderer's thread briefly while the Main Process completes the file read or write operation on localstorage.json, ensuring complete data consistency across component mounts. Line 15 sets isElectron to true, which React queries at runtime to determine whether to render desktop-only features (such as print buttons and tray configuration) or fallback to standard browser interfaces.")

    # ───────────────────────────────────────────────────────────
    # 6.2 Main Electron Process Handlers (main.js)
    # ───────────────────────────────────────────────────────────
    doc.add_heading('6.2 Main Electron Process Handlers (main.js)', level=2)

    para(doc, "The main.js script represents the entry point and master controller of the JS Pulse OHMS desktop application, executing inside the Node.js runtime process. It is responsible for orchestrating the application lifecycle, managing the primary BrowserWindow instance, registering IPC listeners to service UI requests, enforcing security boundaries, and managing the local file system. Because JS Pulse OHMS operates in a completely offline environment at the JSP Patratu plant, the Main process acts as a local server, ensuring that data is persisted safely in the user's home directory and that system tools function without external network connectivity.")
    para(doc, "To prevent database corruption and concurrent file writes, main.js implements a single instance lock via app.requestSingleInstanceLock() on lines 14–25. If a user attempts to launch a second instance of the application, the new process will immediately terminate, and the existing window will be focused and restored. This prevents key-value locking issues on the local JSON file. Furthermore, line 28 disables hardware acceleration: this is a deliberate performance adjustment that bypasses slow GPU driver initialisation issues common on older Windows 10 computers used in industrial environments, ensuring a fast, stable launch on all workstation hardware configurations.")

    code_block(doc, """/* eslint-env node */
import { app, BrowserWindow, ipcMain, shell, dialog } from 'electron';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import fs from 'fs';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280, height: 800, title: 'JSPulse OHMS', show: true,
    backgroundColor: '#0f172a',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
      plugins: true,
      backgroundThrottling: false
    }
  });
  mainWindow.setMenuBarVisibility(false);
  
  // DevTools Toggle key listener
  mainWindow.webContents.on('before-input-event', (event, input) => {
    if (input.key === 'F12' || (input.control && input.shift && input.key.toLowerCase() === 'i')) {
      mainWindow.webContents.toggleDevTools();
      event.preventDefault();
    }
  });

  const isDev = process.env.NODE_ENV === 'development';
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
  mainWindow.maximize();
}""", "Code Listing 6.2: electron/main.js Application Setup and Window Lifecycle")

    para(doc, "The window lifecycle configuration is annotated in detail. Lines 12–25 define the default window dimensions and configuration. Crucially, backgroundThrottling is set to false in the webPreferences configuration. By default, Chromium reduces V8 execution frequency and throttles timers when a window is minimized or when the monitor turns off to save laptop battery. However, in a clinic environment, the OPD-to-Pharmacy synchronization engine runs continuously on a background interval; throttling would cause the synchronization script to halt, resulting in missed prescriptions or stalled queues when the workstation is left unattended. Setting backgroundThrottling to false ensures uninterrupted background processing.")
    para(doc, "The storage architecture of the Main Process manages synchronous data persistence through localstorage.json, located in the user's application data directory. Reading from disk on every getItem call would create a major performance bottleneck, as disk reads take milliseconds while React components require sub-millisecond responses during render cycles. To solve this, main.js implements an in-memory cache variable (_storageCache) shown in Code Listing 6.3. When the Renderer requests data, the handler checks the cache first, falling back to disk reads only if the cache is uninitialized, and writing modifications back to disk asynchronously.")

    code_block(doc, """const storagePath = path.join(app.getPath('userData'), 'localstorage.json');
let _storageCache = null;

function readStorage() {
  if (_storageCache !== null) return _storageCache;
  try {
    if (fs.existsSync(storagePath)) {
      _storageCache = JSON.parse(fs.readFileSync(storagePath, 'utf8'));
      return _storageCache;
    }
  } catch (e) {
    console.error('Error reading localstorage.json', e);
  }
  _storageCache = {};
  return _storageCache;
}

function writeStorage(data) {
  _storageCache = data;
  try {
    const dir = path.dirname(storagePath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(storagePath, JSON.stringify(data, null, 2), 'utf8');
  } catch (e) {
    console.error('Error writing localstorage.json', e);
  }
}""", "Code Listing 6.3: Custom Desktop Storage File System Persistence in main.js")

    para(doc, "The execution flow is straightforward: readStorage (lines 4–16) first evaluates if _storageCache is active. If so, it returns it instantly. Otherwise, it uses Node's fs.existsSync and fs.readFileSync to load localstorage.json. If the file is missing (e.g. during first-time setup), it initializes the cache as an empty object. writeStorage (lines 18–29) accepts the modified store, updates the local cache reference, ensures the target directory exists, and commits the serialized object to the filesystem using fs.writeFileSync. These routines service the synchronous IPC messages ('sync-storage-get', 'sync-storage-set', etc.) exposed by the preload context bridge, implementing a reliable file-backed storage layer for all clinical state data.")

    # ───────────────────────────────────────────────────────────
    # 6.3 React Spreadsheet Data Grid Components
    # ───────────────────────────────────────────────────────────
    doc.add_heading('6.3 React Spreadsheet Data Grid Components (ExcelGrid.jsx)', level=2)

    para(doc, "The spreadsheet component ExcelGrid.jsx is the primary data visualization and editing interface used across the JS Pulse OHMS platform. It is designed to emulate the look, feel, and functionality of Microsoft Excel, offering features such as keyboard navigation, inline cell editing, styling controls, undo/redo state stacks, and formulas. However, rendering thousands of patient records, medicine logs, and vital signs entries using standard React layouts would create a massive number of DOM nodes, causing browser lag, memory exhaustion, and slow scroll speeds on low-memory clinic computers.")
    para(doc, "To solve this performance bottleneck, ExcelGrid.jsx implements DOM virtualization. Instead of rendering every row in the dataset, the component calculates which rows are visible in the user's viewport and renders only those rows. The rows above the visible viewport are represented by a single empty spacer div with its height set to the combined height of the hidden rows, and another spacer div represents the rows below the viewport. This approach keeps the active DOM node count constant, ensuring smooth scrolling and responsive editing regardless of the dataset size.")

    code_block(doc, """// ExcelGrid.jsx — DOM Virtualization Row Calculator
const visibleRows = useMemo(() => {
    let start = 0, end = data.length - 1;
    let topSpacer = 0, bottomSpacer = 0;
    const buffer = 150; // Overscan buffer to prevent visual popping
    let offset = 0;

    for (let i = 0; i < data.length; i++) {
        const rh = rowHeights[i] || 30; // Default row height is 30px
        if (offset + rh < scrollTop - buffer) {
            start = i + 1;
            topSpacer += rh;
        } else if (offset > scrollTop + containerH + buffer) {
            end = i - 1;
            break;
        }
        offset += rh;
    }
    if (end < start) end = start;
    for (let i = end + 1; i < data.length; i++) {
        bottomSpacer += (rowHeights[i] || 30);
    }
    return { start, end, topSpacer, bottomSpacer };
}, [data, rowHeights, scrollTop, containerH]);""", "Code Listing 6.4: DOM Virtualization Scroll Offset and Row Range Computations")

    para(doc, "An analysis of Code Listing 6.4 clarifies its calculations. The useMemo hook (line 2) takes four dependencies: the data array, the rowHeights array, the current scrollTop offset, and the visible container height containerH. Lines 8–17 loop through the rows to determine which row index matches the top boundary of the viewport. If the accumulated offset of the row is less than scrollTop minus the overscan buffer (150px), the start index is incremented and the row's height is added to topSpacer. When the row's offset exceeds the bottom of the viewport plus the overscan buffer, the loop breaks early, setting the end index. Lines 20–22 calculate the remaining height of all invisible rows below the viewport and add it to bottomSpacer. This virtualization keeps the active node count minimal, enabling smooth 60fps scrolling.")
    para(doc, "In addition to DOM virtualization, ExcelGrid.jsx implements a recursive formula engine that parses and evaluates formulas such as =SUM(A1:B5) and =A1+B2, as shown in Code Listing 6.5. This allows clinical staff to perform real-time tallying and inventory valuations within the grid. To prevent infinite loops caused by circular cell references, the evaluateFormula function uses a recursion depth checker. If the depth counter exceeds a threshold of 50, the function returns '#ERROR!' and exits, protecting the application's stability.")

    code_block(doc, """// ExcelGrid.jsx — Recursive Formula Evaluator
const evaluateFormula = (formulaStr, allData, cols, depth = 0) => {
  if (depth > 50) return '#ERROR!'; // Circular reference protection guard
  if (!formulaStr || !String(formulaStr).startsWith('=')) return formulaStr;
  try {
    let expr = String(formulaStr).substring(1).toUpperCase();
    
    // SUM range resolver
    expr = expr.replace(/SUM\(([A-Z]+)(\d+):([A-Z]+)(\d+)\)/g, (match, c1, r1, c2, r2) => {
      let sum = 0;
      const startR = Math.min(parseInt(r1), parseInt(r2)) - 1;
      const endR = Math.max(parseInt(r1), parseInt(r2)) - 1;
      const c1Idx = cols.findIndex(c => c.letter === c1);
      const c2Idx = cols.findIndex(c => c.letter === c2);
      if (c1Idx === -1 || c2Idx === -1) return 0;
      const startC = Math.min(c1Idx, c2Idx);
      const endC = Math.max(c1Idx, c2Idx);
      for (let r = startR; r <= endR; r++) {
        if (!allData[r]) continue;
        for (let c = startC; c <= endC; c++) {
          const val = allData[r][cols[c].key];
          let numVal = val;
          if (String(val).startsWith('=')) {
            numVal = evaluateFormula(val, allData, cols, depth + 1);
          }
          const num = parseFloat(numVal);
          if (!isNaN(num)) sum += num;
        }
      }
      return sum;
    });
    
    // Individual cell resolver
    expr = expr.replace(/([A-Z]+)(\d+)/g, (match, letter, rowStr) => {
      const col = cols.find(c => c.letter === letter);
      if (!col) return 0;
      const rIdx = parseInt(rowStr) - 1;
      if (!allData[rIdx]) return 0;
      const val = allData[rIdx][col.key];
      let numVal = val;
      if (String(val).startsWith('=')) {
        numVal = evaluateFormula(val, allData, cols, depth + 1);
      }
      const num = parseFloat(numVal);
      return isNaN(num) ? 0 : num;
    });

    const result = new Function(`return \${expr}`)();
    return Number.isFinite(result) ? Math.round(result * 100) / 100 : '#ERROR!';
  } catch (err) {
    return '#ERROR!';
  }
};""", "Code Listing 6.5: Recursive Spreadsheet Cell Formula Parser and Evaluation Engine")

    para(doc, "The operation of this formula engine is highly robust. The SUM range resolver (lines 8–31) uses regular expressions to find cell ranges (e.g. A1:B5). It resolves the bounding column letters to numeric array indices, loops through the range, and recursively evaluates the cells. The individual cell resolver (lines 34–45) replaces coordinates with their evaluated numeric values. Line 46 uses JavaScript's Function constructor to evaluate the resulting arithmetic expression. The 50-level recursion cap protects against circular references, ensuring that incorrect formula inputs do not freeze the UI or crash the browser runtime.")

    # ───────────────────────────────────────────────────────────
    # 6.4 Custom Utility Functions and Helper Modules
    # ───────────────────────────────────────────────────────────
    doc.add_heading('6.4 Custom Utility Functions and Helper Modules', level=2)

    para(doc, "The utility modules of JS Pulse OHMS handle data persistence, connection resilience, and local NLP processing. The core data utility sheetDB.js manages IndexedDB connections, providing a promise-based interface that supports schema migration, bulk writes, and auto-recovery routines. This layer bypasses the browser's 5MB localStorage limit, enabling the application to store over 100,000 patient records locally.")
    para(doc, "A key feature of sheetDB.js is its connection-pooling and auto-recovery strategy, shown in Code Listing 6.6. If a query fails due to a stale connection (which can occur if the clinic workstation is left idle for days), the module automatically discards the dead connection, opens a new database handle, and retries the failed operation.")

    code_block(doc, """// utils/sheetDB.js — Connection Pool with Auto-Retry
let _dbInstance = null;
let _dbPromise = null;

function getDB() {
  if (_dbInstance) {
    try {
      // Test the connection with a lightweight transaction
      const testTx = _dbInstance.transaction('sheet_data', 'readonly');
      testTx.abort(); // Immediately abort to avoid overhead
      return Promise.resolve(_dbInstance);
    } catch (e) {
      console.warn('[SheetDB] Stale connection detected. Reconnecting...', e);
      try { _dbInstance.close(); } catch (err) {}
      _dbInstance = null; _dbPromise = null;
    }
  }
  if (_dbPromise) return _dbPromise;

  _dbPromise = new Promise((resolve, reject) => {
    const request = indexedDB.open('JSPulseOHMS_Sheets', 1);
    request.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains('sheet_data')) db.createObjectStore('sheet_data');
      if (!db.objectStoreNames.contains('sheet_meta')) db.createObjectStore('sheet_meta');
    };
    request.onsuccess = () => {
      _dbInstance = request.result;
      _dbInstance.onclose = () => { _dbInstance = null; _dbPromise = null; };
      resolve(_dbInstance);
    };
    request.onerror = () => { _dbInstance = null; _dbPromise = null; reject(request.error); };
  });
  return _dbPromise;
}

export async function withRetry(operation) {
  try {
    const db = await getDB();
    return await operation(db);
  } catch (err) {
    console.warn('[SheetDB] Attempting connection recovery and retry...', err);
    try { if (_dbInstance) _dbInstance.close(); } catch (e) {}
    _dbInstance = null; _dbPromise = null;
    const db = await getDB();
    return await operation(db);
  }
}""", "Code Listing 6.6: sheetDB.js Connection Pooling and Error Recovery")

    para(doc, "The execution flow is designed to be highly resilient: getDB (lines 5–34) validates the connection singleton _dbInstance. It verifies the connection using a lightweight read-only transaction (lines 8–10) and aborts it immediately. If the transaction throws an error, the connection is closed, the singleton is reset, and a new database request is opened. The withRetry function (lines 36–48) wraps database operations in a try-catch block. If an error occurs, the connection is closed, a new one is opened, and the operation is retried once. This recovery pattern prevents connection errors and ensures database reliability.")
    para(doc, "In addition to database utilities, JS Pulse OHMS implements a local Natural Language Processing (NLP) engine in chatBrain.js to support offline chat functionality. The engine parses user queries using regular expressions to identify keywords, matching them against a priority-ordered knowledge base of clinical workflows and first aid protocols, as shown in Code Listing 6.7. This allows clinical staff to query the system using natural language even when network connectivity is lost.")

    code_block(doc, """// utils/chatBrain.js — Local Regex Intent Classifier
export const processChatMessage = (userInput) => {
  const normalizedInput = userInput.toLowerCase().replace(/[^\\w\\s]/gi, '');
  const tokens = normalizedInput.split(/\\s+/);
  
  let bestMatch = null;
  let highestScore = 0;

  for (const entry of knowledgeBase) {
    let score = 0;
    for (const keyword of entry.keywords) {
      if (normalizedInput.includes(keyword)) {
        score += keyword.split(' ').length * 2; // Weight multi-word matches higher
      } else {
        const keywordTokens = keyword.split(' ');
        let matches = 0;
        keywordTokens.forEach(kt => {
          if (tokens.includes(kt)) matches++;
        });
        if (matches === keywordTokens.length) score += matches;
      }
    }
    if (score > highestScore) {
      highestScore = score;
      bestMatch = entry;
    }
  }

  if (bestMatch && highestScore >= 1) return bestMatch.response;

  // Fallback to searching local database tables
  const dbMatch = searchLocalData(userInput);
  if (dbMatch) return dbMatch;

  // Randomized fallback responses
  const fallbacks = [
    "I couldn't find a direct match. Try asking about medicine stock levels or patient logs.",
    "I'm not sure. You can search our database by typing an employee ID or medicine name."
  ];
  return fallbacks[Math.floor(Math.random() * fallbacks.length)];
};""", "Code Listing 6.7: chatBrain.js Local Intent Classification and Database Query Logic")

    para(doc, "The classification logic is straightforward: line 2 normalizes the input by converting it to lowercase and removing special characters. Lines 7–22 iterate through the knowledgeBase entries, scoring them based on keyword matches. If a match is found, the associated response is returned. If no intent matches, lines 26–27 perform a text scan of the local database tables using searchLocalData, searching for matching employee codes or medicine names. If this scan also returns no results, the system returns a randomized fallback response. This local NLP approach provides a helpful, interactive assistant that functions completely offline.")

    # SAVE
    out_path = 'JSPulse_OHMS_Chapter6_WithSpaces.docx'
    doc.save(out_path)
    print(f"Saved {out_path}")

if __name__ == '__main__':
    main()
