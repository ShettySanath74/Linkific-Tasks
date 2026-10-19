
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "ecommerce_sales.csv"
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

# Calculate sales for each order
df["sales"] = df["quantity"] * df["unit_price"]

# 1. Dataset overview
overview = pd.DataFrame({
    "Metric": [
        "Total rows",
        "Total columns",
        "Duplicate rows",
        "Total missing values",
        "Memory usage (bytes)"
    ],
    "Value": [
        len(df),
        len(df.columns),
        int(df.duplicated().sum()),
        int(df.isnull().sum().sum()),
        int(df.memory_usage(deep=True).sum())
    ]
})

# 2. Column-level data quality report
column_report = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing Count": df.isnull().sum().values,
    "Missing Percentage": (
        df.isnull().mean().values * 100
    ).round(2),
    "Unique Values": df.nunique().values
})

# 3. Numeric summary
numeric_summary = df.describe().round(2).T
numeric_summary.index.name = "Column"

# 4. Save reports
overview.to_csv(OUTPUT_DIR / "dataset_overview.csv", index=False)
column_report.to_csv(
    OUTPUT_DIR / "column_data_quality.csv", index=False
)
numeric_summary.to_csv(OUTPUT_DIR / "numeric_summary.csv")

print("\n=== DATASET OVERVIEW ===")
print(overview.to_string(index=False))

print("\n=== COLUMN DATA QUALITY ===")
print(column_report.to_string(index=False))

print("\n=== NUMERIC SUMMARY ===")
print(numeric_summary)

print("\nProfiling completed successfully!")
print(f"Reports saved to: {OUTPUT_DIR}")
