import time
from bs4 import BeautifulSoup
from config.settings import TIMEOUT, STAGING_DIR
from scripts.api_ingestion import request_json
from scripts.common import get_logger, write_jsonl

logger = get_logger("web_scraper")

def scrape_books(max_pages=3):
    records = []
    for page in range(1, max_pages + 1):
        url = "https://books.toscrape.com/catalogue/page-{}.html".format(page)
        # requests + BeautifulSoup handles this static HTML site; no browser needed.
        import requests
        response = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "Linkific-Day23/1.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")
        if not products:
            break
        for product in products:
            title_node = product.select_one("h3 a")
            price_node = product.select_one(".price_color")
            availability_node = product.select_one(".availability")
            rating_node = product.select_one("p.star-rating")
            records.append({
                "title": title_node.get("title") if title_node else None,
                "relative_url": title_node.get("href") if title_node else None,
                "price": price_node.get_text(strip=True) if price_node else None,
                "availability": availability_node.get_text(" ", strip=True) if availability_node else None,
                "rating": rating_node.get("class", [])[-1] if rating_node and len(rating_node.get("class", [])) > 1 else None,
                "source_page": page
            })
        time.sleep(1)  # polite crawl delay
    write_jsonl(records, STAGING_DIR / "scraped" / "books_to_scrape.jsonl")
    logger.info("Web scraper: collected %d book records", len(records))
    return len(records)

if __name__ == "__main__":
    print({"scraped_records": scrape_books()})
