"""Scan CSV files and generate basic, schema-neutral data-quality reports."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from datetime import datetime, timezone

def inspect_csv(path: Path) -> dict:
    result = {
        "file": path.name, "path": str(path), "size_bytes": path.stat().st_size,
        "status": "ok", "row_count": 0, "column_count": 0,
        "headers": [], "blank_cells": 0, "duplicate_rows": 0,
        "inconsistent_rows": 0, "nulls_by_column": {}, "issues": []
    }
    if result["size_bytes"] == 0:
        result["status"] = "failed"
        result["issues"].append("File is empty (0 bytes).")
        return result
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers is None:
                result["status"] = "failed"
                result["issues"].append("No header row found.")
                return result
            result["headers"] = headers
            result["column_count"] = len(headers)
            result["nulls_by_column"] = {h: 0 for h in headers}
            seen = set()
            for row in reader:
                result["row_count"] += 1
                if len(row) != len(headers):
                    result["inconsistent_rows"] += 1
                normalized = tuple(cell.strip() for cell in row)
                if normalized in seen:
                    result["duplicate_rows"] += 1
                seen.add(normalized)
                for idx, header in enumerate(headers):
                    value = row[idx].strip() if idx < len(row) else ""
                    if not value:
                        result["blank_cells"] += 1
                        result["nulls_by_column"][header] += 1
            if len(set(headers)) != len(headers):
                result["issues"].append("Duplicate column names detected.")
            if result["inconsistent_rows"]:
                result["issues"].append("Rows with a different number of fields than the header.")
            if result["blank_cells"]:
                result["issues"].append("Blank cells detected; assess whether they are permitted.")
            if result["duplicate_rows"]:
                result["issues"].append("Duplicate data rows detected; assess whether they are valid.")
            if result["issues"]:
                result["status"] = "review"
    except (UnicodeDecodeError, csv.Error, OSError) as exc:
        result["status"] = "failed"
        result["issues"].append(f"{type(exc).__name__}: {exc}")
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, help="Folder containing source CSV files")
    parser.add_argument("--output-dir", required=True, help="Folder for JSON and CSV reports")
    args = parser.parse_args()
    data_dir, output_dir = Path(args.data_dir), Path(args.output_dir)
    if not data_dir.exists() or not data_dir.is_dir():
        parser.error(f"Data directory does not exist: {data_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_files = sorted(data_dir.rglob("*.csv"))
    results = [inspect_csv(p) for p in csv_files]
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_directory": str(data_dir.resolve()),
        "files_scanned": len(results),
        "status_counts": {s: sum(r["status"] == s for r in results) for s in ("ok", "review", "failed")},
        "results": results
    }
    (output_dir / "data_quality_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with (output_dir / "data_quality_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file","status","size_bytes","row_count","column_count","blank_cells","duplicate_rows","inconsistent_rows","issues"])
        writer.writeheader()
        for r in results:
            writer.writerow({**{k:r[k] for k in writer.fieldnames[:-1]}, "issues":" | ".join(r["issues"])})
    print(f"Scanned {len(results)} CSV file(s).")
    print(f"JSON report: {output_dir / 'data_quality_report.json'}")
    print(f"CSV summary: {output_dir / 'data_quality_summary.csv'}")
    if not results:
        print("WARNING: No CSV files were found. Check --data-dir.")
    print("Review the report; 'review' means investigate, not necessarily a business-rule failure.")

if __name__ == "__main__":
    main()
