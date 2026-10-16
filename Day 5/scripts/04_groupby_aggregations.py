
import pandas as pd
from pathlib import Path

Path("outputs").mkdir(exist_ok=True)

# Sample sales dataset
data = {
    "Order_ID": [101, 102, 103, 104, 105, 106, 107, 108],
    "Customer": ["Asha", "Ravi", "Meera", "Kiran", "John", "Sara", "Asha", "Ravi"],
    "City": ["Mangalore", "Udupi", "Mangalore", "Bangalore",
             "Udupi", "Bangalore", "Mangalore", "Udupi"],
    "Category": ["Electronics", "Clothing", "Electronics", "Food",
                 "Clothing", "Food", "Food", "Electronics"],
    "Amount": [1500, 800, 2500, 400, 1200, 650, 700, 1800],
    "Quantity": [2, 3, 1, 5, 2, 4, 3, 1]
}

df = pd.DataFrame(data)
df["Sales"] = df["Amount"] * df["Quantity"]

print("\n--- ORIGINAL SALES DATA ---")
print(df.to_string(index=False))

# 1. Total sales by city
city_sales = df.groupby("City")["Sales"].sum()
print("\n--- TOTAL SALES BY CITY ---")
print(city_sales)

# 2. Average sales by category
category_average = df.groupby("Category")["Sales"].mean()
print("\n--- AVERAGE SALES BY CATEGORY ---")
print(category_average)

# 3. Multiple aggregations for each category
category_summary = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Average_Sales=("Sales", "mean"),
    Order_Count=("Order_ID", "count"),
    Total_Quantity=("Quantity", "sum")
)
print("\n--- CATEGORY SUMMARY ---")
print(category_summary)

# 4. Group by both city and category
city_category = df.groupby(["City", "Category"])["Sales"].sum()
print("\n--- SALES BY CITY AND CATEGORY ---")
print(city_category)

# 5. Pivot table: cities as rows, categories as columns
pivot = pd.pivot_table(
    df,
    values="Sales",
    index="City",
    columns="Category",
    aggfunc="sum",
    fill_value=0,
    observed=True
)
print("\n--- SALES PIVOT TABLE ---")
print(pivot)

# 6. Crosstab: order counts by city and category
cross_tab = pd.crosstab(df["City"], df["Category"])
print("\n--- ORDER COUNT CROSS-TABULATION ---")
print(cross_tab)

# 7. GroupBy transform: each order's share of its city's sales
df["City_Total_Sales"] = df.groupby("City")["Sales"].transform("sum")
df["City_Sales_Share_Percent"] = (
    df["Sales"] / df["City_Total_Sales"] * 100
).round(2)

print("\n--- DATA WITH CITY SALES SHARE ---")
print(df[[
    "Order_ID", "City", "Category", "Sales",
    "City_Total_Sales", "City_Sales_Share_Percent"
]].to_string(index=False))

# 8. GroupBy filter: cities with at least 2 orders
cities_with_multiple_orders = df.groupby("City").filter(
    lambda group: len(group) >= 2
)
print("\n--- ORDERS FROM CITIES WITH AT LEAST 2 ORDERS ---")
print(cities_with_multiple_orders.to_string(index=False))

# 9. Save all results inside Day 5/outputs
df.to_csv("outputs/sales_with_group_metrics.csv", index=False)
category_summary.to_csv("outputs/category_summary.csv")
pivot.to_csv("outputs/city_category_pivot.csv")
cross_tab.to_csv("outputs/city_category_crosstab.csv")

print("\nAll GroupBy and aggregation outputs saved inside Day 5/outputs/")

