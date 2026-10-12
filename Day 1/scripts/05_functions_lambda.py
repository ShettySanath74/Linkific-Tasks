
# Script 05: Functions and Lambda Functions
# Linkific Data Engineering Internship

print("=== 1. Basic Function ===")

def greet(name):
    return f"Hello, {name}!"

message = greet("Sanath")
print(message)


print("\n=== 2. Data Cleaning Function ===")

def clean_name(name):
    """Remove extra spaces and convert a name to uppercase."""
    return name.strip().upper()

raw_names = ["  sanath ", " ASHA", "rahul  ", "  priya  "]

cleaned_names = []

for name in raw_names:
    cleaned_names.append(clean_name(name))

print("Original names:", raw_names)
print("Cleaned names:", cleaned_names)


print("\n=== 3. Function with Multiple Parameters ===")

def calculate_total(price, quantity):
    return price * quantity

total = calculate_total(250, 4)
print("Total order value:", total)


print("\n=== 4. Function with a Default Parameter ===")

def calculate_tax(amount, rate=0.18):
    return amount * rate

print("Default tax (18%):", calculate_tax(1000))
print("Custom tax (5%):", calculate_tax(1000, 0.05))


print("\n=== 5. Lambda Function ===")

square = lambda number: number * number

print("Square of 5:", square(5))


print("\n=== 6. Data Engineering Example ===")

employees = [
    {"id": 101, "name": "Asha", "salary": 45000},
    {"id": 102, "name": "Rahul", "salary": 38000},
    {"id": 103, "name": "Priya", "salary": 52000},
]

def get_annual_salary(employee):
    return employee["salary"] * 12

for employee in employees:
    annual_salary = get_annual_salary(employee)
    print(employee["name"], "-> Annual salary:", annual_salary)


print("\n=== 7. Sort Data Using Lambda ===")

numbers = [45, 12, 89, 23, 5]

sorted_numbers = sorted(numbers, key=lambda number: number)

print("Original numbers:", numbers)
print("Sorted numbers:", sorted_numbers)


print("\n=== 8. Filter Records Using a Function ===")

def is_high_salary(employee):
    return employee["salary"] >= 45000

high_salary_employees = list(
    filter(is_high_salary, employees)
)

print("Employees with salary >= 45000:")
for employee in high_salary_employees:
    print(employee["name"], "-", employee["salary"])
