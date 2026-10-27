# Day 13 — Apache Airflow

## Objectives
- Set up Apache Airflow using Ubuntu on WSL.
- Learn DAGs, tasks, operators, and dependencies.
- Create and test TaskFlow, BashOperator, and PythonOperator DAGs.
- Orchestrate the Day 12 ETL pipeline.
- Practise scheduled workflow execution.

## DAG Files
- `dags/first_dag.py` — introductory TaskFlow DAG.
- `dags/bash_operator_dag.py` — BashOperator practice.
- `dags/python_operator_dag.py` — PythonOperator practice.
- `dags/day12_etl_pipeline_dag.py` — ETL orchestration.
- `dags/scheduled_learning_dag.py` — scheduled workflow practice.

## Environment
- Apache Airflow running through WSL Ubuntu.
- Python virtual environment for ETL dependencies.
- Pandas and Requests installed for the ETL project.

## Validation
The DAGs were registered in Airflow. The scheduled learning DAG was reported as running successfully. Record the final ETL validation results after confirming the latest run in the Airflow UI.

## Notes
Airflow was configured locally for learning and development.
