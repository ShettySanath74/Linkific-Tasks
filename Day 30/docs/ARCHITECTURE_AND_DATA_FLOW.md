# Architecture and Data Flow

## Implemented logical workflow
```text
customers.csv ─┐
orders.csv ────┼──> Python / SQL analysis ──> KPI summaries and chart outputs
order_items.csv┤              │
products.csv ──┘              └──> SQLite-compatible analytical queries
                                           │
                                           v
                                 Power BI semantic model
                                           │
                                           v
                                  Sales analytics report
                                           │
                                           v
                              Business interpretation / review
```

## Data model
- `customers (1) → orders (many)`
- `orders (1) → order_items (many)`
- `products (1) → order_items (many)`

Join keys:
- `customers.customer_id = orders.customer_id`
- `orders.order_id = order_items.order_id`
- `products.product_id = order_items.product_id`

## Technologies
- CSV for source data
- Python and pandas for analysis
- SQLite-compatible SQL for analytical queries
- Jupyter Notebook for exploratory analysis
- Power BI Desktop for semantic modeling and visualization

## Architecture boundaries
The available project documentation supports a local CSV/Python/SQL/Power BI workflow. It does not establish an Airflow-based orchestration layer or a production cloud deployment. Any such extension should be described as future work unless separately implemented and verified.
