
import pandas as pd

# 1. Create a DataFrame from a dictionary
data = {
    "Employee": ["Asha", "Ravi", "Meera", "Kiran", "John"],
    "Department": ["IT", "Sales", "IT", "HR", "Sales"],
    "Salary": [45000, 35000, 50000, 40000, 38000],
    "Experience": [3, 2, 5, 4, 2]
}

df = pd.DataFrame(data)

# 2. Display the complete DataFrame
print("\n--- Employee DataFrame ---")
print(df)

# 3. View the first and last rows
print("\n--- First 3 Rows ---")
print(df.head(3))

print("\n--- Last 2 Rows ---")
print(df.tail(2))

# 4. Inspect the structure
print("\n--- DataFrame Shape ---")
print(df.shape)

print("\n--- Column Names ---")
print(df.columns.tolist())

print("\n--- Data Types and Non-null Counts ---")
df.info()

# 5. Statistical summary
print("\n--- Statistical Summary ---")
print(df.describe())

# 6. Select one column
print("\n--- Employee Names ---")
print(df["Employee"])

# 7. Select multiple columns
print("\n--- Employee and Salary ---")
print(df[["Employee", "Salary"]])

# 8. Filter rows by condition
print("\n--- Employees Earning More Than 40000 ---")
print(df[df["Salary"] > 40000])

# 9. Save the dataset
df.to_csv("data/employees.csv", index=False)

print("\nDataset saved to data/employees.csv")
