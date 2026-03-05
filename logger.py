# logger.py
import logging
import sys
from pathlib import Path
import config

# Module-level logger
_logger = None


def setup_logger() -> logging.Logger:
    global _logger
    
    config.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    _logger = logging.getLogger("news_scraper")
    _logger.setLevel(logging.DEBUG)
    
    # Hapus handler lama
    if _logger.handlers:
        _logger.handlers.clear()
    
    # Buat formatter dari config.LOG_FORMAT
    formatter = logging.Formatter(config.LOG_FORMAT)
    
    # FileHandler
    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)
    
    # StreamHandler
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
