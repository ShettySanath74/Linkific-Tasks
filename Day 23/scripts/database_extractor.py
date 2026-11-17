import json
import sqlite3
from datetime import datetime, timezone
from config.settings import SOURCE_DB, STAGING_DIR, STATE_FILE
from scripts.common import get_logger, write_jsonl

logger = get_logger("database_extractor")

def initialize_source_database():
    SOURCE_DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(SOURCE_DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS source_orders (
            order_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            amount REAL NOT NULL,
            updated_at TEXT NOT NULL
        )''')
        count = conn.execute("SELECT COUNT(*) FROM source_orders").fetchone()[0]
        if count == 0:
            now = datetime.now(timezone.utc).isoformat()
            rows = [
                (1, "Asha", 1250.50, now),
                (2, "Rahul", 2400.00, now),
                (3, "Meera", 875.25, now),
            ]
            conn.executemany("INSERT INTO source_orders VALUES (?, ?, ?, ?)", rows)
        conn.commit()
    logger.info("Source SQLite database initialized at %s", SOURCE_DB)

def extract_incremental():
    initialize_source_database()
    state = json.loads(STATE_FILE.read_text(encoding="utf-8")) if STATE_FILE.exists() else {}
    last_id = int(state.get("source_orders_last_id", 0))
    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM source_orders WHERE order_id > ? ORDER BY order_id", (last_id,)
        ).fetchall()
    records = [dict(row) for row in rows]
    output = STAGING_DIR / "database" / "source_orders.jsonl"
    # Append newly extracted records so later incremental runs preserve prior raw batches.
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, default=str) + "\n")
    if records:
        state["source_orders_last_id"] = max(r["order_id"] for r in records)
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    logger.info("Database incremental extraction: %d new rows (watermark=%s)", len(records), state.get("source_orders_last_id", last_id))
    return len(records)

if __name__ == "__main__":
    print({"new_database_records": extract_incremental()})
