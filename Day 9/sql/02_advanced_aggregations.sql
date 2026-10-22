
-- ============================================================
-- DAY 9: ADVANCED AGGREGATIONS
-- Database: ecommerce_db
-- ============================================================

-- 1. Count all orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- 2. Count unique customers who placed orders
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;

-- 3. Calculate total value for each order
SELECT
    o.order_id,
    SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
ORDER BY order_total DESC;

-- 4. Calculate average order value
SELECT
    AVG(order_total) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(quantity * unit_price) AS order_total
    FROM order_items
    GROUP BY order_id
) AS order_totals;

-- 5. Total sales by customer
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spending
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spending DESC;

-- 6. Revenue by product category
SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS category_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 7. Categories with revenue greater than 10000
SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS category_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
HAVING SUM(oi.quantity * oi.unit_price) > 10000;

-- 8. Count products per category and calculate average price
SELECT
    category,
    COUNT(*) AS product_count,
    AVG(price) AS average_price,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price
FROM products
GROUP BY category;

-- 9. Calculate revenue and units sold per product
SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC;

-- 10. Group sales by order status
SELECT
    o.status,
    COUNT(DISTINCT o.order_id) AS order_count,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_value
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.status
ORDER BY total_value DESC;

-- 11. ROLLUP: category subtotals and grand total
SELECT
    category,
    SUM(price * stock_quantity) AS inventory_value
FROM products
GROUP BY ROLLUP(category)
ORDER BY category NULLS LAST;

-- 12. CUBE: category and stock-level combinations
SELECT
    category,
    CASE
        WHEN stock_quantity < 20 THEN 'Low stock'
        ELSE 'Adequate stock'
    END AS stock_level,
    COUNT(*) AS product_count
FROM products
GROUP BY CUBE (
    category,
    CASE
        WHEN stock_quantity < 20 THEN 'Low stock'
        ELSE 'Adequate stock'
    END
)
ORDER BY category NULLS LAST, stock_level NULLS LAST;

-- 13. Conditional aggregation: orders by status
SELECT
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE status = 'Delivered') AS delivered_orders,
    COUNT(*) FILTER (WHERE status = 'Pending') AS pending_orders,
    COUNT(*) FILTER (WHERE status = 'Cancelled') AS cancelled_orders
FROM orders;

-- 14. Monthly order counts and value
SELECT
    DATE_TRUNC('month', o.order_date)::date AS order_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS order_value
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY order_month;

-- END OF ADVANCED AGGREGATIONS
