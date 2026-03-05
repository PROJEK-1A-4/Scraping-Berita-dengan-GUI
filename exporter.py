# exporter.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Kemal                                               ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Langkah Kemal:
#   1. Implementasi export_csv() — simpan data ke .csv pakai pandas
#      encoding utf-8-sig agar Excel bisa baca karakter Indonesia
#   2. Implementasi export_excel() — simpan ke .xlsx, tambahkan
#      auto-width kolom supaya tampilannya rapi di Excel
#   3. Kolom yang ditulis: sesuai config.CSV_HEADERS (urutan WAJIB sama)
#   4. Tambahkan kolom "No" (nomor urut mulai dari 1)

import pandas as pd
from pathlib import Path
import config
import logger


def export_csv(data: list[dict], filename: str) -> Path:
    """
    Ekspor daftar artikel ke file CSV.

    Args:
        data:     list of dict artikel (format sesuai kesepakatan tim)
        filename: nama file output tanpa ekstensi, misal "hasil_scraping"

    Returns:
        Path: path lengkap file yang disimpan

    Spesifikasi:
        - Simpan ke config.OUTPUT_DIR / f"{filename}.csv"
        - Encoding: utf-8-sig (agar Excel tidak garbled)
        - Kolom mengikuti urutan config.CSV_HEADERS
        - Kolom "No" = nomor urut mulai 1
    """
    # TODO Kemal: implementasikan ekspor CSV di sini
    # Hint:
    #   1. Buat DataFrame dari data, tambahkan kolom No
    #   2. Reorder kolom sesuai config.CSV_HEADERS
    #   3. df.to_csv(path, encoding="utf-8-sig", index=False)
    #   4. Panggil logger.log_info() setelah berhasil
    #   5. return path file
    raise NotImplementedError("TODO Kemal: implementasi export_csv()")


def export_excel(data: list[dict], filename: str) -> Path:
    """
    Ekspor daftar artikel ke file Excel (.xlsx).

    Args:
        data:     list of dict artikel (format sesuai kesepakatan tim)
        filename: nama file output tanpa ekstensi, misal "hasil_scraping"

    Returns:
        Path: path lengkap file yang disimpan

    Spesifikasi:
        - Simpan ke config.OUTPUT_DIR / f"{filename}.xlsx"
        - Kolom mengikuti urutan config.CSV_HEADERS
        - Kolom "No" = nomor urut mulai 1
        - Auto-width kolom: sesuaikan lebar kolom dengan konten terpanjang
    """
    # TODO Kemal: implementasikan ekspor Excel di sini
    # Hint:
    #   1. Buat DataFrame dari data, tambahkan kolom No
    #   2. Pakai pd.ExcelWriter dengan engine openpyxl untuk auto-width:
    #      with pd.ExcelWriter(path, engine="openpyxl") as writer:
    #          df.to_excel(writer, index=False)
    #          worksheet = writer.sheets["Sheet1"]
    #          for col in worksheet.columns:
    #              lebar = max(len(str(cell.value)) for cell in col)
    #              worksheet.column_dimensions[col[0].column_letter].width = lebar + 2
    #   3. Panggil logger.log_info() setelah berhasil
    #   4. return path file
    raise NotImplementedError("TODO Kemal: implementasi export_excel()")
