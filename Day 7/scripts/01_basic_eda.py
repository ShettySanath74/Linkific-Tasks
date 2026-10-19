
from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "ecommerce_sales.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)
df["sales"] = df["quantity"] * df["unit_price"]

print("\n===== DATASET OVERVIEW =====")
print("Rows and columns:", df.shape)
print("\nFirst five rows:")
print(df.head())

print("\n===== COLUMN INFORMATION =====")
df.info()

print("\n===== SUMMARY STATISTICS =====")
print(df.describe(include="all").to_string())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print("Duplicate rows:", df.duplicated().sum())

print("\n===== SALES BY CATEGORY =====")
print(df.groupby("category")["sales"].agg(
    ["count", "sum", "mean"]
))

print("\n===== CORRELATION =====")
print(
    df[["quantity", "unit_price", "rating", "sales"]]
    .corr()
    .round(2)
)

# Save reports
df.describe(include="all").to_csv(
    OUTPUT_DIR / "basic_eda_summary.csv"
)

df.isnull().sum().to_csv(
    OUTPUT_DIR / "missing_values_report.csv",
    header=["missing_count"]
)

print("\nEDA completed!")
print("Reports saved to:", OUTPUT_DIR)
