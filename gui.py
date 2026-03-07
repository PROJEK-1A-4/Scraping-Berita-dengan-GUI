from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QSpinBox, QCheckBox, QDateEdit, QMessageBox,
    QHeaderView, QSizePolicy, QDialog, QTextBrowser,
    QMenuBar, QMenu, QAction, QFormLayout, QDoubleSpinBox, QGroupBox,
    QGridLayout, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QDate, QLocale
from PyQt5.QtGui import QFont, QPixmap, QIcon

import config
import worker as worker_module
import exporter

# ── Mapping bulan Indonesia untuk format tanggal ──────────────
_BULAN_ID = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}

def _format_tanggal(raw: str) -> str:
    """
    Konversi string tanggal mentah (ISO 8601 dsb.) ke format
    'dd MMMM yyyy, HH:mm WIB' yang mudah dibaca.

    Contoh:
        '2026-03-05T21:00:42Z'       → '05 Maret 2026, 21:00 WIB'
        '2026-03-05T21-00-42Z'       → '05 Maret 2026, 21:00 WIB'
        '2026-03-05'                 → '05 Maret 2026'
        'Rabu, 5 Mar 2026 10:30'     → tetap apa adanya (fallback)
    """
    if not raw or raw == config.FIELD_KOSONG:
        return raw

    from datetime import datetime, timezone, timedelta
    import re

    text = raw.strip()

    # Normalisasi: ganti T21-00-42Z → T21:00:42Z (beberapa sumber pakai dash)
    # Pattern: huruf T diikuti digit-digit-digit lalu Z atau offset
    text = re.sub(
        r'T(\d{2})-(\d{2})-(\d{2})(\.\d+)?(Z|[+\-]\d{2}:\d{2})?',
        r'T\1:\2:\3\4\5',
        text
    )

    # Coba parse berbagai format ISO umum
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",           # 2026-03-05T21:00:42Z
        "%Y-%m-%dT%H:%M:%S%z",          # 2026-03-05T21:00:42+07:00
        "%Y-%m-%dT%H:%M:%S.%fZ",        # 2026-03-05T20:48:39.000Z
        "%Y-%m-%dT%H:%M:%S.%f%z",       # 2026-03-05T20:48:39.000+07:00
        "%Y-%m-%dT%H:%M:%S",            # 2026-03-05T21:00:42
        "%Y/%m/%d %H:%M:%S",            # 2026/03/05 19:07:34 (CNN Indonesia)
        "%Y-%m-%d %H:%M:%S",            # 2026-03-05 21:00:42
        "%Y-%m-%d",                     # 2026-03-05
        "%d %b %Y %I:%M%p",             # 03 Mar 2026 04:01pm (CNA)
        "%d %b %Y %I:%M %p",            # 03 Mar 2026 04:01 pm
        "%d %b %Y",                     # 03 Mar 2026
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            hari = f"{dt.day:02d}"
            bulan = _BULAN_ID.get(dt.month, str(dt.month))
            tahun = dt.year
            if dt.hour or dt.minute:
                return f"{hari} {bulan} {tahun}, {dt.hour:02d}:{dt.minute:02d} WIB"
            return f"{hari} {bulan} {tahun}"
        except ValueError:
            continue

    # Fallback: kembalikan apa adanya
    return raw

class InputPanel(QWidget):
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

    def _get_label_font(self) -> QFont:
        font = QFont()
        font.setPointSize(10)
        font.setWeight(QFont.Medium)  # Semi-bold
        return font

    def _setup_ui(self) -> None:
        # Layout utama dengan margin dan spacing
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)  # padding di semua sisi
        layout.setSpacing(10)  # spacing antar widget

        # Tambahkan semua sub-layout menggunakan helper methods
        layout.addLayout(self._create_url_layout())
        layout.addLayout(self._create_limit_layout())
        layout.addWidget(self._create_date_filter_layout())
        layout.addLayout(self._create_date_range_layout())

        # Hubungkan checkbox signal ke toggle method
        self.checkbox_filter.stateChanged.connect(self._toggle_date_filter)

        # Add stretch di akhir agar widget tidak mengambil full height
        layout.addStretch()

    def _create_url_layout(self) -> QHBoxLayout:
        url_layout = QHBoxLayout()
        url_layout.setSpacing(8)  # spacing antar widget
        
        label_url = QLabel("URL:")
        label_url.setFixedWidth(60)
        label_url.setFont(self._get_label_font())  # Apply label styling
        
        self.input_url.setPlaceholderText("https://www.cnnindonesia.com")
        self.input_url.setMinimumHeight(36)  # Increased for better visibility
        self.input_url.setClearButtonEnabled(True)  # Built-in clear button
        
        url_layout.addWidget(label_url)
        url_layout.addWidget(self.input_url)
        return url_layout

    def _create_limit_layout(self) -> QHBoxLayout:
        limit_layout = QHBoxLayout()
        limit_layout.setSpacing(8)  # spacing antar widget
        
        label_limit = QLabel("Limit:")
        label_limit.setFixedWidth(60)
        label_limit.setFont(self._get_label_font())  # Apply label styling
        
        self.input_limit.setRange(1, 500)
        self.input_limit.setValue(config.DEFAULT_LIMIT)
        self.input_limit.setMinimumHeight(36)   # Sedikit lebih tinggi agar tombol terlihat
        self.input_limit.setMaximumWidth(120)   # Max width untuk spinbox
        self.input_limit.setAlignment(Qt.AlignCenter)  # Angka di tengah
        self.input_limit.setButtonSymbols(QSpinBox.PlusMinus)  # Gunakan simbol +/−
        
        label_artikel = QLabel("artikel")
        label_artikel.setStyleSheet("color: #8A99B6; font-size: 12px; padding-left: 4px; font-weight: 500;")
        
        limit_layout.addWidget(label_limit)
        limit_layout.addWidget(self.input_limit)
        limit_layout.addWidget(label_artikel)
        limit_layout.addStretch()  # Push ke kiri
        return limit_layout

    def _create_date_filter_layout(self) -> QCheckBox:
        self.checkbox_filter.setToolTip("Centang untuk mengaktifkan filter tanggal (artikel antara Dari dan Sampai)")
        self.checkbox_filter.setChecked(False)  # Explicit default unchecked
        return self.checkbox_filter

    def _create_date_range_layout(self) -> QHBoxLayout:
        date_layout = QHBoxLayout()
        date_layout.setSpacing(8)  # spacing antar widget
        
        label_dari = QLabel("Dari:")
        label_dari.setFixedWidth(60)
        label_dari.setFont(self._get_label_font())  # Apply label styling
        
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setEnabled(False)
        self.date_start.setDisplayFormat("dd MMMM yyyy")  # Format lengkap: 05 Maret 2026
        self.date_start.setLocale(QLocale(QLocale.Indonesian, QLocale.Indonesia))
        self.date_start.setCalendarPopup(True)  # Popup calendar saat diklik
        self.date_start.setMinimumHeight(36)  # Match other widgets + 4px
        self.date_start.setMinimumWidth(180)  # Lebar cukup untuk nama bulan
        self.date_start.setToolTip("Pilih tanggal awal (Double-click atau klik icon kalender)")

        label_sampai = QLabel("Sampai:")
        label_sampai.setFont(self._get_label_font())  # Apply label styling
        
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setEnabled(False)
        self.date_end.setDisplayFormat("dd MMMM yyyy")  # Format lengkap: 05 Maret 2026
        self.date_end.setLocale(QLocale(QLocale.Indonesian, QLocale.Indonesia))
        self.date_end.setCalendarPopup(True)  # Popup calendar saat diklik
        self.date_end.setMinimumHeight(36)  # Match other widgets + 4px
        self.date_end.setToolTip("Pilih tanggal akhir (Double-click atau klik icon kalender)")

        date_layout.addWidget(label_dari)
        date_layout.addWidget(self.date_start)
        date_layout.addWidget(label_sampai)
        date_layout.addWidget(self.date_end)
        date_layout.addStretch()  # Push ke kiri
        return date_layout

    def get_inputs(self) -> dict:
        filter_aktif = self.checkbox_filter.isChecked()
        
        # Normalize URL: strip whitespace dan convert scheme ke lowercase
        raw_url = self.input_url.text().strip()
        normalized_url = self._normalize_url(raw_url) if raw_url else ""
        
        return {
            "url"          : normalized_url,
            "limit"        : self.input_limit.value(),
            "filter_aktif" : filter_aktif,
            "start_date"   : self.date_start.date() if filter_aktif else None,
            "end_date"     : self.date_end.date() if filter_aktif else None,
        }

    def _normalize_url(self, url: str) -> str:
        url = url.strip()
        if url.lower().startswith("https://"):
            return "https://" + url[8:]
        elif url.lower().startswith("http://"):
            return "http://" + url[7:]
        return url

    def validate(self) -> bool:
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
        
        # Validasi 3: URL harus memiliki domain yang valid (bukan hanya https:// atau http://)
        url_after_protocol = inputs["url"][8:] if inputs["url"].startswith("https://") else inputs["url"][7:]
        if not url_after_protocol or url_after_protocol == "/":
            QMessageBox.warning(
                self,
                "Input Error",
                "URL harus memiliki domain yang valid!\n\nContoh: https://www.cnnindonesia.com"
            )
            self.input_url.setFocus()
            return False
        
        # Validasi 4: Jika filter aktif, date_end tidak boleh sebelum date_start (sama boleh)
        if inputs["filter_aktif"]:
            if inputs["end_date"] < inputs["start_date"]:
                QMessageBox.warning(
                    self,
                    "Input Error",
                    "Tanggal selesai ('Sampai') tidak boleh sebelum tanggal mulai ('Dari')!"
                )
                self.date_end.setFocus()
                return False
        
        # Validasi 5: Limit artikel harus dalam range 1-500
        if inputs["limit"] < 1 or inputs["limit"] > 500:
            QMessageBox.warning(
                self,
                "Input Error",
                "Limit artikel harus antara 1 dan 500!"
            )
            self.input_limit.setFocus()
            return False
        
        # Semua validasi berhasil
        return True

    def _toggle_date_filter(self, state: int) -> None:
        aktif = (state == Qt.Checked)
        self.date_start.setEnabled(aktif)
        self.date_end.setEnabled(aktif)


# ══════════════════════════════════════════════════════════════
#  BAGIAN RICHARD — MainWindow
# ══════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    # Urutan kolom sesuai mockup: #, Judul, Tanggal, Penulis, Kategori, Isi (preview), URL
    # Kolom Gambar dihapus dari tabel — gambar ditampilkan di dialog detail (double-click)
    # CATATAN: Berbeda dengan CSV_HEADERS di config.py yang menyertakan kolom Gambar_URL untuk export
    KOLOM_TABEL = ["#", "Judul", "Tanggal", "Penulis", "Kategori", "Isi (preview)", "URL"]

    def __init__(self):

        super().__init__()

        # ─── State aplikasi ────────────────────────────────────────
        self.data_hasil: list[dict] = []    # artikel valid yang terkumpul
        self.worker = None                  # ScraperWorker — SIMPAN DI SINI!

        # ─── Widget declaration ────────────────────────────────────
        self.input_panel    = InputPanel()
        self.tabel          = QTableWidget()
        self.progress_bar   = QProgressBar()
        self.btn_scrape     = QPushButton("▶  Mulai Scraping")
        self.btn_stop       = QPushButton("■  Stop")
        self.btn_export_csv = QPushButton("↓  Export CSV")
        self.btn_export_xl  = QPushButton("↓  Export Excel")
        self.label_status   = QLabel("Menampilkan 0 artikel")
        self.label_jumlah   = QLabel("0 artikel")
        # Bottom status bar labels
        self.label_dot      = QLabel("●")
        self.label_state    = QLabel("SIAP")
        self.label_delay    = QLabel(f"DELAY: {config.DEFAULT_DELAY}s")
        self.label_headless = QLabel(f"HEADLESS: {'ON' if config.HEADLESS else 'OFF'}")
        self.label_logfile  = QLabel(str(config.LOG_FILE))
        # Set object names for per-button styling
        self.btn_stop.setObjectName("btn_stop")
        self.btn_export_csv.setObjectName("btn_export_csv")
        self.btn_export_xl.setObjectName("btn_export_xl")

        self._setup_menu_bar()
        self._setup_ui()
        self._connect_signals()
        self._set_state_idle()  

    def _setup_menu_bar(self) -> None:
        """Buat menu bar: File, Pengaturan, Tentang."""
        menubar = self.menuBar()
        menubar.setObjectName("main_menubar")

        # ─── Menu File ────────────────────────────────────────
        menu_file = menubar.addMenu("File")

        self.act_scrape = QAction("▶  Mulai Scraping", self)
        self.act_scrape.setShortcut("Ctrl+R")
        self.act_scrape.triggered.connect(lambda: self.mulai_scraping())
        menu_file.addAction(self.act_scrape)

        self.act_stop = QAction("■  Stop Scraping", self)
        self.act_stop.setShortcut("Ctrl+Q")
        self.act_stop.triggered.connect(lambda: self.stop_scraping())
        menu_file.addAction(self.act_stop)

        menu_file.addSeparator()

        act_csv = QAction("↓  Export CSV", self)
        act_csv.setShortcut("Ctrl+Shift+C")
        act_csv.triggered.connect(lambda: self.export_csv())
        menu_file.addAction(act_csv)

        act_xl = QAction("↓  Export Excel", self)
        act_xl.setShortcut("Ctrl+Shift+E")
        act_xl.triggered.connect(lambda: self.export_excel())
        menu_file.addAction(act_xl)

        menu_file.addSeparator()

        act_keluar = QAction("Keluar", self)
        act_keluar.setShortcut("Ctrl+W")
        act_keluar.triggered.connect(self.close)
        menu_file.addAction(act_keluar)

        # ─── Menu Pengaturan ──────────────────────────────────
        menu_pengaturan = menubar.addMenu("Pengaturan")

        act_setting = QAction("⚙  Konfigurasi Scraping", self)
        act_setting.triggered.connect(self._buka_pengaturan)
        menu_pengaturan.addAction(act_setting)

        # ─── Menu Tentang ─────────────────────────────────────
        menu_tentang = menubar.addMenu("Tentang")

        act_about = QAction("ℹ  Tentang Aplikasi", self)
        act_about.triggered.connect(self._buka_tentang)
        menu_tentang.addAction(act_about)

        act_tim = QAction("👥  Tim Pengembang", self)
        act_tim.triggered.connect(self._buka_tim)
        menu_tentang.addAction(act_tim)

    def _buka_pengaturan(self) -> None:
        """Buka dialog pengaturan scraping."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Konfigurasi Scraping")
        dialog.setFixedSize(500, 340)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # ─── Judul ────────────────────────────────────────────
        title = QLabel("⚙  Konfigurasi Scraping")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #E8EAF0; padding-bottom: 4px;")
        layout.addWidget(title)

        # ─── Form ─────────────────────────────────────────────
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        # Delay
        spin_delay = QDoubleSpinBox()
        spin_delay.setRange(0.5, 10.0)
        spin_delay.setSingleStep(0.5)
        spin_delay.setValue(config.DEFAULT_DELAY)
        spin_delay.setSuffix(" detik")
        spin_delay.setDecimals(1)
        label_delay = QLabel("Delay antar request:")
        label_delay.setStyleSheet("color: #E8EAF0; font-size: 12px;")
        form.addRow(label_delay, spin_delay)

        # Headless
        chk_headless = QCheckBox("Mode Headless")
        chk_headless.setToolTip("Jalankan browser tanpa tampilan (lebih cepat)")
        chk_headless.setChecked(config.HEADLESS)
        label_headless = QLabel("Browser:")
        label_headless.setStyleSheet("color: #E8EAF0; font-size: 12px;")
        form.addRow(label_headless, chk_headless)

        # Keterangan headless
        lbl_note = QLabel("Tanpa tampilan browser, proses lebih cepat")
        lbl_note.setStyleSheet("color: #6B7699; font-size: 10px; padding-left: 2px;")
        form.addRow(QLabel(""), lbl_note)

        # Page Load Wait
        spin_wait = QSpinBox()
        spin_wait.setRange(5, 60)
        spin_wait.setValue(config.PAGE_LOAD_WAIT)
        spin_wait.setSuffix(" detik")
        label_wait = QLabel("Timeout halaman:")
        label_wait.setStyleSheet("color: #E8EAF0; font-size: 12px;")
        form.addRow(label_wait, spin_wait)

        # Max Isi Chars
        spin_isi = QSpinBox()
        spin_isi.setRange(500, 10000)
        spin_isi.setSingleStep(500)
        spin_isi.setValue(config.MAX_ISI_CHARS)
        spin_isi.setSuffix(" karakter")
        label_isi = QLabel("Maks isi artikel:")
        label_isi.setStyleSheet("color: #E8EAF0; font-size: 12px;")
        form.addRow(label_isi, spin_isi)

        layout.addLayout(form)
        layout.addStretch()

        # Tombol Simpan & Batal
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_batal = QPushButton("Batal")
        btn_batal.setObjectName("btn_stop")
        btn_batal.setFixedWidth(100)
        btn_batal.clicked.connect(dialog.reject)
        btn_layout.addWidget(btn_batal)

        btn_simpan = QPushButton("Simpan")
        btn_simpan.setFixedWidth(100)
        btn_layout.addWidget(btn_simpan)

        layout.addLayout(btn_layout)

        def simpan():
            config.DEFAULT_DELAY = spin_delay.value()
            config.HEADLESS = chk_headless.isChecked()
            config.PAGE_LOAD_WAIT = spin_wait.value()
            config.MAX_ISI_CHARS = spin_isi.value()
            # Update bottom bar
            self.label_delay.setText(f"DELAY: {config.DEFAULT_DELAY}s")
            self.label_headless.setText(f"HEADLESS: {'ON' if config.HEADLESS else 'OFF'}")
            dialog.accept()

        btn_simpan.clicked.connect(simpan)
        dialog.exec_()

    def _buka_tentang(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Tentang Aplikasi")
        dialog.setFixedSize(config.DIALOG_W, config.DIALOG_H)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        # Icon / Judul
        title = QLabel("📰  News Scraper App")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4F8EF7;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Versi
        ver = QLabel("Versi 1.0.0")
        ver.setStyleSheet("font-size: 12px; color: #6B7699;")
        ver.setAlignment(Qt.AlignCenter)
        layout.addWidget(ver)

        layout.addSpacing(8)

        # Deskripsi
        desc = QLabel(
            "Aplikasi desktop berbasis Python untuk mengambil data berita\n"
            "secara otomatis dari website berita Indonesia.\n\n"
            "User cukup memasukkan URL, aplikasi akan mengambil\n"
            "semua artikel beserta isinya dan menampilkan hasilnya\n"
            "dalam tabel yang rapi."
        )
        desc.setStyleSheet("font-size: 12px; color: #E8EAF0; line-height: 1.5;")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addSpacing(4)

        # Stack
        stack = QLabel("Python 3.12  •  Selenium  •  PyQt5  •  pandas")
        stack.setStyleSheet("font-size: 11px; color: #00D4AA; font-family: monospace;")
        stack.setAlignment(Qt.AlignCenter)
        layout.addWidget(stack)

        layout.addStretch()

        # Tombol tutup
        btn_tutup = QPushButton("Tutup")
        btn_tutup.setFixedWidth(120)
        btn_tutup.clicked.connect(dialog.accept)
        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(btn_tutup)
        h.addStretch()
        layout.addLayout(h)

        dialog.exec_()

    def _buka_tim(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Tim Pengembang")
        dialog.resize(config.DIALOG_W + 180, config.DIALOG_H + 220)
        dialog.setMinimumSize(config.DIALOG_W + 120, config.DIALOG_H + 160)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("👥  Tim Pengembang")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4F8EF7;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Proyek 1: Pengembangan Perangkat Lunak Desktop")
        subtitle.setStyleSheet("font-size: 11px; color: #6B7699;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        # Daftar anggota tim
        tim = [
            ("Darva Aryasatya Putra Hermawan - 251524006",   "Lead Developer + Reviewer",         "#4F8EF7"),
            ("Kemal Melvin Ibrahim - 251524017",   "Data & Reliability Developer",      "#00D4AA"),
            ("Richard Fadhilah Irwandi Putra - 251524028", "GUI Developer (Fungsional)",         "#F7C948"),
            ("Kyla Khansa - 251524018",    "GUI Developer (Input & Filter)",     "#F75A5A"),
            ("Aulia Rahmi Taufik - 251524003",   "UI Polish + Dokumentasi",            "#C084FC"),
            ("Muhammad Rizqi Sholahuddin - 199105302019031019", "Manager Proyek", "#6B7699"),
        ]

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        for nama, peran, warna in tim:
            card = QFrame()
            card.setObjectName("tim_card")
            card.setMinimumHeight(72)
            card.setStyleSheet(
                f"QFrame#tim_card {{"
                f"  background-color: #1E2333;"
                f"  border: 1px solid #2A3147;"
                f"  border-left: 3px solid {warna};"
                f"  border-radius: 6px;"
                f"  padding: 8px 12px;"
                f"}}"
            )
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(12, 6, 12, 6)

            # Gunakan layout vertikal agar nama/NIM panjang tidak terpotong.
            text_layout = QVBoxLayout()
            text_layout.setSpacing(2)

            lbl_nama = QLabel(nama)
            lbl_nama.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {warna}; background: transparent;")
            lbl_nama.setWordWrap(True)

            lbl_peran = QLabel(peran)
            lbl_peran.setStyleSheet("font-size: 12px; color: #E8EAF0; background: transparent;")
            lbl_peran.setWordWrap(True)

            text_layout.addWidget(lbl_nama)
            text_layout.addWidget(lbl_peran)

            card_layout.addLayout(text_layout, 1)

            list_layout.addWidget(card)

        list_layout.addStretch()
        scroll.setWidget(list_container)
        layout.addWidget(scroll, 1)

        btn_tutup = QPushButton("Tutup")
        btn_tutup.setFixedWidth(120)
        btn_tutup.clicked.connect(dialog.accept)
        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(btn_tutup)
        h.addStretch()
        layout.addLayout(h)

        dialog.exec_()

    def _setup_ui(self) -> None:
        # Setup central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 8)

        # ─── 1. Input Panel (Kyla) ────────────────────────────────
        main_layout.addWidget(self.input_panel)

        # ─── 2. Tombol ( sesuai mockup: kiri scrape+stop, kanan export ) ─
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        buttons_layout.addWidget(self.btn_scrape)
        buttons_layout.addWidget(self.btn_stop)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_export_csv)
        buttons_layout.addWidget(self.btn_export_xl)
        main_layout.addLayout(buttons_layout)

        # ─── 3. Progress Row ( status kiri, bar tengah, % kanan ) ────────
        progress_row = QHBoxLayout()
        progress_row.setSpacing(10)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setTextVisible(True)
        progress_row.addWidget(self.label_status)
        progress_row.addWidget(self.progress_bar, stretch=1)
        main_layout.addLayout(progress_row)

        # ─── 4. Tabel header row ( counter artikel ) ──────────────────────
        table_header_row = QHBoxLayout()
        table_header_row.addWidget(self.label_jumlah)
        table_header_row.addStretch()
        main_layout.addLayout(table_header_row)

        # ─── 5. Tabel ─────────────────────────────────────────────────────
        self.tabel.setColumnCount(len(self.KOLOM_TABEL))
        self.tabel.setHorizontalHeaderLabels(self.KOLOM_TABEL)
        self.tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabel.setAlternatingRowColors(True)
        self.tabel.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabel.verticalHeader().setVisible(False)
        self.tabel.horizontalHeader().setHighlightSections(False)
        # Column widths: Judul(1) dan Isi(5) stretch, sisanya ResizeToContents
        hdr = self.tabel.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # #
        hdr.setSectionResizeMode(1, QHeaderView.Stretch)            # Judul
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Tanggal
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Penulis
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Kategori
        hdr.setSectionResizeMode(5, QHeaderView.Stretch)            # Isi
        hdr.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # URL
        main_layout.addWidget(self.tabel, stretch=1)

        # ─── 6. Bottom status bar ( sesuai mockup ) ───────────────────────
        bottom_bar = QWidget()
        bottom_bar.setObjectName("bottom_bar")
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(8, 4, 8, 4)
        bottom_layout.setSpacing(16)
        self.label_dot.setObjectName("label_dot_active" if False else "label_dot_idle")
        bottom_layout.addWidget(self.label_dot)
        bottom_layout.addWidget(self.label_state)
        bottom_layout.addWidget(QLabel("|"))
        bottom_layout.addWidget(self.label_delay)
        bottom_layout.addWidget(self.label_headless)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.label_logfile)
        main_layout.addWidget(bottom_bar)

        self.setWindowTitle(config.APP_TITLE)
        self.resize(config.WINDOW_W, config.WINDOW_H)
        pass

    def _connect_signals(self) -> None:
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
        self.btn_scrape.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_export_csv.setEnabled(len(self.data_hasil) > 0)
        self.btn_export_xl.setEnabled(len(self.data_hasil) > 0)
        # Update bottom status bar
        self.label_dot.setObjectName("label_dot_idle")
        self.label_dot.setStyleSheet("color: #6B7699;")
        self.label_state.setText("SIAP")
        self.label_state.setStyleSheet("color: #6B7699; font-family: monospace; font-size: 11px;")
        pass

    def _set_state_scraping(self) -> None:
        """Set state GUI saat sedang scraping."""                           #(DONE)
        self.btn_scrape.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_export_csv.setEnabled(False)
        self.btn_export_xl.setEnabled(False)
        # Update bottom status bar
        self.label_dot.setStyleSheet("color: #00D4AA;")
        self.label_state.setText("SCRAPING AKTIF")
        self.label_state.setStyleSheet("color: #00D4AA; font-family: monospace; font-size: 11px; font-weight: bold;")
        pass

    def mulai_scraping(self) -> None:
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
        # self.data_hasil.append(artikel)
        self.data_hasil.append(artikel)
        # row = self.tabel.rowCount()
        row = self.tabel.rowCount()
        # self.tabel.insertRow(row)
        self.tabel.insertRow(row)

        # Urutan kolom: #(0), Judul(1), Tanggal(2), Penulis(3), Kategori(4), Isi(5), URL(6)
        no_item = QTableWidgetItem(f"{row + 1:02d}")
        no_item.setTextAlignment(Qt.AlignCenter)
        self.tabel.setItem(row, 0, no_item)
        self.tabel.setItem(row, 1, QTableWidgetItem(artikel.get("judul", "")))
        self.tabel.setItem(row, 2, QTableWidgetItem(_format_tanggal(artikel.get("tanggal", ""))))
        self.tabel.setItem(row, 3, QTableWidgetItem(artikel.get("penulis", "")))
        self.tabel.setItem(row, 4, QTableWidgetItem(artikel.get("kategori", "")))

        # Kolom Isi — preview 150 karakter, double-click untuk lihat lengkap
        isi_raw = artikel.get("isi", "")
        isi_singkat = isi_raw[:150] + ("..." if len(isi_raw) > 150 else "")
        self.tabel.setItem(row, 5, QTableWidgetItem(isi_singkat))

        self.tabel.setItem(row, 6, QTableWidgetItem(artikel.get("url", "")))

        self.label_jumlah.setText(f"Menampilkan {len(self.data_hasil)} artikel")
        self.label_status.setText(f"Menampilkan {len(self.data_hasil)} artikel")
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
        self.label_jumlah.setText(f"Menampilkan {jumlah} artikel")
        self._set_state_idle()
        pass

    def tampilkan_error(self, pesan: str) -> None:
        """Dipanggil saat worker emit sinyal_error."""                      #(YET TO BE TESTED)
        # TODO Richard: tampilkan QMessageBox.critical, set state idle       (DONE)

        QMessageBox.critical(self, "Error", pesan)
        self._set_state_idle()
        pass

    def _lihat_detail(self, row: int, col: int) -> None:
        if row >= len(self.data_hasil):
            return

        artikel = self.data_hasil[row]

        dialog = QDialog(self)
        dialog.setWindowTitle(artikel.get("judul", "Detail Artikel")[:80])
        dialog.resize(config.DETAIL_DLG_W, config.DETAIL_DLG_H)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(8)

        # ─── Judul ───────────────────────────────────────────────
        label_judul = QLabel(f"<h3>{artikel.get('judul', '-')}</h3>")
        label_judul.setWordWrap(True)
        label_judul.setTextFormat(Qt.RichText)
        layout.addWidget(label_judul)

        # ─── Info meta ───────────────────────────────────────────
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

        # ─── Gambar artikel ──────────────────────────────────────
        gambar_url = artikel.get("gambar_url", "-")
        if gambar_url and gambar_url not in ("-", ""):
            import urllib.request
            try:
                req = urllib.request.Request(
                    gambar_url,
                    headers={"User-Agent": config.USER_AGENT}
                )
                data = urllib.request.urlopen(req, timeout=5).read()
                pixmap = QPixmap()
                if pixmap.loadFromData(data) and not pixmap.isNull():
                    label_img = QLabel()
                    # Scale gambar agar muat di dialog (max lebar 720px, jaga aspek ratio)
                    scaled = pixmap.scaledToWidth(
                        min(720, pixmap.width()),
                        Qt.SmoothTransformation
                    )
                    # Batasi tinggi max 260px
                    if scaled.height() > 260:
                        scaled = pixmap.scaledToHeight(260, Qt.SmoothTransformation)
                    label_img.setPixmap(scaled)
                    label_img.setAlignment(Qt.AlignCenter)
                    layout.addWidget(label_img)
            except Exception:
                pass  # Gambar gagal dimuat — lewati, tidak crash

        # ─── Isi artikel ─────────────────────────────────────────
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
        try:
            path = exporter.export_csv(self.data_hasil, "hasil_scraping")
            QMessageBox.information(self, "Sukses", f"Data berhasil diexport ke CSV:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    def export_excel(self) -> None:
        try:
            path = exporter.export_excel(self.data_hasil, "hasil_scraping")
            QMessageBox.information(self, "Sukses", f"Data berhasil diexport ke Excel:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))
