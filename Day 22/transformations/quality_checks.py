"""Starter data-quality checks for e-commerce order-line data."""
from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {
    "order_id", "order_item_id", "customer_id", "product_id",
    "quantity", "unit_price", "discount_amount"
}

def validate_order_items(df: pd.DataFrame) -> dict:
    """Return a compact quality report; does not modify the input DataFrame."""
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        return {
            "passed": False,
            "row_count": len(df),
            "missing_columns": missing_columns,
            "null_required_fields": {},
            "duplicate_source_lines": 0,
            "invalid_quantity_rows": 0,
            "invalid_price_rows": 0,
        }

    required = ["order_id", "order_item_id", "customer_id", "product_id", "quantity", "unit_price"]
    null_counts = df[required].isna().sum().astype(int).to_dict()
    duplicate_count = int(df.duplicated(["order_id", "order_item_id"]).sum())

    quantity = pd.to_numeric(df["quantity"], errors="coerce")
    price = pd.to_numeric(df["unit_price"], errors="coerce")
    discount = pd.to_numeric(df["discount_amount"], errors="coerce")

    invalid_quantity = int((quantity.isna() | (quantity <= 0)).sum())
    invalid_price = int((price.isna() | (price < 0)).sum())
    invalid_discount = int((discount.isna() | (discount < 0)).sum())

    passed = (
        not any(null_counts.values())
        and duplicate_count == 0
        and invalid_quantity == 0
        and invalid_price == 0
        and invalid_discount == 0
    )
    return {
        "passed": passed,
        "row_count": len(df),
        "missing_columns": [],
        "null_required_fields": null_counts,
        "duplicate_source_lines": duplicate_count,
        "invalid_quantity_rows": invalid_quantity,
        "invalid_price_rows": invalid_price,
        "invalid_discount_rows": invalid_discount,
    }
