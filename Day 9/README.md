# Day 9: Advanced SQL

## Overview
This module focuses on advanced SQL techniques using PostgreSQL, including joins, aggregations, window functions, subqueries, Common Table Expressions (CTEs), and query optimization.

## Learning Objectives
- Understand and apply different SQL JOIN types.
- Perform complex aggregations using `GROUP BY`, `HAVING`, `COUNT(DISTINCT)`, `ROLLUP`, and `CUBE`.
- Analyze data using window functions such as `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, and `LEAD()`.
- Write subqueries, correlated subqueries, and CTEs.
- Inspect query execution plans using `EXPLAIN` and `EXPLAIN ANALYZE`.
- Build multi-table queries for customer, product, order, and sales analysis.

## Project Structure

```text
Day 9/
├── README.md
├── sql/
│   ├── 01_advanced_joins.sql
│   ├── 02_advanced_aggregations.sql
│   ├── 03_window_functions.sql
│   ├── 04_subqueries_ctes.sql
│   ├── 05_query_optimization.sql
│   └── 06_advanced_sql_practice.sql
├── data/
└── docs/
```

## SQL Files

| File | Topics Covered |
|---|---|
| `01_advanced_joins.sql` | INNER, LEFT, RIGHT, FULL OUTER, CROSS, self joins, multi-table joins |
| `02_advanced_aggregations.sql` | GROUP BY, HAVING, distinct counts, category summaries, ROLLUP, CUBE, FILTER |
| `03_window_functions.sql` | Ranking, partitioning, running totals, LAG, LEAD, moving averages, NTILE |
| `04_subqueries_ctes.sql` | Scalar and correlated subqueries, EXISTS, CTEs, multiple CTEs, recursive CTEs |
| `05_query_optimization.sql` | EXPLAIN, EXPLAIN ANALYZE, indexes, ANALYZE, filtering and execution plans |
| `06_advanced_sql_practice.sql` | Integrated customer, product, order, inventory, and sales analysis |

## Database Requirements

This project uses the existing PostgreSQL `ecommerce_db` database from Day 8.

Expected tables:
- `customers`
- `products`
- `orders`
- `order_items`

**Important:** Use the existing database and tables. Do not rerun the Day 8 schema or sample-data scripts against a populated database unless you are intentionally setting up a separate fresh database.

## How to Run

1. Open pgAdmin 4.
2. Connect to PostgreSQL and select `ecommerce_db`.
3. Open the Query Tool.
4. Open a SQL file from the `sql/` directory.
5. Execute individual queries or run the file in manageable sections.
6. Review the result grid and any error messages.

Run the files in this order:

1. `01_advanced_joins.sql`
2. `02_advanced_aggregations.sql`
3. `03_window_functions.sql`
4. `04_subqueries_ctes.sql`
5. `05_query_optimization.sql`
6. `06_advanced_sql_practice.sql`

## Key SQL Patterns

### Joining related tables
```sql
SELECT c.customer_id, c.first_name, o.order_id
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

### Aggregating grouped data
```sql
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
HAVING COUNT(*) > 1;
```

### Ranking with a window function
```sql
SELECT product_name, price,
       RANK() OVER (ORDER BY price DESC) AS price_rank
FROM products;
```

### Creating a reusable query with a CTE
```sql
WITH customer_orders AS (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_orders
ORDER BY order_count DESC;
```

### Inspecting a query plan
```sql
EXPLAIN
SELECT product_name, price
FROM products
WHERE category = 'Electronics';
```

## Query Optimization Notes

- Select only the columns required instead of using `SELECT *` unnecessarily.
- Filter rows as early as practical.
- Use appropriate join conditions and indexes where useful.
- Compare execution plans using `EXPLAIN`.
- Use `EXPLAIN ANALYZE` carefully because it executes the query.
- On a small sample database, indexes may not improve query speed because PostgreSQL may choose a sequential scan.

## Validation Status

The SQL files have been organized for testing. Mark queries as validated only after executing them successfully in PostgreSQL and reviewing their outputs.

## Deliverables
- Advanced SQL query examples covering joins and aggregations.
- Window function demonstrations.
- Subqueries and CTE examples.
- Query execution plan and optimization examples.
- Integrated SQL analysis practice.
- This README documenting the project structure and SQL patterns.
