# Day 29 - SQL Optimization and Performance Report

## 1. Objective

Evaluate SQL query performance in the Day 28 Business Intelligence project.
Test SQLite indexes using a separate copy of the original database and compare
execution time and query correctness.

## 2. Testing Environment

- Database: SQLite
- Source database: Day 28/data/sales_analytics.db
- Test database: Day 29/outputs/sales_analytics_optimization_test.db
- SQL source: Day 28/sql/analytical_queries.sql
- Queries tested: 10
- Measurement: Five-run average after one warm-up execution

The original database was not modified.

## 3. Indexes Tested

1. idx_orders_status_date
   - orders(order_status, order_date)
2. idx_orders_status_customer
   - orders(order_status, customer_id)
3. idx_order_items_order
   - order_items(order_id)
4. idx_order_items_product
   - order_items(product_id)
5. idx_customers_customer
   - customers(customer_id)
6. idx_products_product
   - products(product_id)

## 4. Benchmark Results

| Query | Baseline (sec) | Indexed (sec) | Change |
|---|---:|---:|---:|
| Executive KPI | 0.025592 | 0.026582 | -3.87% |
| Monthly revenue | 0.023685 | 0.034060 | -43.80% |
| Category performance | 0.026019 | 0.031062 | -19.38% |
| Product ranking | 0.028392 | 0.043416 | -52.91% |
| Regional comparison | 0.025251 | 0.019876 | +21.29% |
| Customer lifetime value | 0.036262 | 0.023588 | +34.95% |
| Order status mix | 0.004587 | 0.000882 | +80.77% |
| Average order value | 0.019095 | 0.018901 | +1.02% |
| Discount analysis | 0.020194 | 0.014214 | +29.61% |
| Month-over-month growth | 0.038191 | 0.017154 | +55.08% |

Positive percentages represent lower execution time. Negative percentages
represent slower execution.

## 5. Overall Findings

- Combined baseline execution time: 0.247268 seconds.
- Combined indexed execution time: 0.229735 seconds.
- Combined execution time decreased by approximately 7.09%.
- Six queries became faster.
- Four queries became slower.
- Query 7 showed the largest measured improvement.
- Query 4 showed the largest measured regression.

These results are specific to the available dataset and test environment.

## 6. Correctness and Integrity Verification

Both the original and indexed database returned "ok" from SQLite
PRAGMA integrity_check.

All 10 analytical queries were executed against both databases.
Every query returned identical results, including identical row counts.

Result: 10 out of 10 queries matched.

## 7. Recommendations

- Do not apply all tested indexes automatically.
- Review query execution plans before selecting production indexes.
- Retest with larger datasets to understand scalability.
- Repeat measurements under comparable conditions.
- Consider index storage and write-operation overhead.
- Keep the original database unchanged until improvements are validated.

## 8. Limitations

The dataset is relatively small. Execution times are measured in milliseconds
and can be affected by caching, system activity, and SQLite query planning.

The combined 7.09% reduction is an observed benchmark result, not a guaranteed
production improvement. The test compares the original database with a copy
containing all six indexes; it does not isolate the contribution of each index.

## 9. Conclusion

The indexing experiment preserved database integrity and analytical query
results. It reduced combined execution time in this particular benchmark,
although performance varied across individual queries.

Further testing with larger datasets and individual index comparisons is
recommended before production adoption.
