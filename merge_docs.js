import fs from 'fs';
const compReportPath = 'JSPulse_OHMS_Final_Comprehensive_Internship_Report.md';
const techReportPath = 'JSPulse_OHMS_Technical_Architecture_Flows.md';
const exhaustivePath = 'JSPulse_OHMS_Exhaustive_Component_Catalog.md';
const diagramsPath = 'JSPulse_OHMS_System_Diagrams.md';
const sequencePath = 'JSPulse_OHMS_Advanced_Sequence_Diagrams.md';
const outPath = 'Internship_Report_at_Jindal_Steel_Patratu.md';

const compLines = fs.readFileSync(compReportPath, 'utf8').split('\n');
const techLines = fs.readFileSync(techReportPath, 'utf8').split('\n');
const exhLines = fs.readFileSync(exhaustivePath, 'utf8').split('\n');
const diagLines = fs.readFileSync(diagramsPath, 'utf8').split('\n');
const seqLines = fs.readFileSync(sequencePath, 'utf8').split('\n');

let part1 = [];
let part4 = [];

let inToC = false;

// Parse Part 1 (up to section 8)
for (let i = 0; i < compLines.length; i++) {
    const line = compLines[i];
    if (line.startsWith('## 4. Table of Contents')) {
        inToC = true;
        continue;
    }
    if (inToC && line.startsWith('## 5.')) {
        inToC = false;
    }
    if (inToC) continue;
    
    if (line.startsWith('## 8. Core Modules')) {
        break; // Stop at section 8
    }
    part1.push(line);
}

// Parse Part 4 (Final sections, renumbered to 28-30)
let foundSection10 = false;
for (let i = 0; i < compLines.length; i++) {
    let line = compLines[i];
    if (line.startsWith('## 10. Verification')) foundSection10 = true;
    
    if (foundSection10) {
        line = line.replace(/^## 10\./, '## 28.');
        line = line.replace(/^### 10\./, '### 28.');
        line = line.replace(/^## 11\./, '## 29.');
        line = line.replace(/^### 11\./, '### 29.');
        line = line.replace(/^## 12\./, '## 30.');
        line = line.replace(/^### 12\./, '### 30.');
        part4.push(line);
    }
}

// Parse Part 2 (Tech flows, renumbered 1->8, 2->9 ... 12->19)
let part2 = [];
let foundTechStart = false;
for (let i = 0; i < techLines.length; i++) {
    let line = techLines[i];
    if (line.startsWith('## 1. Custom')) foundTechStart = true;
    
    if (foundTechStart) {
        if (line.startsWith('**End of Technical')) continue;
        
        let match = line.match(/^## (\d+)\./);
        if (match) {
            let num = parseInt(match[1]);
            let newNum = num + 7;
            line = line.replace(/^## \d+\./, `## ${newNum}.`);
        }
        part2.push(line);
    }
}

// Combine: Part 1 + Diagrams + Part 2 + Part 3 + Part 4 + Sequence Diagrams
const merged = [...part1, '', ...diagLines, '', '---', '', ...part2, '', '---', '', ...exhLines, '', '---', '', ...part4, '', '---', '', ...seqLines];
fs.writeFileSync(outPath, merged.join('\n'));
console.log('Massive 5-part merged markdown with Sequence Diagrams created successfully.');
