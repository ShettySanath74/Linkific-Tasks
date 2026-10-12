
import csv
import json
import re
from pathlib import Path


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

INPUT_FILE = DATA_DIR / "employees_to_validate.csv"
CLEAN_FILE = OUTPUT_DIR / "clean_employees.csv"
ERROR_FILE = OUTPUT_DIR / "validation_errors.json"

REQUIRED_FIELDS = ["employee_id", "name", "email", "age"]


def validate_record(row, seen_ids):
    """Return a list of validation errors for one employee."""

    errors = []

    # Check for missing required fields
    for field in REQUIRED_FIELDS:
        if not row.get(field, "").strip():
            errors.append(f"Missing required field: {field}")

    # Validate employee ID and detect duplicates
    employee_id = row.get("employee_id", "").strip()

    if employee_id:
        if not employee_id.isdigit():
            errors.append("Employee ID must be a positive integer.")
        elif int(employee_id) <= 0:
            errors.append("Employee ID must be greater than zero.")
        elif employee_id in seen_ids:
            errors.append(f"Duplicate employee ID: {employee_id}")
        else:
            seen_ids.add(employee_id)

    # Validate email format
    email = row.get("email", "").strip()

    if email and not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email
    ):
        errors.append("Invalid email format.")

    # Validate age
    age_text = row.get("age", "").strip()

    if age_text:
        try:
            age = int(age_text)

            if not 0 <= age <= 120:
                errors.append("Age must be between 0 and 120.")

        except ValueError:
            errors.append("Age must be a whole number.")

    return errors


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    valid_records = []
    invalid_records = []
    seen_ids = set()

    try:
        with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Validation failed: CSV header is missing.")
                return

            missing_columns = [
                field for field in REQUIRED_FIELDS
                if field not in reader.fieldnames
            ]

            if missing_columns:
                print(f"Missing columns: {missing_columns}")
                return

            for line_number, row in enumerate(reader, start=2):
                errors = validate_record(row, seen_ids)

                if errors:
                    invalid_records.append({
                        "line_number": line_number,
                        "record": row,
                        "errors": errors
                    })
                else:
                    # Convert age from string to integer
                    row["age"] = int(row["age"])
                    valid_records.append(row)

    except FileNotFoundError:
        print(f"Input file not found: {INPUT_FILE}")
        return

    # Save valid records
    with open(CLEAN_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        writer.writerows(valid_records)

    # Save validation errors
    with open(ERROR_FILE, "w", encoding="utf-8") as file:
        json.dump(invalid_records, file, indent=4)

    print("DATA VALIDATION REPORT")
    print("-" * 30)
    print(f"Total records: {len(valid_records) + len(invalid_records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records: {len(invalid_records)}")
    print(f"Clean data saved to: {CLEAN_FILE}")
    print(f"Error report saved to: {ERROR_FILE}")

    print("\nValidation issues:")
    for record in invalid_records:
        print(f"Line {record['line_number']}:")
        for error in record["errors"]:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
