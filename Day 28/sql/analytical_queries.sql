-- Day 28: Sales Performance Analytics (SQLite-compatible)
-- Load CSV files into tables named customers, products, orders, order_items.
-- Only Completed orders count toward sales and profit KPIs.

-- 1. Executive KPI summary
SELECT
    COUNT(DISTINCT o.order_id) AS completed_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(oi.line_revenue), 2) AS total_revenue,
    ROUND(SUM(oi.quantity * p.unit_cost), 2) AS total_cost,
    ROUND(SUM(oi.line_revenue - oi.quantity * p.unit_cost), 2) AS estimated_profit,
    ROUND(100.0 * SUM(oi.line_revenue - oi.quantity * p.unit_cost)
          / NULLIF(SUM(oi.line_revenue), 0), 2) AS profit_margin_pct
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.order_status = 'Completed';

-- 2. Monthly revenue trend
SELECT strftime('%Y-%m', o.order_date) AS sales_month,
       ROUND(SUM(oi.line_revenue), 2) AS revenue,
       COUNT(DISTINCT o.order_id) AS orders
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY sales_month;

-- 3. Category performance
SELECT p.category, ROUND(SUM(oi.line_revenue),2) AS revenue,
       SUM(oi.quantity) AS units_sold,
       ROUND(SUM(oi.line_revenue - oi.quantity*p.unit_cost),2) AS estimated_profit
FROM orders o
JOIN order_items oi ON oi.order_id=o.order_id
JOIN products p ON p.product_id=oi.product_id
WHERE o.order_status='Completed'
GROUP BY p.category ORDER BY revenue DESC;

-- 4. Product ranking
SELECT p.product_name, p.category, SUM(oi.quantity) AS units_sold,
       ROUND(SUM(oi.line_revenue),2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id=o.order_id
JOIN products p ON p.product_id=oi.product_id
WHERE o.order_status='Completed'
GROUP BY p.product_id,p.product_name,p.category
ORDER BY revenue DESC;

-- 5. Regional comparison
SELECT o.region, COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(oi.line_revenue),2) AS revenue,
       ROUND(AVG(oi.line_revenue),2) AS avg_line_revenue
FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
WHERE o.order_status='Completed'
GROUP BY o.region ORDER BY revenue DESC;

-- 6. Customer lifetime value (observed period)
SELECT c.customer_id,c.customer_name,c.region,
       COUNT(DISTINCT o.order_id) AS completed_orders,
       ROUND(SUM(oi.line_revenue),2) AS lifetime_revenue
FROM customers c
JOIN orders o ON o.customer_id=c.customer_id
JOIN order_items oi ON oi.order_id=o.order_id
WHERE o.order_status='Completed'
GROUP BY c.customer_id,c.customer_name,c.region
ORDER BY lifetime_revenue DESC LIMIT 20;

-- 7. Order status mix
SELECT order_status, COUNT(*) AS order_count,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM orders),2) AS pct_of_all_orders
FROM orders GROUP BY order_status ORDER BY order_count DESC;

-- 8. Average order value (AOV)
WITH order_totals AS (
    SELECT o.order_id, SUM(oi.line_revenue) AS order_revenue
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    WHERE o.order_status='Completed'
    GROUP BY o.order_id
)
SELECT ROUND(AVG(order_revenue),2) AS average_order_value,
       ROUND(SUM(order_revenue),2) AS total_revenue,
       COUNT(*) AS completed_orders
FROM order_totals;

-- 9. Discount analysis
SELECT ROUND(oi.discount_pct*100,0) AS discount_pct,
       SUM(oi.quantity) AS units_sold,
       ROUND(SUM(oi.line_revenue),2) AS revenue
FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
WHERE o.order_status='Completed'
GROUP BY oi.discount_pct ORDER BY discount_pct;

-- 10. Month-over-month revenue change
WITH monthly AS (
    SELECT strftime('%Y-%m',o.order_date) AS sales_month,
           SUM(oi.line_revenue) AS revenue
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    WHERE o.order_status='Completed'
    GROUP BY strftime('%Y-%m',o.order_date)
), compared AS (
    SELECT sales_month,revenue,LAG(revenue) OVER (ORDER BY sales_month) AS prior_month_revenue
    FROM monthly
)
SELECT sales_month,ROUND(revenue,2) AS revenue,
       ROUND(prior_month_revenue,2) AS prior_month_revenue,
       ROUND(100.0*(revenue-prior_month_revenue)/NULLIF(prior_month_revenue,0),2) AS mom_growth_pct
FROM compared ORDER BY sales_month;
