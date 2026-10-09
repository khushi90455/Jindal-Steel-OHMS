import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const targetFiles = [
  'src/main.jsx',
  'src/App.jsx',
  'src/components/Dashboard.jsx',
  'src/components/clinical/ExcelGrid.jsx',
  'src/components/clinical/OPDCounter.jsx',
  'src/components/DispenseMedicine.jsx',
  'src/components/clinical/DailyConsume.jsx',
  'src/utils/chatBrain.js',
  'src/components/GlobalSearch.jsx'
];

let mdContent = '## 31. Appendix: Primary Source Code Listings\n\n';
mdContent += 'This appendix provides the raw, unedited source code for the most critical modules of the JSPulse OHMS application. It serves as an exhaustive reference for the custom React logic, proxy engines, and algorithms detailed in previous chapters.\n\n';

targetFiles.forEach((file, index) => {
  try {
    const fullPath = path.join(__dirname, file);
    if (fs.existsSync(fullPath)) {
      const code = fs.readFileSync(fullPath, 'utf8');
      mdContent += `### A.${index + 1} ${file}\n`;
      mdContent += '```javascript\n';
      mdContent += code + '\n';
      mdContent += '```\n\n';
    } else {
      console.error(`File not found: ${file}`);
    }
  } catch (err) {
    console.error(`Failed to read ${file}: `, err);
  }
});

const outPath = path.join(__dirname, 'JSPulse_OHMS_Source_Code_Appendix.md');
fs.writeFileSync(outPath, mdContent);
console.log('Source Code Appendix Markdown generated successfully!');
