"""Extract customer and sales CSV files into JSON records."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.common import SOURCE_DIR, EXTRACT_DIR, ensure_directories, get_logger

logger = get_logger(__name__)


def extract_csv_to_json(source_path: Path, output_path: Path) -> str:
    """Read a CSV file and persist its rows as a JSON array."""
    ensure_directories()
    if not source_path.exists():
        raise FileNotFoundError(f"Source file does not exist: {source_path}")

    with source_path.open("r", newline="", encoding="utf-8-sig") as file:
        records = list(csv.DictReader(file))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)

    logger.info("Extracted %d rows from %s", len(records), source_path.name)
    return str(output_path)


def extract_customers() -> str:
    return extract_csv_to_json(
        SOURCE_DIR / "customers.csv", EXTRACT_DIR / "customers.json"
    )


def extract_sales() -> str:
    return extract_csv_to_json(
        SOURCE_DIR / "sales.csv", EXTRACT_DIR / "sales.json"
    )
