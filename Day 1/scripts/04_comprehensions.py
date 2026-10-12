

# --------------------------------------------------
# 1. NORMAL LOOP: Calculate squares
# --------------------------------------------------

numbers = [1, 2, 3, 4, 5]

squares_loop = []

for number in numbers:
    squares_loop.append(number ** 2)

print("1. Squares using a normal loop:")
print(squares_loop)


# --------------------------------------------------
# 2. LIST COMPREHENSION: Calculate squares
# --------------------------------------------------

squares_comprehension = [
    number ** 2 for number in numbers
]

print("\n2. Squares using a comprehension:")
print(squares_comprehension)


# --------------------------------------------------
# 3. FILTER DATA: Find even numbers
# --------------------------------------------------

values = [10, 15, 20, 25, 30, 35, 40]

even_numbers = [
    value for value in values
    if value % 2 == 0
]

print("\n3. Even numbers:")
print(even_numbers)


# --------------------------------------------------
# 4. TRANSFORM AND FILTER DATA
# Keep even numbers and calculate their squares
# --------------------------------------------------

even_squares = [
    value ** 2 for value in values
    if value % 2 == 0
]

print("\n4. Squares of even numbers:")
print(even_squares)


# --------------------------------------------------
# 5. STRING PROCESSING
# Remove leading/trailing spaces and convert to uppercase
# --------------------------------------------------

raw_names = [" asha ", "rahul", " PRIYA ", "kiran"]

clean_names = [
    name.strip().upper() for name in raw_names
]

print("\n5. Cleaned employee names:")
print(clean_names)


# --------------------------------------------------
# 6. DICTIONARY COMPREHENSION
# Map each number to its square
# --------------------------------------------------

number_squares = {
    number: number ** 2 for number in range(1, 6)
}

print("\n6. Number-to-square dictionary:")
print(number_squares)


# --------------------------------------------------
# 7. DATA ENGINEERING EXAMPLE
# Extract employee IDs and names from records
# --------------------------------------------------

employees = [
    {"id": 101, "name": "Asha", "department": "Data Engineering"},
    {"id": 102, "name": "Rahul", "department": "Analytics"},
    {"id": 103, "name": "Priya", "department": "Data Engineering"},
    {"id": 104, "name": "Kiran", "department": "Analytics"}
]

employee_names = {
    employee["id"]: employee["name"]
    for employee in employees
}

print("\n7. Employee ID-to-name mapping:")
print(employee_names)


# --------------------------------------------------
# 8. FILTER EMPLOYEES BY DEPARTMENT
# --------------------------------------------------

data_engineers = [
    employee["name"]
    for employee in employees
    if employee["department"] == "Data Engineering"
]

print("\n8. Data Engineering employees:")
print(data_engineers)
