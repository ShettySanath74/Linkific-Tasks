import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "warehouse" / "analytics.db"


def validate_warehouse():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Warehouse not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as connection:
        total_rows, unique_ids, total_sales, invalid_rows = connection.execute("""
            SELECT
                COUNT(*),
                COUNT(DISTINCT order_id),
                COALESCE(SUM(total_amount), 0),
                SUM(
                    CASE
                        WHEN order_id IS NULL
                          OR quantity <= 0
                          OR unit_price < 0
                          OR total_amount < 0
                        THEN 1 ELSE 0
                    END
                )
            FROM sales
        """).fetchone()

    checks = {
        "At least one sales record exists": total_rows > 0,
        "No duplicate order IDs": total_rows == unique_ids,
        "No invalid sales records": (invalid_rows or 0) == 0,
        "Expected sample record count is five": total_rows == 5,
        "Expected sample sales total is 83050": abs(total_sales - 83050) < 0.01,
    }

    print("WAREHOUSE VALIDATION")
    print("-" * 35)

    for description, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {description}")

    print(f"\nRows: {total_rows}")
    print(f"Unique order IDs: {unique_ids}")
    print(f"Total sales: {total_sales:.2f}")

    if not all(checks.values()):
        raise SystemExit("Warehouse validation failed.")

    print("\nAll warehouse checks passed!")


if __name__ == "__main__":
    validate_warehouse()