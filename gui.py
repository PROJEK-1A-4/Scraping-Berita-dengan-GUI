# gui.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Kyla (InputPanel) + Richard (MainWindow)            ║
# ╚══════════════════════════════════════════════════════════════╝
#
# FILE INI DIBAGI DUA:
#   - Bagian atas (≈ baris 30–110) → TUGAS KYLA: class InputPanel
#   - Bagian bawah (≈ baris 115+)  → TUGAS RICHARD: class MainWindow
#
# Cara kolaborasi:
#   - Kyla kerjakan di branch dev/kyla, Richard di dev/richard
#   - Kalau edit baris yang sama, koordinasi dulu biar tidak konflik!

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QSpinBox, QCheckBox, QDateEdit, QMessageBox,
    QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

import config
import worker as worker_module
import exporter


# ══════════════════════════════════════════════════════════════
#  BAGIAN KYLA — InputPanel
# ══════════════════════════════════════════════════════════════

class InputPanel(QWidget):
    """
    Panel input di bagian atas/kiri aplikasi.
    Berisi: URL input, limit artikel, toggle filter tanggal, date picker.

    TUGAS KYLA:
        1. _setup_ui() — susun semua widget dalam layout yang rapi
        2. get_inputs() — kembalikan nilai semua input sebagai dict
        3. validate() — validasi input sebelum scraping dimulai
        4. _toggle_date_filter() — enable/disable date picker saat checkbox berubah
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # ─── Widget declaration — JANGAN HAPUS nama-nama ini ──────
        # MainWindow bergantung pada nama atribut ini!
        self.input_url      = QLineEdit()
        self.input_limit    = QSpinBox()
        self.checkbox_filter = QCheckBox("Filter Tanggal")
        self.date_start     = QDateEdit()
        self.date_end       = QDateEdit()

        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Susun semua widget dalam layout.

        Spesifikasi:
            - input_url    : placeholder "https://...", full width
            - input_limit  : range 1–500, default config.DEFAULT_LIMIT
            - checkbox_filter: default unchecked
            - date_start, date_end: QDateEdit, disabled saat checkbox off
                                    default: hari ini
            - Tampilan rapi — gunakan QHBoxLayout / QVBoxLayout / QFormLayout
        """
        # Layout utama
        layout = QVBoxLayout(self)

        # ─── Baris 1: URL Input ──────────────────────────────────
        url_layout = QHBoxLayout()
        label_url = QLabel("URL:")
        label_url.setFixedWidth(60)
        self.input_url.setPlaceholderText("https://www.cnnindonesia.com")
        self.input_url.setMinimumHeight(32)
        self.input_url.setClearButtonEnabled(True)  # Built-in clear button
        url_layout.addWidget(label_url)
        url_layout.addWidget(self.input_url)
        layout.addLayout(url_layout)

        # ─── Baris 2: Limit Artikel ──────────────────────────────
        limit_layout = QHBoxLayout()
        label_limit = QLabel("Limit:")
        label_limit.setFixedWidth(60)
        self.input_limit.setRange(1, 500)
        self.input_limit.setValue(config.DEFAULT_LIMIT)
        self.input_limit.setSuffix(" artikel")  # Add suffix untuk clarity
        self.input_limit.setMinimumHeight(32)   # Match URL input height
        self.input_limit.setMinimumWidth(120)   # Cukup lebar untuk display
        limit_layout.addWidget(label_limit)
        limit_layout.addWidget(self.input_limit)
        limit_layout.addStretch()  # Push ke kiri
        layout.addLayout(limit_layout)

        # ─── Baris 3: Checkbox Filter Tanggal ────────────────────
        layout.addWidget(self.checkbox_filter)

        # ─── Baris 4: Date Range ────────────────────────────────
        date_layout = QHBoxLayout()
        label_dari = QLabel("Dari:")
        label_dari.setFixedWidth(60)
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setEnabled(False)

        label_sampai = QLabel("Sampai:")
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setEnabled(False)

        date_layout.addWidget(label_dari)
        date_layout.addWidget(self.date_start)
        date_layout.addWidget(label_sampai)
        date_layout.addWidget(self.date_end)
        date_layout.addStretch()  # Push ke kiri
        layout.addLayout(date_layout)

        # ─── Hubungkan checkbox signal ke toggle method ──────────
        self.checkbox_filter.stateChanged.connect(self._toggle_date_filter)

        # Add stretch di akhir agar widget tidak mengambil full height
        layout.addStretch()

    def get_inputs(self) -> dict:
        """
        Ambil nilai semua input dari widget.

        Returns:
            dict dengan key:
                "url"          : str
                "limit"        : int
                "filter_aktif" : bool
                "start_date"   : QDate (atau None jika filter off)
                "end_date"     : QDate (atau None jika filter off)
        """
        # TODO Kyla: return nilai dari setiap widget
        return {
            "url"          : "",
            "limit"        : config.DEFAULT_LIMIT,
            "filter_aktif" : False,
            "start_date"   : None,
            "end_date"     : None,
        }

    def validate(self) -> bool:
        """
        Validasi input sebelum scraping dimulai.
        Tampilkan QMessageBox jika ada error.

        Rules:
            - URL tidak boleh kosong
            - URL harus diawali "http://" atau "https://"
            - Jika filter aktif: date_end tidak boleh sebelum date_start

        Returns:
            bool: True jika semua input valid, False jika ada error
        """
        # TODO Kyla: implementasikan validasi
        # Hint:
        #   inputs = self.get_inputs()
        #   if not inputs["url"]:
        #       QMessageBox.warning(self, "Input Error", "URL tidak boleh kosong!")
        #       return False
        #   if not inputs["url"].startswith(("http://", "https://")):
        #       QMessageBox.warning(...)
        #       return False
        #   if inputs["filter_aktif"] and inputs["end_date"] < inputs["start_date"]:
        #       QMessageBox.warning(...)
        #       return False
        #   return True
        return False

    def _toggle_date_filter(self, state: int) -> None:
        """
        Enable/disable date picker sesuai state checkbox filter.

        Args:
            state: Qt.Checked atau Qt.Unchecked
        """
        aktif = (state == Qt.Checked)
        self.date_start.setEnabled(aktif)
        self.date_end.setEnabled(aktif)


# ══════════════════════════════════════════════════════════════
#  BAGIAN RICHARD — MainWindow
# ══════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    """
    Jendela utama aplikasi News Scraper.

    TUGAS RICHARD:
        1. _setup_ui()        — susun tabel, progress bar, tombol, label dalam layout
        2. _connect_signals() — hubungkan sinyal worker ke slot GUI
        3. mulai_scraping()   — validasi input lalu start worker
        4. stop_scraping()    — panggil worker.stop()
        5. tambah_baris()     — tambahkan 1 artikel ke tabel
        6. update_progress()  — update progress bar
        7. export_csv()       — panggil exporter.export_csv()
        8. export_excel()     — panggil exporter.export_excel()

    PENTING: Simpan worker di self.worker (BUKAN variabel lokal!)
    """

    KOLOM_TABEL = ["No", "Judul", "Tanggal", "Penulis", "Kategori", "URL", "Gambar"]
    # Kolom "Isi" tidak ditampilkan di tabel tapi tetap ada di self.data_hasil untuk ekspor

    def __init__(self):
        super().__init__()

        # ─── State aplikasi ────────────────────────────────────────
        self.data_hasil: list[dict] = []    # artikel valid yang terkumpul
        self.worker = None                  # ScraperWorker — SIMPAN DI SINI!

        # ─── Widget declaration ────────────────────────────────────
        self.input_panel    = InputPanel()
        self.tabel          = QTableWidget()
        self.progress_bar   = QProgressBar()
        self.btn_scrape     = QPushButton("Mulai Scraping")
        self.btn_stop       = QPushButton("Stop")
        self.btn_export_csv = QPushButton("Export CSV")
        self.btn_export_xl  = QPushButton("Export Excel")
        self.label_status   = QLabel("Siap.")
        self.label_jumlah   = QLabel("0 artikel")

        self._setup_ui()
        self._connect_signals()
        self._set_state_idle()   # set initial button states

    def _setup_ui(self) -> None:
        """
        Susun semua widget dalam layout utama.

        Spesifikasi:
            - self.tabel: 7 kolom (KOLOM_TABEL), stretch ke lebar window
            - self.progress_bar: range 0–100
            - Tombol scrape: di kiri, stop: di sebelah scrape
            - Tombol export: di kanan, disabled sampai ada data
            - label_status + label_jumlah di area bawah
            - input_panel di atas atau sidebar kiri
        """
        # Setup central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Setup tabel:
        self.tabel.setColumnCount(len(self.KOLOM_TABEL))
        self.tabel.setHorizontalHeaderLabels(self.KOLOM_TABEL)
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabel.setAlternatingRowColors(True)

        # Progress bar:
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # ─── Add InputPanel (Kyla's work) ────────────────────────
        main_layout.addWidget(self.input_panel)

        # ─── Add Table ───────────────────────────────────────────
        main_layout.addWidget(self.tabel)

        # ─── Add Progress Bar ────────────────────────────────────
        main_layout.addWidget(self.progress_bar)

        # ─── Add Buttons Layout ──────────────────────────────────
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.btn_scrape)
        buttons_layout.addWidget(self.btn_stop)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_export_csv)
        buttons_layout.addWidget(self.btn_export_xl)
        main_layout.addLayout(buttons_layout)

        # ─── Add Status Bar ──────────────────────────────────────
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.label_status)
        status_layout.addStretch()
        status_layout.addWidget(self.label_jumlah)
        main_layout.addLayout(status_layout)

        # Window settings:
        self.setWindowTitle(config.APP_TITLE)
        self.resize(config.WINDOW_W, config.WINDOW_H)

    def _connect_signals(self) -> None:
        """
        Hubungkan sinyal tombol ke slot.

        Koneksi yang dibutuhkan:
            btn_scrape     → mulai_scraping()
            btn_stop       → stop_scraping()
            btn_export_csv → export_csv()
            btn_export_xl  → export_excel()
        """
        # TODO Richard: sambungkan sinyal tombol
        # self.btn_scrape.clicked.connect(self.mulai_scraping)
        # self.btn_stop.clicked.connect(self.stop_scraping)
        # dst.
        pass

    def _set_state_idle(self) -> None:
        """Set state GUI saat idle (tidak sedang scraping)."""
        # TODO Richard: atur enabled/disabled tombol untuk state idle
        # btn_scrape: enabled, btn_stop: disabled
        # btn_export_*: enabled hanya jika self.data_hasil tidak kosong
        pass

    def _set_state_scraping(self) -> None:
        """Set state GUI saat sedang scraping."""
        # TODO Richard: atur enabled/disabled tombol untuk state scraping
        # btn_scrape: disabled, btn_stop: enabled, btn_export_*: disabled
        pass

    def mulai_scraping(self) -> None:
        """
        Dipanggil saat tombol "Mulai Scraping" diklik.

        Alur:
            1. Panggil self.input_panel.validate() — batalkan jika gagal
            2. Reset tabel dan self.data_hasil
            3. Buat ScraperWorker dengan input dari input_panel.get_inputs()
            4. Sambungkan sinyal worker ke slot GUI
            5. Set state scraping
            6. worker.start()
        """
        # TODO Richard: implementasikan mulai scraping
        # INGAT: simpan worker di self.worker, bukan variabel lokal!
        pass

    def stop_scraping(self) -> None:
        """Minta worker berhenti scraping."""
        # TODO Richard: panggil self.worker.stop() jika worker aktif
        pass

    def tambah_baris(self, artikel: dict) -> None:
        """
        Tambahkan 1 artikel valid ke tabel dan self.data_hasil.

        Args:
            artikel: dict artikel (format kesepakatan tim)

        Urutan kolom tabel: No, Judul, Tanggal, Penulis, Kategori, URL, Gambar
        (Isi tidak ditampilkan di tabel, tapi disimpan di self.data_hasil untuk ekspor)
        """
        # TODO Richard:
        # self.data_hasil.append(artikel)
        # row = self.tabel.rowCount()
        # self.tabel.insertRow(row)
        # Isi setiap kolom dengan QTableWidgetItem
        pass

    def update_progress(self, nilai: int) -> None:
        """Update progress bar ke nilai persen (0-100)."""
        # TODO Richard: self.progress_bar.setValue(nilai)
        pass

    def scraping_selesai(self, jumlah: int) -> None:
        """Dipanggil saat worker emit sinyal_selesai."""
        # TODO Richard: update label_status, label_jumlah, set state idle
        pass

    def tampilkan_error(self, pesan: str) -> None:
        """Dipanggil saat worker emit sinyal_error."""
        # TODO Richard: tampilkan QMessageBox.critical, set state idle
        pass

    def export_csv(self) -> None:
        """Panggil exporter.export_csv() dengan self.data_hasil."""
        # TODO Richard: panggil exporter.export_csv(self.data_hasil, "hasil_scraping")
        # Tampilkan dialog sukses/error
        pass

    def export_excel(self) -> None:
        """Panggil exporter.export_excel() dengan self.data_hasil."""
        # TODO Richard: panggil exporter.export_excel(self.data_hasil, "hasil_scraping")
        pass
