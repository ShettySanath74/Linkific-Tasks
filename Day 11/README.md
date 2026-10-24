# Day 11 — Data Warehousing and Dimensional Modeling

## 1. Project Overview

This project demonstrates the fundamentals of data warehousing, dimensional modeling, star schema design, and Slowly Changing Dimensions (SCDs) using PostgreSQL.

The project uses an e-commerce sales scenario to organize customer, product, date, store, and sales data for analytical reporting.

## 2. Learning Objectives

- Understand OLTP and OLAP systems.
- Differentiate databases, data warehouses, and data marts.
- Design star, snowflake, and galaxy schemas.
- Understand fact tables, dimension tables, measures, and attributes.
- Apply surrogate keys and natural keys.
- Implement SCD Type 1 and Type 2 concepts.
- Build analytical queries for sales reporting.

## 3. OLTP vs. OLAP

**OLTP (Online Transaction Processing)** supports day-to-day operations such as creating orders, updating customer information, and recording payments.

**OLAP (Online Analytical Processing)** supports analytical workloads such as calculating revenue, comparing product performance, and identifying sales trends.

A data warehouse consolidates data for reporting and analysis. A data mart serves a specific business function or subject area.

## 4. Dimensional Modeling

Dimensional modeling organizes data into fact and dimension tables.

### Fact Table

`fact_sales` stores sales measures and foreign keys connecting transactions to dimensions.

Measures include:
- Quantity sold
- Unit price
- Sales amount

**Declared grain:** One row per product line within a sales transaction.

### Dimension Tables

- `dim_customer`: Customer attributes and historical versions.
- `dim_product`: Product names, categories, and prices.
- `dim_date`: Calendar, month, quarter, and year attributes.
- `dim_store`: Store and sales-channel attributes.

## 5. Schema Types

- **Star schema:** A central fact table connects directly to dimension tables.
- **Snowflake schema:** Dimensions are normalized into related sub-dimension tables.
- **Galaxy schema:** Multiple fact tables share common dimensions.

This project uses a star schema.

## 6. Keys

- **Natural key:** An identifier originating from the source system, such as `customer_id`.
- **Surrogate key:** A warehouse-generated identifier, such as `customer_key`.
- **Foreign key:** A reference connecting a fact record to a dimension record.

Surrogate keys are especially important when dimension records need historical versions.

## 7. Slowly Changing Dimensions

### Type 1 — Overwrite

Updates an attribute in place. The previous value is not retained in the dimension.

### Type 2 — Historical versioning

Creates a new dimension row when a tracked attribute changes. The old row is retained with its effective end date and current flag updated.

The customer dimension uses:
- `effective_start_date`
- `effective_end_date`
- `is_current`

The demonstration tracks a customer's city changing from Mangaluru to Bengaluru.

### Type 3 — Previous-value column

Stores a limited amount of history in additional columns, such as `previous_city`. It is suitable when only a limited number of previous values need to be retained.

## 8. Analytical Queries

The analytical SQL script demonstrates:
- Overall revenue and units sold
- Revenue by product and category
- Customer spending
- Revenue by city
- Monthly and daily sales
- Revenue by sales channel
- Category revenue percentages

## 9. Project Structure

```text
Day 11/
├── README.md
├── sql/
│   ├── 01_create_warehouse.sql
│   ├── 02_insert_sample_data.sql
│   ├── 03_analytical_queries.sql
│   └── 04_scd_type2.sql
├── data/
├── docs/
├── erd/
│   └── star_schema.md
├── scripts/
└── outputs/
```

## 10. Execution Order

1. Create the `ecommerce_warehouse` database in PostgreSQL.
2. Execute `sql/01_create_warehouse.sql`.
3. Execute `sql/02_insert_sample_data.sql`.
4. Execute `sql/03_analytical_queries.sql`.
5. Execute and verify `sql/04_scd_type2.sql`.
6. Review the ERD in `erd/star_schema.md`.

Run the SQL scripts in the `ecommerce_warehouse` database, not the existing operational database.

## 11. Tools and Technologies

- PostgreSQL 18
- pgAdmin 4
- SQL
- Visual Studio Code
- Git and GitHub

## 12. Conclusion

This project demonstrates how an e-commerce data warehouse can support analytical reporting through dimensional modeling, fact and dimension tables, aggregation queries, and historical customer tracking.


