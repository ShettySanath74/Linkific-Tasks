
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "outputs" / "files" / "employees_from_xml.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PARQUET_FILE = OUTPUT_DIR / "employees.parquet"
CSV_FILE = OUTPUT_DIR / "employees_parquet_restored.csv"


def convert_to_parquet():
    print("Reading employee CSV...")

    df = pd.read_csv(INPUT_FILE)

    print("\nOriginal DataFrame:")
    print(df)

    # Convert DataFrame to Parquet
    df.to_parquet(PARQUET_FILE, index=False)

    print("\nParquet file created:", PARQUET_FILE)

    # Read Parquet file
    parquet_df = pd.read_parquet(PARQUET_FILE)

    print("\nData read from Parquet:")
    print(parquet_df)

    # Convert back to CSV
    parquet_df.to_csv(CSV_FILE, index=False)

    print("\nRestored CSV created:", CSV_FILE)
    print("\nParquet conversion completed successfully!")


if __name__ == "__main__":
    convert_to_parquet()
