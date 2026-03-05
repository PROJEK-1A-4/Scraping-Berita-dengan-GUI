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
# from selenium.webdriver.support.ui import WebDriverWait      # reserved — untuk explicit wait jika dibutuhkan
# from selenium.webdriver.support import expected_conditions as EC  # reserved — pasangan WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

import config
# import logger  # reserved — aktifkan setelah logger.py (Kemal) selesai


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
    options.page_load_strategy = "eager"  # berhenti tunggu saat DOM siap, abaikan resource lambat

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
            text = element.text.strip()
            if text:
                return text
        except NoSuchElementException:
            continue

    return default


def _extract_meta(driver: webdriver.Chrome, names: list[str], default: str = "-") -> str:
    """
    Helper: baca atribut 'content' dari <meta> tag secara berurutan.
    Mendukung OpenGraph (property=), Standard meta (name=), dan Schema.org (itemprop=).

    Ini adalah cara paling GENERAL karena merupakan standar internasional:
      - OpenGraph: dipakai semua website untuk share ke sosmed
      - Schema.org: standar Google untuk SEO / rich snippets
      - Keduanya ada di SEMUA website berita modern, tanpa kecuali.

    Contoh:
        _extract_meta(driver, ["og:title", "twitter:title"])
        → mencari <meta property='og:title'> lalu <meta name='twitter:title'>

    Args:
        driver: WebDriver aktif
        names:  list nama property/name/itemprop meta tag, dicoba dari indeks 0
        default: nilai kembalian jika semua gagal

    Returns:
        str: nilai content meta tag pertama yang ditemukan, atau default
    """
    from selenium.common.exceptions import NoSuchElementException

    for name in names:
        # 1. Coba property="..." — OpenGraph (og:title, og:description, article:published_time)
        for attr in ("property", "name"):
            try:
                el = driver.find_element(
                    By.CSS_SELECTOR, f'meta[{attr}="{name}"]'
                )
                content = el.get_attribute("content")
                if content and content.strip():
                    return content.strip()
            except NoSuchElementException:
                continue

        # 2. Coba itemprop="..." — Schema.org (bisa di elemen apa pun, bukan cuma <meta>)
        try:
            el = driver.find_element(By.CSS_SELECTOR, f'[itemprop="{name}"]')
            # Coba atribut content dulu (utk <meta>), lalu datetime (<time>), lalu text
            for attr in ("content", "datetime"):
                val = el.get_attribute(attr)
                if val and val.strip():
                    return val.strip()
            text = el.text.strip()
            if text:
                return text
        except NoSuchElementException:
            pass

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
    from urllib.parse import urlparse, urljoin
    from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

    links: list[str] = []
    seen: set[str] = set()
    parsed_input  = urlparse(url)
    base          = f"{parsed_input.scheme}://{parsed_input.netloc}"

    # Base domain untuk filter same-domain: ambil 2 segmen terakhir
    # Contoh: "nasional.kompas.com" → "kompas.com"
    #          "www.cnnindonesia.com" → "cnnindonesia.com"
    netloc_parts = parsed_input.netloc.split(".")
    base_domain  = ".".join(netloc_parts[-2:])  # e.g. "kompas.com"

    # Keyword yang menandakan URL bukan artikel (path/query pattern)
    NON_ARTIKEL_KW = (
        "search", "query=", "/tag/", "/kirim", "/login",
        "/register", "/subscribe", "#", "javascript:",
        "/topik", "/topic", "/author/", "/penulis/",
        "/jadwal-", "/quran", "/ramadan", "/live",
        "gampad", "doubleclick", "?source=", "?ref=",
        "/video/", "/foto/", "/galeri/", "/photo/",
        "/podcast/", "/infografis/",
    )

    try:
        driver.get(url)
    except TimeoutException:
        pass

    while len(links) < limit:
        # Kumpulkan href sebagai plain string dulu — hindari StaleElementReferenceException
        raw_hrefs: list[str] = []
        for anchor in driver.find_elements(By.TAG_NAME, "a"):
            try:
                href = anchor.get_attribute("href") or ""
                if href:
                    raw_hrefs.append(href)
            except StaleElementReferenceException:
                continue

        for href in raw_hrefs:
            if len(links) >= limit:
                break

            # Jadikan full URL jika masih relative
            if href.startswith("/"):
                href = urljoin(base, href)

            # Filter: hanya http/https
            if not href.startswith("http"):
                continue

            # ── FILTER DOMAIN: hanya ambil link dari domain yang sama ──────
            # Izinkan subdomain berbeda (mis. m.detik.com saat input www.detik.com)
            parsed_href = urlparse(href)
            if not parsed_href.netloc.endswith(base_domain):
                continue

            # Buang URL yang mengandung keyword non-artikel
            if any(kw in href for kw in NON_ARTIKEL_KW):
                continue

            # Buang URL dengan ekstensi non-artikel
            if parsed_href.path.lower().endswith((".jpg", ".png", ".gif", ".pdf", ".mp4", ".webp")):
                continue

            # Hanya ambil URL dengan path minimal 3 level (/kategori/sub/judul-artikel)
            # Depth 2 (/nasional/politik) biasanya halaman kategori, bukan artikel
            path_depth = len([p for p in parsed_href.path.split("/") if p])
            if path_depth < 3:
                continue

            if href in seen:
                continue

            seen.add(href)
            links.append(href)

        # Lanjut ke halaman berikutnya jika belum mencapai limit
        if len(links) < limit and handle_pagination(driver):
            continue
        else:
            break

    return links


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
    import re
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    from selenium.common.exceptions import (
        NoSuchElementException, ElementNotInteractableException,
        ElementClickInterceptedException, StaleElementReferenceException,
    )

    # ── Strategi 1: <a rel="next"> atau <link rel="next"> ─────────────────
    for selector in ['a[rel="next"]', 'link[rel="next"]']:
        try:
            el = driver.find_element(By.CSS_SELECTOR, selector)
            next_url = el.get_attribute("href")
            if next_url:
                driver.get(next_url)
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            pass

    # ── Strategi 2: Tombol dengan teks "next" / variasi bahasa Indonesia ──
    NEXT_TEXTS = ["next", "selanjutnya", "berikutnya", "›", "»", ">"]
    for anchor in driver.find_elements(By.TAG_NAME, "a"):
        try:
            text = anchor.text.strip().lower()
            if text in NEXT_TEXTS:
                anchor.click()
                return True
        except (StaleElementReferenceException,
                ElementNotInteractableException,
                ElementClickInterceptedException):
            continue

    # ── Strategi 3: Konstruksi URL halaman berikutnya dari pola umum ───────
    current_url = driver.current_url
    parsed      = urlparse(current_url)
    qs          = parse_qs(parsed.query, keep_blank_values=True)

    # Pola ?page=N atau ?p=N
    for param in ("page", "p"):
        if param in qs:
            try:
                current_page    = int(qs[param][0])
                qs[param]       = [str(current_page + 1)]
                new_query       = urlencode(qs, doseq=True)
                next_url        = urlunparse(parsed._replace(query=new_query))
                driver.get(next_url)
                return True
            except (ValueError, Exception):
                pass

    # Pola /page/N atau /halaman/N
    for pattern, replacement in [
        (r"(/page/)(\d+)", lambda m: f"{m.group(1)}{int(m.group(2)) + 1}"),
        (r"(/halaman/)(\d+)", lambda m: f"{m.group(1)}{int(m.group(2)) + 1}"),
    ]:
        new_path, subs = re.subn(pattern, replacement, parsed.path)
        if subs:
            next_url = urlunparse(parsed._replace(path=new_path))
            driver.get(next_url)
            return True

    # ── Strategi 4: tidak ketemu → sudah halaman terakhir ─────────────────
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
    from selenium.common.exceptions import TimeoutException

    artikel = ARTIKEL_KOSONG.copy()
    artikel["url"] = url

    try:
        driver.get(url)
    except TimeoutException:
        pass  # DOM kemungkinan sudah siap, lanjutkan scraping

    # ════════════════════════════════════════════════════════════
    # STRATEGI EKSTRAKSI — 3 lapisan dari umum ke spesifik:
    #
    #   Lapisan 1 (UNIVERSAL) — OpenGraph + Schema.org
    #     → Standar internasional. SEMUA website berita modern
    #       mengimplementasikan ini untuk SEO dan social sharing.
    #       Works on ANY website, not just CNN/Detik/Kompas.
    #
    #   Lapisan 2 (SEMI-UMUM) — wildcard [class*='...'] + semantic HTML
    #     → Menebak nama class berdasarkan pola umum konvensi developer.
    #     → Tag HTML5 semantik: <article>, <time>, <main>.
    #
    #   Lapisan 3 (OPTIMASI) — class spesifik Detik/Kompas/CNN
    #     → Bukan "hardcode untuk 1 site" tapi shortcut agar lebih cepat
    #       dan akurat di site yang sudah kita kenal.
    #     → Jika tidak ada, lapisan 1 & 2 sudah cukup.
    # ════════════════════════════════════════════════════════════

    # ── Judul ─────────────────────────────────────────────────
    artikel["judul"] = (
        # L1: OpenGraph og:title & Schema.org headline
        _extract_meta(driver, ["og:title", "twitter:title", "headline"])
        or
        # L2 + L3: fallback ke elemen HTML
        _extract_text(driver, [
            (By.CSS_SELECTOR, "[itemprop='headline']"),     # Schema.org (elemen teks)
            (By.CSS_SELECTOR, "h1.detail__title"),          # Detik (L3)
            (By.CSS_SELECTOR, "h1.read__title"),            # Kompas (L3)
            (By.CSS_SELECTOR, "h1.title"),                  # CNN Indonesia (L3)
            (By.CSS_SELECTOR, "article h1"),                # Semantic HTML5
            (By.TAG_NAME, "h1"),                            # Generic
        ])
    )

    # ── Tanggal ───────────────────────────────────────────────
    # L1: OpenGraph article:published_time / Schema.org datePublished
    tanggal_meta = _extract_meta(
        driver, ["article:published_time", "datePublished", "date", "pubdate"]
    )
    if tanggal_meta != config.FIELD_KOSONG:
        artikel["tanggal"] = tanggal_meta
    else:
        # L2 + L3: fallback ke elemen HTML
        artikel["tanggal"] = _extract_text(driver, [
            (By.CSS_SELECTOR, "time[datetime]"),            # Atribut datetime HTML5
            (By.TAG_NAME, "time"),                          # Semantic HTML5
            (By.CSS_SELECTOR, ".detail__date"),             # Detik (L3)
            (By.CSS_SELECTOR, ".read__time"),               # Kompas (L3)
            (By.CSS_SELECTOR, ".publish_date"),             # CNN Indonesia (L3)
            (By.CSS_SELECTOR, "[class*='publish']"),        # Wildcard
            (By.CSS_SELECTOR, "[class*='date']"),           # Wildcard
            (By.CSS_SELECTOR, "[class*='time']"),           # Wildcard
        ])

    # ── Isi artikel ───────────────────────────────────────────
    # L1: Schema.org articleBody
    isi = _extract_meta(driver, ["articleBody"])
    if isi == config.FIELD_KOSONG:
        # L2 + L3: wildcard class, semantic HTML, lalu site-specific
        isi = _extract_text(driver, [
            (By.CSS_SELECTOR, "[itemprop='articleBody']"),  # Schema.org (elemen teks)
            (By.CSS_SELECTOR, "[class*='article-body']"),   # Wildcard
            (By.CSS_SELECTOR, "[class*='article-content']"),# Wildcard
            (By.CSS_SELECTOR, "[class*='post-content']"),   # Wildcard (WordPress dll)
            (By.CSS_SELECTOR, "[class*='story-body']"),     # Wildcard
            (By.CSS_SELECTOR, "[class*='entry-content']"),  # Wildcard (WordPress)
            (By.CSS_SELECTOR, ".detail__body-text"),        # Detik (L3)
            (By.CSS_SELECTOR, ".read__content"),            # Kompas (L3)
            (By.CSS_SELECTOR, ".detail-text"),              # CNN Indonesia (L3)
            (By.CSS_SELECTOR, "article"),                   # Semantic HTML5
            (By.CSS_SELECTOR, "main"),                      # Semantic HTML5
        ])
    artikel["isi"] = isi[:config.MAX_ISI_CHARS]

    # ── Penulis ───────────────────────────────────────────────
    artikel["penulis"] = (
        # L1: Schema.org author
        _extract_meta(driver, ["author", "article:author"])
        or
        # L2 + L3
        _extract_text(driver, [
            (By.CSS_SELECTOR, "[itemprop='author'] [itemprop='name']"),  # Schema.org
            (By.CSS_SELECTOR, "[itemprop='author']"),                    # Schema.org
            (By.CSS_SELECTOR, "[rel='author']"),                         # Microformat
            (By.CSS_SELECTOR, "[class*='author-name']"),                 # Wildcard
            (By.CSS_SELECTOR, "[class*='author']"),                      # Wildcard
            (By.CSS_SELECTOR, ".detail__author"),                        # Detik (L3)
            (By.CSS_SELECTOR, ".read__author"),                          # Kompas (L3)
        ])
    )

    # ── Kategori ──────────────────────────────────────────────
    artikel["kategori"] = (
        # L1: Schema.org articleSection
        _extract_meta(driver, ["articleSection", "article:section"])
        or
        # L2 + L3
        _extract_text(driver, [
            (By.CSS_SELECTOR, "[itemprop='articleSection']"),    # Schema.org
            (By.CSS_SELECTOR, "[class*='breadcrumb'] a"),        # Wildcard
            (By.CSS_SELECTOR, "[class*='category']"),            # Wildcard
            (By.CSS_SELECTOR, ".detail__nav > a"),               # Detik (L3)
            (By.CSS_SELECTOR, ".breadcrumb__item"),              # Kompas (L3)
            (By.CSS_SELECTOR, ".label_channel"),                 # CNN Indonesia (L3)
        ])
    )

    # ── Gambar URL ────────────────────────────────────────────
    # L1: OpenGraph og:image — PALING RELIABLE, semua website pakai ini untuk share
    gambar_meta = _extract_meta(driver, ["og:image", "twitter:image"])
    if gambar_meta != config.FIELD_KOSONG:
        artikel["gambar_url"] = gambar_meta
    else:
        # L2 + L3: cari img element
        from selenium.common.exceptions import NoSuchElementException
        for by, value in [
            (By.CSS_SELECTOR, "[itemprop='image']"),        # Schema.org
            (By.CSS_SELECTOR, "article img"),               # Gambar dalam artikel
            (By.CSS_SELECTOR, ".photo__wrap img"),          # Detik (L3)
            (By.CSS_SELECTOR, ".detail__media img"),        # Detik (L3)
        ]:
            try:
                img_el = driver.find_element(by, value)
                src = img_el.get_attribute("src") or img_el.get_attribute("data-src")
                if src and src.startswith("http"):
                    artikel["gambar_url"] = src
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