
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[1]

DB_FILE = BASE_DIR / "data" / "databases" / "company.db"
OUTPUT_DIR = BASE_DIR / "outputs" / "files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "integrated_customer_sales.csv"


def integrate_data():
    print("Starting data integration pipeline...")

    # 1. Extract data from SQLite
    connection = sqlite3.connect(DB_FILE)

    customers = pd.read_sql_query(
        "SELECT * FROM customers", connection
    )

    sales = pd.read_sql_query(
        "SELECT * FROM sales", connection
    )

    connection.close()

    print("\nCustomer records:", len(customers))
    print("Sales records:", len(sales))

    # 2. Schema mapping and standardization
    customers = customers.rename(columns={
        "customer_id": "customer_key",
        "name": "customer_name",
        "city": "customer_city"
    })

    sales = sales.rename(columns={
        "customer_id": "customer_key",
        "amount": "sale_amount"
    })

    # 3. Check duplicate customer keys
    if customers["customer_key"].duplicated().any():
        raise ValueError("Duplicate customer keys detected!")

    # 4. Handle missing matching keys
    customers = customers.dropna(subset=["customer_key"])
    sales = sales.dropna(subset=["customer_key"])

    # 5. Integrate using a left join
    integrated = customers.merge(
        sales,
        on="customer_key",
        how="left",
        validate="one_to_many",
        indicator=True
    )

    # 6. Handle unmatched customer records
    integrated["sale_amount"] = (
        integrated["sale_amount"].fillna(0)
    )

    integrated["match_status"] = integrated["_merge"].map({
        "both": "Matched",
        "left_only": "Customer without sales",
        "right_only": "Sale without customer"
    })

    integrated = integrated.drop(columns=["_merge"])

    # 7. Add data lineage
    integrated["source_system"] = "company.db"
    integrated["extraction_timestamp"] = (
        datetime.now(timezone.utc).isoformat()
    )

    # 8. Export integrated dataset
    integrated.to_csv(OUTPUT_FILE, index=False)

    print("\nIntegration completed successfully!")
    print("Integrated records:", len(integrated))

    print("\nIntegrated dataset:")
    print(integrated.to_string(index=False))

    print("\nMatch status:")
    print(integrated["match_status"].value_counts())

    print("\nSaved to:", OUTPUT_FILE)


if __name__ == "__main__":
    integrate_data()
