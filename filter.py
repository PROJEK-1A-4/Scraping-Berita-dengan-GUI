import datetime
import dateparser
import config


def parse_tanggal(tanggal_str: str) -> datetime.date | None:
    """
    Parse string tanggal dari artikel menjadi datetime.date.

    Menggunakan library dateparser yang mendukung 200+ bahasa secara otomatis,
    termasuk Bahasa Indonesia — tanpa perlu hardcode format atau nama bulan.

    Contoh format yang didukung:
        - "2025-03-04T21:00:42Z"              (ISO 8601 UTC)
        - "2026/03/05 19:07:34"               (CNN Indonesia)
        - "Kamis, 5 Maret 2026 | 20:00 WIB"  (Kompas)
        - "Kamis, 05 Mar 2026 20:00 WIB"      (Detik)
        - "03 Mar 2026 04:01pm"               (CNA)
        - "4 Maret 2025"                       (nama bulan Indonesia)
        - "2025-03-04"                         (ISO date only)
        - "04/03/2025"                         (DD/MM/YYYY)

    Args:
        tanggal_str: string tanggal apa adanya dari website

    Returns:
        datetime.date jika format dikenali, None jika tidak dikenali
    """
    if not tanggal_str or tanggal_str == config.FIELD_KOSONG:
        return None

    s = tanggal_str.strip()

    # ── Tahap 1: ISO 8601 (YYYY-...) → strptime (unambiguous, tidak terpengaruh DATE_ORDER) ──
    import re
    s_iso = re.sub(
        r'T(\d{2})-(\d{2})-(\d{2})(\.\d+)?(Z|[+\-]\d{2}:\d{2})?',
        r'T\1:\2:\3\4\5',
        s
    )
    iso_formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in iso_formats:
        try:
            return datetime.datetime.strptime(s_iso, fmt).date()
        except ValueError:
            pass

    # ── Tahap 2: Format bebas (Indonesia/Inggris) → dateparser ───────────────
    result = dateparser.parse(
        s,
        languages=["id", "en"],
        settings={
            "DATE_ORDER":           "DMY",   # DD/MM/YYYY — urutan tanggal Indonesia
            "RETURN_AS_TIMEZONE_AWARE": False,
            "PREFER_DAY_OF_MONTH":  "first",
        },
    )
    return result.date() if result else None


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
