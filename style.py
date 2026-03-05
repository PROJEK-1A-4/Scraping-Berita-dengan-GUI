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
MAIN_STYLESHEET = """
/* ═══════════════════════════════════════════════════════════
   Global — Background & Font
   ═══════════════════════════════════════════════════════════ */
QMainWindow, QWidget {
    background-color: #f5f7fa;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
    color: #2c3e50;
}

/* ═══════════════════════════════════════════════════════════
   QLabel — Teks status & judul
   ═══════════════════════════════════════════════════════════ */
QLabel {
    font-size: 13px;
    color: #34495e;
    padding: 2px;
}

/* ═══════════════════════════════════════════════════════════
   QLineEdit — URL input field
   ═══════════════════════════════════════════════════════════ */
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 13px;
    color: #2c3e50;
}
QLineEdit:focus {
    border: 2px solid #3498db;
}

/* ═══════════════════════════════════════════════════════════
   QSpinBox & QDateEdit — Input number dan tanggal
   ═══════════════════════════════════════════════════════════ */
QSpinBox, QDateEdit {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 13px;
    color: #2c3e50;
}
QSpinBox:focus, QDateEdit:focus {
    border: 2px solid #3498db;
}

/* ═══════════════════════════════════════════════════════════
   QCheckBox — Filter tanggal toggle
   ═══════════════════════════════════════════════════════════ */
QCheckBox {
    font-size: 13px;
    color: #2c3e50;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

/* ═══════════════════════════════════════════════════════════
   QPushButton — Tombol Scraping (hijau)
   ═══════════════════════════════════════════════════════════ */
QPushButton {
    background-color: #27ae60;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: bold;
    min-width: 100px;
}
QPushButton:hover {
    background-color: #219a52;
}
QPushButton:pressed {
    background-color: #1e8449;
}
QPushButton:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
}

/* ── Tombol Stop (merah) ── */
QPushButton#btn_stop {
    background-color: #e74c3c;
}
QPushButton#btn_stop:hover {
    background-color: #c0392b;
}
QPushButton#btn_stop:pressed {
    background-color: #a93226;
}

/* ── Tombol Export CSV (biru) ── */
QPushButton#btn_export_csv {
    background-color: #2980b9;
}
QPushButton#btn_export_csv:hover {
    background-color: #2471a3;
}

/* ── Tombol Export Excel (biru tua) ── */
QPushButton#btn_export_xl {
    background-color: #1a5276;
}
QPushButton#btn_export_xl:hover {
    background-color: #154360;
}

/* ═══════════════════════════════════════════════════════════
   QTableWidget — Tabel hasil scraping
   ═══════════════════════════════════════════════════════════ */
QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #eaf2f8;
    border: 1px solid #d5dbdb;
    gridline-color: #d5dbdb;
    selection-background-color: #3498db;
    selection-color: #ffffff;
    font-size: 12px;
}
QHeaderView::section {
    background-color: #2c3e50;
    color: #ffffff;
    font-weight: bold;
    font-size: 12px;
    padding: 6px;
    border: none;
    border-right: 1px solid #1a252f;
}

/* ═══════════════════════════════════════════════════════════
   QProgressBar — Bar progress scraping
   ═══════════════════════════════════════════════════════════ */
QProgressBar {
    background-color: #d5dbdb;
    border: none;
    border-radius: 5px;
    text-align: center;
    font-size: 12px;
    font-weight: bold;
    color: #2c3e50;
    min-height: 22px;
}
QProgressBar::chunk {
    background-color: #27ae60;
    border-radius: 5px;
}

/* ═══════════════════════════════════════════════════════════
   QMessageBox — Dialog pesan
   ═══════════════════════════════════════════════════════════ */
QMessageBox {
    background-color: #f5f7fa;
}
QMessageBox QLabel {
    font-size: 13px;
    color: #2c3e50;
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
