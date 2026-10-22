
-- ============================================================
-- DAY 9: ADVANCED SQL PRACTICE
-- Database: ecommerce_db
-- Topics: JOINs, CTEs, Aggregations, Window Functions
-- ============================================================

-- 1. Customer spending and order count
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(DISTINCT o.order_id) AS order_count,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spending
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spending DESC;

-- 2. Rank customers by spending
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.first_name,
        COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spending
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY c.customer_id, c.first_name
)
SELECT *,
       DENSE_RANK() OVER (ORDER BY total_spending DESC) AS spending_rank
FROM customer_spending;

-- 3. Revenue by product and category
SELECT
    p.category,
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.category, p.product_id, p.product_name
ORDER BY p.category, revenue DESC;

-- 4. Rank products by revenue within each category
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
    FROM products p
    LEFT JOIN order_items oi ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT *,
       DENSE_RANK() OVER (
           PARTITION BY category
           ORDER BY revenue DESC
       ) AS category_revenue_rank
FROM product_sales;

-- 5. Orders above the overall average order value
WITH order_totals AS (
    SELECT
        o.order_id,
        o.customer_id,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id, o.customer_id
)
SELECT *
FROM order_totals
WHERE order_total > (
    SELECT AVG(order_total) FROM order_totals
)
ORDER BY order_total DESC;

-- 6. Running total of sales
WITH daily_sales AS (
    SELECT
        o.order_date::date AS sales_date,
        SUM(oi.quantity * oi.unit_price) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_date::date
)
SELECT
    sales_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY sales_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue
FROM daily_sales
ORDER BY sales_date;

-- 7. Compare each day's revenue with the previous recorded sales day
WITH daily_sales AS (
    SELECT
        o.order_date::date AS sales_date,
        SUM(oi.quantity * oi.unit_price) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_date::date
)
SELECT
    sales_date,
    daily_revenue,
    LAG(daily_revenue) OVER (ORDER BY sales_date) AS previous_revenue,
    daily_revenue - LAG(daily_revenue) OVER (
        ORDER BY sales_date
    ) AS revenue_change
FROM daily_sales
ORDER BY sales_date;

-- 8. Calculate a three-row moving average of recorded daily revenue
WITH daily_sales AS (
    SELECT
        o.order_date::date AS sales_date,
        SUM(oi.quantity * oi.unit_price) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_date::date
)
SELECT
    sales_date,
    daily_revenue,
    ROUND(
        AVG(daily_revenue) OVER (
            ORDER BY sales_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_average
FROM daily_sales
ORDER BY sales_date;

-- 9. Sales totals by order status
SELECT
    o.status,
    COUNT(DISTINCT o.order_id) AS order_count,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_value
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.status
ORDER BY total_value DESC;

-- 10. Identify customers with no orders
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);

-- 11. Products priced above their category average
SELECT p.product_name, p.category, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category = p.category
);

-- 12. Calculate inventory value and category share
WITH inventory AS (
    SELECT
        product_id,
        product_name,
        category,
        price * stock_quantity AS inventory_value
    FROM products
)
SELECT
    product_name,
    category,
    inventory_value,
    ROUND(
        100.0 * inventory_value /
        NULLIF(SUM(inventory_value) OVER (PARTITION BY category), 0),
        2
    ) AS category_share_percent
FROM inventory
ORDER BY category, inventory_value DESC;

-- 13. Monthly sales summary
SELECT
    DATE_TRUNC('month', o.order_date)::date AS sales_month,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY sales_month;

-- 14. Find customers whose spending exceeds 5000
SELECT
    c.customer_id,
    c.first_name,
    SUM(oi.quantity * oi.unit_price) AS spending
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.first_name
HAVING SUM(oi.quantity * oi.unit_price) > 5000;

-- 15. Compare query plans for a customer order lookup
EXPLAIN
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 1;

-- END OF ADVANCED SQL PRACTICE
