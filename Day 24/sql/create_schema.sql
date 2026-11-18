PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS dim_date (
 date_key INTEGER PRIMARY KEY, full_date TEXT NOT NULL UNIQUE,
 day_number INTEGER NOT NULL, day_name TEXT NOT NULL, day_of_week INTEGER NOT NULL,
 week_of_year INTEGER NOT NULL, month_number INTEGER NOT NULL, month_name TEXT NOT NULL,
 quarter_number INTEGER NOT NULL, year_number INTEGER NOT NULL,
 is_weekend INTEGER NOT NULL CHECK(is_weekend IN (0,1)),
 is_holiday INTEGER NOT NULL CHECK(is_holiday IN (0,1)), holiday_name TEXT
);
CREATE TABLE IF NOT EXISTS dim_customer (
 customer_key INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT NOT NULL,
 customer_name TEXT NOT NULL, city TEXT NOT NULL, effective_start_date TEXT NOT NULL,
 effective_end_date TEXT NOT NULL, is_current INTEGER NOT NULL CHECK(is_current IN (0,1)),
 UNIQUE(customer_id,effective_start_date)
);
CREATE TABLE IF NOT EXISTS dim_product (
 product_key INTEGER PRIMARY KEY AUTOINCREMENT, product_id TEXT NOT NULL UNIQUE,
 product_name TEXT NOT NULL, category TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fact_sales (
 sales_key INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT NOT NULL,
 line_number INTEGER NOT NULL, date_key INTEGER NOT NULL, customer_key INTEGER NOT NULL,
 product_key INTEGER NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>0),
 unit_price REAL NOT NULL CHECK(unit_price>=0), sales_amount REAL NOT NULL CHECK(sales_amount>=0),
 UNIQUE(order_id,line_number),
 FOREIGN KEY(date_key) REFERENCES dim_date(date_key),
 FOREIGN KEY(customer_key) REFERENCES dim_customer(customer_key),
 FOREIGN KEY(product_key) REFERENCES dim_product(product_key)
);
CREATE INDEX IF NOT EXISTS idx_customer_natural_current ON dim_customer(customer_id,is_current);
CREATE INDEX IF NOT EXISTS idx_product_natural ON dim_product(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_sales(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_sales(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_order ON fact_sales(order_id);
