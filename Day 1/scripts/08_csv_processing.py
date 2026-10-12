
# Script 08: CSV File Processing
# Linkific Data Engineering Internship

import csv
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Input files
file1 = DATA_DIR / "employees_part1.csv"
file2 = DATA_DIR / "employees_part2.csv"

# Output files
combined_file = OUTPUT_DIR / "combined_employees.csv"
filtered_file = OUTPUT_DIR / "data_engineering_employees.csv"

fieldnames = ["employee_id", "name", "department", "salary"]

print("=== 1. Creating Sample CSV Files ===")

employees_part1 = [
    {"employee_id": "101", "name": "Asha",
     "department": "Data Engineering", "salary": "45000"},
    {"employee_id": "102", "name": "Rahul",
     "department": "Software Engineering", "salary": "38000"},
]

employees_part2 = [
    {"employee_id": "103", "name": "Priya",
     "department": "Data Engineering", "salary": "52000"},
    {"employee_id": "104", "name": "Kiran",
     "department": "Testing", "salary": "35000"},
]

for path, records in [
    (file1, employees_part1),
    (file2, employees_part2),
]:
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

print("Created:", file1)
print("Created:", file2)


print("\n=== 2. Reading and Combining CSV Files ===")

all_employees = []

for path in [file1, file2]:
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["salary"] = float(row["salary"])
            all_employees.append(row)

print("Total employees:", len(all_employees))

for employee in all_employees:
    print(employee)


print("\n=== 3. Saving Combined CSV ===")

with open(
    combined_file, "w", newline="", encoding="utf-8"
) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_employees)

print("Combined data saved to:", combined_file)


print("\n=== 4. Filtering Data Engineering Employees ===")

data_engineers = [
    employee
    for employee in all_employees
    if employee["department"] == "Data Engineering"
]

for employee in data_engineers:
    print(employee["name"], "-", employee["salary"])


print("\n=== 5. Calculating Salary Statistics ===")

salaries = [employee["salary"] for employee in all_employees]

total_salary = sum(salaries)
average_salary = total_salary / len(salaries) if salaries else 0

print("Total salary:", total_salary)
print("Average salary:", average_salary)


print("\n=== 6. Saving Filtered CSV ===")

with open(
    filtered_file, "w", newline="", encoding="utf-8"
) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_engineers)

print("Filtered data saved to:", filtered_file)


print("\n=== 7. Verifying Output File ===")

with open(
    filtered_file, "r", newline="", encoding="utf-8"
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)

print("\n=== Script Completed ===")
