import json
from pathlib import Path
import pandas as pd

from config.settings import INPUT_DIR, STAGING_DIR, BATCH_SIZE
from scripts.common import get_logger, write_jsonl

logger = get_logger("file_processor")

def process_files():
    summary = {}
    # CSV batch processing
    csv_path = INPUT_DIR / "sample.csv"
    csv_records = []
    for chunk in pd.read_csv(csv_path, chunksize=BATCH_SIZE):
        csv_records.extend(chunk.to_dict(orient="records"))
    write_jsonl(csv_records, STAGING_DIR / "files" / "sample_csv.jsonl")
    summary["csv"] = len(csv_records)

    # Excel read in bounded batches after loading the worksheet.
    excel_path = INPUT_DIR / "sample.xlsx"
    df = pd.read_excel(excel_path, engine="openpyxl")
    excel_records = df.to_dict(orient="records")
    for start in range(0, len(excel_records), BATCH_SIZE):
        batch = excel_records[start:start + BATCH_SIZE]
        # Write one JSONL output; batches are processed sequentially.
        if start == 0:
            output = []
        output.extend(batch)
    write_jsonl(output if excel_records else [], STAGING_DIR / "files" / "sample_excel.jsonl")
    summary["excel"] = len(excel_records)

    # JSON may be an array of objects or newline-delimited JSON.
    json_path = INPUT_DIR / "sample.json"
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    json_records = payload if isinstance(payload, list) else [payload]
    json_batches = [json_records[i:i+BATCH_SIZE] for i in range(0, len(json_records), BATCH_SIZE)]
    flattened = [row for batch in json_batches for row in batch]
    write_jsonl(flattened, STAGING_DIR / "files" / "sample_json.jsonl")
    summary["json"] = len(json_records)
    logger.info("File processing summary: %s", summary)
    return summary

if __name__ == "__main__":
    print(process_files())
