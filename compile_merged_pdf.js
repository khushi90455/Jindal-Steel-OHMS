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

    // Bypass parsing for raw HTML block elements (e.g. tables, custom lists, divs)
    if (line.trim().startsWith('<') && line.trim().includes('>')) {
      if (inList) { html += '</ul>\n'; inList = false; }
      if (inTable) { html += '</tbody></table>\n'; inTable = false; }
      html += line + '\n';
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
      if (titleText.includes('INDUSTRIAL INTERNSHIP')) {
        // Render Cover Page block
        html += `
        <div class="cover-container">
          <div class="orange-bar"></div>
          <div class="logo-header">JINDAL STEEL</div>
          <h1 class="cover-title">JSPulse OHMS<br>(Occupational Health Management System)</h1>
          <h3 class="cover-subtitle">Master Technical Internship Report on the Design, Implementation, Security, and Architectural Automation Algorithms of an Offline-First Enterprise Health Registry</h3>
          <div class="cover-divider"></div>
          <div class="cover-details">
            <p><strong>Developed By:</strong> Ashwini Kumar</p>
            <p><strong>Intern ID:</strong> JSPL-2026-IT-042</p>
            <p><strong>Department:</strong> Information Technology &amp; Occupational Health Services Group</p>
            <p><strong>Location:</strong> Jindal Steel, Patratu</p>
            <p><strong>Period:</strong> Summer 2026</p>
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
    const mdPath = path.join(__dirname, 'Internship_Report_at_Jindal_Steel_Patratu.md');
    const pdfPath = path.join(__dirname, 'Internship_Report_at_Jindal_Steel_Patratu.pdf');

    if (!fs.existsSync(mdPath)) {
      console.error(`Error: Source Markdown report not found at ${mdPath}`);
      app.quit();
      return;
    }

    const mdContent = fs.readFileSync(mdPath, 'utf8');
    const parsedHtmlContent = mdToHtml(mdContent);

    // HTML Wrapper — Academic Print Styling: Times New Roman, 12pt, 1.5 line spacing
    const fullHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Internship Report — JSPulse OHMS — Jindal Steel Patratu</title>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"><\/script>
  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      securityLevel: 'loose',
      flowchart: { useMaxWidth: false, htmlLabels: true }
    });
    window.addEventListener('load', () => {
      setTimeout(() => {
        let diagramIndex = 0;
        document.querySelectorAll('body > div > *').forEach((el) => {
          if (el.classList.contains('mermaid')) {
            diagramIndex++;
            const isError = el.textContent.includes('Syntax error') || el.querySelector('.error-icon');
            console.log(isError ? '[MERMAID ERROR]' : '[MERMAID OK]', 'Diagram #' + diagramIndex);
          }
        });
      }, 1500);
    });
  <\/script>
  <style>
    /* ===================================================================== */
    /* ACADEMIC PRINT STYLESHEET                                             */
    /* Font: Times New Roman | Size: 12pt | Line Spacing: 1.5               */
    /* ===================================================================== */

    @page {
      size: A4;
      margin: 25mm 20mm 28mm 25mm;
    }
    * { box-sizing: border-box; }

    body {
      font-family: 'Times New Roman', Times, serif;
      color: #000000;
      line-height: 1.5;
      font-size: 12pt;
      margin: 0;
      padding: 0;
      background: white;
    }

    /* ---------- Cover Page ---------- */
    .cover-container {
      height: 93vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 40px 50px;
      border: 2px solid #000000;
      margin: 10px;
    }
    .orange-bar, .green-bar {
      width: 80px;
      height: 4px;
      background: #000000;
    }
    .logo-header {
      font-family: 'Times New Roman', Times, serif;
      font-weight: bold;
      font-size: 14pt;
      letter-spacing: 3px;
      color: #000000;
      margin-top: 10px;
      text-transform: uppercase;
    }
    .cover-title {
      font-family: 'Times New Roman', Times, serif;
      font-weight: bold;
      font-size: 20pt;
      color: #000000;
      line-height: 1.4;
      margin: 30px 0 15px;
    }
    .cover-subtitle {
      font-family: 'Times New Roman', Times, serif;
      font-style: italic;
      font-size: 12pt;
      color: #000000;
      max-width: 500px;
      line-height: 1.5;
      margin-bottom: 30px;
    }
    .cover-divider {
      width: 100%;
      height: 1px;
      background: #000000;
    }
    .cover-details {
      text-align: left;
      width: 100%;
      max-width: 480px;
      margin: 20px auto;
      font-size: 11pt;
      line-height: 1.8;
    }
    .cover-details p { margin: 6px 0; color: #000000; }
    .cover-details strong {
      color: #000000;
      display: inline-block;
      width: 200px;
      font-weight: bold;
    }

    /* ---------- Headings ---------- */
    h1 {
      font-family: 'Times New Roman', Times, serif;
      font-size: 16pt;
      font-weight: bold;
      color: #000000;
      border-bottom: 2px solid #000000;
      padding-bottom: 4px;
      margin-top: 30px;
      margin-bottom: 14px;
      page-break-after: avoid;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    h2 {
      font-family: 'Times New Roman', Times, serif;
      font-size: 14pt;
      font-weight: bold;
      color: #000000;
      margin-top: 26px;
      margin-bottom: 10px;
      page-break-after: avoid;
      border-bottom: 1px solid #000000;
      padding-bottom: 3px;
    }
    h3 {
      font-family: 'Times New Roman', Times, serif;
      font-size: 12pt;
      font-weight: bold;
      color: #000000;
      margin-top: 16px;
      margin-bottom: 7px;
      page-break-after: avoid;
    }
    h4 {
      font-family: 'Times New Roman', Times, serif;
      font-size: 12pt;
      font-weight: bold;
      font-style: italic;
      color: #000000;
      margin-top: 12px;
      margin-bottom: 5px;
      page-break-after: avoid;
    }

    /* ---------- Body Text ---------- */
    p {
      margin-top: 0;
      margin-bottom: 10pt;
      text-align: justify;
      font-size: 12pt;
      line-height: 1.5;
      color: #000000;
    }

    /* ---------- Figure / Table Captions ---------- */
    p > em:only-child {
      display: block;
      text-align: center;
      font-style: italic;
      font-size: 11pt;
      color: #444444;
      margin-top: -4pt;
      margin-bottom: 14pt;
    }

    /* ---------- Mermaid Diagrams ---------- */
    .mermaid {
      background: #ffffff;
      border: 1px solid #aaaaaa;
      padding: 10px;
      margin: 12px 0 4px;
      display: flex;
      justify-content: center;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    .mermaid svg {
      max-width: 100% !important;
      max-height: 680px !important;
      height: auto !important;
    }

    .section-divider {
      border: 0;
      border-top: 1px solid #666666;
      margin: 24px 0;
    }

    /* ---------- Lists ---------- */
    ul, ol {
      margin-top: 0;
      margin-bottom: 10pt;
      padding-left: 28px;
      font-size: 12pt;
      line-height: 1.5;
    }
    li { margin-bottom: 3px; color: #000000; }
    .nested-li { list-style-type: circle; margin-left: 20px; }
    .toc-list {
      list-style-type: none;
      padding-left: 0;
      font-size: 12pt;
      line-height: 2.0;
    }
    .toc-list li {
      border-bottom: 1px dotted #999999;
      padding-bottom: 3px;
      margin-bottom: 5px;
    }

    /* ---------- Index Table ---------- */
    .index-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      margin-bottom: 16px;
      font-size: 11pt;
      line-height: 1.4;
    }
    .index-table th {
      background: #000000;
      color: #ffffff;
      font-weight: bold;
      padding: 6px 10px;
      border: 1px solid #000000;
      text-align: left;
      font-family: 'Times New Roman', Times, serif;
      font-size: 11pt;
    }
    .index-table td {
      padding: 5px 10px;
      border: 1px solid #999999;
      vertical-align: middle;
      font-size: 11pt;
    }
    .index-table tr:nth-child(even) { background: #f4f4f4; }
    .index-table .sec-num {
      font-weight: bold;
      color: #000000;
      width: 40px;
      text-align: center;
      background: #eeeeee;
    }
    .index-table .sec-title { font-weight: normal; color: #000000; }

    /* ---------- Report Tables ---------- */
    .report-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 6px;
      margin-bottom: 16pt;
      font-size: 11pt;
      page-break-inside: avoid;
      line-height: 1.4;
    }
    .report-table th {
      background: #000000;
      color: #ffffff;
      font-weight: bold;
      padding: 7px 10px;
      border: 1px solid #000000;
      text-align: left;
      font-family: 'Times New Roman', Times, serif;
    }
    .report-table td {
      padding: 6px 10px;
      border: 1px solid #999999;
      color: #000000;
    }
    .report-table tr:nth-child(even) { background: #f4f4f4; }

    /* ---------- Code Blocks ---------- */
    pre {
      background: #f8f8f8;
      color: #000000;
      border: 1px solid #cccccc;
      border-left: 4px solid #555555;
      padding: 10px 12px;
      font-size: 9.5pt;
      line-height: 1.45;
      margin-top: 4px;
      margin-bottom: 14px;
      white-space: pre-wrap;
      word-wrap: break-word;
      page-break-inside: auto;
    }
    code {
      font-family: 'Fira Code', 'Courier New', Courier, monospace;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 9.5pt;
    }
    p code, li code {
      background: #eeeeee;
      color: #000000;
      padding: 1px 4px;
      border-radius: 2px;
      font-size: 10.5pt;
      font-family: 'Fira Code', 'Courier New', Courier, monospace;
    }

    /* ---------- Page Breaks ---------- */
    .page-break {
      page-break-before: always;
      height: 0;
      margin: 0;
      border: none;
    }

    @media print {
      body { margin: 0; }
      .page-break { page-break-before: always; }
    }
  </style>
</head>
<body>
  <div style="padding: 0;">
    ${parsedHtmlContent}
  </div>
</body>
</html>`;

    // Save temporary HTML compilation file
    const tempHtmlPath = path.join(__dirname, 'temp_merged_report.html');
    fs.writeFileSync(tempHtmlPath, fullHtml);

    // Create an invisible BrowserWindow instance
    const win = new BrowserWindow({
      show: false,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true
      }
    });

    win.webContents.on('console-message', (event, level, message, line, sourceId) => {
      console.log(`[BROWSER] (lvl${level}): ${message}`);
    });

    win.loadFile(tempHtmlPath);

    win.webContents.once('did-finish-load', () => {
      console.log("Page loaded. Waiting 3s for Mermaid.js diagrams to render...");
      setTimeout(async () => {
        try {
          console.log("Compiling academic PDF document...");

          // Print with page number footer in Times New Roman
          const pdfData = await win.webContents.printToPDF({
            printBackground: true,
            preferCSSPageSize: true,
            displayHeaderFooter: true,
            headerTemplate: '<div style="font-size:0px;"></div>',
            footerTemplate: `<div style="width:100%;text-align:center;font-family:'Times New Roman',Times,serif;font-size:10pt;color:#444444;padding:4px 0;"><span class='pageNumber'></span> of <span class='totalPages'></span></div>`,
            margins: {
              top: 1.0,
              bottom: 1.3,
              left: 0.8,
              right: 0.8
            },
            landscape: false
          });

          // Write the PDF file buffer
          fs.writeFileSync(pdfPath, pdfData);
          console.log(`\n✓ Academic PDF report compiled successfully:\n  ${pdfPath}\n`);

          // Cleanup temporary HTML file
          try { fs.unlinkSync(tempHtmlPath); } catch (e) {}
          app.quit();
        } catch (err) {
          console.error("Failed to compile PDF:", err);
          app.quit();
        }
      }, 3000);
    });

  } catch (error) {
    console.error("Compilation error:", error);
    app.quit();
  }
});
