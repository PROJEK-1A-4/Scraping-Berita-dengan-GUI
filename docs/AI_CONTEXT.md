# 🤖 AI_CONTEXT.md — Konteks Proyek untuk AI Assistant
> Paste file ini di awal setiap sesi chat baru dengan AI (ChatGPT / Claude / Copilot / Cursor)
> Untuk sesi cepat sehari-hari, gunakan AI_CONTEXT_SHORT.md (versi ~40 baris)

---

## 📌 Info Proyek

| | |
|---|---|
| **Nama** | News Scraper App |
| **Deskripsi** | Aplikasi desktop Python untuk scraping berita otomatis dari website berita Indonesia |
| **Stack** | Python 3.8+, Selenium, **PyQt5 ≥ 5.15** (bukan PyQt6!), pandas, openpyxl, webdriver-manager |
| **Deadline** | Sabtu, 7 Maret 2025 pukul 23.59 |

---

## 👥 Pembagian Tugas Tim

| Nama | File yang Dikerjakan | Keterangan |
|------|---------------------|------------|
| **Darva** | `scraper.py`, `worker.py`, `filter.py`, `main.py` | Lead dev, reviewer semua PR |
| **Kemal** | `exporter.py`, `logger.py`, `config.py` | Data & reliability |
| **Richard** | `gui.py` (main window, tabel, progress bar, tombol) | GUI fungsional |
| **Kyla** | `gui.py` (input URL, limit, date picker, validasi) | GUI input & filter |
| **Aulia** | `style.py`, `requirements.txt`, `README.md`, PDF laporan | UI polish & dokumentasi |

---

## 📁 Struktur File Lengkap

```
news-scraper/
├── main.py
├── scraper.py
├── worker.py
├── filter.py
├── gui.py
├── style.py
├── exporter.py
├── logger.py
├── config.py
├── requirements.txt          ← runtime saja (untuk submit)
├── requirements-dev.txt      ← dev tools: pyqt5-tools
├── README.md
├── .gitignore
├── output/
├── logs/
└── docs/
    ├── laporan.pdf
    ├── AI_CONTEXT.md
    ├── AI_CONTEXT_SHORT.md
    └── screenshots/
```

---

## 🌿 Struktur Branch GitHub

> ⚠️ Format **SERAGAM: `dev/nama`** — JANGAN pakai format lain!

```
main              ← hanya Darva yang merge (via Pull Request)
├── dev/darva
├── dev/richard
├── dev/kemal
├── dev/kyla
└── dev/aulia
```

---

## 🗂️ Format Data Artikel — KESEPAKATAN TIM (WAJIB DIPATUHI)

```python
artikel = {
    # ── FIELD WAJIB (minimum spesifikasi dosen) ──────────────
    "judul"     : str,   # Judul artikel
    "tanggal"   : str,   # Apa adanya dari website, JANGAN diubah
    "isi"       : str,   # Maksimal 500 karakter pertama

    # ── FIELD BONUS (nilai tambah) ────────────────────────────
    "url"       : str,   # Full URL artikel (https://...)
    "penulis"   : str,   # Nama penulis, atau "-" kalau tidak ada
    "kategori"  : str,   # Kategori berita, atau "-" kalau tidak ada
    "gambar_url": str,   # URL gambar utama, atau "-" kalau tidak ada
}
```

### Aturan wajib:
- ✅ Field tidak ditemukan → isi `"-"` (BUKAN `None`, BUKAN `""`)
- ✅ Isi artikel → potong di **500 karakter** pertama
- ✅ URL → selalu **full URL** dengan `https://`
- ✅ Semua value bertipe **string**
- ✅ Error di field BONUS → `"-"`, jangan crash program

### Header CSV/Excel (urutan wajib sama persis):
```python
["No", "Judul", "Tanggal", "Penulis", "Kategori", "Isi", "URL", "Gambar_URL"]
```

---

## ✅ Validasi Data — is_artikel_valid()

> Spesifikasi dosen: *"Data yang diambil harus valid dan tidak kosong"*
> Threshold **wajib diambil dari config.py** — jangan hardcode angkanya!

```python
# Di scraper.py — import dari config, JANGAN tulis angka langsung
from config import MIN_JUDUL_CHARS, MIN_ISI_CHARS

def is_artikel_valid(artikel: dict) -> bool:
    """
    Cek field WAJIB saja (judul & isi).
    Tanggal boleh "-" karena spesifikasi bilang "jika tersedia".
    Field bonus tidak dicek — boleh "-".
    """
    return (
        artikel["judul"] not in ("-", "") and
        len(artikel["judul"]) >= MIN_JUDUL_CHARS and
        artikel["isi"] not in ("-", "") and
        len(artikel["isi"]) >= MIN_ISI_CHARS
    )

# Di worker.py — skip artikel tidak valid:
artikel = scrape_article(driver, link)
if not is_artikel_valid(artikel):
    log_warning(f"Artikel dilewati (tidak valid): {link}")
    continue
self.sinyal_hasil.emit(artikel)
```

---

## ⚙️ Isi config.py (Pengaturan Global)

> ⚠️ Wajib pakai `pathlib.Path` untuk path file — kompatibel Windows/Mac/Linux!

```python
from pathlib import Path   # ← WAJIB! String path bisa error di OS lain

# Selenium
HEADLESS        = True
USER_AGENT      = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
PAGE_LOAD_WAIT  = 10

# Scraping
DEFAULT_DELAY   = 1.5
DEFAULT_LIMIT   = 20
MAX_ISI_CHARS   = 500
FIELD_KOSONG    = "-"

# Validasi artikel — dipakai is_artikel_valid() di scraper.py
MIN_JUDUL_CHARS = 5      # judul minimal N karakter
MIN_ISI_CHARS   = 20     # isi minimal N karakter

# Filter tanggal
FILTER_INCLUDE_UNKNOWN_DATE = True
# True  = artikel tanggal tidak dikenal TETAP tampil saat filter aktif
# False = artikel tanggal tidak dikenal DIBUANG saat filter aktif

# Path output — pathlib otomatis handle \ vs / antar OS
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"

# GUI
APP_TITLE   = "News Scraper App"
WINDOW_W    = 1200
WINDOW_H    = 700
CSV_HEADERS = ["No","Judul","Tanggal","Penulis","Kategori","Isi","URL","Gambar_URL"]
```

---

## 🔌 Cara Kerja QThread (PENTING untuk Richard & Darva)

```
GUI (Kasir)        QThread/Worker (Koki)          Scraper
     │                      │                         │
     │── worker.start() ───►│                         │
     │                      │── scrape_article() ────►│
     │                      │   is_artikel_valid()    │
     │                      │   (skip jika tidak valid)│
     │◄── sinyal_hasil ─────│◄─ return artikel valid ─│
     │  tambah_baris()      │                         │
     │◄── sinyal_progress ──│                         │
     │  update_progress()   │                         │
     │◄── sinyal_selesai ───│                         │
     │  popup selesai       │                         │
```

### Sinyal di worker.py:
```python
sinyal_progress = pyqtSignal(int)   # 0-100 → update progress bar
sinyal_hasil    = pyqtSignal(dict)  # 1 artikel valid → tambah baris tabel
sinyal_selesai  = pyqtSignal(int)   # total artikel → popup selesai
sinyal_error    = pyqtSignal(str)   # pesan error → popup error
sinyal_status   = pyqtSignal(str)   # teks status → update label
```

### Cara sambungkan di gui.py:
```python
self.worker = ScraperWorker(url, limit, start_date, end_date)
self.worker.sinyal_progress.connect(self.update_progress)
self.worker.sinyal_hasil.connect(self.tambah_baris)
self.worker.sinyal_selesai.connect(self.scraping_selesai)
self.worker.sinyal_error.connect(self.tampilkan_error)
self.worker.sinyal_status.connect(self.label_status.setText)  # ← jangan lupa ini!
self.worker.start()
```

---

## 🖥️ Komponen GUI (gui.py)

### Class InputPanel (Kyla):
```python
self.input_url       # QLineEdit — input URL
self.input_limit     # QSpinBox  — limit 1-500, default 20
self.checkbox_filter # QCheckBox — aktifkan filter tanggal
self.date_start      # QDateEdit — tanggal mulai (disabled jika checkbox off)
self.date_end        # QDateEdit — tanggal selesai (disabled jika checkbox off)

# Methods:
get_url()          # → str
get_limit()        # → int
get_start_date()   # → datetime.date atau None
get_end_date()     # → datetime.date atau None
validasi()         # → str (pesan error) atau "" (valid)
```

### Class MainWindow (Richard):
```python
self.input_panel   # InputPanel (Kyla)
self.btn_scrape    # QPushButton — enabled saat idle
self.btn_stop      # QPushButton — enabled HANYA saat scraping
self.btn_csv       # QPushButton — enabled HANYA setelah ada data
self.btn_excel     # QPushButton — enabled HANYA setelah ada data
self.progress_bar  # QProgressBar 0-100
self.label_status  # QLabel — teks status real-time
self.label_jumlah  # QLabel — "Menampilkan X artikel"
self.tabel         # QTableWidget 7 kolom
self.worker        # ScraperWorker — SIMPAN DI self, bukan variabel lokal!
self.data_hasil    # list of dict — semua artikel hasil scraping
```

---

## 🕷️ Fungsi Scraper (scraper.py)

```python
setup_driver()                          # → webdriver.Chrome headless
get_all_links(driver, url, limit)       # → list[str] URL artikel
scrape_article(driver, url)             # → dict artikel (format kesepakatan)
handle_pagination(driver, base_url)     # → list[str] link halaman 2,3,dst
is_artikel_valid(artikel)               # → bool
```

---

## 💻 Kolaborasi Beda OS dalam Tim

> Penting untuk diketahui AI saat membantu: tim mungkin pakai OS berbeda!

### Perbedaan perintah antar OS:
| Aksi | Windows | Mac / Linux |
|------|---------|-------------|
| Jalankan Python | `python main.py` | `python3 main.py` |
| Install library | `pip install` | `pip3 install` |
| Path separator | `\` (backslash) | `/` (forward slash) |

### Aturan kode wajib supaya kompatibel semua OS:
```python
# ❌ JANGAN — bisa error di OS lain
OUTPUT_DIR = "output/"
LOG_FILE   = "logs\\scraper.log"

# ✅ WAJIB di config.py
from pathlib import Path
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"
```

### Selenium di Linux — wajib tambah flag ini:
```python
# Di setup_driver() scraper.py:
options.add_argument("--no-sandbox")            # WAJIB di Linux
options.add_argument("--disable-dev-shm-usage") # Cegah crash
```

### pyqt5-tools (Qt Designer):
| OS | Status |
|----|--------|
| Windows | ✅ Jalan normal |
| Mac | ❌ Sering gagal — skip, desain GUI di kode saja |
| Linux | ❌ Pakai `sudo apt install qttools5-dev-tools` |

### Requirements yang benar:
```
# requirements.txt (runtime — dikumpulkan ke dosen)
selenium
PyQt5>=5.15.0
pandas
openpyxl
webdriver-manager

# requirements-dev.txt (dev tools — JANGAN ikut dikumpulkan)
pyqt5-tools
```

---

## 📋 Ketentuan Teknis Wajib

| Ketentuan | Detail |
|-----------|--------|
| **PyQt versi** | PyQt5 ≥ 5.15 — **BUKAN PyQt6!** |
| **Threading** | `QThread`, BUKAN `threading.Thread` biasa |
| **Delay** | 1.5 detik antar request dari `config.DEFAULT_DELAY` |
| **Headless** | Chrome tanpa tampilan jendela |
| **General** | Selector umum (`h1`, `article`, `time`) — jangan hardcode nama website |
| **Validasi** | `is_artikel_valid()` wajib, threshold dari `config.py` |
| **Fallback** | Field tidak ada → `"-"`, JANGAN `None` atau crash |
| **Path file** | Wajib `pathlib.Path` — kompatibel Windows/Mac/Linux |
| **Worker** | Simpan di `self.worker`, bukan variabel lokal (anti garbage collect) |

---

## 💬 Template Prompt Efektif untuk AI

```
[Paste AI_CONTEXT_SHORT.md untuk sesi cepat]
[Paste file ini untuk pertanyaan kompleks / integrasi antar modul]

---
Saya: [NAMA]
OS saya: [Windows / Mac / Linux]
Saya mengerjakan: [nama file]
Ini kode saya sekarang: [paste kode]
Tolong bantu: [pertanyaan spesifik]
```

> Tambahkan **OS kamu** di template prompt supaya AI bisa langsung kasih solusi yang sesuai!

---

## ⚠️ Aturan Penting Saat Pakai AI

```
✅ AI_CONTEXT_SHORT.md → pertanyaan sehari-hari (hemat context window)
✅ File ini → pertanyaan kompleks / integrasi antar modul
✅ Selalu paste kode yang sudah ada sebelum minta tambahan
✅ Sebutkan OS kamu (Windows/Mac/Linux) di setiap prompt
✅ Minta AI jelaskan kode yang dihasilkan — biar kamu paham
✅ Baca & pahami dulu sebelum commit

❌ Jangan tanya tanpa konteks
❌ Jangan commit kode yang tidak kamu mengerti
❌ Jangan pakai nama file/variabel berbeda dari kesepakatan
❌ Jangan hardcode nama website di scraper.py
❌ Jangan gunakan PyQt6 atau threading.Thread biasa
❌ Jangan gunakan string path manual — pakai pathlib
```

---

*File ini adalah sumber kebenaran tunggal untuk proyek ini.*
*Jika ada perubahan → update file ini + AI_CONTEXT_SHORT.md → kabari semua anggota.*
