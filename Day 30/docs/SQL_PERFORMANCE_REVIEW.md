# SQL Performance Review

## Method
The recorded report used five-run averages after one warm-up, on the same database copy. Six indexes were created:

- `idx_orders_status_date`
- `idx_orders_status_customer`
- `idx_order_items_order`
- `idx_order_items_product`
- `idx_customers_customer`
- `idx_products_product`

## Results
Positive percentages indicate faster execution; negative percentages indicate slower execution.

| Query | Baseline (s) | Indexed (s) | Change |
|---|---:|---:|---:|
| 1 | 0.025592 | 0.026582 | -3.87% |
| 2 | 0.023685 | 0.034060 | -43.80% |
| 3 | 0.026019 | 0.031062 | -19.38% |
| 4 | 0.028392 | 0.043416 | -52.91% |
| 5 | 0.025251 | 0.019876 | +21.29% |
| 6 | 0.036262 | 0.023588 | +34.95% |
| 7 | 0.004587 | 0.000882 | +80.77% |
| 8 | 0.019095 | 0.018901 | +1.02% |
| 9 | 0.020194 | 0.014214 | +29.61% |
| 10 | 0.038191 | 0.017154 | +55.08% |

## Interpretation
- 6 of 10 queries became faster.
- 4 of 10 queries became slower.
- Largest measured improvement: Query 7 (+80.77%).
- Largest regression: Query 4 (-52.91%).

## Recommended next steps
1. Inspect `EXPLAIN QUERY PLAN` for each regressed query.
2. Check whether the new indexes are used effectively.
3. Compare query predicates, join keys, and sort/group operations with index column order.
4. Re-run multiple measurements under similar conditions.
5. Keep an index only when its read benefit justifies storage and write-maintenance costs.

Do not report this as an overall guaranteed speedup. It is a mixed, query-dependent result.
