# Day 24 – Sales Data Warehouse

A self-contained dimensional warehouse demo using Python's standard library and SQLite. It covers a Star Schema, date dimension, dimension loading, customer SCD Type 2, fact loading, and validation.

**Sample-data note:** The CSVs are fictional demonstration data. After the first run, we can adapt the source files and mappings to your earlier internship datasets if needed.

## Run in PowerShell
Extract the ZIP, open PowerShell in the `Day 24` folder, then run:

```powershell
python --version
python -m scripts.main
python -m unittest discover -s tests -v
```

No third-party packages are required. `requirements.txt` is intentionally empty.

## Design
- `dim_date`: one row per calendar date; day/week/month/quarter/year, weekend and holiday attributes.
- `dim_customer`: customer versions using SCD Type 2 (`customer_key`, effective dates, current flag).
- `dim_product`: product descriptions using SCD Type 1.
- `fact_sales`: one row per `(order_id, line_number)` with date/customer/product foreign keys and quantity, unit price, sales amount.

## Workflow
1. Create SQLite schema, constraints, foreign keys and indexes.
2. Generate dates spanning the sales input.
3. Load customer and product dimensions.
4. For changed customer attributes, expire the old row and insert a new SCD2 version.
5. Resolve dimension keys for each sales line and calculate `quantity * unit_price`.
6. Load facts idempotently (existing order lines are skipped).
7. Validate counts, foreign keys, dimension references, duplicate grain, measures and current customer versions.

## Demonstrating SCD Type 2
First run the pipeline and save its validation output. Then edit a customer's city in `data/source/customers.csv` and set `updated_at` to a date later than the current value. Run the pipeline again. The prior customer version is retained and a new current version is inserted. Do not modify the sample data before the initial run.

## Outputs
Runtime outputs: `database/warehouse.db`, `outputs/pipeline.log`, `outputs/validation_report.txt`.

The configured holiday list is a small example of Indian national/fixed-date observances, not a complete state-specific holiday calendar. Product dimension uses Type 1; customer dimension uses Type 2. This is a learning-scale CSV-to-SQLite implementation, not a production orchestration platform.
