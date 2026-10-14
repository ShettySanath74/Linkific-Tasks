
import json
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"


def clean_records(records, required_fields):
    """Clean text fields, remove incomplete records and duplicates."""
    cleaned = []
    seen = set()

    for record in records:
        # Remove leading/trailing whitespace from text fields
        record = {
            key: value.strip() if isinstance(value, str) else value
            for key, value in record.items()
        }

        # Skip records missing required information
        if any(not record.get(field) for field in required_fields):
            continue

        # Build a key to detect duplicate records
        key = tuple(
            str(record.get(field, "")).casefold()
            for field in required_fields
        )

        if key in seen:
            continue

        seen.add(key)
        cleaned.append(record)

    return cleaned


def process_dataset(input_name, output_name, required_fields):
    input_path = OUTPUT_DIR / input_name
    output_json = OUTPUT_DIR / output_name
    output_csv = OUTPUT_DIR / output_name.replace(".json", ".csv")

    if not input_path.exists():
        print(f"Skipping {input_name}: file not found")
        return

    with open(input_path, "r", encoding="utf-8") as file:
        records = json.load(file)

    cleaned = clean_records(records, required_fields)

    with open(output_json, "w", encoding="utf-8") as file:
        json.dump(cleaned, file, indent=4, ensure_ascii=False)

    # Use all available keys as CSV columns
    fieldnames = list(cleaned[0].keys()) if cleaned else required_fields

    with open(output_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)

    print(f"\nDataset: {input_name}")
    print("Records before cleaning:", len(records))
    print("Records after cleaning:", len(cleaned))
    print("Removed:", len(records) - len(cleaned))
    print("Cleaned JSON:", output_json.name)
    print("Cleaned CSV:", output_csv.name)


if __name__ == "__main__":
    process_dataset(
        "books_paginated.json",
        "books_cleaned.json",
        ["title", "price"]
    )

    process_dataset(
        "quotes.json",
        "quotes_cleaned.json",
        ["quote", "author"]
    )

    process_dataset(
        "dynamic_quotes.json",
        "dynamic_quotes_cleaned.json",
        ["quote", "author"]
    )
