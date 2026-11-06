
import json
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Input and output paths
INPUT_FILE = BASE_DIR / "outputs" / "api1_posts.json"
OUTPUT_DIR = BASE_DIR / "outputs" / "files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "posts_dataframe.csv"

def json_to_dataframe():
    print("Reading JSON data...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Convert JSON records into a DataFrame
    df = pd.DataFrame(data)

    print("\nDataFrame created successfully!")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))

    print("\nFirst five records:")
    print(df.head())

    # Save as CSV
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCSV file saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    json_to_dataframe()
