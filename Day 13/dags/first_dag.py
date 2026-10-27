
from datetime import datetime

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="first_learning_dag",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["day13", "learning"],
)
def first_learning_dag():

    @task
    def say_hello():
        print("Hello! My first Apache Airflow DAG is running.")
        print(f"Execution time: {datetime.now().isoformat()}")

    say_hello()


first_learning_dag()
