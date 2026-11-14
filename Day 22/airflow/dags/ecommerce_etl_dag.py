"""
Apache Airflow DAG starter template.

This DAG demonstrates orchestration structure only. Replace the placeholder
callables with the project's real ingestion, transformation, and load modules,
and configure Airflow in WSL2/Docker before enabling the DAG.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

def extract_data():
    print("TODO: Extract product, customer, order, and inventory source data.")

def transform_and_validate():
    print("TODO: Clean, standardize, and validate staged records.")

def load_warehouse():
    print("TODO: Upsert dimensions and load fact tables into PostgreSQL.")

with DAG(
    dag_id="ecommerce_analytics_etl",
    description="Starter orchestration workflow for the e-commerce analytics platform",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "owner": "data-engineering",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["ecommerce", "etl", "warehouse"],
) as dag:
    extract = PythonOperator(task_id="extract_sources", python_callable=extract_data)
    transform = PythonOperator(task_id="transform_and_validate", python_callable=transform_and_validate)
    load = PythonOperator(task_id="load_postgresql_warehouse", python_callable=load_warehouse)

    extract >> transform >> load
