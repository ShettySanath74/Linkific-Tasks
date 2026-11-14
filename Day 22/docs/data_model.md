# Data Model — Star Schema

## Grain
One row in `fact_sales` represents one product line within one customer order. If an order contains three products, it contributes three fact rows.

## Entity relationship diagram
```mermaid
erDiagram
    DIM_DATE ||--o{ FACT_SALES : date_key
    DIM_CUSTOMER ||--o{ FACT_SALES : customer_key
    DIM_PRODUCT ||--o{ FACT_SALES : product_key
    DIM_LOCATION ||--o{ FACT_SALES : location_key

    DIM_DATE {
        int date_key PK
        date date_value
        int day
        int month
        string month_name
        int quarter
        int year
    }
    DIM_CUSTOMER {
        int customer_key PK
        string source_customer_id
        string customer_name
        string customer_segment
    }
    DIM_PRODUCT {
        int product_key PK
        string source_product_id
        string product_name
        string category
        decimal current_price
    }
    DIM_LOCATION {
        int location_key PK
        string city
        string state
        string country
    }
    FACT_SALES {
        bigint sales_key PK
        string source_order_id
        string source_order_item_id
        int date_key FK
        int customer_key FK
        int product_key FK
        int location_key FK
        int quantity
        decimal unit_price
        decimal discount_amount
        decimal sales_amount
    }
```

## Tables
- `dim_date`: calendar attributes used for time-based analysis.
- `dim_customer`: descriptive customer attributes.
- `dim_product`: product name, category, and price attributes.
- `dim_location`: city/state/country attributes.
- `fact_sales`: measurable sales activity at order-item grain.

## Inventory design note
Inventory is a separate business process and has a different grain: one snapshot per product, location, and snapshot date. A later implementation can add `fact_inventory_snapshot` linked to `dim_product`, `dim_location`, and `dim_date`. Do not mix inventory snapshot quantities into the sales fact table.
