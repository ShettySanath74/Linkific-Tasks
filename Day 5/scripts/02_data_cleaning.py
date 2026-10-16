
import pandas as pd
from pathlib import Path

# Create the required folders if they do not exist
Path("data").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)

# 1. Create a messy sales dataset for practice
data = {
    "Order_ID": [101, 102, 103, 104, 104, 105, 106],
    "Customer": [
        "  Asha  ", "Ravi", "MEERA", "Kiran",
        "Kiran", "John ", None
    ],
    "City": [
        "Mangalore", " Udupi ", "MANGALORE", "Bangalore",
        "Bangalore", None, "Mysore"
    ],
    "Amount": ["1500", "2000", None, "3000", "3000", "2500", "1800"],
    "Quantity": [2, 4, 3, 5, 5, None, 2]
}

df = pd.DataFrame(data)

print("\n--- ORIGINAL MESSY DATA ---")
print(df.to_string(index=False))

# 2. Inspect missing values
print("\n--- MISSING VALUES PER COLUMN ---")
print(df.isnull().sum())

# 3. Remove duplicate rows
df = df.drop_duplicates()

# 4. Clean text columns
df["Customer"] = df["Customer"].str.strip().str.title()
df["City"] = df["City"].str.strip().str.title()

# 5. Convert Amount from text to numeric
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# 6. Handle missing values
df["Customer"] = df["Customer"].fillna("Unknown")
df["City"] = df["City"].fillna("Unknown")
df["Amount"] = df["Amount"].fillna(df["Amount"].median())
df["Quantity"] = df["Quantity"].fillna(0)

# 7. Convert Quantity to integer
df["Quantity"] = df["Quantity"].astype(int)

# 8. Rename columns
df = df.rename(columns={
    "Order_ID": "order_id",
    "Customer": "customer",
    "City": "city",
    "Amount": "amount",
    "Quantity": "quantity"
})

# 9. Reset the index after cleaning
df = df.reset_index(drop=True)

print("\n--- CLEANED DATA ---")
print(df.to_string(index=False))

print("\n--- CLEANED DATA TYPES ---")
print(df.dtypes)

print("\n--- CLEANING SUMMARY ---")
print("Rows after duplicate removal and cleaning:", len(df))
print("Missing values remaining:")
print(df.isnull().sum())

# 10. Save cleaned dataset
output_path = Path("outputs/cleaned_sales.csv")
df.to_csv(output_path, index=False)

print(f"\nCleaned dataset saved to: {output_path}")

