
import os
import logging
import requests
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
OUTPUT_DIR = os.path.join(DAY10_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

load_dotenv(os.path.join(DAY10_DIR, ".env"))

API_URL = "https://jsonplaceholder.typicode.com/posts"
TABLE_NAME = "day10_api_posts"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

Base = declarative_base()


class ApiPost(Base):
    __tablename__ = TABLE_NAME

    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    body = Column(String, nullable=False)


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
    logging.info("Extracting posts from API...")

    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()

    records = response.json()
    if not isinstance(records, list):
        raise ValueError("Expected the API to return a JSON list.")

    df = pd.DataFrame(records)

    required = ["id", "userId", "title", "body"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"API response is missing columns: {sorted(missing)}")

    df = df[required].copy()
    logging.info("Received %s records.", len(df))
    return df


def transform(df):
    logging.info("Transforming API records...")

    df = df.rename(
        columns={
            "id": "post_id",
            "userId": "user_id",
        }
    )

    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df["body"] = df["body"].fillna("").astype(str).str.strip()

    df["post_id"] = pd.to_numeric(df["post_id"], errors="coerce")
    df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce")
    df = df.dropna(subset=["post_id", "user_id"])

    df["post_id"] = df["post_id"].astype(int)
    df["user_id"] = df["user_id"].astype(int)

    df = df.drop_duplicates(subset=["post_id"])
    df = df[
        (df["post_id"] > 0)
        & (df["user_id"] > 0)
        & (df["title"] != "")
    ]

    logging.info("%s valid records after transformation.", len(df))
    return df


def load(df, engine):
    logging.info("Loading records into PostgreSQL...")

    # Creates only the dedicated API table, not your existing ecommerce tables.
    Base.metadata.create_all(engine)

    with engine.begin() as connection:
        existing_ids = set(
            connection.execute(
                text(f"SELECT post_id FROM {TABLE_NAME}")
            ).scalars().all()
        )

        new_df = df.loc[~df["post_id"].isin(existing_ids)].copy()

        if not new_df.empty:
            new_df.to_sql(
                TABLE_NAME,
                con=connection,
                if_exists="append",
                index=False,
                chunksize=100,
            )

    logging.info(
        "Inserted %s new records; skipped %s existing records.",
        len(new_df),
        len(df) - len(new_df),
    )


def main():
    engine = get_engine()

    try:
        raw_df = extract()
        cleaned_df = transform(raw_df)

        cleaned_df.to_csv(
            os.path.join(OUTPUT_DIR, "api_posts_cleaned.csv"),
            index=False,
        )

        if cleaned_df.empty:
            logging.warning("No valid records to load.")
            return

        load(cleaned_df, engine)
        logging.info("API-to-PostgreSQL pipeline completed successfully.")

    except (requests.RequestException, ValueError) as error:
        logging.error("API or data validation failure: %s", error)
        raise
    except Exception:
        logging.exception("Unexpected pipeline failure.")
        raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
