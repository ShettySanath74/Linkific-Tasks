
# Script 09: JSON Processing in Python
# Linkific Data Engineering Internship

import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

input_file = DATA_DIR / "employees.json"
output_file = OUTPUT_DIR / "processed_employees.json"

print("=== 1. Creating Sample JSON Data ===")

company_data = {
    "company": "Linkific",
    "employees": [
        {
            "id": 101,
            "name": "Asha",
            "department": "Data Engineering",
            "salary": 45000,
            "skills": ["Python", "SQL"]
        },
        {
            "id": 102,
            "name": "Rahul",
            "department": "Software Engineering",
            "salary": 38000,
            "skills": ["Java", "Python"]
        },
        {
            "id": 103,
            "name": "Priya",
            "department": "Data Engineering",
            "salary": 52000,
            "skills": ["Python", "Pandas", "SQL"]
        },
        {
            "id": 104,
            "name": "Kiran",
            "department": "Testing",
            "skills": ["Testing", "SQL"]
        }
    ]
}

with open(input_file, "w", encoding="utf-8") as file:
    json.dump(company_data, file, indent=4)

print("JSON file created:", input_file)


print("\n=== 2. Reading JSON from a File ===")

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

print("Company:", data["company"])
print("Total employees:", len(data["employees"]))


print("\n=== 3. Accessing Nested JSON ===")

first_employee = data["employees"][0]

print("Employee name:", first_employee["name"])
print("Department:", first_employee["department"])
print("Skills:", first_employee["skills"])


print("\n=== 4. Extracting Selected Fields ===")

for employee in data["employees"]:
    employee_id = employee["id"]
    name = employee["name"]
    department = employee["department"]

    print(employee_id, "-", name, "-", department)


print("\n=== 5. Handling Missing Values ===")

for employee in data["employees"]:
    salary = employee.get("salary")

    if salary is None:
        print(employee["name"], "- Salary is missing")
    else:
        print(employee["name"], "- Salary:", salary)


print("\n=== 6. Filtering Data Engineering Employees ===")

data_engineers = [
    employee
    for employee in data["employees"]
    if employee.get("department") == "Data Engineering"
]

for employee in data_engineers:
    print(employee["name"], "-", employee["department"])


print("\n=== 7. Extracting Skills ===")

all_skills = set()

for employee in data["employees"]:
    for skill in employee.get("skills", []):
        all_skills.add(skill)

print("Unique skills:", sorted(all_skills))


print("\n=== 8. Saving Processed JSON ===")

processed_data = {
    "company": data["company"],
    "total_data_engineers": len(data_engineers),
    "employees": data_engineers
}

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(processed_data, file, indent=4)

print("Processed JSON saved to:", output_file)


print("\n=== 9. Reading Back Processed JSON ===")

with open(output_file, "r", encoding="utf-8") as file:
    saved_data = json.load(file)

print(json.dumps(saved_data, indent=4))

print("\n=== Script Completed ===")
