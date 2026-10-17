
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("DAY 6: END-TO-END DATA ENGINEERING PIPELINE")
print("=" * 65)

# STEP 1: Create employee and department datasets
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105],
    "employee_name": ["Asha", "Ravi", "Meera", "Kiran", "Neha"],
    "department_id": [1, 2, 1, 3, 2]
})

departments = pd.DataFrame({
    "department_id": [1, 2, 3],
    "department_name": ["Engineering", "Analytics", "Marketing"]
})

employees.to_csv(DATA_DIR / "pipeline_employees.csv", index=False)
departments.to_csv(DATA_DIR / "pipeline_departments.csv", index=False)

# STEP 2: Merge employee and department data
employee_details = employees.merge(
    departments,
    on="department_id",
    how="left",
    validate="many_to_one"
)

employee_details.to_csv(
    OUTPUT_DIR / "pipeline_employee_details.csv",
    index=False
)

print("\n1. MERGED EMPLOYEE DETAILS")
print(employee_details)

# STEP 3: Create daily sales records
rng = np.random.default_rng(42)

dates = pd.date_range(
    start="2026-01-01",
    periods=90,
    freq="D"
)

daily_sales = pd.DataFrame({
    "date": dates,
    "sales": rng.integers(1000, 6000, size=len(dates))
})

daily_sales.to_csv(DATA_DIR / "pipeline_daily_sales.csv", index=False)

# STEP 4: Analyze time series
daily_sales["date"] = pd.to_datetime(daily_sales["date"])
daily_sales = daily_sales.set_index("date")

daily_sales["rolling_7_day_average"] = (
    daily_sales["sales"].rolling(window=7, min_periods=1).mean()
)

weekly_sales = daily_sales[["sales"]].resample("W").sum()
weekly_sales = weekly_sales.rename(
    columns={"sales": "weekly_sales"}
)

weekly_sales.to_csv(OUTPUT_DIR / "pipeline_weekly_sales.csv")
daily_sales.to_csv(OUTPUT_DIR / "pipeline_daily_analysis.csv")

print("\n2. WEEKLY SALES SUMMARY")
print(weekly_sales.head())

# STEP 5: Create summary reports
department_summary = (
    employee_details.groupby("department_name", as_index=False)
    .agg(employee_count=("employee_id", "count"))
)

sales_summary = pd.DataFrame({
    "metric": ["Total sales", "Average daily sales", "Highest daily sales"],
    "value": [
        daily_sales["sales"].sum(),
        daily_sales["sales"].mean(),
        daily_sales["sales"].max()
    ]
})

print("\n3. DEPARTMENT SUMMARY")
print(department_summary)

print("\n4. SALES SUMMARY")
print(sales_summary)

# STEP 6: Export all reports into one Excel workbook
excel_file = OUTPUT_DIR / "day6_data_engineering_report.xlsx"

with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
    employee_details.to_excel(
        writer, sheet_name="Employee Details", index=False
    )
    department_summary.to_excel(
        writer, sheet_name="Department Summary", index=False
    )
    daily_sales.reset_index().to_excel(
        writer, sheet_name="Daily Sales", index=False
    )
    weekly_sales.to_excel(
        writer, sheet_name="Weekly Sales"
    )
    sales_summary.to_excel(
        writer, sheet_name="Sales Summary", index=False
    )

    workbook = writer.book
    header_format = workbook.add_format({
        "bold": True,
        "font_color": "white",
        "bg_color": "#1F4E78",
        "border": 1
    })

    for sheet_name, worksheet in writer.sheets.items():
        worksheet.freeze_panes(1, 0)
        worksheet.set_column("A:Z", 20)

        # Format header cells using their actual column names
        if sheet_name == "Employee Details":
            headers = employee_details.columns
        elif sheet_name == "Department Summary":
            headers = department_summary.columns
        elif sheet_name == "Daily Sales":
            headers = ["date", "sales", "rolling_7_day_average"]
        elif sheet_name == "Weekly Sales":
            headers = ["date", "weekly_sales"]
        else:
            headers = sales_summary.columns

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

print("\n5. EXCEL REPORT CREATED")
print(excel_file)

# STEP 7: Verify the workbook
with pd.ExcelFile(excel_file) as workbook:
    print("\nExcel sheets:", workbook.sheet_names)

print("\nPIPELINE COMPLETED SUCCESSFULLY!")
print("All project files are saved inside the Day 6 folder.")
