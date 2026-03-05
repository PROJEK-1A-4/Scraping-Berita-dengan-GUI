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
    if not tanggal_str or tanggal_str == config.FIELD_KOSONG:
        return None

    s = tanggal_str.strip()

    # Format 1: ISO 8601 — "2025-03-04"
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        pass

    # Format 2: DD/MM/YYYY — "04/03/2025"
    try:
        return datetime.datetime.strptime(s, "%d/%m/%Y").date()
    except ValueError:
        pass

    # Format 3: "04 Mar 2025" (singkatan bahasa Inggris — strptime %b)
    try:
        return datetime.datetime.strptime(s, "%d %b %Y").date()
    except ValueError:
        pass

    # Format 4: "4 Maret 2025" (nama bulan Indonesia — replace dulu)
    s_lower = s.lower()
    for nama, nomor in BULAN_INDONESIA.items():
        if nama in s_lower:
            s_lower = s_lower.replace(nama, str(nomor))
            break
    try:
        return datetime.datetime.strptime(s_lower, "%d %m %Y").date()
    except ValueError:
        pass

    # Semua format gagal
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
    hasil = []
    for artikel in articles:
        tgl = parse_tanggal(artikel["tanggal"])
        if tgl is None:
            if config.FILTER_INCLUDE_UNKNOWN_DATE:
                hasil.append(artikel)
        elif start_date <= tgl <= end_date:
            hasil.append(artikel)
    return hasil
