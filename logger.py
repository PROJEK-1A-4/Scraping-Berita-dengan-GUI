# logger.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Kemal                                               ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Langkah Kemal:
#   1. Implementasi setup_logger() — buat logger dengan FileHandler ke LOG_FILE
#      dan StreamHandler ke terminal, lengkap dengan format timestamp
#   2. Implementasi log_info / log_error / log_warning sebagai wrapper
#   3. Pastikan folder logs/ sudah ada sebelum setup_logger() dipanggil
#      (sudah dihandle main.py, tapi tambahkan guard juga di sini)

import logging
import sys
from pathlib import Path
import config

# Module-level logger — di-inisialisasi oleh setup_logger()
_logger = None


def setup_logger() -> logging.Logger:
    """
    Inisialisasi logger aplikasi.

    - Output ke file: config.LOG_FILE (dengan timestamp)
    - Output ke terminal: untuk monitoring real-time saat development
    - Format log: [YYYY-MM-DD HH:MM:SS] LEVEL: pesan

    Returns:
        logging.Logger: logger yang sudah dikonfigurasi
    """
    global _logger
    
    # Pastikan folder logs/ sudah ada
    config.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Buat logger dengan nama "news_scraper"
    _logger = logging.getLogger("news_scraper")
    _logger.setLevel(logging.DEBUG)
    
    # Hapus handler lama jika ada (cegah duplikasi)
    if _logger.handlers:
        _logger.handlers.clear()
    
    # Buat formatter dari config.LOG_FORMAT
    formatter = logging.Formatter(config.LOG_FORMAT)
    
    # FileHandler — simpan ke file LOG_FILE
    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)
    
    # StreamHandler — output ke terminal (stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)
    
    return _logger


def log_info(message: str) -> None:
    """Catat pesan informasi ke log."""
    global _logger
    if _logger is None:
        setup_logger()
    _logger.info(message)


def log_error(message: str) -> None:
    """Catat pesan error ke log."""
    global _logger
    if _logger is None:
        setup_logger()
    _logger.error(message)


def log_warning(message: str) -> None:
    """Catat pesan peringatan ke log."""
    global _logger
    if _logger is None:
        setup_logger()
    _logger.warning(message)
