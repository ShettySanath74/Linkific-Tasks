# Live Demo Script (Suggested 8–10 Minutes)

## 1. Introduce the project (45 seconds)
"This project analyzes a synthetic retail dataset. I used CSV source tables, Python and SQL for analysis, and Power BI for presenting the results."

## 2. Show the source data model (1 minute)
Open `Day 28/data/` and explain customers, orders, order_items, and products. Point out the one-to-many relationships.

## 3. Show validation evidence (1 minute)
Open `Day 29/outputs/data_quality_report.json`. Explain that four CSV files were scanned and all four were marked OK. Mention that the validator checks structural issues and does not replace business-rule validation.

## 4. Show analytical SQL and KPI output (2 minutes)
Open `Day 28/sql/analytical_queries.sql` and the executive summary. Explain that only Completed orders contribute to revenue and estimated profit.

## 5. Show the Power BI dashboard (2 minutes)
Open the PBIX in Power BI Desktop. Before presenting, manually verify that the file opens, visuals render, relationships are correct, and filters work. Do not rely only on the file's existence.

## 6. Explain testing and optimization (2 minutes)
Show the Day 29 unit-test output and SQL optimization report. Explain that six queries improved and four regressed; this led to a recommendation to inspect query plans.

## 7. Close (30 seconds)
Summarize the business findings and the next improvements.

## Demo safety
- Keep the dataset described as synthetic.
- Say CU (generic currency units), not INR.
- Do not claim Airflow execution unless a working DAG run is separately demonstrated.
- If a live application fails, explain the verified saved artifacts instead of claiming the live feature worked.
