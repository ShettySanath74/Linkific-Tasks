
-- ============================================================
-- DAY 9: WINDOW FUNCTIONS
-- Database: ecommerce_db
-- ============================================================

-- 1. ROW_NUMBER: assign a unique row number to each product
SELECT
    product_name,
    category,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) AS row_num
FROM products;

-- 2. RANK: rank products by price, including tied ranks
SELECT
    product_name,
    price,
    RANK() OVER (ORDER BY price DESC) AS price_rank
FROM products;

-- 3. DENSE_RANK: rank products without gaps after ties
SELECT
    product_name,
    price,
    DENSE_RANK() OVER (ORDER BY price DESC) AS dense_price_rank
FROM products;

-- 4. PARTITION BY: rank products within each category
SELECT
    product_name,
    category,
    price,
    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY price DESC
    ) AS category_rank
FROM products;

-- 5. Find the most expensive product in each category
WITH ranked_products AS (
    SELECT
        product_name,
        category,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY price DESC
        ) AS rn
    FROM products
)
SELECT product_name, category, price
FROM ranked_products
WHERE rn = 1;

-- 6. Running total of order values by order date
WITH order_totals AS (
    SELECT
        o.order_id,
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_date
)
SELECT
    order_id,
    order_date,
    order_total,
    SUM(order_total) OVER (
        ORDER BY order_date, order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM order_totals
ORDER BY order_date, order_id;

-- 7. Compare each order with the previous order's value using LAG
WITH order_totals AS (
    SELECT
        o.order_id,
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_date
)
SELECT
    order_id,
    order_date,
    order_total,
    LAG(order_total) OVER (
        ORDER BY order_date, order_id
    ) AS previous_order_total
FROM order_totals;

-- 8. Compare each order with the next order's value using LEAD
WITH order_totals AS (
    SELECT
        o.order_id,
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_date
)
SELECT
    order_id,
    order_date,
    order_total,
    LEAD(order_total) OVER (
        ORDER BY order_date, order_id
    ) AS next_order_total
FROM order_totals;

-- 9. Difference between the current and previous order values
WITH order_totals AS (
    SELECT
        o.order_id,
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_date
),
comparisons AS (
    SELECT
        order_id,
        order_date,
        order_total,
        LAG(order_total) OVER (
            ORDER BY order_date, order_id
        ) AS previous_total
    FROM order_totals
)
SELECT
    order_id,
    order_date,
    order_total,
    previous_total,
    order_total - previous_total AS change_from_previous
FROM comparisons;

-- 10. Moving average of the last three orders
WITH order_totals AS (
    SELECT
        o.order_id,
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_date
)
SELECT
    order_id,
    order_date,
    order_total,
    ROUND(
        AVG(order_total) OVER (
            ORDER BY order_date, order_id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS three_order_moving_average
FROM order_totals
ORDER BY order_date, order_id;

-- 11. Percentage of total sales contributed by each order
WITH order_totals AS (
    SELECT
        o.order_id,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
)
SELECT
    order_id,
    order_total,
    ROUND(
        100.0 * order_total / NULLIF(SUM(order_total) OVER (), 0),
        2
    ) AS percentage_of_total_sales
FROM order_totals
ORDER BY order_total DESC;

-- 12. Rank customers by total spending
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spending
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT
    customer_id,
    first_name,
    last_name,
    total_spending,
    DENSE_RANK() OVER (
        ORDER BY total_spending DESC
    ) AS spending_rank
FROM customer_spending;

-- 13. Calculate each product's percentage of category inventory value
WITH product_inventory AS (
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
    ) AS category_inventory_percentage
FROM product_inventory
ORDER BY category, inventory_value DESC;

-- 14. NTILE: divide products into four price groups
SELECT
    product_name,
    price,
    NTILE(4) OVER (ORDER BY price DESC) AS price_group
FROM products;

-- 15. FIRST_VALUE: show the highest-priced product in each category
SELECT
    product_name,
    category,
    price,
    FIRST_VALUE(product_name) OVER (
        PARTITION BY category
        ORDER BY price DESC
    ) AS highest_priced_product
FROM products;

-- END OF WINDOW FUNCTION EXAMPLES
