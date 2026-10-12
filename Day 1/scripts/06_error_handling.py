
# Script 06: Error Handling in Python
# Linkific Data Engineering Internship

print("=== 1. Handling Invalid Numbers ===")

try:
    number = int("hello")
    print("Number:", number)
except ValueError:
    print("Error: The input cannot be converted to an integer.")


print("\n=== 2. Handling Division by Zero ===")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        return None

print("10 / 2 =", safe_divide(10, 2))
print("10 / 0 =", safe_divide(10, 0))


print("\n=== 3. Handling Missing Files ===")

filename = "data/missing_file.csv"

try:
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"Error: '{filename}' does not exist.")
    print("Please check the file path.")


print("\n=== 4. Using try, except, else, finally ===")

try:
    value = int("250")
except ValueError:
    print("Conversion failed.")
else:
    print("Conversion successful:", value)
finally:
    print("Conversion attempt completed.")


print("\n=== 5. Processing Data Records Safely ===")

records = [
    {"employee_id": 101, "salary": "45000"},
    {"employee_id": 102, "salary": "invalid"},
    {"employee_id": 103, "salary": "52000"},
    {"employee_id": 104, "salary": None},
]

valid_records = []
failed_records = []

for record in records:
    try:
        salary = float(record["salary"])

        if salary < 0:
            raise ValueError("Salary cannot be negative.")

        cleaned_record = {
            "employee_id": record["employee_id"],
            "salary": salary,
        }

        valid_records.append(cleaned_record)

    except (ValueError, TypeError) as error:
        failed_records.append({
            "employee_id": record["employee_id"],
            "error": str(error),
        })

print("Valid records:")
for record in valid_records:
    print(record)

print("\nFailed records:")
for record in failed_records:
    print(record)

print("\nValid record count:", len(valid_records))
print("Failed record count:", len(failed_records))


print("\n=== 6. Raising Your Own Error ===")

def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return age

try:
    print("Validated age:", validate_age(-5))
except ValueError as error:
    print("Validation error:", error)


print("\n=== Script Completed ===")
