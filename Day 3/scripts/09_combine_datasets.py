
import csv
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

# Read a JSON file and return its records
def load_json(filename):
    path = OUTPUT_DIR / filename

    if not path.exists():
        print(f"Skipping missing file: {filename}")
        return []

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        print(f"Skipping {filename}: expected a list of records")
        return []

    return data


combined = []

# 1. Standardize book records
for book in load_json("books_paginated.json"):
    combined.append({
        "source": "Books to Scrape",
        "item_name": book.get("title", ""),
        "description": "",
        "price": book.get("price", ""),
        "author": "",
        "category_or_tags": "",
        "rating_or_availability": (
            f"Rating: {book.get('rating', '')}; "
            f"Availability: {book.get('availability', '')}"
        ),
        "source_url": book.get("source_page", "")
    })

# 2. Standardize quote records
for quote in load_json("quotes.json"):
    combined.append({
        "source": "Quotes to Scrape",
        "item_name": quote.get("quote", ""),
        "description": "",
        "price": "",
        "author": quote.get("author", ""),
        "category_or_tags": quote.get("tags", ""),
        "rating_or_availability": "",
        "source_url": quote.get("source_page", "")
    })

# 3. Standardize product records
for product in load_json("products.json"):
    combined.append({
        "source": "WebScraper.io demo",
        "item_name": product.get("product", ""),
        "description": product.get("description", ""),
        "price": product.get("price", ""),
        "author": "",
        "category_or_tags": "",
        "rating_or_availability": product.get("rating_count", ""),
        "source_url": product.get("source_url", "")
    })

# Save combined JSON
json_path = OUTPUT_DIR / "combined_scraped_data.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(combined, file, indent=4, ensure_ascii=False)

# Save combined CSV
csv_path = OUTPUT_DIR / "combined_scraped_data.csv"

fields = [
    "source",
    "item_name",
    "description",
    "price",
    "author",
    "category_or_tags",
    "rating_or_availability",
    "source_url"
]

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(combined)

# Print a summary by source
print("\nCombined dataset created!")
print("Total records:", len(combined))

for source in sorted({record["source"] for record in combined}):
    count = sum(1 for record in combined if record["source"] == source)
    print(f"{source}: {count} records")

print("JSON saved to:", json_path)
print("CSV saved to:", csv_path)
