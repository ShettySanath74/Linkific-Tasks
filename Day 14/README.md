# Day 14 — Big Data Processing with PySpark and Data Quality Testing

## Overview
This project introduces big data concepts, Apache Spark, PySpark DataFrame operations, and data quality validation using sample sales data.

## Learning Objectives
- Understand the 3 V's of big data: Volume, Velocity, and Variety.
- Learn distributed storage and distributed processing concepts.
- Set up Apache Spark using PySpark.
- Perform DataFrame operations, aggregations, joins, window functions, and UDFs.
- Implement data quality checks and negative test cases.

## Environment
- Python 3.13
- Java 17
- PySpark 4.2.1
- Ubuntu on WSL

## Project Structure
- `scripts/01_spark_basics.py` — SparkSession and DataFrame basics.
- `scripts/02_process_sales_csv.py` — CSV ingestion, revenue calculation, aggregation, and output.
- `scripts/03_data_quality.py` — five initial data quality checks.
- `scripts/04_advanced_operations.py` — joins, window functions, and UDF.
- `scripts/05_validate_bad_data.py` — negative validation tests.
- `data/sales.csv` — clean sample sales dataset.
- `data/sales_invalid.csv` — dataset with deliberately invalid records.
- `outputs/processed_sales/` — processed Spark CSV output.
- `outputs/data_quality_report/` — initial validation report.

## Data Processing
The sales-processing script reads ten orders, calculates revenue as quantity multiplied by unit price, and aggregates revenue by category.

Observed category totals:
- Electronics: 86,000
- Furniture: 39,000
- Clothing: 11,800
- Total revenue: 136,800

## Data Quality Checks
The initial validation script checks:
1. The dataset is not empty.
2. Required fields contain no null values.
3. Order IDs are unique.
4. Quantities are positive.
5. Unit prices are non-negative.

All five checks passed on the clean sample dataset.

## Negative Testing
A separate script tested deliberately invalid records. All four expected issues were detected:
- Duplicate order IDs
- Missing customer name
- Zero quantity
- Negative unit price

## Key Learnings
- Spark DataFrames support scalable data transformations.
- Grouping and aggregations summarize data by category.
- Joins combine records from related datasets.
- Window functions support rankings and cumulative calculations.
- UDFs apply custom Python logic to Spark columns.
- Data quality testing checks both valid and invalid data.

## Execution
Activate the project environment and run the scripts from the `Day 14` directory:

```bash
source .venv/bin/activate
python scripts/01_spark_basics.py
python scripts/02_process_sales_csv.py
python scripts/03_data_quality.py
python scripts/04_advanced_operations.py
python scripts/05_validate_bad_data.py
```

