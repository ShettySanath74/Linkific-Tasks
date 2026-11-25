"""Display SQLite EXPLAIN QUERY PLAN output for a supplied read-only SQL query."""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, help="Path to SQLite database")
    parser.add_argument("--sql", required=True, help="Single SQL SELECT statement")
    args = parser.parse_args()

    sql = args.sql.strip().rstrip(";")
    if not sql.lower().startswith("select"):
        parser.error("Only SELECT statements are accepted by this helper.")

    db_path = Path(args.database).resolve()
    if not db_path.is_file():
        parser.error(f"Database not found: {db_path}")

    # URI mode=ro prevents accidental database modification.
    uri = db_path.as_uri() + "?mode=ro"
    try:
        with sqlite3.connect(uri, uri=True) as connection:
            rows = connection.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
    except sqlite3.Error as exc:
        print(f"SQLite error: {exc}")
        return 1

    print(f"Query plan for: {sql}")
    for row in rows:
        print(" | ".join(str(value) for value in row))
    print("\nNote: a query plan describes the chosen strategy; benchmark execution time separately.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
