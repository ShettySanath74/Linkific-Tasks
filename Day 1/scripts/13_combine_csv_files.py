
import csv
from pathlib import Path


# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

# Input files
INPUT_FILES = [
    DATA_DIR / "employees_january.csv",
    DATA_DIR / "employees_february.csv"
]

# Output file
OUTPUT_FILE = OUTPUT_DIR / "all_employees.csv"


def combine_csv_files(input_files, output_file):
    """Combine multiple CSV files with matching column names."""

    all_records = []
    expected_columns = None

    for file_path in input_files:
        print(f"Reading: {file_path.name}")

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError(f"Missing CSV header: {file_path.name}")

            if expected_columns is None:
                expected_columns = reader.fieldnames
            elif reader.fieldnames != expected_columns:
                raise ValueError(
                    f"Column mismatch in {file_path.name}"
                )

            for row in reader:
                all_records.append(row)

    if expected_columns is None:
        raise ValueError("No input CSV files were provided.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(
        output_file, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=expected_columns)
        writer.writeheader()
        writer.writerows(all_records)

    print(f"\nTotal records combined: {len(all_records)}")
    print(f"Combined file saved to: {output_file}")


def main():
    try:
        for file_path in INPUT_FILES:
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Input file not found: {file_path}"
                )

        combine_csv_files(INPUT_FILES, OUTPUT_FILE)

    except (FileNotFoundError, ValueError) as error:
        print(f"Processing failed: {error}")


if __name__ == "__main__":
    main()
