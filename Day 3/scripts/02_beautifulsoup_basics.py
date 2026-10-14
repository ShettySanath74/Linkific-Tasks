
import requests
from bs4 import BeautifulSoup

# Website for practicing web scraping
URL = "https://quotes.toscrape.com/"

# Step 1: Download the webpage
response = requests.get(
    URL,
    headers={"User-Agent": "LinkificLearningProject/1.0"},
    timeout=15
)

# Step 2: Check for HTTP errors
response.raise_for_status()

# Step 3: Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Step 4: Print the webpage title
print("Page title:", soup.title.get_text(strip=True))

# Step 5: Find all quote containers
quotes = soup.select(".quote")
print("Total quotes found:", len(quotes))

# Step 6: Extract quotes, authors and tags
for number, quote in enumerate(quotes, start=1):
    quote_text = quote.select_one(".text").get_text(strip=True)
    author = quote.select_one(".author").get_text(strip=True)

    tags = [
        tag.get_text(strip=True)
        for tag in quote.select(".tag")
    ]

    print(f"\nQuote {number}")
    print("Text:", quote_text)
    print("Author:", author)
    print("Tags:", ", ".join(tags))
