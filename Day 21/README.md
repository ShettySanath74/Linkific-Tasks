# Day 21 – Multi-Source Data Collection, Format Handling and Integration

## 1. Overview

This project demonstrates a multi-source data engineering workflow involving data collection, format conversion, data integration, pipeline execution, logging, and scheduling.

## 2. Learning Objectives

- Collect data from multiple sources.
- Work with APIs, databases, files, web scraping, and SFTP.
- Process JSON, XML, CSV, Excel, Parquet, and Avro formats.
- Perform schema mapping and data integration.
- Implement pipeline orchestration, logging, and error handling.
- Demonstrate automated pipeline scheduling.

## 3. Project Structure

```text
Day 21/
├── config/
├── data/
│   ├── databases/
│   └── files/
├── integration/
│   ├── 01_inspect_database.py
│   └── 02_data_integration.py
├── outputs/
│   ├── files/
│   ├── logs/
│   ├── api1_posts.json
│   ├── api2_countries.json
│   ├── api3_github.json
│   └── scraped_books.csv
├── pipeline/
│   ├── 01_orchestrate_pipeline.py
│   └── 02_schedule_pipeline.py
├── sources/
│   ├── apis/
│   ├── databases/
│   ├── files/
│   ├── ftp/
│   └── web/
├── tests/
│   └── 01_test_integration_pipeline.py
└── transformations/
    ├── 01_json_to_dataframe.py
    ├── 02_xml_parsing.py
    ├── 03_parquet_conversion.py
    └── 04_avro_conversion.py
```

## 4. Data Sources

The collection exercises cover:

- REST APIs: JSONPlaceholder, Countries API, and GitHub API.
- Databases: SQLite and DuckDB.
- Files: CSV, JSON, and Excel.
- Web scraping: Book data collection.
- SFTP: Remote CSV file collection.

## 5. Data Format Handling

| Format | Implementation |
|---|---|
| JSON | Converted into Pandas DataFrame |
| XML | Parsed using ElementTree |
| Parquet | Converted and read using PyArrow |
| Avro | Serialized and deserialized using FastAvro |
| CSV | Used for structured data storage |

## 6. Data Integration

The SQLite integration exercise combines the `customers` and `sales` tables using `customer_id`.

Implemented concepts:

- Schema mapping
- Key matching
- Left joins
- Duplicate customer-key validation
- Unmatched customer identification
- Data lineage tracking

Output: `integrated_customer_sales.csv`

## 7. Pipeline Orchestration

The pipeline follows an Extract, Transform, Load (ETL) structure.

- Extract: Retrieve customer and sales records from SQLite.
- Transform: Standardize column names and integrate records.
- Load: Export the integrated dataset to CSV.

Logging and exception handling are implemented to record execution details and failures.

## 8. Scheduling

APScheduler is used to demonstrate periodic execution of the integration pipeline.

The scheduler runs the pipeline immediately and then every 24 hours while the scheduler process remains active.

## 9. Testing

A Python unittest script is included to validate:

- Integrated record count
- Required output columns
- Customer record retention
- Sales amount calculations
- Unmatched customer handling
- Data lineage fields

## 10. Technologies Used

- Python
- Pandas
- SQLite
- DuckDB
- Requests
- BeautifulSoup
- Paramiko
- PyArrow
- FastAvro
- APScheduler
- Logging
- Unittest

## 11. Execution

Run the integration pipeline:

```powershell
& "C:\Python314\python.exe" "Day 21\pipeline\01_orchestrate_pipeline.py"
```

Run the pipeline tests:

```powershell
& "C:\Python314\python.exe" "Day 21\tests\01_test_integration_pipeline.py"
```

Run the scheduler:

```powershell
& "C:\Python314\python.exe" "Day 21\pipeline\02_schedule_pipeline.py"
```

## 12. Conclusion

Day 21 provides practical exposure to multi-source data collection, data format processing, relational data integration, ETL pipeline development, logging, error handling, testing, and scheduling.

The exercises demonstrate how data from different sources can be collected, transformed, validated, and prepared for downstream analytics and data engineering workflows.