import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

import config
import style
import logger


def buat_folder_wajib() -> None:
    """
    Pastikan folder output/ dan logs/ ada sebelum app jalan.
    Dibuat otomatis di sini — user tidak perlu buat manual.
    """
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    (Path("logs")).mkdir(exist_ok=True)


def main() -> None:
    """Entry point aplikasi News Scraper."""

    # Buat folder yang dibutuhkan
    buat_folder_wajib()

    # Setup logger (guard sementara sampai Kemal implementasi logger)
    try:
        logger.setup_logger()
    except NotImplementedError:
        pass  # logger belum diimplementasi — skip dulu

    # Inisialisasi Qt application
    app = QApplication(sys.argv)

    # Terapkan stylesheet sebelum window dibuat
    style.apply_style(app)

    # Buat dan tampilkan MainWindow
    from gui import MainWindow
    window = MainWindow()
    window.show()

    # Jalankan event loop dan exit bersih
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
