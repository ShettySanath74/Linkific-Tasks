from pathlib import Path
import sqlite3
BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR / "data" / "source"
OUTPUT_DIR = BASE_DIR / "outputs"
DB_PATH = BASE_DIR / "database" / "warehouse.db"
CUSTOMERS_CSV = SOURCE_DIR / "customers.csv"
PRODUCTS_CSV = SOURCE_DIR / "products.csv"
SALES_CSV = SOURCE_DIR / "sales.csv"
SCHEMA_SQL = BASE_DIR / "sql" / "create_schema.sql"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
