
import json
from pathlib import Path
from fastavro import writer, reader, parse_schema

BASE_DIR = Path(__file__).resolve().parents[1]

OUTPUT_DIR = BASE_DIR / "outputs" / "files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AVRO_FILE = OUTPUT_DIR / "employees.avro"
JSON_FILE = OUTPUT_DIR / "employees_from_avro.json"

# Define Avro schema
schema = {
    "type": "record",
    "name": "Employee",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "department", "type": "string"},
        {"name": "salary", "type": "int"}
    ]
}

parsed_schema = parse_schema(schema)

# Sample employee records
employees = [
    {"id": 101, "name": "Rahul Sharma",
     "department": "Engineering", "salary": 45000},
    {"id": 102, "name": "Priya Nair",
     "department": "HR", "salary": 40000},
    {"id": 103, "name": "Arjun Kumar",
     "department": "Finance", "salary": 50000},
    {"id": 104, "name": "Ananya Rao",
     "department": "Engineering", "salary": 55000}
]


def convert_to_avro():
    print("Writing employee records to Avro...")

    with open(AVRO_FILE, "wb") as file:
        writer(file, parsed_schema, employees)

    print("Avro file created:", AVRO_FILE)

    print("\nReading Avro records...")

    restored_records = []

    with open(AVRO_FILE, "rb") as file:
        for record in reader(file):
            restored_records.append(record)

    print("Records restored:", len(restored_records))

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(restored_records, file, indent=4)

    print("\nRestored JSON created:", JSON_FILE)

    print("\nRestored employee records:")
    for employee in restored_records:
        print(employee)

    print("\nAvro conversion completed successfully!")


if __name__ == "__main__":
    convert_to_avro()
