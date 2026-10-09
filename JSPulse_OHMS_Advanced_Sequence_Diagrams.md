## 31. Advanced Subsystem Visual Mappings & Logical Algorithms

Rather than providing raw source code, this chapter maps out the exact logical execution paths, state machines, and Inter-Process Communication (IPC) pipelines that power the system's most complex behaviors.

### 31.1 The Electron IPC Bridge (React to Node.js Sequence)
The following sequence diagram maps the exact chronological flow of data when a user triggers an export operation. Because the React frontend is completely sandboxed for security, it cannot touch the Windows filesystem directly. It must serialize the data, pass it over the isolated `window.electronAPI` bridge, and await the Node.js Main Process to execute the native `fs.writeFileSync` operations.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant ReactUI as React Frontend (Renderer)
    participant Preload as Preload Sandbox (Context Bridge)
    participant MainProcess as Electron Main (Node.js)
    participant FS as Native Windows FileSystem (C:\OHSData)

    User->>ReactUI: Clicks "Export to Excel"
    ReactUI->>ReactUI: Aggregates virtual DOM Data
    ReactUI->>ReactUI: Serializes data to JSON Buffer
    ReactUI->>Preload: window.electronAPI.exportExcel(buffer)
    activate Preload
    Preload->>MainProcess: IPC Invoke ('export-excel', buffer)
    deactivate Preload
    activate MainProcess
    MainProcess->>MainProcess: Initialize xlsx workbook
    MainProcess->>MainProcess: Convert JSON array to Sheet
    MainProcess->>FS: fs.writeFileSync(path, binaryData)
    activate FS
    FS-->>MainProcess: Return OK (File Locked & Saved)
    deactivate FS
    MainProcess-->>Preload: IPC Reply (Success Path)
    deactivate MainProcess
    activate Preload
    Preload-->>ReactUI: Resolve Promise
    deactivate Preload
    ReactUI->>User: Render Success Toast Notification
```

*Figure 31.1: Electron IPC Bridge Export Sequence — React Renderer to Native Windows FileSystem*

### 31.2 The Patient Lifecycle State Machine
The following state diagram visualizes the strict lifecycle of a patient record. A record cannot jump from Registration directly to Dispensed without passing through the OPD assessment. The `extracted` boolean flag securely gates the transition between the OPD database and the Pharmacy queue.

```mermaid
stateDiagram-v2
    [*] --> PendingVitals: Patient Arrives at Reception
    
    PendingVitals --> InConsultation: Vitals Recorded (OPDCounter)
    
    InConsultation --> PrescriptionDrafting: Doctor Inputting Diagnosis
    
    state PrescriptionDrafting {
        [*] --> CheckInteractions
        CheckInteractions --> AddDrug
        AddDrug --> CheckInteractions
        CheckInteractions --> SubmitPrescription: Safety Matrix Cleared
    }
    
    PrescriptionDrafting --> PharmacyQueue: Record Saved (extracted: false)
    
    PharmacyQueue --> DispensingPending: Pharmacy Sync Loop Sweeps Record
    
    DispensingPending --> Completed: Pharmacist clicks "Mark Dispensed"
    
    Completed --> [*]: `DailyConsume.jsx` Deducts Stock Array
```

*Figure 31.2: Patient Record State Machine — OPD Registration to Dispensing Completion*

### 31.3 LocalStorage to IndexedDB Data Migration Flowchart
Because JSPulse OHMS operates offline without a cloud backend, it relies heavily on local browser storage. The following flowchart demonstrates the autonomous quota-defense mechanism that prevents the `5MB QuotaExceededError` from crashing the application.

```mermaid
flowchart TD
    Start((Migration Hook Fires)) --> ReadKeys[Read all localStorage Keys]
    ReadKeys --> ByteCalc[Calculate UTF-16 String Length in Bytes]
    ByteCalc --> Summation{Is Total Size > 4.5MB?}
    
    Summation -->|No| Safe[Do Nothing. System Healthy]
    
    Summation -->|Yes| Filter[Filter keys ending in `_auto_backup`]
    Filter --> Batch[Aggregate into massive JSON array]
    Batch --> IDB[Open sheetDB IndexedDB Pool]
    IDB --> IDBPush[Push JSON array into IDB Object Store]
    
    IDBPush --> ValidateIDB{Did IDB Write Succeed?}
    
    ValidateIDB -->|No| ErrorHandler[Trigger Emergency C:\OHSData JSON Dump via IPC]
    ErrorHandler --> Purge
    
    ValidateIDB -->|Yes| Purge[Purge `_auto_backup` keys from localStorage]
    Purge --> ReRender[Force React DOM Re-render]
    ReRender --> Safe
```

*Figure 31.3: LocalStorage to IndexedDB Quota-Defense Auto-Migration Flowchart*

### 31.4 The Offline AI Intent Classification Tree
The offline ChatBrain NLP engine replaces the need for cloud APIs during network outages. The following decision tree maps out how raw conversational English is tokenized and routed to the correct local database index.

```mermaid
graph TD
    UserQuery[Raw String: "How much Paracetamol is left in stock?"]
    UserQuery --> Tokenizer[Lowercase, Regex Strip Punctuation]
    Tokenizer --> TokenArray["[how, much, paracetamol, is, left, in, stock]"]
    
    TokenArray --> IntentMatcher{Regex Intent Matching}
    
    IntentMatcher -->|Matches 'stock'| StockLogic[Trigger Inventory Subsystem]
    IntentMatcher -->|Matches 'visit'| VisitLogic[Trigger Patient Log Subsystem]
    IntentMatcher -->|Matches 'excel'| ExcelLogic[Trigger Grid Command Subsystem]
    
    StockLogic --> FilterArray[Extract 'paracetamol' as subject]
    FilterArray --> LocalStorageRead[Read `cms_medstock_data`]
    LocalStorageRead --> SearchIndex[Fuzzy match 'paracetamol' against IDs]
    
    SearchIndex --> MatchFound{Match Found?}
    
    MatchFound -->|Yes| ConstructSuccess[Return: "Paracetamol currently has 450 units in stock."]
    MatchFound -->|No| ConstructFail[Return: "I couldn't find Paracetamol in the local inventory."]
    
    ConstructSuccess --> UIRender[Append AI message to ChatAssistant State]
    ConstructFail --> UIRender
```

*Figure 31.4: Offline AI Intent Classification Decision Tree for Natural Language Queries*
