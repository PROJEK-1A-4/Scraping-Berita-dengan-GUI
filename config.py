# config.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Kemal                                               ║
# ║  PRIORITAS: SELESAIKAN HARI 1 — semua file lain import di sini! ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Langkah Kemal:
#   1. Verifikasi semua nilai konstanta di bawah — sesuaikan jika perlu
#   2. Pastikan OUTPUT_DIR dan LOG_FILE pakai pathlib.Path (sudah ada)
#   3. Tambahkan konstanta lain jika kamu butuhkan di exporter.py / logger.py
#   4. Jangan hapus konstanta yang sudah ada — file lain sudah import dari sini

from pathlib import Path   # WAJIB — kompatibel Windows/Mac/Linux

# ─── Selenium ─────────────────────────────────────────────────
HEADLESS       = True
USER_AGENT     = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
PAGE_LOAD_WAIT = 10       # detik — timeout tunggu halaman load

# ─── Scraping ─────────────────────────────────────────────────
DEFAULT_DELAY  = 1.5      # detik — jeda antar request (jangan dihapus!)
DEFAULT_LIMIT  = 20       # jumlah artikel default
MAX_ISI_CHARS  = 500      # isi artikel dipotong di karakter ke-N
FIELD_KOSONG   = "-"      # nilai default untuk field yang tidak ditemukan

# ─── Validasi artikel — dipakai is_artikel_valid() di scraper.py ──
# TODO Kemal: pastikan nilai ini masuk akal sebelum commit
MIN_JUDUL_CHARS = 5       # judul minimal N karakter agar dianggap valid
MIN_ISI_CHARS   = 20      # isi minimal N karakter agar dianggap valid

# ─── Filter tanggal ───────────────────────────────────────────
# True  = artikel tanggal tidak dikenali TETAP tampil saat filter aktif
# False = artikel tanggal tidak dikenali DIBUANG saat filter aktif
FILTER_INCLUDE_UNKNOWN_DATE = True

# ─── Path output — pathlib otomatis handle \ vs / antar OS ───
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"

# ─── GUI ──────────────────────────────────────────────────────
APP_TITLE  = "News Scraper App"
WINDOW_W   = 1200
WINDOW_H   = 700

# ─── Header CSV/Excel (urutan WAJIB sama) ─────────────────────
CSV_HEADERS = ["No", "Judul", "Tanggal", "Penulis", "Kategori", "Isi", "URL", "Gambar_URL"]
