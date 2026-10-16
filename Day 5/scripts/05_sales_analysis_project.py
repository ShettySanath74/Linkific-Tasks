
import pandas as pd
from pathlib import Path

# All paths are relative to the Day 5 folder
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Create a sample raw sales dataset
raw_data = {
    "Order_ID": [1001, 1002, 1003, 1004, 1005, 1005, 1006, 1007, 1008],
    "Customer": [
        " Asha ", "RAVI", "Meera", "Kiran", "John", "John",
        None, "Sara", "Asha"
    ],
    "City": [
        "Mangalore", " Udupi", "MANGALORE", "Bangalore",
        "Udupi", "Udupi", None, "Bangalore", "Mangalore"
    ],
    "Category": [
        "Electronics", "Clothing", "Electronics", "Food",
        "Clothing", "Clothing", "Food", "Electronics", "Food"
    ],
    "Amount": [
        "1500", "800", "2500", "400", "1200", "1200",
        "650", "1800", "700"
    ],
    "Quantity": [2, 3, 1, 5, 2, 2, None, 1, 3]
}

raw_df = pd.DataFrame(raw_data)
raw_df.to_csv(DATA_DIR / "raw_sales.csv", index=False)

print("\n1. RAW DATA")
print(raw_df.to_string(index=False))

# 2. Clean the data
df = raw_df.drop_duplicates().copy()

df["Customer"] = df["Customer"].str.strip().str.title()
df["City"] = df["City"].str.strip().str.title()
df["Category"] = df["Category"].str.strip().str.title()

df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

df["Customer"] = df["Customer"].fillna("Unknown")
df["City"] = df["City"].fillna("Unknown")

# Fill missing values using explicit practice rules
df["Amount"] = df["Amount"].fillna(df["Amount"].median())
df["Quantity"] = df["Quantity"].fillna(0).astype(int)

df = df.rename(columns={
    "Order_ID": "order_id",
    "Customer": "customer",
    "City": "city",
    "Category": "category",
    "Amount": "unit_price",
    "Quantity": "quantity"
})

# 3. Transform the data
df["sales_value"] = df["unit_price"] * df["quantity"]
df["discount"] = df["sales_value"] * 0.10
df["final_sales"] = df["sales_value"] - df["discount"]

df["sales_band"] = pd.cut(
    df["final_sales"],
    bins=[-1, 1000, 3000, float("inf")],
    labels=["Small", "Medium", "Large"]
)

# 4. Generate category-level metrics
category_report = df.groupby("category", observed=True).agg(
    total_sales=("final_sales", "sum"),
    average_order_value=("final_sales", "mean"),
    order_count=("order_id", "count"),
    units_sold=("quantity", "sum")
).reset_index()

# 5. Generate city-level metrics
city_report = df.groupby("city", observed=True).agg(
    total_sales=("final_sales", "sum"),
    order_count=("order_id", "count")
).reset_index()

# 6. Generate a city-by-category pivot table
sales_pivot = pd.pivot_table(
    df,
    values="final_sales",
    index="city",
    columns="category",
    aggfunc="sum",
    fill_value=0,
    observed=True
)

# 7. Save all project outputs inside Day 5/outputs
df.to_csv(OUTPUT_DIR / "cleaned_sales_analysis.csv", index=False)
category_report.to_csv(OUTPUT_DIR / "category_sales_report.csv", index=False)
city_report.to_csv(OUTPUT_DIR / "city_sales_report.csv", index=False)
sales_pivot.to_csv(OUTPUT_DIR / "city_category_sales_pivot.csv")

print("\n2. CLEANED AND TRANSFORMED DATA")
print(df.to_string(index=False))

print("\n3. CATEGORY SALES REPORT")
print(category_report.to_string(index=False))

print("\n4. CITY SALES REPORT")
print(city_report.to_string(index=False))

print("\n5. CITY-CATEGORY PIVOT TABLE")
print(sales_pivot)

print("\nProject completed successfully!")
print(f"Raw input: {DATA_DIR / 'raw_sales.csv'}")
print(f"Reports saved in: {OUTPUT_DIR.resolve()}")
