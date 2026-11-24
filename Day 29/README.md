# Day 29 – Final Documentation, Testing, Optimization & Presentation

## Purpose
This package provides a practical finalization toolkit for the Linkific Business Intelligence / Analytics project. It includes documentation templates, reusable CSV data-quality and performance checks, automated tests, and presentation materials.

> **Important:** This package is designed to be copied into the repository alongside `Day 28`. It does not assume an undocumented database schema or claim that the user's actual Day 28 pipeline has already passed. Run the checks against the real Day 28 data and record the generated results before marking them complete.

## Learning objectives
- Document architecture, data definitions, ETL workflow, and dashboard usage.
- Validate input data and test edge cases.
- Measure script runtime and basic dataset characteristics.
- Identify optimization opportunities without changing business logic blindly.
- Present the end-to-end data flow and dashboard.

## Folder structure
```text
Day 29/
├── README.md
├── config/
│   └── settings.json
├── docs/
│   ├── system_architecture.md
│   ├── data_dictionary.md
│   ├── etl_documentation.md
│   ├── user_guide.md
│   └── optimization_report.md
├── scripts/
│   ├── run_validation.py
│   └── benchmark_csv.py
├── tests/
│   ├── test_quality_checks.py
│   └── test_edge_cases.py
├── outputs/
│   └── .gitkeep
└── presentation/
    ├── demo_script.md
    ├── data_flow_walkthrough.md
    └── Day29_Final_Project_Presentation.pptx
```

## Requirements
- Python 3.10+ (the scripts use only the Python standard library).
- Optional: `pytest` to run the automated tests.
- Power BI Desktop to inspect and measure the `.pbix` dashboard manually.

## Setup (Windows PowerShell)
Run from the repository root:
```powershell
Set-Location "D:\Linkific-Tasks-Upload"
```
If the ZIP is extracted into the repository root, the expected path is `.\Day 29`.

## Run data-quality validation
```powershell
python ".\Day 29\scripts\run_validation.py" --data-dir ".\Day 28\data" --output-dir ".\Day 29\outputs"
```
The script scans CSV files, reports empty files, inconsistent row widths, blank cells, duplicate rows, and column-level null counts. It writes JSON and CSV reports. It does not impose business-specific rules such as valid order totals because those require the actual schema and business definitions.

## Benchmark CSV loading
```powershell
python ".\Day 29\scripts\benchmark_csv.py" --data-dir ".\Day 28\data" --output-dir ".\Day 29\outputs"
```
This measures elapsed time to read each CSV with Python's CSV reader and records row/column counts and file sizes. Results depend on the computer, disk, and current system load.

## Run automated tests
```powershell
python -m unittest discover -s ".\Day 29\tests" -v
```
No third-party test framework is required.

## Final verification checklist
1. Confirm the Day 28 source files are present.
2. Run validation and inspect both generated reports.
3. Run benchmark twice under similar conditions; record the measurements.
4. Inspect SQL queries and Power BI visuals manually.
5. Update the documentation with actual table names, transformations, test counts, and measurements.
6. Do not describe an optimization as successful unless a before/after measurement supports it.

## Limitations
- The package cannot inspect or modify Power BI visuals or model internals automatically.
- SQL tuning recommendations must be applied to the actual SQL/database engine and measured there.
- The data dictionary is a structured template until verified against the actual CSV headers and business definitions.
- No test result is pre-filled as passed. Generated reports are evidence to review, not an automatic sign-off.
