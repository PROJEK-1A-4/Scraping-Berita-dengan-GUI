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
    QHeaderView, QSizePolicy, QDialog, QTextBrowser
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
        self.checkbox_filter.setToolTip("Centang untuk mengaktifkan filter tanggal (artikel antara Dari dan Sampai)")
        self.checkbox_filter.setChecked(False)  # Explicit default unchecked
        layout.addWidget(self.checkbox_filter)

        # ─── Baris 4: Date Range ────────────────────────────────
        date_layout = QHBoxLayout()
        label_dari = QLabel("Dari:")
        label_dari.setFixedWidth(60)
        
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setEnabled(False)
        self.date_start.setDisplayFormat("dd/MM/yyyy")  # Readable format
        self.date_start.setCalendarPopup(True)  # Popup calendar saat diklik
        self.date_start.setMinimumHeight(32)  # Match other widgets
        self.date_start.setToolTip("Pilih tanggal awal (Double-click atau klik icon kalender)")

        label_sampai = QLabel("Sampai:")
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setEnabled(False)
        self.date_end.setDisplayFormat("dd/MM/yyyy")  # Readable format
        self.date_end.setCalendarPopup(True)  # Popup calendar saat diklik
        self.date_end.setMinimumHeight(32)  # Match other widgets
        self.date_end.setToolTip("Pilih tanggal akhir (Double-click atau klik icon kalender)")

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
        filter_aktif = self.checkbox_filter.isChecked()
        
        return {
            "url"          : self.input_url.text().strip(),
            "limit"        : self.input_limit.value(),
            "filter_aktif" : filter_aktif,
            "start_date"   : self.date_start.date() if filter_aktif else None,
            "end_date"     : self.date_end.date() if filter_aktif else None,
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
        inputs = self.get_inputs()
        
        # Validasi 1: URL tidak boleh kosong
        if not inputs["url"]:
            QMessageBox.warning(
                self, 
                "Input Error", 
                "URL tidak boleh kosong!\n\nContoh: https://www.cnnindonesia.com"
            )
            self.input_url.setFocus()
            return False
        
        # Validasi 2: URL harus diawali http:// atau https://
        if not inputs["url"].startswith(("http://", "https://")):
            QMessageBox.warning(
                self,
                "Input Error",
                "URL harus diawali dengan 'http://' atau 'https://'\n\nContoh: https://www.cnnindonesia.com"
            )
            self.input_url.setFocus()
            return False
        
        # Validasi 3: Jika filter aktif, date_end tidak boleh sebelum date_start
        if inputs["filter_aktif"]:
            if inputs["end_date"] < inputs["start_date"]:
                QMessageBox.warning(
                    self,
                    "Input Error",
                    "Tanggal selesai ('Sampai') tidak boleh sebelum tanggal mulai ('Dari')!"
                )
                self.date_end.setFocus()
                return False
        
        # Semua validasi berhasil
        return True

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

    KOLOM_TABEL = ["No", "Judul", "Tanggal", "Penulis", "Kategori", "URL", "Gambar", "Isi"]
    # Kolom "Isi" ditampilkan singkat (150 karakter). Double-click baris untuk lihat isi lengkap.

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
        # Double-click baris → tampilkan isi lengkap
        self.tabel.cellDoubleClicked.connect(self._lihat_detail)
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

        # Konversi QDate → datetime.date agar kompatibel dengan filter.py
        if inputs["start_date"] is not None:
            inputs["start_date"] = inputs["start_date"].toPyDate()
        if inputs["end_date"] is not None:
            inputs["end_date"] = inputs["end_date"].toPyDate()

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

        # Kolom Isi — tampilkan 150 karakter pertama, double-click untuk lihat lengkap
        isi_raw = artikel.get("isi", "")
        isi_singkat = isi_raw[:150] + ("..." if len(isi_raw) > 150 else "")
        self.tabel.setItem(row, 7, QTableWidgetItem(isi_singkat))

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

    def _lihat_detail(self, row: int, col: int) -> None:
        """
        Tampilkan dialog popup isi lengkap artikel saat baris di-double-click.

        Args:
            row: indeks baris yang diklik
            col: indeks kolom yang diklik (tidak dipakai)
        """
        if row >= len(self.data_hasil):
            return

        artikel = self.data_hasil[row]

        dialog = QDialog(self)
        dialog.setWindowTitle(artikel.get("judul", "Detail Artikel")[:80])
        dialog.resize(700, 500)

        layout = QVBoxLayout(dialog)

        # ─── Info singkat (meta artikel) ────────────────────────
        info_html = (
            f"<b>Tanggal:</b> {artikel.get('tanggal', '-')} &nbsp;|&nbsp; "
            f"<b>Penulis:</b> {artikel.get('penulis', '-')} &nbsp;|&nbsp; "
            f"<b>Kategori:</b> {artikel.get('kategori', '-')}<br>"
            f"<b>URL:</b> <a href='{artikel.get('url', '')}' style='color:#2980b9;'>"
            f"{artikel.get('url', '-')}</a>"
        )
        label_info = QLabel(info_html)
        label_info.setWordWrap(True)
        label_info.setOpenExternalLinks(True)
        label_info.setTextFormat(Qt.RichText)
        layout.addWidget(label_info)

        # ─── Isi artikel (teks lengkap) ─────────────────────────
        layout.addWidget(QLabel("<b>Isi Artikel:</b>"))
        text_isi = QTextBrowser()
        text_isi.setPlainText(artikel.get("isi", "-"))
        text_isi.setReadOnly(True)
        layout.addWidget(text_isi)

        # ─── Tombol tutup ────────────────────────────────────────
        btn_tutup = QPushButton("Tutup")
        btn_tutup.clicked.connect(dialog.accept)
        layout.addWidget(btn_tutup)

        dialog.exec_()

    def export_csv(self) -> None:
        """Panggil exporter.export_csv() dengan self.data_hasil."""
        try:
            path = exporter.export_csv(self.data_hasil, "hasil_scraping")
            QMessageBox.information(self, "Sukses", f"Data berhasil diexport ke CSV:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    def export_excel(self) -> None:
        """Panggil exporter.export_excel() dengan self.data_hasil."""
        try:
            path = exporter.export_excel(self.data_hasil, "hasil_scraping")
            QMessageBox.information(self, "Sukses", f"Data berhasil diexport ke Excel:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))
