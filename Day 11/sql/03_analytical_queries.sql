
-- Day 11: Data Warehouse Analytical Queries
-- Database: ecommerce_warehouse

-- 1. Overall sales performance
SELECT
    COUNT(*) AS total_sales_lines,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    SUM(sales_amount) AS total_revenue,
    ROUND(AVG(sales_amount), 2) AS average_line_value
FROM fact_sales;


-- 2. Revenue by product
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name, p.category
ORDER BY revenue DESC;


-- 3. Revenue by customer
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    SUM(f.sales_amount) AS total_spent,
    COUNT(DISTINCT f.order_id) AS number_of_orders
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;


-- 4. Revenue by city
SELECT
    c.city,
    SUM(f.sales_amount) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.city
ORDER BY total_revenue DESC;


-- 5. Revenue by month
SELECT
    d.year_number,
    d.month_number,
    d.month_name,
    SUM(f.sales_amount) AS monthly_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year_number, d.month_number, d.month_name
ORDER BY d.year_number, d.month_number;


-- 6. Revenue by sales channel
SELECT
    s.sales_channel,
    SUM(f.sales_amount) AS total_revenue,
    SUM(f.quantity) AS units_sold
FROM fact_sales f
JOIN dim_store s
    ON f.store_key = s.store_key
GROUP BY s.sales_channel
ORDER BY total_revenue DESC;


-- 7. Daily revenue
SELECT
    d.full_date,
    SUM(f.sales_amount) AS daily_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.full_date
ORDER BY d.full_date;


-- 8. Category performance
SELECT
    p.category,
    SUM(f.sales_amount) AS total_revenue,
    SUM(f.quantity) AS total_units,
    ROUND(
        100.0 * SUM(f.sales_amount)
        / NULLIF(SUM(SUM(f.sales_amount)) OVER (), 0),
        2
    ) AS revenue_percentage
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_revenue DESC;
