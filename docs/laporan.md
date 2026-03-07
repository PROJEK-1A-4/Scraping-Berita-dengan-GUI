# 📰 Laporan Proyek — News Scraper App

**Tugas Kelompok Web Scraping**

---

## Halaman 1 — Informasi Tim & Deskripsi Aplikasi

### Informasi Tim

| No | Nama | Peran |
|----|------|-------|
| 1 | Darva | Lead Developer + Reviewer |
| 2 | Kemal | Data & Reliability Dev |
| 3 | Richard | GUI Developer (Fungsional) |
| 4 | Kyla | GUI Developer (Input & Filter) |
| 5 | Aulia | UI Polish + Dokumentasi |

### Deskripsi Aplikasi

**News Scraper App** adalah aplikasi desktop berbasis Python yang dapat mengambil data berita secara otomatis dari website berita Indonesia. User cukup memasukkan satu URL halaman berita (homepage atau kategori), dan aplikasi akan mengumpulkan semua artikel beserta isinya, lalu menampilkan hasilnya dalam tabel yang rapi.

### Daftar Fitur

| No | Fitur | Keterangan |
|----|-------|------------|
| 1 | Scraping Otomatis | Mengambil semua artikel dari URL menggunakan Selenium headless (Chrome 145) |
| 2 | 3-Layer Extraction | OpenGraph/Schema.org → wildcard CSS → site-specific untuk akurasi tinggi |
| 3 | Pagination | Otomatis mengikuti halaman berikutnya (4 strategi: rel=next, teks, URL pattern) |
| 4 | Filter Tanggal | Menyaring artikel berdasarkan rentang tanggal, parse multi-format Indonesia & Inggris |
| 5 | Limit Artikel | Mengatur jumlah maksimal artikel (1–500, default 20) |
| 6 | Validasi Data | Hanya artikel valid (judul ≥15ch & isi ≥100ch) yang ditampilkan |
| 7 | Tabel 7 Kolom | #, Judul, Tanggal, Penulis, Kategori, Isi (preview 150ch), URL |
| 8 | Dialog Detail | Double-click baris → popup dengan gambar asli (QPixmap) + isi 2000ch + meta |
| 9 | Progress Real-time | Progress bar gradient biru→teal + label status |
| 10 | GUI Responsif | Antarmuka tidak freeze saat scraping (QThread) |
| 11 | Export CSV & Excel | Menyimpan hasil ke `.csv` (utf-8-sig) atau `.xlsx` (auto-width) |
| 12 | Bottom Status Bar | Dot indicator (SIAP/AKTIF) + delay + headless + logfile |
| 13 | Dark Theme | QSS styling sesuai gui-mockup.html (#0F1117 bg, #4F8EF7 accent, #00D4AA teal) |
| 14 | Logging | Pencatatan aktivitas dan error ke file log + console |

### Teknologi yang Digunakan

- **Python 3.12** — Bahasa pemrograman utama
- **Selenium** — Web scraping dengan browser automation (headless Chrome 145)
- **PyQt5 ≥ 5.15** — Framework GUI desktop
- **pandas** — Manipulasi data untuk export
- **openpyxl** — Export ke format Excel (.xlsx)
- **webdriver-manager** — Manajemen ChromeDriver otomatis

---

## Halaman 2 — Arsitektur & Pembagian Tugas

### Diagram Arsitektur Modul

```
main.py  ─────── Entry point: buat folder, setup logger, apply style, MainWindow
  │
  ├── config.py ──────── Konstanta global
  │     MAX_ISI_CHARS=2000, MIN_JUDUL=15, MIN_ISI=100
  │     CSV_ENCODING, EXCEL_ENGINE, LOG_FORMAT, LOG_LEVEL
  │
  ├── style.py ───────── Dark theme QSS (#0F1117 bg, #4F8EF7 accent, #00D4AA teal)
  │
  ├── gui.py ─────────── Tampilan GUI
  │     ├── InputPanel ── URL, limit, date picker (calendarPopup), validasi
  │     └── MainWindow ── Tabel 7 kolom, progress bar gradient, tombol aksi,
  │                       bottom bar (dot + state + delay + headless + logfile),
  │                       dialog detail double-click (gambar + isi 2000ch)
  │
  ├── worker.py ──────── QThread: jembatan GUI ↔ scraper
  │     └── ScraperWorker ── 5 sinyal (progress, hasil, selesai, error, status)
  │         + filter_aktif, start_date, end_date parameters
  │
  ├── scraper.py ─────── Logika scraping 3-layer
  │     ├── setup_driver() ── Chrome headless + eager + anti-bot
  │     ├── get_all_links() ── same-domain, path_depth≥3, 20+ NON_ARTIKEL kw
  │     ├── handle_pagination() ── 4 strategi (rel=next, teks, URL, berhenti)
  │     ├── scrape_article() ── 3-layer: OG/Schema → wildcard → site-specific
  │     ├── is_artikel_valid() ── threshold dari config
  │     ├── _extract_text() ── helper CSS/XPath selector
  │     └── _extract_meta() ── helper OpenGraph/Schema.org/itemprop
  │
  ├── filter.py ──────── Filter artikel berdasarkan tanggal
  │     ├── parse_tanggal() ── multi-format ID/EN + BULAN_INDONESIA mapping
  │     └── filter_by_date() ── range filter + FILTER_INCLUDE_UNKNOWN_DATE
  │
  ├── exporter.py ────── Export data ke CSV & Excel
  │     ├── export_csv() ── pandas, utf-8-sig, rename kolom
  │     └── export_excel() ── pandas + openpyxl, auto-width
  │
  └── logger.py ──────── Logging & error handling
        ├── setup_logger() ── FileHandler + StreamHandler
        ├── log_info(), log_error(), log_warning()
        └── auto-init jika belum setup
```

### Pembagian Tugas per Anggota

| Anggota | File | Tugas Utama |
|---------|------|-------------|
| **Darva** | `scraper.py`, `worker.py`, `filter.py`, `main.py` | 3-layer scraping, threading, filter tanggal, integrasi |
| **Kemal** | `config.py`, `logger.py`, `exporter.py` | Konfigurasi global, logging, export CSV/Excel |
| **Richard** | `gui.py` (MainWindow) | Tabel 7 kolom, progress bar, tombol, bottom bar, dialog detail |
| **Kyla** | `gui.py` (InputPanel) | Input URL, limit, date picker, validasi input |
| **Aulia** | `style.py`, `README.md`, laporan, screenshot | Dark theme QSS, dokumentasi |

### Ketergantungan Antar Modul

1. `config.py` harus selesai duluan — semua modul import dari sini
2. `scraper.py` bergantung pada `config.py` (threshold validasi, delay, MAX_ISI)
3. `worker.py` menjembatani `scraper.py` + `filter.py` dengan `gui.py`
4. `exporter.py` bergantung pada `config.py` (path output, CSV_HEADERS, CSV_ENCODING)
5. `logger.py` bergantung pada `config.py` (LOG_FILE, LOG_FORMAT)
6. `style.py` independen — tidak bergantung modul lain

---

## Halaman 3 — Alur Scraping & Screenshot

### Alur Scraping Step-by-Step

```
┌─────────────────────────────────────────────────────┐
│  1. USER BUKA APLIKASI                              │
│     → Window dark theme (#0F1117) dengan form input  │
│     → Bottom bar: ● SIAP | DELAY: 1.5s | HEADLESS   │
├─────────────────────────────────────────────────────┤
│  2. USER ISI FORM                                   │
│     → URL homepage/kategori berita                   │
│     → (Opsional) Limit artikel (1-500)               │
│     → (Opsional) Filter tanggal (start–end date)     │
├─────────────────────────────────────────────────────┤
│  3. USER KLIK "▶  Mulai Scraping"                   │
│     → Validasi input (URL, format, tanggal)          │
│     → Progress bar gradient biru→teal bergerak       │
│     → Bottom bar: ● SCRAPING AKTIF                   │
├─────────────────────────────────────────────────────┤
│  4. SELENIUM + 3-LAYER EXTRACTION                   │
│     a. get_all_links() — same-domain, path_depth≥3   │
│     b. handle_pagination() — 4 strategi              │
│     c. scrape_article() per link:                    │
│        L1: OpenGraph + Schema.org meta tags          │
│        L2: wildcard [class*='...'] + semantic HTML   │
│        L3: class spesifik Detik/Kompas/CNN           │
│     d. is_artikel_valid() — judul≥15, isi≥100        │
│     e. filter_by_date() — jika filter aktif          │
│     f. Delay 1.5 detik antar request                 │
├─────────────────────────────────────────────────────┤
│  5. HASIL MUNCUL DI TABEL (real-time per artikel)   │
│     → 7 Kolom: #, Judul, Tanggal, Penulis,          │
│       Kategori, Isi (preview 150ch), URL             │
│     → Double-click → dialog: gambar + isi 2000ch     │
│     → Progress bar penuh = selesai ✅                │
├─────────────────────────────────────────────────────┤
│  6. USER KLIK "Export"                              │
│     → Export CSV (utf-8-sig) atau Excel (.xlsx)      │
│     → File tersimpan di folder output/               │
└─────────────────────────────────────────────────────┘
```

### Hasil Test Scraper (3 Website)

| Website | Links | Valid | Invalid | Status |
|---------|-------|-------|---------|--------|
| CNN Indonesia | 5 | 5 | 0 | ✅ OK |
| Detik | 5 | 4 | 1 | ✅ OK |
| Kompas Nasional | 5 | 5 | 0 | ✅ OK |

### Screenshot Aplikasi

| No | Tampilan | File |
|----|----------|------|
| 1 | Tampilan awal — window sebelum scraping | `docs/screenshots/ss1_awal.png` |
| 2 | Saat scraping — progress bar aktif | `docs/screenshots/ss2_scraping.png` |
| 3 | Selesai — tabel penuh artikel | `docs/screenshots/ss3_selesai.png` |

> **Catatan:** Screenshot diambil setelah semua fitur terintegrasi.

---

*Dibuat oleh Tim News Scraper App*
