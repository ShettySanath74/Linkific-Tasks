# Project Proposal and Requirements

## 1. Project title
E-commerce Analytics Platform

## 2. Problem statement
E-commerce operations generate data across products, customers, orders, payments, and inventory. When this data is held in disconnected files and systems, it is difficult to produce consistent sales reports, identify product trends, and monitor stock levels. This project proposes a centralized analytical platform that integrates these sources into a structured warehouse.

## 3. Objectives
- Collect product, order, customer, and inventory data from APIs and files.
- Validate, clean, standardize, and transform incoming records.
- Store analytical data in PostgreSQL using a dimensional star schema.
- Orchestrate repeatable ETL workflows using Apache Airflow.
- Expose reliable datasets for a Power BI dashboard.
- Track data quality and pipeline execution.

## 4. Scope
**In scope:** batch ingestion, CSV/JSON/API inputs, staging and transformation, dimensional warehouse design, data quality checks, scheduled orchestration, sales and inventory reporting.

**Out of scope for the initial version:** payment processing, customer-facing application features, production-scale streaming, personally identifiable customer data, and automated replenishment.

## 5. Functional requirements
1. Ingest product, customer, order, order-item, and inventory records.
2. Support API and CSV/JSON file inputs.
3. retain source identifiers and ingestion timestamps for traceability.
4. Standardize dates, currencies, categories, and identifiers.
5. Reject or quarantine invalid records.
6. Load dimensions before dependent fact records.
7. Support repeatable loads and avoid duplicate fact records.
8. Produce curated tables for dashboard reporting.
9. Log pipeline outcomes and errors.

## 6. Non-functional requirements
- **Reliability:** failed tasks should be logged and safely retryable.
- **Data quality:** key fields, uniqueness, valid ranges, and relationships must be checked.
- **Maintainability:** separate ingestion, transformation, warehouse, and orchestration code.
- **Security:** credentials are stored in environment variables or Airflow Connections.
- **Scalability:** design should allow additional sources and dimensions.
- **Traceability:** include source and load metadata.

## 7. Data sources and assumptions
| Source | Data | Initial method | Expected scale |
|---|---|---|---|
| Product API or sample API | Product ID, name, category, price | REST API | 1,000–10,000 records |
| Orders API or sample files | Order and order-item details | REST API / CSV / JSON | 1,000–10,000 records |
| Customer file/API | Customer ID and attributes | CSV / JSON / API | 1,000–10,000 records |
| Inventory file/API | Product ID, stock quantity, location | CSV / API | 100–5,000 records |

The initial scale is a development estimate, not a measured production volume. Use sample or synthetic records if a suitable API is unavailable.

## 8. Update frequency
- Orders and sales: daily batch for the initial version.
- Products and customers: daily or when source data changes.
- Inventory: daily batch initially; later simulate more frequent updates.

## 9. Analytics and dashboard requirements
- Revenue, order count, units sold, and average order value.
- Revenue by date, category, and product.
- Top and low-performing products.
- Inventory on hand and low-stock indicators.
- Filters for date, category, and location.

## 10. User personas
- Business manager: monitors overall performance and trends.
- Sales analyst: explores revenue, order volume, and product performance.
- Inventory manager: monitors stock and identifies low-stock products.

## 11. Success criteria
- All agreed source datasets can be ingested into staging.
- Data quality checks identify invalid and duplicate records.
- Warehouse tables follow the documented model.
- A repeatable pipeline loads validated data.
- Dashboard measures reconcile with warehouse queries.
- Pipeline runs and failures are observable through logs.

## 12. Risks and mitigations
| Risk | Mitigation |
|---|---|
| API limits or downtime | retries, rate limiting, sample-file fallback |
| Inconsistent source schemas | explicit schema mapping and validation |
| Duplicate records | natural/business keys and idempotent loads |
| Missing or invalid values | quarantine and quality reports |
| Local setup complexity | document PostgreSQL and Airflow setup separately |
