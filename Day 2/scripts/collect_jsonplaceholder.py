
import json
from pathlib import Path

import requests

# Find the Day 2 project folder
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://jsonplaceholder.typicode.com/posts"

try:
    print("Connecting to JSONPlaceholder API...")

    response = requests.get(
        API_URL,
        params={"_limit": 20},
        timeout=15
    )

    response.raise_for_status()
    posts = response.json()

    # Extract the fields we need
    records = [
        {
            "post_id": post["id"],
            "user_id": post["userId"],
            "title": post["title"]
        }
        for post in posts
    ]

    # Save the data as JSON
    output_file = OUTPUT_DIR / "posts.json"
    output_file.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )

    print(f"Success! Collected {len(records)} posts.")
    print(f"Saved dataset to: {output_file}")

except requests.RequestException as error:
    print(f"API request failed: {error}")

except (KeyError, ValueError, TypeError) as error:
    print(f"Data processing failed: {error}")
