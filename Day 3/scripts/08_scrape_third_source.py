
import csv
import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"
START_URL = BASE_URL + "/computers/laptops"

HEADERS = {
    "User-Agent": "LinkificLearningProject/1.0"
}

session = requests.Session()
session.headers.update(HEADERS)

products = []
current_url = START_URL
max_pages = 3
pages_scraped = 0

while current_url and pages_scraped < max_pages:
    print(f"Scraping page {pages_scraped + 1}: {current_url}")

    response = session.get(current_url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract product cards
    for card in soup.select(".thumbnail"):
        title_element = card.select_one(".title")
        price_element = card.select_one(".price")
        description_element = card.select_one(".description")
        rating_element = card.select_one(".ratings")

        products.append({
            "product": title_element.get("title", "").strip()
                if title_element else "",
            "price": price_element.get_text(strip=True)
                if price_element else "",
            "description": description_element.get_text(" ", strip=True)
                if description_element else "",
            "rating_count": rating_element.get_text(" ", strip=True)
                if rating_element else "",
            "source_url": current_url
        })

    pages_scraped += 1

    # Follow the next-page link if the website provides one
    next_link = soup.select_one("a[rel='next'], li.next a")

    if next_link and next_link.get("href"):
        current_url = urljoin(current_url, next_link["href"])
        time.sleep(1)
    else:
        current_url = None

# Save JSON
json_path = OUTPUT_DIR / "products.json"
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(products, file, indent=4, ensure_ascii=False)

# Save CSV
csv_path = OUTPUT_DIR / "products.csv"
fields = ["product", "price", "description", "rating_count", "source_url"]

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(products)

print("\nScraping completed!")
print("Pages scraped:", pages_scraped)
print("Products collected:", len(products))
print("JSON saved to:", json_path)
print("CSV saved to:", csv_path)
