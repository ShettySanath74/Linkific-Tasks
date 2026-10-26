import json
import logging
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
STAGING_DIR = PROJECT_DIR / "staging"
LOG_DIR = PROJECT_DIR / "logs"

STAGING_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def extract_csv_data():
    try:
        source_file = DATA_DIR / "sales.csv"

        logging.info("Starting CSV extraction from %s", source_file)

        df = pd.read_csv(source_file)

        records = df.to_dict(orient="records")

        output_file = STAGING_DIR / "sales_raw.json"

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=2, ensure_ascii=False, default=str)

        logging.info("Extracted %s records from CSV", len(records))

        print(f"Successfully extracted {len(records)} records")
        print(f"Saved to: {output_file}")

        return df

    except (OSError, ValueError, pd.errors.ParserError):
        logging.exception("CSV extraction failed")
        print("CSV extraction failed. Check logs/etl_pipeline.log")
        return None

if __name__ == "__main__":
    extract_csv_data()