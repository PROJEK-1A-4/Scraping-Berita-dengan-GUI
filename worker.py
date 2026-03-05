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
        # TODO Darva: simpan semua parameter sebagai atribut self
        # Buat juga self._running = True sebagai flag berhenti
        pass

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
        # TODO Darva: implementasikan alur scraping di sini
        # Pastikan ada try-except di level atas:
        #   except Exception as e:
        #       self.sinyal_error.emit(str(e))
        pass

    def stop(self) -> None:
        """
        Minta worker berhenti (graceful stop).
        Worker akan selesai setelah artikel yang sedang diproses selesai.
        """
        # TODO Darva: set self._running = False
        pass
