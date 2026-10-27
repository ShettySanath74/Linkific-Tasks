from datetime import timedelta

import pendulum
from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator

PROJECT_DIR = "/mnt/c/Users/Comp/Linkific-Tasks-Upload/Day 12"
PYTHON = "/home/comp/airflow-project/.venv-etl/bin/python"


@dag(
    dag_id="day12_etl_pipeline",
    description="Orchestrate the Day 12 ETL pipeline",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    default_args={
        "owner": "linkific-intern",
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["day13", "etl", "day12"],
)
def day12_etl_pipeline():
    extract_api = BashOperator(
        task_id="extract_api",
        bash_command=f'cd "{PROJECT_DIR}" && "{PYTHON}" scripts/01_extract_api.py',
    )

    extract_files = BashOperator(
        task_id="extract_files",
        bash_command=f'cd "{PROJECT_DIR}" && "{PYTHON}" scripts/02_extract_files.py',
    )

    extract_database = BashOperator(
        task_id="extract_database",
        bash_command=f'cd "{PROJECT_DIR}" && "{PYTHON}" scripts/03_extract_database.py',
    )

    transform = BashOperator(
        task_id="transform_data",
        bash_command=f'cd "{PROJECT_DIR}" && "{PYTHON}" scripts/04_transform_data.py',
    )

    load = BashOperator(
        task_id="load_warehouse",
        bash_command=f'cd "{PROJECT_DIR}" && "{PYTHON}" scripts/05_load_warehouse.py',
    )

    validate = BashOperator(
        task_id="validate_warehouse",
        bash_command=f'cd "{PROJECT_DIR}" && "{PYTHON}" scripts/08_validate_warehouse.py',
    )

    [extract_api, extract_files, extract_database] >> transform >> load >> validate


day12_etl_pipeline()
