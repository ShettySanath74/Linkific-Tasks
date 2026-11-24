import sqlite3
import shutil
import re
import time
import statistics
import json
from pathlib import Path
from datetime import datetime, timezone

source_db = Path("Day 28/data/sales_analytics.db")
sql_file = Path("Day 28/sql/analytical_queries.sql")
output_dir = Path("Day 29/outputs")
test_db = output_dir / "sales_analytics_optimization_test.db"
report_file = output_dir / "sql_optimization_report.json"

output_dir.mkdir(parents=True, exist_ok=True)

if not source_db.exists() or not sql_file.exists():
    raise FileNotFoundError("Source database or SQL file not found.")

shutil.copy2(source_db, test_db)

content = sql_file.read_text(encoding="utf-8")
content = re.sub(r"--.*", "", content)

queries = [q.strip() for q in content.split(";") if q.strip()]

def benchmark(cursor, query):
    cursor.execute(query)
    cursor.fetchall()

    timings = []
    for _ in range(5):
        start = time.perf_counter()
        cursor.execute(query)
        cursor.fetchall()
        timings.append(time.perf_counter() - start)

    return statistics.mean(timings)

indexes = [
    ("idx_orders_status_date",
     "CREATE INDEX idx_orders_status_date ON orders(order_status, order_date)"),
    ("idx_orders_status_customer",
     "CREATE INDEX idx_orders_status_customer ON orders(order_status, customer_id)"),
    ("idx_order_items_order",
     "CREATE INDEX idx_order_items_order ON order_items(order_id)"),
    ("idx_order_items_product",
     "CREATE INDEX idx_order_items_product ON order_items(product_id)"),
    ("idx_customers_customer",
     "CREATE INDEX idx_customers_customer ON customers(customer_id)"),
    ("idx_products_product",
     "CREATE INDEX idx_products_product ON products(product_id)")
]

conn = sqlite3.connect(test_db)
cursor = conn.cursor()

baseline = []
optimized = []

try:
    print("Measuring baseline on database copy...")
    for i, query in enumerate(queries, 1):
        baseline.append(benchmark(cursor, query))
        print(f"Baseline query {i:02}: {baseline[-1]:.6f} sec")

    print("\nCreating indexes...")
    for name, statement in indexes:
        cursor.execute(statement)
        print("Created:", name)

    conn.commit()
    cursor.execute("PRAGMA optimize")

    print("\nMeasuring optimized queries...")
    for i, query in enumerate(queries, 1):
        optimized.append(benchmark(cursor, query))
        print(f"Optimized query {i:02}: {optimized[-1]:.6f} sec")

    results = []
    for i, (before, after) in enumerate(zip(baseline, optimized), 1):
        improvement = (
            ((before - after) / before) * 100 if before > 0 else 0
        )
        results.append({
            "query": i,
            "baseline_seconds": round(before, 6),
            "optimized_seconds": round(after, 6),
            "improvement_percent": round(improvement, 2)
        })

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Five-run average after one warm-up; same database copy",
        "source_database": str(source_db),
        "test_database": str(test_db),
        "indexes_created": [name for name, _ in indexes],
        "results": results
    }

    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\nOptimization report:", report_file)
    print("Test database:", test_db)

finally:
    conn.close()
