# config.py
from pathlib import Path 

# ─── Selenium ─────────────────────────────────────────────────
HEADLESS       = True
USER_AGENT     = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
PAGE_LOAD_WAIT = 10       # timeout tunggu halaman load

# ─── Scraping ─────────────────────────────────────────────────
DEFAULT_DELAY  = 1.5      # jeda antar request
DEFAULT_LIMIT  = 20       # jumlah artikel default
MAX_ISI_CHARS  = 500      # Jumlah isi karakter 
FIELD_KOSONG   = "-"      # nilai default untuk field yang tidak ditemukan

# ─── Validasi artikel — dipakai is_artikel_valid() di scraper.py ──
MIN_JUDUL_CHARS = 15       # Minimal karakter judul
MIN_ISI_CHARS   = 100      # Minimal karakter isi

# ─── Filter tanggal ───────────────────────────────────────────
FILTER_INCLUDE_UNKNOWN_DATE = True

# ─── Path output  ───
OUTPUT_DIR = Path("output")
LOG_FILE   = Path("logs") / "scraper.log"

# ─── GUI ──────────────────────────────────────────────────────
APP_TITLE  = "News Scraper App"
WINDOW_W   = 1200
WINDOW_H   = 700
# ─── Encoding dan format ──────────────────────────────────
CSV_ENCODING = "utf-8-sig"  # encoding untuk file CSV
EXCEL_ENGINE = "openpyxl"   # engine untuk export Excel (.xlsx)

# ─── Logging ──────────────────────────────────────────────────
LOG_FORMAT   = "%(asctime)s - %(levelname)s - %(message)s"  # format log
LOG_LEVEL    = "DEBUG"      # level log: DEBUG, INFO, WARNING, ERROR

# ─── Header CSV/Excel ─────────────────────
CSV_HEADERS = ["No", "judul", "tanggal", "penulis", "kategori", "isi", "url", "gambar_url"]
