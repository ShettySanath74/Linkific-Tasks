"""Batch-aware post-load quality checks."""
import csv, json, sqlite3
from contextlib import closing
from pathlib import Path
from scripts.common import DATABASE_PATH, OUTPUT_DIR, ensure_directories, get_logger
logger=get_logger(__name__)

def run_quality_checks(transformed_csv, database_path=None):
    ensure_directories(); db=Path(database_path) if database_path else DATABASE_PATH
    with Path(transformed_csv).open(newline="",encoding="utf-8") as f: expected=list(csv.DictReader(f))
    ids=[r["sale_id"] for r in expected]
    # Explicitly close the SQLite handle; its context manager alone only commits.
    with closing(sqlite3.connect(db)) as con:
      with con:
        total=con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        duplicates=con.execute("SELECT COUNT(*) FROM (SELECT sale_id FROM sales GROUP BY sale_id HAVING COUNT(*)>1)").fetchone()[0]
        invalid=con.execute("SELECT COUNT(*) FROM sales WHERE amount<=0 OR amount IS NULL").fetchone()[0]
        missing=con.execute("SELECT COUNT(*) FROM sales WHERE customer_id IS NULL OR TRIM(customer_id)=''").fetchone()[0]
        missing_batch=sum(con.execute("SELECT COUNT(*) FROM sales WHERE sale_id=?",(sid,)).fetchone()[0]==0 for sid in ids)
    checks={"all_batch_records_loaded":missing_batch==0,"no_duplicate_sale_ids":duplicates==0,
            "all_amounts_positive":invalid==0,"customer_ids_present":missing==0}
    result={"status":"PASSED" if all(checks.values()) else "FAILED","expected_records_in_current_batch":len(expected),
            "warehouse_total_records":total,"missing_batch_records":missing_batch,"duplicate_sale_ids":duplicates,
            "invalid_amounts":invalid,"missing_customer_ids":missing,"checks":checks}
    path=OUTPUT_DIR/"quality_report.json"; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2),encoding="utf-8")
    logger.info("Quality checks %s: %s",result["status"],checks)
    if result["status"]!="PASSED": raise ValueError(f"Data quality checks failed: {result}")
    return str(path)
