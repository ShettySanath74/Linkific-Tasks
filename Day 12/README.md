# Day 12 — End-to-End ETL Pipeline

## 1. Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline using Python. It extracts data from multiple sources, transforms raw records into structured datasets, and loads sales data into a SQLite warehouse.

The project demonstrates multi-source extraction, data cleaning, transformations, incremental loading, upserts, logging, error handling, and retry logic.

## 2. Architecture

```text
API Source ─────────┐
CSV Source ─────────┼──> Extraction Layer
SQLite Source ──────┘          |
                               v
                         Staging Area
                               |
                               v
                     Transformation Layer
                               |
                               v
                      Transformed CSV Files
                               |
                               v
                       SQLite Warehouse
                               |
                               v
                    Validation and Analytics
```

## 3. Technology Stack

- Python 3.14
- Requests — API extraction
- Pandas — data processing and transformation
- SQLite — source database and target warehouse
- JSON and CSV — intermediate data storage
- Logging — execution monitoring
- urllib3 Retry — HTTP retry handling

## 4. Project Structure

```text
Day 12/
├── data/
│   ├── sales.csv
│   └── source.db
├── logs/
│   └── etl_pipeline.log
├── scripts/
│   ├── 01_extract_api.py
│   ├── 02_extract_files.py
│   ├── 03_extract_database.py
│   ├── 04_transform_data.py
│   ├── 05_load_warehouse.py
│   ├── 06_run_pipeline.py
│   └── 07_incremental_load.py
├── staging/
│   ├── api_posts.json
│   ├── sales_raw.json
│   ├── customers_raw.json
│   ├── sales_transformed.csv
│   ├── customers_transformed.csv
│   └── api_posts_transformed.csv
├── warehouse/
│   ├── analytics.db
│   └── etl_state.json
├── tests/
├── requirements.txt
└── README.md
```

## 5. Extraction Layer

### API Extraction
Retrieves records from the JSONPlaceholder posts API and stores the response in JSON format.

### CSV Extraction
Reads the sales CSV file using Pandas and saves the extracted records as JSON in the staging area.

### Database Extraction
Uses Python's SQLite library to create a sample source database, insert sample customer records if absent, and extract the customer table into JSON.

## 6. Transformation Layer

The transformation script:

- Removes leading and trailing whitespace from text fields.
- Converts quantities and prices to numeric types.
- Converts timestamps to datetime values.
- Removes records missing required fields.
- Removes duplicate sales order IDs and customer IDs.
- Calculates order totals using quantity multiplied by unit price.
- Joins sales records with customer data.
- Exports transformed sales, customer, and API datasets to CSV.

## 7. Warehouse Loading

The warehouse loader writes sales records into `warehouse/analytics.db`.

The `sales` table uses `order_id` as its primary key. An upsert inserts new orders or updates existing orders when the incoming timestamp is newer than the stored timestamp.

## 8. Incremental Loading

The incremental loading script reads the timestamp watermark from `warehouse/etl_state.json`.

It selects records with timestamps later than the saved watermark, upserts those records into the warehouse, and advances the watermark after a successful load.

The current implementation uses a strict timestamp comparison. Production systems may require compound watermarks, lookback windows, or CDC to handle equal timestamps and deletions safely.

## 9. Error Handling and Logging

- HTTP requests use a timeout and retry selected temporary failures.
- Exceptions are logged in `logs/etl_pipeline.log`.
- The pipeline runner stops when a script returns a non-zero exit status.
- The API extractor writes new output to a temporary file before replacing the previous output.

## 10. How to Run

Run these commands from the Day 12 project directory:

```powershell
C:\Python314\python.exe -m pip install -r requirements.txt
C:\Python314\python.exe scripts\06_run_pipeline.py
C:\Python314\python.exe scripts\07_incremental_load.py
```

The main pipeline performs extraction, transformation, and standard warehouse loading. The incremental loader is currently a separate execution step.

## 11. Verified Results

During a successful pipeline run:

- 100 API posts were extracted.
- 5 sales records were extracted.
- 4 customer records were extracted.
- 5 sales records were loaded into the warehouse.
- Total calculated sales value was ₹79,050.
- Repeated incremental runs found zero records newer than the saved watermark when the source data remained unchanged.

These results describe the sample data used in this project.

## 12. Current Limitations

- The main pipeline performs full source extraction on each run.
- The incremental loader is separate from the main pipeline runner.
- API and customer datasets are transformed and staged but are not yet loaded into warehouse tables.
- The current watermark implementation does not handle every equal-timestamp or source-deletion scenario.
- Email alerts and automated test coverage remain future improvements.

## 13. Conclusion

This project demonstrates the core stages of a Python ETL workflow: extracting data from multiple sources, transforming records, loading a warehouse, tracking incremental changes, and recording execution details.

The next improvements would be integrating incremental loading into orchestration, loading all target datasets, expanding automated tests, and implementing alerting for production-style reliability.
