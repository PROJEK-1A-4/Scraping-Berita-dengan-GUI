# 📰 BLUEPRINT — News Scraper App

---

## 👥 Anggota Tim & Peran

| Nama | Peran |
|------|-------|
| **Darva** | Lead Developer + Reviewer |
| **Kemal** | Data & Reliability Dev |
| **Richard** | GUI Developer (Fungsional) |
| **Kyla** | GUI Developer (Input & Filter) |
| **Aulia** | UI Polish + Dokumentasi |

---

## 🎯 Deskripsi Aplikasi

Aplikasi desktop berbasis Python yang dapat **mengambil data berita secara otomatis** dari sebuah website berita Indonesia. User cukup memasukkan 1 URL, aplikasi akan mengambil semua artikel beserta isinya dan menampilkan hasilnya dalam tabel yang rapi.

**Stack:** Python 3.12, Selenium, PyQt5 ≥ 5.15, pandas, openpyxl, webdriver-manager
**Browser:** Google Chrome 145 (headless mode)

---

## 🎬 Alur Aplikasi (User Flow)

```
STEP 1: User buka aplikasi
        → Muncul window dark theme (#0F1117 bg) dengan form input

STEP 2: User isi form
        → Masukkan URL homepage/kategori berita
        → (Opsional) Pilih rentang tanggal: start date – end date
        → (Opsional) Set limit jumlah berita (1–500, default 20)

STEP 3: User klik tombol "▶  Mulai Scraping"
        → Validasi input (URL kosong? format salah? tanggal valid?)
        → Progress bar gradient biru→teal mulai bergerak
        → GUI tetap responsif (QThread), bottom bar "SCRAPING AKTIF"

STEP 4: Di balik layar — Selenium bekerja (3-layer extraction)
        4a. Buka URL → kumpulkan link artikel (same-domain, path_depth≥3)
            → filter 20+ NON_ARTIKEL keywords
            → Kalau ada pagination → ikuti (4 strategi)
        4b. Buka satu per satu link artikel → 3-layer extraction:
            → L1: OpenGraph + Schema.org meta tags (UNIVERSAL)
            → L2: wildcard [class*='...'] + semantic HTML5 (SEMI-UMUM)
            → L3: class spesifik Detik/Kompas/CNN (OPTIMASI)
        4c. Validasi: is_artikel_valid() — judul≥15ch, isi≥100ch
        4d. Filter tanggal (jika aktif) — parse multi-format ID/EN
        4e. Delay 1.5 detik antar request

STEP 5: Hasil muncul di tabel GUI secara real-time
        → 7 Kolom: #, Judul, Tanggal, Penulis, Kategori, Isi (preview 150ch), URL
        → Double-click baris → dialog detail: gambar asli + isi 2000ch + meta
        → Progress bar penuh = selesai ✅

STEP 6: User klik "Export"
        → Export CSV atau Excel (.xlsx)
        → File tersimpan di folder output/
```

---

## 🏗️ Arsitektur Aplikasi

```
main.py
  │
  ├── config.py          ← pengaturan global (Kemal)
  │     MAX_ISI_CHARS=2000, MIN_JUDUL=15, MIN_ISI=100
  │     CSV_ENCODING, EXCEL_ENGINE, LOG_FORMAT, LOG_LEVEL
  │
  ├── gui.py             ← tampilan aplikasi
  │     ├── [Kyla]       InputPanel: URL, limit, date picker, validasi
  │     └── [Richard]    MainWindow: tabel 7 kolom, progress bar, tombol,
  │                      bottom bar, dialog detail double-click
  │
  ├── style.py           ← Dark theme QSS (Aulia)
  │     #0F1117 bg, #4F8EF7 accent, #00D4AA teal, #F75A5A danger
  │
  ├── worker.py          ← QThread: 5 sinyal GUI ↔ scraper (Darva)
  │     sinyal_progress, sinyal_hasil, sinyal_selesai, sinyal_error, sinyal_status
  │
  ├── scraper.py         ← otak scraping — 3-layer extraction (Darva)
  │     ├── setup_driver()          headless Chrome + eager + anti-bot
  │     ├── get_all_links()         same-domain, path_depth≥3, 20+ NON_ARTIKEL kw
  │     ├── handle_pagination()     4 strategi (rel=next, teks, URL, berhenti)
  │     ├── scrape_article()        3-layer: OG/Schema → wildcard → site-specific
  │     ├── is_artikel_valid()      threshold dari config
  │     ├── _extract_text()         helper CSS/XPath selector
  │     └── _extract_meta()         helper OpenGraph/Schema.org/itemprop
  │
  ├── filter.py          ← filter tanggal multi-format ID/EN (Darva)
  │     parse_tanggal(), filter_by_date()
  │
  ├── exporter.py        ← export CSV & Excel (Kemal)
  │     export_csv(), export_excel()
  │
  └── logger.py          ← logging file + console (Kemal)
        setup_logger(), log_info(), log_error(), log_warning()
```

---

## 📁 Struktur Folder Project

```
news-scraper/
├── main.py                   ← entry point
├── config.py                 ← konstanta global
├── scraper.py                ← logika scraping 3-layer
├── worker.py                 ← QThread bridge
├── filter.py                 ← filter tanggal
├── gui.py                    ← InputPanel + MainWindow
├── style.py                  ← dark theme QSS
├── exporter.py               ← export CSV & Excel
├── logger.py                 ← logging
├── requirements.txt          ← runtime (untuk submit)
├── requirements-dev.txt      ← dev tools
├── test_scraper_cli.py       ← test CLI
├── test_results.txt          ← hasil test
├── gui-mockup (1).html       ← mockup desain
├── README.md
├── TekproWebScraping.iml
├── output/
│   └── hasil_scraping.csv
├── logs/
└── docs/
    ├── AI_CONTEXT.md
    ├── BLUEPRINT_NEWS_SCRAPER.md
    ├── COMMIT_GUIDE.md
    ├── PROMPT_GUIDE.md
    ├── TESTING_CHECKLIST.md
    ├── laporan.md
    └── screenshots/
```

---

## 🗂️ Struktur Data Artikel (KESEPAKATAN TIM)

```python
artikel = {
    # ── FIELD WAJIB ──────────────────────────────────────────
    "judul"     : str,   # Judul artikel
    "tanggal"   : str,   # Apa adanya dari website
    "isi"       : str,   # Maksimal 2000 karakter pertama

    # ── FIELD BONUS ──────────────────────────────────────────
    "url"       : str,   # Full URL (https://...)
    "penulis"   : str,   # Nama penulis → "-" kalau tidak ada
    "kategori"  : str,   # Kategori → "-" kalau tidak ada
    "gambar_url": str,   # URL gambar utama → "-" kalau tidak ada
}
```

### Aturan Wajib:
- ✅ Field tidak ditemukan → isi `"-"` (BUKAN `None`, BUKAN `""`)
- ✅ Isi artikel → maksimal **2000 karakter** (cukup 3-5 paragraf)
- ✅ Tanggal → simpan **apa adanya** dari website
- ✅ URL → selalu **full URL** (`https://...`)
- ✅ Semua value bertipe **STRING**
- ✅ Error di field BONUS → `"-"`, selalu try-except

### Validasi Data — is_artikel_valid():

```python
def is_artikel_valid(artikel: dict) -> bool:
    return (
        artikel["judul"] not in (config.FIELD_KOSONG, "") and
        len(artikel["judul"]) >= config.MIN_JUDUL_CHARS and    # 15
        artikel["isi"] not in (config.FIELD_KOSONG, "") and
        len(artikel["isi"]) >= config.MIN_ISI_CHARS             # 100
    )
```

### Header CSV/Excel:
```
No, Judul, Tanggal, Penulis, Kategori, Isi, URL, Gambar_URL
```

---

## 📋 Pembagian Tugas Detail

### 🔴 Darva — scraper.py, worker.py, filter.py, main.py

**scraper.py — 3-Layer Extraction Strategy:**
```python
setup_driver()              # Chrome headless + eager + anti-bot + Linux flags
get_all_links(url, limit)   # same-domain filter, path_depth≥3, 20+ NON_ARTIKEL keywords
handle_pagination()         # 4 strategi: rel=next → teks tombol → URL pattern → berhenti
scrape_article(url)         # 3-layer extraction per field
is_artikel_valid(artikel)   # threshold dari config (MIN_JUDUL=15, MIN_ISI=100)
_extract_text(selectors)    # helper: coba CSS/XPath satu per satu
_extract_meta(names)        # helper: OpenGraph + Schema.org + itemprop
```

**worker.py — ScraperWorker(QThread):**
```python
sinyal_progress = pyqtSignal(int)
sinyal_hasil    = pyqtSignal(dict)
sinyal_selesai  = pyqtSignal(int)
sinyal_error    = pyqtSignal(str)
sinyal_status   = pyqtSignal(str)

__init__(url, limit, filter_aktif, start_date, end_date)
run()   # setup_driver → get_all_links → loop scrape_article → filter → emit
stop()  # self._running = False (graceful stop)
```

**filter.py — Multi-format Date Parsing:**
```python
parse_tanggal(tanggal_str)
  # Support: ISO "2025-03-04", DD/MM/YYYY, "04 Mar 2025", "4 Maret 2025"
  # + BULAN_INDONESIA mapping (Januari–Desember + singkatan)

filter_by_date(articles, start_date, end_date)
  # Dalam range → masuk | Luar range → buang
  # Tanggal tidak dikenali → ikuti FILTER_INCLUDE_UNKNOWN_DATE
```

**main.py:**
```python
buat_folder_wajib()   # OUTPUT_DIR + LOG_FILE.parent mkdir
main()                # QApplication → apply_style → MainWindow → app.exec_()
```

---

### 🟠 Kemal — config.py, exporter.py, logger.py

**config.py — Pengaturan Global:**
```python
# Selenium
HEADLESS=True, USER_AGENT, PAGE_LOAD_WAIT=10

# Scraping
DEFAULT_DELAY=1.5, DEFAULT_LIMIT=20, MAX_ISI_CHARS=2000, FIELD_KOSONG="-"
MIN_JUDUL_CHARS=15, MIN_ISI_CHARS=100

# Filter
FILTER_INCLUDE_UNKNOWN_DATE=True

# Path (pathlib)
OUTPUT_DIR=Path("output"), LOG_FILE=Path("logs")/"scraper.log"

# GUI
APP_TITLE, WINDOW_W=1200, WINDOW_H=700

# Format
CSV_ENCODING="utf-8-sig", EXCEL_ENGINE="openpyxl"
LOG_FORMAT="%(asctime)s - %(levelname)s - %(message)s", LOG_LEVEL="DEBUG"
CSV_HEADERS=[...]
```

**exporter.py:**
```python
export_csv(data, filename)    # pandas → CSV, encoding utf-8-sig, rename kolom
export_excel(data, filename)  # pandas + openpyxl → .xlsx, auto-width kolom
```

**logger.py:**
```python
setup_logger()     # FileHandler + StreamHandler, format dari config
log_info(message)
log_error(message)
log_warning(message)
```

---

### 🔵 Richard — gui.py (MainWindow)

```python
class MainWindow(QMainWindow):
    KOLOM_TABEL = ["#", "Judul", "Tanggal", "Penulis", "Kategori", "Isi (preview)", "URL"]

    # Widget utama:
    self.input_panel     # InputPanel
    self.tabel           # QTableWidget 7 kolom, alternating rows
    self.progress_bar    # QProgressBar (gradient biru→teal)
    self.btn_scrape      # "▶  Mulai Scraping"
    self.btn_stop        # "■  Stop" (objectName: btn_stop)
    self.btn_export_csv  # "↓  Export CSV" (objectName: btn_export_csv)
    self.btn_export_xl   # "↓  Export Excel" (objectName: btn_export_xl)
    self.label_status    # Teks status real-time
    self.label_jumlah    # Counter artikel

    # Bottom status bar:
    self.label_dot       # "●" — idle (#6B7699) / aktif (#00D4AA)
    self.label_state     # "SIAP" / "SCRAPING AKTIF"
    self.label_delay     # "DELAY: 1.5s"
    self.label_headless  # "HEADLESS: ON"
    self.label_logfile   # "logs/scraper.log"

    # Methods:
    _setup_ui()          # susun layout lengkap
    _connect_signals()   # btn → slot + cellDoubleClicked → _lihat_detail
    _set_state_idle()    # enable/disable tombol
    _set_state_scraping()
    mulai_scraping()     # validate → reset → buat worker → start
    stop_scraping()      # worker.stop()
    tambah_baris(artikel)# tambah baris, isi preview 150ch
    update_progress(int)
    scraping_selesai(int)
    tampilkan_error(str)
    _lihat_detail(row,col)  # QDialog: gambar (QPixmap/urllib) + isi 2000ch + meta
    export_csv()
    export_excel()
```

---

### 🟣 Kyla — gui.py (InputPanel)

```python
class InputPanel(QWidget):
    self.input_url       # QLineEdit — placeholder, clearButtonEnabled, minH 32
    self.input_limit     # QSpinBox — range 1-500, default 20, suffix " artikel"
    self.checkbox_filter # QCheckBox "Filter Tanggal"
    self.date_start      # QDateEdit — calendarPopup, format dd/MM/yyyy
    self.date_end        # QDateEdit — calendarPopup, format dd/MM/yyyy

    # Methods:
    _setup_ui()           # layout: URL row, limit row, checkbox, date range row
    get_inputs()          # → dict {url, limit, filter_aktif, start_date(QDate|None), end_date}
    validate()            # → bool + QMessageBox jika error
    _toggle_date_filter() # enable/disable date picker
```

---

### 🟢 Aulia — style.py, docs, README

**style.py — Dark Theme QSS:**
```python
MAIN_STYLESHEET = """..."""
# Palette: bg #0F1117, surface #181C27, surface2 #1E2333
#          border #2A3147, accent #4F8EF7, teal #00D4AA
#          danger #F75A5A, text #E8EAF0, muted #6B7699
# Komponen: QMainWindow, QLabel, InputPanel, QLineEdit, QSpinBox, QDateEdit,
#           QCheckBox, QPushButton (4 varian), QTableWidget, QProgressBar,
#           bottom_bar, QMessageBox, QDialog, QTextBrowser

apply_style(app)  # dipanggil di main.py sebelum MainWindow
```

---

## 💻 Kolaborasi Beda OS

### Perbedaan perintah:
| Aksi | Windows | Mac / Linux |
|------|---------|-------------|
| Jalankan Python | `python main.py` | `python3 main.py` |
| Install library | `pip install` | `pip3 install` |
| Path separator | `\` | `/` |

### Kode kompatibel semua OS:
```python
from pathlib import Path      # WAJIB
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"
```

### Selenium Linux flags:
```python
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```

---

## ⚙️ Ketentuan Teknis

| Ketentuan | Detail |
|-----------|--------|
| **Python versi** | 3.12 (system) |
| **PyQt versi** | PyQt5 ≥ 5.15 — **BUKAN PyQt6!** |
| **Browser** | Google Chrome 145 (headless) |
| **Threading** | `QThread`, BUKAN `threading.Thread` |
| **Delay** | 1.5 detik dari `config.DEFAULT_DELAY` |
| **Headless** | `page_load_strategy = "eager"` |
| **Extraction** | 3-layer: OG/Schema → wildcard → site-specific |
| **Validasi** | MIN_JUDUL=15, MIN_ISI=100 dari config |
| **Fallback** | `"-"`, JANGAN `None` atau crash |
| **Path** | `pathlib.Path` wajib |
| **Worker** | `self.worker`, bukan variabel lokal |

---

## 📦 Requirements

```
# requirements.txt — runtime
selenium
PyQt5>=5.15.0
pandas
openpyxl
webdriver-manager
```

```
# requirements-dev.txt — dev tools
pyqt5-tools
```

---

## ✅ Status Fitur (Semua SELESAI)

### Wajib:
- ✅ Python + PyQt GUI
- ✅ 1 URL input + validasi
- ✅ Ambil link + pagination
- ✅ Scrape tiap artikel
- ✅ Tampilkan di tabel (Judul + Tanggal + Isi)

### Opsional:
- ✅ Export CSV & Excel
- ✅ Progress bar
- ✅ Limit artikel
- ✅ Logging
- ✅ Filter tanggal

### Bonus:
- ✅ 3-layer extraction strategy
- ✅ Dialog detail double-click (gambar + isi 2000ch)
- ✅ Bottom status bar
- ✅ Dark theme sesuai gui-mockup.html
- ✅ Test CLI — lulus 3 website: CNN, Detik, Kompas
- ✅ get_all_links: same-domain, path_depth≥3, 20+ NON_ARTIKEL keywords

---

## 🔗 Diagram Ketergantungan Tugas

```
config.py (Kemal) ← HARUS SELESAI DULUAN (pakai pathlib!)
    │
    ├──► scraper.py (Darva) — MIN_JUDUL, MIN_ISI, FIELD_KOSONG, MAX_ISI_CHARS
    │    └──► worker.py (Darva) ──► filter.py → Integrasi GUI
    │
    ├──► logger.py → exporter.py (Kemal) — LOG_FORMAT, CSV_ENCODING, CSV_HEADERS
    │
    ├──► gui.py Richard (MainWindow) — APP_TITLE, WINDOW_W/H, DEFAULT_DELAY, HEADLESS
    └──► gui.py Kyla (InputPanel) — DEFAULT_LIMIT
```

---

*Update jika ada perubahan kesepakatan → update juga AI_CONTEXT.md → kabari semua anggota.*
