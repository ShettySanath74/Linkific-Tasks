
import csv
import json
import re
from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

INPUT_FILES = [
    DATA_DIR / "etl_employees_january.csv",
    DATA_DIR / "etl_employees_february.csv",
]

CLEAN_FILE = OUTPUT_DIR / "etl_clean_employees.csv"
REJECTED_FILE = OUTPUT_DIR / "etl_rejected_records.json"
SUMMARY_FILE = OUTPUT_DIR / "etl_summary.json"

REQUIRED_COLUMNS = [
    "employee_id",
    "name",
    "email",
    "department",
    "monthly_salary",
]


# --------------------------------------------------
# 2. EXTRACT
# --------------------------------------------------

def extract_data(input_files):
    """Read employee records from multiple CSV files."""

    records = []

    for file_path in input_files:
        print(f"Extracting: {file_path.name}")

        with open(
            file_path, "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError(
                    f"Missing CSV header: {file_path.name}"
                )

            missing_columns = [
                column for column in REQUIRED_COLUMNS
                if column not in reader.fieldnames
            ]

            if missing_columns:
                raise ValueError(
                    f"{file_path.name} is missing columns: "
                    f"{missing_columns}"
                )

            for row in reader:
                row["_source_file"] = file_path.name
                records.append(row)

    return records


# --------------------------------------------------
# 3. TRANSFORM AND VALIDATE
# --------------------------------------------------

def transform_data(records):
    """Validate records and transform valid employee data."""

    clean_records = []
    rejected_records = []
    seen_ids = set()

    for row in records:
        errors = []

        employee_id = row["employee_id"].strip()
        name = row["name"].strip()
        email = row["email"].strip()
        department = row["department"].strip()
        salary_text = row["monthly_salary"].strip()

        # Validate employee ID
        if not employee_id.isdigit() or int(employee_id) <= 0:
            errors.append("Employee ID must be a positive integer.")
        elif employee_id in seen_ids:
            errors.append(f"Duplicate employee ID: {employee_id}")
        else:
            seen_ids.add(employee_id)

        # Validate required text fields
        if not name:
            errors.append("Name is missing.")

        if not department:
            errors.append("Department is missing.")

        # Basic email format check
        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email
        ):
            errors.append("Invalid email format.")

        # Validate monthly salary
        try:
            monthly_salary = float(salary_text)

            if monthly_salary <= 0:
                errors.append("Salary must be greater than zero.")

        except ValueError:
            monthly_salary = None
            errors.append("Salary must be numeric.")

        # Reject invalid records
        if errors:
            rejected_records.append({
                "source_file": row["_source_file"],
                "record": {
                    key: value
                    for key, value in row.items()
                    if key != "_source_file"
                },
                "errors": errors,
            })
            continue

        # Transform valid records
        clean_records.append({
            "employee_id": int(employee_id),
            "name": " ".join(name.split()).title(),
            "email": email.lower(),
            "department": department.strip().title(),
            "monthly_salary": round(monthly_salary, 2),
            "annual_salary": round(monthly_salary * 12, 2),
            "source_file": row["_source_file"],
        })

    return clean_records, rejected_records


# --------------------------------------------------
# 4. LOAD
# --------------------------------------------------

def load_data(clean_records, rejected_records, summary):
    """Save the processed data and reports."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save clean employee records
    clean_columns = [
        "employee_id",
        "name",
        "email",
        "department",
        "monthly_salary",
        "annual_salary",
        "source_file",
    ]

    with open(
        CLEAN_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=clean_columns
        )
        writer.writeheader()
        writer.writerows(clean_records)

    # Save rejected records with explanations
    with open(REJECTED_FILE, "w", encoding="utf-8") as file:
        json.dump(rejected_records, file, indent=4)

    # Save the processing summary
    with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    print("\nLOAD COMPLETE")
    print(f"Clean data: {CLEAN_FILE}")
    print(f"Rejected data: {REJECTED_FILE}")
    print(f"Summary: {SUMMARY_FILE}")


# --------------------------------------------------
# 5. MAIN PIPELINE
# --------------------------------------------------

def main():
    start_time = datetime.now()

    print("=" * 45)
    print("EMPLOYEE ETL PIPELINE")
    print("=" * 45)

    try:
        # EXTRACT
        for file_path in INPUT_FILES:
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Input file not found: {file_path}"
                )

        records = extract_data(INPUT_FILES)

        # TRANSFORM
        clean_records, rejected_records = transform_data(records)

        # Calculate summary metrics
        department_counts = {}
        total_monthly_salary = 0

        for record in clean_records:
            department = record["department"]
            department_counts[department] = (
                department_counts.get(department, 0) + 1
            )
            total_monthly_salary += record["monthly_salary"]

        end_time = datetime.now()

        summary = {
            "pipeline": "Employee ETL",
            "run_timestamp": start_time.isoformat(
                timespec="seconds"
            ),
            "total_input_records": len(records),
            "clean_records": len(clean_records),
            "rejected_records": len(rejected_records),
            "total_monthly_salary": round(
                total_monthly_salary, 2
            ),
            "average_monthly_salary": round(
                total_monthly_salary / len(clean_records), 2
            ) if clean_records else 0,
            "department_counts": department_counts,
            "duration_seconds": round(
                (end_time - start_time).total_seconds(), 3
            ),
        }

        # LOAD
        load_data(clean_records, rejected_records, summary)

        # Final report
        print("\nPIPELINE SUMMARY")
        print("-" * 30)
        print(f"Input records: {len(records)}")
        print(f"Clean records: {len(clean_records)}")
        print(f"Rejected records: {len(rejected_records)}")
        print(
            "Average monthly salary: "
            f"{summary['average_monthly_salary']:.2f}"
        )
        print(f"Department counts: {department_counts}")
        print("\nETL pipeline completed successfully.")

    except (FileNotFoundError, ValueError) as error:
        print(f"\nETL pipeline failed: {error}")


if __name__ == "__main__":
    main()

