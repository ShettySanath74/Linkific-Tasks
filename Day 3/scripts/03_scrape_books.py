
import requests
from bs4 import BeautifulSoup
import csv
import json
from pathlib import Path

BASE_URL = "https://books.toscrape.com/"
# Always save outputs inside the Day 3 project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "LinkificLearningProject/1.0"
}

# Download the first page of books
response = requests.get(BASE_URL, headers=HEADERS, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

books = []

# Extract information from each book
for item in soup.select("article.product_pod"):
    title = item.select_one("h3 a")["title"]
    price = item.select_one(".price_color").get_text(strip=True)
    availability = item.select_one(".availability").get_text(strip=True)

    rating_element = item.select_one(".star-rating")
    rating = "Unknown"

    if rating_element:
        rating = rating_element.get("class", ["", "Unknown"])[1]

    books.append({
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating
    })

# Save as JSON
json_path = OUTPUT_DIR / "books.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(books, file, indent=4, ensure_ascii=False)

# Save as CSV
csv_path = OUTPUT_DIR / "books.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["title", "price", "availability", "rating"]
    )
    writer.writeheader()
    writer.writerows(books)

print(f"Books collected: {len(books)}")
print(f"JSON saved to: {json_path}")
print(f"CSV saved to: {csv_path}")

# Display a preview
for book in books[:5]:
    print(book)
