# 📰 News Scraper App

Aplikasi desktop Python untuk **scraping artikel berita otomatis** dari website berita Indonesia. Cukup masukkan URL halaman berita, dan aplikasi akan mengumpulkan semua artikel beserta isinya secara otomatis.

**Stack:** Python 3.8+ · Selenium · PyQt5 ≥ 5.15 · pandas · openpyxl

---

## ✨ Fitur

- **Scraping otomatis** — masukkan URL homepage/kategori berita, aplikasi mengambil semua artikel
- **Pagination** — otomatis mengikuti halaman berikutnya (Next, Selanjutnya, dll.)
- **Filter tanggal** — opsional, saring artikel berdasarkan rentang tanggal
- **Limit artikel** — atur jumlah maksimal artikel yang diambil (1–500)
- **Validasi data** — hanya artikel valid (judul & isi tidak kosong) yang ditampilkan
- **Progress real-time** — progress bar dan tabel terisi secara live saat scraping berjalan
- **GUI responsif** — antarmuka tidak freeze saat scraping (menggunakan QThread)
- **Export CSV & Excel** — simpan hasil scraping ke file `.csv` atau `.xlsx`
- **Headless browser** — Selenium berjalan tanpa membuka jendela browser

---

## 📋 Prasyarat

- **Python** 3.8 atau lebih baru
- **Google Chrome** terinstall (Selenium menggunakan ChromeDriver)
- **pip** (Python package manager)

---

## 🚀 Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/<username>/news-scraper-app.git
   cd news-scraper-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   > Pada Mac/Linux gunakan `pip3` jika `pip` mengarah ke Python 2.

---

## ▶️ Cara Menjalankan

```bash
python main.py
```
> Pada Mac/Linux gunakan `python3 main.py` jika diperlukan.

### Alur Penggunaan

1. Masukkan **URL** halaman berita (contoh: halaman kategori)
2. *(Opsional)* Atur **limit** jumlah artikel
3. *(Opsional)* Centang **Filter Tanggal** dan pilih rentang tanggal
4. Klik **Mulai Scraping** — tunggu progress bar selesai
5. Hasil muncul di tabel: No, Judul, Tanggal, Penulis, Kategori, URL, Gambar
6. Klik **Export CSV** atau **Export Excel** untuk menyimpan data

---

## 📁 Struktur Proyek

```
news-scraper-app/
├── main.py           ← Entry point aplikasi
├── config.py         ← Pengaturan global (konstanta, path, threshold)
├── scraper.py        ← Logika scraping dengan Selenium
├── worker.py         ← QThread: jembatan GUI ↔ scraper
├── filter.py         ← Filter artikel berdasarkan tanggal
├── gui.py            ← Tampilan GUI (InputPanel + MainWindow)
├── style.py          ← QSS stylesheet untuk tampilan aplikasi
├── exporter.py       ← Export data ke CSV & Excel
├── logger.py         ← Logging & error handling
├── requirements.txt  ← Dependensi runtime
├── output/           ← Folder hasil export
├── logs/             ← Folder log aplikasi
└── docs/             ← Dokumentasi & screenshot
```

---

## 📸 Screenshot

> Screenshot tersedia di folder `docs/screenshots/`

| Tampilan Awal | Saat Scraping | Hasil Selesai |
|:---:|:---:|:---:|
| ![Awal](docs/screenshots/ss1_awal.png) | ![Scraping](docs/screenshots/ss2_scraping.png) | ![Selesai](docs/screenshots/ss3_selesai.png) |

---

## 👥 Tim Pengembang

| Nama | Peran |
|------|-------|
| **Darva** | Lead Developer + Reviewer |
| **Kemal** | Data & Reliability Dev |
| **Richard** | GUI Developer (Fungsional) |
| **Kyla** | GUI Developer (Input & Filter) |
| **Aulia** | UI Polish + Dokumentasi |

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan tugas kelompok mata kuliah Web Scraping.
