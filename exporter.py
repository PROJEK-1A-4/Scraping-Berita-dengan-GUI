# exporter.py

import pandas as pd
from pathlib import Path
import config
import logger


def export_csv(data: list[dict], filename: str) -> Path:
    
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    csv_path = config.OUTPUT_DIR / f"{filename}.csv"
    
    try:
        # Buat DataFrame
        df = pd.DataFrame(data)
        
        # Tambah kolom "No"
        df.insert(0, "No", range(1, len(df) + 1))
        
        # No kolom sesuai config.CSV_HEADERS
        df = df[config.CSV_HEADERS]
        
        # Simpan ke file CSV dengan encoding utf-8-sig
        df.to_csv(csv_path, encoding=config.CSV_ENCODING, index=False)
        
        logger.log_info(f"CSV exported successfully: {csv_path} ({len(df)} articles)")
        
        return csv_path
    
    except Exception as e:
        logger.log_error(f"Error exporting CSV: {str(e)}")
        raise


def export_excel(data: list[dict], filename: str) -> Path:
    
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Buat path lengkap file Excel
    excel_path = config.OUTPUT_DIR / f"{filename}.xlsx"
    
    try:
        df = pd.DataFrame(data)
        
        # Tambah kolom "No"
        df.insert(0, "No", range(1, len(df) + 1))
        
        # No kolom sesuai config.CSV_HEADERS
        df = df[config.CSV_HEADERS]
        
        # Menyimpan ke Excel dengan auto-width kolom menggunakan openpyxl
        with pd.ExcelWriter(excel_path, engine=config.EXCEL_ENGINE) as writer:
            df.to_excel(writer, index=False)
            
            worksheet = writer.sheets["Sheet1"]
            for col in worksheet.columns:
                max_length = max(len(str(cell.value)) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max_length + 2
        
        logger.log_info(f"Excel exported successfully: {excel_path} ({len(df)} articles)")
        
        return excel_path
    
    except Exception as e:
        logger.log_error(f"Error exporting Excel: {str(e)}")
        raise
