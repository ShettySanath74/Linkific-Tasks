
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_DIR = PROJECT_ROOT.parent / "Day 24" / "data" / "source"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATABASE_DIR = PROJECT_ROOT / "database"
LOG_DIR = PROJECT_ROOT / "logs"

CUSTOMERS_FILE = SOURCE_DIR / "customers.csv"
PRODUCTS_FILE = SOURCE_DIR / "products.csv"
SALES_FILE = SOURCE_DIR / "sales.csv"

DATABASE_FILE = DATABASE_DIR / "day25_warehouse.db"

# Required columns based on the actual Day 24 source files.
REQUIRED_CUSTOMER_COLUMNS = {
    "customer_id",
    "customer_name",
    "city",
    "updated_at",
}

REQUIRED_PRODUCT_COLUMNS = {
    "product_id",
    "product_name",
    "category",
}

REQUIRED_SALES_COLUMNS = {
    "order_id",
    "line_number",
    "order_date",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
}

