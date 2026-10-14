
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import json
import time

# Keep all outputs inside the Day 3 project
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "LinkificLearningProject/1.0"
}

session = requests.Session()
session.headers.update(HEADERS)

all_quotes = []
next_page = BASE_URL
page_count = 0
MAX_PAGES = 3

while next_page and page_count < MAX_PAGES:
    print(f"Scraping page {page_count + 1}: {next_page}")

    response = session.get(next_page, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select(".quote"):
        text_element = item.select_one(".text")
        author_element = item.select_one(".author")

        tags = [
            tag.get_text(strip=True)
            for tag in item.select(".tag")
        ]

        all_quotes.append({
            "quote": text_element.get_text(strip=True) if text_element else "",
            "author": author_element.get_text(strip=True) if author_element else "",
            "tags": ", ".join(tags),
            "source_page": next_page
        })

    page_count += 1

    # Find the next-page link
    next_link = soup.select_one("li.next a")

    if next_link:
        next_page = requests.compat.urljoin(
            next_page,
            next_link.get("href", "")
        )
        time.sleep(1)
    else:
        next_page = None

# Save as JSON
json_path = OUTPUT_DIR / "quotes.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(all_quotes, file, indent=4, ensure_ascii=False)

# Save as CSV
csv_path = OUTPUT_DIR / "quotes.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["quote", "author", "tags", "source_page"]
    )
    writer.writeheader()
    writer.writerows(all_quotes)

print("\nScraping completed!")
print("Pages scraped:", page_count)
print("Quotes collected:", len(all_quotes))
print("JSON saved to:", json_path)
print("CSV saved to:", csv_path)
