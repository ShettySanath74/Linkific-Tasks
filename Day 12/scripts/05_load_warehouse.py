import logging
import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
STAGING_DIR = PROJECT_DIR / "staging"
WAREHOUSE_DIR = PROJECT_DIR / "warehouse"
LOG_DIR = PROJECT_DIR / "logs"

WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = WAREHOUSE_DIR / "analytics.db"

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_sales():
    source_file = STAGING_DIR / "sales_transformed.csv"

    if not source_file.exists():
        raise FileNotFoundError(
            f"Missing transformed data: {source_file}. "
            "Run the extraction and transformation scripts first."
        )

    df = pd.read_csv(source_file)

    if "updated_at" not in df.columns and "updated_at_sale" in df.columns:
     df = df.rename(columns={"updated_at_sale": "updated_at"})

    required_columns = {
        "order_id", "customer", "product", "quantity",
        "unit_price", "total_amount", "updated_at"
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.drop_duplicates(subset=["order_id"], keep="last")

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                order_id INTEGER PRIMARY KEY,
                customer TEXT NOT NULL,
                product TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit_price REAL NOT NULL,
                total_amount REAL NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        connection.executemany("""
            INSERT INTO sales (
                order_id, customer, product, quantity,
                unit_price, total_amount, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(order_id) DO UPDATE SET
                customer = excluded.customer,
                product = excluded.product,
                quantity = excluded.quantity,
                unit_price = excluded.unit_price,
                total_amount = excluded.total_amount,
                updated_at = excluded.updated_at
            WHERE excluded.updated_at >= sales.updated_at
        """, [
            (
                int(row["order_id"]),
                str(row["customer"]),
                str(row["product"]),
                float(row["quantity"]),
                float(row["unit_price"]),
                float(row["total_amount"]),
                str(row["updated_at"]),
            )
            for _, row in df.iterrows()
        ])

        total_rows = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

    logging.info("Sales warehouse upsert completed; rows=%s", total_rows)
    print(f"Sales records processed: {len(df)}")
    print(f"Total records in warehouse: {total_rows}")
    print(f"Warehouse database: {DB_PATH}")


if __name__ == "__main__":
    try:
        load_sales()
    except (OSError, ValueError, sqlite3.Error) as error:
        logging.exception("Warehouse loading failed")
        print(f"Warehouse loading failed: {error}")