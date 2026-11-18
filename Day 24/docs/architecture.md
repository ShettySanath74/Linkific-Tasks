# Architecture

```text
customers.csv -> clean + SCD2 -> dim_customer --products.csv  -> clean + SCD1 -> dim_product ----> fact_sales -> validation report
sales.csv ---------------------> date/key lookups /
sales.csv dates ---------------> dim_date
```

Relationships:
- `fact_sales.date_key` references `dim_date.date_key`
- `fact_sales.customer_key` references `dim_customer.customer_key`
- `fact_sales.product_key` references `dim_product.product_key`

Fact grain: one row per order line `(order_id, line_number)`.
Loading order: schema, date dimension, dimensions, facts, validation.
