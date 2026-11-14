-- E-commerce analytical warehouse starter schema (PostgreSQL)

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,             -- YYYYMMDD
    date_value DATE NOT NULL UNIQUE,
    day SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter SMALLINT NOT NULL,
    year SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key BIGSERIAL PRIMARY KEY,
    source_customer_id VARCHAR(100) NOT NULL UNIQUE,
    customer_name VARCHAR(200),
    customer_segment VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_key BIGSERIAL PRIMARY KEY,
    source_product_id VARCHAR(100) NOT NULL UNIQUE,
    product_name VARCHAR(250) NOT NULL,
    category VARCHAR(150),
    current_price NUMERIC(12,2) CHECK (current_price IS NULL OR current_price >= 0)
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_key BIGSERIAL PRIMARY KEY,
    city VARCHAR(120),
    state VARCHAR(120),
    country VARCHAR(120),
    CONSTRAINT uq_dim_location UNIQUE (city, state, country)
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    source_order_id VARCHAR(100) NOT NULL,
    source_order_item_id VARCHAR(100) NOT NULL,
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    customer_key BIGINT NOT NULL REFERENCES dim_customer(customer_key),
    product_key BIGINT NOT NULL REFERENCES dim_product(product_key),
    location_key BIGINT REFERENCES dim_location(location_key),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (discount_amount >= 0),
    sales_amount NUMERIC(12,2) NOT NULL CHECK (sales_amount >= 0),
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_fact_sales_source_line UNIQUE (source_order_id, source_order_item_id)
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales(customer_key);

-- Inventory is a separate fact process with a different grain.
CREATE TABLE IF NOT EXISTS fact_inventory_snapshot (
    inventory_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    product_key BIGINT NOT NULL REFERENCES dim_product(product_key),
    location_key BIGINT NOT NULL REFERENCES dim_location(location_key),
    quantity_on_hand INTEGER NOT NULL CHECK (quantity_on_hand >= 0),
    reorder_threshold INTEGER CHECK (reorder_threshold IS NULL OR reorder_threshold >= 0),
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_inventory_snapshot UNIQUE (date_key, product_key, location_key)
);
