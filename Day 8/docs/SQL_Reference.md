
# SQL Quick Reference – PostgreSQL

## 1. Read Data
```sql
SELECT * FROM products;
SELECT product_name, price FROM products;
```

## 2. Filter Rows
```sql
SELECT * FROM products WHERE price > 1000;
SELECT * FROM products WHERE category IN ('Electronics', 'Furniture');
SELECT * FROM products WHERE price BETWEEN 500 AND 10000;
SELECT * FROM products WHERE product_name ILIKE '%o%';
```

## 3. Sort and Limit
```sql
SELECT * FROM products ORDER BY price DESC;
SELECT * FROM products ORDER BY price ASC LIMIT 3;
SELECT DISTINCT category FROM products;
```

## 4. Aggregate Data
```sql
SELECT COUNT(*) FROM products;
SELECT AVG(price) FROM products;
SELECT MIN(price), MAX(price) FROM products;
SELECT SUM(price * stock_quantity) FROM products;
```

## 5. Group Data
```sql
SELECT category, COUNT(*)
FROM products
GROUP BY category;

SELECT category, AVG(price)
FROM products
GROUP BY category
HAVING AVG(price) > 1000;
```

## 6. Join Tables
```sql
SELECT o.order_id, c.first_name, o.status
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id;

SELECT c.first_name, o.order_id
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;
```

## 7. Insert, Update, and Delete
```sql
INSERT INTO products (product_name, category, price, stock_quantity)
VALUES ('Example Product', 'Practice', 500, 10)
RETURNING *;

UPDATE products
SET price = 600
WHERE product_name = 'Example Product'
RETURNING *;

DELETE FROM products
WHERE product_name = 'Example Product'
RETURNING *;
```

Run data-modification examples carefully and use a test record.

## 8. Constraints
- PRIMARY KEY: uniquely identifies each row.
- FOREIGN KEY: enforces relationships between tables.
- NOT NULL: requires a value.
- UNIQUE: prevents duplicate values.
- CHECK: enforces a condition.
- DEFAULT: supplies a value when one is omitted.

## 9. Indexes and Performance
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'products';

EXPLAIN
SELECT * FROM orders WHERE customer_id = 1;
```

## 10. Useful Notes
- `WHERE` filters rows before grouping.
- `HAVING` filters groups after aggregation.
- `COUNT(*)` counts rows.
- `INNER JOIN` returns matching rows.
- `LEFT JOIN` retains every row from the left table.
- `ILIKE` performs case-insensitive pattern matching in PostgreSQL.
- `RETURNING` displays rows affected by INSERT, UPDATE, or DELETE.
