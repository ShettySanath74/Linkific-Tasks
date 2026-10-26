import json
import logging
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
STAGING_DIR = PROJECT_DIR / "staging"
LOG_DIR = PROJECT_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def read_json(file_path):
    """Read a JSON file and return its records."""
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def transform_data():
    try:
        # 1. Read staged data from the three sources
        api_records = read_json(STAGING_DIR / "api_posts.json")
        sales_records = read_json(STAGING_DIR / "sales_raw.json")
        customer_records = read_json(STAGING_DIR / "customers_raw.json")

        # 2. Convert source records into DataFrames
        api_df = pd.DataFrame(api_records)
        sales_df = pd.DataFrame(sales_records)
        customers_df = pd.DataFrame(customer_records)

        # 3. Clean the sales data
        sales_df["customer"] = sales_df["customer"].astype("string").str.strip()
        sales_df["product"] = sales_df["product"].astype("string").str.strip()
        sales_df["quantity"] = pd.to_numeric(
            sales_df["quantity"], errors="coerce"
        )
        sales_df["unit_price"] = pd.to_numeric(
            sales_df["unit_price"], errors="coerce"
        )
        sales_df["updated_at"] = pd.to_datetime(
            sales_df["updated_at"], errors="coerce"
        )

        # Remove records missing essential fields
        sales_df = sales_df.dropna(
            subset=["order_id", "customer", "product",
                    "quantity", "unit_price", "updated_at"]
        )

        # Remove duplicate orders
        sales_df = sales_df.drop_duplicates(subset=["order_id"])

        # Apply business logic
        sales_df["total_amount"] = (
            sales_df["quantity"] * sales_df["unit_price"]
        )

        # 4. Clean the customer data
        customers_df["customer_name"] = (
            customers_df["customer_name"].astype("string").str.strip()
        )
        customers_df["city"] = (
            customers_df["city"].astype("string").str.strip()
        )
        customers_df["updated_at"] = pd.to_datetime(
            customers_df["updated_at"], errors="coerce"
        )

        customers_df = customers_df.dropna(
            subset=["customer_id", "customer_name", "updated_at"]
        )
        customers_df = customers_df.drop_duplicates(
            subset=["customer_id"]
        )

        # 5. Join sales with customer records
        combined_sales = sales_df.merge(
            customers_df,
            left_on="customer",
            right_on="customer_name",
            how="left",
            suffixes=("_sale", "_customer"),
        )

        # 6. Prepare the API records
        api_df = api_df.rename(
            columns={"id": "post_id", "title": "post_title"}
        )

        # 7. Save transformed datasets
        sales_output = STAGING_DIR / "sales_transformed.csv"
        api_output = STAGING_DIR / "api_posts_transformed.csv"
        customers_output = STAGING_DIR / "customers_transformed.csv"

        combined_sales.to_csv(
            sales_output, index=False, encoding="utf-8-sig"
        )
        api_df.to_csv(api_output, index=False, encoding="utf-8-sig")
        customers_df.to_csv(
            customers_output, index=False, encoding="utf-8-sig"
        )

        logging.info(
            "Transformation complete: %s sales, %s customers, %s posts",
            len(combined_sales), len(customers_df), len(api_df)
        )

        print("Transformation completed successfully")
        print(f"Sales records: {len(combined_sales)}")
        print(f"Customer records: {len(customers_df)}")
        print(f"API posts: {len(api_df)}")
        print(f"Transformed files saved in: {STAGING_DIR}")

    except (OSError, ValueError, KeyError, TypeError) as error:
        logging.exception("Transformation failed")
        print(f"Transformation failed: {error}")


if __name__ == "__main__":
    transform_data()