import json
import random
from pathlib import Path
from faker import Faker

fake = Faker("en_US")
random.seed(20)
Faker.seed(20)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

departments = ["Engineering", "Finance", "HR", "Sales", "Operations"]

employees = []
for employee_id in range(1, 201):
    hire_date = fake.date_between(start_date="-10y", end_date="today")
    employees.append({
        "employee_id": employee_id,
        "name": fake.name(),
        "email": fake.unique.email(),
        "department": random.choice(departments),
        "job_title": fake.job(),
        "hire_date": hire_date.isoformat(),
        "salary": round(random.uniform(30000, 150000), 2),
        "manager_id": random.randint(1, employee_id - 1)
            if employee_id > 1 and random.random() < 0.8 else None,
    })

employee_ids = {employee["employee_id"] for employee in employees}
assert all(
    employee["manager_id"] is None or employee["manager_id"] in employee_ids
    for employee in employees
)

with (DATA_DIR / "employees.json").open("w", encoding="utf-8") as file:
    json.dump(employees, file, indent=2)

print(f"Employees generated: {len(employees)}")
print("Validation passed: manager references are valid.")