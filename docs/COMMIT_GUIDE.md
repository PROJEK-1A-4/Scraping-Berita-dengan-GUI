# 📝 GIT COMMIT GUIDE — News Scraper Team
> Commit message yang baik = tim paham apa yang berubah tanpa harus buka kodenya

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
git commit -m "chore(scraper): setup Selenium headless driver dengan eager loading"
git commit -m "feat(scraper): tambah _extract_meta() untuk OpenGraph dan Schema.org"
git commit -m "feat(scraper): implementasi 3-layer extraction di scrape_article()"
git commit -m "feat(scraper): tambah get_all_links() dengan same-domain filter dan path_depth"
git commit -m "feat(scraper): implementasi handle_pagination() 4 strategi"
git commit -m "feat(scraper): tambah is_artikel_valid() threshold dari config"

# worker.py
git commit -m "feat(worker): implementasi ScraperWorker QThread dengan 5 sinyal"
git commit -m "feat(worker): tambah filter_by_date di loop scraping"
git commit -m "feat(worker): tambah graceful stop via _running flag"

# filter.py
git commit -m "feat(filter): implementasi parse_tanggal() multi-format ID/EN"
git commit -m "feat(filter): implementasi filter_by_date() dengan FILTER_INCLUDE_UNKNOWN_DATE"

# main.py
git commit -m "feat(main): inisialisasi QApplication + apply_style + MainWindow"
git commit -m "feat(main): buat folder output/ dan logs/ otomatis via pathlib"
```

### Kemal — config.py, logger.py, exporter.py
```bash
git commit -m "chore(config): buat config.py dengan semua konstanta (pathlib)"
git commit -m "feat(config): tambah CSV_ENCODING, EXCEL_ENGINE, LOG_FORMAT, LOG_LEVEL"
git commit -m "feat(logger): setup logging file + console dengan format dari config"
git commit -m "feat(exporter): implementasi export_csv() dengan rename kolom"
git commit -m "feat(exporter): implementasi export_excel() dengan auto-width"
```

### Richard — gui.py (MainWindow)
```bash
git commit -m "feat(gui): setup MainWindow dengan tabel 7 kolom dan progress bar"
git commit -m "feat(gui): tambah bottom status bar (dot, state, delay, headless, logfile)"
git commit -m "feat(gui): implementasi mulai_scraping() dengan worker signals"
git commit -m "feat(gui): implementasi dialog detail double-click dengan gambar QPixmap"
git commit -m "feat(gui): tambah _set_state_idle dan _set_state_scraping"
git commit -m "feat(gui): implementasi export_csv dan export_excel dari tabel"
```

### Kyla — gui.py (InputPanel)
```bash
git commit -m "feat(gui): buat InputPanel dengan URL, limit, date picker"
git commit -m "feat(gui): tambah validasi URL dan date range"
git commit -m "feat(gui): tambah calendarPopup dan toggle filter tanggal"
git commit -m "feat(gui): implementasi get_inputs() return dict lengkap"
```

### Aulia — style.py, docs
```bash
git commit -m "feat(style): implementasi dark theme QSS sesuai gui-mockup.html"
git commit -m "style(style): tambah per-button styling (stop, export) via objectName"
git commit -m "style(style): tambah progress bar gradient biru→teal"
git commit -m "style(style): tambah bottom bar dan dialog styling"
git commit -m "docs(readme): tulis README dengan fitur, install, dan struktur"
git commit -m "docs(laporan): finalisasi laporan proyek"
```

---

## ❌ Contoh Commit yang BURUK

```bash
# ❌ Terlalu singkat
git commit -m "update"
git commit -m "fix bug"
git commit -m "done"

# ❌ Campur-campur
git commit -m "tambah scraping dan perbaiki gui dan update config"

# ❌ Tidak jelas
git commit -m "perubahan kode"
git commit -m "revisi"
```

---

## 🔄 Alur Kerja Git Harian

```bash
# 1. Pastikan di branch sendiri
git checkout dev/namakamu

# 2. Sync dari main
git pull origin main

# 3. Coding...

# 4. Cek perubahan
git status && git diff

# 5. Stage & commit
git add nama_file.py
git commit -m "feat(gui): tambah validasi input URL"

# 6. Push
git push origin dev/namakamu

# 7. Buat Pull Request → assign ke Darva
```

---

## 💡 Tips Commit

```
✅ 1 commit = 1 perubahan yang jelas
✅ Commit sesering mungkin — 10 commit kecil > 1 commit besar
✅ Jangan commit kode yang masih error

❌ Jangan commit file output/ atau logs/
❌ Jangan commit __pycache__
```

---

## 📄 .gitignore

```gitignore
__pycache__/
*.py[cod]
*.pyo
.env
output/
logs/
.vscode/
.idea/
*.code-workspace
.DS_Store
Thumbs.db
```

---

## 🎯 Target Minimum Commit Per Orang

| Nama | Target Commit | Catatan |
|------|--------------|---------|
| Darva | 10-12 | scraper + worker + filter + main + review |
| Kemal | 6-8 | config + logger + exporter |
| Richard | 6-8 | gui fungsional |
| Kyla | 5-6 | gui input panel |
| Aulia | 5-6 | style + docs + screenshot |
