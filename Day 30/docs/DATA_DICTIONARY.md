# Data Dictionary – Entity-Level Overview

> This is an entity-level summary based on the documented project model. Confirm exact column definitions against the current CSV headers and `Day 29/docs/data_dictionary.md` before treating this as a column-complete specification.

| Entity | Purpose | Relationship |
|---|---|---|
| customers | Customer dimension / customer attributes | One customer can have many orders |
| orders | Order-level transaction and status information | Each order belongs to a customer |
| order_items | Line-level product, quantity, and revenue details | Each line belongs to an order and a product |
| products | Product attributes, category, and unit cost | One product can appear in many order lines |

## Key fields referenced by the project
- `customer_id`: customer join key
- `order_id`: order join key
- `product_id`: product join key
- `status`: order status used to filter completed orders
- `line_revenue`: line revenue used in revenue calculation
- `quantity`: units used in estimated cost calculation
- `unit_cost`: product cost used in estimated profit calculation

## Metric rules
- Revenue includes only `Completed` orders.
- Returned and Cancelled orders are excluded.
- Revenue is the sum of `order_items.line_revenue`.
- Estimated profit is line revenue minus `quantity × product unit_cost`.
- The simplified profit model excludes shipping, tax, overhead, and refunds.
