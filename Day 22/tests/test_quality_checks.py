import pandas as pd
from transformations.quality_checks import validate_order_items

def test_valid_order_items_pass():
    df = pd.DataFrame([{
        "order_id": "O100", "order_item_id": "1", "customer_id": "C1",
        "product_id": "P1", "quantity": 2, "unit_price": 50.0,
        "discount_amount": 5.0
    }])
    assert validate_order_items(df)["passed"] is True

def test_duplicate_order_lines_fail():
    row = {
        "order_id": "O100", "order_item_id": "1", "customer_id": "C1",
        "product_id": "P1", "quantity": 2, "unit_price": 50.0,
        "discount_amount": 0.0
    }
    assert validate_order_items(pd.DataFrame([row, row]))["passed"] is False
