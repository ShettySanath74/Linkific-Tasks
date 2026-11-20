"""Enrich sales with customer details and separate invalid records."""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

from scripts.common import (
    TRANSFORM_DIR, DEAD_LETTER_DIR, ensure_directories, get_logger
)

logger = get_logger(__name__)

OUTPUT_FIELDS = [
    "sale_id", "customer_id", "customer_name", "city",
    "product", "amount", "sale_date"
]
DEAD_LETTER_FIELDS = ["sale_id", "customer_id", "product", "amount", "sale_date", "reason"]


def transform_records(customers_json: str, sales_json: str) -> str:
    """Validate sales and enrich valid rows with customer attributes."""
    ensure_directories()

    with Path(customers_json).open(encoding="utf-8") as file:
        customers = json.load(file)
    with Path(sales_json).open(encoding="utf-8") as file:
        sales = json.load(file)

    customer_lookup = {
        customer["customer_id"].strip(): customer for customer in customers
        if customer.get("customer_id")
    }

    accepted = []
    rejected = []
    seen_sale_ids = set()

    for sale in sales:
        sale_id = (sale.get("sale_id") or "").strip()
        customer_id = (sale.get("customer_id") or "").strip()
        amount_text = (sale.get("amount") or "").strip()
        sale_date = (sale.get("sale_date") or "").strip()
        reason = ""

        if not sale_id:
            reason = "Missing sale_id"
        elif sale_id in seen_sale_ids:
            reason = "Duplicate sale_id"
        elif customer_id not in customer_lookup:
            reason = "Customer reference not found"
        else:
            try:
                amount = float(amount_text)
                if amount <= 0:
                    reason = "Amount must be greater than zero"
            except (TypeError, ValueError):
                reason = "Amount is not numeric"

            if not reason:
                try:
                    date.fromisoformat(sale_date)
                except ValueError:
                    reason = "sale_date must use YYYY-MM-DD format"

        if sale_id:
            seen_sale_ids.add(sale_id)

        if reason:
            rejected.append({
                "sale_id": sale_id,
                "customer_id": customer_id,
                "product": sale.get("product", ""),
                "amount": amount_text,
                "sale_date": sale_date,
                "reason": reason,
            })
            continue

        customer = customer_lookup[customer_id]
        accepted.append({
            "sale_id": sale_id,
            "customer_id": customer_id,
            "customer_name": customer.get("name", ""),
            "city": customer.get("city", ""),
            "product": (sale.get("product") or "").strip(),
            "amount": float(amount_text),
            "sale_date": sale_date,
        })

    accepted_path = TRANSFORM_DIR / "accepted_sales.csv"
    with accepted_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(accepted)

    dead_letter_path = DEAD_LETTER_DIR / "rejected_sales.csv"
    with dead_letter_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=DEAD_LETTER_FIELDS)
        writer.writeheader()
        writer.writerows(rejected)

    logger.info(
        "Transformation complete: %d accepted, %d rejected",
        len(accepted), len(rejected)
    )
    return str(accepted_path)
