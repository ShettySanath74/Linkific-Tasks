import numpy as np
import csv
from pathlib import Path

# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 55)
print("SALES DATA STATISTICAL ANALYSIS")
print("=" * 55)

# 1. Create a sample sales dataset
sales_data = [
    ["Date", "Product", "Units_Sold", "Unit_Price"],
    ["2026-10-01", "Laptop", 5, 50000],
    ["2026-10-02", "Phone", 12, 20000],
    ["2026-10-03", "Tablet", 8, 15000],
    ["2026-10-04", "Laptop", 3, 50000],
    ["2026-10-05", "Phone", 15, 20000],
    ["2026-10-06", "Tablet", 10, 15000],
    ["2026-10-07", "Laptop", 4, 50000],
    ["2026-10-08", "Phone", 9, 20000],
    ["2026-10-09", "Tablet", 6, 15000],
    ["2026-10-10", "Laptop", 7, 50000],
]

# 2. Save the dataset as CSV
csv_path = DATA_DIR / "sales_data.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(sales_data)

print("\n1. Sample sales dataset saved:", csv_path)

# 3. Load the numeric data into NumPy arrays
rows = sales_data[1:]

units = np.array([int(row[2]) for row in rows])
prices = np.array([float(row[3]) for row in rows])

# 4. Calculate revenue for every transaction
revenue = units * prices

print("\n2. Transaction revenue:")
for row, amount in zip(rows, revenue):
    print(f"{row[1]} on {row[0]}: Rs. {amount:,.2f}")

# 5. Overall statistics
print("\n3. Overall sales statistics")
print("Total units sold:", np.sum(units))
print("Total revenue: Rs.", f"{np.sum(revenue):,.2f}")
print("Average units per transaction:", f"{np.mean(units):.2f}")
print("Median units sold:", np.median(units))
print("Standard deviation of units:", f"{np.std(units):.2f}")

# 6. Percentiles
print("\n4. Revenue percentiles")
print("25th percentile:", np.percentile(revenue, 25))
print("50th percentile:", np.percentile(revenue, 50))
print("75th percentile:", np.percentile(revenue, 75))

# 7. Find the highest and lowest revenue transactions
best_index = np.argmax(revenue)
worst_index = np.argmin(revenue)

print("\n5. Highest revenue transaction:")
print(rows[best_index][1], "Rs.", f"{revenue[best_index]:,.2f}")

print("Lowest revenue transaction:")
print(rows[worst_index][1], "Rs.", f"{revenue[worst_index]:,.2f}")

# 8. Filter high-revenue transactions
high_revenue_mask = revenue >= 100000
high_revenue = revenue[high_revenue_mask]

print("\n6. Transactions with revenue >= Rs. 1,00,000:")
print(high_revenue)
print("Number of qualifying transactions:", len(high_revenue))

# 9. Analyze sales by product
print("\n7. Revenue by product")
products = np.array([row[1] for row in rows])

for product in np.unique(products):
    product_mask = products == product
    product_revenue = np.sum(revenue[product_mask])
    product_units = np.sum(units[product_mask])

    print(
        f"{product}: {product_units} units, "
        f"Rs. {product_revenue:,.2f} revenue"
    )

# 10. Save the enriched transaction data
output_path = OUTPUT_DIR / "sales_analysis.csv"

with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Date", "Product", "Units_Sold", "Unit_Price", "Revenue"
    ])

    for row, amount in zip(rows, revenue):
        writer.writerow(row + [float(amount)])

print("\n8. Enriched data saved:", output_path)
print("\nSales analysis completed successfully!")