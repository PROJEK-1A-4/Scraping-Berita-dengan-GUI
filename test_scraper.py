from scraper import setup_driver, get_all_links

driver = setup_driver()

# Ganti dengan URL halaman listing yang punya banyak artikel
url   = "https://news.detik.com/berita"
limit = 30  # melebihi 1 halaman agar pagination terpicu

links = get_all_links(driver, url, limit)
print(f"Total link: {len(links)}")
for i, link in enumerate(links, 1):
    print(f"  {i}. {link}")

driver.quit()