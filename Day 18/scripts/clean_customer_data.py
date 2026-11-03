import csv
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "customers.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "cleaned_customers.csv"

EMAIL_PATTERN = re.compile(
    r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"
)
PHONE_PATTERN = re.compile(r"\D")
SPECIAL_CHARACTERS = re.compile(r"[^A-Za-z0-9 ]")
WHITESPACE_PATTERN = re.compile(r"\s+")

DATE_FORMATS = ("%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y")


def clean_name(value):
    value = SPECIAL_CHARACTERS.sub("", value)
    return WHITESPACE_PATTERN.sub(" ", value).strip()


def clean_email(value):
    value = value.strip().lower()
    return value if EMAIL_PATTERN.fullmatch(value) else ""


def clean_phone(value):
    digits = PHONE_PATTERN.sub("", value)

    # Remove India's country code when the number has 12 digits.
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]

    # Keep only valid-looking 10-digit Indian mobile numbers.
    if len(digits) == 10 and digits[0] in "6789":
        return digits

    return ""


def standardize_date(value):
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), date_format).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return ""


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as source:
        rows = csv.DictReader(source)
        cleaned_rows = []

        for row in rows:
            cleaned_rows.append({
                "customer_id": row["customer_id"].strip(),
                "name": clean_name(row["name"]),
                "email": clean_email(row["email"]),
                "phone": clean_phone(row["phone"]),
                "join_date": standardize_date(row["join_date"]),
            })

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as destination:
        fieldnames = ["customer_id", "name", "email", "phone", "join_date"]
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Processed {len(cleaned_rows)} customer records.")
    print(f"Cleaned data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()