# Optimization Notes – Day 27

Implemented optimizations and measured experiments:

1. SQLite batch writes use `executemany` rather than one insert call per row.
2. A composite index on `(customer_id, sale_date)` supports common filtered lookups.
3. Validation precomputes the customer ID set once per transformation rather than rebuilding it for every sale.
4. The benchmark records indexed and unindexed query timings plus the SQLite query plan.
5. Threaded validation is benchmarked against sequential validation; threading is not assumed to be faster.
6. SQLite connections are explicitly closed after transaction handling to release file handles reliably on Windows.

See `PERFORMANCE_REPORT.md` and `outputs/performance/performance_report.json` for measured values from the latest successful run. The index benefit varies by data volume; for small datasets, index maintenance/lookup overhead can outweigh the benefit.
