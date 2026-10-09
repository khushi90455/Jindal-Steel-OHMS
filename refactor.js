const fs = require('fs');
const path = require('path');

const components = [
  {
    name: 'AdvancedPatientRecords',
    title: 'Patient Visits',
    prefix: 'PAT-',
    columns: `
  { key: 'patientId', label: 'Patient ID', letter: 'A', width: 100, type: 'text' },
  { key: 'patientName', label: 'Patient Name', letter: 'B', width: 160, type: 'text' },
  { key: 'age', label: 'Age', letter: 'C', width: 60, type: 'number' },
  { key: 'gender', label: 'Gender', letter: 'D', width: 90, type: 'select', options: ['Male', 'Female', 'Other'] },
  { key: 'diagnosis', label: 'Diagnosis', letter: 'E', width: 180, type: 'text' },
  { key: 'doctor', label: 'Assigned Doctor', letter: 'F', width: 160, type: 'text' },
  { key: 'visitDate', label: 'Visit Date', letter: 'G', width: 130, type: 'date' },
  { key: 'status', label: 'Status', letter: 'H', width: 120, type: 'status', options: ['Active', 'Critical', 'Follow-up', 'Discharged'] },
  { key: 'notes', label: 'Notes', letter: 'I', width: 220, type: 'text' }
    `,
    data: `
  { patientId: 'PAT-001', patientName: 'Rajesh Kumar', age: 45, gender: 'Male', diagnosis: 'Heat Exhaustion', doctor: 'Dr. Sharma', visitDate: '2026-06-09', status: 'Active', notes: 'Blast Furnace worker' },
  { patientId: 'PAT-002', patientName: 'Suresh Yadav', age: 38, gender: 'Male', diagnosis: 'Chemical Burns', doctor: 'Dr. Patel', visitDate: '2026-06-08', status: 'Critical', notes: 'Coke Oven exposure' }
    `
  },
  {
    name: 'FirstAidBoxTracker',
    title: 'First Aid Box Location Tracker',
    prefix: 'FA-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'location', label: 'Location', letter: 'B', width: 150, type: 'text' },
  { key: 'outside', label: 'Outside', letter: 'C', width: 100, type: 'text' },
  { key: 'name', label: 'Name', letter: 'D', width: 150, type: 'text' },
  { key: 'gcode', label: 'G.Code', letter: 'E', width: 100, type: 'text' },
  { key: 'mobile', label: 'Mobile No.', letter: 'F', width: 120, type: 'text' },
  { key: 'qty', label: 'Qty', letter: 'G', width: 60, type: 'number' },
  { key: 'chk1', label: 'Chk1', letter: 'H', width: 60, type: 'text' },
  { key: 'chk2', label: 'Chk2', letter: 'I', width: 60, type: 'text' },
  { key: 'chk3', label: 'Chk3', letter: 'J', width: 60, type: 'text' },
  { key: 'chk4', label: 'Chk4', letter: 'K', width: 60, type: 'text' },
  { key: 'chk5', label: 'Chk5', letter: 'L', width: 60, type: 'text' },
  { key: 'signature', label: 'Signature', letter: 'M', width: 120, type: 'text' }
    `,
    data: `
  { id: 'FA-001', location: 'Blast Furnace', outside: 'No', name: 'R. Sharma', gcode: 'G-101', mobile: '9876543210', qty: 5, chk1: 'OK', chk2: 'OK', chk3: 'OK', chk4: 'OK', chk5: 'OK', signature: 'RS' },
  { id: 'FA-002', location: 'Coke Oven', outside: 'Yes', name: 'S. Singh', gcode: 'G-102', mobile: '9876543211', qty: 3, chk1: 'OK', chk2: 'Low', chk3: 'OK', chk4: 'OK', chk5: 'OK', signature: 'SS' }
    `
  },
  {
    name: 'MedicineStockRegister',
    title: 'Medicine Stock Register',
    prefix: 'MED-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'medicineName', label: 'Medicine Name', letter: 'B', width: 180, type: 'text' },
  { key: 'category', label: 'Category', letter: 'C', width: 120, type: 'select', options: ['Analgesic', 'Antibiotic', 'Antiseptic', 'Bandage', 'ORS', 'Ointment', 'Other'] },
  { key: 'quantity', label: 'Quantity In Stock', letter: 'D', width: 100, type: 'number' },
  { key: 'unit', label: 'Unit', letter: 'E', width: 90, type: 'select', options: ['Tablets', 'Capsules', 'Bottles', 'Tubes', 'Strips', 'Pieces'] },
  { key: 'expiry', label: 'Expiry Date', letter: 'F', width: 120, type: 'date' },
  { key: 'reorder', label: 'Reorder Level', letter: 'G', width: 100, type: 'number' },
  { key: 'lastUpdated', label: 'Last Updated', letter: 'H', width: 120, type: 'date' }
    `,
    data: `
  { id: 'MED-001', medicineName: 'Paracetamol 500mg', category: 'Analgesic', quantity: 500, unit: 'Tablets', expiry: '2025-12-31', reorder: 100, lastUpdated: '2024-06-01' },
  { id: 'MED-002', medicineName: 'Amoxicillin 250mg', category: 'Antibiotic', quantity: 15, unit: 'Capsules', expiry: '2023-12-31', reorder: 50, lastUpdated: '2024-06-01' }
    `,
    extra: `
const getRowStyle = (row) => {
  if (!row) return {};
  if (row.quantity && row.reorder && Number(row.quantity) <= Number(row.reorder)) {
    return { background: '#fef2f2', color: '#dc2626' }; // Light red
  }
  if (row.expiry && new Date(row.expiry) < new Date()) {
    return { background: '#7f1d1d', color: '#ffffff' }; // Dark red
  }
  return {};
};
    `
  },
  {
    name: 'InjuryReportLog',
    title: 'Injury Report Log',
    prefix: 'INJ-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'date', label: 'Date', letter: 'B', width: 120, type: 'date' },
  { key: 'employeeName', label: 'Employee Name', letter: 'C', width: 160, type: 'text' },
  { key: 'department', label: 'Department', letter: 'D', width: 120, type: 'text' },
  { key: 'natureOfInjury', label: 'Nature of Injury', letter: 'E', width: 150, type: 'text' },
  { key: 'bodyPart', label: 'Body Part Affected', letter: 'F', width: 150, type: 'text' },
  { key: 'firstAid', label: 'First Aid Given', letter: 'G', width: 150, type: 'text' },
  { key: 'referred', label: 'Referred to Hospital', letter: 'H', width: 120, type: 'select', options: ['No', 'Yes'] },
  { key: 'reportedBy', label: 'Reported By', letter: 'I', width: 120, type: 'text' },
  { key: 'status', label: 'Status', letter: 'J', width: 100, type: 'status', options: ['Open', 'Closed'] }
    `,
    data: `
  { id: 'INJ-001', date: '2024-06-08', employeeName: 'Ramesh Patel', department: 'Rolling Mill', natureOfInjury: 'Laceration', bodyPart: 'Left Hand', firstAid: 'Bandaged', referred: 'No', reportedBy: 'Supervisor Singh', status: 'Closed' },
  { id: 'INJ-002', date: '2024-06-09', employeeName: 'Suresh Kumar', department: 'Blast Furnace', natureOfInjury: 'Burn', bodyPart: 'Right Arm', firstAid: 'Cooling gel applied', referred: 'Yes', reportedBy: 'Shift Lead', status: 'Open' }
    `
  },
  {
    name: 'VitalSignsChart',
    title: 'Vital Signs Chart',
    prefix: 'VIT-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'patientName', label: 'Patient Name', letter: 'B', width: 160, type: 'text' },
  { key: 'dateTime', label: 'Date & Time', letter: 'C', width: 160, type: 'date' },
  { key: 'bp', label: 'Blood Pressure', letter: 'D', width: 120, type: 'text' },
  { key: 'pulse', label: 'Pulse Rate', letter: 'E', width: 100, type: 'number' },
  { key: 'temp', label: 'Temperature (F)', letter: 'F', width: 120, type: 'number' },
  { key: 'spo2', label: 'SpO2 (%)', letter: 'G', width: 100, type: 'number' },
  { key: 'sugar', label: 'Blood Sugar', letter: 'H', width: 100, type: 'number' },
  { key: 'weight', label: 'Weight (kg)', letter: 'I', width: 100, type: 'number' },
  { key: 'remarks', label: 'Remarks', letter: 'J', width: 200, type: 'text' }
    `,
    data: `
  { id: 'VIT-001', patientName: 'Amit Tiwari', dateTime: '2024-06-09', bp: '120/80', pulse: 72, temp: 98.6, spo2: 98, sugar: 95, weight: 75, remarks: 'Normal' },
  { id: 'VIT-002', patientName: 'Mohan Lal', dateTime: '2024-06-09', bp: '160/100', pulse: 105, temp: 100.2, spo2: 94, sugar: 210, weight: 85, remarks: 'High BP, Tachycardia' }
    `,
    extra: `
const getCustomCellContent = (col, value) => {
  if (!value) return value;
  let isAbnormal = false;
  if (col.key === 'bp' && value.includes('/')) {
    const parts = value.split('/');
    if (parseInt(parts[0]) > 140 || parseInt(parts[0]) < 90) isAbnormal = true;
  }
  if (col.key === 'pulse' && (value < 60 || value > 100)) isAbnormal = true;
  if (col.key === 'temp' && (value > 99.5 || value < 96.0)) isAbnormal = true;
  if (col.key === 'spo2' && value < 95) isAbnormal = true;
  if (col.key === 'sugar' && (value > 200 || value < 70)) isAbnormal = true;
  
  if (isAbnormal) return <span style={{ color: '#dc2626', fontWeight: 'bold' }}>{value}</span>;
  return value;
};
    `
  },
  {
    name: 'EmployeeHealthRecords',
    title: 'Employee Health Records',
    prefix: 'EMP-',
    columns: `
  { key: 'id', label: 'Emp ID', letter: 'A', width: 100, type: 'text' },
  { key: 'name', label: 'Employee Name', letter: 'B', width: 160, type: 'text' },
  { key: 'department', label: 'Department', letter: 'C', width: 140, type: 'select', options: ['Blast Furnace', 'Rolling Mill', 'Coke Oven', 'Sinter Plant', 'Power Plant', 'Admin'] },
  { key: 'designation', label: 'Designation', letter: 'D', width: 140, type: 'text' },
  { key: 'doj', label: 'Date of Joining', letter: 'E', width: 120, type: 'date' },
  { key: 'bloodGroup', label: 'Blood Group', letter: 'F', width: 100, type: 'select', options: ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'] },
  { key: 'conditions', label: 'Pre-Existing Conditions', letter: 'G', width: 180, type: 'text' },
  { key: 'allergies', label: 'Allergies', letter: 'H', width: 120, type: 'text' },
  { key: 'emergency', label: 'Emergency Contact', letter: 'I', width: 140, type: 'text' },
  { key: 'lastExam', label: 'Last Medical Exam', letter: 'J', width: 120, type: 'date' },
  { key: 'status', label: 'Fitness Status', letter: 'K', width: 120, type: 'status', options: ['Fit', 'Unfit', 'Conditional'] }
    `,
    data: `
  { id: 'EMP-001', name: 'Rajesh Kumar', department: 'Blast Furnace', designation: 'Operator', doj: '2020-01-15', bloodGroup: 'B+', conditions: 'None', allergies: 'None', emergency: '9876543210', lastExam: '2023-11-10', status: 'Fit' },
  { id: 'EMP-002', name: 'Suresh Yadav', department: 'Rolling Mill', designation: 'Technician', doj: '2019-05-20', bloodGroup: 'O+', conditions: 'Asthma', allergies: 'Dust', emergency: '9876543211', lastExam: '2023-10-05', status: 'Conditional' }
    `
  },
  {
    name: 'AnnualHealthCheckup',
    title: 'Annual Health Checkup',
    prefix: 'AHC-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'empId', label: 'Emp ID', letter: 'B', width: 100, type: 'text' },
  { key: 'empName', label: 'Employee Name', letter: 'C', width: 160, type: 'text' },
  { key: 'department', label: 'Department', letter: 'D', width: 140, type: 'text' },
  { key: 'checkupDate', label: 'Checkup Date', letter: 'E', width: 120, type: 'date' },
  { key: 'nextDueDate', label: 'Next Due Date', letter: 'F', width: 120, type: 'date' },
  { key: 'vision', label: 'Vision Test', letter: 'G', width: 100, type: 'select', options: ['Pass', 'Fail'] },
  { key: 'hearing', label: 'Hearing Test', letter: 'H', width: 100, type: 'select', options: ['Pass', 'Fail'] },
  { key: 'lung', label: 'Lung Function', letter: 'I', width: 120, type: 'select', options: ['Normal', 'Abnormal'] },
  { key: 'blood', label: 'Blood Test', letter: 'J', width: 100, type: 'select', options: ['Normal', 'Abnormal'] },
  { key: 'xray', label: 'X-Ray', letter: 'K', width: 100, type: 'select', options: ['Normal', 'Abnormal'] },
  { key: 'status', label: 'Overall Status', letter: 'L', width: 120, type: 'status', options: ['Fit', 'Unfit', 'Review'] }
    `,
    data: `
  { id: 'AHC-001', empId: 'EMP-001', empName: 'Rajesh Kumar', department: 'Blast Furnace', checkupDate: '2023-11-10', nextDueDate: '2024-11-10', vision: 'Pass', hearing: 'Pass', lung: 'Normal', blood: 'Normal', xray: 'Normal', status: 'Fit' }
    `
  },
  {
    name: 'VaccinationRecords',
    title: 'Vaccination Records',
    prefix: 'VAC-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'empId', label: 'Emp ID', letter: 'B', width: 100, type: 'text' },
  { key: 'empName', label: 'Employee Name', letter: 'C', width: 160, type: 'text' },
  { key: 'vaccine', label: 'Vaccine Name', letter: 'D', width: 140, type: 'select', options: ['Tetanus', 'Hepatitis B', 'COVID-19', 'Typhoid'] },
  { key: 'dose', label: 'Dose No.', letter: 'E', width: 80, type: 'number' },
  { key: 'dateAdmin', label: 'Date Administered', letter: 'F', width: 140, type: 'date' },
  { key: 'nextDose', label: 'Next Dose Due', letter: 'G', width: 120, type: 'date' },
  { key: 'adminBy', label: 'Administered By', letter: 'H', width: 140, type: 'text' },
  { key: 'status', label: 'Status', letter: 'I', width: 120, type: 'status', options: ['Complete', 'Pending', 'Overdue'] }
    `,
    data: `
  { id: 'VAC-001', empId: 'EMP-001', empName: 'Rajesh Kumar', vaccine: 'Tetanus', dose: 1, dateAdmin: '2024-01-10', nextDose: '2029-01-10', adminBy: 'Nurse Alice', status: 'Complete' }
    `
  },
  {
    name: 'ShiftHealthReport',
    title: 'Shift Health Report',
    prefix: 'SHF-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'date', label: 'Date', letter: 'B', width: 120, type: 'date' },
  { key: 'shift', label: 'Shift', letter: 'C', width: 120, type: 'select', options: ['A Shift', 'B Shift', 'C Shift', 'General'] },
  { key: 'patients', label: 'Total Patients', letter: 'D', width: 120, type: 'number' },
  { key: 'minor', label: 'Minor Injuries', letter: 'E', width: 120, type: 'number' },
  { key: 'major', label: 'Major Injuries', letter: 'F', width: 120, type: 'number' },
  { key: 'nurse', label: 'Nurse on Duty', letter: 'G', width: 140, type: 'text' },
  { key: 'doctor', label: 'Doctor on Duty', letter: 'H', width: 140, type: 'text' },
  { key: 'notes', label: 'Handover Notes', letter: 'I', width: 200, type: 'text' }
    `,
    data: `
  { id: 'SHF-001', date: '2024-06-09', shift: 'A Shift', patients: 15, minor: 2, major: 0, nurse: 'Nurse Alice', doctor: 'Dr. Sharma', notes: 'Quiet shift' }
    `
  },
  {
    name: 'EmergencyAmbulanceLog',
    title: 'Emergency Ambulance Log',
    prefix: 'AMB-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'dateTime', label: 'Date & Time', letter: 'B', width: 140, type: 'date' },
  { key: 'patientName', label: 'Patient Name', letter: 'C', width: 160, type: 'text' },
  { key: 'nature', label: 'Nature of Emergency', letter: 'D', width: 160, type: 'text' },
  { key: 'location', label: 'Location', letter: 'E', width: 140, type: 'text' },
  { key: 'ambulance', label: 'Ambulance No.', letter: 'F', width: 120, type: 'text' },
  { key: 'referredTo', label: 'Referred To', letter: 'G', width: 160, type: 'text' },
  { key: 'status', label: 'Status', letter: 'H', width: 120, type: 'status', options: ['Dispatched', 'In Transit', 'Completed', 'Cancelled'] }
    `,
    data: `
  { id: 'AMB-001', dateTime: '2024-06-08', patientName: 'Suresh Yadav', nature: 'Chemical Burns', location: 'Coke Oven', ambulance: 'AMB-01', referredTo: 'City Hospital', status: 'Completed' }
    `
  },
  {
    name: 'PPEComplianceTracker',
    title: 'PPE Compliance Tracker',
    prefix: 'PPE-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'empName', label: 'Employee Name', letter: 'B', width: 160, type: 'text' },
  { key: 'department', label: 'Department', letter: 'C', width: 140, type: 'text' },
  { key: 'ppeType', label: 'PPE Type', letter: 'D', width: 140, type: 'text' },
  { key: 'issueDate', label: 'Issue Date', letter: 'E', width: 120, type: 'date' },
  { key: 'status', label: 'Condition Status', letter: 'F', width: 140, type: 'status', options: ['Good', 'Fair', 'Replace'] }
    `,
    data: `
  { id: 'PPE-001', empName: 'Rajesh Kumar', department: 'Blast Furnace', ppeType: 'Safety Helmet', issueDate: '2023-01-15', status: 'Good' }
    `
  },
  {
    name: 'BioMedicalWasteLog',
    title: 'Bio-Medical Waste Log',
    prefix: 'BMW-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'date', label: 'Date', letter: 'B', width: 120, type: 'date' },
  { key: 'category', label: 'Waste Category', letter: 'C', width: 140, type: 'select', options: ['Yellow (Anatomical)', 'Red (Plastics)', 'White (Sharps)', 'Blue (Glass)'] },
  { key: 'weight', label: 'Weight (kg)', letter: 'D', width: 100, type: 'number' },
  { key: 'handedTo', label: 'Handed Over To', letter: 'E', width: 160, type: 'text' },
  { key: 'status', label: 'Disposal Status', letter: 'F', width: 140, type: 'status', options: ['Pending', 'Completed'] }
    `,
    data: `
  { id: 'BMW-001', date: '2024-06-09', category: 'Red (Plastics)', weight: 2.5, handedTo: 'Enviro Waste Mgmt', status: 'Completed' }
    `
  },
  {
    name: 'HealthCertificateTracker',
    title: 'Health Certificate Tracker',
    prefix: 'HC-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'empName', label: 'Employee Name', letter: 'B', width: 160, type: 'text' },
  { key: 'certType', label: 'Certificate Type', letter: 'C', width: 160, type: 'text' },
  { key: 'issueDate', label: 'Issue Date', letter: 'D', width: 120, type: 'date' },
  { key: 'validUntil', label: 'Valid Until', letter: 'E', width: 120, type: 'date' },
  { key: 'status', label: 'Validity Status', letter: 'F', width: 120, type: 'status', options: ['Active', 'Expired'] }
    `,
    data: `
  { id: 'HC-001', empName: 'Rajesh Kumar', certType: 'Food Handler', issueDate: '2024-01-01', validUntil: '2025-01-01', status: 'Active' }
    `
  },
  {
    name: 'OccupationalDiseaseRegistry',
    title: 'Occupational Disease Registry',
    prefix: 'ODR-',
    columns: `
  { key: 'id', label: 'ID', letter: 'A', width: 80, type: 'text' },
  { key: 'empName', label: 'Employee Name', letter: 'B', width: 160, type: 'text' },
  { key: 'department', label: 'Department', letter: 'C', width: 140, type: 'text' },
  { key: 'disease', label: 'Disease Diagnosed', letter: 'D', width: 160, type: 'text' },
  { key: 'dateDiagnosed', label: 'Date Diagnosed', letter: 'E', width: 140, type: 'date' },
  { key: 'status', label: 'Current Status', letter: 'F', width: 120, type: 'status', options: ['Active', 'Recovered', 'Chronic'] }
    `,
    data: `
  { id: 'ODR-001', empName: 'Priya Sharma', department: 'Rolling Mill', disease: 'Noise-Induced Hearing Loss', dateDiagnosed: '2024-06-07', status: 'Chronic' }
    `
  }
];

components.forEach(comp => {
  const content = \`import React from 'react';
import ExcelGrid from './ExcelGrid';

const initialData = [
\${comp.data}
];

const columns = [
\${comp.columns}
];
\${comp.extra || ''}
const \${comp.name} = () => {
  return (
    <div className="animate-fade-in" style={{ height: 'calc(100vh - 120px)' }}>
      <ExcelGrid 
        title="\${comp.title}"
        storageKey="cms_\${comp.name.toLowerCase()}_data"
        initialData={initialData}
        columns={columns}
        idPrefix="\${comp.prefix}"
        \${comp.extra ? (comp.extra.includes('getRowStyle') ? 'getRowStyle={getRowStyle}' : 'getCustomCellContent={getCustomCellContent}') : ''}
      />
    </div>
  );
};

export default \${comp.name};
\`;

  fs.writeFileSync(path.join(__dirname, 'src', 'components', 'clinical', \`\${comp.name}.jsx\`), content);
});

console.log('Refactoring complete!');
