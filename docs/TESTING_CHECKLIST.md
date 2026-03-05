# ✅ CHECKLIST TESTING — News Scraper App
> Wajib dicek semua sebelum submit! Centang satu per satu.
> Lakukan testing di branch `dev/masing-masing` dulu, baru merge ke main.

---

## 🔴 FASE 1 — Test Per Modul (Hari 2, setelah coding selesai)
> Setiap orang test file miliknya sendiri sebelum integrasi

### Kemal — config.py, logger.py, exporter.py
```
[ ] python config.py        → tidak ada error saat diimport
[ ] python logger.py        → file logs/scraper.log terbuat otomatis
[ ] python exporter.py      → folder output/ terbuat, file test_export.csv & .xlsx muncul
[ ] Buka test_export.csv    → 2 baris data dummy muncul, kolom sesuai CSV_HEADERS
[ ] Buka test_export.xlsx   → sama, terbuka normal di Excel/Google Sheets
[ ] Cek logger.py           → log_info, log_error, log_warning semua tulis ke .log
```

### Darva — scraper.py, filter.py, worker.py
```
[ ] python scraper.py       → minimal 1 link artikel berhasil diambil dari URL test
[ ] python scraper.py       → scrape_article() return dict dengan 7 field (tidak ada None)
[ ] is_artikel_valid()      → return False kalau judul atau isi adalah "-" atau terlalu pendek
[ ] is_artikel_valid()      → return True kalau judul dan isi ada dan cukup panjang
[ ] python filter.py        → filter_by_date() dengan data dummy berhasil menyaring
[ ] python filter.py        → kalau start_date & end_date = None → return semua artikel
[ ] worker.py               → tidak ada ImportError saat diimport
[ ] Semua field artikel     → tidak ada yang None atau "" (harus "-" kalau kosong)
```

### Richard + Kyla — gui.py
```
[ ] python main.py          → window muncul tanpa error
[ ] Input URL               → bisa diketik
[ ] SpinBox limit           → bisa diubah angkanya, range 1-500
[ ] Checkbox filter tanggal → saat dicentang, DateEdit aktif; saat uncheck, DateEdit grey
[ ] DatePicker              → calendar popup muncul saat diklik
[ ] Tombol Stop             → muncul tapi disabled saat belum scraping
[ ] Tombol Export           → muncul tapi disabled saat belum ada data
[ ] Tabel                   → 7 kolom dengan header yang benar
```

### Aulia — style.py
```
[ ] python main.py          → tampilan tidak default/jelek (stylesheet diterapkan)
[ ] Semua tombol            → warna sesuai fungsinya (primer, danger, success)
[ ] Tabel                   → alternating row color terlihat
[ ] GroupBox                → ada judul "Pengaturan Scraping"
[ ] Tidak ada komponen      → yang terpotong atau tidak kelihatan
```

---

## 🟡 FASE 2 — Test Integrasi (Hari 2 malam, setelah sambungkan GUI + scraper)

```
[ ] Klik "Mulai Scraping" tanpa isi URL    → muncul pesan error "URL tidak boleh kosong"
[ ] Klik "Mulai Scraping" dengan URL salah → muncul pesan error "URL harus http/https"
[ ] Klik "Mulai Scraping" dengan URL valid → progress bar mulai bergerak
[ ] Saat scraping berjalan                 → GUI TIDAK freeze (masih bisa diklik)
[ ] Saat scraping berjalan                 → tombol Stop aktif, tombol Scrape disabled
[ ] Data muncul di tabel                   → real-time per artikel (tidak nunggu selesai)
[ ] Artikel dengan judul/isi kosong        → DILEWATI, tidak masuk tabel (is_artikel_valid)
[ ] Progress bar                           → bergerak dari 0% sampai 100%
[ ] Setelah selesai                        → popup "Scraping selesai! X artikel"
[ ] Setelah selesai                        → tombol Export CSV & Excel aktif
[ ] Klik Stop di tengah scraping           → scraping berhenti, tidak crash
```

---

## 🟢 FASE 3 — Test Fitur Opsional (Hari 3 pagi)

```
[ ] Export CSV    → file tersimpan di output/, bisa dibuka, data sesuai tabel
[ ] Export Excel  → sama, format .xlsx, bisa dibuka di Excel
[ ] Filter tanggal aktif + URL valid → hanya artikel dalam rentang tanggal yang muncul
[ ] Filter tanggal dengan range sempit → bisa return 0 artikel (tidak crash)
[ ] Limit 5 artikel → hanya 5 artikel yang diambil, tidak lebih
[ ] Log file      → logs/scraper.log terisi setelah scraping, ada timestamp
[ ] Error handling → kalau URL tidak bisa diakses, muncul pesan error di GUI (tidak crash)
```

---

## 🔵 FASE 4 — Test Website (Hari 3, minimal 3 website berbeda)

> Gunakan website berita Indonesia yang umum

| Website | URL Test | Status |
|---------|----------|--------|
| CNN Indonesia | https://www.cnnindonesia.com/nasional | `[ ] Lulus` |
| Detik | https://news.detik.com | `[ ] Lulus` |
| Kompas | https://www.kompas.com/tag/berita-terkini | `[ ] Lulus` |
| Tribun | https://www.tribunnews.com/nasional | `[ ] Opsional` |

Untuk setiap website, cek:
```
[ ] Minimal 3 link artikel berhasil ditemukan
[ ] Judul berhasil diambil (bukan "-" semua)
[ ] Isi berhasil diambil (bukan "-" semua)
[ ] Tidak ada crash / error fatal
[ ] is_artikel_valid() berhasil menyaring artikel yang datanya tidak lengkap
```

---

## 🚫 FASE 4B — Anti-Hardcode Check (WAJIB — nilai teknis)

> Spesifikasi dosen: *"Hindari hardcode khusus 1 website saja (usahakan general)"*

```
[ ] Cek scraper.py → tidak ada string "detik", "kompas", "cnnindonesia" di dalam kode
[ ] Cek scraper.py → selector pakai tag umum: h1, article, time, [class*='title']
[ ] Cek scraper.py → tidak ada if/else berdasarkan nama domain website
[ ] Test dengan website BARU yang belum pernah dicoba → masih bisa ambil minimal judul
[ ] _is_artikel_link() → tidak ada nama website yang di-hardcode di dalamnya
```

---

## 🏁 FASE 5 — Final Check Sebelum Submit (Hari 3 malam)

### Code & GitHub
```
[ ] Semua branch sudah di-merge ke main oleh Darva
[ ] File .gitignore ada di root repo (output/, logs/, __pycache__ tidak ter-commit)
[ ] requirements.txt sudah update dan lengkap
[ ] README.md ada cara install & cara jalankan
[ ] Setiap anggota punya minimal 4 commit di branch masing-masing
[ ] Tidak ada API key / password yang ter-commit secara tidak sengaja
[ ] Repo GitHub statusnya PUBLIC (bisa diakses tanpa login)
```

### Aplikasi
```
[ ] python main.py berjalan dari clone repo yang fresh (bukan dari folder lama)
[ ] pip install -r requirements.txt tidak error
[ ] Folder output/ dan logs/ terbuat otomatis saat startup (tidak perlu buat manual)
[ ] is_artikel_valid() berjalan dan menyaring data tidak valid
```

### Screenshot Wajib (minimal 3, simpan di docs/screenshots/)
```
[ ] SS 1 — Tampilan awal: window kosong sebelum scraping, semua komponen terlihat
[ ] SS 2 — Saat scraping: progress bar bergerak, data mulai masuk ke tabel
[ ] SS 3 — Selesai: tabel penuh dengan data artikel lengkap
[ ] SS 4 (bonus) — Hasil export CSV/Excel terbuka di Excel / Google Sheets
[ ] SS 5 (bonus) — Filter tanggal aktif dengan hasil yang sudah tersaring
```

> Tips screenshot: gunakan Snipping Tool (Win) atau Cmd+Shift+4 (Mac). Pastikan resolusi cukup jelas, tidak buram, dan seluruh window terlihat!

### Dokumen PDF Laporan (maks 3 halaman)
```
[ ] Halaman 1: Info tim + deskripsi aplikasi + daftar fitur (wajib & opsional)
[ ] Halaman 2: Arsitektur (diagram modul) + pembagian tugas tim
[ ] Halaman 3: Alur scraping step-by-step + screenshot aplikasi
[ ] PDF bisa dibuka normal (tidak corrupt)
[ ] Ukuran file tidak terlalu besar (< 5MB)
```

---

## 🐛 Kalau Ada yang Tidak Lulus

1. Catat error message-nya dengan lengkap
2. Screenshot terminal/aplikasi saat error
3. Cek dulu di `DEBUGGING_GUIDE.md`
4. Kalau tidak ketemu → tag Darva di grup dengan error + screenshot

---

*Checklist ini dikerjakan Kemal sebagai QA tester — catat hasilnya dan laporkan ke Darva!*
