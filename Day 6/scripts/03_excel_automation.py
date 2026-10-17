
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("DAY 6: EXCEL AUTOMATION")
print("=" * 60)

# 1. Create sample business data
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105],
    "name": ["Asha", "Ravi", "Meera", "Kiran", "Neha"],
    "department": [
        "Engineering", "Analytics", "Engineering",
        "Marketing", "Analytics"
    ],
    "salary": [65000, 58000, 72000, 49000, 61000],
    "city": ["Bengaluru", "Mangaluru", "Bengaluru", "Udupi", "Mysuru"]
})

sales = pd.DataFrame({
    "month": ["January", "February", "March", "April", "May"],
    "revenue": [120000, 145000, 138000, 162000, 175000],
    "expenses": [80000, 90000, 85000, 97000, 102000]
})

sales["profit"] = sales["revenue"] - sales["expenses"]

# 2. Create an input Excel workbook with multiple sheets
input_file = DATA_DIR / "business_data.xlsx"

with pd.ExcelWriter(input_file, engine="openpyxl") as writer:
    employees.to_excel(writer, sheet_name="Employees", index=False)
    sales.to_excel(writer, sheet_name="Monthly Sales", index=False)

print(f"\nCreated input workbook: {input_file}")

# 3. Read one sheet
employees_read = pd.read_excel(
    input_file,
    sheet_name="Employees"
)

print("\nEmployees sheet:")
print(employees_read.head())

# 4. Read all sheets at once
all_sheets = pd.read_excel(input_file, sheet_name=None)

print("\nAvailable sheets:")
for sheet_name, dataframe in all_sheets.items():
    print(f"{sheet_name}: {len(dataframe)} rows")

# 5. Generate summary reports
department_summary = (
    employees_read.groupby("department", as_index=False)
    .agg(
        employee_count=("employee_id", "count"),
        average_salary=("salary", "mean"),
        total_salary=("salary", "sum")
    )
)

sales_read = all_sheets["Monthly Sales"].copy()
sales_read["profit_margin_percent"] = (
    sales_read["profit"] / sales_read["revenue"] * 100
).round(2)

# 6. Write an automated multi-sheet Excel report
report_file = OUTPUT_DIR / "automated_business_report.xlsx"

with pd.ExcelWriter(
    report_file,
    engine="xlsxwriter",
    datetime_format="yyyy-mm-dd"
) as writer:
    employees_read.to_excel(
        writer, sheet_name="Employees", index=False
    )
    department_summary.to_excel(
        writer, sheet_name="Department Summary", index=False
    )
    sales_read.to_excel(
        writer, sheet_name="Monthly Sales", index=False
    )

    # 7. Format the worksheets
    workbook = writer.book

    header_format = workbook.add_format({
        "bold": True,
        "bg_color": "#1F4E78",
        "font_color": "white",
        "border": 1
    })

    money_format = workbook.add_format({
        "num_format": "₹#,##0.00"
    })

    percent_format = workbook.add_format({
        "num_format": "0.00%"
    })

    for sheet_name, dataframe in [
        ("Employees", employees_read),
        ("Department Summary", department_summary),
        ("Monthly Sales", sales_read)
    ]:
        worksheet = writer.sheets[sheet_name]

        # Format column headings
        for col_num, column_name in enumerate(dataframe.columns):
            worksheet.write(0, col_num, column_name, header_format)

        # Set readable column widths
        worksheet.set_column(
            0, len(dataframe.columns) - 1, 18
        )

        # Freeze the header row and add filters
        worksheet.freeze_panes(1, 0)
        worksheet.autofilter(
            0, 0, len(dataframe), len(dataframe.columns) - 1
        )

    # Format salary and financial columns
    writer.sheets["Employees"].set_column(3, 3, 18, money_format)

    writer.sheets["Department Summary"].set_column(
        2, 3, 20, money_format
    )

    writer.sheets["Monthly Sales"].set_column(
        1, 3, 18, money_format
    )

    # Excel stores percentages as fractions, so divide by 100
    # only if the column is written as a fraction. Here the data
    # already contains percentage points (e.g. 25.0), so use 0.00%.
    # Convert to fractions for correct percentage formatting.
    sales_read["profit_margin_fraction"] = (
        sales_read["profit_margin_percent"] / 100
    )

    sales_read.to_excel(
        writer, sheet_name="Monthly Sales", index=False
    )

print(f"\nExcel report saved to: {report_file}")

# 8. Verify the generated workbook
check = pd.ExcelFile(report_file)
print("\nReport sheets:", check.sheet_names)

print("\nDepartment summary:")
print(department_summary)

print("\nMonthly sales report:")
print(sales_read)

print("\nExcel automation completed!")
