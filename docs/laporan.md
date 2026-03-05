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
| 1 | Scraping Otomatis | Mengambil semua artikel dari URL yang diberikan menggunakan Selenium headless |
| 2 | Pagination | Otomatis mengikuti halaman berikutnya (Next, Selanjutnya, dll.) |
| 3 | Filter Tanggal | Menyaring artikel berdasarkan rentang tanggal (opsional) |
| 4 | Limit Artikel | Mengatur jumlah maksimal artikel yang diambil (1–500) |
| 5 | Validasi Data | Hanya menampilkan artikel valid (judul & isi tidak kosong) |
| 6 | Progress Real-time | Progress bar dan tabel terisi secara live saat scraping |
| 7 | GUI Responsif | Antarmuka tidak freeze saat scraping (QThread) |
| 8 | Export CSV & Excel | Menyimpan hasil ke format `.csv` atau `.xlsx` |
| 9 | Logging | Pencatatan aktivitas dan error ke file log |

### Teknologi yang Digunakan

- **Python 3.8+** — Bahasa pemrograman utama
- **Selenium** — Web scraping dengan browser automation
- **PyQt5 ≥ 5.15** — Framework GUI desktop
- **pandas** — Manipulasi data untuk export
- **openpyxl** — Export ke format Excel (.xlsx)
- **webdriver-manager** — Manajemen ChromeDriver otomatis

---

## Halaman 2 — Arsitektur & Pembagian Tugas

### Diagram Arsitektur Modul

```
main.py  ─────── Entry point, inisialisasi app
  │
  ├── config.py ──────── Konstanta global (Selenium, scraping, GUI, path)
  │
  ├── style.py ───────── QSS stylesheet untuk tampilan aplikasi
  │
  ├── gui.py ─────────── Tampilan GUI
  │     ├── InputPanel ── URL input, limit, date picker, validasi
  │     └── MainWindow ── Tabel hasil, progress bar, tombol aksi
  │
  ├── worker.py ──────── QThread: jembatan GUI ↔ scraper
  │     └── ScraperWorker ── 5 sinyal (artikel_baru, progress, selesai, error, log)
  │
  ├── scraper.py ─────── Logika scraping inti
  │     ├── setup_driver() ── Selenium headless + anti-bot
  │     ├── get_all_links() ── Kumpulkan link artikel
  │     ├── handle_pagination() ── Ikuti halaman berikutnya
  │     ├── scrape_article() ── Ekstrak data 1 artikel
  │     └── is_artikel_valid() ── Validasi field wajib
  │
  ├── filter.py ──────── Filter artikel berdasarkan tanggal
  │
  ├── exporter.py ────── Export data ke CSV & Excel
  │
  └── logger.py ──────── Logging & error handling
```

### Pembagian Tugas per Anggota

| Anggota | File | Tugas Utama |
|---------|------|-------------|
| **Darva** | `scraper.py`, `worker.py`, `filter.py`, `main.py` | Logika scraping, threading, filter tanggal, integrasi |
| **Kemal** | `config.py`, `logger.py`, `exporter.py` | Konfigurasi global, logging, export CSV/Excel |
| **Richard** | `gui.py` (MainWindow) | Window utama, tabel, progress bar, tombol aksi |
| **Kyla** | `gui.py` (InputPanel) | Input URL, limit, date picker, validasi input |
| **Aulia** | `style.py`, `README.md`, laporan, screenshot | Styling QSS, dokumentasi, screenshot |

### Ketergantungan Antar Modul

1. `config.py` harus selesai duluan — semua modul import dari sini
2. `scraper.py` bergantung pada `config.py` (threshold validasi)
3. `worker.py` menjembatani `scraper.py` dengan `gui.py`
4. `exporter.py` bergantung pada `config.py` (path output, CSV headers)
5. `style.py` independen — tidak bergantung modul lain

---

## Halaman 3 — Alur Scraping & Screenshot

### Alur Scraping Step-by-Step

```
┌─────────────────────────────────────────────────────┐
│  1. USER BUKA APLIKASI                              │
│     → Muncul window dengan form input               │
├─────────────────────────────────────────────────────┤
│  2. USER ISI FORM                                   │
│     → Masukkan URL homepage/kategori berita          │
│     → (Opsional) Pilih rentang tanggal               │
│     → (Opsional) Set limit jumlah berita             │
├─────────────────────────────────────────────────────┤
│  3. USER KLIK "MULAI SCRAPING"                      │
│     → Validasi input (URL kosong? format salah?)     │
│     → Progress bar mulai bergerak                    │
│     → GUI tetap responsif, tidak freeze              │
├─────────────────────────────────────────────────────┤
│  4. SELENIUM BEKERJA DI BACKGROUND                  │
│     a. Buka URL → kumpulkan semua link artikel       │
│     b. Ikuti pagination (Next / Halaman 2)           │
│     c. Buka tiap link → ambil Judul, Tanggal, Isi   │
│     d. Validasi: skip jika judul/isi kosong          │
│     e. Filter tanggal (jika aktif)                   │
│     f. Delay 1.5 detik antar request                 │
├─────────────────────────────────────────────────────┤
│  5. HASIL MUNCUL DI TABEL                           │
│     → 7 Kolom: No, Judul, Tanggal, Penulis,         │
│       Kategori, URL, Gambar                          │
│     → Progress bar penuh = selesai ✅                │
├─────────────────────────────────────────────────────┤
│  6. USER KLIK "EXPORT"                              │
│     → Pilih format: CSV atau Excel (.xlsx)           │
│     → File tersimpan di folder output/               │
└─────────────────────────────────────────────────────┘
```

### Screenshot Aplikasi

| No | Tampilan | File |
|----|----------|------|
| 1 | Tampilan awal — window sebelum scraping | `docs/screenshots/ss1_awal.png` |
| 2 | Saat scraping — progress bar aktif | `docs/screenshots/ss2_scraping.png` |
| 3 | Selesai — tabel penuh artikel | `docs/screenshots/ss3_selesai.png` |

> **Catatan:** Screenshot diambil setelah semua fitur terintegrasi.

---

*Dibuat oleh Tim News Scraper App — 2025*
