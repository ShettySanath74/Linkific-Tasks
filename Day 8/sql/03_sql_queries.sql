
-- ============================================================
-- DAY 8: SQL PRACTICE QUERIES
-- Project: E-commerce Database
-- Database: ecommerce_db
-- PostgreSQL
-- ============================================================

-- SECTION 1: BASIC SELECT QUERIES

-- 1. Display all customers
SELECT * FROM customers;

-- 2. Display all products
SELECT * FROM products;

-- 3. Display all orders
SELECT * FROM orders;

-- 4. Display all order items
SELECT * FROM order_items;

-- 5. Select specific product columns
SELECT product_name, price FROM products;

-- 6. Rename columns using aliases
SELECT product_name AS product, price AS price_in_rupees
FROM products;

-- SECTION 2: FILTERING WITH WHERE

-- 7. Products costing more than 1000
SELECT * FROM products WHERE price > 1000;

-- 8. Products costing less than 1000
SELECT * FROM products WHERE price < 1000;

-- 9. Products priced at exactly 1500
SELECT * FROM products WHERE price = 1500;

-- 10. Products not in the Electronics category
SELECT * FROM products WHERE category <> 'Electronics';

-- 11. Products costing at least 1000 and at most 10000
SELECT * FROM products WHERE price >= 1000 AND price <= 10000;

-- 12. Products costing more than 1000 OR having stock below 20
SELECT * FROM products WHERE price > 1000 OR stock_quantity < 20;

-- 13. Products that are NOT in the Stationery category
SELECT * FROM products WHERE NOT category = 'Stationery';

-- 14. Customers from Bangalore
SELECT * FROM customers WHERE city = 'Bangalore';

-- 15. Orders that are delivered
SELECT * FROM orders WHERE status = 'Delivered';

-- SECTION 3: LIKE, ILIKE, IN, BETWEEN, NULL

-- 16. Product names starting with 'P'
SELECT * FROM products WHERE product_name LIKE 'P%';

-- 17. Product names containing 'o', case-insensitively
SELECT * FROM products WHERE product_name ILIKE '%o%';

-- 18. Products priced between 500 and 10000
SELECT * FROM products WHERE price BETWEEN 500 AND 10000;

-- 19. Products in selected categories
SELECT * FROM products
WHERE category IN ('Electronics', 'Furniture');

-- 20. Orders in selected statuses
SELECT * FROM orders
WHERE status IN ('Pending', 'Processing');

-- 21. Customers whose city is unknown
SELECT * FROM customers WHERE city IS NULL;

-- 22. Customers whose city is known
SELECT * FROM customers WHERE city IS NOT NULL;

-- SECTION 4: SORTING AND LIMITS

-- 23. Sort products by price, lowest first
SELECT * FROM products ORDER BY price ASC;

-- 24. Sort products by price, highest first
SELECT * FROM products ORDER BY price DESC;

-- 25. Display the three most expensive products
SELECT * FROM products ORDER BY price DESC LIMIT 3;

-- 26. Display the two cheapest products
SELECT * FROM products ORDER BY price ASC LIMIT 2;

-- 27. List distinct product categories
SELECT DISTINCT category FROM products;

-- 28. Sort customers alphabetically by last name
SELECT * FROM customers ORDER BY last_name ASC;

-- SECTION 5: AGGREGATE FUNCTIONS

-- 29. Count all customers
SELECT COUNT(*) AS total_customers FROM customers;

-- 30. Count all products
SELECT COUNT(*) AS total_products FROM products;

-- 31. Calculate the average product price
SELECT AVG(price) AS average_price FROM products;

-- 32. Find the cheapest product price
SELECT MIN(price) AS minimum_price FROM products;

-- 33. Find the most expensive product price
SELECT MAX(price) AS maximum_price FROM products;

-- 34. Calculate the sum of product prices
SELECT SUM(price) AS sum_of_prices FROM products;

-- 35. Calculate total inventory value
SELECT SUM(price * stock_quantity) AS inventory_value
FROM products;

-- SECTION 6: GROUP BY AND HAVING

-- 36. Count products in each category
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;

-- 37. Average price in each category
SELECT category, AVG(price) AS average_price
FROM products
GROUP BY category;

-- 38. Total stock in each category
SELECT category, SUM(stock_quantity) AS total_stock
FROM products
GROUP BY category;

-- 39. Categories whose average price exceeds 1000
SELECT category, AVG(price) AS average_price
FROM products
GROUP BY category
HAVING AVG(price) > 1000;

-- 40. Count orders by status
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status;

-- SECTION 7: JOINS

-- 41. Display orders with customer names
SELECT o.order_id, c.first_name, c.last_name, o.order_date, o.status
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- 42. Display all customers, including those without orders
SELECT c.customer_id, c.first_name, c.last_name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id;

-- 43. Display order items with product names
SELECT oi.order_id, p.product_name, oi.quantity, oi.unit_price
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id;

-- 44. Display complete order details
SELECT o.order_id, c.first_name, c.last_name,
       p.product_name, oi.quantity, oi.unit_price,
       oi.quantity * oi.unit_price AS line_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id;

-- 45. Find customers who have never placed an order
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- SECTION 8: BUSINESS ANALYSIS

-- 46. Total spending per order
SELECT o.order_id,
       SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
ORDER BY o.order_id;

-- 47. Total spending per customer
SELECT c.customer_id, c.first_name, c.last_name,
       SUM(oi.quantity * oi.unit_price) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spending DESC;

-- 48. Customers whose total spending exceeds 5000
SELECT c.customer_id, c.first_name, c.last_name,
       SUM(oi.quantity * oi.unit_price) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(oi.quantity * oi.unit_price) > 5000;

-- 49. Total quantity sold for each product
SELECT p.product_name, SUM(oi.quantity) AS quantity_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY quantity_sold DESC;

-- 50. Products that have never appeared in an order
SELECT p.product_id, p.product_name
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

-- 51. Count orders per customer, including customers with zero orders
SELECT c.customer_id, c.first_name, c.last_name,
       COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY c.customer_id;

-- 52. Total value of stock grouped by category
SELECT category,
       SUM(price * stock_quantity) AS inventory_value
FROM products
GROUP BY category
ORDER BY inventory_value DESC;

-- 53. Find orders placed during October 2026
SELECT * FROM orders
WHERE order_date >= DATE '2026-10-01'
  AND order_date < DATE '2026-11-01'
ORDER BY order_date;

-- 54. Find products with low stock
SELECT * FROM products
WHERE stock_quantity < 20
ORDER BY stock_quantity ASC;

-- SECTION 9: SUBQUERIES

-- 55. Products priced above the overall average
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- 56. Find the most expensive product(s)
SELECT * FROM products
WHERE price = (SELECT MAX(price) FROM products);

-- 57. Customers who have placed at least one order
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);

-- SECTION 10: DDL EXAMPLES
-- These are reference examples. Do not run them automatically.

-- 58. Add a description column
-- ALTER TABLE products ADD COLUMN description TEXT;

-- 59. Rename a column
-- ALTER TABLE products RENAME COLUMN description TO product_description;

-- 60. Remove a column (destructive example; keep commented)
-- ALTER TABLE products DROP COLUMN description;

-- SECTION 11: INDEX AND QUERY PERFORMANCE

-- 61. Review a query execution plan
EXPLAIN
SELECT * FROM orders WHERE customer_id = 1;

-- 62. Check existing indexes on a table
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'products';

-- SECTION 12: SAFE CRUD PRACTICE
-- This transaction is rolled back, so it does not permanently
-- change your practice database.
-- Run this section separately if you want to practise CRUD.

BEGIN;

-- 63. Insert a temporary product
INSERT INTO products
    (product_name, category, price, stock_quantity)
VALUES
    ('Temporary SQL Practice Product', 'Practice', 999, 5)
RETURNING *;

-- 64. Read the temporary product
SELECT * FROM products
WHERE product_name = 'Temporary SQL Practice Product';

-- 65. Update the temporary product
UPDATE products
SET price = 1099
WHERE product_name = 'Temporary SQL Practice Product'
RETURNING *;

-- 66. Delete the temporary product
DELETE FROM products
WHERE product_name = 'Temporary SQL Practice Product'
RETURNING *;

-- Undo all changes made in this practice transaction
ROLLBACK;

-- END OF DAY 8 SQL PRACTICE QUERIES
