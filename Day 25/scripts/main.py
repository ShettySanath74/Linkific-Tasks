
import json
import logging
from datetime import datetime

from .config import (
    CUSTOMERS_FILE,
    PRODUCTS_FILE,
    SALES_FILE,
    OUTPUT_DIR,
)
from .db import connect
from .transform import (
    transform_sources,
    aggregate_daily_category,
)
from .quality_checks import run_quality_checks
from .incremental_load import apply_incremental_load
from .error_handler import log_pipeline_error
from .config import REQUIRED_CUSTOMER_COLUMNS, REQUIRED_PRODUCT_COLUMNS, REQUIRED_SALES_COLUMNS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

def write_csv(path, records):
    import csv

    if not records:
        path.write_text("", encoding="utf-8")
        return

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(records[0].keys()),
        )
        writer.writeheader()
        writer.writerows(records)

def validate_source_headers():
    import csv

    required_files = [
        (CUSTOMERS_FILE, REQUIRED_CUSTOMER_COLUMNS),
        (PRODUCTS_FILE, REQUIRED_PRODUCT_COLUMNS),
        (SALES_FILE, REQUIRED_SALES_COLUMNS),
    ]

    errors = []

    for file_path, required_columns in required_files:
        try:
            with file_path.open(
                "r",
                newline="",
                encoding="utf-8-sig",
            ) as file:
                reader = csv.DictReader(file)
                actual_columns = set(reader.fieldnames or [])

            missing = required_columns - actual_columns

            if missing:
                errors.append(
                    f"{file_path.name}: missing columns {sorted(missing)}"
                )

        except FileNotFoundError:
            errors.append(f"Source file not found: {file_path}")

    return errors

def run_pipeline():
    conn = connect()
    run_id = None

    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO pipeline_runs (started_at, status)
                VALUES (?, 'RUNNING')
                """,
                (datetime.now().isoformat(timespec="seconds"),),
            )
            run_id = cursor.lastrowid

        logger.info("Starting Day 25 ETL pipeline.")

        # Step 1: Validate source file headers.
        header_errors = validate_source_headers()

        if header_errors:
            raise ValueError("; ".join(header_errors))

        # Step 2: Transform source data.
        transformed, rejects = transform_sources(
            CUSTOMERS_FILE,
            PRODUCTS_FILE,
            SALES_FILE,
        )

        # Step 3: Run data quality checks.
        quality = run_quality_checks(transformed, rejects)

        # Step 4: Detect duplicate sales lines using a composite key.
        seen = set()
        duplicate_ids = []
        unique_records = []

        for record in transformed:
            record_id = (
                record["order_id"],
                record["line_number"],
            )

            if record_id in seen:
                duplicate_ids.append(record_id)
            else:
                seen.add(record_id)
                unique_records.append(record)

        quality["duplicate_sales_line_ids"] = [
            list(record_id) for record_id in duplicate_ids
        ]

        quality["passed"] = (
            quality["passed"] and not duplicate_ids
        )

        # Step 5: Save transformation and quality outputs.
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        write_csv(
            OUTPUT_DIR / "transformed_sales.csv",
            unique_records,
        )

        active_records = [
            record
            for record in unique_records
            if not record["is_deleted"]
        ]

        write_csv(
            OUTPUT_DIR / "daily_category_summary.csv",
            aggregate_daily_category(active_records),
        )

        (OUTPUT_DIR / "quality_report.json").write_text(
            json.dumps(quality, indent=2),
            encoding="utf-8",
        )

        (OUTPUT_DIR / "rejected_records.json").write_text(
            json.dumps(rejects, indent=2),
            encoding="utf-8",
        )

        # Step 6: Stop loading if duplicate sales lines exist.
        if duplicate_ids:
            raise ValueError(
                f"Duplicate sales line IDs detected: {duplicate_ids}"
            )

        if rejects:
            logger.warning(
                "%s records rejected by transformation quality rules.",
                len(rejects),
            )

        # Step 7: Apply incremental loading.
        # 'seen' contains (order_id, line_number) composite keys.
        counts = apply_incremental_load(
            conn,
            unique_records,
            seen,
        )

        # Step 8: Update pipeline execution status.
        with conn:
            conn.execute(
                """
                UPDATE pipeline_runs
                SET finished_at=?,
                    status='SUCCESS',
                    records_read=?,
                    records_inserted=?,
                    records_updated=?,
                    records_deleted=?,
                    records_rejected=?
                WHERE run_id=?
                """,
                (
                    datetime.now().isoformat(timespec="seconds"),
                    len(unique_records),
                    counts["inserted"],
                    counts["updated"],
                    counts["deleted"],
                    len(rejects),
                    run_id,
                ),
            )

        logger.info("Pipeline completed successfully. %s", counts)

        return counts

    except Exception as exc:
        logger.exception("Pipeline execution failed.")

        try:
            log_pipeline_error(conn, exc)

            if run_id is not None:
                with conn:
                    conn.execute(
                        """
                        UPDATE pipeline_runs
                        SET finished_at=?,
                            status='FAILED'
                        WHERE run_id=?
                        """,
                        (
                            datetime.now().isoformat(timespec="seconds"),
                            run_id,
                        ),
                    )
        except Exception:
            logger.exception("Could not record pipeline failure.")

        raise

    finally:
        conn.close()

if __name__ == "__main__":
    run_pipeline()