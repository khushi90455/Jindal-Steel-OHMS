import { app, BrowserWindow, ipcMain } from 'electron';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const diagrams = [
  // we will inject diagrams here
];

const htmlTemplate = `<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
  </script>
  <style>
    body { background: white; margin: 0; padding: 20px; display: inline-block; }
    .mermaid { display: inline-block; }
  </style>
</head>
<body>
  <div class="mermaid" id="diagram"></div>
  <script>
    const { ipcRenderer } = require('electron');
    // Not possible to use require if contextIsolation is true, but we can set it to false for this temp script.
  </script>
</body>
</html>`;

app.whenReady().then(async () => {
    // Read diagrams from diagrams.json
    let diagramList = [];
    try {
        diagramList = JSON.parse(fs.readFileSync('diagrams.json', 'utf8'));
    } catch (e) {
        console.error("diagrams.json not found", e);
        app.quit();
        return;
    }
    
    if (!fs.existsSync('diagram_images')) {
        fs.mkdirSync('diagram_images');
    }

    const win = new BrowserWindow({
      show: false,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
      }
    });

    for (let i = 0; i < diagramList.length; i++) {
        const diagramCode = diagramList[i];
        
        const pageHtml = `<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
  </script>
  <style>
    body { background: white; margin: 0; padding: 20px; display: inline-block; overflow: hidden; }
    .mermaid { display: inline-block; }
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
        const rect = el.getBoundingClientRect();
        ipcRenderer.send('diagram-ready', { width: rect.width, height: rect.height });
    }, 2000);
  </script>
</body>
</html>`;
        
        fs.writeFileSync('temp_diagram.html', pageHtml);
        
        await new Promise((resolve) => {
            ipcMain.once('diagram-ready', async (event, rect) => {
                const w = Math.ceil(rect.width) + 40;
                const h = Math.ceil(rect.height) + 40;
                win.setSize(w, h);
                const image = await win.webContents.capturePage({ x: 0, y: 0, width: w, height: h });
                fs.writeFileSync(`diagram_images/diagram_${i}.png`, image.toPNG());
                console.log(`Saved diagram_${i}.png`);
                resolve();
            });
            win.loadFile('temp_diagram.html');
        });
    }
    
    console.log("All diagrams rendered.");
    app.quit();
});
