
-- ============================================================
-- DAY 9: SQL QUERY OPTIMIZATION
-- Database: ecommerce_db
-- PostgreSQL
-- ============================================================

-- 1. Inspect the execution plan of an order lookup
EXPLAIN
SELECT *
FROM orders
WHERE customer_id = 1;

-- 2. Inspect actual execution time and row counts
-- EXPLAIN ANALYZE executes the query.
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE customer_id = 1;

-- 3. Compare SELECT * with selecting only required columns
EXPLAIN ANALYZE
SELECT *
FROM products
WHERE category = 'Electronics';

EXPLAIN ANALYZE
SELECT product_id, product_name, price
FROM products
WHERE category = 'Electronics';

-- 4. Inspect indexes on the products table
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'products';

-- 5. Inspect indexes on the orders table
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'orders';

-- 6. Create an index for product category lookups
-- IF NOT EXISTS prevents an error if the index already exists.
CREATE INDEX IF NOT EXISTS idx_products_category
ON products(category);

-- 7. Create an index for customer order lookups
CREATE INDEX IF NOT EXISTS idx_orders_customer_id
ON orders(customer_id);

-- 8. Create an index for date-based order searches
CREATE INDEX IF NOT EXISTS idx_orders_order_date
ON orders(order_date);

-- 9. Check a date-range query's execution plan
EXPLAIN ANALYZE
SELECT order_id, order_date, status
FROM orders
WHERE order_date >= TIMESTAMP '2026-10-01 00:00:00'
  AND order_date < TIMESTAMP '2026-11-01 00:00:00';

-- 10. Avoid applying a function to the filtered column
-- Preferred: direct date range can use a suitable index.
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE order_date >= TIMESTAMP '2026-10-01 00:00:00'
  AND order_date < TIMESTAMP '2026-11-01 00:00:00';

-- Alternative expression for comparison
-- Applying DATE() to order_date may prevent ordinary index use.
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE order_date::date = DATE '2026-10-10';

-- 11. Inspect a multi-table JOIN execution plan
EXPLAIN ANALYZE
SELECT
    c.first_name,
    o.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE c.customer_id = 1;

-- 12. Compare EXISTS with an IN subquery
EXPLAIN ANALYZE
SELECT c.customer_id, c.first_name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);

EXPLAIN ANALYZE
SELECT c.customer_id, c.first_name
FROM customers c
WHERE c.customer_id IN (
    SELECT o.customer_id
    FROM orders o
);

-- 13. Use LIMIT when only a few rows are required
EXPLAIN ANALYZE
SELECT product_name, price
FROM products
ORDER BY price DESC
LIMIT 3;

-- 14. Update planner statistics after significant data changes
ANALYZE products;
ANALYZE orders;
ANALYZE order_items;
ANALYZE customers;

-- 15. Inspect estimated cost and row count
EXPLAIN
SELECT *
FROM order_items
WHERE product_id = 2;

-- END OF QUERY OPTIMIZATION EXAMPLES
