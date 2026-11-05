from faker import Faker
import json
from pathlib import Path

fake = Faker("en_US")

def generate_customer(customer_id: int) -> dict:
    return {
        "customer_id": customer_id,
        "full_name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
        "address": fake.address().replace("\n", ", "),
        "city": fake.city(),
        "company": fake.company(),
        "created_at": fake.date_time_between(
            start_date="-2y",
            end_date="now"
        ).isoformat()
    }

customers = [generate_customer(i) for i in range(1, 11)]

output_path = Path(__file__).resolve().parents[1] / "data" / "customers.json"
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as file:
    json.dump(customers, file, indent=2)

print(f"Generated {len(customers)} customers.")
print(f"Saved to: {output_path}")