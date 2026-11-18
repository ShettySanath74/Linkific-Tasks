import csv
from scripts.config import SALES_CSV, OUTPUT_DIR, get_connection

def validate():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with SALES_CSV.open(newline="", encoding="utf-8") as f:
        source_count = sum(1 for _ in csv.DictReader(f))
    checks = []
    with get_connection() as conn:
        fact_count = conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
        checks.append(("Source count equals fact count", source_count == fact_count, f"source={source_count}, fact={fact_count}"))
        fk = conn.execute("PRAGMA foreign_key_check").fetchall()
        checks.append(("Foreign key integrity", not fk, f"violations={len(fk)}"))
        missing = conn.execute("""
            SELECT COUNT(*) FROM fact_sales f
            LEFT JOIN dim_date d ON f.date_key=d.date_key
            LEFT JOIN dim_customer c ON f.customer_key=c.customer_key
            LEFT JOIN dim_product p ON f.product_key=p.product_key
            WHERE d.date_key IS NULL OR c.customer_key IS NULL OR p.product_key IS NULL
        """).fetchone()[0]
        checks.append(("All dimension lookups resolve", missing == 0, f"unresolved={missing}"))
        dup = conn.execute("""
            SELECT COUNT(*) FROM (SELECT order_id,line_number FROM fact_sales
            GROUP BY order_id,line_number HAVING COUNT(*)>1)
        """).fetchone()[0]
        checks.append(("No duplicate order lines", dup == 0, f"duplicate_groups={dup}"))
        invalid = conn.execute("""
            SELECT COUNT(*) FROM fact_sales
            WHERE quantity<=0 OR unit_price<0 OR ABS(sales_amount-quantity*unit_price)>0.001
        """).fetchone()[0]
        checks.append(("Measures valid", invalid == 0, f"invalid_rows={invalid}"))
        current = conn.execute("""
            SELECT COUNT(*) FROM (SELECT customer_id FROM dim_customer
            GROUP BY customer_id HAVING SUM(is_current)<>1)
        """).fetchone()[0]
        checks.append(("One current customer version per ID", current == 0, f"invalid_customers={current}"))
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ("dim_date","dim_customer","dim_product","fact_sales")}
    lines = ["DAY 24 DATA WAREHOUSE VALIDATION","="*36,"","TABLE COUNTS:"]
    lines += [f"{k}: {v}" for k,v in counts.items()]
    lines += ["","CHECK RESULTS:"]
    lines += [f"[{'PASS' if ok else 'FAIL'}] {name} | {detail}" for name,ok,detail in checks]
    passed = all(ok for _,ok,_ in checks)
    lines += ["",f"OVERALL STATUS: {'PASS' if passed else 'FAIL'}"]
    report = "\n".join(lines) + "\n"
    path = OUTPUT_DIR / "validation_report.txt"
    path.write_text(report, encoding="utf-8")
    print(report)
    print(f"Saved report: {path}")
    if not passed:
        raise SystemExit("Validation failed.")
    return True

if __name__ == "__main__":
    validate()
