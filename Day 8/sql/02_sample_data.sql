
-- Day 8: E-commerce Sample Data
-- Run this file only once on a fresh database.

-- 1. Customers
INSERT INTO customers (first_name, last_name, email, city)
VALUES
('Sanath', 'Shetty', 'sanath@example.com', 'Mangalore'),
('Asha', 'Rao', 'asha@example.com', 'Bangalore'),
('Rahul', 'Kumar', 'rahul@example.com', 'Mysore'),
('Meera', 'Pai', 'meera@example.com', 'Udupi'),
('Arjun', 'Sharma', 'arjun@example.com', 'Bangalore');

-- 2. Products
INSERT INTO products (product_name, category, price, stock_quantity)
VALUES
('Laptop', 'Electronics', 65000.00, 10),
('Mouse', 'Electronics', 800.00, 50),
('Office Chair', 'Furniture', 7500.00, 15),
('Notebook', 'Stationery', 100.00, 100),
('Keyboard', 'Electronics', 1500.00, 30),
('Desk', 'Furniture', 12000.00, 8),
('Pen Pack', 'Stationery', 250.00, 75);

-- 3. Orders
INSERT INTO orders (customer_id, order_date, status)
VALUES
(1, '2026-10-10 10:00:00', 'Delivered'),
(2, '2026-10-12 14:30:00', 'Shipped'),
(3, '2026-10-15 09:15:00', 'Pending'),
(1, '2026-10-18 16:00:00', 'Processing'),
(4, '2026-10-19 11:45:00', 'Delivered');

-- 4. Order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 1, 65000.00),
(1, 2, 2, 800.00),
(2, 3, 1, 7500.00),
(2, 4, 5, 100.00),
(3, 5, 2, 1500.00),
(4, 6, 1, 12000.00),
(4, 7, 3, 250.00),
(5, 2, 1, 800.00);
