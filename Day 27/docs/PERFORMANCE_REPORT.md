# Performance Report – Day 27

Measurements from the successful full run in the build environment. Your Windows machine may produce different timings.

| Input rows | Accepted | Rejected | ETL elapsed | Input throughput | Indexed query | Unindexed query |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | 900 | 100 | 0.024s | 41,779 rows/s | 0.1514 ms | 0.1267 ms |
| 10,000 | 9,000 | 1,000 | 0.200s | 49,996 rows/s | 0.2206 ms | 0.6945 ms |
| 100,000 | 90,000 | 10,000 | 1.473s | 67,889 rows/s | 0.3115 ms | 6.0002 ms |

## Parallel-processing experiment

For 10,000 records, sequential validation took 0.00757 s and threaded validation took 0.00905 s. Measured parallel speedup: 0.837x. Threads were slower in this run, so sequential validation remains the recommended path for this CPU-bound workload.

## Notes

The benchmark measures full ETL elapsed time and input-record throughput. It compares a composite-index query with the same query after dropping the index and captures SQLite `EXPLAIN QUERY PLAN` output. These measurements are machine- and data-dependent; repeat runs before drawing general conclusions.
