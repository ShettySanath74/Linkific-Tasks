"""Compare sequential and thread-parallel independent row validation."""
import csv, time, json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from scripts.common import PROJECT_ROOT
from scripts.generate_test_data import generate
from scripts.transform import validate_sale

def run_parallel_comparison(size=10000):
    src=generate(size)
    with src.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    customer_ids={f"C{i:05d}" for i in range(1,101)}
    def validate_chunk(chunk):
        seen=set(); valid=0
        for row in chunk:
            # Unique IDs are guaranteed by generator; seen is local to each chunk.
            if not validate_sale(row,customer_ids,seen): valid+=1
            if row.get("sale_id"): seen.add(row["sale_id"])
        return valid
    t=time.perf_counter(); sequential=validate_chunk(rows); seq=time.perf_counter()-t
    chunks=[rows[i::4] for i in range(4)]
    t=time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool: parallel=sum(pool.map(validate_chunk,chunks))
    par=time.perf_counter()-t
    result={"records":size,"sequential_validated":sequential,"parallel_validated":parallel,
            "sequential_seconds":round(seq,5),"parallel_seconds":round(par,5),
            "parallel_speedup":round(seq/par,3) if par else None,
            "note":"Threading is an experiment; Python's GIL and small workloads can make it slower. Results must be measured."}
    out=PROJECT_ROOT/"outputs"/"performance"; out.mkdir(parents=True,exist_ok=True)
    (out/"parallel_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(result); return result

if __name__=="__main__": run_parallel_comparison()
