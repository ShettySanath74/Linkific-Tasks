
import csv
import math
from datetime import datetime
from pathlib import Path


def read_csv(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Required source file not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)

        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")

        return list(reader), set(reader.fieldnames)


def clean_text(value):
    return (value or "").strip()


def parse_date(value):
    value = clean_text(value)

    if not value:
        raise ValueError("order_date is required")

    return datetime.strptime(value, "%Y-%m-%d").date().isoformat()


def parse_timestamp(value):
    value = clean_text(value)

    if not value:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()


def parse_bool(value):
    value = clean_text(value).lower()

    if value in {"true", "1", "yes", "y"}:
        return True

    if value in {"false", "0", "no", "n", ""}:
        return False

    raise ValueError(f"Invalid boolean value: {value!r}")


def transform_sources(customers_path, products_path, sales_path):
    customers, _ = read_csv(customers_path)
    products, _ = read_csv(products_path)
    sales, _ = read_csv(sales_path)

    # Build customer lookup.
    customer_map = {}

    for row in customers:
        customer_id = clean_text(row.get("customer_id"))

        if customer_id:
            customer_map[customer_id] = {
                "customer_name": clean_text(row.get("customer_name")),
                "city": clean_text(row.get("city")),
            }

    # Build product lookup.
    product_map = {}

    for row in products:
        product_id = clean_text(row.get("product_id"))

        if product_id:
            product_map[product_id] = {
                "product_name": clean_text(row.get("product_name")),
                "category": clean_text(row.get("category")),
            }

    transformed = []
    rejects = []

    for row_number, row in enumerate(sales, start=2):
        try:
            order_id = clean_text(row.get("order_id"))
            line_number = int(clean_text(row.get("line_number")))
            customer_id = clean_text(row.get("customer_id"))
            product_id = clean_text(row.get("product_id"))

            if not order_id:
                raise ValueError("order_id is required")

            if line_number <= 0:
                raise ValueError("line_number must be greater than zero")

            customer = customer_map.get(customer_id)
            product = product_map.get(product_id)

            if customer is None:
                raise ValueError(f"Unknown customer_id: {customer_id}")

            if product is None:
                raise ValueError(f"Unknown product_id: {product_id}")

            quantity = int(clean_text(row.get("quantity")))
            unit_price = float(clean_text(row.get("unit_price")))

            if quantity <= 0:
                raise ValueError("quantity must be greater than zero")

            if not math.isfinite(unit_price) or unit_price < 0:
                raise ValueError("unit_price must be a valid non-negative number")

            order_date = parse_date(row.get("order_date"))

            # Day 24 does not contain these two fields.
            # Use safe defaults when they are absent.
            is_deleted = parse_bool(row.get("is_deleted"))
            source_updated_at = parse_timestamp(row.get("updated_at"))

            record = {
                "order_id": order_id,
                "line_number": line_number,
                "customer_id": customer_id,
                "customer_name": customer["customer_name"],
                "city": customer["city"],
                "product_id": product_id,
                "product_name": product["product_name"],
                "category": product["category"],
                "order_date": order_date,
                "quantity": quantity,
                "unit_price": unit_price,
                "revenue": round(quantity * unit_price, 2),
                "source_updated_at": source_updated_at,
                "is_deleted": int(is_deleted),
            }

            transformed.append(record)

        except (ValueError, TypeError) as exc:
            rejects.append({
                "source_row": row_number,
                "order_id": clean_text(row.get("order_id")),
                "line_number": clean_text(row.get("line_number")),
                "reason": str(exc),
            })

    return transformed, rejects


def aggregate_daily_category(records):
    totals = {}

    for row in records:
        if row["is_deleted"]:
            continue

        key = (row["order_date"], row["category"])

        item = totals.setdefault(
            key,
            {
                "order_date": key[0],
                "category": key[1],
                "orders": 0,
                "units": 0,
                "revenue": 0.0,
                "_order_ids": set(),
            },
        )

        # Count distinct orders, not individual sales lines.
        item["_order_ids"].add(row["order_id"])
        item["units"] += row["quantity"]
        item["revenue"] += row["revenue"]

    results = []

    for item in totals.values():
        item["orders"] = len(item["_order_ids"])
        item["revenue"] = round(item["revenue"], 2)
        del item["_order_ids"]
        results.append(item)

    return results
