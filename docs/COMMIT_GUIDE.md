# 📝 GIT COMMIT GUIDE — News Scraper Team
> Commit message yang baik = tim paham apa yang berubah tanpa harus buka kodenya
> Ini juga berpengaruh ke kesan dosen saat lihat history GitHub kalian!

---

## 🏗️ Format Commit Message

```
<tipe>(<file>): <deskripsi singkat>

[opsional: penjelasan tambahan]
```

### Tipe yang dipakai:
| Tipe | Kapan dipakai |
|------|--------------|
| `feat` | Menambah fitur baru |
| `fix` | Memperbaiki bug |
| `style` | Perubahan tampilan/styling (tanpa ubah logika) |
| `refactor` | Rapikan/restruktur kode (tanpa ubah fungsi) |
| `docs` | Update dokumentasi / README / komentar |
| `test` | Menambah atau memperbaiki testing |
| `chore` | Setup awal, install library, gitignore, dsb |

---

## ✅ Contoh Commit yang BAIK

### Darva — scraper.py, worker.py, filter.py, main.py
```bash
# scraper.py
git commit -m "chore(scraper): setup Selenium headless driver dengan user-agent"
git commit -m "feat(scraper): tambah fungsi get_all_links() ambil link dari halaman"
git commit -m "feat(scraper): implementasi scrape_article() ekstrak judul tanggal isi"
git commit -m "feat(scraper): tambah delay antar request dari config.DEFAULT_DELAY"
git commit -m "feat(scraper): tambah is_artikel_valid() validasi data tidak kosong"
git commit -m "fix(scraper): perbaiki _is_artikel_link() yang filter link terlalu agresif"

# worker.py
git commit -m "feat(worker): implementasi QThread ScraperWorker dengan 5 sinyal"
git commit -m "feat(worker): tambah logika skip artikel tidak valid via is_artikel_valid"
git commit -m "refactor(worker): pindahkan logika filter ke setelah semua artikel selesai"

# filter.py
git commit -m "feat(filter): tambah fungsi parse_tanggal() support format Indonesia"
git commit -m "feat(filter): implementasi filter_by_date() dengan range tanggal"
git commit -m "fix(filter): perbaiki parsing tanggal format DD/MM/YYYY"

# main.py
git commit -m "feat(main): inisialisasi QApplication dan buka MainWindow"
git commit -m "feat(main): buat folder output/ dan logs/ otomatis saat startup"
git commit -m "chore(main): tambah .gitignore untuk output, logs, pycache"
git commit -m "feat(main): sambungkan semua modul di entry point"
```

### Kemal — config.py, logger.py, exporter.py
```bash
git commit -m "chore(config): buat config.py dengan semua pengaturan default"
git commit -m "feat(logger): setup logging ke file dan terminal sekaligus"
git commit -m "feat(logger): tambah fungsi log_info, log_error, log_warning"
git commit -m "feat(exporter): implementasi export_csv() dengan encoding utf-8-sig"
git commit -m "feat(exporter): implementasi export_excel() dengan auto-width kolom"
git commit -m "fix(exporter): perbaiki urutan kolom sesuai CSV_HEADERS di config"
git commit -m "test(exporter): tambah data dummy untuk test export di __main__"
```

### Richard — gui.py (fungsional)
```bash
git commit -m "chore(gui): setup QMainWindow dengan layout dasar"
git commit -m "feat(gui): tambah QTableWidget 7 kolom sesuai kesepakatan tim"
git commit -m "feat(gui): tambah QProgressBar dan label status scraping"
git commit -m "feat(gui): tambah tombol Mulai Scraping, Stop, Export CSV, Export Excel"
git commit -m "feat(gui): implementasi fungsi tambah_baris() terima sinyal dari worker"
git commit -m "feat(gui): sambungkan ScraperWorker ke GUI lewat sinyal"
git commit -m "fix(gui): perbaiki tombol Export yang tidak disable saat scraping berjalan"
git commit -m "feat(gui): implementasi dialog export file dengan QFileDialog"
```

### Kyla — gui.py (input panel)
```bash
git commit -m "feat(gui): buat class InputPanel dengan QGroupBox"
git commit -m "feat(gui): tambah QLineEdit input URL dengan placeholder"
git commit -m "feat(gui): tambah QSpinBox untuk limit artikel range 1-500"
git commit -m "feat(gui): tambah QCheckBox dan QDateEdit untuk filter tanggal"
git commit -m "feat(gui): implementasi toggle aktifkan/nonaktifkan date picker"
git commit -m "feat(gui): tambah validasi URL tidak boleh kosong dan harus https"
git commit -m "fix(gui): perbaiki validasi tanggal start tidak boleh lebih besar dari end"
```

### Aulia — style.py, docs
```bash
git commit -m "chore(style): buat style.py dengan variabel warna dan fungsi apply_style"
git commit -m "style(style): tambah QSS untuk QPushButton dengan warna per fungsi"
git commit -m "style(style): tambah QSS untuk QTableWidget dengan alternating rows"
git commit -m "style(style): tambah QSS untuk QProgressBar dan QGroupBox"
git commit -m "style(style): polish hover effect dan warna disabled state tombol"
git commit -m "docs(readme): tulis cara install dan cara jalankan aplikasi"
git commit -m "docs(readme): tambah tabel fitur dan struktur project"
git commit -m "docs(laporan): tambah screenshot aplikasi ke folder docs/screenshots"
git commit -m "docs(laporan): finalisasi PDF laporan 3 halaman"
```

---

## ❌ Contoh Commit yang BURUK

```bash
# ❌ Terlalu singkat, tidak informatif
git commit -m "update"
git commit -m "fix bug"
git commit -m "aaa"
git commit -m "coba"
git commit -m "done"
git commit -m "waduh"

# ❌ Terlalu panjang dan campur-campur
git commit -m "tambah fungsi scraping dan juga perbaiki gui dan update config dan export juga"

# ❌ Tidak jelas perubahan apa
git commit -m "perubahan kode"
git commit -m "revisi"
```

---

## 🔄 Alur Kerja Git Harian

```bash
# 1. Pastikan kamu di branch sendiri
git checkout dev/namakamu

# 2. Sebelum mulai coding, sync dulu dari main
git pull origin main

# 3. Coding... coding...

# 4. Cek apa yang berubah
git status
git diff

# 5. Stage perubahan
git add nama_file.py        # kalau mau pilih file tertentu
# atau
git add .                   # semua perubahan

# 6. Commit dengan pesan yang jelas
git commit -m "feat(gui): tambah validasi input URL"

# 7. Push ke branch kamu
git push origin dev/namakamu

# 8. Kalau sudah siap merge → buat Pull Request di GitHub
#    Assign ke Darva sebagai reviewer
```

---

## 💡 Tips Commit yang Bagus

```
✅ 1 commit = 1 perubahan yang jelas (bukan campur-campur)
✅ Commit sesering mungkin — lebih baik 10 commit kecil dari 1 commit besar
✅ Commit setiap kali 1 fungsi/fitur selesai dan berjalan
✅ Jangan commit kode yang masih error / belum jalan

❌ Jangan commit file output/ atau logs/ (sudah ada di .gitignore)
❌ Jangan commit file .pyc atau __pycache__
```

---

## 📄 .gitignore yang Harus Ada di Root Repo

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.env

# Output & Logs
output/
logs/

# IDE
.vscode/
.idea/
*.code-workspace

# OS
.DS_Store
Thumbs.db
```

> Darva: buat file `.gitignore` ini di root repo di hari pertama — sebelum yang lain push!

---

## 🎯 Target Minimum Commit Per Orang

| Nama | Target Commit | Catatan |
|------|--------------|---------|
| Darva | 10-12 | scraper + worker + filter + main + review |
| Kemal | 6-8 | config + logger + exporter |
| Richard | 6-8 | gui fungsional |
| Kyla | 5-6 | gui input panel |
| Aulia | 5-6 | style + docs + screenshot |

---

*Commit history yang rapi = nilai GitHub yang bagus = tim profesional 💪*
