# worker.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Darva                                               ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Langkah Darva:
#   1. Implementasi __init__() — simpan semua parameter, buat flag _running
#   2. Implementasi run() — loop utama scraping di background thread
#      - Panggil setup_driver(), get_all_links(), scrape_article()
#      - Emit sinyal_hasil untuk setiap artikel valid
#      - Emit sinyal_progress setiap kali 1 artikel selesai
#      - Emit sinyal_selesai saat semua artikel sudah diproses
#      - Emit sinyal_error jika ada exception
#   3. Implementasi stop() — set flag berhenti scraping
#
# PENTING: Objek ScraperWorker HARUS disimpan di self.worker di MainWindow,
#          BUKAN variabel lokal — kalau variabel lokal bisa di-garbage collect!

from PyQt5.QtCore import QThread, pyqtSignal
import scraper
import filter as filter_module
import config


class ScraperWorker(QThread):
    """
    QThread yang menjalankan scraping di background.
    GUI tetap responsif selama scraping berlangsung.

    Sinyal yang tersedia:
        sinyal_progress(int)  — persentase progress 0-100
        sinyal_hasil(dict)    — 1 artikel valid siap ditambahkan ke tabel
        sinyal_selesai(int)   — scraping selesai, membawa jumlah artikel valid
        sinyal_error(str)     — pesan error jika terjadi exception
        sinyal_status(str)    — pesan status teks untuk label GUI
    """

    sinyal_progress = pyqtSignal(int)
    sinyal_hasil    = pyqtSignal(dict)
    sinyal_selesai  = pyqtSignal(int)
    sinyal_error    = pyqtSignal(str)
    sinyal_status   = pyqtSignal(str)

    def __init__(self, url: str, limit: int,
                 filter_aktif: bool = False,
                 start_date=None, end_date=None,
                 parent=None):
        """
        Args:
            url:          URL halaman daftar berita
            limit:        maksimal jumlah artikel
            filter_aktif: apakah filter tanggal diaktifkan
            start_date:   datetime.date batas awal (None jika filter off)
            end_date:     datetime.date batas akhir (None jika filter off)
        """
        super().__init__(parent)
        self.url          = url
        self.limit        = limit
        self.filter_aktif = filter_aktif
        self.start_date   = start_date
        self.end_date     = end_date
        self._running     = True

    def run(self) -> None:
        """
        Entry point QThread — dipanggil otomatis saat worker.start().

        Alur:
            1. Setup driver
            2. Emit sinyal_status("Mengumpulkan link artikel...")
            3. get_all_links() untuk kumpulkan semua URL artikel
            4. Loop per artikel:
               a. scrape_article()
               b. is_artikel_valid() → skip jika tidak valid
               c. filter_by_date() → skip jika di luar rentang (jika filter aktif)
               d. emit sinyal_hasil(artikel)
               e. emit sinyal_progress(persentase)
               f. Cek self._running — berhenti jika False
            5. emit sinyal_selesai(jumlah_valid)
            6. Tutup driver
        """
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
        """
        Minta worker berhenti (graceful stop).
        Worker akan selesai setelah artikel yang sedang diproses selesai.
        """
        self._running = False
