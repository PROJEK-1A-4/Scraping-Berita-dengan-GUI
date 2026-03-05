# 🤖 AI_CONTEXT.md — Konteks Proyek untuk AI Assistant

---

## 📌 Info Proyek

| | |
|---|---|
| **Nama** | News Scraper App |
| **Deskripsi** | Aplikasi desktop Python untuk scraping berita otomatis dari website berita Indonesia |
| **Stack** | Python 3.12, Selenium, **PyQt5 ≥ 5.15** (bukan PyQt6!), pandas, openpyxl, webdriver-manager |
| **Browser** | Google Chrome 145 (headless) |
| **Status** | ✅ Semua fitur wajib & opsional SELESAI |

---

## 👥 Pembagian Tugas Tim

| Nama | File yang Dikerjakan | Keterangan |
|------|---------------------|------------|
| **Darva** | `scraper.py`, `worker.py`, `filter.py`, `main.py` | Lead dev, reviewer semua PR |
| **Kemal** | `exporter.py`, `logger.py`, `config.py` | Data & reliability |
| **Richard** | `gui.py` (main window, tabel, progress bar, tombol) | GUI fungsional |
| **Kyla** | `gui.py` (input URL, limit, date picker, validasi) | GUI input & filter |
| **Aulia** | `style.py`, `requirements.txt`, `README.md`, laporan | UI polish & dokumentasi |

---

## 📁 Struktur File Lengkap

```
news-scraper/
├── main.py                   ← entry point, QApplication + apply_style + MainWindow
├── config.py                 ← konstanta global (MAX_ISI_CHARS=2000, DEFAULT_LIMIT=20, dll)
├── scraper.py                ← Selenium scraping: setup_driver, get_all_links, handle_pagination, scrape_article, is_artikel_valid
├── worker.py                 ← QThread ScraperWorker: 5 sinyal (progress, hasil, selesai, error, status)
├── filter.py                 ← parse_tanggal (multi-format ID/EN), filter_by_date
├── gui.py                    ← InputPanel (Kyla) + MainWindow (Richard): 7 kolom tabel, dialog detail double-click
├── style.py                  ← Dark theme QSS (#0F1117 bg, #4F8EF7 accent, #00D4AA teal)
├── exporter.py               ← export_csv(), export_excel()
├── logger.py                 ← setup_logger(), log_info/error/warning
├── requirements.txt          ← runtime (untuk submit)
├── requirements-dev.txt      ← dev tools: pyqt5-tools
├── test_scraper_cli.py       ← test scraper CLI tanpa GUI, output ringkasan per website
├── test_results.txt          ← hasil test terakhir
├── gui-mockup (1).html       ← mockup desain GUI (dark theme reference)
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

## 🗂️ Format Data Artikel — KESEPAKATAN TIM

```python
artikel = {
    # ── FIELD WAJIB (minimum spesifikasi dosen) ──────────────
    "judul"     : str,   # Judul artikel
    "tanggal"   : str,   # Apa adanya dari website, JANGAN diubah
    "isi"       : str,   # Maksimal 2000 karakter pertama

    # ── FIELD BONUS (nilai tambah) ────────────────────────────
    "url"       : str,   # Full URL artikel (https://...)
    "penulis"   : str,   # Nama penulis, atau "-" kalau tidak ada
    "kategori"  : str,   # Kategori berita, atau "-" kalau tidak ada
    "gambar_url": str,   # URL gambar utama, atau "-" kalau tidak ada
}
```

### Aturan wajib:
- ✅ Field tidak ditemukan → isi `"-"` (BUKAN `None`, BUKAN `""`)
- ✅ Isi artikel → potong di **2000 karakter** pertama (cukup untuk 3-5 paragraf)
- ✅ URL → selalu **full URL** dengan `https://`
- ✅ Semua value bertipe **string**
- ✅ Error di field BONUS → `"-"`, jangan crash program

### Header CSV/Excel (urutan wajib sama persis):
```python
["No", "Judul", "Tanggal", "Penulis", "Kategori", "Isi", "URL", "Gambar_URL"]
```

---

## ✅ Validasi Data — is_artikel_valid()

> Threshold **wajib diambil dari config.py** — jangan hardcode angkanya!

```python
from config import MIN_JUDUL_CHARS, MIN_ISI_CHARS  # 15, 100

def is_artikel_valid(artikel: dict) -> bool:
    return (
        artikel["judul"] not in (config.FIELD_KOSONG, "") and
        len(artikel["judul"]) >= config.MIN_JUDUL_CHARS and    # 15
        artikel["isi"] not in (config.FIELD_KOSONG, "") and
        len(artikel["isi"]) >= config.MIN_ISI_CHARS             # 100
    )
```

---

## ⚙️ Isi config.py (Pengaturan Global Aktual)

```python
from pathlib import Path

# Selenium
HEADLESS        = True
USER_AGENT      = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
PAGE_LOAD_WAIT  = 10

# Scraping
DEFAULT_DELAY   = 1.5
DEFAULT_LIMIT   = 20
MAX_ISI_CHARS   = 2000     # Cukup untuk 3-5 paragraf berita
FIELD_KOSONG    = "-"

# Validasi artikel
MIN_JUDUL_CHARS = 15       # judul minimal 15 karakter
MIN_ISI_CHARS   = 100      # isi minimal 100 karakter

# Filter tanggal
FILTER_INCLUDE_UNKNOWN_DATE = True

# Path output
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"

# GUI
APP_TITLE   = "News Scraper App"
WINDOW_W    = 1200
WINDOW_H    = 700

# Encoding dan format
CSV_ENCODING = "utf-8-sig"
EXCEL_ENGINE = "openpyxl"

# Logging
LOG_FORMAT   = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL    = "DEBUG"

# Header CSV/Excel (urutan WAJIB sama)
CSV_HEADERS = ["No", "Judul", "Tanggal", "Penulis", "Kategori", "Isi", "URL", "Gambar_URL"]
```

---

## 🔌 Cara Kerja QThread (Worker ↔ GUI)

```
GUI (MainWindow)    QThread/Worker          Scraper
     │                      │                         │
     │── worker.start() ───►│                         │
     │                      │── setup_driver() ──────►│
     │◄── sinyal_status ────│ "Mengumpulkan link..."  │
     │                      │── get_all_links() ─────►│
     │                      │── scrape_article() ────►│
     │                      │   is_artikel_valid()    │
     │                      │   filter_by_date()      │
     │◄── sinyal_hasil ─────│◄─ return artikel valid ─│
     │  tambah_baris()      │                         │
     │◄── sinyal_progress ──│                         │
     │  update_progress()   │                         │
     │◄── sinyal_selesai ───│                         │
     │  scraping_selesai()  │                         │
```

### Sinyal di worker.py:
```python
sinyal_progress = pyqtSignal(int)   # 0-100 → update progress bar
sinyal_hasil    = pyqtSignal(dict)  # 1 artikel valid → tambah baris tabel
sinyal_selesai  = pyqtSignal(int)   # total artikel → set state idle
sinyal_error    = pyqtSignal(str)   # pesan error → popup error
sinyal_status   = pyqtSignal(str)   # teks status → update label
```

---

## 🖥️ Komponen GUI (gui.py)

### Class InputPanel (Kyla):
```python
self.input_url       # QLineEdit — input URL, placeholder, clearButtonEnabled
self.input_limit     # QSpinBox  — range 1-500, default 20, suffix " artikel"
self.checkbox_filter # QCheckBox — aktifkan filter tanggal
self.date_start      # QDateEdit — tanggal mulai, calendarPopup, disabled jika checkbox off
self.date_end        # QDateEdit — tanggal selesai, calendarPopup, disabled jika checkbox off

# Methods:
get_inputs()       # → dict {url, limit, filter_aktif, start_date, end_date}
validate()         # → bool (True jika valid, False + QMessageBox jika error)
_toggle_date_filter(state)  # enable/disable date picker
```

### Class MainWindow (Richard):
```python
# Tabel 7 kolom: #, Judul, Tanggal, Penulis, Kategori, Isi (preview 150ch), URL
KOLOM_TABEL = ["#", "Judul", "Tanggal", "Penulis", "Kategori", "Isi (preview)", "URL"]

self.input_panel     # InputPanel (Kyla)
self.btn_scrape      # QPushButton "▶  Mulai Scraping"
self.btn_stop        # QPushButton "■  Stop"          (objectName: btn_stop)
self.btn_export_csv  # QPushButton "↓  Export CSV"    (objectName: btn_export_csv)
self.btn_export_xl   # QPushButton "↓  Export Excel"  (objectName: btn_export_xl)
self.progress_bar    # QProgressBar 0-100, gradient biru→teal
self.label_status    # QLabel — teks status real-time
self.label_jumlah    # QLabel — "Menampilkan X artikel"
self.tabel           # QTableWidget 7 kolom
self.worker          # ScraperWorker — SIMPAN DI self!
self.data_hasil      # list of dict

# Bottom status bar:
self.label_dot       # QLabel "●" — warna berubah: #6B7699 (idle) / #00D4AA (aktif)
self.label_state     # QLabel "SIAP" / "SCRAPING AKTIF"
self.label_delay     # QLabel "DELAY: 1.5s"
self.label_headless  # QLabel "HEADLESS: ON/OFF"
self.label_logfile   # QLabel path log file

# Double-click baris → dialog detail:
_lihat_detail()      # QDialog: gambar asli (QPixmap/urllib) + isi 2000ch + meta lengkap
```

---

## 🕷️ Fungsi Scraper (scraper.py) — Strategi 3 Lapisan

```python
setup_driver()                             # Chrome headless + eager + anti-bot
get_all_links(driver, url, limit)          # same-domain, path_depth≥3, 20+ NON_ARTIKEL keywords
scrape_article(driver, url)                # 3-layer extraction
handle_pagination(driver)                  # 4 strategi (rel=next, teks, URL pattern, berhenti)
is_artikel_valid(artikel)                  # threshold dari config
_extract_text(driver, selectors, default)  # helper: coba CSS/XPath satu per satu
_extract_meta(driver, names, default)      # helper: baca <meta> OpenGraph/Schema.org/itemprop
```

### Strategi Ekstraksi 3 Lapisan:
```
L1 (UNIVERSAL)    — OpenGraph + Schema.org meta tags
  → og:title, article:published_time, articleBody, og:image, dll.

L2 (SEMI-UMUM)    — wildcard [class*='...'] + semantic HTML5
  → [class*='article-body'], [class*='author'], <article>, <time>, <h1>

L3 (OPTIMASI)     — class spesifik Detik/Kompas/CNN
  → .detail__title, .read__title, .detail__body-text, dll.
```

---

## 📋 Ketentuan Teknis

| Ketentuan | Detail |
|-----------|--------|
| **Python versi** | 3.12 (system) |
| **PyQt versi** | PyQt5 ≥ 5.15 — **BUKAN PyQt6!** |
| **Browser** | Google Chrome 145 (headless) |
| **Threading** | `QThread`, BUKAN `threading.Thread` biasa |
| **Delay** | 1.5 detik antar request dari `config.DEFAULT_DELAY` |
| **Headless** | `page_load_strategy = "eager"` |
| **Extraction** | 3-layer: OpenGraph/Schema → wildcard → site-specific |
| **Validasi** | `is_artikel_valid()` — MIN_JUDUL=15, MIN_ISI=100 |
| **Fallback** | Field tidak ada → `"-"`, JANGAN `None` atau crash |
| **Path file** | Wajib `pathlib.Path` |
| **Worker** | Simpan di `self.worker`, bukan variabel lokal |

---

## ✅ Status Fitur (Semua SELESAI)

### Wajib:
- ✅ Python + PyQt GUI
- ✅ 1 URL input + validasi
- ✅ Ambil link + pagination (4 strategi)
- ✅ Scrape tiap artikel (3-layer extraction)
- ✅ Tampilkan di tabel 7 kolom (#, Judul, Tanggal, Penulis, Kategori, Isi preview, URL)

### Opsional:
- ✅ Export CSV & Excel (dengan Isi lengkap)
- ✅ Progress bar (gradient biru→teal + label status real-time)
- ✅ Limit artikel (1–500)
- ✅ Logging (file + console dengan timestamp)
- ✅ Filter tanggal (start–end date, parse multi-format Indonesia)

### Bonus:
- ✅ Dialog detail double-click (gambar asli QPixmap/urllib + isi 2000ch + meta)
- ✅ Bottom status bar (dot SIAP/AKTIF + delay + headless + logfile)
- ✅ Dark theme sesuai gui-mockup.html (#0F1117 bg, #4F8EF7 accent, #00D4AA teal)
- ✅ Scraper lulus test 3 website: CNN 5/5, Detik 4/5, Kompas 5/5
- ✅ Test CLI (`test_scraper_cli.py`)

---

*File ini adalah sumber kebenaran tunggal untuk proyek ini.*
