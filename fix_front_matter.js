import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const mdPath = path.join(__dirname, 'Internship_Report_at_Jindal_Steel_Patratu.md');
let mdLines = fs.readFileSync(mdPath, 'utf8').split('\n');

// We need to build the Index Page dynamically by scanning for all ## headers that have numbers
let indexPage = '## Index\n\n<ul class="toc-list">\n';
for (let line of mdLines) {
    if (line.startsWith('## ') && line.match(/^## \d+\./)) {
        // e.g. "## 3. Executive Summary"
        let title = line.substring(3).trim();
        indexPage += `<li><strong>${title}</strong></li>\n`;
    }
}
indexPage += '</ul>\n\n<div class="page-break"></div>\n\n';

let newLines = [];
let foundDeclaration = false;
let foundAck = false;
let foundExecSum = false;

for (let i = 0; i < mdLines.length; i++) {
    let line = mdLines[i];

    if (line.startsWith('## 1. Declaration of Originality')) {
        newLines.push('<div class="page-break"></div>');
        newLines.push('## Declaration of Originality');
        foundDeclaration = true;
        continue;
    }

    if (line.startsWith('## 2. Acknowledgements')) {
        // We want this on the same page as Declaration, so no page-break before it
        newLines.push('## Acknowledgements');
        foundAck = true;
        continue;
    }
    
    if (line.startsWith('## 3. Executive Summary') && !foundExecSum) {
        // Right before the Executive Summary, insert the page break and the generated Index
        newLines.push('<div class="page-break"></div>');
        newLines.push(indexPage.trim());
        newLines.push('\n<div class="page-break"></div>');
        newLines.push(line);
        foundExecSum = true;
        continue;
    }

    newLines.push(line);
}

fs.writeFileSync(mdPath, newLines.join('\n'));
console.log('Front matter perfectly restructured: Declaration/Acknowledgements combined, numbers removed, and dynamic Index injected.');
