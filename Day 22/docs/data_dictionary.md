# Data Dictionary

## fact_sales
| Column | Type | Description | Rule |
|---|---|---|---|
| sales_key | BIGINT | Warehouse row identifier | Primary key |
| source_order_id | VARCHAR | Source order identifier | Required |
| source_order_item_id | VARCHAR | Source order-line identifier | Required; part of source uniqueness |
| date_key | INTEGER | Order date dimension key | Foreign key |
| customer_key | INTEGER | Customer dimension key | Foreign key |
| product_key | INTEGER | Product dimension key | Foreign key |
| location_key | INTEGER | Location dimension key | Foreign key |
| quantity | INTEGER | Units purchased | Greater than zero |
| unit_price | NUMERIC(12,2) | Price per unit | Non-negative |
| discount_amount | NUMERIC(12,2) | Discount for the line | Non-negative |
| sales_amount | NUMERIC(12,2) | Net line sales | Non-negative |

## dim_customer
| Column | Type | Description |
|---|---|---|
| customer_key | SERIAL | Surrogate primary key |
| source_customer_id | VARCHAR | Original customer identifier; unique |
| customer_name | VARCHAR | Customer display name |
| customer_segment | VARCHAR | Optional segment |

## dim_product
| Column | Type | Description |
|---|---|---|
| product_key | SERIAL | Surrogate primary key |
| source_product_id | VARCHAR | Original product identifier; unique |
| product_name | VARCHAR | Product name |
| category | VARCHAR | Product category |
| current_price | NUMERIC(12,2) | Current listed price |

## dim_location
| Column | Type | Description |
|---|---|---|
| location_key | SERIAL | Surrogate primary key |
| city | VARCHAR | City |
| state | VARCHAR | State or region |
| country | VARCHAR | Country |

## dim_date
| Column | Type | Description |
|---|---|---|
| date_key | INTEGER | YYYYMMDD primary key |
| date_value | DATE | Calendar date |
| day | SMALLINT | Day of month |
| month | SMALLINT | Month number |
| month_name | VARCHAR | Month name |
| quarter | SMALLINT | Calendar quarter |
| year | SMALLINT | Calendar year |

## Common metadata for ingestion/staging
| Field | Description |
|---|---|
| source_system | Name of source API/file/system |
| extracted_at | Timestamp when data was extracted |
| batch_id | Identifier for one ingestion batch |
| record_status | Valid, rejected, or quarantined |
