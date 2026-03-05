# ✅ CHECKLIST TESTING — News Scraper App
> Wajib dicek semua sebelum submit! Centang satu per satu.

---

## 🔴 FASE 1 — Test Per Modul
> Setiap orang test file miliknya sendiri

### Kemal — config.py, logger.py, exporter.py
```
[x] python config.py        → tidak ada error saat diimport
[x] python logger.py        → file logs/scraper.log terbuat otomatis
[x] python exporter.py      → folder output/ terbuat, file CSV & .xlsx muncul
[x] Buka CSV                → kolom sesuai CSV_HEADERS, encoding utf-8-sig
[x] Buka .xlsx              → terbuka normal, auto-width kolom
[x] Cek logger.py           → log_info, log_error, log_warning tulis ke .log + console
[x] Config values           → MAX_ISI=2000, MIN_JUDUL=15, MIN_ISI=100, CSV_ENCODING="utf-8-sig"
```

### Darva — scraper.py, filter.py, worker.py
```
[x] python scraper.py       → minimal 1 link berhasil diambil
[x] scrape_article()        → return dict 7 field (tidak ada None, pakai "-")
[x] 3-layer extraction      → OpenGraph/Schema → wildcard → site-specific semua berfungsi
[x] get_all_links()         → same-domain filter, path_depth≥3, NON_ARTIKEL keywords
[x] handle_pagination()     → 4 strategi dicoba secara berurutan
[x] is_artikel_valid()      → False jika judul <15ch atau isi <100ch
[x] is_artikel_valid()      → True jika judul ≥15ch dan isi ≥100ch
[x] filter.py               → parse_tanggal() support ISO, DD/MM/YYYY, "04 Mar 2025", "4 Maret 2025"
[x] filter.py               → filter_by_date() dengan range + FILTER_INCLUDE_UNKNOWN_DATE
[x] worker.py               → tidak ada ImportError saat diimport
```

### Richard + Kyla — gui.py
```
[x] python main.py          → window muncul dark theme (#0F1117)
[x] Input URL               → bisa diketik, placeholder, clearButton
[x] SpinBox limit           → range 1-500, default 20, suffix " artikel"
[x] Checkbox filter         → centang → DateEdit aktif; uncheck → disabled
[x] DatePicker              → calendarPopup muncul, format dd/MM/yyyy
[x] Tabel                   → 7 kolom: #, Judul, Tanggal, Penulis, Kategori, Isi (preview), URL
[x] Tombol Stop             → muncul tapi disabled saat idle
[x] Tombol Export            → muncul tapi disabled saat belum ada data
[x] Bottom bar              → dot ● + state SIAP + delay + headless + logfile
```

### Aulia — style.py
```
[x] python main.py          → dark theme diterapkan (#0F1117 bg)
[x] Tombol scrape           → biru #4F8EF7 dengan hover
[x] Tombol stop             → outline merah #F75A5A
[x] Tombol export           → outline teal #00D4AA
[x] Progress bar            → gradient biru→teal chunk
[x] Tabel                   → alternating rows, header monospace
[x] Bottom bar              → #181C27 bg, monospace labels
[x] Dialog detail           → dark bg, QTextBrowser styled
```

---

## 🟡 FASE 2 — Test Integrasi

```
[x] Klik "Mulai Scraping" tanpa URL    → QMessageBox warning "URL tidak boleh kosong"
[x] Klik "Mulai Scraping" URL salah    → QMessageBox warning format http/https
[x] Klik "Mulai Scraping" URL valid    → progress bar mulai bergerak
[x] Saat scraping                      → GUI TIDAK freeze (QThread)
[x] Saat scraping                      → Stop aktif, Scrape disabled, bottom bar "SCRAPING AKTIF"
[x] Data muncul di tabel               → real-time per artikel (sinyal_hasil)
[x] Isi di tabel                       → preview 150ch + "..."
[x] Artikel judul/isi tidak valid      → DILEWATI (is_artikel_valid)
[x] Progress bar                       → bergerak 0% sampai 100%, gradient chunk
[x] Setelah selesai                    → label "Selesai", state idle, Export aktif
[x] Klik Stop tengah scraping          → berhenti graceful, tidak crash
[x] Double-click baris                 → dialog detail: gambar + isi 2000ch + meta + URL link
```

---

## 🟢 FASE 3 — Test Fitur Opsional

```
[x] Export CSV    → file di output/, encoding utf-8-sig, kolom sesuai CSV_HEADERS
[x] Export Excel  → file di output/, .xlsx, auto-width kolom
[x] Filter tanggal aktif + URL valid → hanya artikel dalam rentang yang muncul
[x] Filter tanggal range sempit → bisa return 0 artikel (tidak crash)
[x] Limit 5 artikel → hanya 5 link diambil
[x] Log file      → logs/scraper.log terisi, timestamp + level
[x] Error handling → URL tidak bisa diakses → sinyal_error → QMessageBox (tidak crash)
```

---

## 🔵 FASE 4 — Test Website (3 website berbeda)

| Website | URL Test | Status |
|---------|----------|--------|
| CNN Indonesia | https://www.cnnindonesia.com | `[x] Lulus 5/5` |
| Detik | https://www.detik.com/ | `[x] Lulus 4/5` |
| Kompas Nasional | https://nasional.kompas.com/ | `[x] Lulus 5/5` |

Untuk setiap website:
```
[x] Link artikel ditemukan (same-domain, path_depth≥3)
[x] Judul berhasil diambil (bukan "-" semua) — via L1/L2/L3
[x] Isi berhasil diambil, dipotong max 2000ch
[x] Tidak ada crash / error fatal
[x] is_artikel_valid() menyaring yang tidak lengkap
```

---

## 🚫 FASE 4B — Anti-Hardcode Check

> 3-layer strategy → L3 adalah OPTIMASI, bukan hardcode satu-satunya

```
[x] scraper.py → L1 (OpenGraph/Schema) dan L2 (wildcard) dicoba DULUAN sebelum L3
[x] scraper.py → selector pakai tag umum: h1, article, time, [class*='...']
[x] scraper.py → L3 class spesifik ada tapi sebagai fallback terakhir
[x] get_all_links() → filter berdasarkan domain dan path, bukan nama website
[x] Test dengan website BARU → L1+L2 masih bisa ambil minimal judul
```

---

## 🏁 FASE 5 — Final Check

### Code & Repo
```
[x] requirements.txt lengkap: selenium, PyQt5>=5.15.0, pandas, openpyxl, webdriver-manager
[x] README.md ada cara install & cara jalankan
[x] File .gitignore ada (output/, logs/, __pycache__)
```

### Aplikasi
```
[x] python main.py berjalan tanpa error
[x] pip install -r requirements.txt tidak error
[x] Folder output/ dan logs/ terbuat otomatis (pathlib mkdir)
[x] is_artikel_valid() aktif dan menyaring data
```

### Screenshot (simpan di docs/screenshots/)
```
[ ] SS 1 — Tampilan awal: dark theme, semua komponen terlihat
[ ] SS 2 — Saat scraping: progress bar gradient aktif, data masuk
[ ] SS 3 — Selesai: tabel penuh artikel, bottom bar SIAP
[ ] SS 4 (bonus) — Dialog detail: gambar + isi + meta
[ ] SS 5 (bonus) — Hasil export terbuka di Excel
```

---

## 🐛 Kalau Ada yang Tidak Lulus

1. Catat error message lengkap
2. Screenshot terminal/aplikasi saat error
3. Cek OS (Linux), Python version (3.12), Chrome version (145)
4. Tag Darva di grup dengan error + screenshot
