
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "files" / "employees.xml"
OUTPUT_DIR = BASE_DIR / "outputs" / "files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "employees_from_xml.csv"


def parse_xml():
    print("Reading XML file...")

    tree = ET.parse(INPUT_FILE)
    root = tree.getroot()

    employees = []

    for employee in root.findall("employee"):
        record = {
            "id": employee.findtext("id"),
            "name": employee.findtext("name"),
            "department": employee.findtext("department"),
            "salary": employee.findtext("salary")
        }

        employees.append(record)

    df = pd.DataFrame(employees)

    df["id"] = pd.to_numeric(df["id"])
    df["salary"] = pd.to_numeric(df["salary"])

    print("\nXML parsing successful!")
    print("Total employees:", len(df))
    print("\nExtracted records:")
    print(df)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCSV saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    parse_xml()
