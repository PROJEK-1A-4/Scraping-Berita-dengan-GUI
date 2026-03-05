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
        # TODO Kyla: susun layout di sini
        # Hint:
        #   layout = QVBoxLayout(self)
        #   Baris 1: Label "URL:" + self.input_url
        #   Baris 2: Label "Limit:" + self.input_limit
        #   Baris 3: self.checkbox_filter
        #   Baris 4: Label "Dari:" + self.date_start + Label "s/d:" + self.date_end
        #
        #   # Konfigurasi widget:
        #   self.input_url.setPlaceholderText("https://...")
        #   self.input_limit.setRange(1, 500)
        #   self.input_limit.setValue(config.DEFAULT_LIMIT)
        #   self.date_start.setDate(QDate.currentDate())
        #   self.date_end.setDate(QDate.currentDate())
        #   self.date_start.setEnabled(False)
        #   self.date_end.setEnabled(False)
        #
        #   # Hubungkan checkbox ke toggle:
        #   self.checkbox_filter.stateChanged.connect(self._toggle_date_filter)
        pass

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
        # TODO Kyla: aktifkan/nonaktifkan date_start dan date_end
        # aktif = (state == Qt.Checked)
        # self.date_start.setEnabled(aktif)
        # self.date_end.setEnabled(aktif)
        pass


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
        Susun semua widget dalam layout utama.                              (DONE)

        Spesifikasi:
            - self.tabel: 7 kolom (KOLOM_TABEL), stretch ke lebar window    (DONE)
            - self.progress_bar: range 0–100                                (DONE)
            - Tombol scrape: di kiri, stop: di sebelah scrape               (DONE)
            - Tombol export: di kanan, disabled sampai ada data             (DONE)
            - label_status + label_jumlah di area bawah                     (DONE)
            - input_panel di atas atau sidebar kiri                         (DONE)
        """
        # TODO Richard: implementasikan layout utama                        (DONE)

        #   central = QWidget()
        central = QWidget()
        #   self.setCentralWidget(central)
        self.setCentralWidget(central)
        #   main_layout = QVBoxLayout(central)
        main_layout = QVBoxLayout(central)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.input_panel)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_scrape)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_export_csv)
        btn_layout.addWidget(self.btn_export_xl)
        top_layout.addLayout(btn_layout)

        main_layout.addLayout(top_layout)

        #   SETUP TABEL:                                                    (DONE)

        #   self.tabel.setColumnCount(len(self.KOLOM_TABEL))
        self.tabel.setColumnCount(len(self.KOLOM_TABEL))
        #   self.tabel.setHorizontalHeaderLabels(self.KOLOM_TABEL)
        self.tabel.setHorizontalHeaderLabels(self.KOLOM_TABEL)
        #   self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #   self.tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        #   self.tabel.setAlternatingRowColors(True)
        self.tabel.setAlternatingRowColors(True)
        main_layout.addWidget(self.tabel)

        #   PROGRESS BAR:                                                   (DONE)

        #   self.progress_bar.setRange(0, 100)
        self.progress_bar.setRange(0, 100)
        #   self.progress_bar.setValue(0)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self.label_status)
        status_layout.addStretch()
        status_layout.addWidget(self.label_jumlah)
        main_layout.addLayout(status_layout)

        # WINDOW SETTING:                                                   (DONE)

        #   self.setWindowTitle(config.APP_TITLE)
        self.setWindowTitle(config.APP_TITLE)
        #   self.resize(config.WINDOW_W, config.WINDOW_H)
        self.resize(config.WINDOW_W, config.WINDOW_H)
        pass

    def _connect_signals(self) -> None:
        """
        Hubungkan sinyal tombol ke slot.                                    (DONE)

        Koneksi yang dibutuhkan:
            btn_scrape     → mulai_scraping()                               (DONE)
            btn_stop       → stop_scraping()                                (DONE)
            btn_export_csv → export_csv()                                   (DONE)
            btn_export_xl  → export_excel()                                 (DONE)
        """
        # TODO Richard: sambungkan sinyal tombol                            (DONE)

        # self.btn_scrape.clicked.connect(self.mulai_scraping)
        self.btn_scrape.clicked.connect(self.mulai_scraping)
        # self.btn_stop.clicked.connect(self.stop_scraping)
        self.btn_stop.clicked.connect(self.stop_scraping)
        # dst.
        self.btn_export_csv.clicked.connect(self.export_csv)
        self.btn_export_xl.clicked.connect(self.export_excel)
        pass

    def _set_state_idle(self) -> None:
        """Set state GUI saat idle (tidak sedang scraping)."""              #(DONE)
        # TODO Richard: atur enabled/disabled tombol untuk state idle        (DONE)

        # btn_scrape: enabled                                                (DONE)
        self.btn_scrape.setEnabled(True)
        # btn_stop: disabled                                                 (DONE)
        self.btn_stop.setEnabled(False)
        # btn_export_*: enabled hanya jika self.data_hasil tidak kosong      (DONE)
        self.btn_export_csv.setEnabled(len(self.data_hasil) > 0)
        self.btn_export_xl.setEnabled(len(self.data_hasil) > 0)
        pass

    def _set_state_scraping(self) -> None:
        """Set state GUI saat sedang scraping."""                           #(DONE)
        # TODO Richard: atur enabled/disabled tombol untuk state scraping    (DONE)

        # btn_scrape: disabled                                               (DONE)
        self.btn_scrape.setEnabled(False)
        # btn_stop: enabled                                                  (DONE)
        self.btn_stop.setEnabled(True)
        # btn_export_*: disabled                                             (DONE)
        self.btn_export_csv.setEnabled(False)
        self.btn_export_xl.setEnabled(False)
        pass

    def mulai_scraping(self) -> None:
        """
        Dipanggil saat tombol "Mulai Scraping" diklik. (Should Be Working, Yet To Be Tested)

        Alur:
            1. Panggil self.input_panel.validate() — batalkan jika gagal     (DONE)
            2. Reset tabel dan self.data_hasil                               (DONE)
            3. Buat ScraperWorker dengan input dari input_panel.get_inputs() (DONE)
            4. Sambungkan sinyal worker ke slot GUI                          (DONE)
            5. Set state scraping                                            (DONE)
            6. worker.start()                                                (DONE)
        """
        # TODO Richard: implementasikan mulai scraping                       (DONE)

        if not self.input_panel.validate():
            return

        self.data_hasil.clear()
        self.tabel.setRowCount(0)

        # INGAT: simpan worker di self.worker, bukan variabel lokal! (STORED TO self)
        inputs = self.input_panel.get_inputs()
        self.worker = worker_module.ScraperWorker(**inputs)

        self.worker.sinyal_progress.connect(self.update_progress)
        self.worker.sinyal_hasil.connect(self.tambah_baris)
        self.worker.sinyal_selesai.connect(self.scraping_selesai)
        self.worker.sinyal_error.connect(self.tampilkan_error)
        self.worker.sinyal_status.connect(self.label_status.setText)

        self._set_state_scraping()
        self.worker.start()
        pass

    def stop_scraping(self) -> None:
        """Minta worker berhenti scraping."""                               #(DONE)
        # TODO Richard: panggil self.worker.stop() jika worker aktif         (DONE)
        if self.worker:
            self.worker.stop()
        pass

    def tambah_baris(self, artikel: dict) -> None:
        """
        Tambahkan 1 artikel valid ke tabel dan self.data_hasil.              (DONE)

        Args:
            artikel: dict artikel (format kesepakatan tim)

        Urutan kolom tabel: No, Judul, Tanggal, Penulis, Kategori, URL, Gambar
        (Isi tidak ditampilkan di tabel, tapi disimpan di self.data_hasil untuk ekspor)
        """
        # TODO Richard:                                                      (DONE)

        # self.data_hasil.append(artikel)
        self.data_hasil.append(artikel)
        # row = self.tabel.rowCount()
        row = self.tabel.rowCount()
        # self.tabel.insertRow(row)
        self.tabel.insertRow(row)

        # Isi setiap kolom dengan QTableWidgetItem
        self.tabel.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.tabel.setItem(row, 1, QTableWidgetItem(artikel.get("judul", "")))
        self.tabel.setItem(row, 2, QTableWidgetItem(artikel.get("tanggal", "")))
        self.tabel.setItem(row, 3, QTableWidgetItem(artikel.get("penulis", "")))
        self.tabel.setItem(row, 4, QTableWidgetItem(artikel.get("kategori", "")))
        self.tabel.setItem(row, 5, QTableWidgetItem(artikel.get("url", "")))
        self.tabel.setItem(row, 6, QTableWidgetItem(artikel.get("gambar_url", "")))

        self.label_jumlah.setText(f"{len(self.data_hasil)} artikel")
        pass

    def update_progress(self, nilai: int) -> None:
        """Update progress bar ke nilai persen (0-100)."""                  #(DONE)
        # TODO Richard: self.progress_bar.setValue(nilai)                    (DONE)

        self.progress_bar.setValue(nilai)
        pass

    def scraping_selesai(self, jumlah: int) -> None:
        """Dipanggil saat worker emit sinyal_selesai."""                    #(DONE)
        # TODO Richard: update label_status, label_jumlah, set state idle    (DONE)

        self.label_status.setText("Selesai.")
        self.label_jumlah.setText(f"{jumlah} artikel")
        self._set_state_idle()
        pass

    def tampilkan_error(self, pesan: str) -> None:
        """Dipanggil saat worker emit sinyal_error."""                      #(YET TO BE TESTED)
        # TODO Richard: tampilkan QMessageBox.critical, set state idle       (DONE)

        QMessageBox.critical(self, "Error", pesan)
        self._set_state_idle()
        pass

    def export_csv(self) -> None:
        """Panggil exporter.export_csv() dengan self.data_hasil."""
        # TODO Richard: panggil exporter.export_csv(self.data_hasil, "hasil_scraping") (DONE)
        # Tampilkan dialog sukses/error

        exporter.export_csv(self.data_hasil, "hasil_scraping")
        QMessageBox.information(self, "Success", "Data berhasil diexport ke CSV.")
        pass

    def export_excel(self) -> None:
        """Panggil exporter.export_excel() dengan self.data_hasil."""
        # TODO Richard: panggil exporter.export_excel(self.data_hasil, "hasil_scraping") (DONE)

        exporter.export_excel(self.data_hasil, "hasil_scraping")
        QMessageBox.information(self, "Success", "Data berhasil diexport ke Excel.")
        pass
