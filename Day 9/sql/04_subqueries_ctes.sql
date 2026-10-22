
-- ============================================================
-- DAY 9: SUBQUERIES AND COMMON TABLE EXPRESSIONS (CTEs)
-- Database: ecommerce_db
-- ============================================================

-- 1. Subquery in WHERE: products priced above average
SELECT product_name, price
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
);

-- 2. Subquery in WHERE: most expensive products
SELECT product_name, price
FROM products
WHERE price = (
    SELECT MAX(price)
    FROM products
);

-- 3. Subquery with IN: customers who placed orders
SELECT customer_id, first_name, last_name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
);

-- 4. Subquery with NOT EXISTS: customers with no orders
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);

-- 5. Subquery in SELECT: compare each product to average price
SELECT
    product_name,
    price,
    (SELECT AVG(price) FROM products) AS average_price
FROM products;

-- 6. Subquery in FROM: calculate average order value
SELECT AVG(order_total) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(quantity * unit_price) AS order_total
    FROM order_items
    GROUP BY order_id
) AS order_totals;

-- 7. Correlated subquery: products above their own category average
SELECT p.product_name, p.category, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category = p.category
);

-- 8. Correlated subquery: orders above that customer's average order value
WITH order_totals AS (
    SELECT
        o.order_id,
        o.customer_id,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id, o.customer_id
)
SELECT ot.*
FROM order_totals ot
WHERE ot.order_total > (
    SELECT AVG(ot2.order_total)
    FROM order_totals ot2
    WHERE ot2.customer_id = ot.customer_id
);

-- 9. CTE: calculate order totals
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
ORDER BY order_total DESC;

-- 10. Multiple CTEs: order totals and customer spending
WITH order_totals AS (
    SELECT
        o.order_id,
        o.customer_id,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id, o.customer_id
),
customer_spending AS (
    SELECT
        customer_id,
        SUM(order_total) AS total_spending,
        COUNT(*) AS order_count
    FROM order_totals
    GROUP BY customer_id
)
SELECT
    c.first_name,
    c.last_name,
    COALESCE(cs.total_spending, 0) AS total_spending,
    COALESCE(cs.order_count, 0) AS order_count
FROM customers c
LEFT JOIN customer_spending cs
    ON cs.customer_id = c.customer_id
ORDER BY total_spending DESC;

-- 11. CTE plus window function: rank customer spending
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spending
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT
    *,
    DENSE_RANK() OVER (ORDER BY total_spending DESC) AS spending_rank
FROM customer_spending;

-- 12. Recursive CTE: generate numbers from 1 through 10
WITH RECURSIVE number_series(n) AS (
    SELECT 1

    UNION ALL

    SELECT n + 1
    FROM number_series
    WHERE n < 10
)
SELECT n
FROM number_series;

-- 13. Recursive CTE: generate the next 7 calendar dates
WITH RECURSIVE date_series(day_date) AS (
    SELECT DATE '2026-10-22'

    UNION ALL

    SELECT day_date + 1
    FROM date_series
    WHERE day_date < DATE '2026-10-28'
)
SELECT day_date
FROM date_series
ORDER BY day_date;

-- 14. CTE: products with stock below the category average
WITH category_stock AS (
    SELECT
        category,
        AVG(stock_quantity) AS average_stock
    FROM products
    GROUP BY category
)
SELECT
    p.product_name,
    p.category,
    p.stock_quantity,
    cs.average_stock
FROM products p
JOIN category_stock cs ON cs.category = p.category
WHERE p.stock_quantity < cs.average_stock;

-- 15. CTE: calculate each order's total and classify its value
WITH order_totals AS (
    SELECT
        o.order_id,
        o.status,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id, o.status
)
SELECT
    order_id,
    status,
    order_total,
    CASE
        WHEN order_total >= 10000 THEN 'High Value'
        WHEN order_total >= 2000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_category
FROM order_totals
ORDER BY order_total DESC;

-- END OF SUBQUERY AND CTE EXAMPLES
