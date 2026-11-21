# Linkific Day 27 – ETL Pipeline Testing, Data Quality & Performance

## Objective
Extend the Day 26 CSV → JSON → validation/enrichment → SQLite ETL pipeline with reproducible synthetic datasets, automated tests, end-to-end verification, performance benchmarks, and optimization experiments.

## Technology
Python 3.14, CSV/JSON, SQLite, `unittest`, `time.perf_counter`, `concurrent.futures`, Apache Airflow (optional orchestration).

## Quick start (Windows PowerShell)
From the `Day 27` folder:

```powershell
& "C:\Python314\python.exe" run_all.py
```

No third-party Python packages are required for the core workflow. The Airflow DAG is optional and requires an existing compatible Airflow environment.

## Workflow
1. Generate 100, 1,000, 10,000 and 100,000 row synthetic sales files, including invalid amounts, invalid customer references, malformed dates and missing IDs.
2. Run automated unit/integration tests for valid rows, invalid data, duplicates, missing files, idempotent upsert and quality checks.
3. Execute the bundled Day 26 sample through extraction, transformation, loading and quality validation.
4. Benchmark end-to-end ETL at 1k/10k/100k input records.
5. Compare indexed and unindexed query latency and inspect SQLite query plan.
6. Compare sequential and thread-based validation. Threading is an experiment, not a guaranteed optimization.

## Structure
- `scripts/`: ETL, synthetic data, benchmark and parallel experiment scripts
- `tests/`: automated unit/integration tests
- `data/source/`: original Day 26 sample source data
- `data/test_data/`: generated synthetic data
- `outputs/`: extracted/transformed data, SQLite warehouse and reports
- `docs/`: test, performance and optimization notes
- `dags/`: optional Day 26 Airflow DAG

## Individual commands
```powershell
& "C:\Python314\python.exe" -m unittest discover -s tests -v
& "C:\Python314\python.exe" scripts/generate_test_data.py
& "C:\Python314\python.exe" scripts/performance_test.py
& "C:\Python314\python.exe" scripts/parallel_test.py
```

## Validation rules
A sale is rejected if its ID is missing/duplicated, customer reference is unknown, amount is nonnumeric or not positive, or date is not ISO `YYYY-MM-DD`. Accepted rows are enriched with customer name and city. Rejected rows are written to a dead-letter CSV with a reason.

## Optimization
- SQLite `executemany` is used for batch inserts/upserts.
- SQLite connections are explicitly closed after transactions to avoid Windows file-lock cleanup errors.
- A composite index on `(customer_id, sale_date)` supports common customer/date filtering.
- Performance script records indexed/unindexed query timings and `EXPLAIN QUERY PLAN`.
- Parallel comparison measures threads against sequential validation; no speedup is assumed.

## Outputs
- `outputs/day27_execution_summary.json`
- `outputs/quality_report.json`
- `outputs/performance/performance_report.json` and `.csv`
- `outputs/performance/parallel_comparison.json`
- `outputs/transformed/accepted_sales.csv`
- `data/dead_letter/rejected_sales.csv`
- `logs/pipeline.log`

## Important notes
- Performance values are machine-dependent and are generated when the runner executes.
- The test dataset intentionally contains invalid rows; rejected records are expected behavior.
- The warehouse uses upsert semantics keyed by `sale_id`; repeated loads should not create duplicates.
- Core tests and pipeline do not require Airflow. Airflow orchestration should be separately verified in the configured Airflow environment.
