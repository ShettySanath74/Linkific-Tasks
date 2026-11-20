# Day 26 – Apache Airflow DAG Orchestration

## Project overview
This project demonstrates a scheduled ETL pipeline orchestrated by Apache Airflow. It extracts customer and sales data in parallel, transforms and validates the records, loads accepted records into SQLite, and runs post-load quality checks.

**Implementation status:** Source code and sample data are prepared. The project has not yet been installed, executed, or tested in an Airflow environment. Execution results must be added only after running the pipeline.

## Objectives
- Define an Airflow DAG and task dependencies.
- Schedule automated pipeline execution.
- Monitor task and DAG success/failure through callbacks and logs.
- Retry transient failures and route rejected records to a dead-letter CSV.
- Demonstrate parallel extraction and basic resource/concurrency controls.
- Document the workflow and operational behavior.

## Technologies
- Python 3.10+ recommended for the Airflow environment (use the Python version supported by the selected Airflow release).
- Apache Airflow 2.4+ or a compatible Airflow 3 release using the stable `airflow.decorators` API.
- SQLite and Python standard-library modules (`csv`, `json`, `sqlite3`, `logging`, `datetime`, `pathlib`).

The ETL scripts use only the Python standard library. Apache Airflow is the orchestration dependency and should be installed separately using the official installation instructions and matching constraints for your Python version.

## Folder structure
```text
Day 26/
├── README.md
├── requirements.txt
├── dags/
│   └── etl_orchestration_dag.py
├── scripts/
│   ├── __init__.py
│   ├── common.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── quality_check.py
├── data/
│   └── source/
│       ├── customers.csv
│       └── sales.csv
├── outputs/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
└── docs/
    └── DAG_DOCUMENTATION.md
```

## Workflow
1. `extract_customers` and `extract_sales` run in parallel.
2. `transform_data` waits for both extraction tasks, enriches sales with customer details, and separates rejected rows.
3. `load_data` upserts accepted records into SQLite.
4. `quality_check` validates the loaded row count, unique sale IDs, positive amounts, and customer references.

```text
extract_customers ─┐
                   ├─> transform_data -> load_data -> quality_check
extract_sales ─────┘
```

## Installation and setup
1. Use a supported Linux environment for Airflow, such as WSL2 or Docker. Airflow is not natively supported as a production installation on Windows.
2. Install an Airflow version compatible with the Python version in that environment. Follow the official Airflow installation guide and use its matching constraints file:
   https://airflow.apache.org/docs/apache-airflow/stable/installation/
3. Copy this complete `Day 26` folder into the Airflow environment.
4. Configure the Airflow DAGs folder to include `Day 26/dags`, or copy `etl_orchestration_dag.py` into the configured DAGs folder while keeping the sibling `scripts` directory available at the project root.
5. Initialize and start Airflow using the commands appropriate for the installed Airflow version and executor. Do not run these commands until the environment is confirmed.

`requirements.txt` intentionally does not pin or install Airflow. Airflow has version-specific dependency constraints and should not be installed with an unconstrained generic `pip install apache-airflow`.

## Schedule
The DAG is configured with `0 2 * * *`, which means daily at 02:00 UTC. Change the cron expression and timezone deliberately if a different local schedule is required. `catchup=False` prevents automatic backfilling of all historical dates.

## Monitoring and failure handling
- Python logging writes application events to `Day 26/logs/pipeline.log`.
- Airflow's own task logs remain available through the Airflow UI/log backend.
- Task success and failure callbacks write structured JSON events to `Day 26/logs/airflow_callbacks.jsonl`.
- Each task is configured for two retries with a two-minute delay.
- A DAG-level failure callback records DAG failures.
- Rejected records are written to `Day 26/data/dead_letter/rejected_sales.csv`.
- Airflow task duration and state can be inspected in the Airflow UI. Callback logs include task/DAG identity and timestamps.
- Email/SMS/chat alerts are not enabled by default. They require configuring an alerting backend or Airflow connection/notification integration.

## Optimization choices
- Customer and sales extraction are independent and therefore run in parallel.
- `max_active_runs=1` prevents overlapping DAG runs that could compete over the same local output files.
- `max_active_tasks=4` caps concurrent task execution for this DAG.
- A ten-minute task execution timeout prevents a task from running indefinitely.
- SQLite is used to keep the demonstration self-contained; a production workload may use PostgreSQL or a warehouse.

## Execution and verification
After Airflow is installed and configured:
1. Confirm the DAG appears in the Airflow UI and has no import errors.
2. Trigger a manual run.
3. Confirm the two extraction tasks run independently, then the transform, load, and quality tasks run in dependency order.
4. Inspect task logs and callback JSONL events.
5. Inspect `outputs/warehouse.db` and the dead-letter CSV.
6. Confirm the quality task succeeds and reports matching expected/actual record counts.

The exact commands depend on the Airflow version and executor selected. We will add the tested commands and actual run results after environment inspection.

## Limitations and future improvements
- Sample data is local CSV and is intended for learning.
- The local SQLite database and output paths assume a shared filesystem visible to Airflow workers. Distributed workers require shared storage or remote object storage.
- The callbacks log events but do not send external notifications until an alerting backend is configured.
- The demo uses a simple daily UTC schedule; production schedules should use an explicitly selected business timezone.
- Future improvements: PostgreSQL target, remote storage, data lineage, metrics export, external alerting, secrets management, and integration tests.
