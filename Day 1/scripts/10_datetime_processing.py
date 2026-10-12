
# Script 10: Date and Time Processing
# Linkific Data Engineering Internship

from datetime import date, datetime, timedelta
from pathlib import Path
import json

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=== 1. Current Date and Time ===")

now = datetime.now()

print("Current date and time:", now)
print("Current date:", now.date())
print("Current time:", now.strftime("%H:%M:%S"))


print("\n=== 2. Formatting Dates ===")

sample_date = datetime(2026, 10, 12, 14, 30, 0)

print("Original datetime:", sample_date)
print("DD-MM-YYYY:", sample_date.strftime("%d-%m-%Y"))
print("YYYY-MM-DD:", sample_date.strftime("%Y-%m-%d"))
print("Readable date:", sample_date.strftime("%d %B %Y"))
print("Time:", sample_date.strftime("%H:%M:%S"))


print("\n=== 3. Converting Text into a Date ===")

date_text = "12-10-2026"

parsed_date = datetime.strptime(
    date_text, "%d-%m-%Y"
)

print("Original text:", date_text)
print("Parsed date:", parsed_date.date())


print("\n=== 4. Calculating Date Differences ===")

start_date = date(2026, 10, 1)
end_date = date(2026, 10, 12)

difference = end_date - start_date

print("Start date:", start_date)
print("End date:", end_date)
print("Difference in days:", difference.days)


print("\n=== 5. Adding and Subtracting Days ===")

today_example = date(2026, 10, 12)

next_week = today_example + timedelta(days=7)
previous_week = today_example - timedelta(days=7)

print("Example date:", today_example)
print("Seven days later:", next_week)
print("Seven days earlier:", previous_week)


print("\n=== 6. Processing Transaction Dates ===")

transactions = [
    {"id": 1, "amount": 1500, "date": "2026-10-10"},
    {"id": 2, "amount": 2500, "date": "2026-10-12"},
    {"id": 3, "amount": 1800, "date": "2026-10-15"},
    {"id": 4, "amount": 3200, "date": "2026-10-20"},
]

for transaction in transactions:
    transaction["date"] = datetime.strptime(
        transaction["date"], "%Y-%m-%d"
    ).date()

    print(
        "Transaction:", transaction["id"],
        "| Amount:", transaction["amount"],
        "| Date:", transaction["date"]
    )


print("\n=== 7. Filtering Transactions by Date ===")

filter_start = date(2026, 10, 11)
filter_end = date(2026, 10, 15)

filtered_transactions = [
    transaction
    for transaction in transactions
    if filter_start <= transaction["date"] <= filter_end
]

for transaction in filtered_transactions:
    print(transaction)

print("Transactions found:", len(filtered_transactions))


print("\n=== 8. Calculating Total for Filtered Transactions ===")

total_amount = sum(
    transaction["amount"]
    for transaction in filtered_transactions
)

print("Total transaction amount:", total_amount)


print("\n=== 9. Saving Date-Processed Data as JSON ===")

output_file = OUTPUT_DIR / "date_processed_transactions.json"

# JSON cannot directly serialize Python date objects.
# Convert dates back to strings before writing.
export_data = [
    {
        "id": transaction["id"],
        "amount": transaction["amount"],
        "date": transaction["date"].isoformat()
    }
    for transaction in filtered_transactions
]

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(export_data, file, indent=4)

print("Saved to:", output_file)


print("\n=== Script Completed ===")
