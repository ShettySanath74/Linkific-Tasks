import csv
import random
from pathlib import Path
from faker import Faker

fake = Faker("en_US")
Faker.seed(20)
random.seed(20)

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

output_file = OUTPUT_DIR / "financial_transactions_100k.csv"
record_count = 100_000

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "transaction_id",
            "account_id",
            "transaction_date",
            "transaction_type",
            "amount",
            "currency",
            "merchant",
            "status",
        ],
    )
    writer.writeheader()

    for transaction_id in range(1, record_count + 1):
        writer.writerow({
            "transaction_id": transaction_id,
            "account_id": random.randint(10001, 20000),
            "transaction_date": fake.date_time_between(
                start_date="-1y",
                end_date="now",
            ).isoformat(),
            "transaction_type": random.choice(["credit", "debit"]),
            "amount": round(random.uniform(5, 5000), 2),
            "currency": random.choice(["USD", "EUR", "INR"]),
            "merchant": fake.company(),
            "status": random.choice(["completed", "pending", "failed"]),
        })

print(f"Generated {record_count:,} transactions.")
print(f"Saved to: {output_file}")