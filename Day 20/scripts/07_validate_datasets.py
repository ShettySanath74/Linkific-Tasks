import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

def load_json(filename):
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)

customers = load_json("customers.json")
products = load_json("products.json")
orders = load_json("orders.json")
order_items = load_json("order_items.json")
employees = load_json("employees.json")
transactions = load_json("financial_transactions.json")

customer_ids = {row["customer_id"] for row in customers}
product_ids = {row["product_id"] for row in products}
order_ids = {row["order_id"] for row in orders}
employee_ids = {row["employee_id"] for row in employees}

assert all(row["customer_id"] in customer_ids for row in orders)
assert all(row["order_id"] in order_ids for row in order_items)
assert all(row["product_id"] in product_ids for row in order_items)
assert all(
    row["manager_id"] is None or row["manager_id"] in employee_ids
    for row in employees
)
assert all(row["amount"] > 0 for row in transactions)

large_csv = OUTPUT_DIR / "financial_transactions_100k.csv"
with large_csv.open(newline="", encoding="utf-8") as file:
    large_count = sum(1 for _ in csv.DictReader(file))

assert large_count == 100_000, f"Expected 100,000 rows; found {large_count}"

print("Dataset validation passed.")
print(f"Customers: {len(customers)}")
print(f"Products: {len(products)}")
print(f"Orders: {len(orders)}")
print(f"Order items: {len(order_items)}")
print(f"Employees: {len(employees)}")
print(f"Financial transactions: {len(transactions)}")
print(f"Large CSV records: {large_count:,}")