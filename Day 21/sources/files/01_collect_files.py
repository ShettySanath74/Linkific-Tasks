
import pandas as pd
import json
from pathlib import Path

# Locate project directories
BASE_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = BASE_DIR.parent

# Input files
CSV_FILE = (
    REPO_DIR / "Day 20" / "outputs"
    / "financial_transactions_100k.csv"
)

POSTS_FILE = BASE_DIR / "outputs" / "api1_posts.json"

COUNTRIES_FILE = BASE_DIR / "outputs" / "api2_countries.json"

# Output directory
OUTPUT_DIR = BASE_DIR / "outputs" / "files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def collect_csv():

    print("\n--- CSV COLLECTION ---")

    df = pd.read_csv(CSV_FILE)

    print("CSV loaded successfully!")
    print("Records:", len(df))
    print("Columns:", list(df.columns))

    df.to_csv(
        OUTPUT_DIR / "collected_transactions.csv",
        index=False
    )

    return df


def collect_json():

    print("\n--- JSON COLLECTION ---")

    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        posts = json.load(file)

    df = pd.DataFrame(posts)

    print("JSON loaded successfully!")
    print("Records:", len(df))
    print("Columns:", list(df.columns))

    df.to_json(
        OUTPUT_DIR / "collected_posts.json",
        orient="records",
        indent=4
    )

    return df


def collect_excel():

    print("\n--- EXCEL COLLECTION ---")

    # Read countries JSON
    with open(COUNTRIES_FILE, "r", encoding="utf-8") as file:
        countries = json.load(file)

    # Convert JSON into DataFrame
    df = pd.DataFrame(countries)

    # Create an Excel workbook
    excel_file = BASE_DIR / "data" / "files" / "countries.xlsx"

    df.to_excel(excel_file, index=False)

    # Read the Excel workbook
    excel_df = pd.read_excel(excel_file)

    print("Excel loaded successfully!")
    print("Records:", len(excel_df))
    print("Columns:", list(excel_df.columns))

    excel_df.to_excel(
        OUTPUT_DIR / "collected_countries.xlsx",
        index=False
    )

    return excel_df


if __name__ == "__main__":

    transactions = collect_csv()
    posts = collect_json()
    countries = collect_excel()

    print("\nAll file collection operations completed!")
