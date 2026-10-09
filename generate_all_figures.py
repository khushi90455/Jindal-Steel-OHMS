"""
Generate all technical diagrams for JSPulse OHMS Internship Report.
Produces high-resolution PNG images (300 DPI, A4-friendly, white background).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figures')
DPI = 300
BG = 'white'

# Color palette
C_MAIN    = '#1a73e8'   # Blue
C_RENDER  = '#34a853'   # Green
C_IPC     = '#ea4335'   # Red
C_DB      = '#fbbc04'   # Yellow/Gold
C_DARK    = '#202124'   # Dark
C_LIGHT   = '#f8f9fa'   # Light gray
C_PURPLE  = '#9334e8'   # Purple
C_ORANGE  = '#ff6d01'   # Orange
C_TEAL    = '#00897b'   # Teal

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG, edgecolor='none', pad_inches=0.3)
    plt.close(fig)
    print(f"  Saved: {name}")

def draw_box(ax, x, y, w, h, text, color, fontsize=9, textcolor='white', style='round,pad=0.02'):
    box = FancyBboxPatch((x, y), w, h, boxstyle=style, facecolor=color, edgecolor='#333333', linewidth=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, color=textcolor, fontweight='bold', wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, color='#555555', style='->', lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))

def draw_label(ax, x1, y1, x2, y2, label, color='#555555'):
    mx, my = (x1+x2)/2, (y1+y2)/2
    ax.text(mx, my+0.02, label, ha='center', va='bottom', fontsize=7, color=color, fontstyle='italic')


# ═══════════════════════════════════════════════
# FIGURE 2.1: High-Level Electron System Architecture
# ═══════════════════════════════════════════════
def fig_2_1():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 2.1: High-Level Electron System Architecture\n& Secure IPC Context Bridge Flow', fontsize=13, fontweight='bold', pad=15)

    # Main Process
    draw_box(ax, 0.02, 0.55, 0.28, 0.38, '', C_MAIN+'22', style='round,pad=0.02', textcolor=C_DARK)
    ax.text(0.16, 0.90, 'MAIN PROCESS', ha='center', fontsize=11, fontweight='bold', color=C_MAIN)
    ax.text(0.16, 0.85, '(Node.js Runtime)', ha='center', fontsize=8, color='#555555')
    draw_box(ax, 0.05, 0.72, 0.22, 0.08, 'BrowserWindow\nManager', C_MAIN, fontsize=8)
    draw_box(ax, 0.05, 0.60, 0.22, 0.08, 'File System I/O\n& Dialog APIs', C_MAIN, fontsize=8)

    # Context Bridge (center)
    draw_box(ax, 0.36, 0.58, 0.28, 0.32, '', C_IPC+'22', style='round,pad=0.02', textcolor=C_DARK)
    ax.text(0.50, 0.87, 'CONTEXT BRIDGE', ha='center', fontsize=11, fontweight='bold', color=C_IPC)
    ax.text(0.50, 0.82, '(preload.js)', ha='center', fontsize=8, color='#555555')
    draw_box(ax, 0.39, 0.68, 0.22, 0.08, 'contextBridge\n.exposeInMainWorld', C_IPC, fontsize=7)
    draw_box(ax, 0.39, 0.60, 0.22, 0.06, 'ipcRenderer.invoke()', C_IPC, fontsize=7)

    # Renderer Process
    draw_box(ax, 0.70, 0.55, 0.28, 0.38, '', C_RENDER+'22', style='round,pad=0.02', textcolor=C_DARK)
    ax.text(0.84, 0.90, 'RENDERER PROCESS', ha='center', fontsize=11, fontweight='bold', color=C_RENDER)
    ax.text(0.84, 0.85, '(Chromium + React)', ha='center', fontsize=8, color='#555555')
    draw_box(ax, 0.73, 0.72, 0.22, 0.08, 'React Component\nTree (JSX/Vite)', C_RENDER, fontsize=8)
    draw_box(ax, 0.73, 0.60, 0.22, 0.08, 'DOM Virtualization\n& State Management', C_RENDER, fontsize=8)

    # Arrows
    draw_arrow(ax, 0.27, 0.76, 0.36, 0.72, C_IPC, lw=2)
    draw_arrow(ax, 0.64, 0.72, 0.73, 0.76, C_IPC, lw=2)
    ax.text(0.32, 0.77, 'IPC', ha='center', fontsize=7, color=C_IPC, fontweight='bold')
    ax.text(0.68, 0.77, 'IPC', ha='center', fontsize=7, color=C_IPC, fontweight='bold')

    # Storage Layer
    draw_box(ax, 0.10, 0.10, 0.22, 0.35, '', C_DB+'22', style='round,pad=0.02', textcolor=C_DARK)
    ax.text(0.21, 0.42, 'STORAGE LAYER', ha='center', fontsize=10, fontweight='bold', color='#b8860b')
    draw_box(ax, 0.13, 0.30, 0.16, 0.07, 'IndexedDB\n(sheetDB.js)', '#e8a800', fontsize=7, textcolor=C_DARK)
    draw_box(ax, 0.13, 0.20, 0.16, 0.07, 'localStorage\n(Proxy Engine)', '#e8a800', fontsize=7, textcolor=C_DARK)
    draw_box(ax, 0.13, 0.12, 0.16, 0.06, 'Native File System', '#e8a800', fontsize=7, textcolor=C_DARK)

    # UI Layer
    draw_box(ax, 0.42, 0.10, 0.22, 0.35, '', C_PURPLE+'22', style='round,pad=0.02', textcolor=C_DARK)
    ax.text(0.53, 0.42, 'UI MODULES', ha='center', fontsize=10, fontweight='bold', color=C_PURPLE)
    draw_box(ax, 0.45, 0.32, 0.16, 0.06, 'OPD Module', C_PURPLE, fontsize=7)
    draw_box(ax, 0.45, 0.24, 0.16, 0.06, 'Pharmacy Module', C_PURPLE, fontsize=7)
    draw_box(ax, 0.45, 0.16, 0.16, 0.06, 'Pathology Module', C_PURPLE, fontsize=7)
    draw_box(ax, 0.45, 0.10, 0.16, 0.05, 'Reports & Chat', C_PURPLE, fontsize=7)

    # Utility Layer
    draw_box(ax, 0.72, 0.10, 0.26, 0.35, '', C_TEAL+'22', style='round,pad=0.02', textcolor=C_DARK)
    ax.text(0.85, 0.42, 'UTILITIES', ha='center', fontsize=10, fontweight='bold', color=C_TEAL)
    draw_box(ax, 0.75, 0.32, 0.20, 0.06, 'chatBrain.js (NLP)', C_TEAL, fontsize=7)
    draw_box(ax, 0.75, 0.24, 0.20, 0.06, 'PDF Generator', C_TEAL, fontsize=7)
    draw_box(ax, 0.75, 0.16, 0.20, 0.06, 'Global Search', C_TEAL, fontsize=7)
    draw_box(ax, 0.75, 0.10, 0.20, 0.05, 'Sync Engine', C_TEAL, fontsize=7)

    # Connections
    draw_arrow(ax, 0.16, 0.55, 0.21, 0.45, '#888888', lw=1)
    draw_arrow(ax, 0.84, 0.55, 0.85, 0.45, '#888888', lw=1)
    draw_arrow(ax, 0.53, 0.55, 0.53, 0.45, '#888888', lw=1)

    save(fig, 'Figure_2_1_System_Architecture.png')


# ═══════════════════════════════════════════════
# FIGURE 3.1: Complete System Architecture
# ═══════════════════════════════════════════════
def fig_3_1():
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.1: JS Pulse OHMS Complete System Architecture\nElectron Dual-Process Model, IPC Bridge, and IndexedDB Integration', fontsize=12, fontweight='bold', pad=15)

    # User Layer
    draw_box(ax, 0.30, 0.90, 0.40, 0.07, 'USER (Doctor / Pharmacist / Admin)', '#455a64', fontsize=10)

    # Electron Shell
    r = mpatches.FancyBboxPatch((0.03, 0.10), 0.94, 0.76, boxstyle='round,pad=0.02', facecolor='#e3f2fd', edgecolor=C_MAIN, linewidth=2, linestyle='--')
    ax.add_patch(r)
    ax.text(0.50, 0.84, 'Electron Desktop Shell (Chromium + Node.js)', ha='center', fontsize=11, fontweight='bold', color=C_MAIN)

    # Main Process Column
    draw_box(ax, 0.05, 0.68, 0.25, 0.08, 'Main Process\n(main.js)', C_MAIN, fontsize=9)
    draw_box(ax, 0.05, 0.57, 0.25, 0.08, 'ipcMain.handle()\nEvent Listeners', '#1565c0', fontsize=8)
    draw_box(ax, 0.05, 0.46, 0.25, 0.08, 'BrowserWindow\n& Menu Bar', '#1565c0', fontsize=8)
    draw_box(ax, 0.05, 0.35, 0.25, 0.08, 'dialog.showSaveDialog\nNative File I/O', '#1565c0', fontsize=8)

    # Preload Bridge Column (center)
    draw_box(ax, 0.37, 0.68, 0.26, 0.08, 'Preload Script\n(preload.js)', C_IPC, fontsize=9)
    draw_box(ax, 0.37, 0.57, 0.26, 0.08, 'contextBridge\n.exposeInMainWorld()', '#c62828', fontsize=8)

    # Renderer Column
    draw_box(ax, 0.70, 0.68, 0.27, 0.08, 'Renderer Process\n(React + Vite)', C_RENDER, fontsize=9)
    draw_box(ax, 0.70, 0.57, 0.27, 0.08, 'App.jsx\nRouter & Layout', '#2e7d32', fontsize=8)
    draw_box(ax, 0.70, 0.46, 0.13, 0.08, 'OPD\nModule', '#43a047', fontsize=7)
    draw_box(ax, 0.84, 0.46, 0.13, 0.08, 'Pharmacy\nModule', '#43a047', fontsize=7)
    draw_box(ax, 0.70, 0.35, 0.13, 0.08, 'Pathology\nModule', '#43a047', fontsize=7)
    draw_box(ax, 0.84, 0.35, 0.13, 0.08, 'Reports\nModule', '#43a047', fontsize=7)

    # Storage
    draw_box(ax, 0.15, 0.14, 0.22, 0.12, 'IndexedDB\n(sheetDB.js)\nPersistent Storage', C_DB, fontsize=8, textcolor=C_DARK)
    draw_box(ax, 0.42, 0.14, 0.18, 0.12, 'localStorage\nProxy Engine\n(storage.js)', C_ORANGE, fontsize=8)
    draw_box(ax, 0.65, 0.14, 0.18, 0.12, 'chatBrain.js\nOffline NLP\nEngine', C_TEAL, fontsize=8)

    # Arrows
    draw_arrow(ax, 0.50, 0.90, 0.84, 0.76, '#555555')
    draw_arrow(ax, 0.30, 0.72, 0.37, 0.72, C_IPC, lw=2)
    draw_arrow(ax, 0.63, 0.72, 0.70, 0.72, C_IPC, lw=2)
    draw_arrow(ax, 0.50, 0.57, 0.50, 0.50, '#888888')
    ax.text(0.34, 0.73, 'IPC', fontsize=7, color=C_IPC, fontweight='bold')
    ax.text(0.66, 0.73, 'IPC', fontsize=7, color=C_IPC, fontweight='bold')

    draw_arrow(ax, 0.17, 0.35, 0.26, 0.26, '#888888')
    draw_arrow(ax, 0.84, 0.35, 0.74, 0.26, '#888888')
    draw_arrow(ax, 0.84, 0.46, 0.51, 0.26, '#888888')

    save(fig, 'Figure_3_1_System_Architecture.png')


# ═══════════════════════════════════════════════
# FIGURE 3.2: Use Case Diagram
# ═══════════════════════════════════════════════
def fig_3_2():
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.2: JS Pulse OHMS Use Case Diagram\nActors and System Functions', fontsize=13, fontweight='bold', pad=15)

    # System boundary
    r = mpatches.FancyBboxPatch((0.22, 0.05), 0.56, 0.88, boxstyle='round,pad=0.02', facecolor='#f5f5f5', edgecolor='#333333', linewidth=2)
    ax.add_patch(r)
    ax.text(0.50, 0.91, 'JS Pulse OHMS System', ha='center', fontsize=12, fontweight='bold', color=C_DARK)

    # Actors (left side)
    actors_left = [('Doctor', 0.08, 0.78), ('Pharmacist', 0.08, 0.45)]
    actors_right = [('Lab Tech', 0.88, 0.78), ('Admin', 0.88, 0.45)]

    for name, x, y in actors_left + actors_right:
        # Stick figure
        ax.plot(x, y+0.06, 'o', color=C_MAIN, markersize=10)
        ax.plot([x, x], [y+0.04, y-0.02], color=C_MAIN, lw=2)
        ax.plot([x-0.03, x+0.03], [y+0.02, y+0.02], color=C_MAIN, lw=2)
        ax.plot([x-0.02, x, x+0.02], [y-0.06, y-0.02, y-0.06], color=C_MAIN, lw=2)
        ax.text(x, y-0.09, name, ha='center', fontsize=9, fontweight='bold', color=C_DARK)

    # Use cases (ellipses)
    use_cases = [
        ('Register Patient', 0.38, 0.82, C_MAIN),
        ('Record Vitals &\nConsultation', 0.60, 0.82, C_MAIN),
        ('Write Prescription', 0.38, 0.70, C_MAIN),
        ('Generate OPD Report', 0.60, 0.70, C_MAIN),
        ('Dispense Medicine', 0.38, 0.55, C_TEAL),
        ('Update Stock', 0.60, 0.55, C_TEAL),
        ('View Pending\nPrescriptions', 0.38, 0.42, C_TEAL),
        ('Enter Lab Results', 0.60, 0.42, C_PURPLE),
        ('Generate Monthly\nReports', 0.38, 0.28, C_ORANGE),
        ('Manage Users &\nSettings', 0.60, 0.28, C_ORANGE),
        ('Backup & Export\nData', 0.38, 0.15, C_ORANGE),
        ('AI Chat Assistant', 0.60, 0.15, C_ORANGE),
    ]

    for text, x, y, color in use_cases:
        e = mpatches.Ellipse((x, y), 0.18, 0.09, facecolor=color+'22', edgecolor=color, linewidth=1.5)
        ax.add_patch(e)
        ax.text(x, y, text, ha='center', va='center', fontsize=7, color=C_DARK, fontweight='bold')

    # Lines from actors to use cases
    for _, ux, uy, _ in use_cases[:4]:
        ax.plot([0.11, ux-0.09], [0.78, uy], color='#888888', lw=0.8)
    for _, ux, uy, _ in use_cases[4:7]:
        ax.plot([0.11, ux-0.09], [0.45, uy], color='#888888', lw=0.8)
    for _, ux, uy, _ in use_cases[7:8]:
        ax.plot([0.85, ux+0.09], [0.78, uy], color='#888888', lw=0.8)
    for _, ux, uy, _ in use_cases[8:]:
        ax.plot([0.85, ux+0.09], [0.45, uy], color='#888888', lw=0.8)

    save(fig, 'Figure_3_2_Use_Case_Diagram.png')


# ═══════════════════════════════════════════════
# FIGURE 3.3: Activity Diagram - Patient Clinical Journey
# ═══════════════════════════════════════════════
def fig_3_3():
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.3: Patient Clinical Journey Activity Diagram', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('●', 0.50, 0.95, '#333333', 0.03),
        ('Patient Arrives\nat OPD Counter', 0.50, 0.89, C_MAIN, 0.06),
        ('Search/Register\nPatient Record', 0.50, 0.81, C_MAIN, 0.06),
        ('Record Vital Signs\n(BP, Temp, SpO2)', 0.50, 0.73, C_MAIN, 0.06),
        ('◇ New Patient?', 0.50, 0.65, C_DB, 0.04),
        ('Create New Record\nin IndexedDB', 0.25, 0.58, C_TEAL, 0.05),
        ('Load Existing\nHistory', 0.75, 0.58, C_TEAL, 0.05),
        ('Doctor Consultation\n& Diagnosis Entry', 0.50, 0.50, C_MAIN, 0.06),
        ('Write Prescription\n(Medicine + Dosage)', 0.50, 0.42, C_MAIN, 0.06),
        ('◇ Lab Tests\nRequired?', 0.50, 0.34, C_DB, 0.04),
        ('Send to Pathology\nLab Module', 0.25, 0.27, C_PURPLE, 0.05),
        ('Auto-Sync to\nPharmacy Queue', 0.50, 0.22, C_TEAL, 0.06),
        ('Dispense Medicines\n& Update Stock', 0.50, 0.14, C_ORANGE, 0.06),
        ('Generate Visit\nSummary PDF', 0.50, 0.06, C_MAIN, 0.05),
    ]

    for text, x, y, color, h in steps:
        if text == '●':
            ax.plot(x, y, 'o', color=color, markersize=15)
        elif text.startswith('◇'):
            diamond = plt.Polygon([(x, y+h), (x+0.08, y), (x, y-h), (x-0.08, y)], facecolor=color+'33', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=7, fontweight='bold', color=C_DARK)
        else:
            draw_box(ax, x-0.10, y-h/2, 0.20, h, text, color, fontsize=7)

    # Arrows (main flow)
    arrows = [(0.50,0.93,0.50,0.92), (0.50,0.86,0.50,0.84), (0.50,0.78,0.50,0.76),
              (0.50,0.70,0.50,0.69), (0.50,0.61,0.50,0.56),
              (0.42,0.65,0.35,0.60), (0.58,0.65,0.65,0.60),
              (0.25,0.53,0.40,0.50), (0.75,0.53,0.60,0.50),
              (0.50,0.47,0.50,0.45), (0.50,0.39,0.50,0.38),
              (0.50,0.30,0.50,0.28), (0.42,0.34,0.35,0.29),
              (0.25,0.22,0.40,0.22),
              (0.50,0.19,0.50,0.17), (0.50,0.11,0.50,0.09)]

    for x1,y1,x2,y2 in arrows:
        draw_arrow(ax, x1, y1, x2, y2, '#555555', lw=1.5)

    # Decision labels
    ax.text(0.35, 0.66, 'Yes', fontsize=7, color=C_TEAL, fontweight='bold')
    ax.text(0.63, 0.66, 'No', fontsize=7, color=C_TEAL, fontweight='bold')
    ax.text(0.35, 0.35, 'Yes', fontsize=7, color=C_PURPLE, fontweight='bold')
    ax.text(0.55, 0.31, 'No', fontsize=7, color='#888888', fontweight='bold')

    save(fig, 'Figure_3_3_Activity_Diagram.png')


# ═══════════════════════════════════════════════
# FIGURE 3.4: Sequence Diagram - Electron IPC
# ═══════════════════════════════════════════════
def fig_3_4():
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.4: Electron IPC Communication Sequence Diagram\nHeadless PDF Print Transaction', fontsize=12, fontweight='bold', pad=15)

    # Lifeline participants
    parts = [
        ('User\n(Click)', 0.08, C_DARK),
        ('React\nComponent', 0.22, C_RENDER),
        ('preload.js\n(Bridge)', 0.38, C_IPC),
        ('ipcMain\n(main.js)', 0.54, C_MAIN),
        ('BrowserWindow\n(Hidden)', 0.70, C_PURPLE),
        ('File System\n(dialog)', 0.86, C_ORANGE),
    ]

    for name, x, color in parts:
        draw_box(ax, x-0.06, 0.90, 0.12, 0.07, name, color, fontsize=7)
        ax.plot([x, x], [0.90, 0.08], color='#cccccc', lw=1, linestyle='--')

    # Messages
    msgs = [
        (0.08, 0.85, 0.22, 0.85, '1: onClick(printPDF)', C_DARK),
        (0.22, 0.80, 0.38, 0.80, '2: window.electronAPI\n   .printReport(data)', C_RENDER),
        (0.38, 0.74, 0.54, 0.74, '3: ipcRenderer.invoke\n   ("print-pdf", data)', C_IPC),
        (0.54, 0.67, 0.70, 0.67, '4: new BrowserWindow\n   ({show:false})', C_MAIN),
        (0.70, 0.61, 0.54, 0.61, '5: loadURL(reportHTML)', C_PURPLE),
        (0.54, 0.55, 0.70, 0.55, '6: webContents\n   .printToPDF()', C_MAIN),
        (0.70, 0.48, 0.54, 0.48, '7: pdfBuffer', C_PURPLE),
        (0.54, 0.42, 0.86, 0.42, '8: dialog.showSaveDialog()', C_MAIN),
        (0.86, 0.36, 0.54, 0.36, '9: filePath', C_ORANGE),
        (0.54, 0.30, 0.86, 0.30, '10: fs.writeFile\n    (path, buffer)', C_MAIN),
        (0.86, 0.24, 0.54, 0.24, '11: success', C_ORANGE),
        (0.54, 0.18, 0.38, 0.18, '12: resolve(filePath)', C_MAIN),
        (0.38, 0.13, 0.22, 0.13, '13: Promise resolved', C_IPC),
        (0.22, 0.09, 0.08, 0.09, '14: Show success toast', C_RENDER),
    ]

    for x1, y1, x2, y2, label, color in msgs:
        draw_arrow(ax, x1, y1, x2, y2, color, lw=1.5)
        mx = (x1+x2)/2
        ax.text(mx, y1+0.02, label, ha='center', va='bottom', fontsize=6, color=color, fontweight='bold')

    save(fig, 'Figure_3_4_Sequence_Diagram.png')


# ═══════════════════════════════════════════════
# FIGURE 3.5a & 3.5b: Electron App Lifecycle
# ═══════════════════════════════════════════════
def fig_3_5a():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.5(a): Electron App Lifecycle\nMain Process Boot Sequence', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('app.exe Launched', 0.50, 0.92, C_DARK, 0.18),
        ('app.whenReady()', 0.50, 0.83, C_MAIN, 0.18),
        ('Create BrowserWindow\n{width:1280, height:800}', 0.50, 0.73, C_MAIN, 0.22),
        ('Inject preload.js\n(contextIsolation: true)', 0.50, 0.63, C_IPC, 0.22),
        ('Register ipcMain\nHandlers', 0.50, 0.53, C_MAIN, 0.18),
        ('win.loadURL()\nor loadFile()', 0.50, 0.43, C_MAIN, 0.18),
        ('Chromium Renderer\nProcess Spawned', 0.50, 0.33, C_RENDER, 0.20),
        ('contextBridge\n.exposeInMainWorld()', 0.50, 0.23, C_IPC, 0.22),
        ('React App Mount\n<App /> → DOM', 0.50, 0.13, C_RENDER, 0.18),
    ]

    for text, x, y, color, w in steps:
        draw_box(ax, x-w/2, y-0.035, w, 0.07, text, color, fontsize=8)

    for i in range(len(steps)-1):
        draw_arrow(ax, 0.50, steps[i][2]-0.035, 0.50, steps[i+1][2]+0.035, '#555555', lw=1.5)

    save(fig, 'Figure_3_5a_Electron_Lifecycle_Boot.png')

def fig_3_5b():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.5(b): Electron App Lifecycle\nDB Connection and Dashboard Mount', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('React App Mounted', 0.50, 0.92, C_RENDER, 0.18),
        ('useEffect() →\nInitialize Storage', 0.50, 0.82, C_RENDER, 0.20),
        ('sheetDB.getDB()\nOpen IndexedDB Connection', 0.50, 0.72, C_DB, 0.24),
        ('◇ DB Version\nCheck', 0.50, 0.62, '#888888', 0.15),
        ('Run onupgradeneeded\nCreate Object Stores', 0.20, 0.52, C_TEAL, 0.22),
        ('Load Existing\nData', 0.80, 0.52, C_MAIN, 0.18),
        ('Hydrate React State\nfrom IndexedDB', 0.50, 0.42, C_RENDER, 0.22),
        ('Check localStorage\nMigration Needed?', 0.50, 0.32, C_ORANGE, 0.22),
        ('Render Dashboard\nwith Patient Counts', 0.50, 0.22, C_MAIN, 0.22),
        ('App Ready ✓', 0.50, 0.12, C_RENDER, 0.16),
    ]

    for text, x, y, color, w in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.04), (x+0.08, y), (x, y-0.04), (x-0.08, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=7, fontweight='bold')
        else:
            draw_box(ax, x-w/2, y-0.035, w, 0.07, text, color, fontsize=8)

    # Main flow arrows
    for i in range(3):
        draw_arrow(ax, 0.50, steps[i][2]-0.035, 0.50, steps[i+1][2]+0.04, '#555555', lw=1.5)

    # Diamond branches
    draw_arrow(ax, 0.42, 0.62, 0.31, 0.555, '#555555')
    draw_arrow(ax, 0.58, 0.62, 0.71, 0.555, '#555555')
    ax.text(0.37, 0.60, 'New', fontsize=7, color=C_TEAL, fontweight='bold')
    ax.text(0.60, 0.60, 'Exists', fontsize=7, color=C_MAIN, fontweight='bold')

    draw_arrow(ax, 0.20, 0.485, 0.40, 0.455, '#555555')
    draw_arrow(ax, 0.80, 0.485, 0.60, 0.455, '#555555')

    for i in range(6, len(steps)-1):
        draw_arrow(ax, 0.50, steps[i][2]-0.035, 0.50, steps[i+1][2]+0.035, '#555555', lw=1.5)

    save(fig, 'Figure_3_5b_Electron_Lifecycle_DB.png')


# ═══════════════════════════════════════════════
# FIGURE 3.6a & 3.6b: IndexedDB Data Flow
# ═══════════════════════════════════════════════
def fig_3_6a():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.6(a): IndexedDB Migration Hook\nand Storage Quota Evaluation', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('App Startup\nTrigger Migration Check', 0.50, 0.92, C_MAIN),
        ('Scan localStorage Keys\nwith cms_ prefix', 0.50, 0.80, C_TEAL),
        ('Calculate Total Byte Size\nnew Blob([JSON]).size', 0.50, 0.68, C_ORANGE),
        ('◇ Size > 4.5 MB\nQuota Threshold?', 0.50, 0.56, '#888888'),
        ('Trigger Migration\nto IndexedDB', 0.25, 0.44, C_IPC),
        ('Continue Using\nlocalStorage', 0.75, 0.44, C_RENDER),
        ('Group Keys by\nModule Category', 0.25, 0.32, C_PURPLE),
        ('Create Batch Write\nTransaction', 0.25, 0.20, C_DB),
        ('Log Migration\nStatus Report', 0.25, 0.08, C_MAIN),
    ]

    for text, x, y, color in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.05), (x+0.10, y), (x, y-0.05), (x-0.10, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=7, fontweight='bold')
        else:
            draw_box(ax, x-0.12, y-0.04, 0.24, 0.08, text, color, fontsize=8)

    pairs = [(0,1),(1,2)]
    for a,b in pairs:
        draw_arrow(ax, 0.50, steps[a][2]-0.04, 0.50, steps[b][2]+0.04, '#555555', lw=1.5)
    draw_arrow(ax, 0.50, steps[2][2]-0.04, 0.50, steps[3][2]+0.05, '#555555', lw=1.5)
    draw_arrow(ax, 0.40, 0.56, 0.37, 0.48, '#555555')
    draw_arrow(ax, 0.60, 0.56, 0.63, 0.48, '#555555')
    ax.text(0.36, 0.55, 'Yes', fontsize=7, color=C_IPC, fontweight='bold')
    ax.text(0.62, 0.55, 'No', fontsize=7, color=C_RENDER, fontweight='bold')
    draw_arrow(ax, 0.25, 0.40, 0.25, 0.36, '#555555', lw=1.5)
    draw_arrow(ax, 0.25, 0.28, 0.25, 0.24, '#555555', lw=1.5)
    draw_arrow(ax, 0.25, 0.16, 0.25, 0.12, '#555555', lw=1.5)

    save(fig, 'Figure_3_6a_IndexedDB_Migration.png')

def fig_3_6b():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.6(b): IndexedDB Batch Write Execution\nand Legacy Data Purge', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('Begin Batch Write\nTransaction', 0.50, 0.92, C_MAIN),
        ('For Each Key Group:\nPut Data to ObjectStore', 0.50, 0.80, C_DB),
        ('Await transaction\n.oncomplete', 0.50, 0.68, C_TEAL),
        ('◇ Write\nSuccessful?', 0.50, 0.56, '#888888'),
        ('Verify Written Records\nRead-back Validation', 0.25, 0.44, C_RENDER),
        ('Emergency JSON\nFallback Export', 0.75, 0.44, C_IPC),
        ('Purge Legacy\nlocalStorage Keys', 0.25, 0.32, C_ORANGE),
        ('Log Migration\nComplete ✓', 0.25, 0.20, C_RENDER),
        ('fs.writeFile()\nbackup.json', 0.75, 0.32, C_PURPLE),
    ]

    for text, x, y, color in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.05), (x+0.10, y), (x, y-0.05), (x-0.10, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=7, fontweight='bold')
        else:
            draw_box(ax, x-0.12, y-0.04, 0.24, 0.08, text, color, fontsize=8)

    draw_arrow(ax, 0.50, 0.88, 0.50, 0.84, '#555555', lw=1.5)
    draw_arrow(ax, 0.50, 0.76, 0.50, 0.72, '#555555', lw=1.5)
    draw_arrow(ax, 0.50, 0.64, 0.50, 0.61, '#555555', lw=1.5)
    draw_arrow(ax, 0.40, 0.56, 0.37, 0.48, '#555555')
    draw_arrow(ax, 0.60, 0.56, 0.63, 0.48, '#555555')
    ax.text(0.36, 0.55, 'Yes', fontsize=7, color=C_RENDER, fontweight='bold')
    ax.text(0.62, 0.55, 'No', fontsize=7, color=C_IPC, fontweight='bold')
    draw_arrow(ax, 0.25, 0.40, 0.25, 0.36, '#555555', lw=1.5)
    draw_arrow(ax, 0.25, 0.28, 0.25, 0.24, '#555555', lw=1.5)
    draw_arrow(ax, 0.75, 0.40, 0.75, 0.36, '#555555', lw=1.5)

    save(fig, 'Figure_3_6b_IndexedDB_Batch_Write.png')


# ═══════════════════════════════════════════════
# FIGURE 3.7: ER Diagram
# ═══════════════════════════════════════════════
def fig_3_7():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.7: Entity-Relationship (ER) Diagram\nPATIENT_VISITS, DISPENSE_LOG, and MED_STOCK Entities', fontsize=13, fontweight='bold', pad=15)

    # PATIENT_VISITS entity
    draw_box(ax, 0.02, 0.55, 0.28, 0.07, 'PATIENT_VISITS', C_MAIN, fontsize=10)
    attrs_pv = ['PK: visitId (auto)', 'employeeCode', 'patientName', 'department',
                'visitDate', 'vitalSigns (JSON)', 'diagnosis', 'prescription (JSON)',
                'followUpDate', 'createdAt']
    for i, attr in enumerate(attrs_pv):
        y = 0.50 - i*0.04
        style = 'bold' if 'PK' in attr else 'normal'
        color = C_MAIN if 'PK' in attr else '#333333'
        ax.text(0.16, y, attr, ha='center', fontsize=7, fontweight=style, color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#e3f2fd', edgecolor='#90caf9', linewidth=0.5))

    # DISPENSE_LOG entity
    draw_box(ax, 0.36, 0.55, 0.28, 0.07, 'DISPENSE_LOG', C_TEAL, fontsize=10)
    attrs_dl = ['PK: dispenseId (auto)', 'FK: visitId → PATIENT_VISITS', 'employeeCode',
                'medicines (JSON Array)', 'dispensedBy', 'dispensedAt',
                'status (pending/done)', 'notes']
    for i, attr in enumerate(attrs_dl):
        y = 0.50 - i*0.04
        style = 'bold' if 'PK' in attr or 'FK' in attr else 'normal'
        color = C_TEAL if 'PK' in attr else (C_IPC if 'FK' in attr else '#333333')
        ax.text(0.50, y, attr, ha='center', fontsize=7, fontweight=style, color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#e0f2f1', edgecolor='#80cbc4', linewidth=0.5))

    # MED_STOCK entity
    draw_box(ax, 0.70, 0.55, 0.28, 0.07, 'MED_STOCK', C_ORANGE, fontsize=10)
    attrs_ms = ['PK: medicineId (auto)', 'medicineName', 'genericName',
                'category', 'currentStock (int)', 'unit (tabs/ml/caps)',
                'expiryDate', 'batchNumber', 'lastUpdated']
    for i, attr in enumerate(attrs_ms):
        y = 0.50 - i*0.04
        style = 'bold' if 'PK' in attr else 'normal'
        color = C_ORANGE if 'PK' in attr else '#333333'
        ax.text(0.84, y, attr, ha='center', fontsize=7, fontweight=style, color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#fff3e0', edgecolor='#ffcc80', linewidth=0.5))

    # Relationships
    ax.annotate('', xy=(0.36, 0.58), xytext=(0.30, 0.58),
                arrowprops=dict(arrowstyle='->', color=C_IPC, lw=2))
    ax.text(0.33, 0.60, '1 : N', ha='center', fontsize=8, fontweight='bold', color=C_IPC)

    ax.annotate('', xy=(0.70, 0.58), xytext=(0.64, 0.58),
                arrowprops=dict(arrowstyle='->', color=C_IPC, lw=2))
    ax.text(0.67, 0.60, 'N : 1', ha='center', fontsize=8, fontweight='bold', color=C_IPC)

    # Legend
    ax.text(0.50, 0.08, 'Relationships: PATIENT_VISITS 1:N → DISPENSE_LOG N:1 → MED_STOCK',
            ha='center', fontsize=9, fontweight='bold', color='#555555',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f5f5f5', edgecolor='#cccccc'))

    save(fig, 'Figure_3_7_ER_Diagram.png')


# ═══════════════════════════════════════════════
# FIGURE 3.8: localStorage Proxy Engine
# ═══════════════════════════════════════════════
def fig_3_8():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 3.8: localStorage Proxy Engine\nData Interception and Multi-Tier Routing Flow', fontsize=13, fontweight='bold', pad=15)

    # Source
    draw_box(ax, 0.35, 0.88, 0.30, 0.07, 'React Component\nsetItem(key, value)', C_RENDER, fontsize=9)

    # Proxy
    draw_box(ax, 0.30, 0.72, 0.40, 0.08, 'localStorage Proxy Engine\n(storage.js – Proxy Handler)', C_IPC, fontsize=9)

    # Three tiers
    draw_box(ax, 0.05, 0.50, 0.25, 0.12, 'Tier 1: In-Memory Map\n(Instant Read/Write)\nMap<string, string>', C_MAIN, fontsize=8)
    draw_box(ax, 0.37, 0.50, 0.26, 0.12, 'Tier 2: localStorage\n(Browser Persistent)\n5MB Quota Limit', C_ORANGE, fontsize=8)
    draw_box(ax, 0.70, 0.50, 0.26, 0.12, 'Tier 3: IndexedDB\n(sheetDB.js Overflow)\nUnlimited Storage', C_DB, fontsize=8, textcolor=C_DARK)

    # Read path
    draw_box(ax, 0.25, 0.28, 0.50, 0.10, 'Read Path: Memory Map → localStorage → IndexedDB\n(Cascading Fallback with Automatic Promotion)', C_TEAL, fontsize=8)

    # Write path
    draw_box(ax, 0.25, 0.12, 0.50, 0.10, 'Write Path: Synchronous Memory + localStorage\n+ Async IndexedDB Batch (Debounced 500ms)', C_PURPLE, fontsize=8)

    # Arrows
    draw_arrow(ax, 0.50, 0.88, 0.50, 0.80, '#555555', lw=2)
    draw_arrow(ax, 0.35, 0.72, 0.17, 0.62, C_MAIN, lw=1.5)
    draw_arrow(ax, 0.50, 0.72, 0.50, 0.62, C_ORANGE, lw=1.5)
    draw_arrow(ax, 0.65, 0.72, 0.83, 0.62, C_DB, lw=1.5)

    draw_arrow(ax, 0.17, 0.50, 0.35, 0.36, C_TEAL, lw=1)
    draw_arrow(ax, 0.50, 0.50, 0.50, 0.38, C_TEAL, lw=1)
    draw_arrow(ax, 0.83, 0.50, 0.65, 0.36, C_TEAL, lw=1)

    save(fig, 'Figure_3_8_LocalStorage_Proxy.png')


# ═══════════════════════════════════════════════
# FIGURE 4.1: DOM Virtualization
# ═══════════════════════════════════════════════
def fig_4_1():
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.1: DOM Viewport Virtualization\nRow Calculation Sequence Diagram', fontsize=13, fontweight='bold', pad=15)

    parts = [('User\nScroll', 0.10, C_DARK), ('onScroll\nHandler', 0.28, C_MAIN),
             ('Row\nCalculator', 0.46, C_TEAL), ('DOM\nRecycler', 0.64, C_RENDER),
             ('Virtual\nSpacers', 0.82, C_PURPLE)]
    for name, x, color in parts:
        draw_box(ax, x-0.07, 0.88, 0.14, 0.07, name, color, fontsize=8)
        ax.plot([x, x], [0.88, 0.10], color='#dddddd', lw=1, linestyle='--')

    msgs = [
        (0.10, 0.82, 0.28, 0.82, '1: scrollTop event'),
        (0.28, 0.76, 0.46, 0.76, '2: startIdx = floor(scrollTop/ROW_H)'),
        (0.46, 0.70, 0.28, 0.70, '3: endIdx = startIdx + visibleCount'),
        (0.28, 0.64, 0.64, 0.64, '4: slice(startIdx, endIdx)'),
        (0.64, 0.58, 0.82, 0.58, '5: topSpacer = startIdx × ROW_H'),
        (0.82, 0.52, 0.64, 0.52, '6: bottomSpacer = remaining × ROW_H'),
        (0.64, 0.46, 0.28, 0.46, '7: render visible rows only'),
        (0.28, 0.40, 0.46, 0.40, '8: apply key={row.id} for recycling'),
        (0.46, 0.34, 0.64, 0.34, '9: React reconciliation'),
        (0.64, 0.28, 0.10, 0.28, '10: DOM updated (O(visible) nodes)'),
    ]

    for x1, y1, x2, y2, label in msgs:
        color = C_MAIN if '1:' in label or '2:' in label else (C_TEAL if '3:' in label or '8:' in label or '9:' in label else C_RENDER)
        draw_arrow(ax, x1, y1, x2, y2, color, lw=1.2)
        mx = (x1+x2)/2
        ax.text(mx, y1+0.015, label, ha='center', va='bottom', fontsize=6.5, color='#333333', fontweight='bold')

    save(fig, 'Figure_4_1_DOM_Virtualization.png')


# ═══════════════════════════════════════════════
# FIGURE 4.2: Undo/Redo Stack
# ═══════════════════════════════════════════════
def fig_4_2():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.2: Undo/Redo State History\nStack Management Flow', fontsize=13, fontweight='bold', pad=15)

    # Current state
    draw_box(ax, 0.35, 0.85, 0.30, 0.08, 'User Edits Cell\n(onChange Event)', C_MAIN, fontsize=9)

    # Deep clone
    draw_box(ax, 0.35, 0.72, 0.30, 0.07, 'Deep Clone Current State\nJSON.parse(JSON.stringify())', C_TEAL, fontsize=8)

    draw_arrow(ax, 0.50, 0.85, 0.50, 0.79, '#555555', lw=1.5)
    draw_arrow(ax, 0.50, 0.72, 0.50, 0.67, '#555555', lw=1.5)

    # Decision
    diamond = plt.Polygon([(0.50, 0.67), (0.62, 0.60), (0.50, 0.53), (0.38, 0.60)],
                          facecolor='#fff9c4', edgecolor='#f9a825', linewidth=1.5)
    ax.add_patch(diamond)
    ax.text(0.50, 0.60, 'History\n> 30?', ha='center', va='center', fontsize=8, fontweight='bold')

    # Yes - shift
    draw_box(ax, 0.08, 0.50, 0.22, 0.07, 'Shift() Oldest Entry\n(FIFO Cap at 30)', C_ORANGE, fontsize=8)
    draw_arrow(ax, 0.38, 0.58, 0.30, 0.55, '#555555')
    ax.text(0.33, 0.59, 'Yes', fontsize=7, fontweight='bold', color=C_ORANGE)

    # No - push
    draw_box(ax, 0.68, 0.50, 0.22, 0.07, 'Push Clone to\nUndo Stack', C_RENDER, fontsize=8)
    draw_arrow(ax, 0.62, 0.58, 0.68, 0.55, '#555555')
    ax.text(0.65, 0.59, 'No', fontsize=7, fontweight='bold', color=C_RENDER)

    # Clear redo
    draw_box(ax, 0.35, 0.38, 0.30, 0.07, 'Clear Redo Stack\n(New Branch)', C_IPC, fontsize=8)
    draw_arrow(ax, 0.19, 0.50, 0.35, 0.42, '#555555')
    draw_arrow(ax, 0.79, 0.50, 0.65, 0.42, '#555555')

    # Undo operation
    draw_box(ax, 0.05, 0.20, 0.22, 0.10, 'UNDO (Ctrl+Z)\nPop from Undo Stack\nPush to Redo Stack', C_PURPLE, fontsize=7)

    # Redo operation
    draw_box(ax, 0.73, 0.20, 0.22, 0.10, 'REDO (Ctrl+Y)\nPop from Redo Stack\nPush to Undo Stack', C_MAIN, fontsize=7)

    # Stacks visualization
    draw_box(ax, 0.33, 0.15, 0.14, 0.18, 'UNDO\nSTACK\n[S₁]\n[S₂]\n[S₃]\n...', '#e8eaf6', fontsize=7, textcolor=C_DARK)
    draw_box(ax, 0.53, 0.15, 0.14, 0.18, 'REDO\nSTACK\n[S₄]\n[S₅]\n...', '#fce4ec', fontsize=7, textcolor=C_DARK)

    draw_arrow(ax, 0.27, 0.24, 0.33, 0.24, C_PURPLE, lw=2)
    draw_arrow(ax, 0.73, 0.24, 0.67, 0.24, C_MAIN, lw=2)

    save(fig, 'Figure_4_2_Undo_Redo_Stack.png')


# ═══════════════════════════════════════════════
# FIGURE 4.3: Formula Parsing Flow
# ═══════════════════════════════════════════════
def fig_4_3():
    fig, ax = plt.subplots(1, 1, figsize=(10, 9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.3: Spreadsheet Formula Parsing\nand Recursive Evaluation Flow', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('Cell Value Starts with "="', 0.50, 0.93, C_DARK),
        ('Extract Formula String\n=SUM(A1:A10)', 0.50, 0.83, C_MAIN),
        ('◇ Contains\nSUM()?', 0.50, 0.72, '#888888'),
        ('Parse Range A1:A10\nExtract Start/End Cells', 0.20, 0.60, C_TEAL),
        ('Parse as Expression\nnew Function("return ...")', 0.80, 0.60, C_PURPLE),
        ('For Each Cell in Range:\nResolve Cell Value', 0.20, 0.48, C_MAIN),
        ('◇ Cell Has\nFormula?', 0.20, 0.36, '#888888'),
        ('Recursive Resolve\n(depth < 50)', 0.05, 0.24, C_IPC),
        ('Use Numeric Value', 0.35, 0.24, C_RENDER),
        ('Accumulate Sum', 0.20, 0.14, C_DB),
        ('Execute Function\nConstructor', 0.80, 0.48, C_PURPLE),
        ('Return Computed\nResult', 0.50, 0.04, C_RENDER),
    ]

    for text, x, y, color in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.05), (x+0.09, y), (x, y-0.05), (x-0.09, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=7, fontweight='bold')
        else:
            draw_box(ax, x-0.12, y-0.04, 0.24, 0.08, text, color, fontsize=7)

    draw_arrow(ax, 0.50, 0.89, 0.50, 0.87, '#555555', lw=1.5)
    draw_arrow(ax, 0.50, 0.79, 0.50, 0.77, '#555555', lw=1.5)
    draw_arrow(ax, 0.41, 0.72, 0.32, 0.64, '#555555')
    draw_arrow(ax, 0.59, 0.72, 0.68, 0.64, '#555555')
    ax.text(0.38, 0.73, 'Yes', fontsize=7, color=C_TEAL, fontweight='bold')
    ax.text(0.61, 0.73, 'No', fontsize=7, color=C_PURPLE, fontweight='bold')
    draw_arrow(ax, 0.20, 0.56, 0.20, 0.52, '#555555', lw=1.5)
    draw_arrow(ax, 0.20, 0.44, 0.20, 0.41, '#555555', lw=1.5)
    draw_arrow(ax, 0.11, 0.36, 0.05, 0.28, '#555555')
    draw_arrow(ax, 0.29, 0.36, 0.35, 0.28, '#555555')
    ax.text(0.10, 0.37, 'Yes', fontsize=7, color=C_IPC, fontweight='bold')
    ax.text(0.30, 0.37, 'No', fontsize=7, color=C_RENDER, fontweight='bold')
    draw_arrow(ax, 0.05, 0.20, 0.12, 0.18, '#555555')
    draw_arrow(ax, 0.35, 0.20, 0.28, 0.18, '#555555')
    draw_arrow(ax, 0.80, 0.56, 0.80, 0.52, '#555555', lw=1.5)
    draw_arrow(ax, 0.20, 0.10, 0.38, 0.08, '#555555')
    draw_arrow(ax, 0.80, 0.44, 0.62, 0.08, '#555555')

    save(fig, 'Figure_4_3_Formula_Parsing.png')


# ═══════════════════════════════════════════════
# FIGURE 4.4: ChatBrain NLP Flow
# ═══════════════════════════════════════════════
def fig_4_4():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.4: Local ChatBrain NLP Intent Classification\nand Database Query Flow', fontsize=13, fontweight='bold', pad=15)

    draw_box(ax, 0.35, 0.88, 0.30, 0.07, 'User Types Query\n"How many patients today?"', C_DARK, fontsize=8)

    draw_box(ax, 0.35, 0.76, 0.30, 0.06, '◇ Network\nAvailable?', '#888888', fontsize=8)

    draw_box(ax, 0.05, 0.62, 0.25, 0.08, 'Gemini API\n(Online Mode)\nFull NLU Pipeline', C_MAIN, fontsize=8)

    draw_box(ax, 0.68, 0.62, 0.28, 0.08, 'chatBrain.js\n(Offline Mode)\nLocal Regex Classifier', C_TEAL, fontsize=8)

    draw_box(ax, 0.68, 0.48, 0.28, 0.08, 'Tokenize Query\nLowercase + Split Words', C_ORANGE, fontsize=8)
    draw_box(ax, 0.68, 0.35, 0.28, 0.08, 'Score Against\nIntent Patterns (6 intents)', C_PURPLE, fontsize=8)
    draw_box(ax, 0.68, 0.22, 0.28, 0.08, 'Query IndexedDB\nBuild Response String', C_DB, fontsize=8, textcolor=C_DARK)

    draw_box(ax, 0.30, 0.10, 0.40, 0.07, 'Display Response\nin Chat Window', C_RENDER, fontsize=9)

    draw_arrow(ax, 0.50, 0.88, 0.50, 0.82, '#555555', lw=1.5)
    draw_arrow(ax, 0.35, 0.79, 0.17, 0.70, '#555555')
    draw_arrow(ax, 0.65, 0.79, 0.82, 0.70, '#555555')
    ax.text(0.28, 0.80, 'Yes', fontsize=7, color=C_MAIN, fontweight='bold')
    ax.text(0.70, 0.80, 'No', fontsize=7, color=C_TEAL, fontweight='bold')

    draw_arrow(ax, 0.82, 0.62, 0.82, 0.56, '#555555', lw=1.5)
    draw_arrow(ax, 0.82, 0.48, 0.82, 0.43, '#555555', lw=1.5)
    draw_arrow(ax, 0.82, 0.35, 0.82, 0.30, '#555555', lw=1.5)

    draw_arrow(ax, 0.17, 0.62, 0.38, 0.17, '#555555')
    draw_arrow(ax, 0.82, 0.22, 0.62, 0.15, '#555555')

    save(fig, 'Figure_4_4_ChatBrain_NLP.png')


# ═══════════════════════════════════════════════
# FIGURE 4.5a & 4.5b: Global Search
# ═══════════════════════════════════════════════
def fig_4_5a():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.5(a): Global Search\nDebounce and Scan Initialisation', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('User Types in\nSearch Bar', 0.50, 0.90, C_DARK),
        ('Clear Previous\nDebounce Timer', 0.50, 0.78, C_IPC),
        ('Set New Timer\n(300ms delay)', 0.50, 0.66, C_MAIN),
        ('◇ Timer\nFired?', 0.50, 0.54, '#888888'),
        ('Scan All localStorage\nKeys with cms_ prefix', 0.50, 0.40, C_TEAL),
        ('For Each Key:\nParse JSON Value', 0.50, 0.28, C_ORANGE),
        ('Pass Records to\nMatching Engine →', 0.50, 0.16, C_RENDER),
    ]

    for text, x, y, color in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.05), (x+0.09, y), (x, y-0.05), (x-0.09, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=8, fontweight='bold')
        else:
            draw_box(ax, x-0.13, y-0.04, 0.26, 0.08, text, color, fontsize=8)

    for i in range(len(steps)-1):
        if i == 3:
            draw_arrow(ax, 0.50, 0.49, 0.50, 0.44, '#555555', lw=1.5)
        else:
            draw_arrow(ax, 0.50, steps[i][2]-0.04, 0.50, steps[i+1][2]+0.05, '#555555', lw=1.5)

    # Reset loop
    ax.annotate('', xy=(0.80, 0.78), xytext=(0.80, 0.54),
                arrowprops=dict(arrowstyle='->', color=C_IPC, lw=1.5, connectionstyle='arc3,rad=-0.3'))
    ax.text(0.87, 0.66, 'New\nKeystroke\nResets', fontsize=6, color=C_IPC, ha='center')

    save(fig, 'Figure_4_5a_Global_Search_Debounce.png')

def fig_4_5b():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.5(b): Global Search\nRecord Matching, Snippet Generation, and Result Cap', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('Receive Parsed\nRecords Array', 0.50, 0.90, C_TEAL),
        ('For Each Record:\nLowercase All Fields', 0.50, 0.78, C_MAIN),
        ('◇ Query\nMatches?', 0.50, 0.66, '#888888'),
        ('Extract Matching\nSnippet (±30 chars)', 0.25, 0.54, C_RENDER),
        ('Skip Record', 0.75, 0.54, '#cccccc'),
        ('◇ Results\n> 100?', 0.25, 0.42, '#888888'),
        ('Cap at 100\nBreak Loop', 0.05, 0.30, C_IPC),
        ('Add to Results\nArray', 0.40, 0.30, C_RENDER),
        ('Sort by Relevance\nScore', 0.25, 0.18, C_PURPLE),
        ('Render Results\nin Dropdown', 0.25, 0.08, C_MAIN),
    ]

    for text, x, y, color in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.05), (x+0.09, y), (x, y-0.05), (x-0.09, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=7, fontweight='bold')
        else:
            draw_box(ax, x-0.12, y-0.04, 0.24, 0.08, text, color, fontsize=7)

    draw_arrow(ax, 0.50, 0.86, 0.50, 0.82, '#555555', lw=1.5)
    draw_arrow(ax, 0.50, 0.74, 0.50, 0.71, '#555555', lw=1.5)
    draw_arrow(ax, 0.41, 0.66, 0.37, 0.58, '#555555')
    draw_arrow(ax, 0.59, 0.66, 0.63, 0.58, '#555555')
    ax.text(0.39, 0.67, 'Yes', fontsize=7, color=C_RENDER, fontweight='bold')
    ax.text(0.61, 0.67, 'No', fontsize=7, color='#888888', fontweight='bold')
    draw_arrow(ax, 0.25, 0.50, 0.25, 0.47, '#555555', lw=1.5)
    draw_arrow(ax, 0.16, 0.42, 0.10, 0.34, '#555555')
    draw_arrow(ax, 0.34, 0.42, 0.40, 0.34, '#555555')
    ax.text(0.14, 0.43, 'Yes', fontsize=7, color=C_IPC, fontweight='bold')
    ax.text(0.35, 0.43, 'No', fontsize=7, color=C_RENDER, fontweight='bold')
    draw_arrow(ax, 0.25, 0.26, 0.25, 0.22, '#555555', lw=1.5)
    draw_arrow(ax, 0.25, 0.14, 0.25, 0.12, '#555555', lw=1.5)

    save(fig, 'Figure_4_5b_Global_Search_Matching.png')


# ═══════════════════════════════════════════════
# FIGURE 4.6: Prescription Sync Pipeline
# ═══════════════════════════════════════════════
def fig_4_6():
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.6: Background OPD-to-Pharmacy\nPrescription Synchronization Pipeline', fontsize=13, fontweight='bold', pad=15)

    parts = [('OPD\nModule', 0.08, C_MAIN), ('Sync\nEngine', 0.28, C_TEAL),
             ('localStorage\n(cms_daily_opd)', 0.48, C_ORANGE), ('Pharmacy\nQueue', 0.68, C_PURPLE),
             ('Stock\nManager', 0.88, C_IPC)]
    for name, x, color in parts:
        draw_box(ax, x-0.07, 0.88, 0.14, 0.07, name, color, fontsize=8)
        ax.plot([x, x], [0.88, 0.15], color='#dddddd', lw=1, linestyle='--')

    msgs = [
        (0.08, 0.82, 0.28, 0.82, '1: Doctor saves prescription'),
        (0.28, 0.76, 0.48, 0.76, '2: Write to cms_daily_opd (localStorage)'),
        (0.48, 0.70, 0.28, 0.70, '3: setInterval(10000) polling tick'),
        (0.28, 0.64, 0.48, 0.64, '4: extractFromOPD() scan records'),
        (0.48, 0.58, 0.28, 0.58, '5: Return new/updated prescriptions'),
        (0.28, 0.52, 0.68, 0.52, '6: Push to pharmacy pending queue'),
        (0.68, 0.46, 0.88, 0.46, '7: Pharmacist dispenses medicines'),
        (0.88, 0.40, 0.68, 0.40, '8: Update stock quantities'),
        (0.68, 0.34, 0.48, 0.34, '9: Mark prescription as "dispensed"'),
        (0.48, 0.28, 0.28, 0.28, '10: Sync status back to OPD'),
    ]

    for x1, y1, x2, y2, label in msgs:
        draw_arrow(ax, x1, y1, x2, y2, '#555555', lw=1.2)
        mx = (x1+x2)/2
        ax.text(mx, y1+0.015, label, ha='center', va='bottom', fontsize=6.5, color='#333333', fontweight='bold')

    # Timer annotation
    ax.text(0.28, 0.20, '⏱ 10-second polling interval', ha='center', fontsize=8,
            color=C_TEAL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#e0f2f1', edgecolor=C_TEAL))

    save(fig, 'Figure_4_6_Prescription_Sync.png')


# ═══════════════════════════════════════════════
# FIGURE 4.7a & 4.7b: Stock Deduction
# ═══════════════════════════════════════════════
def fig_4_7a():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.7(a): Medicine Verification\nand Stock Lookup (Part 1)', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('Pharmacist Clicks\n"Dispense"', 0.50, 0.90, C_DARK),
        ('Load Prescription\nMedicine List', 0.50, 0.78, C_MAIN),
        ('For Each Medicine\nin Prescription:', 0.50, 0.66, C_TEAL),
        ('Normalize Name\n.toLowerCase().trim()', 0.50, 0.54, C_ORANGE),
        ('Search MED_STOCK\nCase-Insensitive Match', 0.50, 0.42, C_DB),
        ('◇ Medicine\nFound?', 0.50, 0.30, '#888888'),
        ('Proceed to\nStock Check →', 0.25, 0.18, C_RENDER),
        ('Add to\nmissingMeds Queue', 0.75, 0.18, C_IPC),
    ]

    for text, x, y, color in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.05), (x+0.09, y), (x, y-0.05), (x-0.09, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=8, fontweight='bold')
        else:
            draw_box(ax, x-0.13, y-0.04, 0.26, 0.08, text, color, fontsize=8)

    for i in range(5):
        draw_arrow(ax, 0.50, steps[i][2]-0.04, 0.50, steps[i+1][2]+0.05, '#555555', lw=1.5)
    draw_arrow(ax, 0.41, 0.30, 0.37, 0.22, '#555555')
    draw_arrow(ax, 0.59, 0.30, 0.63, 0.22, '#555555')
    ax.text(0.38, 0.31, 'Yes', fontsize=7, color=C_RENDER, fontweight='bold')
    ax.text(0.61, 0.31, 'No', fontsize=7, color=C_IPC, fontweight='bold')

    save(fig, 'Figure_4_7a_Stock_Lookup.png')

def fig_4_7b():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure 4.7(b): Stock Quantity Update,\nTimestamp Logging, and Missing Medicine Alert', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('Medicine Found\nin MED_STOCK', 0.50, 0.90, C_RENDER),
        ('◇ Stock ≥\nPrescribed Qty?', 0.50, 0.78, '#888888'),
        ('Subtract Quantity\nstock -= prescribed', 0.25, 0.64, C_TEAL),
        ('Alert: Insufficient\nStock Warning', 0.75, 0.64, C_IPC),
        ('Update lastUpdated\nTimestamp', 0.25, 0.50, C_ORANGE),
        ('Log to\nDISPENSE_LOG', 0.25, 0.36, C_DB),
        ('◇ More\nMedicines?', 0.50, 0.24, '#888888'),
        ('Process Next\nMedicine', 0.25, 0.12, C_MAIN),
        ('Show Summary\n& Missing Meds Alert', 0.75, 0.12, C_PURPLE),
    ]

    for text, x, y, color in steps:
        if text.startswith('◇'):
            diamond = plt.Polygon([(x, y+0.05), (x+0.09, y), (x, y-0.05), (x-0.09, y)],
                                  facecolor=color+'22', edgecolor=color, linewidth=1.5)
            ax.add_patch(diamond)
            ax.text(x, y, text.replace('◇ ', ''), ha='center', va='center', fontsize=7, fontweight='bold')
        else:
            draw_box(ax, x-0.13, y-0.04, 0.26, 0.08, text, color, fontsize=8)

    draw_arrow(ax, 0.50, 0.86, 0.50, 0.83, '#555555', lw=1.5)
    draw_arrow(ax, 0.41, 0.78, 0.37, 0.68, '#555555')
    draw_arrow(ax, 0.59, 0.78, 0.63, 0.68, '#555555')
    ax.text(0.38, 0.79, 'Yes', fontsize=7, color=C_TEAL, fontweight='bold')
    ax.text(0.61, 0.79, 'No', fontsize=7, color=C_IPC, fontweight='bold')
    draw_arrow(ax, 0.25, 0.60, 0.25, 0.54, '#555555', lw=1.5)
    draw_arrow(ax, 0.25, 0.46, 0.25, 0.40, '#555555', lw=1.5)
    draw_arrow(ax, 0.25, 0.32, 0.41, 0.29, '#555555')
    draw_arrow(ax, 0.75, 0.60, 0.59, 0.29, '#555555')
    draw_arrow(ax, 0.41, 0.24, 0.37, 0.16, '#555555')
    draw_arrow(ax, 0.59, 0.24, 0.63, 0.16, '#555555')
    ax.text(0.38, 0.25, 'Yes', fontsize=7, color=C_MAIN, fontweight='bold')
    ax.text(0.61, 0.25, 'No', fontsize=7, color=C_PURPLE, fontweight='bold')

    save(fig, 'Figure_4_7b_Stock_Update.png')


# ═══════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating all technical diagrams...\n")
    fig_2_1()
    fig_3_1()
    fig_3_2()
    fig_3_3()
    fig_3_4()
    fig_3_5a()
    fig_3_5b()
    fig_3_6a()
    fig_3_6b()
    fig_3_7()
    fig_3_8()
    fig_4_1()
    fig_4_2()
    fig_4_3()
    fig_4_4()
    fig_4_5a()
    fig_4_5b()
    fig_4_6()
    fig_4_7a()
    fig_4_7b()
    print(f"\nAll diagrams saved to: {OUT}")
