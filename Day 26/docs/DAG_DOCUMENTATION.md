# DAG Technical Documentation

## DAG identity
- DAG ID: `linkific_day26_etl_orchestration`
- Schedule: `0 2 * * *` (daily at 02:00 UTC)
- Catchup: disabled
- Maximum active DAG runs: 1
- Maximum active tasks for this DAG: 4

## Tasks and dependencies

| Task ID | Responsibility | Upstream dependency |
|---|---|---|
| `extract_customer_task` | Extract customers CSV to JSON | None |
| `extract_sales_task` | Extract sales CSV to JSON | None |
| `transform_task` | Enrich sales, validate rows, create accepted and dead-letter files | Both extraction tasks |
| `load_task` | Upsert accepted sales into SQLite | Transform |
| `quality_check_task` | Validate loaded data | Load and transform |

The two extraction tasks can run in parallel because neither depends on the other's output.

## Data locations
- Source: `data/source/customers.csv`, `data/source/sales.csv`
- Extracted: `outputs/extracted/`
- Accepted transformed records: `outputs/transformed/accepted_sales.csv`
- Rejected records: `data/dead_letter/rejected_sales.csv`
- Warehouse: `outputs/warehouse.db`
- Quality report: `outputs/quality_report.json`
- Application log: `logs/pipeline.log`
- Callback event log: `logs/airflow_callbacks.jsonl`

## Transformation and dead-letter behavior
A sales record is rejected when its sale ID is missing or duplicated, its customer reference does not exist, its amount is nonnumeric or not positive, or its date is not in `YYYY-MM-DD` format. Rejected rows include a reason and are written to the dead-letter CSV. Accepted rows are enriched with customer name and city.

## Loading
The SQLite `sales` table uses `sale_id` as its primary key. The load uses an upsert so rerunning the same sample data does not create duplicate sale IDs.

## Data quality checks
- Current transformed batch row count equals the warehouse row count.
- No duplicate sale IDs exist.
- No non-positive amounts exist.
- Customer IDs are present.

The sample is designed for a clean first run. If the database is reused after source data changes, the batch-vs-total row-count check may need to be changed to a batch/run identifier model.

## Retries and callbacks
Every task has two retries with a two-minute delay and a ten-minute execution timeout. Task success/failure callbacks append JSON events to `logs/airflow_callbacks.jsonl`. A DAG failure callback records DAG-level failure. Airflow UI task logs remain the primary detailed execution logs.

## Monitoring and alerts
The Airflow UI provides task state, duration, graph view, and task logs. The callback JSONL file records success/failure events. External email or chat delivery is not enabled; configure an Airflow notification integration or callback transport before describing external alerting as active.

## Operational note
The project uses local filesystem paths and SQLite. All Airflow components/workers executing this DAG must have access to the same project files. For distributed execution, replace local files with shared/object storage and SQLite with a server database.
