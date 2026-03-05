# 💬 PROMPT_GUIDE.md — Template Prompt AI per Anggota
> Salin template sesuai namamu → paste ke AI (Claude/ChatGPT/Cursor) → tulis pertanyaanmu di bawahnya
> Selalu sertakan kode yang sudah ada agar AI tidak jawab asal!

---

## 🔴 DARVA — scraper.py · worker.py · filter.py · main.py

### Template Dasar
```
Saya Darva, Lead Developer proyek News Scraper App.

KONTEKS PROYEK:
- Stack: Python, Selenium, PyQt5>=5.15
- Saya mengerjakan: [scraper.py / worker.py / filter.py / main.py]

FORMAT DATA ARTIKEL yang disepakati tim:
artikel = {
    "judul": str, "tanggal": str, "isi": str (maks 500 char),
    "url": str, "penulis": str, "kategori": str, "gambar_url": str
}
Field tidak ada → "-"  |  BUKAN None atau ""

FUNGSI WAJIB di scraper.py:
- setup_driver()              → Chrome headless
- get_all_links(driver, url, limit)  → list URL artikel
- scrape_article(driver, url) → dict artikel
- handle_pagination()         → ikuti halaman berikutnya
- is_artikel_valid(artikel)   → cek judul & isi tidak kosong
  (threshold dari config: MIN_JUDUL_CHARS=5, MIN_ISI_CHARS=20)

KETENTUAN WAJIB:
- Selector umum (h1, article, time) — JANGAN hardcode nama website
- Delay 1.5 detik antar request
- Headless mode, pakai webdriver-manager

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

### Contoh Pertanyaan yang Bagus untuk Darva
```
# Scraper
"Tolong buatkan fungsi get_all_links() yang mencari semua link artikel
 dari halaman menggunakan selector umum, tidak hardcode untuk website tertentu"

"Fungsi scrape_article() saya return semua '-' padahal websitenya ada konten.
 Kemungkinan masalahnya apa dan bagaimana solusinya?"

"Tolong buatkan strategi handle_pagination() yang mencoba 4 metode:
 rel=next, teks tombol Next/Selanjutnya, pola URL page=N, lalu berhenti"

# Worker
"Tolong buatkan class ScraperWorker(QThread) dengan 5 sinyal:
 sinyal_progress(int), sinyal_hasil(dict), sinyal_selesai(int),
 sinyal_error(str), sinyal_status(str)"

"Bagaimana cara tambahkan ThreadPoolExecutor(max_workers=3) ke worker.py
 supaya scraping beberapa artikel sekaligus?"

# Filter
"Tolong buatkan parse_tanggal() yang support format:
 '04 Mar 2025', '4 Maret 2025', '2025-03-04', '04/03/2025'"
```

---

## 🟠 KEMAL — config.py · logger.py · exporter.py

### Template Dasar
```
Saya Kemal, Data & Reliability Developer proyek News Scraper App.

KONTEKS PROYEK:
- Stack: Python, PyQt5, pandas, openpyxl
- Saya mengerjakan: [config.py / logger.py / exporter.py]

CONFIG yang sudah ada (config.py):
DEFAULT_DELAY=1.5, DEFAULT_LIMIT=20, MAX_ISI_CHARS=500
MIN_JUDUL_CHARS=5, MIN_ISI_CHARS=20
FILTER_INCLUDE_UNKNOWN_DATE=True
FIELD_KOSONG="-"
OUTPUT_DIR="output/", LOG_FILE="logs/scraper.log"
CSV_HEADERS=["No","Judul","Tanggal","Penulis","Kategori","Isi","URL","Gambar_URL"]

FORMAT DATA ARTIKEL:
artikel = {
    "judul": str, "tanggal": str, "isi": str,
    "url": str, "penulis": str, "kategori": str, "gambar_url": str
}

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

### Contoh Pertanyaan yang Bagus untuk Kemal
```
# config.py — ini HARUS selesai HARI PERTAMA
"Tolong buatkan config.py lengkap dengan semua variabel ini:
 [paste daftar variabel dari blueprint]
 Tambahkan komentar penjelasan di tiap variabel"

# logger.py
"Tolong buatkan logger.py dengan fungsi setup_logger(), log_info(),
 log_error(), log_warning() yang menulis ke file logs/scraper.log
 DAN tampil di terminal sekaligus, dengan format timestamp"

# exporter.py
"Tolong buatkan export_csv(data, filename) menggunakan pandas.
 - data adalah list of dict dengan key: judul, tanggal, penulis, kategori, isi, url, gambar_url
 - Header CSV: ['No','Judul','Tanggal','Penulis','Kategori','Isi','URL','Gambar_URL']
 - Encoding: utf-8-sig (supaya Excel bisa baca)
 - Simpan ke folder output/"

"Tolong buatkan export_excel(data, filename) menggunakan openpyxl.
 - Sama dengan CSV tapi format .xlsx
 - Auto-width tiap kolom sesuai kontennya
 - Header row dengan background color biru"

# Test
"Tolong buatkan test sederhana di if __name__ == '__main__' untuk
 test export dengan 2 baris data dummy"
```

---

## 🔵 RICHARD — gui.py (Main Window, Tabel, Tombol, Progress Bar)

### Template Dasar
```
Saya Richard, GUI Developer proyek News Scraper App.
Saya mengerjakan bagian fungsional gui.py (main window, tabel, tombol, progress bar).

KONTEKS PROYEK:
- Framework: PyQt5>=5.15 (BUKAN PyQt6!)
- File ini: gui.py — class MainWindow

KOMPONEN YANG SAYA BUAT:
- QMainWindow (main window utama)
- QTableWidget (7 kolom: No, Judul, Tanggal, Penulis, Kategori, URL, Gambar)
- QProgressBar (0-100%)
- QPushButton: "Mulai Scraping", "Stop", "Export CSV", "Export Excel"
- QLabel: label_status (teks status), label_jumlah (counter artikel)
- self.worker = ScraperWorker(QThread) — disimpan di self, bukan variabel lokal!
- self.data_hasil = [] — list of dict semua artikel

SINYAL DARI WORKER yang harus disambungkan:
sinyal_progress(int) → update_progress()
sinyal_hasil(dict)   → tambah_baris()
sinyal_selesai(int)  → scraping_selesai()
sinyal_error(str)    → tampilkan_error()
sinyal_status(str)   → label_status.setText()

FORMAT DICT ARTIKEL:
{"judul": str, "tanggal": str, "penulis": str,
 "kategori": str, "isi": str, "url": str, "gambar_url": str}

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

### Contoh Pertanyaan yang Bagus untuk Richard
```
"Tolong buatkan skeleton class MainWindow(QMainWindow) dengan layout:
 - Panel atas: tempat untuk InputPanel (akan diisi Kyla)
 - Row tombol: Mulai Scraping | Stop | [spacer] | Export CSV | Export Excel
 - Progress bar + label status
 - QTableWidget 7 kolom di bawah"

"Tolong buatkan fungsi tambah_baris(self, artikel: dict) yang menerima
 sinyal dari worker dan menambahkan 1 baris ke QTableWidget.
 Kolom: No, Judul, Tanggal, Penulis, Kategori, URL, Gambar"

"Tolong buatkan fungsi mulai_scraping(self) yang:
 1. Ambil URL, limit, start_date, end_date dari self.input_panel
 2. Buat ScraperWorker dan simpan di self.worker
 3. Sambungkan semua sinyal
 4. Disable tombol Scrape, enable tombol Stop
 5. Jalankan worker.start()"

"Bagaimana cara export CSV dari self.data_hasil menggunakan
 fungsi export_csv() dari exporter.py dengan QFileDialog?"
```

---

## 🟣 KYLA — gui.py (Input Panel, Date Picker, Validasi)

### Template Dasar
```
Saya Kyla, GUI Developer proyek News Scraper App.
Saya mengerjakan bagian input di gui.py — class InputPanel.

KONTEKS PROYEK:
- Framework: PyQt5>=5.15 (BUKAN PyQt6!)
- File ini: gui.py — class InputPanel

KOMPONEN YANG SAYA BUAT:
- QLineEdit input_url      → input URL berita
- QSpinBox input_limit     → limit artikel, range 1-500, default 20
- QCheckBox checkbox_filter → aktifkan/nonaktifkan filter tanggal
- QDateEdit date_start     → tanggal mulai (disabled jika checkbox off)
- QDateEdit date_end       → tanggal selesai (disabled jika checkbox off)

METHODS yang harus ada:
- get_url() → str
- get_limit() → int  
- get_start_date() → datetime.date atau None
- get_end_date() → datetime.date atau None
- validasi() → str (pesan error) atau "" (jika valid)

ATURAN VALIDASI:
- URL tidak boleh kosong
- URL harus dimulai dengan http:// atau https://
- Kalau filter aktif: date_end tidak boleh sebelum date_start

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

### Contoh Pertanyaan yang Bagus untuk Kyla
```
"Tolong buatkan class InputPanel(QWidget) dengan QGroupBox berjudul
 'Pengaturan Scraping', berisi:
 - QLineEdit untuk URL dengan placeholder 'https://...'
 - QSpinBox untuk limit (1-500, default 20)
 - QCheckBox 'Filter Tanggal' + 2 QDateEdit (start & end)
 Sertakan method get_url(), get_limit(), get_start_date(), get_end_date()"

"Tolong buatkan fungsi toggle_filter(self, state) yang dipanggil
 saat QCheckBox berubah. Jika checked → date_start & date_end di-enable.
 Jika unchecked → keduanya di-disable (greyed out)."

"Tolong buatkan fungsi validasi(self) yang:
 - Cek URL tidak kosong
 - Cek URL dimulai http:// atau https://
 - Cek (kalau filter aktif) date_end tidak sebelum date_start
 - Return string pesan error, atau '' kalau semua valid"

"Bagaimana cara ambil nilai dari QDateEdit dan convert ke datetime.date
 di Python? Saya bingung karena QDateEdit return QDate, bukan datetime."
```

---

## 🟢 AULIA — style.py · README.md · requirements.txt · PDF laporan

### Template Dasar
```
Saya Aulia, UI Polish & Dokumentasi proyek News Scraper App.
Saya mengerjakan style.py dan dokumentasi.

KONTEKS PROYEK:
- Framework: PyQt5>=5.15
- File ini: [style.py / README.md / requirements.txt]

KOMPONEN GUI yang ada (perlu di-styling):
- QMainWindow, QGroupBox
- QLineEdit, QSpinBox, QDateEdit, QCheckBox
- QPushButton (4 tipe: primary/biru, danger/merah, success/hijau, disabled/abu)
- QProgressBar
- QTableWidget (dengan alternating row colors)
- QLabel, QStatusBar

ATURAN STYLING:
- Pakai QSS (mirip CSS tapi untuk PyQt5)
- Warna primer bisa dipilih bebas — yang penting konsisten
- Jangan terlalu fancy, yang penting clean dan rapi
- apply_style(app) harus dipanggil di main.py SEBELUM MainWindow dibuat

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

### Contoh Pertanyaan yang Bagus untuk Aulia
```
# style.py
"Tolong buatkan MAIN_STYLESHEET untuk PyQt5 dengan tema gelap.
 Komponen: QMainWindow, QGroupBox, QLineEdit, QSpinBox, QDateEdit,
 QCheckBox, QPushButton (4 varian), QProgressBar, QTableWidget, QLabel.
 Warna primer: biru #2563EB, background: #1e1e2e"

"Tolong buatkan QSS untuk QPushButton dengan 4 class berbeda:
 .btn-primary (biru), .btn-danger (merah), .btn-success (hijau), .btn-disabled (abu)
 Sertakan juga hover state untuk tiap tombol"

"Tolong buatkan QSS untuk QTableWidget dengan:
 - Header row warna biru
 - Alternating row: putih dan abu muda
 - Selected row warna biru muda
 - Font ukuran 11px"

# README.md
"Tolong buatkan README.md untuk aplikasi News Scraper dengan:
 - Judul + deskripsi singkat
 - Cara install (pip install -r requirements.txt)
 - Cara menjalankan (python main.py)
 - Daftar fitur
 - Screenshot (placeholder)
 - Struktur file"

# requirements.txt
"Tolong pastikan requirements.txt ini sudah benar untuk runtime saja:
selenium, PyQt5>=5.15.0, pandas, openpyxl, webdriver-manager
Dan requirements-dev.txt untuk: pyqt5-tools"
```

---

## 💡 Tips Universal untuk Semua Anggota

### Kalau AI jawabnya tidak sesuai proyek:
```
"Jawaban kamu tidak sesuai kesepakatan tim kami. Di proyek kami:
 - Nama variabel untuk judul adalah 'judul' (bukan 'title')
 - Field tidak ada diisi '-' (bukan None)
 - Pakai PyQt5 (bukan PyQt6 atau tkinter)
 Tolong revisi sesuai ketentuan ini."
```

### Kalau mau minta penjelasan kode:
```
"Tolong jelaskan kode yang kamu buat baris per baris,
 karena saya masih belajar dan harus bisa menjelaskan ke dosen."
```

### Kalau ada error:
```
"Saya dapat error ini:
[paste error message LENGKAP]

Ini kode yang error:
[paste kode]

OS saya: [Windows/Mac/Linux]
Python version: [hasil python --version]
Tolong bantu debug."
```

### Kalau mau minta review kode:
```
"Tolong review kode saya ini.
 Cek apakah sudah sesuai kesepakatan tim:
 1. Nama field artikel (judul, tanggal, isi, url, penulis, kategori, gambar_url)
 2. Field kosong pakai '-' bukan None atau ''
 3. Tidak ada hardcode nama website
 4. Sudah ada try-except untuk field yang mungkin tidak ada"
```

---

*Simpan file ini di docs/ → buka setiap kali mau minta bantuan AI*
