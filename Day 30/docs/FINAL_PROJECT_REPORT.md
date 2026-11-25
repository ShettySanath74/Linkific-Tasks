# Final Project Report – Business Intelligence & Analytics

## 1. Objective
Build an analytical workflow that converts structured synthetic retail data into useful views of sales performance, profitability, customer activity, category contribution, and regional performance.

## 2. Concepts covered
- Relational data modeling and one-to-many relationships
- CSV ingestion and structural data-quality validation
- SQL joins, filtering, aggregation, and KPI calculation
- Python-based exploratory analysis
- Power BI semantic modeling and DAX measure design
- Unit testing and edge-case handling
- SQLite index benchmarking and query-plan review
- Technical documentation and project handover

## 3. Work completed

### Day 28 – Business Intelligence & Analytics
- Prepared a synthetic retail dataset with customers, orders, order items, and products.
- Created reusable SQLite-compatible analytical SQL.
- Prepared a Python exploratory analysis notebook.
- Prepared Power BI model guidance and DAX measure definitions.
- Produced KPI summary outputs and category, monthly, and regional chart artifacts.
- Documented business insights and recommendations.

### Day 29 – Documentation, Testing, Optimization & Presentation
- Prepared architecture, data dictionary, ETL, user, and optimization documentation.
- Executed CSV structural validation against the four Day 28 source files.
- Executed the Day 29 automated test suite.
- Benchmarked ten SQL queries before and after index creation.
- Prepared a technical presentation and supporting walkthrough material.

### Day 30 – Final handover package
- Consolidated the project summary, architecture, operating guidance, test evidence, performance findings, business insights, limitations, demo script, mentor Q&A, and tracker entry.
- Added helper utilities to audit expected repository artifacts and inspect SQLite query plans.
- Included the latest prepared PowerPoint presentation.

## 4. Implementation details
The documented analytical flow is:

`Source CSV files → Python / SQL preparation and analysis → analytical outputs → Power BI model and dashboard → business interpretation`

The four source entities are customers, orders, order_items, and products. Relationships are customers to orders, orders to order_items, and products to order_items.

## 5. Testing and validation evidence

| Check | Recorded result |
|---|---:|
| CSV files scanned | 4 |
| Files with status OK | 4 |
| Review / failed files | 0 / 0 |
| Day 29 automated tests | 6 passed |
| SQL benchmark queries faster after indexing | 6 of 10 |
| SQL benchmark queries slower after indexing | 4 of 10 |

The Day 29 test output reported `Ran 6 tests` and `OK`. The CSV report found no blank cells, duplicate rows, inconsistent rows, or nulls in the four scanned files.

## 6. Key challenges and observations
- Indexing did not improve every query. Query-specific measurement is necessary.
- The current architecture documentation describes a local file-based analytical workflow. It does not establish an Airflow-orchestrated production pipeline.
- The dataset is synthetic and currency is expressed in generic currency units.
- Power BI Desktop assembly/visual behavior requires manual inspection.

## 7. Key learnings
- Data quality should be checked before analysis.
- Business metrics require explicit definitions and filters.
- Indexes must be evaluated against actual query workloads.
- Technical claims should be supported by execution evidence.
- Clear documentation makes an analytical project easier to reproduce and hand over.

## 8. Deliverables
See `PROJECT_HANDOVER.md` and `FINAL_HANDOVER_CHECKLIST.md` for the inventory and completion checks.

## 9. Conclusion
The Day 28–29 work demonstrates a practical learning workflow for retail business intelligence: structured data, analytical SQL and Python, quality checks, testing, measured SQL tuning, and dashboard-oriented reporting. The Day 30 package organizes the known evidence for review and handover. It does not claim unverified production orchestration or dashboard behavior.
