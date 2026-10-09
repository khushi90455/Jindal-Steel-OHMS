import { app, BrowserWindow } from 'electron';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Helper to escape characters and format inline md tags
function parseInline(text) {
  let formatted = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Bold formatting **text**
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // Italic formatting *text*
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  // Inline code `code`
  formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
  
  // Links [text](url)
  formatted = formatted.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
  
  return formatted;
}

// Custom Markdown to HTML parser
function mdToHtml(md) {
  const lines = md.split('\n');
  let html = '';
  let inList = false;
  let inCode = false;
  let codeLang = '';
  let inTable = false;
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    
    // Code block check
    if (line.trim().startsWith('```')) {
      if (inCode) {
        if (codeLang === 'mermaid') {
          html += '</div>\n';
        } else {
          html += '</code></pre>\n';
        }
        inCode = false;
      } else {
        codeLang = line.trim().substring(3).toLowerCase().trim();
        if (codeLang === 'mermaid') {
          html += '<div class="mermaid">\n';
        } else {
          html += `<pre><code class="language-${codeLang}">`;
        }
        inCode = true;
      }
      continue;
    }
    
    if (inCode) {
      if (codeLang === 'mermaid') {
        html += line + '\n';
      } else {
        html += line
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;') + '\n';
      }
      continue;
    }

    // Page break / horizontal rules
    if (line.trim() === '---') {
      if (inList) { html += '</ul>\n'; inList = false; }
      if (inTable) { html += '</tbody></table>\n'; inTable = false; }
      html += '<hr class="section-divider">\n';
      continue;
    }

    // Headers
    if (line.startsWith('# ')) {
      if (inList) { html += '</ul>\n'; inList = false; }
      if (inTable) { html += '</tbody></table>\n'; inTable = false; }
      
      const titleText = line.substring(2);
      if (titleText.includes('Technical Architecture')) {
        // Render Cover Page block
        html += `
        <div class="cover-container">
          <div class="orange-bar"></div>
          <div class="logo-header">JINDAL STEEL</div>
          <h1 class="cover-title">JSPulse OHMS<br>Technical Architecture &amp; Algorithm Flows</h1>
          <h3 class="cover-subtitle">A Deep-Dive into the Core Logic, Automation Pipelines, and Codebase Architecture</h3>
          <div class="cover-divider"></div>
          <div class="cover-details">
            <p><strong>Developed By:</strong> Ashwini Kumar</p>
            <p><strong>Intern ID:</strong> JSPL-2026-IT-042</p>
            <p><strong>Department:</strong> Information Technology &amp; Occupational Health Services Group</p>
            <p><strong>Host Organization:</strong> Jindal Steel</p>
          </div>
          <div class="green-bar"></div>
        </div>
        <div class="page-break"></div>
        `;
      } else {
        html += `<h1>${parseInline(titleText)}</h1>\n`;
      }
      continue;
    }
    
    if (line.startsWith('## ')) {
      if (inList) { html += '</ul>\n'; inList = false; }
      if (inTable) { html += '</tbody></table>\n'; inTable = false; }
      html += `<h2>${parseInline(line.substring(3))}</h2>\n`;
      continue;
    }
    
    if (line.startsWith('### ')) {
      if (inList) { html += '</ul>\n'; inList = false; }
      if (inTable) { html += '</tbody></table>\n'; inTable = false; }
      html += `<h3>${parseInline(line.substring(4))}</h3>\n`;
      continue;
    }
    
    if (line.startsWith('#### ')) {
      if (inList) { html += '</ul>\n'; inList = false; }
      if (inTable) { html += '</tbody></table>\n'; inTable = false; }
      html += `<h4>${parseInline(line.substring(5))}</h4>\n`;
      continue;
    }

    // Tables
    if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
      if (inList) { html += '</ul>\n'; inList = false; }
      const parts = line.split('|').map(p => p.trim()).filter((p, idx, arr) => idx > 0 && idx < arr.length - 1);
      
      if (line.includes('---')) {
        continue;
      }
      
      if (!inTable) {
        inTable = true;
        html += '<table class="report-table">\n<thead>\n<tr>\n';
        parts.forEach(p => {
          html += `<th>${parseInline(p)}</th>\n`;
        });
        html += '</tr>\n</thead>\n<tbody>\n';
      } else {
        html += '<tr>\n';
        parts.forEach(p => {
          html += `<td>${parseInline(p)}</td>\n`;
        });
        html += '</tr>\n';
      }
      continue;
    } else {
      if (inTable) {
        html += '</tbody></table>\n';
        inTable = false;
      }
    }

    // Bullet Lists
    if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
      if (!inList) {
        inList = true;
        html += '<ul>\n';
      }
      let content = line.trim().substring(2);
      html += `<li>${parseInline(content)}</li>\n`;
      continue;
    } else {
      if (inList && (line.startsWith('  - ') || line.startsWith('  * '))) {
        let content = line.trim().substring(4);
        html += `<li class="nested-li">${parseInline(content)}</li>\n`;
        continue;
      }
      if (inList && line.trim() === '') {
        html += '</ul>\n';
        inList = false;
      }
    }

    // Empty lines
    if (line.trim() === '') {
      continue;
    }

    // Paragraph
    html += `<p>${parseInline(line)}</p>\n`;
  }
  
  if (inList) html += '</ul>\n';
  if (inTable) html += '</tbody></table>\n';
  
  return html;
}

// Main Electron execution logic
app.whenReady().then(async () => {
  try {
    const mdPath = path.join(__dirname, 'JSPulse_OHMS_Technical_Architecture_Flows.md');
    const pdfPath = path.join(__dirname, 'JSPulse_OHMS_Technical_Architecture_Flows.pdf');
    
    if (!fs.existsSync(mdPath)) {
      console.error(`Error: Source Markdown report not found at ${mdPath}`);
      app.quit();
      return;
    }

    const mdContent = fs.readFileSync(mdPath, 'utf8');
    const parsedHtmlContent = mdToHtml(mdContent);

    // HTML Wrapper with premium print styling
    const fullHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Jindal Steel JSPulse OHMS Architecture</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      securityLevel: 'loose',
      flowchart: { useMaxWidth: false, htmlLabels: true }
    });
  </script>
  <style>
    * {
      box-sizing: border-box;
    }
    body {
      font-family: 'Inter', sans-serif;
      color: #0f172a;
      line-height: 1.7;
      font-size: 14.5px;
      margin: 0;
      padding: 0;
      background: white;
    }
    
    /* Cover Page Premium Layout */
    .cover-container {
      height: 95vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 40px;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      margin: 20px;
    }
    .orange-bar {
      width: 120px;
      height: 6px;
      background: #f97316;
      border-radius: 3px;
    }
    .green-bar {
      width: 120px;
      height: 6px;
      background: #22c55e;
      border-radius: 3px;
    }
    .logo-header {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 20px;
      letter-spacing: 2px;
      color: #1e3a8a;
      margin-top: 20px;
    }
    .cover-title {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 32px;
      color: #0f172a;
      line-height: 1.3;
      margin: 40px 0 20px;
    }
    .cover-subtitle {
      font-family: 'Inter', sans-serif;
      font-weight: 400;
      font-size: 16px;
      color: #475569;
      max-width: 650px;
      line-height: 1.5;
      margin-bottom: 40px;
    }
    .cover-divider {
      width: 100%;
      height: 1px;
      background: #e2e8f0;
    }
    .cover-details {
      text-align: left;
      width: 100%;
      max-width: 500px;
      margin: 30px auto;
      font-size: 15px;
    }
    .cover-details p {
      margin: 8px 0;
      color: #334155;
    }
    .cover-details strong {
      color: #0f172a;
      display: inline-block;
      width: 180px;
    }
    
    /* General Report Typography */
    h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      color: #1e3a8a;
      border-bottom: 2px solid #3b82f6;
      padding-bottom: 6px;
      margin-top: 35px;
      margin-bottom: 20px;
      page-break-after: avoid;
    }
    h2 {
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      color: #0f172a;
      margin-top: 0;
      margin-bottom: 16px;
      page-break-before: always;
      padding-top: 20px;
    }
    h3 {
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      color: #334155;
      margin-top: 18px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }
    h4 {
      font-family: 'Outfit', sans-serif;
      font-size: 13.5px;
      color: #475569;
      margin-top: 12px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }
    p {
      margin-top: 0;
      margin-bottom: 16px;
      text-align: justify;
    }
    
    /* Mermaid Sequence & Chart Diagrams */
    .mermaid {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 16px;
      margin: 20px 0;
      display: flex;
      justify-content: center;
      page-break-inside: avoid;
    }
    .mermaid svg {
      width: 100% !important;
      max-height: 80vh !important;
      height: auto !important;
    }
    
    .section-divider {
      border: 0;
      height: 1px;
      background: #cbd5e1;
      margin: 35px 0;
    }
    
    /* Lists Styling */
    ul {
      margin-top: 0;
      margin-bottom: 16px;
      padding-left: 24px;
    }
    li {
      margin-bottom: 6px;
    }
    .nested-li {
      list-style-type: circle;
      margin-left: 20px;
    }
    
    /* Tables Styling */
    .report-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      margin-bottom: 24px;
      font-size: 13px;
      page-break-inside: avoid;
    }
    .report-table th {
      background: #1e3a8a;
      color: white;
      font-weight: 600;
      padding: 10px 12px;
      border: 1px solid #1e3a8a;
      text-align: left;
    }
    .report-table td {
      padding: 8px 12px;
      border: 1px solid #cbd5e1;
    }
    .report-table tr:nth-child(even) {
      background: #f8fafc;
    }
    
    /* Code block container layout */
    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 8px;
      font-size: 11.5px;
      line-height: 1.5;
      overflow-x: auto;
      margin-top: 8px;
      margin-bottom: 20px;
      page-break-inside: avoid;
    }
    code {
      font-family: 'Fira Code', 'Courier New', Courier, monospace;
    }
    p code, li code {
      background: #f1f5f9;
      color: #0f172a;
      padding: 2px 5px;
      border-radius: 4px;
      font-size: 13px;
    }
    
    /* Print Layout Configuration */
    .page-break {
      page-break-before: always;
      height: 0;
      margin: 0;
      border: none;
    }
    
    @media print {
      body {
        margin: 15mm;
      }
      .page-break {
        page-break-before: always;
      }
    }
  </style>
</head>
<body>
  <div style="padding: 15px 30px;">
    ${parsedHtmlContent}
  </div>
</body>
</html>`;

    // Save temporary HTML compilation file
    const tempHtmlPath = path.join(__dirname, 'temp_tech_report.html');
    fs.writeFileSync(tempHtmlPath, fullHtml);

    // Create an invisible BrowserWindow instance
    const win = new BrowserWindow({
      show: false,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true
      }
    });

    win.loadFile(tempHtmlPath);

    win.webContents.once('did-finish-load', () => {
      console.log("WebContents loaded. Waiting 2.5s for Mermaid.js rendering engine to compile SVGs...");
      setTimeout(async () => {
        try {
          console.log("Rendering HTML layout and printing PDF document...");
          
          // Print window contents to PDF file buffer
          const pdfData = await win.webContents.printToPDF({
            printBackground: true,
            pageSize: 'A4',
            margins: {
              top: 1,
              bottom: 1,
              left: 1,
              right: 1
            },
            landscape: false
          });

          // Write the PDF file buffer
          fs.writeFileSync(pdfPath, pdfData);
          console.log(`Success! PDF report compiled successfully at:\n${pdfPath}`);

          // Cleanup temporary HTML file
          try {
            fs.unlinkSync(tempHtmlPath);
          } catch (e) {}

          app.quit();
        } catch (err) {
          console.error("Failed to compile PDF during printing stream: ", err);
          app.quit();
        }
      }, 2500);
    });

  } catch (error) {
    console.error("Compilation script encountered critical error: ", error);
    app.quit();
  }
});
