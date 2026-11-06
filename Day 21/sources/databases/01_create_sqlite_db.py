
import sqlite3
from pathlib import Path

# Locate project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database location
DB_DIR = BASE_DIR / "data" / "databases"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "company.db"


def create_database():

    print("Connecting to SQLite database...")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Enable foreign key validation
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT
        )
    """)

    # Create sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY,
            customer_id TEXT,
            amount REAL,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # Sample customer records
    customers = [
        ("C001", "Rahul", "Bangalore"),
        ("C002", "Priya", "Mangalore"),
        ("C003", "Arjun", "Mysore")
    ]

    # Sample sales records
    sales = [
        ("S001", "C001", 5000),
        ("S002", "C002", 3500),
        ("S003", "C001", 2000)
    ]

    # Insert customers
    cursor.executemany("""
        INSERT OR REPLACE INTO customers
        (customer_id, name, city)
        VALUES (?, ?, ?)
    """, customers)

    # Insert sales
    cursor.executemany("""
        INSERT OR REPLACE INTO sales
        (sale_id, customer_id, amount)
        VALUES (?, ?, ?)
    """, sales)

    connection.commit()

    print("Database created successfully!")

    # Display customers
    cursor.execute("SELECT * FROM customers")
    print("\nCustomers:")
    for row in cursor.fetchall():
        print(row)

    # Display sales
    cursor.execute("SELECT * FROM sales")
    print("\nSales:")
    for row in cursor.fetchall():
        print(row)

    connection.close()


if __name__ == "__main__":
    create_database()
