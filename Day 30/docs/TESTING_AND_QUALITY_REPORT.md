# Testing and Data Quality Report

## Data quality validation
Recorded Day 29 report:
- CSV files scanned: 4
- Status `ok`: 4
- Status `review`: 0
- Status `failed`: 0

Files scanned:
- `customers.csv`: 150 rows, 5 columns
- `order_items.csv`: 1,326 rows, 7 columns
- `orders.csv`: 850 rows, 5 columns
- `products.csv`: 20 rows, 5 columns

The report recorded no blank cells, duplicate rows, inconsistent rows, or nulls in these files.

## Automated test evidence
Command:
```powershell
python -m unittest discover -s ".\Day 29\tests" -v
```

Recorded result: six tests ran and all passed.

Test cases:
- duplicate headers
- empty file
- inconsistent row width
- blank cell flagged for review
- clean CSV
- duplicate row flagged

## Scope and limitations
The validator checks structural CSV issues. It does not enforce every business rule, such as valid order totals, referential integrity across every table, or business-specific date constraints. Those checks require explicit rules and should be added if required by the project.
