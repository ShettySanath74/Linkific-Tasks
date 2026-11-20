"""Run post-load data quality checks against the SQLite warehouse."""
from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

from scripts.common import DATABASE_PATH, OUTPUT_DIR, ensure_directories, get_logger

logger = get_logger(__name__)


def run_quality_checks(transformed_csv: str, database_path: str | None = None) -> str:
    """Validate row counts, unique IDs, positive amounts and customer IDs."""
    ensure_directories()
    db_path = Path(database_path) if database_path else DATABASE_PATH

    with Path(transformed_csv).open("r", newline="", encoding="utf-8") as file:
        expected_records = list(csv.DictReader(file))

    with sqlite3.connect(db_path) as connection:
        actual_count = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]
        duplicate_ids = connection.execute("""
            SELECT COUNT(*) FROM (
                SELECT sale_id FROM sales GROUP BY sale_id HAVING COUNT(*) > 1
            )
        """).fetchone()[0]
        invalid_amounts = connection.execute(
            "SELECT COUNT(*) FROM sales WHERE amount <= 0"
        ).fetchone()[0]
        missing_customers = connection.execute("""
            SELECT COUNT(*) FROM sales
            WHERE customer_id IS NULL OR TRIM(customer_id) = ''
        """).fetchone()[0]

    expected_count = len(expected_records)
    checks = {
        "record_count_matches": actual_count == expected_count,
        "no_duplicate_sale_ids": duplicate_ids == 0,
        "all_amounts_positive": invalid_amounts == 0,
        "customer_ids_present": missing_customers == 0,
    }
    result = {
        "status": "PASSED" if all(checks.values()) else "FAILED",
        "expected_records_in_current_batch": expected_count,
        "actual_records_in_warehouse": actual_count,
        "duplicate_sale_ids": duplicate_ids,
        "invalid_amounts": invalid_amounts,
        "missing_customer_ids": missing_customers,
        "checks": checks,
    }

    result_path = OUTPUT_DIR / "quality_report.json"
    with result_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    logger.info("Quality checks %s: %s", result["status"], checks)
    if result["status"] != "PASSED":
        raise ValueError(f"Data quality checks failed. See {result_path}")

    return str(result_path)
