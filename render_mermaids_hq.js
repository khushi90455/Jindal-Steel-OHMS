import { app, BrowserWindow, ipcMain } from 'electron';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// High-DPI scale factor: 2x produces ~192 DPI from a 96 DPI screen.
// Combined with larger base font sizes, this yields print-quality output.
const SCALE_FACTOR = 2;

app.whenReady().then(async () => {
    let diagramList = [];
    try {
        diagramList = JSON.parse(fs.readFileSync('diagrams.json', 'utf8'));
    } catch (e) {
        console.error("diagrams.json not found", e);
        app.quit();
        return;
    }
    
    if (!fs.existsSync('diagram_images_hq')) {
        fs.mkdirSync('diagram_images_hq');
    }

    const win = new BrowserWindow({
      show: false,
      width: 1600,
      height: 1200,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        zoomFactor: SCALE_FACTOR
      }
    });

    for (let i = 0; i < diagramList.length; i++) {
        const diagramCode = diagramList[i];
        
        // Build HTML with large, readable fonts for print
        const pageHtml = `<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"><\/script>
  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      themeVariables: {
        fontSize: '18px',
        fontFamily: 'Arial, Helvetica, sans-serif'
      },
      flowchart: {
        nodeSpacing: 30,
        rankSpacing: 40,
        diagramPadding: 20,
        htmlLabels: true,
        curve: 'basis',
        useMaxWidth: false
      },
      sequence: {
        diagramMarginX: 30,
        diagramMarginY: 20,
        actorMargin: 80,
        width: 200,
        height: 50,
        boxMargin: 10,
        boxTextMargin: 8,
        noteMargin: 15,
        messageMargin: 40,
        messageFontSize: 16,
        actorFontSize: 18,
        noteFontSize: 14,
        useMaxWidth: false
      },
      state: {
        useMaxWidth: false
      }
    });
  <\/script>
  <style>
    * { box-sizing: border-box; }
    body {
      background: white;
      margin: 0;
      padding: 40px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }
    .mermaid {
      display: inline-block;
      font-size: 18px !important;
    }
    .mermaid text {
      font-size: 16px !important;
    }
    .mermaid .nodeLabel {
      font-size: 16px !important;
      padding: 8px !important;
    }
    .mermaid .edgeLabel {
      font-size: 14px !important;
    }
    .mermaid .actor {
      font-size: 16px !important;
    }
    .mermaid .messageText {
      font-size: 15px !important;
    }
    .mermaid .noteText {
      font-size: 14px !important;
    }
    .mermaid .label {
      font-size: 16px !important;
    }
    .mermaid .statediagram-state .state-title {
      font-size: 16px !important;
    }
  </style>
</head>
<body>
  <div class="mermaid" id="diagram">
${diagramCode}
  </div>
  <script>
    const { ipcRenderer } = require('electron');
    setTimeout(() => {
        const el = document.getElementById('diagram');
        const svg = el.querySelector('svg');
        let w, h;
        if (svg) {
            const bbox = svg.getBBox();
            w = Math.ceil(bbox.width) + 100;
            h = Math.ceil(bbox.height) + 100;
        } else {
            const rect = el.getBoundingClientRect();
            w = Math.ceil(rect.width) + 100;
            h = Math.ceil(rect.height) + 100;
        }
        ipcRenderer.send('diagram-ready', { width: w, height: h });
    }, 3000);
  <\/script>
</body>
</html>`;
        
        fs.writeFileSync('temp_diagram.html', pageHtml);
        
        await new Promise((resolve) => {
            ipcMain.once('diagram-ready', async (event, rect) => {
                // Scale dimensions by our factor for high-DPI capture
                const logicalW = Math.min(Math.ceil(rect.width) + 80, 1800);
                const logicalH = Math.min(Math.ceil(rect.height) + 80, 2400);
                win.setSize(logicalW, logicalH);
                
                // Small delay for resize to settle
                await new Promise(r => setTimeout(r, 500));
                
                const image = await win.webContents.capturePage({
                    x: 0,
                    y: 0,
                    width: logicalW,
                    height: logicalH
                });
                
                fs.writeFileSync(`diagram_images_hq/diagram_${i}.png`, image.toPNG());
                console.log(`Saved HQ diagram_${i}.png (${logicalW}x${logicalH} logical, ${SCALE_FACTOR}x scale)`);
                resolve();
            });
            win.loadFile('temp_diagram.html');
        });
    }
    
    console.log("All high-quality diagrams rendered.");
    app.quit();
});
