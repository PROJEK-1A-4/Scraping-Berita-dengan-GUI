# exporter.py

import pandas as pd
from pathlib import Path
import config
import logger


def export_csv(data: list[dict], filename: str) -> Path:
    
    # Pastikan folder OUTPUT_DIR sudah ada
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Buat path lengkap file CSV
    csv_path = config.OUTPUT_DIR / f"{filename}.csv"
    
    try:
        # Buat DataFrame dari data
        df = pd.DataFrame(data)
        
        # Tambah kolom "No" (nomor urut mulai dari 1)
        df.insert(0, "No", range(1, len(df) + 1))
        
        # Reorder kolom sesuai config.CSV_HEADERS
        df = df[config.CSV_HEADERS]
        
        # Simpan ke CSV dengan encoding utf-8-sig
        df.to_csv(csv_path, encoding=config.CSV_ENCODING, index=False)
        
        # Log berhasil
        logger.log_info(f"CSV exported successfully: {csv_path} ({len(df)} articles)")
        
        return csv_path
    
    except Exception as e:
        logger.log_error(f"Error exporting CSV: {str(e)}")
        raise


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
    # Pastikan folder OUTPUT_DIR sudah ada
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Buat path lengkap file Excel
    excel_path = config.OUTPUT_DIR / f"{filename}.xlsx"
    
    try:
        # Buat DataFrame dari data
        df = pd.DataFrame(data)
        
        # Tambah kolom "No" (nomor urut mulai dari 1)
        df.insert(0, "No", range(1, len(df) + 1))
        
        # Reorder kolom sesuai config.CSV_HEADERS
        df = df[config.CSV_HEADERS]
        
        # Simpan ke Excel dengan auto-width kolom menggunakan openpyxl
        with pd.ExcelWriter(excel_path, engine=config.EXCEL_ENGINE) as writer:
            df.to_excel(writer, index=False)
            
            # Auto-width: hitung lebar kolom berdasarkan konten terpanjang
            worksheet = writer.sheets["Sheet1"]
            for col in worksheet.columns:
                # Hitung panjang maksimal di setiap kolom
                max_length = max(len(str(cell.value)) for cell in col)
                # Set column width + padding 2 untuk spacing
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max_length + 2
        
        # Log berhasil
        logger.log_info(f"Excel exported successfully: {excel_path} ({len(df)} articles)")
        
        return excel_path
    
    except Exception as e:
        logger.log_error(f"Error exporting Excel: {str(e)}")
        raise
