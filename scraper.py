# scraper.py
# ╔══════════════════════════════════════════════════════════════╗
# ║  TUGAS: Darva                                               ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Langkah Darva:
#   1. Implementasi setup_driver() — headless Chrome + anti-bot headers
#      WAJIB tambahkan flag Linux: --no-sandbox dan --disable-dev-shm-usage
#   2. Implementasi _extract_text() — helper coba selector satu per satu
#   3. Implementasi get_all_links() — kumpulkan link artikel dari halaman
#   4. Implementasi handle_pagination() — ikuti halaman berikutnya
#      (4 strategi dari blueprint, jangan hardcode class/id per website!)
#   5. Implementasi scrape_article() — ekstrak semua field dari 1 artikel
#   is_artikel_valid() sudah diisi sesuai kesepakatan tim, JANGAN diubah logikanya

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

import config
import logger


# ─── Kesepakatan tim: struktur data artikel ───────────────────
# Semua value adalah STRING. Field tidak ada → "-" (bukan None atau "")
ARTIKEL_KOSONG = {
    "judul"     : config.FIELD_KOSONG,
    "tanggal"   : config.FIELD_KOSONG,
    "isi"       : config.FIELD_KOSONG,
    "url"       : config.FIELD_KOSONG,
    "penulis"   : config.FIELD_KOSONG,
    "kategori"  : config.FIELD_KOSONG,
    "gambar_url": config.FIELD_KOSONG,
}


def setup_driver() -> webdriver.Chrome:
    """
    Buat dan kembalikan Selenium WebDriver (headless Chrome).

    Konfigurasi yang WAJIB ada:
        - Headless mode (dari config.HEADLESS)
        - User-Agent header (dari config.USER_AGENT)
        - --no-sandbox         (wajib di Linux)
        - --disable-dev-shm-usage  (cegah crash di Linux)
        - Page load timeout (dari config.PAGE_LOAD_WAIT)

    Returns:
        webdriver.Chrome: driver yang siap dipakai
    """
    options = Options()

    if config.HEADLESS:
        options.add_argument("--headless")

    options.add_argument(f"user-agent={config.USER_AGENT}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(config.PAGE_LOAD_WAIT)

    return driver


def _extract_text(driver: webdriver.Chrome, selectors: list[tuple], default: str = "-") -> str:
    """
    Helper: coba beberapa selector CSS/XPath secara berurutan, kembalikan teks pertama yang ketemu.

    Args:
        driver:    WebDriver aktif
        selectors: list of (By.xxx, "selector_string"), dicoba dari indeks 0
        default:   nilai kembalian jika semua selector gagal

    Returns:
        str: teks elemen pertama yang ditemukan, atau default jika tidak ada
    """
    from selenium.common.exceptions import NoSuchElementException

    for by, value in selectors:
        try:
            element = driver.find_element(by, value)
            return element.text.strip()
        except NoSuchElementException:
            continue

    return default


def get_all_links(driver: webdriver.Chrome, url: str, limit: int) -> list[str]:
    """
    Kumpulkan semua link artikel dari URL (termasuk pagination) sampai limit tercapai.

    Args:
        driver: WebDriver aktif
        url:    URL halaman daftar berita
        limit:  maksimal jumlah link yang dikumpulkan

    Returns:
        list[str]: daftar URL artikel (full URL, bukan relative)
    """
    # TODO Darva: implementasikan pengumpulan link
    # Hint:
    #   - Buka url dengan driver.get(url)
    #   - Cari semua <a> yang mengarah ke artikel (gunakan selector generik)
    #   - Panggil handle_pagination() untuk lanjut ke halaman berikutnya
    #   - Hentikan jika len(links) >= limit atau tidak ada halaman berikutnya
    return []


def handle_pagination(driver: webdriver.Chrome) -> bool:
    """
    Deteksi dan klik tombol "halaman berikutnya" jika ada.

    Strategi (urutan prioritas — JANGAN hardcode class/id per website!):
        1. Cari <a rel="next"> atau <link rel="next">
        2. Cari teks tombol: "Next", "Selanjutnya", "›", "»", "Berikutnya"
        3. Cari pola URL: ?page=N, ?p=N, /page/N, /halaman/N
        4. Tidak ketemu → return False (sudah halaman terakhir)

    Returns:
        bool: True jika berhasil pindah ke halaman berikutnya, False jika tidak ada
    """
    # TODO Darva: implementasikan deteksi & klik pagination
    return False


def scrape_article(driver: webdriver.Chrome, url: str) -> dict:
    """
    Ekstrak semua field dari 1 halaman artikel.

    Args:
        driver: WebDriver aktif
        url:    URL artikel yang akan di-scrape

    Returns:
        dict: artikel dengan semua field (format ARTIKEL_KOSONG sebagai template)
              Field tidak ditemukan → config.FIELD_KOSONG ("-"), JANGAN crash

    Wajib:
        - judul, tanggal, isi (field wajib)
        - url, penulis, kategori, gambar_url (field bonus, boleh "-")
        - isi dipotong maksimal config.MAX_ISI_CHARS karakter
        - Gunakan try-except untuk setiap field bonus
        - Delay config.DEFAULT_DELAY detik setelah scraping
    """
    artikel = ARTIKEL_KOSONG.copy()
    artikel["url"] = url

    driver.get(url)

    artikel["judul"] = _extract_text(driver, [
        (By.TAG_NAME, "h1"),
        (By.CSS_SELECTOR, "article h1"),
    ])

    artikel["tanggal"] = _extract_text(driver, [
        (By.CSS_SELECTOR, ".read__time"),
        (By.CSS_SELECTOR, ".detail__date"),
        (By.TAG_NAME, "time"),
        (By.CSS_SELECTOR, ".date"),
    ])

    isi = _extract_text(driver, [
        (By.CSS_SELECTOR, ".read__content"),
        (By.CSS_SELECTOR, ".detail__body-text"),
        (By.CSS_SELECTOR, "article"),
        (By.CSS_SELECTOR, ".content"),
    ])
    artikel["isi"] = isi[:config.MAX_ISI_CHARS]

    # ── Field bonus ───────────────────────────────────────────
    artikel["penulis"] = _extract_text(driver, [
        (By.CSS_SELECTOR, ".read__author"),
        (By.CSS_SELECTOR, ".detail__author"),
        (By.CSS_SELECTOR, ".author"),
    ])

    artikel["kategori"] = _extract_text(driver, [
        (By.CSS_SELECTOR, ".breadcrumb__item"),
        (By.CSS_SELECTOR, ".detail__nav > a"),
        (By.CSS_SELECTOR, ".category"),
    ])

    from selenium.common.exceptions import NoSuchElementException
    for by, value in [
        (By.CSS_SELECTOR, ".photo__wrap img"),
        (By.CSS_SELECTOR, ".detail__media img"),
        (By.TAG_NAME, "img"),
    ]:
        try:
            img_element = driver.find_element(by, value)
            artikel["gambar_url"] = img_element.get_attribute("src")
            break
        except NoSuchElementException:
            continue

    time.sleep(config.DEFAULT_DELAY)
    return artikel


def is_artikel_valid(artikel: dict) -> bool:
    """
    Validasi artikel: pastikan field wajib tidak kosong dan cukup panjang.

    Threshold diambil dari config.py supaya bisa diubah tanpa edit kode ini.
    Hanya field WAJIB yang dicek (judul + isi). Field bonus boleh "-".

    Args:
        artikel: dict artikel hasil scrape_article()

    Returns:
        bool: True jika artikel valid, False jika harus di-skip
    """
    # Fungsi ini SUDAH FINAL sesuai kesepakatan tim — jangan ubah logikanya!
    return (
        artikel["judul"] not in (config.FIELD_KOSONG, "") and
        len(artikel["judul"]) >= config.MIN_JUDUL_CHARS and
        artikel["isi"] not in (config.FIELD_KOSONG, "") and
        len(artikel["isi"]) >= config.MIN_ISI_CHARS
    )