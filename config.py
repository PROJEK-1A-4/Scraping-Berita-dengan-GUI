# config.py
from pathlib import Path 

# === Selenium ===
HEADLESS       = True
USER_AGENT     = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
PAGE_LOAD_WAIT = 10       # timeout tunggu halaman load

# ─── Scraping ─────────────────────────────────────────────────
DEFAULT_DELAY  = 1.5      # jeda antar request
DEFAULT_LIMIT  = 20       # jumlah artikel default
MAX_ISI_CHARS  = 2000     # Jumlah isi karakter (cukup untuk 3-5 paragraf berita) 
FIELD_KOSONG   = "-"      # nilai default untuk field yang tidak ditemukan

# ─── Validasi artikel — dipakai is_artikel_valid() di scraper.py ──
MIN_JUDUL_CHARS = 15       # Minimal karakter judul
MIN_ISI_CHARS   = 100      # Minimal karakter isi

# ─── Link filtering — dipakai get_all_links() di scraper.py ───
PATH_DEPTH_MIN  = 3        # Minimal kedalaman path URL (filter halaman kategori)
NON_ARTIKEL_KEYWORDS = (
    "search", "query=", "/tag/", "/kirim", "/login",
    "/register", "/subscribe", "#", "javascript:",
    "/topik", "/topic", "/author/", "/penulis/",
    "/jadwal-", "/quran", "/ramadan", "/live",
    "gampad", "doubleclick", "?source=", "?ref=",
    "/video/", "/foto/", "/galeri/", "/photo/",
    "/podcast/", "/infografis/",
)

# ─── Filter tanggal ───────────────────────────────────────────
FILTER_INCLUDE_UNKNOWN_DATE = True

# ─── Path output  ───
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"

# ─── GUI ──────────────────────────────────────────────────────
APP_TITLE     = "News Scraper App"
WINDOW_W      = 1200
WINDOW_H      = 700
DIALOG_W      = 460        # Lebar default untuk dialog (Tentang, Tim, dll)
DIALOG_H      = 320        # Tinggi default untuk dialog
DETAIL_DLG_W  = 760        # Lebar dialog detail artikel
DETAIL_DLG_H  = 620        # Tinggi dialog detail artikel
# ─── Encoding dan format ──────────────────────────────────
CSV_ENCODING = "utf-8-sig"  # encoding untuk file CSV
EXCEL_ENGINE = "openpyxl"   # engine untuk export Excel (.xlsx)

# ─── Logging ──────────────────────────────────────────────────
LOG_FORMAT   = "%(asctime)s - %(levelname)s - %(message)s"  # format log
LOG_LEVEL    = "DEBUG"      # level log: DEBUG, INFO, WARNING, ERROR

# ─── Header CSV/Excel (urutan WAJIB sama) ─────────────────────
# CATATAN: CSV_HEADERS berbeda dengan KOLOM_TABEL di gui.py
#   - CSV_HEADERS: untuk export file, termasuk kolom Gambar_URL
#   - KOLOM_TABEL (gui.py): untuk tampilan tabel GUI, tanpa Gambar (gambar di dialog detail)
CSV_HEADERS = ["No", "Judul", "Tanggal", "Penulis", "Kategori", "Isi", "URL", "Gambar_URL"]
