import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

def load_json(filename):
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)

customers = load_json("customers.json")
products = load_json("products.json")
orders = load_json("orders.json")

product_by_id = {product["product_id"]: product for product in products}

order_items = []
for order in orders:
    item_count = (order["order_id"] % 3) + 1

    for item_number in range(1, item_count + 1):
        product = products[(order["order_id"] + item_number) % len(products)]
        quantity = (item_number % 3) + 1

        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order["order_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": product["price"],
            "line_total": round(quantity * product["price"], 2),
        })

# Validate all foreign-key references
customer_ids = {customer["customer_id"] for customer in customers}
order_ids = {order["order_id"] for order in orders}
product_ids = set(product_by_id)

assert all(order["customer_id"] in customer_ids for order in orders)
assert all(item["order_id"] in order_ids for item in order_items)
assert all(item["product_id"] in product_ids for item in order_items)

with (DATA_DIR / "order_items.json").open("w", encoding="utf-8") as file:
    json.dump(order_items, file, indent=2)

print(f"Order items generated: {len(order_items)}")
print("Validation passed: all order and product references are valid.")