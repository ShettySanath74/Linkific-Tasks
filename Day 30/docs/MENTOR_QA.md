# Possible Mentor Questions and Suggested Answers

## Why did you use a synthetic dataset?
It provides a safe, repeatable dataset for practicing the workflow. The results demonstrate the analytical process and are not real company performance.

## Why are there four tables?
They separate customer, order, order-line, and product information. This reduces duplication and supports relational joins.

## Why calculate revenue only for Completed orders?
The documented business rule excludes Returned and Cancelled orders from revenue and profit calculations.

## How is estimated profit calculated?
Line revenue minus quantity multiplied by product unit cost. It is simplified and excludes shipping, tax, overhead, and refunds.

## Did indexing improve performance?
Not for every query. Six of ten queries became faster, while four became slower. The next step is to inspect query plans and tune query-specific indexes.

## What does the data-quality report prove?
It shows that four CSV files passed the implemented structural checks. It does not prove every business rule or cross-table relationship is valid.

## Is Airflow part of the verified implementation?
The available Day 28–29 documentation does not establish a verified Airflow execution for this project. I describe the workflow that is supported by the repository evidence.

## What would you improve next?
I would add business-rule and referential-integrity checks, inspect the regressed SQL query plans, verify Power BI interactions, and expand customer and profitability analysis.
