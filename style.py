# style.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Aulia                                               ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Langkah Aulia:
#   1. Isi MAIN_STYLESHEET dengan QSS (Qt Style Sheet) untuk styling seluruh app
#   2. apply_style() sudah siap — kamu hanya perlu mengisi MAIN_STYLESHEET
#
# Elemen yang perlu di-styling (lihat gui.py untuk nama widget):
#   - QMainWindow, QWidget  → background color
#   - QTableWidget          → header, row, alternating colors
#   - QPushButton           → warna tombol scraping, stop, export
#   - QProgressBar          → warna bar progress
#   - QLineEdit             → URL input field
#   - QLabel                → font, warna teks status
#   - QSpinBox, QDateEdit   → input number dan tanggal
#
# Referensi QSS: https://doc.qt.io/qt-5/stylesheet-reference.html
# Contoh selector: QPushButton { background-color: #4CAF50; color: white; }
#                  QPushButton:hover { background-color: #45a049; }
#                  QPushButton:disabled { background-color: #cccccc; }


# Aulia: MAIN_STYLESHEET — QSS styling untuk seluruh aplikasi
# Dark theme sesuai gui-mockup.html
# Palette:
#   bg:       #0F1117   surface:  #181C27   surface2: #1E2333
#   border:   #2A3147   accent:   #4F8EF7   accent2:  #00D4AA
#   danger:   #F75A5A   text:     #E8EAF0   muted:    #6B7699

MAIN_STYLESHEET = """
/* ═══ Global ═════════════════════════════════════════════════════════ */
QMainWindow, QWidget {
    background-color: #0F1117;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
    color: #E8EAF0;
}

/* ═══ QMenuBar ════════════════════════════════════════════════════════ */
QMenuBar {
    background-color: #181C27;
    border-bottom: 1px solid #2A3147;
    padding: 2px 4px;
    font-size: 12px;
    color: #E8EAF0;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 14px;
    border-radius: 4px;
    color: #E8EAF0;
}
QMenuBar::item:selected {
    background-color: #2A3147;
    color: #4F8EF7;
}
QMenu {
    background-color: #1E2333;
    border: 1px solid #2A3147;
    border-radius: 6px;
    padding: 4px 0px;
}
QMenu::item {
    padding: 8px 24px 8px 16px;
    font-size: 12px;
    color: #E8EAF0;
}
QMenu::item:selected {
    background-color: rgba(79, 142, 247, 0.15);
    color: #4F8EF7;
}
QMenu::separator {
    height: 1px;
    background-color: #2A3147;
    margin: 4px 8px;
}
QMenu::item:disabled {
    color: #3A4566;
}

/* ═══ QLabel ══════════════════════════════════════════════════════════ */
QLabel {
    font-size: 12px;
    color: #6B7699;
    padding: 1px;
    background: transparent;
}

/* ═══ Input Panel background ═════════════════════════════════════════ */
InputPanel {
    background-color: #181C27;
    border: 1px solid #2A3147;
    border-radius: 8px;
    padding: 4px;
}

/* ═══ QLineEdit ════════════════════════════════════════════════════════ */
QLineEdit {
    background-color: #1E2333;
    border: 1px solid #2A3147;
    border-radius: 5px;
    padding: 7px 12px;
    font-size: 12px;
    color: #00D4AA;
    font-family: "Courier New", monospace;
}
QLineEdit:focus {
    border: 1px solid #6BA3F9;
    background-color: #222941;
    color: #E8EAF0;
}

/* ═══ QSpinBox & QDateEdit ═════════════════════════════════════════════ */
QSpinBox, QDateEdit {
    background-color: #1E2333;
    border: 1px solid #2A3147;
    border-radius: 5px;
    padding: 6px 8px;
    font-size: 12px;
    color: #E8EAF0;
    font-family: "Courier New", monospace;
    min-width: 110px;
}
QSpinBox:focus, QDateEdit:focus {
    border: 1px solid #6BA3F9;
    background-color: #222941;
}
QSpinBox::up-button, QSpinBox::down-button {
    background-color: #2A3147;
    border: none;
    width: 24px;
    border-radius: 3px;
    margin: 1px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #4F8EF7;
}
QSpinBox::up-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 6px solid #E8EAF0;
    width: 0;
    height: 0;
}
QSpinBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #E8EAF0;
    width: 0;
    height: 0;
}
QSpinBox::up-arrow:hover {
    border-bottom-color: #ffffff;
}
QSpinBox::down-arrow:hover {
    border-top-color: #ffffff;
}
QDateEdit::up-button, QDateEdit::down-button {
    background-color: #2A3147;
    border: none;
    width: 16px;
}
QDateEdit::up-button:hover, QDateEdit::down-button:hover {
    background-color: #4F8EF7;
}

/* ═══ QCheckBox ═════════════════════════════════════════════════════════ */
QCheckBox {
    font-size: 12px;
    color: #6B7699;
    spacing: 8px;
    font-family: "Courier New", monospace;
}
QCheckBox:checked {
    color: #00D4AA;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    border: 1px solid #2A3147;
    background-color: #1E2333;
}
QCheckBox::indicator:checked {
    background-color: #4F8EF7;
    border-color: #4F8EF7;
}

/* ═══ QPushButton — Mulai Scraping (biru, default) ═════════════════════ */
QPushButton {
    background-color: #4F8EF7;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 9px 20px;
    font-size: 12px;
    font-weight: 600;
    font-family: "Courier New", monospace;
    min-width: 120px;
}
QPushButton:hover {
    background-color: #6BA3F9;
}
QPushButton:pressed {
    background-color: #3A7AE4;
}
QPushButton:disabled {
    background-color: #1E2333;
    color: #556080;
    border: 1px solid #2A3147;
}

/* ── Stop (outline merah) ── */
QPushButton#btn_stop {
    background-color: #1E2333;
    color: #F75A5A;
    border: 1px solid #F75A5A;
}
QPushButton#btn_stop:hover {
    background-color: rgba(247, 90, 90, 0.15);
}
QPushButton#btn_stop:disabled {
    background-color: #1E2333;
    color: #556080;
    border: 1px solid #2A3147;
}

/* ── Export CSV & Excel (outline teal) ── */
QPushButton#btn_export_csv, QPushButton#btn_export_xl {
    background-color: #1E2333;
    color: #00D4AA;
    border: 1px solid #00D4AA;
}
QPushButton#btn_export_csv:hover, QPushButton#btn_export_xl:hover {
    background-color: rgba(0, 212, 170, 0.12);
}
QPushButton#btn_export_csv:disabled, QPushButton#btn_export_xl:disabled {
    background-color: #1E2333;
    color: #556080;
    border: 1px solid #2A3147;
}

/* ═══ QTableWidget ═══════════════════════════════════════════════════════ */
QTableWidget {
    background-color: #0F1117;
    alternate-background-color: rgba(30, 35, 51, 0.4);
    border: 1px solid #2A3147;
    border-radius: 6px;
    gridline-color: rgba(42, 49, 71, 0.5);
    selection-background-color: rgba(79, 142, 247, 0.15);
    selection-color: #E8EAF0;
    font-size: 12px;
    color: #E8EAF0;
}
QTableWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid rgba(42, 49, 71, 0.5);
}
QTableWidget::item:selected {
    background-color: rgba(79, 142, 247, 0.12);
    border-left: 2px solid #4F8EF7;
    color: #E8EAF0;
}
QHeaderView {
    background-color: #1E2333;
}
QHeaderView::section {
    background-color: #1E2333;
    color: #6B7699;
    font-family: "Courier New", monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 1px;
    padding: 9px 10px;
    border: none;
    border-bottom: 1px solid #2A3147;
    border-right: 1px solid #2A3147;
    text-transform: uppercase;
}
QHeaderView::section:last {
    border-right: none;
}
QTableWidget QScrollBar:vertical {
    background: #181C27;
    width: 8px;
    border-radius: 4px;
}
QTableWidget QScrollBar::handle:vertical {
    background: #2A3147;
    border-radius: 4px;
    min-height: 20px;
}
QTableWidget QScrollBar::handle:vertical:hover {
    background: #4F8EF7;
}

/* ═══ QProgressBar ═════════════════════════════════════════════════════ */
QProgressBar {
    background-color: #1E2333;
    border: 1px solid #2A3147;
    border-radius: 4px;
    text-align: right;
    padding-right: 6px;
    font-size: 11px;
    font-family: "Courier New", monospace;
    font-weight: bold;
    color: #6B7699;
    min-height: 16px;
    max-height: 16px;
}
QProgressBar::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #4F8EF7, stop:1 #00D4AA
    );
    border-radius: 3px;
}

/* ═══ Bottom bar ════════════════════════════════════════════════════════ */
QWidget#bottom_bar {
    background-color: #181C27;
    border-top: 1px solid #2A3147;
    border-radius: 0px;
}
QWidget#bottom_bar QLabel {
    font-family: "Courier New", monospace;
    font-size: 10px;
    color: #6B7699;
    letter-spacing: 1px;
    background: transparent;
    padding: 0px;
}

/* ═══ QMessageBox & QDialog ═══════════════════════════════════════════ */
QMessageBox, QDialog {
    background-color: #181C27;
}
QMessageBox QLabel, QDialog QLabel {
    font-size: 13px;
    color: #E8EAF0;
}
QTextBrowser {
    background-color: #1E2333;
    border: 1px solid #2A3147;
    border-radius: 4px;
    color: #E8EAF0;
    font-size: 13px;
    padding: 8px;
}

/* ═══ QToolTip (polish kecil, non-fungsional) ═════════════════════════ */
QToolTip {
    background-color: #1E2333;
    color: #E8EAF0;
    border: 1px solid #2A3147;
    padding: 6px 8px;
    font-size: 11px;
}

/* ═══ QScrollArea/QScrollBar (polish kecil, non-fungsional) ═══════════ */
QScrollArea {
    background: transparent;
    border: none;
}
QScrollBar:vertical {
    background: #181C27;
    width: 8px;
    border-radius: 4px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #2A3147;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #4F8EF7;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


def apply_style(app) -> None:
    """
    Terapkan MAIN_STYLESHEET ke seluruh aplikasi.
    Dipanggil di main.py SEBELUM MainWindow dibuat.

    Args:
        app: QApplication instance
    """
    app.setStyleSheet(MAIN_STYLESHEET)
