
import requests
import json
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# API URL
API_URL = "https://jsonplaceholder.typicode.com/posts"

# Output directory
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "api1_posts.json"


def collect_posts():

    print("Connecting to JSONPlaceholder API...")

    try:
        # Send GET request
        response = requests.get(API_URL, timeout=15)

        # Check HTTP response
        response.raise_for_status()

        # Convert response into Python data
        posts = response.json()

        # Save data as JSON
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(posts, file, indent=4)

        print("Collection successful!")
        print(f"HTTP Status: {response.status_code}")
        print(f"Total posts collected: {len(posts)}")
        print(f"Saved to: {OUTPUT_FILE}")

    except requests.exceptions.RequestException as error:
        print(f"API collection failed: {error}")


if __name__ == "__main__":
    collect_posts()
