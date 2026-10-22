
-- ============================================================
-- DAY 9: ADVANCED SQL
-- File: 01_advanced_joins.sql
-- Database: ecommerce_db
-- ============================================================

-- 1. INNER JOIN: orders with customer names
SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    o.order_date,
    o.status
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id;

-- 2. LEFT JOIN: all customers, including those without orders
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    o.order_id
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id;

-- 3. RIGHT JOIN: all customers represented by their orders,
-- including any orders without a matching customer
SELECT
    c.first_name,
    c.last_name,
    o.order_id,
    o.status
FROM orders o
RIGHT JOIN customers c
    ON o.customer_id = c.customer_id;

-- 4. FULL OUTER JOIN: retain unmatched rows from both sides
SELECT
    c.customer_id,
    c.first_name,
    o.order_id,
    o.customer_id AS order_customer_id
FROM customers c
FULL OUTER JOIN orders o
    ON c.customer_id = o.customer_id;

-- 5. CROSS JOIN: every product-category combination
SELECT
    p.product_name,
    categories.category_name
FROM products p
CROSS JOIN (
    VALUES ('Premium'), ('Standard'), ('Budget')
) AS categories(category_name);

-- 6. Multiple-table JOIN: complete order line details
SELECT
    o.order_id,
    c.first_name,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS line_total
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
ORDER BY o.order_id;

-- 7. Self JOIN: find customers living in the same city
SELECT
    c1.first_name AS customer_one,
    c2.first_name AS customer_two,
    c1.city
FROM customers c1
JOIN customers c2
    ON c1.city = c2.city
   AND c1.customer_id < c2.customer_id
WHERE c1.city IS NOT NULL;

-- 8. LEFT JOIN with aggregation: count orders per customer
SELECT
    c.customer_id,
    c.first_name,
    COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name
ORDER BY total_orders DESC;

-- 9. Find customers who have never placed an order
SELECT
    c.customer_id,
    c.first_name,
    c.last_name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- 10. Find products that have never been ordered
SELECT
    p.product_id,
    p.product_name
FROM products p
LEFT JOIN order_items oi
    ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

-- END OF ADVANCED JOIN EXAMPLES
