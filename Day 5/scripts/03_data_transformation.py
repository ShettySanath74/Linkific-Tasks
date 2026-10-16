
import pandas as pd
from pathlib import Path

# Ensure output folder exists
Path("outputs").mkdir(exist_ok=True)

# Sample sales dataset
data = {
    "Order_ID": [101, 102, 103, 104, 105, 106],
    "Customer": ["Asha", "Ravi", "Meera", "Kiran", "John", "Sara"],
    "Category": ["Electronics", "Clothing", "Electronics", "Food", "Clothing", "Food"],
    "Amount": [1500, 800, 2500, 400, 1200, 650],
    "Quantity": [2, 3, 1, 5, 2, 4]
}

df = pd.DataFrame(data)

print("\n--- ORIGINAL DATA ---")
print(df.to_string(index=False))

# 1. Create new columns
df["Total_Value"] = df["Amount"] * df["Quantity"]

# 2. Apply a function to calculate a 10% discount
df["Discount"] = df["Total_Value"].apply(lambda value: value * 0.10)
df["Final_Amount"] = df["Total_Value"] - df["Discount"]

# 3. Map categories to department codes
category_codes = {
    "Electronics": "ELEC",
    "Clothing": "CLOTH",
    "Food": "FOOD"
}
df["Category_Code"] = df["Category"].map(category_codes)

# 4. Replace category names
df["Category"] = df["Category"].replace({
    "Food": "Groceries"
})

# 5. Sort by final amount, highest first
df = df.sort_values(by="Final_Amount", ascending=False)

# 6. Rank orders by final amount
df["Sales_Rank"] = df["Final_Amount"].rank(
    ascending=False,
    method="dense"
).astype(int)

# 7. Categorize orders using bins
df["Order_Size"] = pd.cut(
    df["Final_Amount"],
    bins=[-1, 1000, 3000, float("inf")],
    labels=["Small", "Medium", "Large"]
)

# 8. Demonstrate pivot: total final amount by category
pivot = pd.pivot_table(
    df,
    values="Final_Amount",
    index="Category",
    aggfunc="sum",
    observed=True
)

# 9. Demonstrate melt: convert selected columns to long format
melted = df[["Order_ID", "Amount", "Quantity"]].melt(
    id_vars="Order_ID",
    var_name="Measure",
    value_name="Value"
)

print("\n--- TRANSFORMED DATA ---")
print(df.to_string(index=False))

print("\n--- PIVOT TABLE: SALES BY CATEGORY ---")
print(pivot)

print("\n--- MELTED DATA: LONG FORMAT ---")
print(melted.to_string(index=False))

# Save outputs within Day 5
df.to_csv("outputs/transformed_sales.csv", index=False)
pivot.to_csv("outputs/category_sales_pivot.csv")
melted.to_csv("outputs/sales_melted.csv", index=False)

print("\nAll transformation outputs saved inside Day 5/outputs/")
