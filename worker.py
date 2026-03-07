from PyQt5.QtCore import QThread, pyqtSignal
import scraper
import filter as filter_module
import config


class ScraperWorker(QThread):
    sinyal_progress = pyqtSignal(int)
    sinyal_hasil    = pyqtSignal(dict)
    sinyal_selesai  = pyqtSignal(int)
    sinyal_error    = pyqtSignal(str)
    sinyal_status   = pyqtSignal(str)

    def __init__(self, url: str, limit: int,
                 filter_aktif: bool = False,
                 start_date=None, end_date=None,
                 parent=None):
        super().__init__(parent)
        self.url          = url
        self.limit        = limit
        self.filter_aktif = filter_aktif
        self.start_date   = start_date
        self.end_date     = end_date
        self._running     = True

    def run(self) -> None:
        driver = None
        try:
            # 1. Setup driver
            self.sinyal_status.emit("Menyiapkan browser...")
            driver = scraper.setup_driver()

            # 2. Kumpulkan semua link artikel
            self.sinyal_status.emit("Mengumpulkan link artikel...")
            links = scraper.get_all_links(driver, self.url, self.limit)

            if not links:
                self.sinyal_error.emit("Tidak ada link artikel yang ditemukan.")
                self.sinyal_selesai.emit(0)
                return

            total = len(links)
            jumlah_valid = 0

            # 3. Loop per artikel
            for i, link in enumerate(links):
                if not self._running:
                    break

                self.sinyal_status.emit(f"Scraping artikel {i + 1}/{total}...")
                artikel = scraper.scrape_article(driver, link)

                # Skip artikel tidak valid
                if not scraper.is_artikel_valid(artikel):
                    self.sinyal_progress.emit(int((i + 1) / total * 100))
                    continue

                # Filter tanggal jika aktif
                if self.filter_aktif and self.start_date and self.end_date:
                    hasil = filter_module.filter_by_date(
                        [artikel], self.start_date, self.end_date
                    )
                    if not hasil:
                        self.sinyal_progress.emit(int((i + 1) / total * 100))
                        continue

                jumlah_valid += 1
                self.sinyal_hasil.emit(artikel)
                self.sinyal_progress.emit(int((i + 1) / total * 100))

            # 4. Selesai
            self.sinyal_status.emit(f"Selesai. {jumlah_valid} artikel valid ditemukan.")
            self.sinyal_selesai.emit(jumlah_valid)

        except Exception as e:
            self.sinyal_error.emit(str(e))
        finally:
            if driver:
                driver.quit()

    def stop(self) -> None:
        self._running = False
