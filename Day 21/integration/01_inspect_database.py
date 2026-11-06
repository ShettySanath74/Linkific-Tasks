
import sqlite3

db_path = r"Day 21\data\databases\company.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

tables = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("DATABASE TABLES")
print("----------------")

for (table_name,) in tables:
    print(f"\nTable: {table_name}")

    columns = cursor.execute(
        f'PRAGMA table_info("{table_name}")'
    ).fetchall()

    print("Columns:", [column[1] for column in columns])

    rows = cursor.execute(
        f'SELECT * FROM "{table_name}" LIMIT 5'
    ).fetchall()

    print("Sample records:")
    for row in rows:
        print(row)

connection.close()
