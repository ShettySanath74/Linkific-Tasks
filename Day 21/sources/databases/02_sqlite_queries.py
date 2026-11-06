
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "databases" / "company.db"

# Connect to database
connection = sqlite3.connect(DB_PATH)

# SQL query
query = """
SELECT
    customers.name,
    customers.city,
    sales.amount
FROM customers
INNER JOIN sales
ON customers.customer_id = sales.customer_id;
"""

# Execute query
cursor = connection.cursor()
cursor.execute(query)

# Display results
results = cursor.fetchall()

print("Customer Sales Report")
print("-" * 40)

for row in results:
    print(row)

connection.close()
