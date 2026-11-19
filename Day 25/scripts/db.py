
import sqlite3
from .config import DATABASE_DIR, DATABASE_FILE


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS source_state (
    entity_type TEXT NOT NULL,
    record_id TEXT NOT NULL,
    row_hash TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    last_seen_at TEXT NOT NULL,
    PRIMARY KEY (entity_type, record_id)
);

CREATE TABLE IF NOT EXISTS pipeline_errors (
    error_id INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_at TEXT NOT NULL,
    stage TEXT NOT NULL,
    message TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    records_read INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    records_deleted INTEGER DEFAULT 0,
    records_rejected INTEGER DEFAULT 0,
    error_message TEXT
);
"""


TRANSFORMED_SALES_SCHEMA = """
CREATE TABLE IF NOT EXISTS transformed_sales (
    order_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    customer_id TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL,
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    order_date TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    revenue REAL NOT NULL CHECK(revenue >= 0),
    source_updated_at TEXT,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    loaded_at TEXT NOT NULL,
    PRIMARY KEY (order_id, line_number)
);
"""


def connect():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        conn.executescript(SCHEMA)

        # Check whether the existing table uses the old schema.
        table_info = conn.execute(
            "PRAGMA table_info(transformed_sales)"
        ).fetchall()

        columns = {row["name"] for row in table_info}

        if table_info and "line_number" not in columns:
            # Preserve existing records during the schema migration.
            conn.execute(
                "ALTER TABLE transformed_sales "
                "RENAME TO transformed_sales_legacy"
            )

            conn.execute(TRANSFORMED_SALES_SCHEMA)

            conn.execute("""
                INSERT INTO transformed_sales (
                    order_id, line_number,
                    customer_id, customer_name, city,
                    product_id, product_name, category,
                    order_date, quantity, unit_price, revenue,
                    source_updated_at, is_deleted, loaded_at
                )
                SELECT
                    order_id, 1,
                    customer_id, customer_name, city,
                    product_id, product_name, category,
                    order_date, quantity, unit_price, revenue,
                    source_updated_at, is_deleted, loaded_at
                FROM transformed_sales_legacy
            """)

            conn.execute("DROP TABLE transformed_sales_legacy")

        else:
            conn.execute(TRANSFORMED_SALES_SCHEMA)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_order_date
            ON transformed_sales(order_date)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_category
            ON transformed_sales(category)
        """)

        conn.commit()
        return conn

    except Exception:
        conn.rollback()
        conn.close()
        raise
