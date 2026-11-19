# Day 25 – Data Transformation, Data Quality, CDC and Error Handling

A runnable Python + SQLite ETL project for the Linkific Data Engineering internship.

## What it does
1. Reads `customers.csv`, `products.csv`, and `sales.csv`.
2. Cleans values, converts types, joins the sources, applies business rules and creates daily/category aggregates.
3. Runs reusable quality checks: required/null fields, numeric ranges, date/format checks, duplicate IDs and referential integrity.
4. Detects inserts, updates and deletes using row hashes and a persisted source-state table.
5. Upserts changed records into SQLite and handles deletions from a full source snapshot.
6. Logs pipeline activity, retries transient database operations, records failures, and optionally sends email alerts when SMTP settings are supplied.
7. Includes unit and integration tests using Python's built-in `unittest`.

## Important compatibility note
This project is self-contained and uses a Day 25 working database at `database/day25_warehouse.db`. It does not overwrite Day 24's `database/warehouse.db`. The Day 24 project is known to contain `customers.csv`, `products.csv`, `sales.csv`, and warehouse dimensions/facts, but its exact source column definitions are not assumed here. The sample CSVs in this folder define the Day 25 input contract. After inspecting your Day 24 headers, we can map/adjust the input columns to your exact files.

## Input CSV contract

- `customers.csv`: `customer_id, customer_name, city, updated_at`
- `products.csv`: `product_id, product_name, category, updated_at`
- `sales.csv`: `order_id, customer_id, product_id, order_date, quantity, unit_price, updated_at, is_deleted`

Dates use `YYYY-MM-DD`; `is_deleted` accepts `true/false`, `1/0`, or `yes/no`.

## Folder structure

```text
Day 25/
├── README.md
├── requirements.txt
├── data/source/                 # sample source CSVs
├── database/                    # created at runtime
├── logs/                         # created at runtime
├── outputs/                      # transformed data and reports
├── scripts/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── transform.py
│   ├── quality_checks.py
│   ├── cdc.py
│   ├── incremental_load.py
│   ├── error_handler.py
│   └── main.py
└── tests/
    ├── __init__.py
    ├── test_transform.py
    ├── test_quality.py
    ├── test_cdc.py
    └── test_pipeline.py
```

## Setup (PowerShell)

```powershell
Set-Location "C:\Users\Comp\Linkific-Tasks-Upload\Day 25"
& "C:\Python314\python.exe" --version
```

No third-party dependencies are required. `requirements.txt` is intentionally empty because this implementation uses only Python's standard library (csv, sqlite3, hashlib, logging, smtplib, unittest, pathlib, datetime).

## Run

```powershell
& "C:\Python314\python.exe" -m scripts.main
```

## Run tests

```powershell
& "C:\Python314\python.exe" -m unittest discover -s tests -v
```

## Simulate an incremental change

After the first successful run, edit a value in `data/source/sales.csv` (for example, change the quantity for `S1001`) and run the pipeline again. The CDC state should report an update and the target should be upserted.

To test deletion, remove one sales row from the source CSV and run again. This project treats `sales.csv` as a complete snapshot: a previously seen row missing from the next snapshot is marked deleted in the target. Do not use this missing-row delete strategy with partial/delta files. For delta feeds, use the explicit `is_deleted` flag instead.

## Email alerts (optional)
Set SMTP variables in the PowerShell session before running:

```powershell
$env:SMTP_HOST = "smtp.example.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your-email@example.com"
$env:SMTP_PASSWORD = "your-app-password"
$env:ALERT_TO = "mentor@example.com"
$env:ALERT_FROM = "your-email@example.com"
```

Email is attempted only when a pipeline failure occurs and all required settings are present. Never commit real credentials. For Gmail, use an app password where applicable.

## Outputs
- `outputs/transformed_sales.csv`
- `outputs/daily_category_summary.csv`
- `outputs/quality_report.json`
- `logs/pipeline.log`
- `database/day25_warehouse.db`

## Design notes / limitations
- CDC uses SHA-256 hashes of normalized source rows and persists the last-seen hash per order ID.
- This is a practical file-based CDC demonstration, not database-log-based CDC.
- A missing record is considered deleted only because the sales input is defined as a complete snapshot.
- The pipeline uses SQLite transactions for atomic upserts and deletion updates.
- The sample project demonstrates transformation into a curated sales table. It does not silently alter Day 24's existing star-schema tables.
