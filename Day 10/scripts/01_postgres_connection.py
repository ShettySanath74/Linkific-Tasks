
import os

import psycopg2
from dotenv import load_dotenv

# Load environment variables from Day 10/.env
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
ENV_FILE = os.path.join(PROJECT_ROOT, "Day 10", ".env")

load_dotenv(ENV_FILE)


def get_connection():
    """Create and return a PostgreSQL database connection."""
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
                cursor.execute(
                    "SELECT current_database(), current_user, version();"
                )
                database, username, version = cursor.fetchone()

                print("Database connection successful!")
                print(f"Database: {database}")
                print(f"User: {username}")
                print(f"PostgreSQL version: {version}")

    except psycopg2.Error as error:
        print("Database connection failed.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
