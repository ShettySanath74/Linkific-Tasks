# Data Dictionary

- `dim_date`: `date_key` (YYYYMMDD key), `full_date`, day name/number, weekday, week, month, quarter, year, weekend and holiday flags.
- `dim_customer`: generated `customer_key`, source `customer_id`, name, city, effective start/end dates, current flag. SCD Type 2.
- `dim_product`: generated `product_key`, source `product_id`, product name and category. SCD Type 1.
- `fact_sales`: generated `sales_key`, order ID and line number, three dimension foreign keys, quantity, unit price and sales amount.
