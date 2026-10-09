import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const mdPath = path.join(__dirname, 'Internship_Report_at_Jindal_Steel_Patratu.md');
let mdContent = fs.readFileSync(mdPath, 'utf8');

// 1. Manual vs Automated Workflow
const manualVsAutoChart = `
#### Automation Contrast: Manual vs. Desktop Pipeline
\`\`\`mermaid
graph TD
    subgraph "Legacy Manual Process (Slow & Error Prone)"
        A[Doctor writes Rx on paper] --> B[Patient walks to Pharmacy]
        B --> C[Pharmacist searches paper ledger]
        C --> D[Pharmacist manually deducts stock]
        D --> E[End of Month: Manual Tallying]
    end

    subgraph "JSPulse OHMS Automated Pipeline (Instant)"
        F[Doctor inputs Rx digitally] --> G[Proxy Engine intercepts & saves locally]
        G -.->|Background Sync Loop| H[Pharmacy Queue auto-updates]
        H --> I[Pharmacist clicks 'Dispense']
        I --> J[Stock auto-deducted via DailyConsume algorithm]
        J -.->|Automated Aggregation| K[End of Month: One-click MIS Generation]
    end
\`\`\`
`;

mdContent = mdContent.replace(
  '### 6.2 Proposed Desktop JSPulse OHMS Solution',
  '### 6.2 Proposed Desktop JSPulse OHMS Solution\n' + manualVsAutoChart
);

// 2. Global Search Debounced Indexing
const globalSearchChart = `
### Global Search Indexing Automation Flowchart
\`\`\`mermaid
stateDiagram-v2
    [*] --> Idle: User hits CTRL+K
    
    Idle --> Typing: User types query
    
    Typing --> Debouncing: 300ms delay timer
    
    Debouncing --> Typing: User types again (timer reset)
    Debouncing --> Searching: Timer expires
    
    state Searching {
        SearchEngine --> cms_patient_visit_log: Scan Patient DB
        SearchEngine --> cms_medstock_data: Scan Pharmacy DB
        SearchEngine --> cms_employee_health: Scan Employee DB
    }
    
    Searching --> Rendering: Map results to UI
    Rendering --> [*]: User clicks result
\`\`\`
`;

mdContent = mdContent.replace(
  '### Granular Button & Element Catalog\n*   **[Global Search Bar (CTRL+K)]:**',
  globalSearchChart + '\n### Granular Button & Element Catalog\n*   **[Global Search Bar (CTRL+K)]:**'
);

// 3. Emergency Crash Recovery Automation
const recoveryChart = `
### Emergency Crash Recovery Automation Flowchart
\`\`\`mermaid
sequenceDiagram
    autonumber
    participant App as React UI
    participant Storage as localStorage
    participant Monitor as Health Monitor Loop
    participant FS as C:\OHSData (Hard Drive)

    loop Every 60 Seconds
        Monitor->>Storage: Measure total byte size
        alt Quota Exceeded (5MB Limit)
            Monitor-->>App: Trigger UI Freeze (Red Alert)
            Monitor->>Storage: Serialize all arrays to massive JSON
            Monitor->>FS: IPC dump JSON directly to Hard Drive
            FS-->>Monitor: Acknowledge Safe Dump
            Monitor->>Storage: Execute localStorage.clear()
            Monitor-->>App: Reload Window (Crash Avoided)
        end
    end
\`\`\`
`;

mdContent = mdContent.replace(
  '### Granular Button & Element Catalog\n*   **[Estimate Quota Button]:**',
  recoveryChart + '\n### Granular Button & Element Catalog\n*   **[Estimate Quota Button]:**'
);

// 4. Monthly MIS Aggregation Engine
const misChapter = `
## 27.5 Exhaustive UI Component: Monthly MIS Aggregation Engine
**Location:** \`src/components/clinical/MonthlyMISReport.jsx\`

### Comprehensive Overview
The Monthly Management Information System (MIS) aggregator automates the excruciatingly tedious process of generating end-of-month clinical reports. Rather than human operators manually counting ledgers, this component runs a heavy algorithmic pipeline across the entire local database.

### Algorithmic Aggregation Flowchart
\`\`\`mermaid
flowchart TD
    Start[User selects Month/Year] --> Load[Load \`cms_patient_visit_log\`]
    Load --> Filter[Filter out records not matching Month/Year]
    Filter --> InitializeCounters[Initialize Counters: Total, Male, Female, Diseases]
    
    InitializeCounters --> Loop[Loop through every filtered record]
    
    Loop --> CheckGender{Is patient Male?}
    CheckGender -->|Yes| Male++
    CheckGender -->|No| Female++
    
    Loop --> CheckCategory{Check Diagnosis Category}
    CheckCategory -->|Cardiology| Card++
    CheckCategory -->|Dermatology| Derm++
    CheckCategory -->|Respiratory| Resp++
    CheckCategory -->|Others| Other++
    
    Loop --> NextRecord{More records?}
    NextRecord -->|Yes| Loop
    
    NextRecord -->|No| Output[Construct massive Analytics Object]
    Output --> RenderUI[Render React Tables & KPIs]
    RenderUI --> Export[Generate Excel Binary]
\`\`\`

### Granular Button & Element Catalog
*   **[Generate Report Button]:** Triggers the \`for\` loop over potentially thousands of records. It blocks the UI to prioritize CPU cycles for the counting algorithm.
*   **[Export to Excel (IPC)]:** Packages the calculated counters into a multi-sheet array buffer and passes it to the Electron IPC bridge for native saving.

---
`;

mdContent = mdContent.replace(
  '## 28. Verification & Quality Assurance (QA)',
  misChapter + '\n## 28. Verification & Quality Assurance (QA)'
);

fs.writeFileSync(mdPath, mdContent);
console.log('Successfully injected 4 massive automation flowcharts into the master document.');
