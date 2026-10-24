
-- Day 11: Sample data for the e-commerce warehouse

BEGIN;

-- 1. Customer dimension
INSERT INTO dim_customer
    (customer_id, first_name, last_name, email, city)
VALUES
    (101, 'Rahul', 'Sharma', 'rahul@example.com', 'Bengaluru'),
    (102, 'Priya', 'Shetty', 'priya@example.com', 'Mangaluru'),
    (103, 'Amit', 'Kumar', 'amit@example.com', 'Mysuru'),
    (104, 'Sneha', 'Rao', 'sneha@example.com', 'Udupi')
ON CONFLICT (customer_id) WHERE is_current = TRUE
DO NOTHING;

-- 2. Product dimension
INSERT INTO dim_product (product_id, product_name, category, unit_price)
VALUES
    (201, 'Laptop', 'Electronics', 65000.00),
    (202, 'Mouse', 'Electronics', 850.00),
    (203, 'Office Chair', 'Furniture', 7500.00),
    (204, 'Notebook', 'Stationery', 100.00),
    (205, 'Keyboard', 'Electronics', 1500.00)
ON CONFLICT (product_id) DO NOTHING;

-- 3. Store / sales channel
INSERT INTO dim_store (store_id, store_name, sales_channel)
VALUES
    (1, 'Online Store', 'Online')
ON CONFLICT (store_id) DO NOTHING;

-- 4. Date dimension
INSERT INTO dim_date
    (date_key, full_date, day_number, month_number,
     month_name, quarter_number, year_number, day_of_week)
VALUES
    (20261020, DATE '2026-10-20', 20, 10, 'October', 4, 2026, 'Tuesday'),
    (20261021, DATE '2026-10-21', 21, 10, 'October', 4, 2026, 'Wednesday'),
    (20261022, DATE '2026-10-22', 22, 10, 'October', 4, 2026, 'Thursday'),
    (20261023, DATE '2026-10-23', 23, 10, 'October', 4, 2026, 'Friday'),
    (20261024, DATE '2026-10-24', 24, 10, 'October', 4, 2026, 'Saturday')
ON CONFLICT (date_key) DO NOTHING;

-- 5. Sales facts
-- Grain: one row per order item / product line
-- IDs 1001-1005 are sample warehouse orders, not source-system orders.
INSERT INTO fact_sales
    (order_id, order_item_id, customer_key,
     product_key, date_key, store_key, quantity, unit_price)
SELECT v.order_id, v.order_item_id,
       c.customer_key, p.product_key, v.date_key,
       s.store_key, v.quantity, v.unit_price
FROM (VALUES
    (1001, 1, 101, 201, 20261020, 1, 1, 65000.00::NUMERIC),
    (1001, 2, 101, 202, 20261020, 1, 2,   850.00::NUMERIC),
    (1002, 1, 102, 203, 20261021, 1, 1,  7500.00::NUMERIC),
    (1003, 1, 103, 205, 20261022, 1, 1,  1500.00::NUMERIC),
    (1004, 1, 104, 204, 20261023, 1, 5,   100.00::NUMERIC),
    (1005, 1, 102, 202, 20261024, 1, 3,   850.00::NUMERIC)
) AS v(order_id, order_item_id, customer_id, product_id,
       date_key, store_id, quantity, unit_price)
JOIN dim_customer c
    ON c.customer_id = v.customer_id
   AND c.is_current = TRUE
JOIN dim_product p ON p.product_id = v.product_id
JOIN dim_date d ON d.date_key = v.date_key
JOIN dim_store s ON s.store_id = v.store_id
ON CONFLICT (order_id, order_item_id) DO NOTHING;

COMMIT;
