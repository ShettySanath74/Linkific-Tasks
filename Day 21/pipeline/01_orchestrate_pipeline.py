
import logging
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[1]

DB_FILE = BASE_DIR / "data" / "databases" / "company.db"
OUTPUT_DIR = BASE_DIR / "outputs" / "files"
LOG_DIR = BASE_DIR / "outputs" / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "pipeline_integrated_data.csv"
LOG_FILE = LOG_DIR / "integration_pipeline.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)


def extract_data():
    logging.info("Starting data extraction")

    if not DB_FILE.exists():
        raise FileNotFoundError(f"Database not found: {DB_FILE}")

    with sqlite3.connect(DB_FILE) as connection:
        customers = pd.read_sql_query(
            "SELECT * FROM customers", connection
        )
        sales = pd.read_sql_query(
            "SELECT * FROM sales", connection
        )

    logging.info(
        "Extracted %d customers and %d sales",
        len(customers), len(sales)
    )

    return customers, sales


def transform_data(customers, sales):
    logging.info("Starting data transformation")

    customers = customers.rename(columns={
        "customer_id": "customer_key",
        "name": "customer_name",
        "city": "customer_city"
    })

    sales = sales.rename(columns={
        "customer_id": "customer_key",
        "amount": "sale_amount"
    })

    if customers["customer_key"].duplicated().any():
        raise ValueError("Duplicate customer keys detected")

    integrated = customers.merge(
        sales,
        on="customer_key",
        how="left",
        validate="one_to_many",
        indicator=True
    )

    integrated["match_status"] = integrated["_merge"].map({
        "both": "Matched",
        "left_only": "Customer without sales",
        "right_only": "Sale without customer"
    })

    integrated = integrated.drop(columns=["_merge"])

    integrated["source_system"] = "company.db"
    integrated["processed_at"] = (
        datetime.now(timezone.utc).isoformat()
    )

    logging.info(
        "Transformation completed with %d records",
        len(integrated)
    )

    return integrated


def load_data(data):
    logging.info("Starting data loading")

    data.to_csv(OUTPUT_FILE, index=False)

    logging.info("Output saved to %s", OUTPUT_FILE)


def run_pipeline():
    logging.info("========== PIPELINE STARTED ==========")

    try:
        customers, sales = extract_data()

        integrated = transform_data(customers, sales)

        load_data(integrated)

        logging.info("PIPELINE COMPLETED SUCCESSFULLY")

        print("Pipeline completed successfully!")
        print("Integrated records:", len(integrated))
        print("Output:", OUTPUT_FILE)
        print("Log:", LOG_FILE)

    except Exception:
        logging.exception("PIPELINE FAILED")
        print("Pipeline failed. Check the log file for details.")


if __name__ == "__main__":
    run_pipeline()
