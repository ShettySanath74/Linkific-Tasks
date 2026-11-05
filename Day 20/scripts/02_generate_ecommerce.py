import json
import random
from pathlib import Path
from faker import Faker

fake = Faker("en_US")
random.seed(20)
Faker.seed(20)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Generate customers
customers = [
    {
        "customer_id": customer_id,
        "name": fake.name(),
        "email": fake.unique.email(),
        "city": fake.city(),
    }
    for customer_id in range(1, 101)
]

# Generate product catalog
products = [
    {
        "product_id": product_id,
        "name": fake.catch_phrase(),
        "category": random.choice(
            ["Electronics", "Home", "Books", "Clothing"]
        ),
        "price": round(random.uniform(5, 500), 2),
    }
    for product_id in range(1, 31)
]

# Generate orders using valid customer IDs
orders = []
for order_id in range(1, 501):
    customer = random.choice(customers)
    order_date = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    orders.append({
        "order_id": order_id,
        "customer_id": customer["customer_id"],
        "order_date": order_date.isoformat(),
        "status": random.choice(
            ["pending", "processing", "shipped", "delivered"]
        ),
        "total": round(random.uniform(10, 1500), 2),
    })

# Save datasets
for filename, records in [
    ("customers.json", customers),
    ("products.json", products),
    ("orders.json", orders),
]:
    with (DATA_DIR / filename).open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)

# Validate relationships
customer_ids = {customer["customer_id"] for customer in customers}
assert all(order["customer_id"] in customer_ids for order in orders)

print(f"Customers: {len(customers)}")
print(f"Products: {len(products)}")
print(f"Orders: {len(orders)}")
print("Validation passed: every order references an existing customer.")
