
import psycopg2
from psycopg2 import sql

from dotenv import load_dotenv
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
load_dotenv(os.path.join(PROJECT_ROOT, "Day 10", ".env"))


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ecommerce_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


def main():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:

                # 1. Execute a SELECT query and fetch multiple rows
                cursor.execute("""
                    SELECT product_id, product_name, price
                    FROM products
                    ORDER BY price DESC
                    LIMIT 5;
                """)

                print("\n--- Top 5 Products by Price ---")
                for product_id, product_name, price in cursor.fetchall():
                    print(product_id, product_name, price)

                # 2. Use a parameterized query
                category = "Electronics"

                cursor.execute(
                    """
                    SELECT product_name, price
                    FROM products
                    WHERE category = %s
                    ORDER BY price DESC;
                    """,
                    (category,),
                )

                print(f"\n--- Products in {category} ---")
                for product_name, price in cursor.fetchall():
                    print(product_name, price)

                # 3. Demonstrate a transaction using a read-only statement
                cursor.execute("SELECT COUNT(*) FROM products;")
                product_count = cursor.fetchone()[0]

                print(f"\nTotal products: {product_count}")

        print("\nSQL queries executed successfully.")

    except psycopg2.Error as error:
        print("Database query failed.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
