import json
import random
from pathlib import Path
from faker import Faker

fake = Faker("en_US")
random.seed(20)
Faker.seed(20)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

transactions = []
for transaction_id in range(1, 1001):
    transactions.append({
        "transaction_id": transaction_id,
        "account_id": random.randint(10001, 10200),
        "transaction_date": fake.date_time_between(
            start_date="-1y",
            end_date="now"
        ).isoformat(),
        "transaction_type": random.choice(["credit", "debit"]),
        "amount": round(random.uniform(5, 5000), 2),
        "currency": random.choice(["USD", "EUR", "INR"]),
        "merchant": fake.company(),
        "status": random.choice(["completed", "pending", "failed"]),
    })

with (DATA_DIR / "financial_transactions.json").open(
    "w", encoding="utf-8"
) as file:
    json.dump(transactions, file, indent=2)

assert len(transactions) == 1000
assert all(transaction["amount"] > 0 for transaction in transactions)

print(f"Financial transactions generated: {len(transactions)}")
print("Validation passed: amounts are positive.")