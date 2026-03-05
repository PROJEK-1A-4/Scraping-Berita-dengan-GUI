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


# TODO Aulia: isi string QSS di bawah ini
# Minimal styling: warna background, font, dan tombol utama
MAIN_STYLESHEET = """
/* TODO Aulia: tambahkan styling QSS di sini */
"""


def apply_style(app) -> None:
    """
    Terapkan MAIN_STYLESHEET ke seluruh aplikasi.
    Dipanggil di main.py SEBELUM MainWindow dibuat.

    Args:
        app: QApplication instance
    """
    app.setStyleSheet(MAIN_STYLESHEET)
