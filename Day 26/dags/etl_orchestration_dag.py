"""Airflow DAG: parallel extraction -> transform -> load -> quality checks."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from airflow import DAG
from airflow.decorators import task

# Make the Day 26 project root importable when this file is in Day 26/dags.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.extract import extract_customers, extract_sales
from scripts.transform import transform_records
from scripts.load import load_sales
from scripts.quality_check import run_quality_checks

CALLBACK_LOG = PROJECT_ROOT / "logs" / "airflow_callbacks.jsonl"
logger = logging.getLogger("day26.airflow_callbacks")


def _write_callback_event(event: dict) -> None:
    """Append a JSON event to the project callback log."""
    CALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CALLBACK_LOG.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, default=str) + "\n")


def task_success_callback(context: dict) -> None:
    ti = context.get("task_instance")
    _write_callback_event({
        "event": "task_success",
        "dag_id": context.get("dag").dag_id if context.get("dag") else None,
        "task_id": ti.task_id if ti else None,
        "run_id": context.get("run_id"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


def task_failure_callback(context: dict) -> None:
    ti = context.get("task_instance")
    exception = context.get("exception")
    event = {
        "event": "task_failure",
        "dag_id": context.get("dag").dag_id if context.get("dag") else None,
        "task_id": ti.task_id if ti else None,
        "run_id": context.get("run_id"),
        "error": str(exception) if exception else "Unknown task failure",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _write_callback_event(event)
    logger.error("Task failure callback: %s", event)


def dag_failure_callback(context: dict) -> None:
    dag_run = context.get("dag_run")
    event = {
        "event": "dag_failure",
        "dag_id": dag_run.dag_id if dag_run else None,
        "run_id": dag_run.run_id if dag_run else None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _write_callback_event(event)
    logger.error("DAG failure callback: %s", event)


default_args = {
    "owner": "linkific-intern",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "execution_timeout": timedelta(minutes=10),
    "on_failure_callback": task_failure_callback,
    "on_success_callback": task_success_callback,
}

with DAG(
    dag_id="linkific_day26_etl_orchestration",
    description="Scheduled ETL pipeline with monitoring and failure handling",
    default_args=default_args,
    start_date=datetime(2026, 11, 20, tzinfo=timezone.utc),
    schedule="0 2 * * *",  # Daily at 02:00 UTC
    catchup=False,
    max_active_runs=1,
    max_active_tasks=4,
    on_failure_callback=dag_failure_callback,
    tags=["linkific", "data-engineering", "etl", "monitoring"],
    doc_md="""
    ### Linkific Day 26 ETL orchestration
    Customer and sales extraction run in parallel. Their outputs feed the
    transformation task, followed by SQLite loading and data quality checks.
    Rejected records are written to the project's dead-letter CSV.
    """,
) as dag:

    @task
    def extract_customer_task() -> str:
        return extract_customers()

    @task
    def extract_sales_task() -> str:
        return extract_sales()

    @task
    def transform_task(customers_path: str, sales_path: str) -> str:
        return transform_records(customers_path, sales_path)

    @task
    def load_task(transformed_path: str) -> str:
        return load_sales(transformed_path)

    @task
    def quality_check_task(transformed_path: str, database_path: str) -> str:
        return run_quality_checks(transformed_path, database_path)

    customers_file = extract_customer_task()
    sales_file = extract_sales_task()
    transformed_file = transform_task(customers_file, sales_file)
    database_file = load_task(transformed_file)
    quality_check_task(transformed_file, database_file)
