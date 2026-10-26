import json
import sqlite3
import logging
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
STAGING_DIR = PROJECT_DIR / "staging"
LOG_DIR = PROJECT_DIR / "logs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
STAGING_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

DB_PATH = DATA_DIR / "source.db"


def create_sample_database():
    """Create a sample source database and insert customers if absent."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                city TEXT,
                updated_at TEXT NOT NULL
            )
        """)

        connection.executemany("""
            INSERT OR IGNORE INTO customers
                (customer_id, customer_name, city, updated_at)
            VALUES (?, ?, ?, ?)
        """, [
            (1, "Asha", "Bengaluru", "2026-10-25 10:00:00"),
            (2, "Rahul", "Mysuru", "2026-10-25 11:00:00"),
            (3, "Meera", "Mangaluru", "2026-10-26 09:00:00"),
            (4, "Arjun", "Hubballi", "2026-10-26 10:00:00"),
        ])

    logging.info("Sample source database is ready")


def extract_database_data():
    try:
        create_sample_database()

        with sqlite3.connect(DB_PATH) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT customer_id, customer_name, city, updated_at
                FROM customers
                ORDER BY customer_id
            """).fetchall()

        records = [dict(row) for row in rows]

        output_file = STAGING_DIR / "customers_raw.json"
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=2, ensure_ascii=False)

        logging.info("Extracted %s customer records", len(records))
        print(f"Successfully extracted {len(records)} customers")
        print(f"Saved to: {output_file}")

        return records

    except sqlite3.Error:
        logging.exception("Database extraction failed")
        print("Database extraction failed. Check logs/etl_pipeline.log")
        return []


if __name__ == "__main__":
    extract_database_data()