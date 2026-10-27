import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="scheduled_learning_dag",
    description="Daily scheduled workflow for Airflow practice",
    schedule="30 4 * * *",
    start_date=pendulum.datetime(2026, 10, 27, tz="UTC"),
    catchup=False,
    tags=["day13", "scheduling", "learning"],
)
def scheduled_learning_dag():

    @task
    def show_schedule():
        print("Daily scheduled workflow executed successfully!")
        print("Timezone: UTC; scheduled time: 04:30 UTC (10:00 AM IST).")

    show_schedule()


scheduled_learning_dag()
