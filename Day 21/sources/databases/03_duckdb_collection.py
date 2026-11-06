
import duckdb
from pathlib import Path

# Locate project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Input CSV from Day 20
CSV_PATH = (
    BASE_DIR.parent
    / "Day 20"
    / "outputs"
    / "financial_transactions_100k.csv"
)

# Database location
DB_DIR = BASE_DIR / "data" / "databases"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "analytics.duckdb"


def collect_and_analyze():

    print("Connecting to DuckDB...")

    connection = duckdb.connect(str(DB_PATH))

    # Load CSV into a database table
    connection.execute("""
        CREATE OR REPLACE TABLE transactions AS
        SELECT *
        FROM read_csv_auto(?)
    """, [str(CSV_PATH)])

    print("Data loaded successfully!")

    # Count records
    count = connection.execute("""
        SELECT COUNT(*)
        FROM transactions
    """).fetchone()[0]

    print(f"Total transactions: {count:,}")

    # Display sample records
    print("\nSample transactions:")

    sample = connection.execute("""
        SELECT *
        FROM transactions
        LIMIT 5
    """).fetchall()

    for row in sample:
        print(row)

    # Calculate total transaction amount
    print("\nFinancial Summary:")

    summary = connection.execute("""
        SELECT SUM(amount)
        FROM transactions
    """).fetchone()

    print(f"Total transaction amount: {summary[0]}")

    connection.close()

    print("\nDuckDB processing completed!")


if __name__ == "__main__":
    collect_and_analyze()

