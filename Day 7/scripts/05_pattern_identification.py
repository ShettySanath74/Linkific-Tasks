
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "ecommerce_sales.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["sales"] = df["quantity"] * df["unit_price"]

# Remove duplicate orders for the analysis
df = df.drop_duplicates(subset=["order_id"], keep="first")

# 1. Category performance
category_report = (
    df.groupby("category")
    .agg(
        total_orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
        total_sales=("sales", "sum"),
        average_order_value=("sales", "mean")
    )
    .sort_values("total_sales", ascending=False)
    .round(2)
)

# 2. Customer spending
customer_report = (
    df.groupby("customer")
    .agg(
        total_orders=("order_id", "nunique"),
        total_spent=("sales", "sum"),
        average_spend=("sales", "mean")
    )
    .sort_values("total_spent", ascending=False)
    .round(2)
)

# 3. Monthly sales trend
df["month"] = df["order_date"].dt.to_period("M").astype(str)

monthly_report = (
    df.groupby("month")
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales", "sum")
    )
    .sort_index()
    .round(2)
)

# 4. Find unusually high sales using the IQR method
q1 = df["sales"].quantile(0.25)
q3 = df["sales"].quantile(0.75)
iqr = q3 - q1

upper_limit = q3 + 1.5 * iqr
outliers = df[df["sales"] > upper_limit].copy()

# 5. Save the reports
category_report.to_csv(OUTPUT_DIR / "category_pattern_report.csv")
customer_report.to_csv(OUTPUT_DIR / "customer_spending_report.csv")
monthly_report.to_csv(OUTPUT_DIR / "monthly_sales_trend.csv")
outliers.to_csv(OUTPUT_DIR / "sales_anomalies.csv", index=False)

print("\n=== CATEGORY PERFORMANCE ===")
print(category_report)

print("\n=== CUSTOMER SPENDING ===")
print(customer_report)

print("\n=== MONTHLY SALES TREND ===")
print(monthly_report)

print(f"\nUpper outlier threshold: {upper_limit:.2f}")
print(f"Unusually high sales records: {len(outliers)}")
print(outliers[["order_id", "customer", "sales"]].to_string(index=False))

print("\nPattern identification completed!")
print(f"Reports saved in: {OUTPUT_DIR}")
