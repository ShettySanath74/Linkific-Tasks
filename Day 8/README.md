# Day 8 – SQL and PostgreSQL

## Project Overview
This project demonstrates SQL fundamentals and relational database management using PostgreSQL. An e-commerce database is designed to manage customers, products, orders, and order items.

## Learning Objectives
- Understand relational databases and SQL.
- Create tables with primary keys, foreign keys, and constraints.
- Perform CRUD operations.
- Use filtering, sorting, aggregate functions, and joins.
- Practise GROUP BY, HAVING, and subqueries.
- Explore indexes and query execution plans.

## Technology Stack
- PostgreSQL
- SQL
- Visual Studio Code
- PostgreSQL command-line client (psql)

## Database Design
Database name: `ecommerce_db`

| Table | Purpose |
|---|---|
| customers | Customer information |
| products | Product prices, categories, and stock |
| orders | Customer orders and statuses |
| order_items | Products and quantities in orders |

## Project Files
- `sql/01_schema.sql` – Table definitions, constraints, and indexes.
- `sql/02_sample_data.sql` – Sample customer, product, order, and order-item records.
- `sql/03_sql_queries.sql` – Numbered SQL practice queries.
- `docs/SQL_Reference.md` – SQL syntax reference guide.

## SQL Concepts Covered
- DDL: CREATE TABLE, ALTER TABLE, and DROP examples.
- DML: INSERT, UPDATE, DELETE, and RETURNING.
- Filtering: WHERE, LIKE, ILIKE, IN, BETWEEN, AND, OR.
- Sorting: ORDER BY, LIMIT, DISTINCT.
- Aggregation: COUNT, SUM, AVG, MIN, MAX.
- GROUP BY, HAVING, joins, and subqueries.
- Index inspection and EXPLAIN.

## Setup Instructions
1. Install PostgreSQL and ensure its service is running.
2. Create a database named `ecommerce_db`.
3. Connect to the database.
4. On a fresh database, execute `sql/01_schema.sql`.
5. Execute `sql/02_sample_data.sql` once.
6. Practise individual queries from `sql/03_sql_queries.sql`.

**Important:** The schema and sample-data scripts are intended for a fresh database. Do not rerun them against the existing populated database without preparing a fresh database.

## Learning Outcome
Practised relational database design, constraints, data manipulation, SQL querying, joins, aggregation, and basic query performance analysis.