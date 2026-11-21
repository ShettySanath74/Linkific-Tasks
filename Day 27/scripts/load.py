"""SQLite warehouse loading with idempotent upsert."""
import csv, sqlite3
from contextlib import closing
from pathlib import Path
from scripts.common import DATABASE_PATH, ensure_directories, get_logger
logger=get_logger(__name__)

def load_sales(transformed_csv, database_path=None, create_index=True):
    ensure_directories()
    src=Path(transformed_csv)
    if not src.exists(): raise FileNotFoundError(f"Transformed file not found: {src}")
    with src.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    db=Path(database_path) if database_path else DATABASE_PATH
    db.parent.mkdir(parents=True,exist_ok=True)
    # sqlite3 connection context managers commit/rollback but do not close.
    # closing() guarantees the file handle is released (important on Windows).
    with closing(sqlite3.connect(db)) as con:
      with con:
        con.execute("""CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL, customer_name TEXT,
            city TEXT, product TEXT, amount REAL NOT NULL CHECK(amount > 0), sale_date TEXT NOT NULL)""")
        con.executemany("""INSERT INTO sales VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(sale_id) DO UPDATE SET customer_id=excluded.customer_id,
            customer_name=excluded.customer_name, city=excluded.city, product=excluded.product,
            amount=excluded.amount, sale_date=excluded.sale_date""",
            [(r["sale_id"],r["customer_id"],r["customer_name"],r["city"],r["product"],float(r["amount"]),r["sale_date"]) for r in rows])
        if create_index: con.execute("CREATE INDEX IF NOT EXISTS idx_sales_customer_date ON sales(customer_id,sale_date)")
    logger.info("Loaded/upserted %d sales into %s",len(rows),db)
    return str(db)
