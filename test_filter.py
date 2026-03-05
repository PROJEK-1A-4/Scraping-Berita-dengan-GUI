# test_filter.py ← JANGAN di-commit
import datetime
from filter import parse_tanggal, filter_by_date

# ── Test parse_tanggal() ──────────────────────────────────────
print("=== parse_tanggal() ===")
cases = [
    ("2025-03-04",   datetime.date(2025, 3, 4)),   # ISO 8601
    ("04/03/2025",   datetime.date(2025, 3, 4)),   # DD/MM/YYYY
    ("04 Mar 2025",  datetime.date(2025, 3, 4)),   # singkatan Inggris
    ("4 Maret 2025", datetime.date(2025, 3, 4)),   # Indonesia penuh
    ("-",            None),                         # field kosong
    ("tidak dikenal", None),                        # format tidak dikenal
]

for input_str, expected in cases:
    result = parse_tanggal(input_str)
    status = "✅" if result == expected else "❌"
    print(f"  {status}  parse_tanggal({input_str!r:20}) = {result}  (expected: {expected})")

# ── Test filter_by_date() ─────────────────────────────────────
print("\n=== filter_by_date() ===")
articles = [
    {"judul": "Artikel Lama",    "tanggal": "2025-01-01", "isi": "x" * 30},
    {"judul": "Artikel Dalam",   "tanggal": "2025-03-04", "isi": "x" * 30},
    {"judul": "Artikel Baru",    "tanggal": "2025-06-01", "isi": "x" * 30},
    {"judul": "Tanggal Kosong",  "tanggal": "-",          "isi": "x" * 30},
]

start = datetime.date(2025, 3, 1)
end   = datetime.date(2025, 3, 31)

hasil = filter_by_date(articles, start, end)
print(f"  Filter {start} s/d {end}:")
for a in hasil:
    print(f"    → {a['judul']} ({a['tanggal']})")

print(f"\n  Total lolos: {len(hasil)} dari {len(articles)} artikel")
print(f"  (Artikel tanggal '-' ikut config.FILTER_INCLUDE_UNKNOWN_DATE)")
