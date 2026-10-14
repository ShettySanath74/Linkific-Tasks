
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import json
import time

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "LinkificLearningProject/1.0"
}

session = requests.Session()
session.headers.update(HEADERS)

books = []
next_page = BASE_URL
page_count = 0
MAX_PAGES = 5  # Keep the practice run short and polite

while next_page and page_count < MAX_PAGES:
    print(f"Scraping page {page_count + 1}: {next_page}")

    response = session.get(next_page, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select("article.product_pod"):
        title_element = item.select_one("h3 a")
        price_element = item.select_one(".price_color")
        availability_element = item.select_one(".availability")
        rating_element = item.select_one(".star-rating")

        books.append({
            "title": title_element.get("title", "").strip() if title_element else "",
            "price": price_element.get_text(strip=True) if price_element else "",
            "availability": availability_element.get_text(" ", strip=True) if availability_element else "",
            "rating": rating_element.get("class", ["", "Unknown"])[1]
                if rating_element and len(rating_element.get("class", [])) > 1
                else "Unknown",
            "source_page": next_page
        })

    page_count += 1

    # Find the next page link
    next_link = soup.select_one("li.next a")

    if next_link:
        next_page = requests.compat.urljoin(next_page, next_link.get("href", ""))
        time.sleep(1)  # One-second pause between requests
    else:
        next_page = None

# Save JSON
json_path = OUTPUT_DIR / "books_paginated.json"
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(books, file, indent=4, ensure_ascii=False)

# Save CSV
csv_path = OUTPUT_DIR / "books_paginated.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "title", "price", "availability", "rating", "source_page"
    ])
    writer.writeheader()
    writer.writerows(books)

print("\nScraping completed!")
print("Pages scraped:", page_count)
print("Books collected:", len(books))
print("JSON:", json_path)
print("CSV:", csv_path)
