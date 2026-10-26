import json
import logging
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PROJECT_DIR = Path(__file__).resolve().parent.parent
STAGING_DIR = PROJECT_DIR / "staging"
LOG_DIR = PROJECT_DIR / "logs"

STAGING_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

API_URL = "https://jsonplaceholder.typicode.com/posts"


def extract_api_data():
    output_file = STAGING_DIR / "api_posts.json"

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    try:
        with requests.Session() as session:
            session.mount("https://", adapter)

            logging.info("Starting API extraction with retry handling")

            response = session.get(API_URL, timeout=30)
            response.raise_for_status()
            records = response.json()

        # Save to a temporary file first, then replace the output.
        temp_file = output_file.with_suffix(".tmp")

        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=2, ensure_ascii=False)

        temp_file.replace(output_file)

        logging.info("Extracted %s API records", len(records))
        print(f"Successfully extracted {len(records)} records")
        print(f"Saved to: {output_file}")

        return records

    except (requests.RequestException, ValueError, OSError):
        logging.exception("API extraction failed")
        print("API extraction failed. Check logs/etl_pipeline.log")
        return None


if __name__ == "__main__":
    extract_api_data()