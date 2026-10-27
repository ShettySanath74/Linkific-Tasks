import pendulum
from airflow.sdk import dag
from airflow.providers.standard.operators.python import PythonOperator


def extract_data():
    data = [100, 200, 300, 400, 500]
    print(f"Extracted data: {data}")
    return data


def transform_data():
    values = [100, 200, 300, 400, 500]
    total = sum(values)
    print(f"Transformed data total: {total}")
    return total


def load_data():
    print("Data loading task completed successfully.")


@dag(
    dag_id="python_operator_learning_dag",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["day13", "python", "learning"],
)
def python_operator_learning_dag():

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    extract >> transform >> load


python_operator_learning_dag()
