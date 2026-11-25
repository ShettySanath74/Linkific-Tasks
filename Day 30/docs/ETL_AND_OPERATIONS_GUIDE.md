# ETL and Operations Guide

## Current documented workflow
1. Confirm the four source CSV files exist under `Day 28/data/`.
2. Run the Day 29 CSV validation script.
3. Review both the JSON and CSV quality reports.
4. Run the Python exploratory analysis notebook and/or the analytical SQL query pack as appropriate.
5. Review the generated KPI summary and charts.
6. Open the Power BI project in Power BI Desktop and inspect the model and visuals.

## Validation command
```powershell
python ".\Day 29\scripts\run_validation.py" --data-dir ".\Day 28\data" --output-dir ".\Day 29\outputs"
```

## Unit-test command
```powershell
python -m unittest discover -s ".\Day 29\tests" -v
```

## SQL query pack
Open `Day 28/sql/analytical_queries.sql` and execute the required query against the project's SQLite database.

## Operational checks
- Confirm source file paths and headers.
- Review row counts and validation statuses.
- Check that the analytical outputs correspond to the latest input data.
- Verify the Power BI data source path and refresh behavior manually.
- Record exceptions and changes to the workflow.

## Failure handling
The handover package does not claim automated retries, centralized logging, or scheduled orchestration. If these are added, document and test them explicitly.
