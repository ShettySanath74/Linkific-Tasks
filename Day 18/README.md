# Day 18 – Regular Expressions and Data Cleaning

## Learning Objectives
- Practice regular expression patterns and Python's `re` module.
- Extract and validate common data formats.
- Clean customer data and parse application logs.

## Project Structure
- `scripts/regex_practice.py` – basic regex examples
- `scripts/pattern_library.py` – reusable regex patterns
- `scripts/clean_customer_data.py` – cleans customer records
- `scripts/log_parser.py` – extracts fields from log lines
- `data/customers.csv` – sample customer records
- `data/application.log` – sample application logs
- `outputs/cleaned_customers.csv` – cleaned customer data
- `outputs/parsed_logs.csv` – parsed log records

## Regex Concepts Practiced
- Literals and metacharacters
- Character classes and quantifiers
- Anchors, word boundaries, and groups
- `re.search()`, `re.match()`, `re.findall()`
- `re.sub()`, `re.compile()`, and regex flags

## Running the Scripts
Run these commands from the repository root in PowerShell:

```powershell
& C:\Python314\python.exe "Day 18\scripts\regex_practice.py"
& C:\Python314\python.exe "Day 18\scripts\pattern_library.py"
& C:\Python314\python.exe "Day 18\scripts\clean_customer_data.py"
& C:\Python314\python.exe "Day 18\scripts\log_parser.py"