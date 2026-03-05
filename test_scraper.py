from scraper import setup_driver, get_all_links

driver = setup_driver()

url   = "https://news.detik.com/berita"  # halaman daftar berita
limit = 200
links = get_all_links(driver, url, limit)

print(f"Total link: {len(links)}")
for i, link in enumerate(links, 1):
    print(f"  {i}. {link}")

driver.quit()