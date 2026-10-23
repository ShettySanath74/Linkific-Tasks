
import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    text,
)
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
DAY10_DIR = os.path.join(PROJECT_ROOT, "Day 10")

load_dotenv(os.path.join(DAY10_DIR, ".env"))

CSV_PATH = os.path.join(DAY10_DIR, "data", "customers_input.csv")
OUTPUT_DIR = os.path.join(DAY10_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

Base = declarative_base()


class PipelineCustomer(Base):
    __tablename__ = "day10_pipeline_customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    city = Column(String(100), nullable=False)


def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "ecommerce_db"),
    )
    return create_engine(url, pool_pre_ping=True)


def extract():
    print("1. EXTRACT: Reading CSV...")
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Input CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print(f"   Rows read: {len(df)}")
    return df


def transform(df):
    print("2. TRANSFORM: Cleaning and validating data...")

    required = ["first_name", "last_name", "email", "city"]
    missing_columns = set(required) - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df = df[required].copy()

    for column in required:
        df[column] = df[column].astype("string").str.strip()

    # Reject rows with missing or blank required fields.
    df = df.dropna(subset=required)
    for column in required:
        df = df[df[column] != ""]

    # Normalize emails and remove duplicate emails within the file.
    df["email"] = df["email"].str.lower()
    df = df.drop_duplicates(subset=["email"], keep="first")

    # Basic email-format validation.
    valid_email = df["email"].str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    rejected = df.loc[~valid_email].copy()
    df = df.loc[valid_email].copy()

    if not rejected.empty:
        rejected.to_csv(
            os.path.join(OUTPUT_DIR, "rejected_customers.csv"),
            index=False,
        )
        print(f"   Rejected invalid email rows: {len(rejected)}")

    print(f"   Valid rows: {len(df)}")
    return df


def load(df, engine):
    print("3. LOAD: Writing to PostgreSQL...")

    # Create only the dedicated Day 10 pipeline table.
    Base.metadata.create_all(engine)

    # Idempotent loading: skip emails already in the destination table.
    with engine.begin() as connection:
        existing_emails = set(
            connection.execute(
                text("SELECT email FROM day10_pipeline_customers")
            ).scalars().all()
        )

        new_rows = df.loc[~df["email"].isin(existing_emails)].copy()

        if not new_rows.empty:
            new_rows.to_sql(
                "day10_pipeline_customers",
                con=connection,
                if_exists="append",
                index=False,
                chunksize=500,
            )

    print(f"   New rows inserted: {len(new_rows)}")
    print(f"   Existing emails skipped: {len(df) - len(new_rows)}")


def main():
    engine = get_engine()
    try:
        df = extract()
        cleaned_df = transform(df)

        if cleaned_df.empty:
            print("No valid records to load.")
            return

        load(cleaned_df, engine)

        output_path = os.path.join(OUTPUT_DIR, "customers_cleaned.csv")
        cleaned_df.to_csv(output_path, index=False)

        print(f"\nCleaned data saved to: {output_path}")
        print("ETL pipeline completed successfully!")

    except Exception as error:
        print(f"\nETL pipeline failed: {error}")
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
