# 📰 BLUEPRINT — News Scraper App
> Tugas Kelompok Web Scraping | Deadline: Sabtu, 7 Maret 2025 pukul 23.59

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

Aplikasi desktop berbasis Python yang dapat **mengambil data berita secara otomatis** dari sebuah website berita. User cukup memasukkan 1 URL, aplikasi akan mengambil semua artikel beserta isinya dan menampilkan hasilnya dalam tabel yang rapi.

---

## 🎬 Alur Aplikasi (User Flow)

```
STEP 1: User buka aplikasi
        → Muncul window dengan form input

STEP 2: User isi form
        → Masukkan URL homepage/kategori berita
        → (Opsional) Pilih rentang tanggal: start date – end date
        → (Opsional) Set limit jumlah berita, contoh: 50 artikel

STEP 3: User klik tombol "Mulai Scraping"
        → Validasi input dulu (URL kosong? format salah? tanggal valid?)
        → Progress bar mulai bergerak
        → GUI tetap responsif, tidak freeze

STEP 4: Di balik layar — Selenium bekerja
        4a. Buka URL yang diinput user
            → Scan halaman, kumpulkan semua link artikel
            → Kalau ada tombol "Next / Halaman 2" → ikuti juga (pagination)
        4b. Buka satu per satu link artikel
            → Ambil field WAJIB: Judul, Tanggal, Isi
            → Ambil field BONUS: Penulis, Kategori, URL, Gambar (nilai tambah)
            → Cek is_artikel_valid() → skip kalau judul/isi kosong
            → Tunggu sebentar (delay) sebelum buka artikel berikutnya
        4c. Filter data (kalau user set tanggal)
            → Buang artikel di luar rentang tanggal
            → Artikel tanggal tidak dikenali → ikuti config.FILTER_INCLUDE_UNKNOWN_DATE

STEP 5: Hasil muncul di tabel GUI
        → 7 Kolom: No | Judul | Tanggal | Penulis | Kategori | URL | Gambar
        → Progress bar penuh = selesai ✅
        → Hanya artikel VALID yang ditampilkan

STEP 6: User klik "Export"
        → Pilih format: CSV atau Excel (.xlsx)
        → File tersimpan di komputer user
```

---

## 🏗️ Arsitektur Aplikasi

```
main.py
  │
  ├── config.py          ← pengaturan global (Kemal)
  │
  ├── gui.py             ← tampilan aplikasi
  │     ├── [Richard]    Main window, tabel, progress bar, tombol
  │     └── [Kyla]       Input URL, limit, date picker, validasi
  │
  ├── style.py           ← stylesheet visual (Aulia)
  │
  ├── worker.py          ← QThread: jembatan GUI ↔ scraper (Darva)
  │
  ├── scraper.py         ← otak scraping (Darva)
  │     ├── Selenium setup (headless)
  │     ├── get_all_links(url)      → kumpulkan semua link artikel
  │     ├── handle_pagination()     → ikuti halaman berikutnya
  │     ├── scrape_article(url)     → ekstrak data 1 artikel
  │     └── is_artikel_valid()      → cek data tidak kosong ✅
  │
  ├── filter.py          ← filter artikel by tanggal (Darva)
  │
  ├── exporter.py        ← export CSV & Excel (Kemal)
  │
  └── logger.py          ← logging & error handling (Kemal)
```

---

## 📁 Struktur Folder Project

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
├── requirements.txt          ← runtime saja (untuk submit ke dosen)
├── requirements-dev.txt      ← dev tools: pyqt5-tools (JANGAN ikut submit)
├── README.md
├── .gitignore
├── output/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
└── docs/
    ├── laporan.pdf
    ├── AI_CONTEXT.md
    ├── AI_CONTEXT_SHORT.md
    └── screenshots/
```

---

## 🗂️ Struktur Data Artikel (KESEPAKATAN TIM)

> ⚠️ **WAJIB DIPATUHI SEMUA ANGGOTA — jangan ubah nama field atau tipe data!**

```python
artikel = {
    # ── FIELD WAJIB (minimum spesifikasi dosen) ──────────────
    "judul"     : str,   # Judul artikel
    "tanggal"   : str,   # Apa adanya dari website (JANGAN diubah formatnya)
    "isi"       : str,   # Maksimal 500 karakter pertama

    # ── FIELD BONUS (nilai tambah, boleh "-" kalau tidak ada) ─
    "url"       : str,   # Full URL artikel (https://...)
    "penulis"   : str,   # Nama penulis → "-" kalau tidak ada
    "kategori"  : str,   # Kategori berita → "-" kalau tidak ada
    "gambar_url": str,   # URL gambar utama → "-" kalau tidak ada
}
```

### Aturan Wajib:
- ✅ Field tidak ditemukan → isi `"-"` (BUKAN `None`, BUKAN `""`)
- ✅ Isi artikel → maksimal **500 karakter** pertama
- ✅ Tanggal → simpan **apa adanya** dari website
- ✅ URL → selalu **full URL** (`https://...`), bukan relative (`/berita/...`)
- ✅ Semua value bertipe **STRING**
- ✅ Error di field BONUS jangan crash — selalu try-except, fallback ke `"-"`

### Validasi Data — is_artikel_valid() (WAJIB):

> Threshold **wajib diambil dari config.py**, jangan hardcode angkanya langsung di sini!

```python
# Di scraper.py — import threshold dari config:
from config import MIN_JUDUL_CHARS, MIN_ISI_CHARS

def is_artikel_valid(artikel: dict) -> bool:
    """
    Spesifikasi dosen: "Data yang diambil harus valid dan tidak kosong"
    Hanya cek field WAJIB. Field bonus tidak dicek karena boleh "-".
    Threshold dikonfigurasi di config.py supaya mudah diubah tanpa edit kode.
    """
    return (
        artikel["judul"] not in ("-", "") and
        len(artikel["judul"]) >= MIN_JUDUL_CHARS and
        artikel["isi"] not in ("-", "") and
        len(artikel["isi"]) >= MIN_ISI_CHARS
    )
```

### Header CSV/Excel (urutan wajib sama):
```
No, Judul, Tanggal, Penulis, Kategori, Isi, URL, Gambar_URL
```

---

## 📋 Pembagian Tugas Detail

### 🔴 Darva — scraper.py, worker.py, filter.py, main.py

**scraper.py:**
```python
- setup_driver()              → Selenium headless + anti-bot headers
                                ⚠️ Linux: tambahkan --no-sandbox & --disable-dev-shm-usage
- get_all_links(url, limit)   → ambil semua link artikel dari halaman
- handle_pagination()         → deteksi & ikuti halaman berikutnya (lihat strategi bawah)
- scrape_article(url)         → ekstrak semua field dari 1 artikel
- is_artikel_valid(artikel)   → validasi field wajib, threshold dari config ✅
- _extract_text(driver, selectors, default="-")  → helper: coba selector satu per satu
```

**Strategi handle_pagination() — urutan prioritas:**
```python
# 1. Cari: <a rel="next"> atau <link rel="next">
# 2. Cari teks tombol: "Next", "Selanjutnya", "›", "»", "Berikutnya"
# 3. Cari pola URL: ?page=2, ?p=2, /page/2, /halaman/2
# 4. Tidak ketemu → berhenti (sudah halaman terakhir)
# JANGAN hardcode class/id spesifik per website!
```

**worker.py:**
```python
- class ScraperWorker(QThread)
- sinyal_progress = pyqtSignal(int)
- sinyal_hasil    = pyqtSignal(dict)
- sinyal_selesai  = pyqtSignal(int)
- sinyal_error    = pyqtSignal(str)
- sinyal_status   = pyqtSignal(str)
- def run(self) → scraping di background, skip jika not is_artikel_valid()
- ⚠️ Simpan worker di self.worker (BUKAN variabel lokal — bisa kena garbage collect!)
```

**[OPSIONAL — bonus nilai] Multi-threading di worker.py:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(scrape_article, driver, link): link
               for link in links}
    for i, future in enumerate(as_completed(futures)):
        artikel = future.result()
        if is_artikel_valid(artikel):
            self.sinyal_hasil.emit(artikel)
        self.sinyal_progress.emit(int((i + 1) / len(links) * 100))
# max_workers=3 supaya tidak membebani server
```

**filter.py:**
```python
- parse_tanggal(tanggal_str)
    → datetime.date jika berhasil, None jika format tidak dikenali
    → Support: "04 Mar 2025", "4 Maret 2025", "2025-03-04", "04/03/2025"

- filter_by_date(articles, start_date, end_date)
    → Artikel dalam range → masuk hasil
    → Artikel di luar range → dibuang
    → Artikel tanggal tidak dikenali → ikuti config.FILTER_INCLUDE_UNKNOWN_DATE
```

**main.py:**
```python
- Buat folder output/ dan logs/ otomatis (os.makedirs exist_ok=True)
- Inisialisasi QApplication → apply_style(app) → buka MainWindow
```

---

### 🟠 Kemal — config.py, exporter.py, logger.py

**config.py — HARUS SELESAI HARI 1, semua orang butuh ini!**

> ⚠️ Wajib pakai `pathlib.Path` untuk path file supaya kompatibel Windows/Mac/Linux!

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
# True  = artikel dengan tanggal tidak dikenal TETAP tampil saat filter aktif
# False = artikel dengan tanggal tidak dikenal DIBUANG saat filter aktif

# Path output — pathlib otomatis handle \ vs / antar OS
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"

# GUI
APP_TITLE   = "News Scraper App"
WINDOW_W    = 1200
WINDOW_H    = 700
CSV_HEADERS = ["No","Judul","Tanggal","Penulis","Kategori","Isi","URL","Gambar_URL"]
```

**exporter.py:**
```python
- export_csv(data, filename)    → simpan ke .csv (encoding utf-8-sig)
- export_excel(data, filename)  → simpan ke .xlsx (auto-width kolom)
```

**logger.py:**
```python
- setup_logger()       → logging ke file + terminal, dengan timestamp
- log_info(message)
- log_error(message)
- log_warning(message)
```

**requirements.txt** ← runtime, ini yang dikumpulkan ke dosen:
```
selenium
PyQt5>=5.15.0
pandas
openpyxl
webdriver-manager
```

**requirements-dev.txt** ← development tools, JANGAN ikut dikumpulkan:
```
pyqt5-tools
```

---

### 🔵 Richard — gui.py (bagian fungsional)

```python
- QMainWindow setup
- QTableWidget (7 kolom: No, Judul, Tanggal, Penulis, Kategori, URL, Gambar)
- QProgressBar (0-100%)
- QPushButton "Mulai Scraping"  → enabled saat idle
- QPushButton "Stop"            → enabled HANYA saat scraping
- QPushButton "Export CSV"      → enabled HANYA setelah ada data
- QPushButton "Export Excel"    → enabled HANYA setelah ada data
- label_status, label_jumlah
- self.worker = ScraperWorker(...)  ← SIMPAN DI self, BUKAN variabel lokal!
- self.data_hasil = []
```

---

### 🟣 Kyla — gui.py (bagian input & filter)

```python
- QLineEdit input_url       → input URL (placeholder: "https://...")
- QSpinBox input_limit      → limit 1-500, default 20
- QCheckBox checkbox_filter → toggle filter tanggal
- QDateEdit date_start      → disabled kalau checkbox off
- QDateEdit date_end        → disabled kalau checkbox off
- Validasi:
    → URL tidak boleh kosong
    → URL harus dimulai http:// atau https://
    → date_end tidak boleh sebelum date_start (kalau filter aktif)
```

---

### 🟢 Aulia — style.py, screenshot, PDF, requirements, README

**style.py:**
```python
- MAIN_STYLESHEET = "..."   → string QSS styling lengkap
- apply_style(app)          → dipanggil di main.py SEBELUM MainWindow dibuat
```

**Screenshot wajib (simpan di docs/screenshots/):**
```
SS 1 (WAJIB): Tampilan awal — window kosong sebelum scraping
SS 2 (WAJIB): Saat scraping berjalan — progress bar aktif, data masuk
SS 3 (WAJIB): Selesai — tabel penuh artikel
SS 4 (bonus): Hasil export terbuka di Excel
SS 5 (bonus): Filter tanggal aktif dengan hasil tersaring
```

**PDF laporan (maks 3 halaman):**
```
Hal 1: Info tim + deskripsi + daftar fitur
Hal 2: Arsitektur + diagram modul + pembagian tim
Hal 3: Alur scraping step-by-step + screenshot aplikasi
```

---

## 🌿 Struktur Branch GitHub

> ⚠️ Format branch **SERAGAM: `dev/nama`** — SEMUA ANGGOTA wajib pakai ini!
> Jangan pakai format lain (tanpa `dev/`, atau pakai nama lengkap, dsb).

```
main                 ← hanya Darva yang merge via Pull Request
├── dev/darva
├── dev/richard
├── dev/kemal
├── dev/kyla
└── dev/aulia
```

### Cara buat branch — Darva lakukan ini di hari pertama untuk semua anggota:
```bash
git checkout main
git checkout -b dev/darva   && git push origin dev/darva
git checkout -b dev/kemal   && git push origin dev/kemal
git checkout -b dev/richard && git push origin dev/richard
git checkout -b dev/kyla    && git push origin dev/kyla
git checkout -b dev/aulia   && git push origin dev/aulia
```

### Tiap anggota — alur kerja harian:
```bash
git checkout dev/namakamu        # pindah ke branch sendiri
git pull origin main             # sync sebelum mulai coding!
# ... coding ...
git add .
git commit -m "tipe(file): deskripsi singkat"
git push origin dev/namakamu
# → buat Pull Request ke main → assign ke Darva sebagai reviewer
```

### Target minimum commit:
| Nama | Target |
|------|--------|
| Darva | 10–12 |
| Kemal | 6–8 |
| Richard | 6–8 |
| Kyla | 5–6 |
| Aulia | 5–6 |

---

## 💻 Kolaborasi Beda OS dalam Tim

> Tim mungkin pakai OS yang berbeda. Ikuti aturan ini supaya kode tidak konflik!

### Perbedaan perintah antar OS:
| Aksi | Windows | Mac / Linux |
|------|---------|-------------|
| Jalankan Python | `python main.py` | `python3 main.py` |
| Install library | `pip install` | `pip3 install` |
| Cek versi | `python --version` | `python3 --version` |
| Path separator | `\` (backslash) | `/` (forward slash) |
| Terminal | Command Prompt / PowerShell | Terminal |

### Aturan kode supaya kompatibel semua OS:
```python
# ❌ JANGAN — backslash error di Mac/Linux, string "/" bisa beda antar OS
OUTPUT_DIR = "output/"
LOG_FILE   = "logs\\scraper.log"

# ✅ WAJIB — pathlib otomatis pakai separator yang benar di tiap OS
from pathlib import Path
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"
```

### Selenium di Linux — wajib tambahkan flag ini di setup_driver():
```python
options.add_argument("--no-sandbox")            # WAJIB di Linux
options.add_argument("--disable-dev-shm-usage") # Cegah crash
```

### Status pyqt5-tools (Qt Designer) per OS:
| OS | Status |
|----|--------|
| Windows | ✅ `pip install pyqt5-tools` langsung jalan |
| Mac | ❌ Sering gagal — skip, desain GUI langsung di kode |
| Linux | ❌ Pakai `sudo apt install qttools5-dev-tools` |

> pyqt5-tools bukan keharusan. Bisa desain GUI langsung di kode Python tanpa Qt Designer.

### .gitignore — pastikan file OS tidak ter-commit:
```gitignore
__pycache__/
*.py[cod]
output/
logs/
.env
.vscode/
.idea/
.DS_Store      # Mac — wajib ada!
Thumbs.db      # Windows
```

---

## 📅 Timeline Pengerjaan

### HARI 1 — Rabu 5 Maret (Fondasi)

| Siapa | Target |
|-------|--------|
| **Kemal** | ✅ `config.py` DULUAN — pakai pathlib, semua orang butuh ini! |
| **Darva** | Setup repo + buat semua branch `dev/` + Selenium jalan headless |
| **Richard** | `gui.py` skeleton — window muncul, tabel kosong |
| **Kyla** | `gui.py` input panel — URL, limit, date picker |
| **Kemal** | `logger.py` setelah config.py selesai |
| **Aulia** | `style.py` dasar |

### HARI 2 — Kamis 6 Maret (Fitur Utama)

**Pagi:**
| Siapa | Target |
|-------|--------|
| **Darva** | `scrape_article()` + `is_artikel_valid()` + delay + `worker.py` |
| **Kemal** | `handle_pagination()` + `exporter.py` CSV |
| **Richard** | Sambungkan progress bar ke sinyal worker |
| **Kyla** | Validasi input + toggle date picker |
| **Aulia** | Polish stylesheet sesuai komponen Richard & Kyla |

**Malam — INTEGRASI PERTAMA:**
```
Darva + Richard → worker tersambung ke GUI
                  test: klik Mulai → data valid muncul real-time di tabel ✅
Darva + Kyla    → filter tanggal tersambung
                  test: pilih tanggal → hasil tersaring ✅
Kemal           → test export CSV dengan data real
```

### HARI 3 — Jumat 7 Maret (Polish & Docs)

**Pagi:**
| Siapa | Target |
|-------|--------|
| **Darva** | `filter.py` final + review semua PR + `main.py` final |
| **Richard** | Bug fix dari hasil testing integrasi |
| **Kemal** | Export Excel + test 3 website + cek anti-hardcode |
| **Kyla** | Edge case validasi |
| **Aulia** | Final stylesheet + ambil screenshot |

**Siang:**
| Siapa | Target |
|-------|--------|
| **Aulia** | Finalisasi PDF + `README.md` + `requirements.txt` |
| **Darva** | Final merge semua branch ke main |
| **Semua** | Cek jumlah commit, pastikan repo public |

---

## 🔗 Diagram Ketergantungan Tugas

```
config.py (Kemal) ← HARUS SELESAI DULUAN (pakai pathlib!)
    │
    ├──► scraper.py (Darva)
    │    ├── MIN_JUDUL_CHARS, MIN_ISI_CHARS → is_artikel_valid()
    │    └──► worker.py (Darva) ──► Integrasi GUI
    │
    ├──► logger.py → exporter.py (Kemal)
    │
    ├──► filter.py (Darva) — FILTER_INCLUDE_UNKNOWN_DATE
    │
    ├──► gui.py Richard (main window + tabel)
    └──► gui.py Kyla (input + filter) → filter.py
```

---

## ⚙️ Ketentuan Teknis Penting

| Ketentuan | Detail |
|-----------|--------|
| **PyQt versi** | PyQt5 ≥ 5.15 — **BUKAN PyQt6!** |
| **Threading** | `QThread`, BUKAN `threading.Thread` biasa |
| **Delay** | 1.5 detik antar request dari `config.DEFAULT_DELAY` |
| **Headless** | Chrome tanpa tampilan jendela |
| **General** | Selector umum: `h1`, `article`, `time` — jangan hardcode nama website |
| **Validasi** | `is_artikel_valid()` wajib, threshold dari `config.py` |
| **Fallback** | Field tidak ada → `"-"`, jangan crash |
| **Path file** | Wajib `pathlib.Path` — kompatibel Windows/Mac/Linux |
| **Worker** | Simpan di `self.worker`, bukan variabel lokal (anti garbage collect) |

---

## 📦 Requirements

```
# requirements.txt — runtime, ini yang dikumpulkan ke dosen
selenium
PyQt5>=5.15.0
pandas
openpyxl
webdriver-manager

# requirements-dev.txt — development tools, JANGAN ikut dikumpulkan
pyqt5-tools       ← Windows saja; Mac/Linux lihat OS_GUIDE.md
```

```bash
# Install runtime (semua OS):
pip install -r requirements.txt      # Windows
pip3 install -r requirements.txt     # Mac / Linux
```

---

## 📤 Output yang Dikumpulkan

- [ ] Link GitHub — repo **PUBLIC**, semua branch di-merge ke `main`
- [ ] Screenshot minimal 3 — ada di `docs/screenshots/`
- [ ] PDF laporan — **maks 3 halaman**

---

## ❓ FAQ Tim

**Q: Harus bisa scraping semua website di dunia?**
> Tidak. Cukup jalan di 3-5 website berita Indonesia yang strukturnya mirip.

**Q: Pagination itu apa?**
> Tombol "1 2 3 Next »" di bawah daftar berita. Program harus bisa klik & lanjut.

**Q: Kenapa harus delay?**
> Kalau buka 100 halaman sekaligus tanpa jeda, server website bisa ban IP kita.

**Q: Hardcode itu apa contohnya?**
> `if "detik.com" in url` atau `driver.find_element(By.CLASS_NAME, "detail__title")`. Harus dihindari — pakai selector generik.

**Q: Kenapa ada is_artikel_valid()?**
> Dosen: "data yang diambil harus valid dan tidak kosong". Threshold-nya ada di config.py supaya bisa diubah tanpa edit kode scraper.

**Q: Kenapa MIN_JUDUL_CHARS ada di config.py, bukan langsung di scraper.py?**
> Supaya bisa diubah tanpa edit kode. Kalau dosen tanya "kenapa 5 karakter?" — jawab: "bisa dikonfigurasi di config.py sesuai kebutuhan."

**Q: FILTER_INCLUDE_UNKNOWN_DATE itu apa?**
> Kalau tanggal artikel tidak bisa dibaca, apakah tetap tampil (True) atau dibuang (False) saat filter aktif. Default True supaya data tidak hilang tanpa sebab.

**Q: Bedanya requirements.txt dan requirements-dev.txt?**
> `requirements.txt` = library untuk menjalankan app (dikumpulkan ke dosen). `requirements-dev.txt` = tools development yang tidak dibutuhkan dosen saat testing.

**Q: Qt Designer tidak bisa install di Mac/Linux?**
> Benar. pyqt5-tools sering gagal di Mac/Linux. Alternatif: desain GUI langsung di kode, atau install Qt Designer standalone (`brew install qt` / `apt install qttools5-dev-tools`).

**Q: Kenapa harus pakai pathlib bukan string path biasa?**
> String `"logs\\scraper.log"` error di Mac/Linux karena pakai backslash. `pathlib.Path("logs") / "scraper.log"` otomatis pakai separator yang benar di semua OS.

---

*Update jika ada perubahan kesepakatan → update juga AI_CONTEXT.md + AI_CONTEXT_SHORT.md → kabari semua anggota.*
