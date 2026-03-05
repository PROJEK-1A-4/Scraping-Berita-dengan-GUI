# filter.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Darva                                               ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Langkah Darva:
#   1. Implementasi parse_tanggal() — support format tanggal Indonesia:
#      "04 Mar 2025", "4 Maret 2025", "2025-03-04", "04/03/2025"
#      Kembalikan datetime.date jika berhasil, None jika tidak dikenali
#   2. Implementasi filter_by_date() — filter list artikel berdasarkan rentang
#      Artikel tanggal tidak dikenali → ikuti config.FILTER_INCLUDE_UNKNOWN_DATE

import datetime
import config


# Mapping nama bulan Indonesia ke nomor bulan
BULAN_INDONESIA = {
    "januari": 1, "februari": 2, "maret": 3, "april": 4,
    "mei": 5, "juni": 6, "juli": 7, "agustus": 8,
    "september": 9, "oktober": 10, "november": 11, "desember": 12,
    # Singkatan (dari format "04 Mar 2025")
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "agu": 8, "ags": 8,  # "mei" sudah ada di atas
    "sep": 9, "okt": 10, "nov": 11, "des": 12,
}


def parse_tanggal(tanggal_str: str) -> datetime.date | None:
    """
    Parse string tanggal dari artikel menjadi datetime.date.

    Format yang harus didukung:
        - "04 Mar 2025"   (singkatan Inggris — dari strptime %b)
        - "4 Maret 2025"  (Indonesia penuh — pakai BULAN_INDONESIA)
        - "2025-03-04"    (ISO 8601)
        - "04/03/2025"    (DD/MM/YYYY)

    Args:
        tanggal_str: string tanggal apa adanya dari website

    Returns:
        datetime.date jika format dikenali, None jika tidak dikenali
    """
    # TODO Darva: implementasikan parsing multi-format
    # Hint:
    #   - Coba datetime.strptime() untuk format standar
    #   - Untuk format Indonesia, lowercase dan replace nama bulan
    #     dengan nomornya, lalu parse ulang
    #   - Bungkus setiap percobaan dengan try-except ValueError
    #   - Return None hanya jika semua format gagal
    return None


def filter_by_date(articles: list[dict],
                   start_date: datetime.date,
                   end_date: datetime.date) -> list[dict]:
    """
    Filter list artikel agar hanya yang ada dalam rentang tanggal yang lolos.

    Args:
        articles:   list of dict artikel hasil scraping
        start_date: batas awal (inklusif)
        end_date:   batas akhir (inklusif)

    Returns:
        list[dict]: artikel yang lolos filter

    Aturan:
        - Artikel dalam range → masuk hasil
        - Artikel di luar range → dibuang
        - Artikel tanggal tidak dikenali (parse_tanggal() → None):
            config.FILTER_INCLUDE_UNKNOWN_DATE == True  → masuk hasil
            config.FILTER_INCLUDE_UNKNOWN_DATE == False → dibuang
    """
    # TODO Darva: implementasikan filter
    # Hint:
    #   hasil = []
    #   for artikel in articles:
    #       tgl = parse_tanggal(artikel["tanggal"])
    #       if tgl is None:
    #           if config.FILTER_INCLUDE_UNKNOWN_DATE:
    #               hasil.append(artikel)
    #       elif start_date <= tgl <= end_date:
    #           hasil.append(artikel)
    #   return hasil
    return articles
