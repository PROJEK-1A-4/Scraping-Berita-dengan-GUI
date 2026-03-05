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
    # TODO Kemal: implementasikan logger di sini
    # Hint:
    #   logger = logging.getLogger("news_scraper")
    #   logger.setLevel(logging.DEBUG)
    #   formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    #   Buat FileHandler ke config.LOG_FILE dan StreamHandler ke sys.stdout
    #   Tambahkan kedua handler ke logger
    #   Simpan ke global _logger
    raise NotImplementedError("TODO Kemal: implementasi setup_logger()")


def log_info(message: str) -> None:
    """Catat pesan informasi ke log."""
    # TODO Kemal: panggil _logger.info(message)
    # Pastikan _logger sudah diinisialisasi, kalau belum panggil setup_logger()
    pass


def log_error(message: str) -> None:
    """Catat pesan error ke log."""
    # TODO Kemal: panggil _logger.error(message)
    pass


def log_warning(message: str) -> None:
    """Catat pesan peringatan ke log."""
    # TODO Kemal: panggil _logger.warning(message)
    pass
