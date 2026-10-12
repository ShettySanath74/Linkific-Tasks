
# Linkific Internship - Lists, Tuples and Sets

# 1. List: ordered and mutable
employees = ["Asha", "Rahul", "Priya", "Rahul"]
employees.append("Kiran")

print("Employee list:", employees)
print("First employee:", employees[0])

# 2. Tuple: ordered and immutable
database_config = ("localhost", 5432, "analytics")

print("\nDatabase configuration:", database_config)
print("Database host:", database_config[0])

# 3. Set: stores unique values
unique_employees = set(employees)

print("\nUnique employees:", unique_employees)
print("Number of unique employees:", len(unique_employees))

# 4. Practical data engineering example
raw_ids = [101, 102, 101, 103, 102, 104]
clean_ids = sorted(set(raw_ids))

print("\nRaw record IDs:", raw_ids)
print("Deduplicated record IDs:", clean_ids)
