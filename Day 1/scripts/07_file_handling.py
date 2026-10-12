
# Script 07: File Handling in Python
# Linkific Data Engineering Internship

from pathlib import Path

# Project root: python-data-engineering
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

# Create folders if they do not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

input_file = DATA_DIR / "employees.txt"
output_file = OUTPUT_DIR / "processed_employees.txt"
log_file = OUTPUT_DIR / "processing_log.txt"

print("=== 1. Writing to a File ===")

# Create a sample input file
with open(input_file, "w", encoding="utf-8") as file:
    file.write("101, Asha, Data Engineering\n")
    file.write("102, Rahul, Software Engineering\n")
    file.write("103, Priya, Data Engineering\n")

print("Sample input file created:", input_file)


print("\n=== 2. Reading the Entire File ===")

with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

print(content)


print("=== 3. Reading One Line at a Time ===")

with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())


print("\n=== 4. Processing and Saving Records ===")

processed_records = []

with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        parts = line.split(",")

        if len(parts) != 3:
            print("Skipping invalid record:", line)
            continue

        employee_id = parts[0].strip()
        name = parts[1].strip().upper()
        department = parts[2].strip()

        processed_records.append(
            f"{employee_id}, {name}, {department}"
        )

with open(output_file, "w", encoding="utf-8") as file:
    for record in processed_records:
        file.write(record + "\n")

print("Processed records saved to:", output_file)

for record in processed_records:
    print(record)


print("\n=== 5. Appending to a File ===")

with open(log_file, "a", encoding="utf-8") as file:
    file.write("Employee file processed successfully.\n")

print("Processing message appended to:", log_file)


print("\n=== 6. Reading the Saved Output ===")

with open(output_file, "r", encoding="utf-8") as file:
    saved_content = file.read()

print(saved_content)


print("=== 7. Handling a Missing File ===")

missing_file = DATA_DIR / "missing.txt"

try:
    with open(missing_file, "r", encoding="utf-8") as file:
        print(file.read())
except FileNotFoundError:
    print("Error: File not found:", missing_file)


print("\n=== Script Completed ===")
