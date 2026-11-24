# System Architecture – Day 28 Analytics Project

## Status
This document is a documentation framework for the existing Day 28 project. Confirm each component against the actual repository and update any inaccurate or missing details before submission.

## Logical architecture
```text
Source CSV files
(customers, orders, order items, products)
             |
             v
   Python / SQL data preparation
             |
             v
 Data cleaning, transformation & analysis
             |
             v
 Analytical datasets / summary outputs
             |
             v
      Power BI semantic model
             |
             v
 Sales performance dashboard
             |
             v
 Business users / mentor
```

## Components to verify
| Layer | Expected responsibility | Evidence to record |
|---|---|---|
| Source | Store raw business entities and transactions | Actual filenames, row counts |
| Preparation | Load, inspect, clean, and transform data | Script/notebook names |
| Analysis | Calculate KPIs and business summaries | SQL files, Python outputs |
| Presentation | Expose metrics and trends | PBIX file, page/visual names |
| Consumption | Support business decisions | User guide and demo |

## Data flow
1. Source CSV files are read by the project's actual Python/SQL workflow.
2. Data is cleaned and transformed according to implemented rules.
3. Analytical queries and scripts produce summarized outputs.
4. Power BI consumes the configured data sources and presents measures and visuals.
5. Users apply filters and interpret the reported metrics.

## To finalize
Replace generic layer descriptions with exact script names, database/table names (if any), refresh method, relationships, measures, and source-to-target mappings. Do not list a database or orchestration tool unless it is actually used.
