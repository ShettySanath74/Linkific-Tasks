

employee = {
    "employee_id": 101,
    "name": "Asha",
    "department": "Data Engineering",
    "salary": 35000
}

print("1. ORIGINAL EMPLOYEE RECORD")
print(employee)


# 2. ACCESS VALUES

print("\n2. ACCESSING VALUES")
print("Employee name:", employee["name"])
print("Department:", employee["department"])
print("Salary:", employee["salary"])


# 3. ADD AND UPDATE VALUES

employee["email"] = "asha@example.com"  # Add a key
employee["department"] = "Analytics"    # Update a value

print("\n3. UPDATED EMPLOYEE RECORD")
print(employee)



# 4. HANDLE MISSING KEYS

print("\n4. HANDLING MISSING INFORMATION")

# The email_backup key does not exist.
backup_email = employee.get("email_backup", "Not provided")
print("Backup email:", backup_email)


# 5. LOOP THROUGH KEY-VALUE PAIRS

print("\n5. EMPLOYEE FIELDS")

for key, value in employee.items():
    print(f"{key}: {value}")


# 6. WORK WITH NESTED DICTIONARIES

record = {
    "employee_id": 102,
    "details": {
        "name": "Rahul",
        "department": "Data Engineering"
    }
}

print("\n6. NESTED DICTIONARY")
print("Name:", record["details"]["name"])
print("Department:", record["details"]["department"])


# 7. PRACTICAL DATA ENGINEERING EXAMPLE

employees = [
    {"id": 101, "name": "Asha", "department": "Data Engineering"},
    {"id": 102, "name": "Rahul", "department": "Analytics"},
    {"id": 103, "name": "Priya", "department": "Data Engineering"},
    {"id": 104, "name": "Kiran", "department": "Analytics"},
    {"id": 105, "name": "Meera", "department": "Data Engineering"}
]

department_counts = {}

for employee_record in employees:
    department = employee_record["department"]

    # Start the count at zero if this department is new.
    if department not in department_counts:
        department_counts[department] = 0

    department_counts[department] += 1

print("\n7. EMPLOYEE COUNT BY DEPARTMENT")

for department, count in department_counts.items():
    print(f"{department}: {count}")

print("\nTotal employee records:", len(employees))
