import json
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
STATE_PATH = WAREHOUSE_DIR / "etl_state.json"

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def incremental_load():
    source_file = STAGING_DIR / "sales_transformed.csv"

    if not source_file.exists():
        raise FileNotFoundError(
            f"Missing file: {source_file}. Run extraction and transformation first."
        )

    df = pd.read_csv(source_file)

    if "updated_at" not in df.columns and "updated_at_sale" in df.columns:
        df = df.rename(columns={"updated_at_sale": "updated_at"})

    required = {
        "order_id", "customer", "product", "quantity",
        "unit_price", "total_amount", "updated_at"
    }
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")
    df = df.dropna(subset=["order_id", "updated_at"])
    df = df.drop_duplicates(subset=["order_id"], keep="last")

    # Read the last successfully processed timestamp.
    if STATE_PATH.exists():
        with STATE_PATH.open("r", encoding="utf-8") as file:
            state = json.load(file)
        watermark = pd.to_datetime(state.get("sales_watermark"), errors="coerce")
    else:
        watermark = pd.NaT

    if pd.isna(watermark):
        new_records = df.copy()
    else:
        new_records = df[df["updated_at"] > watermark].copy()

    print(f"Current watermark: {watermark}")
    print(f"Newer records to process: {len(new_records)}")

    # Create the destination table if it does not exist.
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

        # Upsert the selected records into the warehouse.
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
            WHERE excluded.updated_at > sales.updated_at
        """, [
            (
                int(row["order_id"]),
                str(row["customer"]),
                str(row["product"]),
                float(row["quantity"]),
                float(row["unit_price"]),
                float(row["total_amount"]),
                row["updated_at"].strftime("%Y-%m-%d %H:%M:%S"),
            )
            for _, row in new_records.iterrows()
        ])

        connection.commit()

    # Update the watermark only after the database load succeeds.
    if not df.empty:
        latest = df["updated_at"].max()

        if pd.isna(watermark) or latest > watermark:
            watermark = latest

        state = {
            "sales_watermark": watermark.strftime("%Y-%m-%d %H:%M:%S")
        }

        temp_path = STATE_PATH.with_suffix(".tmp")
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(state, file, indent=2)
        temp_path.replace(STATE_PATH)

    logging.info(
        "Incremental load finished: processed %s records",
        len(new_records)
    )
    print("Incremental load completed.")
    print(f"Warehouse database: {DB_PATH}")
    print(f"Watermark state: {STATE_PATH}")


if __name__ == "__main__":
    try:
        incremental_load()
    except (OSError, ValueError, sqlite3.Error) as error:
        logging.exception("Incremental load failed")
        print(f"Incremental load failed: {error}")
        raise