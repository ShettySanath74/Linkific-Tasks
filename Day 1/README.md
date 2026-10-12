# Python Data Engineering Fundamentals

A beginner-friendly Python project demonstrating core programming concepts and practical data engineering workflows, including file processing, data validation, API integration, logging, and unit testing.

## Project Objectives

- Build a professional Python development environment.
- Practice Python data structures, functions, and error handling.
- Read and process CSV, JSON, and text files.
- Work with dates and timestamps.
- Fetch and process data from a REST API.
- Combine datasets and validate records.
- Build a basic ETL pipeline.
- Use logging and unit testing.
- Document setup and execution instructions.

## Technologies Used

- Python 3.14.7
- Visual Studio Code
- Python virtual environment (`venv`)
- CSV and JSON modules
- `datetime`, `pathlib`, `logging`, and `unittest`
- `requests` for API integration

## Project Structure

```text
python-data-engineering/
├── .venv/
├── data/
├── notebooks/
├── outputs/
│   └── logs/
├── scripts/
│   ├── 01_variables_types.py
│   ├── 02_lists_tuples_sets.py
│   ├── 03_dictionaries.py
│   ├── 04_comprehensions.py
│   ├── 05_functions_lambda.py
│   ├── 06_error_handling.py
│   ├── 07_file_handling.py
│   ├── 08_csv_processing.py
│   ├── 09_json_processing.py
│   ├── 10_datetime_processing.py
│   ├── 11_api_requests.py
│   ├── 12_log_processing.py
│   ├── 13_combine_csv_files.py
│   ├── 14_data_validation.py
│   ├── 15_mini_etl_pipeline.py
│   ├── 16_config.py
│   ├── 16_logging_demo.py
│   ├── salary_utils.py
│   └── test_salary_utils.py
└── README.md
```

*Note: Update this structure to match the files that actually exist in your project.*

## Environment Setup

### 1. Install Python

Install Python and verify the installation:

```powershell
python --version
```

### 2. Create a virtual environment

Run these commands from the project root:

```powershell
python -m venv .venv
```

### 3. Activate the environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the API dependency

The API example uses the `requests` library:

```powershell
python -m pip install requests
```

The other examples primarily use Python's standard library.

## Running the Scripts

Run commands from the project root. For example:

```powershell
python scripts/01_variables_types.py
```

Run other scripts by replacing the filename with the relevant script name.

Some scripts require sample input files in the `data/` folder. Run those scripts only after creating their required input files.

## Unit Testing

Run the salary utility tests with:

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

Review the terminal output to confirm whether the tests pass or fail.

## Data Processing Workflow

The project demonstrates a basic Extract, Transform, Load (ETL) workflow:

1. **Extract:** Read records from CSV files, JSON files, or an API.
2. **Transform:** Validate fields, clean values, filter records, and calculate summaries.
3. **Load:** Write processed data and rejected records to output files.

## Input and Output Directories

- `data/` — sample input datasets and log files.
- `outputs/` — generated CSV, JSON, and summary files.
- `outputs/logs/` — application log files.

Use synthetic or anonymized data for practice. Do not commit credentials, API keys, or confidential datasets.

## Troubleshooting

**Python is not recognized**

Verify your Python installation and check that the correct interpreter is selected in VS Code.

**ModuleNotFoundError: No module named 'requests'**

Activate the virtual environment and run:

```powershell
python -m pip install requests
```

**FileNotFoundError**

Check that the input file exists in the expected directory and that the script is being run from the project root.

**Unit tests cannot import a module**

Check that the module filename and import statement match, and run the test command from the project root.

## Project Status

This project is being developed incrementally as part of Python Data Engineering training. Mark individual scripts as complete only after verifying that they execute successfully.

## Learning Outcomes

The project is intended to build practical skills in Python programming, file processing, API integration, data quality checks, ETL fundamentals, logging, testing, and technical documentation.