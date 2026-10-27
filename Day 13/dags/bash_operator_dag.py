import pendulum
from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator


@dag(
    dag_id="bash_operator_learning_dag",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["day13", "bash", "learning"],
)
def bash_operator_learning_dag():

    task1 = BashOperator(
        task_id="print_message",
        bash_command="echo 'Hello from BashOperator!'",
    )

    task2 = BashOperator(
        task_id="show_date",
        bash_command="date",
    )

    task3 = BashOperator(
        task_id="show_python_version",
        bash_command="python --version",
    )

    task1 >> task2 >> task3


bash_operator_learning_dag()
