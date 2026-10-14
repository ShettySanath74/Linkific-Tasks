
import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Keep the output inside Day 3/outputs
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://quotes.toscrape.com/js/"

# Start Chrome. Selenium Manager can manage the driver automatically.
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,900")

driver = webdriver.Chrome(options=options)

try:
    print("Opening:", URL)
    driver.get(URL)

    # Wait until JavaScript-rendered quotes appear
    wait = WebDriverWait(driver, 20)
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".quote")
        )
    )

    # Extract quotes after the page has rendered
    quote_elements = driver.find_elements(
        By.CSS_SELECTOR, ".quote"
    )

    records = []

    for item in quote_elements:
        quote_text = item.find_element(
            By.CSS_SELECTOR, ".text"
        ).text.strip()

        author = item.find_element(
            By.CSS_SELECTOR, ".author"
        ).text.strip()

        tags = [
            tag.text.strip()
            for tag in item.find_elements(
                By.CSS_SELECTOR, ".tag"
            )
        ]

        records.append({
            "quote": quote_text,
            "author": author,
            "tags": ", ".join(tags)
        })

    # Save the collected records
    output_file = OUTPUT_DIR / "dynamic_quotes.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    print("Quotes collected:", len(records))
    print("Saved to:", output_file)

    for record in records[:3]:
        print("\n", record)

finally:
    # Close Chrome even if an error occurs
    driver.quit()
