"""CSV extraction stage."""
import csv, json
from pathlib import Path
from scripts.common import SOURCE_DIR, EXTRACT_DIR, ensure_directories, get_logger
logger=get_logger(__name__)

def extract_csv_to_json(source_path, output_path):
    ensure_directories()
    source_path, output_path = Path(source_path), Path(output_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Source file does not exist: {source_path}")
    with source_path.open(newline="", encoding="utf-8-sig") as f:
        rows=list(csv.DictReader(f))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f: json.dump(rows, f)
    logger.info("Extracted %d rows from %s",len(rows),source_path.name)
    return str(output_path)

def extract_customers():
    return extract_csv_to_json(SOURCE_DIR/"customers.csv", EXTRACT_DIR/"customers.json")
def extract_sales():
    return extract_csv_to_json(SOURCE_DIR/"sales.csv", EXTRACT_DIR/"sales.json")
