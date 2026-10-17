
from pathlib import Path
import pandas as pd

# Keep all input and output files inside Day 6
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Sample employee dataset
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104],
    "name": ["Asha", "Ravi", "Meera", "Kiran"],
    "department_id": [1, 2, 1, 3]
})

# Sample department dataset
departments = pd.DataFrame({
    "department_id": [1, 2, 4],
    "department": ["Engineering", "Analytics", "Marketing"]
})

employees.to_csv(DATA_DIR / "employees.csv", index=False)
departments.to_csv(DATA_DIR / "departments.csv", index=False)

# 1. INNER JOIN: only matching department IDs
inner = pd.merge(
    employees, departments,
    on="department_id", how="inner"
)
inner.to_csv(OUTPUT_DIR / "inner_join.csv", index=False)

# 2. LEFT JOIN: keep every employee
left = pd.merge(
    employees, departments,
    on="department_id", how="left"
)
left.to_csv(OUTPUT_DIR / "left_join.csv", index=False)

# 3. RIGHT JOIN: keep every department
right = pd.merge(
    employees, departments,
    on="department_id", how="right"
)
right.to_csv(OUTPUT_DIR / "right_join.csv", index=False)

# 4. OUTER JOIN: keep all employees and departments
outer = pd.merge(
    employees, departments,
    on="department_id", how="outer",
    indicator=True
)
outer.to_csv(OUTPUT_DIR / "outer_join.csv", index=False)

# 5. CONCAT: append DataFrames vertically
employees_extra = pd.DataFrame({
    "employee_id": [105, 106],
    "name": ["Neha", "Arun"],
    "department_id": [2, 1]
})

combined = pd.concat(
    [employees, employees_extra],
    ignore_index=True
)
combined.to_csv(OUTPUT_DIR / "concatenated_employees.csv", index=False)

# 6. MULTI-KEY MERGE
sales = pd.DataFrame({
    "employee_id": [101, 101, 102, 103],
    "month": ["Jan", "Feb", "Jan", "Jan"],
    "sales": [5000, 7000, 6000, 4500]
})

targets = pd.DataFrame({
    "employee_id": [101, 101, 102, 103],
    "month": ["Jan", "Feb", "Jan", "Feb"],
    "target": [4500, 6500, 6500, 4000]
})

multi_key = pd.merge(
    sales, targets,
    on=["employee_id", "month"],
    how="inner"
)
multi_key.to_csv(OUTPUT_DIR / "multi_key_merge.csv", index=False)

print("DATAFRAME MERGING COMPLETED")
print("\nINNER JOIN:")
print(inner)
print("\nLEFT JOIN:")
print(left)
print("\nRIGHT JOIN:")
print(right)
print("\nOUTER JOIN:")
print(outer)
print("\nCONCATENATED EMPLOYEES:")
print(combined)
print("\nMULTI-KEY MERGE:")
print(multi_key)

print(f"\nAll outputs saved to: {OUTPUT_DIR}")

