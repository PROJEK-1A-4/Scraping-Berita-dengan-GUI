# 💬 PROMPT_GUIDE.md — Template Prompt AI per Anggota
> Salin template sesuai namamu → paste ke AI → tulis pertanyaanmu di bawahnya
> Selalu sertakan kode yang sudah ada agar AI tidak jawab asal!

---

## 🔴 DARVA — scraper.py · worker.py · filter.py · main.py

### Template Dasar
```
Saya Darva, Lead Developer proyek News Scraper App.

KONTEKS PROYEK:
- Stack: Python 3.12, Selenium, PyQt5>=5.15, Chrome 145 headless
- Saya mengerjakan: [scraper.py / worker.py / filter.py / main.py]
- Status: semua fitur SELESAI

FORMAT DATA ARTIKEL (kesepakatan tim):
artikel = {
    "judul": str, "tanggal": str, "isi": str (maks 2000 char),
    "url": str, "penulis": str, "kategori": str, "gambar_url": str
}
Field tidak ada → "-"  |  BUKAN None atau ""

FUNGSI di scraper.py:
- setup_driver()              → Chrome headless + eager + anti-bot
- get_all_links(driver, url, limit)  → same-domain, path_depth≥3, NON_ARTIKEL filter
- scrape_article(driver, url) → 3-layer extraction: OG/Schema → wildcard → site-specific
- handle_pagination(driver)   → 4 strategi (rel=next, teks, URL, berhenti)
- is_artikel_valid(artikel)   → threshold dari config (MIN_JUDUL=15, MIN_ISI=100)
- _extract_text(driver, selectors)  → helper CSS/XPath
- _extract_meta(driver, names)      → helper OpenGraph/Schema.org/itemprop

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

---

## 🟠 KEMAL — config.py · logger.py · exporter.py

### Template Dasar
```
Saya Kemal, Data & Reliability Developer proyek News Scraper App.

KONTEKS PROYEK:
- Stack: Python 3.12, PyQt5, pandas, openpyxl
- Saya mengerjakan: [config.py / logger.py / exporter.py]

CONFIG (config.py) — nilai aktual:
DEFAULT_DELAY=1.5, DEFAULT_LIMIT=20, MAX_ISI_CHARS=2000
MIN_JUDUL_CHARS=15, MIN_ISI_CHARS=100
FIELD_KOSONG="-", FILTER_INCLUDE_UNKNOWN_DATE=True
CSV_ENCODING="utf-8-sig", EXCEL_ENGINE="openpyxl"
LOG_FORMAT="%(asctime)s - %(levelname)s - %(message)s", LOG_LEVEL="DEBUG"
OUTPUT_DIR=Path("output"), LOG_FILE=Path("logs")/"scraper.log"
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

---

## 🔵 RICHARD — gui.py (MainWindow)

### Template Dasar
```
Saya Richard, GUI Developer proyek News Scraper App.
Saya mengerjakan bagian fungsional gui.py (MainWindow).

KONTEKS PROYEK:
- Framework: PyQt5>=5.15 (BUKAN PyQt6!)
- File ini: gui.py — class MainWindow

KOMPONEN:
- QMainWindow (dark theme #0F1117)
- QTableWidget (7 kolom: #, Judul, Tanggal, Penulis, Kategori, Isi preview, URL)
- QProgressBar (gradient biru→teal)
- QPushButton: "▶ Mulai Scraping", "■ Stop", "↓ Export CSV", "↓ Export Excel"
- Bottom bar: dot indicator + state + delay + headless + logfile
- Dialog detail: double-click → QDialog (gambar QPixmap/urllib + isi 2000ch + meta)
- self.worker = ScraperWorker(**inputs) — disimpan di self!
- self.data_hasil = [] — list of dict

SINYAL DARI WORKER:
sinyal_progress(int) → update_progress()
sinyal_hasil(dict)   → tambah_baris()   (isi preview 150ch)
sinyal_selesai(int)  → scraping_selesai()
sinyal_error(str)    → tampilkan_error()
sinyal_status(str)   → label_status.setText()

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

---

## 🟣 KYLA — gui.py (InputPanel)

### Template Dasar
```
Saya Kyla, GUI Developer proyek News Scraper App.
Saya mengerjakan bagian input di gui.py — class InputPanel.

KONTEKS PROYEK:
- Framework: PyQt5>=5.15 (BUKAN PyQt6!)
- File ini: gui.py — class InputPanel

KOMPONEN:
- QLineEdit input_url      → placeholder, clearButtonEnabled, minH 32
- QSpinBox input_limit     → range 1-500, default 20, suffix " artikel"
- QCheckBox checkbox_filter → toggle filter tanggal
- QDateEdit date_start     → calendarPopup, dd/MM/yyyy, disabled jika off
- QDateEdit date_end       → calendarPopup, dd/MM/yyyy, disabled jika off

METHODS:
- get_inputs() → dict {url, limit, filter_aktif, start_date(QDate|None), end_date}
- validate() → bool + QMessageBox jika error
- _toggle_date_filter(state) → enable/disable date picker

ATURAN VALIDASI:
- URL tidak boleh kosong
- URL harus dimulai dengan http:// atau https://
- Kalau filter aktif: date_end tidak boleh sebelum date_start

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

---

## 🟢 AULIA — style.py · README.md · laporan

### Template Dasar
```
Saya Aulia, UI Polish & Dokumentasi proyek News Scraper App.
Saya mengerjakan style.py dan dokumentasi.

KONTEKS PROYEK:
- Framework: PyQt5>=5.15
- File ini: [style.py / README.md / requirements.txt]

DARK THEME PALETTE:
bg: #0F1117, surface: #181C27, surface2: #1E2333
border: #2A3147, accent: #4F8EF7, teal: #00D4AA
danger: #F75A5A, text: #E8EAF0, muted: #6B7699

KOMPONEN GUI (sudah ada):
- QMainWindow, QWidget, InputPanel (custom bg)
- QLineEdit, QSpinBox, QDateEdit, QCheckBox
- QPushButton (4 varian via objectName: default/biru, btn_stop/merah, btn_export_csv&xl/teal, disabled)
- QProgressBar (gradient chunk biru→teal)
- QTableWidget (alternating rows, custom header, scrollbar)
- QWidget#bottom_bar (monospace labels)
- QMessageBox, QDialog, QTextBrowser

INI KODE SAYA SEKARANG:
[paste kode di sini]

TOLONG BANTU:
[pertanyaan spesifik di sini]
```

---

## 💡 Tips Universal

### Kalau AI jawab tidak sesuai:
```
"Jawaban kamu tidak sesuai proyek kami:
 - Field artikel: judul, tanggal, isi, url, penulis, kategori, gambar_url
 - Field kosong = '-' (bukan None)
 - PyQt5 bukan PyQt6, MAX_ISI_CHARS=2000, MIN_JUDUL=15, MIN_ISI=100
 Tolong revisi."
```

### Kalau ada error:
```
"Error:
[paste error LENGKAP]

Kode:
[paste kode]

OS: Linux, Python 3.12, Chrome 145
Tolong debug."
```
