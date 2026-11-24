"""Measure basic CSV read time and file characteristics."""
import argparse, csv, json, time
from pathlib import Path
from datetime import datetime, timezone

def benchmark(path: Path) -> dict:
    start = time.perf_counter()
    rows = 0
    columns = 0
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            columns = len(header) if header else 0
            rows = sum(1 for _ in reader)
        status, error = "ok", ""
    except Exception as exc:
        status, error = "failed", f"{type(exc).__name__}: {exc}"
    elapsed = time.perf_counter() - start
    return {"file": path.name, "size_bytes": path.stat().st_size, "data_rows": rows,
            "columns": columns, "read_seconds": round(elapsed, 6),
            "status": status, "error": error}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir", required=True)
    p.add_argument("--output-dir", required=True)
    a = p.parse_args()
    folder, out = Path(a.data_dir), Path(a.output_dir)
    if not folder.is_dir():
        p.error(f"Data directory does not exist: {folder}")
    out.mkdir(parents=True, exist_ok=True)
    results = [benchmark(x) for x in sorted(folder.rglob("*.csv"))]
    report = {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
              "method": "Python csv.reader; elapsed wall-clock time using perf_counter",
              "results": results}
    target = out / "csv_performance_report.json"
    target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Benchmarked {len(results)} CSV file(s). Report: {target}")
    for r in results:
        print(f"{r['file']}: {r['data_rows']} rows, {r['read_seconds']} sec, {r['status']}")
    print("Repeat under comparable conditions before drawing performance conclusions.")

if __name__ == "__main__":
    main()
