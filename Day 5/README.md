\# Day 5 — Pandas for Data Engineering



\## 1. Overview



This module covers data manipulation, cleaning, transformation, aggregation, and analysis using Python Pandas.



\## 2. Learning Objectives



\- Create and inspect Pandas DataFrames.

\- Read and export data in CSV format.

\- Handle missing values and duplicate records.

\- Convert data types and standardize text.

\- Create new columns and transform existing data.

\- Use sorting, ranking, mapping, and categorization.

\- Perform GroupBy aggregations and multi-level analysis.

\- Create pivot tables and cross-tabulations.

\- Build a basic end-to-end sales data analysis workflow.



\## 3. Project Structure



\- `data/` — Input datasets.

\- `scripts/` — Python scripts for Pandas exercises.

\- `notebooks/` — Space for interactive Jupyter notebooks.

\- `outputs/` — Cleaned datasets and analysis reports.

\- `docs/` — Supporting documentation.

\- `requirements.txt` — Python dependencies.



\## 4. Scripts



| Script | Description |

|---|---|

| `01\_dataframe\_fundamentals.py` | DataFrame creation, inspection, selection, and filtering |

| `02\_data\_cleaning.py` | Missing values, duplicates, text cleaning, and type conversion |

| `03\_data\_transformation.py` | Calculated columns, mapping, sorting, ranking, binning, pivot, and melt |

| `04\_groupby\_aggregations.py` | GroupBy summaries, aggregations, pivot tables, and cross-tabulations |

| `05\_sales\_analysis\_project.py` | End-to-end sales data cleaning and analysis |



\## 5. Key Pandas Operations



\- `pd.DataFrame()` — Create a DataFrame.

\- `pd.read\_csv()` — Load a CSV file.

\- `head()`, `tail()`, `info()`, `describe()` — Inspect data.

\- `isnull()` and `fillna()` — Identify and handle missing values.

\- `drop\_duplicates()` — Remove duplicate rows.

\- `astype()` and `to\_numeric()` — Convert data types.

\- `groupby()` and `agg()` — Summarize grouped records.

\- `pivot\_table()` and `crosstab()` — Analyze relationships between categories.

\- `sort\_values()` and `rank()` — Sort and rank records.

\- `to\_csv()` — Export results.



\## 6. Sales Analysis Workflow



1\. Create or load raw sales data.

2\. Inspect missing values and data types.

3\. Remove duplicate rows according to the selected rule.

4\. Standardize text and convert numeric fields.

5\. Calculate sales value, discount, and final sales.

6\. Generate city-level and category-level summaries.

7\. Create a city-by-category pivot table.

8\. Export cleaned data and reports to `outputs/`.



\## 7. Expected Outputs



\- `outputs/cleaned\_sales.csv`

\- `outputs/transformed\_sales.csv`

\- `outputs/category\_sales\_pivot.csv`

\- `outputs/sales\_melted.csv`

\- `outputs/sales\_with\_group\_metrics.csv`

\- `outputs/category\_summary.csv`

\- `outputs/city\_category\_pivot.csv`

\- `outputs/city\_category\_crosstab.csv`

\- `outputs/cleaned\_sales\_analysis.csv`

\- `outputs/category\_sales\_report.csv`

\- `outputs/city\_sales\_report.csv`

\- `outputs/city\_category\_sales\_pivot.csv`



The files listed above are expected outputs from the corresponding scripts. Verify that each script has run successfully before marking its output as completed.



\## 8. Installation and Execution



Install the required libraries:



```powershell

C:\\Python314\\python.exe -m pip install -r requirements.txt

```



Run an individual exercise from the Day 5 directory:



```powershell

C:\\Python314\\python.exe scripts/01\_dataframe\_fundamentals.py

```



Run the sales analysis project:



```powershell

C:\\Python314\\python.exe scripts/05\_sales\_analysis\_project.py

```



\## 9. Important Data Quality Considerations



\- Validate business identifiers before removing duplicates.

\- Choose missing-value handling rules based on business requirements.

\- Check data types before performing calculations.

\- Validate calculated metrics and aggregation results.

\- Keep raw input data separate from processed outputs.



\## 10. Learning Outcome



This module provides practical experience in using Pandas for tabular data processing, data quality checks, transformation, aggregation, and report generation.



