
import requests
import csv
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

URL = "https://books.toscrape.com/"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "scraped_books.csv"


def scrape_books():

    print("Connecting to Books to Scrape website...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        print("Website connected successfully!")

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all book containers
        book_containers = soup.select("article.product_pod")

        books = []

        for book in book_containers:

            title = book.h3.a["title"]

            price = book.select_one(".price_color").text

            availability = (
                book.select_one(".availability")
                .get_text(strip=True)
            )

            rating_element = book.select_one("p.star-rating")

            rating = rating_element.get("class")[1]

            books.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating
            })

        # Save data as CSV
        if books:
            with open(
                CSV_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "title",
                        "price",
                        "availability",
                        "rating"
                    ]
                )

                writer.writeheader()
                writer.writerows(books)

        print("\nScraping completed!")
        print("Books collected:", len(books))
        print("Saved to:", CSV_FILE)

        print("\nSample records:")
        for book in books[:5]:
            print(book)

    except requests.exceptions.RequestException as error:
        print("Website request failed:", error)


if __name__ == "__main__":
    scrape_books()
