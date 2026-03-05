# exporter.py

import pandas as pd
from pathlib import Path
import config
import logger


def export_csv(data: list[dict], filename: str) -> Path:
    
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    csv_path = config.OUTPUT_DIR / f"{filename}.csv"
    
    try:
        df = pd.DataFrame(data)
        df.insert(0, "No", range(1, len(df) + 1))

        # Rename kolom dari key dict (lowercase) ke header tampilan (blueprint)
        RENAME_MAP = {
            "judul": "Judul", "tanggal": "Tanggal", "penulis": "Penulis",
            "kategori": "Kategori", "isi": "Isi", "url": "URL", "gambar_url": "Gambar_URL",
        }
        df.rename(columns=RENAME_MAP, inplace=True)
        df = df[config.CSV_HEADERS]
        
        df.to_csv(csv_path, encoding=config.CSV_ENCODING, index=False)
        
        logger.log_info(f"CSV exported successfully: {csv_path} ({len(df)} articles)")
        return csv_path
    
    except Exception as e:
        logger.log_error(f"Error exporting CSV: {str(e)}")
        raise


def export_excel(data: list[dict], filename: str) -> Path:
    
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    excel_path = config.OUTPUT_DIR / f"{filename}.xlsx"
    
    try:
        df = pd.DataFrame(data)
        df.insert(0, "No", range(1, len(df) + 1))

        # Rename kolom dari key dict (lowercase) ke header tampilan (blueprint)
        RENAME_MAP = {
            "judul": "Judul", "tanggal": "Tanggal", "penulis": "Penulis",
            "kategori": "Kategori", "isi": "Isi", "url": "URL", "gambar_url": "Gambar_URL",
        }
        df.rename(columns=RENAME_MAP, inplace=True)
        df = df[config.CSV_HEADERS]
        
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
