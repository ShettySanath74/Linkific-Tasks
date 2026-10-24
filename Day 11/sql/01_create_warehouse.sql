
-- Day 11: E-commerce Data Warehouse
-- Star schema with customer SCD Type 2 support

-- 1. Customer dimension
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),

    effective_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_end_date DATE NOT NULL DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_customer_dates
        CHECK (effective_end_date >= effective_start_date)
);

-- Only one current version per source customer
CREATE UNIQUE INDEX IF NOT EXISTS
    uq_dim_customer_current
ON dim_customer (customer_id)
WHERE is_current = TRUE;

-- 2. Product dimension
CREATE TABLE IF NOT EXISTS dim_product (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    unit_price NUMERIC(12, 2),
    effective_start_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- 3. Date dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_number INT NOT NULL,
    month_number INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INT NOT NULL,
    year_number INT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL
);

-- 4. Store / sales-channel dimension
CREATE TABLE IF NOT EXISTS dim_store (
    store_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_id INT NOT NULL UNIQUE,
    store_name VARCHAR(150) NOT NULL,
    sales_channel VARCHAR(50)
);

-- 5. Sales fact table
-- Grain: one row per product line within a sales transaction
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT NOT NULL,
    order_item_id INT NOT NULL,

    customer_key BIGINT NOT NULL
        REFERENCES dim_customer(customer_key),
    product_key BIGINT NOT NULL
        REFERENCES dim_product(product_key),
    date_key INT NOT NULL
        REFERENCES dim_date(date_key),
    store_key BIGINT NOT NULL
        REFERENCES dim_store(store_key),

    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL
        CHECK (unit_price >= 0),
    sales_amount NUMERIC(14, 2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED,

    CONSTRAINT uq_fact_sales_order_item
        UNIQUE (order_id, order_item_id)
);

-- Useful indexes for common analytical joins
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer
    ON fact_sales(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product
    ON fact_sales(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date
    ON fact_sales(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_store
    ON fact_sales(store_key);
    