# Dashboard Mockup and Requirements

## Page 1 — Executive Sales Overview
**KPI cards:** Total Revenue, Total Orders, Units Sold, Average Order Value.

**Charts:**
- Revenue trend by day/month (line chart)
- Revenue by category (bar chart)
- Top 10 products by revenue (horizontal bar chart)
- Orders by location (map or bar chart)

**Filters:** date range, category, location.

## Page 2 — Product Performance
- Revenue and units sold by product
- Top and bottom products
- Category contribution
- Discount impact

## Page 3 — Inventory Monitoring
- Total units on hand
- Products below reorder threshold
- Stock by location
- Inventory snapshot trend

## Wireframe
```text
+-----------------------------------------------------------+
| E-COMMERCE ANALYTICS             Date | Category | Location|
+--------------+--------------+--------------+---------------+
| Total Revenue| Total Orders | Units Sold   | Avg Order Value|
+--------------+--------------+--------------+---------------+
| Revenue Trend                 | Revenue by Category         |
| [Line chart]                  | [Bar chart]                 |
+-------------------------------+-----------------------------+
| Top Products                  | Sales by Location           |
| [Horizontal bar chart]        | [Map / bar chart]           |
+-------------------------------+-----------------------------+
```

## Core metric definitions
- Total Revenue = sum of `fact_sales.sales_amount`.
- Total Orders = distinct count of `source_order_id`.
- Units Sold = sum of `quantity`.
- Average Order Value = Total Revenue / Total Orders, with zero-denominator handling.
- Low Stock Products = count of products whose latest available stock is below the configured reorder threshold.

The dashboard is a design specification only; Power BI visuals are not yet implemented.
