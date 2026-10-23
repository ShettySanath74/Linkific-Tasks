
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

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
    output_dir = os.path.join(PROJECT_ROOT, "Day 10", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 1. Read SQL query results into a DataFrame
        with get_connection() as connection:
            query = """
                SELECT product_id, product_name, category, price,
                       stock_quantity
                FROM products
                ORDER BY price DESC;
            """

            df = pd.read_sql_query(query, connection)

        print("\n--- Products DataFrame ---")
        print(df.head())

        # 2. Perform simple analysis
        print("\n--- Summary Statistics ---")
        print(df["price"].describe())

        print("\n--- Average Price by Category ---")
        print(
            df.groupby("category")["price"]
            .mean()
            .sort_values(ascending=False)
        )

        # 3. Export DataFrame to CSV
        csv_path = os.path.join(output_dir, "products_analysis.csv")
        df.to_csv(csv_path, index=False)
        print(f"\nCSV saved to: {csv_path}")

        # 4. Demonstrate chunk processing
        print("\n--- Chunk Processing ---")
        with get_connection() as connection:
            chunks = pd.read_sql_query(
                query,
                connection,
                chunksize=3,
            )

            for chunk_number, chunk in enumerate(chunks, start=1):
                print(f"Chunk {chunk_number}: {len(chunk)} rows")

        print("\nPandas database analysis completed.")

    except Exception as error:
        print(f"Pipeline failed: {error}")


if __name__ == "__main__":
    main()
