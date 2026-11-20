"""Load transformed sales into a SQLite warehouse table."""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

from scripts.common import DATABASE_PATH, ensure_directories, get_logger

logger = get_logger(__name__)


def load_sales(transformed_csv: str) -> str:
    """Create the target table and upsert accepted sales by sale_id."""
    ensure_directories()
    source_path = Path(transformed_csv)
    if not source_path.exists():
        raise FileNotFoundError(f"Transformed file not found: {source_path}")

    with source_path.open("r", newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                customer_name TEXT,
                city TEXT,
                product TEXT,
                amount REAL NOT NULL CHECK (amount > 0),
                sale_date TEXT NOT NULL
            )
        """)
        connection.executemany("""
            INSERT INTO sales (
                sale_id, customer_id, customer_name, city,
                product, amount, sale_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(sale_id) DO UPDATE SET
                customer_id = excluded.customer_id,
                customer_name = excluded.customer_name,
                city = excluded.city,
                product = excluded.product,
                amount = excluded.amount,
                sale_date = excluded.sale_date
        """, [
            (
                row["sale_id"], row["customer_id"], row["customer_name"],
                row["city"], row["product"], float(row["amount"]),
                row["sale_date"]
            )
            for row in records
        ])
        connection.commit()

    logger.info("Loaded/upserted %d sales into %s", len(records), DATABASE_PATH)
    return str(DATABASE_PATH)
