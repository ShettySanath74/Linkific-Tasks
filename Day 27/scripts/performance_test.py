"""Measure load throughput and indexed query latency on generated test data."""
import csv, json, sqlite3, time
from pathlib import Path
from scripts.common import PROJECT_ROOT
from scripts.generate_test_data import generate
from scripts.extract import extract_csv_to_json
from scripts.transform import transform_records
from scripts.load import load_sales

def run_benchmarks():
    out=PROJECT_ROOT/"outputs"/"performance"; out.mkdir(parents=True,exist_ok=True)
    results=[]
    for size in (1000,10000,100000):
        src=generate(size)
        # Benchmark the full Python ETL path with isolated files/database per size.
        cust=PROJECT_ROOT/"data/test_data/customers.csv"
        cjson=out/f"customers_{size}.json"; sjson=out/f"sales_{size}.json"
        accepted=out/f"accepted_{size}.csv"; rejected=out/f"rejected_{size}.csv"; db=out/f"bench_{size}.db"
        t0=time.perf_counter()
        extract_csv_to_json(cust,cjson); extract_csv_to_json(src,sjson)
        transform_records(cjson,sjson,accepted,rejected)
        load_sales(accepted,db)
        elapsed=time.perf_counter()-t0
        with accepted.open(newline="",encoding="utf-8") as f: accepted_count=sum(1 for _ in csv.DictReader(f))
        throughput=round(size/elapsed,2) if elapsed else None
        with sqlite3.connect(db) as con:
            q0=time.perf_counter()
            con.execute("SELECT COUNT(*) FROM sales WHERE customer_id=? AND sale_date>=?",("C00001","2026-01-01")).fetchone()
            indexed_ms=(time.perf_counter()-q0)*1000
            plan=" ".join(str(x) for row in con.execute("EXPLAIN QUERY PLAN SELECT * FROM sales WHERE customer_id=? AND sale_date>=?",("C00001","2026-01-01")) for x in row)
            con.execute("DROP INDEX IF EXISTS idx_sales_customer_date")
            q0=time.perf_counter()
            con.execute("SELECT COUNT(*) FROM sales WHERE customer_id=? AND sale_date>=?",("C00001","2026-01-01")).fetchone()
            unindexed_ms=(time.perf_counter()-q0)*1000
        results.append({"input_records":size,"accepted_records":accepted_count,"rejected_records":size-accepted_count,
            "elapsed_seconds":round(elapsed,4),"records_per_second":throughput,
            "indexed_query_ms":round(indexed_ms,4),"unindexed_query_ms":round(unindexed_ms,4),
            "query_plan_with_index":plan})
        print(f"{size:,} rows: {elapsed:.2f}s | {throughput:,.0f} input rows/sec | accepted {accepted_count:,}")
    report={"note":"Measurements are from this machine/run; compare repeated runs before drawing conclusions.","results":results}
    (out/"performance_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    with (out/"performance_report.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=results[0].keys()); w.writeheader(); w.writerows(results)
    return report
if __name__=="__main__": run_benchmarks()
